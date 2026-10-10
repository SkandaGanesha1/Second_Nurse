"""Attempt all user-provided public URLs; retrieval is not exhaustive deep reading."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import ipaddress
import json
import re
import socket
import time
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

MAX_BYTES = 120_000
CONCURRENCY = 24


async def public_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.username or parsed.password:
        return False
    if not parsed.hostname or parsed.port not in {None, 80, 443}:
        return False
    try:
        addresses = await asyncio.get_running_loop().getaddrinfo(parsed.hostname, None)
        return all(ipaddress.ip_address(row[4][0]).is_global for row in addresses)
    except (socket.gaierror, ValueError):
        return False


async def retrieve(row: dict, client: httpx.AsyncClient, output: Path, index: int, hosts: dict) -> dict:
    started = time.monotonic()
    result = {**row, "id": f"source-{index:04d}", "status": "failed", "bytes_captured": 0,
              "truncated": False, "http_status": None, "final_url": row["url"],
              "title": "", "error": None, "deep_reviewed": False}
    host = urlparse(row["url"]).hostname or "invalid"
    semaphore = hosts.setdefault(host, asyncio.Semaphore(2))
    async with semaphore:
        try:
            current = row["url"]
            for _ in range(6):
                if not await public_url(current):
                    raise ValueError("URL is not a resolvable public HTTP(S) endpoint")
                async with client.stream("GET", current) as response:
                    result["http_status"] = response.status_code
                    result["final_url"] = str(response.url)
                    result["content_type"] = response.headers.get("content-type", "")
                    if response.is_redirect:
                        location = response.headers.get("location")
                        if not location:
                            raise ValueError("Redirect has no destination")
                        current = urljoin(str(response.url), location)
                        continue
                    chunks = bytearray()
                    async for chunk in response.aiter_bytes():
                        if len(chunks) + len(chunk) > MAX_BYTES:
                            chunks.extend(chunk[:MAX_BYTES - len(chunks)])
                            result["truncated"] = True
                            break
                        chunks.extend(chunk)
                    result["bytes_captured"] = len(chunks)
                    result["sha256"] = hashlib.sha256(chunks).hexdigest()
                    if "text" in result["content_type"] or "json" in result["content_type"] or "xml" in result["content_type"]:
                        text = bytes(chunks).decode(response.encoding or "utf-8", errors="replace")
                        if "html" in result["content_type"]:
                            soup = BeautifulSoup(text, "html.parser")
                            result["title"] = soup.title.get_text(" ", strip=True)[:300] if soup.title else ""
                            for tag in soup(["script", "style", "nav", "footer"]):
                                tag.decompose()
                            text = soup.get_text("\n", strip=True)
                        path = output / "snapshots" / f"{index:04d}.txt"
                        path.write_text(text)
                        result["snapshot_path"] = f"snapshots/{index:04d}.txt"
                        result["excerpt"] = re.sub(r"\s+", " ", text)[:500]
                    result["status"] = "retrieved" if 200 <= response.status_code < 300 else "http_error"
                    if result["status"] != "retrieved":
                        result["error"] = f"HTTP {response.status_code}"
                    break
            else:
                raise ValueError("Redirect limit exceeded")
        except Exception as error:
            result["error"] = f"{type(error).__name__}: {str(error)[:180]}"
    result["elapsed_ms"] = round((time.monotonic() - started) * 1000)
    return result


async def main(args: argparse.Namespace) -> None:
    output = Path(args.output)
    (output / "snapshots").mkdir(parents=True, exist_ok=True)
    rows = json.loads(Path(args.inventory).read_text())
    semaphore = asyncio.Semaphore(CONCURRENCY)
    hosts: dict = {}
    completed: list = []
    started = time.monotonic()
    async with httpx.AsyncClient(timeout=httpx.Timeout(12, connect=6), follow_redirects=False,
                                headers={"User-Agent": "SecondNurseResearch/1.0 (public source inventory; bounded single-page retrieval)"},
                                limits=httpx.Limits(max_connections=CONCURRENCY, max_keepalive_connections=12)) as client:
        async def one(index: int, row: dict) -> dict:
            async with semaphore:
                try:
                    result = await asyncio.wait_for(retrieve(row, client, output, index, hosts), timeout=32)
                except asyncio.TimeoutError:
                    result = {**row, "id": f"source-{index:04d}", "status": "failed", "error": "Overall 32-second URL timeout", "deep_reviewed": False}
                completed.append(result)
                if len(completed) % 50 == 0 or len(completed) == len(rows):
                    counts = Counter(r["status"] for r in completed)
                    print(f"Sources {len(completed)}/{len(rows)} | {dict(counts)} | elapsed {round(time.monotonic()-started)}s", flush=True)
                    (output / "coverage-progress.json").write_text(json.dumps({"attempted": len(completed), "total": len(rows), "counts": dict(counts)}))
                return result
        results = await asyncio.gather(*(one(index, row) for index, row in enumerate(rows, 1)))
    (output / "source-coverage.json").write_text(json.dumps(results, indent=2) + "\n")
    counts = Counter(r["status"] for r in results)
    summary = {"total_unique_urls": len(rows), "attempted": len(results), "counts": dict(counts),
               "byte_cap_per_url": MAX_BYTES, "elapsed_seconds": round(time.monotonic()-started),
               "method": "Bounded public landing-page HTTP retrieval, up to five redirects, no recursive crawling.",
               "limitations": "Retrieved does not imply full article reading. Some pages require scripts, login, or reject automated access. Snapshots may be truncated. Deep-research verification is separately recorded."}
    (output / "coverage-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--output", required=True)
    asyncio.run(main(parser.parse_args()))
