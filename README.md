# Second Nurse

**Useful work. No unchecked authority.**

Second Nurse is a complete synthetic-agent demonstration application and AgntID integration workbench. A night-float workflow prepares unsigned transfusion and heparin drafts; independent runtime controls are intended to bound parameters and exclude irreversible actions. The application never provides clinical guidance, issues blood, contacts a family, or handles real patient information.

## Run the application

Python 3.11+ is required; the delivered environment was tested with Python 3.12. The official AgntID SDK 0.2.0 is pinned to a verified source commit because the supplied docs recommend source installation.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
uvicorn server.app:app --host 0.0.0.0 --port 3000
```

Open `http://localhost:3000`. No database, login, model key, or AgntID account is needed for the reference and synthetic before modes. On Windows, activate `.venv\Scripts\Activate.ps1` and run the same pip/uvicorn commands.

**Windows + AgntID (integrated local run):** copy `.env.local.example` to `.env.local`, set secrets, then `.\scripts\start-local.ps1`. Portal steps for registering the ward MCP server and policies are in [docs/WINDOWS-PORTAL-INTEGRATION.md](docs/WINDOWS-PORTAL-INTEGRATION.md). Integration scorecard: `python scripts/live_smoke.py` (app must be running on loopback).

Alternatively:

```bash
docker build -t second-nurse .
docker run --rm -p 3000:3000 second-nurse
```

Docker deployment files are supplied, but the container build was not run in this sandbox because Docker is not installed. The application and official SDK were exercised directly.

## What works

The responsive control room has six views: Ward overview, Agent workspace, Action pack, Audit ledger, Research library, and Runtime connection. Select any of four fixed synthetic patients, inspect the poisoned chart note safely as text, run deterministic scenarios, inspect call arguments/results/stages, filter the ledger, and export evidence or the action-pack manifest. The research library includes every supplied URL's retrieval status and verified mechanism summaries for all nine requested security vendors.

The Python capability server exposes exactly nine tools: `list_patients`, `get_patient`, `get_unit`, `get_chart_note`, `draft_transfusion`, `draft_heparin`, `sign_order`, `discard_unit`, and `message_family`. Portal prefix `ward` may alter their public names; the adapter discovers exact runtime names rather than guessing them. No reset, shell, SQL, arbitrary HTTP, or unchecked-blood tool is exposed.

## Three modes, three distinct claims

**Illustrative reference** displays expected outcomes from fixtures. It never calls ward tools or AgntID, never mutates state, and is not enforcement evidence.

**Raw before** calls the real synthetic ward functions directly, using an isolated memory store per run. It can draft an out-of-range synthetic heparin dose, sign a synthetic draft, discard a synthetic unit, and queue a string-only message. It is a deterministic replay—not an observed model attack. The existing application ABO check rejects mismatches in both conditions; there is no bypass helper.

**Real AgntID** uses the installed official SDK, trusted server identity, exact discovered tool names, accepted task opening, task-specific shortlist, protected client wrapping, and task closing. It has **no raw fallback**. It is a deterministic integration runner, not a local LLM agent. AgntID Simulator is the recommended live model-driven workflow. Live calls require a real runtime and explicit server-side enablement; none was supplied or connected in this task.

## Connect genuine AgntID

Follow [the setup guide](agntid/SETUP.md). At a minimum:

```bash
export AGNTID_MCP_URL=http://localhost:8082/mcp
export AGNTID_AGENT_ID=second-nurse:v1
export AGNTID_USER_ID=synthetic-night-float
export ENABLE_LIVE_EXECUTION=true
# If the runtime requires client OAuth:
export AGNTID_ACCESS_TOKEN='your-current-raw-access-token'
# Secure the runtime-to-raw-ward hop; use your own generated token:
export WARD_MCP_TOKEN='your-own-random-token'
```

The app does not auto-load `.env`; export values, use your shell's environment tooling, or use a deployment secret manager. Never paste secrets into the UI, prompts, audit exports, or committed files. The raw HTTP MCP endpoint is disabled if `WARD_MCP_TOKEN` is unset and requires bearer authentication when enabled. **Do not point the protected client at the raw ward endpoint.**

