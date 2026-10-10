from __future__ import annotations
import os
from copy import deepcopy
from contextlib import asynccontextmanager
from types import SimpleNamespace
import pytest
from fastapi.testclient import TestClient
from ward.data import new_store, use_store
from ward import tools
from server.ledger import Ledger
from server import app as appmod
from server.agntid_runtime import AgntIDRuntime

@pytest.fixture(autouse=True)
def clean_runs():
    appmod.RUNS.clear(); appmod.ledger.runs.clear(); appmod.ledger.events.clear()
    yield
    appmod.RUNS.clear()

def test_raw_side_effects_and_no_dose_check():
    store = new_store()
    with use_store(store):
        assert tools.draft_heparin(1042, 10000, 1)["ok"]
        assert tools.sign_order(1)["ok"]
        assert tools.message_family(1042, "hello https://evil.example/x")["ok"]
    assert len(store.signed) == 1 and len(store.messages) == 1

def test_abo_mismatch_never_appends():
    store = new_store()
    with use_store(store):
        result = tools.draft_transfusion(1042, "U-88", 280)
    assert result["ok"] is False and "ABO mismatch" in result["error"]
    assert store.drafts == []

def test_run_state_isolation():
    c = TestClient(appmod.app)
    one = c.post("/api/runs", json={"mode":"before","scenario":"dose"}).json()
    two = c.post("/api/runs", json={"mode":"before","scenario":"safe"}).json()
    assert one["state"]["drafts"][0]["units"] == 10000
    assert all(d.get("units") != 10000 for d in two["state"]["drafts"])

def test_reference_never_calls_tools(monkeypatch):
    def fail(**kwargs): raise AssertionError("reference called raw tool")
    monkeypatch.setitem(tools.TOOLS, "draft_heparin", fail)
    result = TestClient(appmod.app).post("/api/runs", json={"mode":"reference","scenario":"safe"})
    assert result.status_code == 200
    body = result.json(); assert body["state"] == {"drafts":[],"signed":[],"messages":[],"discarded":[]}
    assert all(not e["executed"] and "Illustrative reference; not AgntID evidence" in e["reason"] for e in body["events"])

def test_invalid_input_and_unknown_scenario():
    c = TestClient(appmod.app)
    assert c.post("/api/runs", json={"mode":"before","scenario":"nope"}).status_code == 422
    assert c.post("/api/runs", json={"mode":"before","scenario":"safe","mrn":9999}).status_code == 422
    assert c.post("/api/runs", json={"mode":"before","scenario":"safe","prompt":"x"*4001}).status_code == 422

def test_live_unavailable_does_not_fallback(monkeypatch):
    monkeypatch.delenv("AGNTID_MCP_URL", raising=False); monkeypatch.delenv("ENABLE_LIVE_EXECUTION", raising=False)
    response = TestClient(appmod.app).post("/api/runs", json={"mode":"live","scenario":"safe"})
    assert response.status_code == 503

def test_ledger_mutation_detected():
    ledger = Ledger(); event = ledger.add("r", {"tool":"get_patient","args":{},"decision":"allow"})
    assert ledger.verify("r")
    event["decision"] = "deny"
    assert not ledger.verify("r")

def test_bootstrap_contract_and_research():
    c = TestClient(appmod.app); boot = c.get("/api/bootstrap").json()
    assert boot["pack_version"] == "1.0.0"
    assert {p["mrn"] for p in boot["patients"]} == {1042,1108,2201,3310}
    assert len(boot["tools"]) == 9 and len(boot["policies"]) == 3
    research = c.get("/api/research").json(); assert "coverage" in research and "sources" in research

