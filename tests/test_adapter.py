from contextlib import asynccontextmanager
from types import SimpleNamespace

import pytest
import agntid
from agntid.intent import TaskOpenResult, TaskIntentSnapshot

from server.agntid_runtime import AgntIDRuntime, RuntimeUnavailable


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["rejected", "missing_snapshot", "empty", "application_error", "transport_error", "signature_without_draft"])
async def test_fail_closed_real_filter_and_wrapper(monkeypatch, kind):
    called, closed, events = [], [], []
    class Client:
        def __init__(self, *args, **kwargs):
            pass
        async def __aenter__(self):
            return self
        async def __aexit__(self, *args):
            return False
        async def call_tool_async(self, name, args):
            called.append((name, args))
            if kind == "transport_error":
                raise TimeoutError("timeout")
            return {"ok": False, "error": "ABO mismatch"} if kind == "application_error" else {"ok": True, "draft_id": 7}
    @asynccontextmanager
    async def task_context(client, task_id):
        try:
            yield
        finally:
            closed.append(task_id)
    async def visible(client):
        return [SimpleNamespace(name="ward.draft_heparin"), SimpleNamespace(name="ward.sign_order")]
    async def opening(*args):
        if kind == "rejected":
            return TaskOpenResult(ok=False, reason="not authorized")
        if kind == "missing_snapshot":
            return TaskOpenResult(ok=True)
        names = () if kind == "empty" else ("ward.draft_heparin", "ward.sign_order")
        return TaskOpenResult(ok=True, intent_prepared=True, snapshot=TaskIntentSnapshot(relevant_tool_names=names))
    monkeypatch.setattr(agntid, "AgntidMCPClient", Client)
    monkeypatch.setattr(agntid, "get_tools_list", visible)
    monkeypatch.setattr(agntid, "send_task_open_details", opening)
    monkeypatch.setattr(agntid, "task_context", task_context)
    monkeypatch.setenv("AGNTID_MCP_URL", "http://localhost:8082/mcp")
    monkeypatch.setenv("ENABLE_LIVE_EXECUTION", "true")
    monkeypatch.setenv("AGNTID_AGENT_ID", "second-nurse")
    monkeypatch.setenv("AGNTID_USER_ID", "synthetic")
    async def cb(*event):
        events.append(event)
    actions = [{"tool": "draft_heparin", "args": {"mrn": 1042, "units": 1000, "route_code": 1}}]
    if kind == "signature_without_draft":
        actions = [{"tool": "sign_order", "args": {"draft_id": 1}}]
    runtime = AgntIDRuntime()
    if kind in {"rejected", "missing_snapshot"}:
        with pytest.raises(RuntimeUnavailable):
            await runtime.run_actions("Draft only", actions, cb)
        assert not called
    else:
        await runtime.run_actions("Draft only", actions, cb)
        if kind in {"empty", "signature_without_draft"}:
            assert not called
        if kind == "empty":
            assert events[0][1] == "deny" and "client shortlist" in events[0][2]
        if kind == "application_error":
            assert events[0][1] == "error" and events[0][3] is True
        if kind == "transport_error":
            assert events[0][1] == "error" and events[0][4]["execution_status"] == "unknown"
        if called:
            assert called[0][1].get("_task_id")
    assert len(closed) == 1
