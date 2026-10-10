#!/usr/bin/env python3
"""Local integration scorecard: runtime check + optional live scenario runs."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("TEST_BASE_URL", "http://localhost:3000").rstrip("/")


def call(method: str, path: str, body: dict | None = None, timeout: float = 60) -> tuple[int, dict]:
    data = None
    headers = {"Content-Type": "application/json", "Host": "localhost:3000"}
    if body is not None:
        data = json.dumps(body).encode()
    req = urllib.request.Request(f"{BASE}{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode()
        try:
            detail = json.loads(payload)
        except json.JSONDecodeError:
            detail = {"detail": payload}
        return exc.code, detail


def main() -> int:
    ok = True
    checks: list[str] = []

    code, health = call("GET", "/health")
    checks.append(f"[{'OK' if code == 200 else 'FAIL'}] GET /health ({code})")
    ok &= code == 200

    code, boot = call("GET", "/api/bootstrap")
    live = boot.get("runtime", {}).get("live_enabled") if code == 200 else False
    checks.append(f"[{'OK' if code == 200 else 'FAIL'}] bootstrap live_enabled={live}")
    ok &= code == 200

    code, runtime = call("POST", "/api/runtime/check", {})
    reachable = runtime.get("reachable") if code == 200 else None
    tools = runtime.get("tool_count")
    checks.append(
        f"[{'OK' if code == 200 and reachable else 'WARN' if code == 200 else 'FAIL'}] "
        f"runtime check reachable={reachable} tool_count={tools}"
    )
    if not live:
        checks.append("[SKIP] live scenarios (ENABLE_LIVE_EXECUTION not set on server)")
        print("\n".join(checks))
        return 0 if ok else 1

    for scenario in ("safe", "dose", "signature"):
        code, run = call(
            "POST",
            "/api/runs",
            {"mode": "live", "scenario": scenario, "mrn": 1042, "prompt": f"Smoke {scenario}"},
        )
        status = run.get("status") if isinstance(run, dict) else None
        events = run.get("events", []) if isinstance(run, dict) else []
        allowed = sum(1 for e in events if e.get("decision") == "allow")
        denied = sum(1 for e in events if e.get("decision") == "deny")
        checks.append(
            f"[{'OK' if code == 200 else 'FAIL'}] live/{scenario} http={code} status={status} allow={allowed} deny={denied} task_id={run.get('task_id') if isinstance(run, dict) else None}"
        )
        ok &= code == 200

    print("\n".join(checks))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
