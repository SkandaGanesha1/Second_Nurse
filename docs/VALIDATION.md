# Validation evidence

## Executed successfully

`python -m pytest -q` completed with **23 passed** in the isolated Python 3.12 environment. Tests cover raw out-of-range dose/sign/message side effects, ABO mismatch rejection, isolated run state, nonexecuting reference, request constraints, missing live runtime/no fallback, ledger tamper detection, complete bootstrap/research contracts, nine-tool registration, raw HTTP disabled/unauthorized responses, evidence export, official SDK task lifecycle, dynamic draft ID handling, rejected task/missing snapshot/empty shortlist, application error classification, transport-unknown outcome, and signature without an observed draft.

Crucially, tests also perform real MCP protocol initialization, list-tools, patient retrieval, draft creation, and subsequent signing through **stdio** and **mounted authenticated streamable HTTP**. These are raw synthetic protocol tests, not AgntID runtime enforcement tests. They exposed and corrected the nested `/mcp/mcp` path, missing parent lifespan management, loopback host validation, and cross-call synthetic state persistence.

The installed official `agntid-sdk` is **0.2.0**, source commit `f4fcd2fe476f0c4dcf800e498530b7042b830f6b`. Required API exports were verified. The local `agntid/` directory remains documentation only so it does not shadow the installed SDK. MCP **1.30.0** and FastMCP **2.14.7** are recorded in the portable dependency lock.

`node --check web/app.js` passed. Browserless JSDOM checks, using real application APIs, passed for all six views, patient selection, nonexecuting reference, raw dose replay, escaped poisoned chart, no attacker-image element, trace rendering, audit search, action-pack JSON download, all-source pagination, and runtime check. These checks do not substitute for a real-browser visual/accessibility audit; no screenshot or responsive pixel-perfect claim is made.

`python -m before.run_before` generated a real deterministic raw synthetic transcript. No model, AgntID enforcement, image loading, or external message occurred.

Local and temporary public `GET /health` returned HTTP 200 and `synthetic_only:true`. `GET /manus-routes.json` returned HTTP 200 with the six real hash routes. Unknown API/assets returned 404, not SPA HTML. Public raw MCP remains 503 because no token is configured. All browser-facing API/asset URLs are relative and the preview has no frame-blocking headers.

All **1574 unique source URLs** have a recorded attempt: **1274 retrieved, 238 HTTP errors, 62 other failures/timeouts**. Coverage totals agree with the source rows. Page retrieval was capped at 120000 bytes and did not recursively read all linked articles. Targeted source verification used sixteen research subjects and one synthesis.

## Source audit

An independent read-only implementation audit was requested and its confirmed discrepancies were checked and corrected before packaging. Any remaining integration/production concerns are stated in the handoff rather than hidden behind a completed label.

## Diagnostics limitation

Host language diagnostics were registered for Python, JavaScript, HTML, CSS, and JSON. Its Python environment still reported unresolved package imports despite successful installation/import/tests in the application virtual environment. Those environment-specific diagnostics are not evidence that the source cannot run, but this report does **not** claim a clean host-LSP pass. Successful runtime imports, compileall, protocol checks, pytest, and JS syntax are the reliable completed checks here.

## Not performed / not claimed

No genuine AgntID runtime or tenant credentials were supplied. No runtime bootstrap, portal policy authoring, APPLIED synchronization, Simulator model execution, scoped-credential observation, actual runtime allow/deny, Reporting screenshots, LLM-based tool-output inspection, or final-answer validation was completed. Mocked official SDK tests verify wiring, not live product behavior.

Docker was unavailable, so the supplied Dockerfile was not built or executed. Direct Python serving was validated. The application is a temporary Preview/checkpoint and downloadable source, not a published production service. No real browser visual audit, clinical validation, real patient data, hospital integration, vendor API integration, signed/WORM storage, or Devfolio submission occurred.

## Independent audit corrections

The read-only audit found task preparation outside the closing context, missing task-level/correlation evidence, premature health availability, public access to enabled runtime identities, unreproducible JSDOM setup, and overstated session isolation. These were corrected: client connects before task creation; discovery/open/calls are inside the official closing context; rejected preparation emits a task-lifecycle event; SDK events retain task IDs; initial health is configured-unverified; loopback Host/peer/Origin guards protect live control; pinned package.json/package-lock and npm test instructions reproduce DOM checks. Shared synthetic replay history remains process-global and is explicitly documented rather than claimed session-isolated. Regression tests cover these corrections.

The completed source was committed and pushed successfully to canonical main at `2e5505a0f4f260ce1e98812e96e709b2cfdf2156`. No structured platform checkpoint card was returned, so this report claims an accepted source push rather than independently confirmed Version-history recording. Publication remains disabled and no deployment was performed.
