# Cursor handoff — Second Nurse

## Start here

Open the extracted application folder in Cursor. Read `README.md`, `plan.md`, `TODO.md`, `docs/ARCHITECTURE.md`, `agntid/SETUP.md`, and `docs/VALIDATION.md`. The app is a Python FastAPI service with static HTML/CSS/JS—not React—and an official FastMCP ward server. No database/login is needed for the supplied synthetic demonstration. Use `requirements.lock`, not the system Python package set.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.lock
pytest -q
uvicorn server.app:app --host 0.0.0.0 --port 3000
```

## Completed implementation

The control room supports patient selection, scenario execution, call-trace inspection, action-pack download, audit search/filter/export, research source search/status/pagination, and runtime readiness guidance. The raw before mode uses real synthetic ward mutations; the reference mode never calls tools. Four patients, two canonical units, the poisoned note, and nine schema-defined MCP tools are implemented. Raw HTTP MCP is disabled without a token and authenticated when enabled. The official AgntID 0.2.0 SDK source is pinned to commit `f4fcd2fe476f0c4dcf800e498530b7042b830f6b`; its lifecycle APIs were checked against the installed source. Backend and protocol tests are included. The local ledger is hash-linked and explicitly not immutable or AgntID Reporting.

All 1,574 user-supplied URLs were attempted: 1,274 successful retrievals, 238 HTTP errors, 62 other failures/timeouts. Sixteen dedicated subject agents verified targeted vendor/engineering mechanisms. Source inventory, full status results, cited synthesis, and source-to-code mapping are included. Snapshots are separately packaged. The nine named security companies are references only, not live integrations.

## The highest-priority unfinished step

**Connect and measure genuine AgntID enforcement.** No bootstrap/access token, running customer runtime, or tenant was supplied to this task. This code is integration-ready but cannot claim a measured live allow/deny or a completed hackathon runtime submission yet.

1. Start the real customer runtime with the supplied Compose reference on your machine. Obtain the bootstrap token through the real portal and connect it privately.
2. Start the ward capability service and configure a random `WARD_MCP_TOKEN` for HTTP, or register a local stdio command reachable by the runtime.
3. Discover all nine exact tools. Review Medium/READ_WRITE, draft writes, execute sign/message, delete discard.
4. Author the intended numeric bounds in the portal and wait for **APPLIED**: units 800–1200, route_code 1–1, volume_ml 200–350.
5. Set server-side `AGNTID_MCP_URL` to the protected runtime, trusted `AGNTID_AGENT_ID` and `AGNTID_USER_ID`, optional raw OAuth token, and `ENABLE_LIVE_EXECUTION=true`. Do not send these from the browser.
6. Run Simulator with one useful allowed task, one numeric deny, and one execute/visibility restriction. Capture actual Reporting correlation IDs and synthetic ward results.
7. Observe the actual LLM/Standard intent mode. Only claim output protection or final-answer validation when Call Flow shows it.

Excluded tools may be hidden rather than callable; a missing shortlist tool is a **client restriction**, not evidence that the runtime received and denied the call. Keep that distinction in the UI and pitch. Do not broaden the shortlist after an empty result or retry a denied action with different arguments unless the user explicitly changes the task.

## Engineering hardening after the demo

Do not turn the raw before path into a production endpoint. The current preview is a synthetic demonstration with in-memory history; it is not multi-tenant or durable. If building a production product later, isolate users/runs, enforce authenticated admin boundaries, remove raw unsafe operations, add durable external append-only audit, key rotation, policy attestation, safe migration/versioning, robust idempotency, and verified actual-state reconciliation after network failures.

Clinical safety cannot be inferred from these fixtures. A real medical system would need independent clinical review, real protocol provenance, proper ABO/crossmatch/time/product invariants, human approval, patient identity control, validated EHR integration, and applicable regulatory review. Do not add clinical advice merely to make the demo “more AI.”

## Useful code entry points

The source modules are described in `docs/ARCHITECTURE.md`. `server/app.py` owns APIs and fixed scenarios. `server/agntid_runtime.py` owns the real official SDK path. `ward/server.py` owns MCP transports. `ward/tools.py` owns synthetic side effects. `web/app.js` owns UI state/rendering and uses relative API requests. `web/styles.css` owns the responsive design. `tests/` and `docs/VALIDATION.md` identify completed checks.

If changing API fields, update both the Python response and `web/app.js`. Never render note/log strings through unescaped HTML or Markdown. Do not fetch the attack image. Keep all event provenance explicit and keep live unknown state as unknown, not zero. Preserve partial events on failure. Never import the local `agntid/` documentation folder as a Python package: it would shadow the official SDK; integration code belongs under `server/`.

## Paste this into Cursor

> Continue this existing Second Nurse application. First run its tests and read README, plan, TODO, ARCHITECTURE, SETUP, and VALIDATION. Preserve the supplied synthetic four-patient scope, nine-tool MCP catalog, no real clinical data, and no substitute AgntID policy engine. The app has functional raw-before and nonexecuting illustrative-reference modes plus an official SDK adapter; genuine runtime bootstrap, APPLIED policy setup, Simulator allow/deny, and Reporting evidence remain external tasks. Help me connect my actual runtime securely, discover exact names/schemas, maintain accepted task-open and shortlist fail-closed semantics, use only wrapped calls, and close tasks. Do not silently retry denials, broaden an empty shortlist, fall back to raw tools, fabricate runtime stages, render the poisoned note as HTML, or describe unknown timeout outcomes as no execution. Capture actual synthetic evidence and update the truthful submission status. Ask for secret entry only through local environment/secret tooling, never in source or chat.

## Submission status

The submission draft intentionally states that live enforcement remains to be demonstrated. Update it only after real evidence exists. Public Luma and Devfolio schedules conflict; confirm the current organizer deadline. Nothing was submitted to Devfolio, no broad public publication was performed, and no account/billing changes were made.

**Live control network boundary:** protected runtime calls and live runtime checks require loopback Host, loopback peer, and loopback Origin when present. Use `http://localhost:3000` on the machine running the app; public Preview cannot exercise configured runtime identities. Replay history is a shared synthetic demonstration history, not per-user session storage. Do not store real records or expose a live-enabled deployment publicly.
