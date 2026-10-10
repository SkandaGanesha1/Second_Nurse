# Second Nurse — implementation and design plan

## Product direction

Implement the supplied Second Nurse action pack: a synthetic night-shift assistant prepares unsigned transfusion and heparin drafts, while a separate real AgntID runtime enforces access before tool execution. Preserve the provided Python MCP stack, four deterministic patients, in-memory ward state, numeric policy bounds, execute/delete action classes, no real PHI, no medical-device claims, and no substitute local policy engine. The user explicitly authorized research, planning, implementation, testing, and a complete Cursor handoff.

Expand the supplied static projector board into a functional control console with Ward overview, Agent workspace, Action pack, Audit ledger, Research library, and Runtime connection. A raw deterministic before-run is a deliberately unsafe synthetic replay, not a claim that a live model was compromised. A documented expected-after reference can illustrate configured controls, but it must say illustrative, must never execute tools, and must never masquerade as measured runtime evidence. Live after mode requires the official AgntID SDK and a configured real runtime. No fallback to raw tools after denial, SDK errors, or missing runtime.

## Architecture

Python 3.11+ (tested on 3.12) FastAPI serves the static interface and application APIs on port 3000; FastMCP exposes nine ward tools via stdio and streamable HTTP in the same ASGI process where practical. Pure ward tools are shared with the raw before script. All side effects remain synthetic and in memory. No database or app login is added. Runtime credentials and optional model settings come only from server environment, never prompts or browser settings. Raw ward state is isolated per replay, while synthetic run history and audit views are process-global (not session-isolated). Live control is limited to a loopback operator; public visitors cannot invoke the protected runtime without an explicit server-side enable flag.

The official AgntID integration opens one task per request, discovers exact profile-visible tool names, passes only accepted task shortlist tools when available, wraps all business calls for correlation, treats denials as normal outcomes, and closes tasks on every exit. Scenario plans are deterministic; Simulator remains the recommended live natural-language agent. Optional local agent orchestration is deferred unless SDK/runtime connectivity is healthy. No unsigned draft is promoted by UI alone. No external messages or image URLs are rendered or sent.

Audit events have explicit provenance: raw before, illustrative reference, local tool observation, or official SDK response. The local append-only hash-linked log is tamper-evident within a process, not immutable or signed by AgntID; Reporting is authoritative for runtime enforcement. Evidence exports preserve this distinction, correlation IDs, arguments, result, execution status, and policy pack version. Runtime health is never inferred from placeholder text. Connection checks do not imply policy sync or clinical approval.

Research: extract all unique URLs from the four supplied directories; bounded HTTP retrieval attempts record status, redirects, title, byte cap, content hash, and failures. Reading 1,574 landing pages is not the same as exhaustive article review. Sixteen dedicated subject agents research nine requested security vendors and seven core engineering/threat-model subjects; one reducer produces cited architecture guidance. Implement only applicable mechanisms; do not import every algorithm or claim vendor-equivalent coverage.

## Project structure

- `ward/`: immutable synthetic fixture definitions, state store, raw tool functions, nine reviewed MCP definitions.
- `before/`: deterministic raw attack transcript executable without any AI model.
- `agntid/`: non-Python action pack manifest, real setup guide, copied original runtime Compose reference.
- `server/`: official SDK adapter, FastAPI app, validated request models, session-scoped demo orchestration, audit ledger, export API.
- `web/`: static HTML, CSS, JS modules, brand icon, route manifest; no framework or decorative stock images.
- `agent/`: concise system instructions and useful/denied prompts.
- `research/`: URL inventory, HTTP coverage results and source snapshots, cited subject synthesis.
- `tests/`: ward behavior, state isolation, API failures, exact adapter lifecycle, nonexecution of denied paths, audit linkage.
- `docs/` and `submission/`: architecture, limitations, reproducible setup, Cursor handoff, judge demo, submission draft.
- `scripts/`: fetch-all-links and evidence generation utilities.

## Dependencies and serving

Pin Python dependencies after successful installation and keep no secrets in source. Use official `mcp`/FastMCP plus FastAPI, uvicorn, httpx, and pytest. Official AgntID 0.2.0 source availability is checked from its documented repository; missing or incompatible APIs are blockers, never emulated. A Python Dockerfile installs pinned dependencies and serves the app on `$PORT` (default 3000). It does not run or bootstrap the separate AgntID runtime. Deployment remains Preview, not broad public publication.

## Design

**Design movement:** precision industrial instrumentation with an editorial clinical night-shift aesthetic.

**Core principles:** safety state is explicit; evidence outranks narration; useful work precedes blocked work; dense details remain readable.

**Color philosophy:** ink-black and slate surfaces reduce projector glare; warm ivory typography provides contrast; ownable safety lime `#c5f26b` marks healthy/allowed states, warm amber distinguishes configuration/reference, coral signals denied/unsafe. Never use color as the only decision marker.

**Layout paradigm:** persistent narrow left rail, wide asymmetric workspace, patient context on one side and execution/evidence on the other. Editorial top-line labels and a continuous status strip replace a generic centered card grid.

**Signature elements:** paired offset nurse/check strokes in the monogram; thin instrument-like rule lines; numbered execution stages and compact monospace evidence chips.

**Interaction philosophy:** inspect before act. Primary CTA runs an explicitly labeled synthetic scenario. Runtime-disabled actions explain their prerequisite. Filters, patient selection, tabs, export, and navigation perform real functions; no fake connection controls.

**Animation:** 150–220 ms opacity/position transitions, subtle execution-stage reveal, no gratuitous particle effects; respect reduced-motion. No pretend live counters.

**Typography:** system sans with optional Manrope/Inter local fallback for headings; Georgia italic for the hero contrast; system monospace for identifiers, doses, hashes, and logs. No dependence on externally loaded fonts for offline operation.

**Brand essence:** independent runtime evidence for useful agents operating around irreversible actions. Precise, calm, accountable.

**Brand voice:** short operational statements: “Useful work. No unchecked authority.” and “The tool did not run. The record explains why.”

**Wordmark:** `second` in ivory with `nurse` in safety lime beside a paired geometric check mark.

**Signature brand color:** safety lime `#c5f26b`.

## Material limitations

Real AgntID runtime is not supplied in the archive, and no bootstrap or access token is configured. Runtime registration and policy authoring may need the user's logged-in portal; protected browser/account workflows cannot be fabricated. Clinical bounds are synthetic constants, not dosing guidance. Static equality-only ABO check is a simplified demonstration, not transfusion medicine. The provided research contains claims that require fresh verification; unsupported percentages, future incident claims, acquisition lists, market dominance and compliance claims will not enter the final pitch.
