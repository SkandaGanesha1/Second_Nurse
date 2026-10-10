# Second Nurse architecture

Second Nurse is an evidence-first synthetic action pack. Its novelty hypothesis is that a narrow useful workflow, a counterfactual comparison, and independent execution evidence make runtime access control understandable and testable. It is not a claim that no competitor offers agent security.

```text
Browser control room (static HTML/CSS/JS)
        │ relative JSON APIs
        ▼
FastAPI / port 3000
        ├── reference fixtures ──► expected events only, no tool dispatch
        ├── raw before ─────────► isolated synthetic Ward Store / real functions
        ├── live SDK runner ────► genuine AgntID MCP endpoint
        │                          task open / accepted intent / shortlist
        │                          wrapped calls / actual runtime policy
        │                          scoped access / tool execution / task close
        │                                   │
        │                                   ▼
        ├── authenticated raw MCP ◄──── reviewed ward capability server
        └── local hash-linked observations / JSON evidence export

AgntID Reporting: authoritative runtime decisions outside this local UI
```

## Components

`ward/data.py` defines the four fictional patients, two canonical units, poisoned note, and in-memory store. `ward/tools.py` contains ordinary functions shared by raw before and the MCP capability server. The raw dose function deliberately lacks the synthetic dose policy, so the before path can demonstrate why a runtime boundary matters. ABO equality and crossmatch remain legacy application checks and are not presented as runtime policy.

`ward/server.py` uses the official Python MCP implementation to expose exactly nine small schema-defined tools. Local stdio is suitable for a runtime-launched process. HTTP discovery/invocation is disabled without an environment token and requires bearer authentication when enabled. There is no reset or arbitrary system/network tool. External message contents remain strings; no attacker URL is fetched.

`server/app.py` serves the UI and JSON APIs, validates requests, creates isolated raw/reference runs, and delegates real protected calls to the official SDK adapter in `server/agntid_runtime.py`. Trusted runtime address, access token, agent identity, user identity, and explicit live-execution enablement come from server configuration. Browser prompts never supply identity or secrets. The SDK path discovers exact names, retains the task shortlist, handles denial, and closes tasks.

`server/ledger.py` canonicalizes and hash-links local events. Hashes detect changes against the retained chain but do not protect against an operator rewriting the whole chain. The ledger is not external, immutable, signed, lossless, or legally certified. The actor does not directly write it through a model tool, but this process remains trusted. In-memory history is temporary and bounded; no durability claim is made.

`web/` is a dependency-free static dashboard using escaped text rendering. It never interprets poisoned chart/log text as HTML or Markdown. Every mode has visible provenance; reference allow does not mean a tool ran. Local stages are descriptive observations, not invented AgntID intent stages. Unknown live state is not displayed as proof that nothing happened.

`research/` holds the 1,574-URL inventory, attempt results, status summary, structured vendor findings, and cited report. Snapshots are capped public-page text and are packaged separately. Sixteen item agents verified specific security/engineering subjects; broad retrieval is distinct from deep review.

## Intended action boundary

The provided synthetic pack asks for Medium/READ_WRITE, numeric heparin units 800–1200, route code 1–1, and transfusion volume 200–350. Sign/message are execute; discard is delete. These intended settings are authored in the real AgntID portal, not enforced by an invented local Python engine. Reference fixtures display expected decisions only. The application does not silently alter a denied request to obtain permission.

The local live runner is deterministic; it sends scenario actions through the official SDK. It is not an LLM tool-selection loop. AgntID Simulator is the supplied model-driven execution surface. A model-generated draft plan does not authorize itself. The real runtime/Reporting and ward result—not a final answer—must establish execution.

## Failure semantics

Missing runtime or incompatible SDK leaves live execution unavailable. Task-open denial and missing snapshot fail closed; empty shortlist stays empty. An action unavailable in the shortlist is a client-side capability restriction, not a runtime-denied call. A runtime denial is recorded with its actual reason. No error falls back to raw calls. A network timeout can mean execution is unknown; do not declare zero side effects or auto-retry a mutation. Partial observations should remain available for investigation.

## Production work deliberately deferred

This is not an EHR integration, dosing engine, validated transfusion checker, clinical approval system, hospital IAM deployment, SIEM product, vendor connector suite, or medical device. In production, independent clinical validation, proper patient/product/protocol invariants, authorization, durable external audit, key management, transport security, idempotency, and an isolated deployment would be needed. The synthetic raw before API is unsuitable for real patient data and should be removed from a production service.

## API surface

`GET /health`, `GET /api/bootstrap`, `POST /api/runs`, `GET /api/runs`, `GET /api/runs/{id}`, `GET /api/runs/{id}/export`, `GET /api/audit`, `POST /api/runtime/check`, `GET /api/research`, and `GET /api/research/report` are the application APIs. `/mcp/` is the authenticated raw capability endpoint. `/`, `/assets/*`, and `/manus-routes.json` serve the interface. The six UI routes use hashes, so no API path is hidden by an SPA fallback.
