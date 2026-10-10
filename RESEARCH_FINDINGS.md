# Research findings register — Second Nurse

**Primary corpus:** [research/RESEARCH-SYNTHESIS.md](research/RESEARCH-SYNTHESIS.md), [research/source-coverage.json](research/source-coverage.json) (1574 URLs attempted; 1274 retrieved).  
**User link files:** [reference/user-provided/](reference/user-provided/) — not re-fetched in this audit pass.

## AgntID (official, in-repo)

| Source | URL / path | Topic | Finding | Evidence | Application gap | Recommendation | Priority | Feasibility |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AgntID attach-server | [reference/agntid-docs/attach-server.md](reference/agntid-docs/attach-server.md) | MCP governance | Remote HTTP MCP + credential env refs | Portal configures runtime; bearer not in form | Ward must be registered behind proxy | Follow [docs/WINDOWS-PORTAL-INTEGRATION.md](docs/WINDOWS-PORTAL-INTEGRATION.md) | Critical | Portal access required |
| AgntID Python guide | [reference/agntid-docs/python-guide.md](reference/agntid-docs/python-guide.md) | SDK harness | task_context, wrap_client, shortlist | Implemented in `agntid_runtime.py` | Live allows need APPLIED policy | Capture Reporting task_id | High | SDK + runtime running |
| RESEARCH-SYNTHESIS §3 | in-repo | Product design | Counterfactual before/after + audit separation | Hypothesis stated | Partially implemented (compare API, UI) | Extend judge demo script | Medium | Low effort |

## Engineering patterns (from prior verified research — sample)

| Source | URL | Topic | Finding | Evidence | Application gap | Recommendation | Priority | Feasibility |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Synthesis §3.1 | RESEARCH-SYNTHESIS | Least privilege | Nine narrow MCP tools, no shell/HTTP tool | Tool catalog in ward | — | Keep catalog frozen | High | Done |
| Synthesis §2.3 | RESEARCH-SYNTHESIS | Evaluation | Model prose ≠ tool execution proof | Architecture doc | UI shows provenance labels | Keep Reporting authoritative | High | Done |
| CrowdStrike / vendor refs | research/verified-research.json | Detection mindset | Causal traces for agent actions | Mapped to ledger + run export | Not SIEM integration | Local ledger as demo aid only | Low | N/A integration |

## Web3 link file

[reference/user-provided/web3-companies-links.md](reference/user-provided/web3-companies-links.md) — **Not applicable** to Second Nurse scope (no on-chain components). No URLs fetched in this audit.

## Audit pass additions

| Source | Topic | Finding | Gap | Recommendation | Priority |
| --- | --- | --- | --- | --- | --- |
| ASD-STE100 audit directive | Process | Defect register before code change | — | Maintain DEFECT_REGISTER.md on future changes | Medium |
| OWASP-style review (manual) | XSS | Escaped rendering for chart note | — | Keep `esc()` on all note/log strings | High |

## Unprocessed in this pass

- Full re-crawl of `all_links(1).txt` — deferred; use existing `source-coverage.json`.
- `D:\Downloads\skills.zip` — not extracted per safety rule.
