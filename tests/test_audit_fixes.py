from contextlib import asynccontextmanager

import pytest
import agntid
from fastapi.testclient import TestClient

from server.agntid_runtime import AgntIDRuntime, RuntimeUnavailable
from server import app as appmod


@pytest.mark.asyncio
async def test_discovery_error_closes_and_records_task(monkeypatch):
    closed, evidence = [], []
    class Client:
        def __init__(self, *args, **kwargs): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *args): return False
    async def discovery(client): raise ConnectionError("discovery failed")
    @asynccontextmanager
    async def context(client, task_id):
        try: yield
        finally: closed.append(task_id)
    monkeypatch.setenv("AGNTID_MCP_URL", "http://localhost:8082/mcp")
    monkeypatch.setenv("AGNTID_AGENT_ID", "synthetic")
    monkeypatch.setenv("AGNTID_USER_ID", "night-float")
    monkeypatch.setenv("ENABLE_LIVE_EXECUTION", "true")
    monkeypatch.setattr(agntid, "AgntidMCPClient", Client)
    monkeypatch.setattr(agntid, "get_tools_list", discovery)
    monkeypatch.setattr(agntid, "task_context", context)
    async def cb(*args): evidence.append(args)
    runtime = AgntIDRuntime()
    assert runtime.status()["status"] == "configured_unverified"
    assert runtime.status()["reachable"] is None
    with pytest.raises(RuntimeUnavailable):
        await runtime.run_actions("draft only", [], cb)
    assert len(closed) == 1
    assert evidence[0][4]["task_id"] == closed[0]
    assert evidence[0][4]["event_kind"] == "task_lifecycle"
    assert evidence[0][4]["execution_status"] == "not_attempted"


def test_public_caller_cannot_use_live_identity(monkeypatch):
    monkeypatch.setattr(appmod.runtime_adapter, "status", lambda: {"live_enabled": True})
    response = TestClient(appmod.app).post("/api/runs", json={"mode": "live", "scenario": "safe"})
    assert response.status_code == 403
    assert "local-operator" in response.json()["detail"]


def test_exported_ledger_event_hash_is_valid():
    from server.ledger import Ledger
    ledger = Ledger()
    ledger.add("example", {"tool": "get_patient", "decision": "allow"})
    event = ledger.recent()[0]
    assert event["hash"] == ledger.event_hash(event)