Use the portal to review Medium/READ_WRITE, read/normal-write tool classes, execute sign/message, delete discard, and the intended bounds: synthetic heparin `units=800–1200`, IV `route_code=1–1`, transfusion `volume_ml=200–350`. Wait for **APPLIED**. The action-pack JSON is a design manifest, not a claimed importable AgntID policy schema. Policy authoring and live Reporting screenshots remain external handoff steps.

## Tests and evidence

```bash
python -m pytest -q
node --check web/app.js
python -m before.run_before
```

Tests cover raw synthetic mutations, ABO mismatch, state isolation, nonexecuting reference, validation, disabled/missing runtime, protected SDK lifecycle and denial, ledger tamper detection, and MCP discovery/auth. See [validation evidence](docs/VALIDATION.md) for the exact completed checks and limitations.

Local hash-linked events are tamper-evident observations, **not immutable, signed, clinically validated, or AgntID Reporting**. A transport timeout may leave execution unknown; inspect the actual runtime before retrying. The app does not auto-retry live mutations. Live remote ward state cannot always be directly observed, so it must not be interpreted as zero mutations.

## Research coverage

All **1,574 unique URLs** from the supplied four directories were attempted with bounded public HTTP retrieval. Results: **1,274 retrieved, 238 HTTP errors, 62 other failures/timeouts**. Each attempt records source files, status, redirects, title, content hash, byte count/cap, and error where relevant. Retrieved does not mean fully or deeply read; 120,000-byte caps and dynamic/login pages limit coverage.

Sixteen dedicated research agents and one synthesis agent verified targeted security/engineering mechanisms. All nine requested vendors are covered: Orca, CrowdStrike, Palo Alto Networks, SentinelOne, Microsoft Security, Darktrace, Vectra AI, Fortinet, and Zscaler. They are **references, not installed integrations**. The implementation uses appropriate narrow-tool, least-privilege, untrusted-rendering, causal-trace, task-correlation, and evaluation patterns rather than importing every algorithm. RAG, model training, crypto custody, and vendor sensors do not improve this specific supplied hackathon scope.

Read [the cited research report](research/RESEARCH-SYNTHESIS.md), [the complete coverage JSON](research/source-coverage.json), and [the architecture](docs/ARCHITECTURE.md). The larger source-snapshot archive is supplied separately to keep application source practical.

## Cursor handoff

Start with [CURSOR-HANDOFF.md](docs/CURSOR-HANDOFF.md). It distinguishes completed code from genuine runtime gates, lists exact next steps, and includes a prompt for continuing implementation without fabricating evidence. [The judge demo](submission/DEMO.md) and [submission draft](submission/DEVFOLIO.md) avoid unsupported research statistics and do not claim a completed live integration.

## Safety and scope

All four patients are fictional. Doses and volume ranges are synthetic constants, not real protocols. ABO equality is deliberately simplified and not a transfusion compatibility algorithm. No real EHR, blood bank, clinician approval, hospital identity, vendor API, clinical validation, compliance certification, medical device, or world-first claim is present. The public Luma and Devfolio schedules conflict; verify the organizer's current deadline. Nothing has been submitted or broadly published.

For a remote raw MCP hostname, set `WARD_ALLOWED_HOSTS=your-hostname:3000` (or the exact host observed through your proxy) before starting the app. Loopback is accepted by default; arbitrary public hosts are not. Keep bearer authentication enabled. The raw MCP ward is shared within one process; it is synthetic, not a multi-tenant clinical store.

**Live control network boundary:** protected runtime calls and live runtime checks require loopback Host, loopback peer, and loopback Origin when present. Use `http://localhost:3000` on the machine running the app; public Preview cannot exercise configured runtime identities. Replay history is a shared synthetic demonstration history, not per-user session storage. Do not store real records or expose a live-enabled deployment publicly.

### Reproduce browserless interface tests

With Node 22 or newer, start the application, then run `npm ci --ignore-scripts` and `npm run test:ui`. The test uses JSDOM and real APIs at `http://127.0.0.1:3000`; set `TEST_BASE_URL` to change it. It is not a real-browser visual audit. Node is optional for running the Python application.
