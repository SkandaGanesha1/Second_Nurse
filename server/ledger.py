from __future__ import annotations
import hashlib, json
from copy import deepcopy
from typing import Any

class Ledger:
    def __init__(self) -> None:
        self.runs: dict[str, dict[str, Any]] = {}
        self.events: list[dict[str, Any]] = []
    @staticmethod
    def event_hash(event: dict[str, Any]) -> str:
        body = {k: v for k, v in event.items() if k != "hash"}
        return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()
    def add(self, run_id: str, event: dict[str, Any]) -> dict[str, Any]:
        prior = self.runs.get(run_id, {}).get("events", [])
        event = deepcopy(event)
        event["run_id"] = run_id
        event["prev_hash"] = prior[-1]["hash"] if prior else None
        event["hash"] = self.event_hash(event)
        self.runs.setdefault(run_id, {"events": []})["events"].append(event)
        self.events.append(event)
        if len(self.events) > 2000:
            del self.events[:-2000]
        while len(self.runs) > 100:
            self.runs.pop(next(iter(self.runs)))
        return event
    def verify(self, run_id: str) -> bool:
        events = self.runs.get(run_id, {}).get("events", [])
        previous = None
        for event in events:
            if event.get("prev_hash") != previous or event.get("hash") != self.event_hash(event): return False
            previous = event["hash"]
        return True
    def recent(self, limit: int = 500) -> list[dict[str, Any]]:
        return deepcopy(self.events[-limit:])