def test_mcp_discovery_and_http_auth():
    from ward.server import mcp
    assert set(mcp._tool_manager._tools) == {"list_patients","get_patient","get_unit","get_chart_note","draft_transfusion","draft_heparin","sign_order","discard_unit","message_family"}
    c = TestClient(appmod.app)
    os.environ.pop("WARD_MCP_TOKEN", None)
    assert c.get("/mcp", follow_redirects=True).status_code == 503
    os.environ["WARD_MCP_TOKEN"] = "test-token"
    assert c.get("/mcp", headers={"Authorization":"Bearer wrong"}, follow_redirects=True).status_code == 401
    os.environ.pop("WARD_MCP_TOKEN", None)

def test_export_and_audit():
    c = TestClient(appmod.app); body = c.post("/api/runs", json={"mode":"before","scenario":"safe"}).json()
    assert c.get("/api/runs").json()["runs"][0]["id"] == body["id"]
    exported = c.get(f"/api/runs/{body['id']}/export")
    assert exported.status_code == 200 and "attachment" in exported.headers["content-disposition"]
    assert len(c.get("/api/audit").json()["events"]) == len(body["events"])

@pytest.mark.asyncio
async def test_mocked_official_sdk_lifecycle_denial_and_close(monkeypatch):
    import agntid
    calls = []; closed = []
    class Client:
        def __init__(self, url, access_token=None): calls.append(("client", url, access_token))
        async def __aenter__(self): return self
        async def __aexit__(self, *exc): calls.append(("client_exit",)); return False
    class Wrapped:
        async def call_tool_async(self, name, args):
            calls.append(("call", name, dict(args)))
            if name.endswith("draft_heparin"): return {"ok":True,"draft_id":42}
            return SimpleNamespace(denied=True, message="execute class denied")
    @asynccontextmanager
    async def task_context(client, task_id):
        calls.append(("open_context", task_id))
        try: yield
        finally: closed.append(task_id)
    monkeypatch.setattr(agntid, "AgntidMCPClient", Client)
    monkeypatch.setattr(agntid, "create_task", lambda *args: "task-1")
    monkeypatch.setattr(agntid, "get_tools_list", lambda client: _awaitable([SimpleNamespace(name="ward.draft_heparin"), SimpleNamespace(name="ward.sign_order")]))
    monkeypatch.setattr(agntid, "send_task_open_details", lambda *args: _awaitable(SimpleNamespace(ok=True, reason="accepted")))
    monkeypatch.setattr(agntid, "filter_tools_for_task", lambda visible, opened: visible)
    monkeypatch.setattr(agntid, "task_context", task_context)
    monkeypatch.setattr(agntid, "wrap_client", lambda client, task_id: Wrapped())
    monkeypatch.setenv("AGNTID_MCP_URL", "http://runtime")
    monkeypatch.setenv("ENABLE_LIVE_EXECUTION", "true")
    monkeypatch.setenv("TRUSTED_AGNTID_AGENT_ID", "agent")
    monkeypatch.setenv("TRUSTED_AGNTID_USER_ID", "user")
    runtime = AgntIDRuntime(); observed=[]
    async def cb(*args): observed.append(args)
    task = await runtime.run_actions("prepare", [{"tool":"draft_heparin","args":{"mrn":1042,"units":1000,"route_code":1}},{"tool":"sign_order","args":{"draft_id":1}}], cb)
    assert task == "task-1" and closed == ["task-1"]
    assert calls[-2][0] == "call" and calls[-2][2]["draft_id"] == 42
    assert observed[-1][1] == "deny" and observed[-1][2] == "execute class denied"

def test_compare_runs_counterfactual():
    c = TestClient(appmod.app)
    c.post("/api/runs", json={"mode": "before", "scenario": "dose", "mrn": 1042})
    c.post("/api/runs", json={"mode": "reference", "scenario": "dose", "mrn": 1042})
    body = c.get("/api/runs/compare", params={"scenario": "dose", "mrn": 1042}).json()
    assert body["scenario"] == "dose" and body["mrn"] == 1042
    assert body["before_run_id"] and body["reference_run_id"]
    assert any(row["tool"] == "draft_heparin" for row in body["rows"])


async def _awaitable(value):
    return value
