"""Normalize research citations and add accurate project-specific evidence boundaries."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
p = root / 'research' / 'RESEARCH-SYNTHESIS.md'
text = p.read_text()
start = text.index('## 10. Titled reference definitions')
end = text.index('## Final recommendation', start)
body = text[:start] + text[end:]
reference_text = text[start:end]
refs = []
for line in reference_text.splitlines():
    match = re.match(r'(\d+)\. \*\*(.*?)\*\* \((.*?)\);', line)
    if not match:
        continue
    number, title, urls = match.groups()
    found = re.findall(r'https?://[^`\s;)]+', urls)
    if found:
        refs.append((number, title.replace('"', "'"), found))
body = re.sub(r'\[(\d+)[–-](\d+)\]', lambda m: ' '.join(f'[{i}]' for i in range(int(m[1]), int(m[2])+1)), body)
body = re.sub(r'\](?=\[\d)', '] ', body)
body += '''\n## Implementation evidence and supplied technical documentation\n\nThe supplied `AgentID.zip` includes first-party AgntID quick-start, MCP, intent, and Python SDK documentation. These files document Medium/READ_WRITE semantics, numeric min/max setup, task opening, protected client wrapping, task shortlisting, and task closing. The public research agents could not read the authenticated online docs, so their “publicly unverified” caveat does not mean that no specification was provided. The build uses the supplied specification and the official SDK source, pinned to Git revision `f4fcd2fe476f0c4dcf800e498530b7042b830f6b`. Documentation and installed SDK API checks are not evidence that a tenant is connected or its policy is applied. Live behavior remains unverified until an actual runtime is configured and its Reporting events are captured.\n\nThe implemented innovation is a **counterfactual evidence workbench for a regulated action pack**. It makes the difference between requested action, policy expectation, observed SDK response, and actual ward side effect visible rather than presenting all of them as “guardrails.” This is a differentiated demo design, not a claim of world-first invention.\n\n**Implemented transfers:** Anthropic’s narrow tool interface and simple workflow appear in `ward/server.py` and `server/app.py`. Microsoft/Cloudflare least-privilege patterns appear in trusted environment identities, token-protected raw MCP ingress, and a fail-closed protected SDK path. CrowdStrike/Vectra-style causal inspection appears in the tool-call trace and audit viewer. Orca/Zscaler audit separation appears in the independent observation ledger and export. OpenZeppelin-inspired normalized argument hashing appears in the local ledger; there are no blockchain transactions or signatures. Databricks-style explicit evaluation appears in the synthetic regression tests. Fortinet’s untrusted web-input principle appears in escaped chart/log rendering and request validation.\n\n**Not implemented:** vendor APIs or sensors, anomaly-learning models, a global CNAPP, enterprise identity management, signed/WORM audit storage, clinical protocols, hospital integration, or an alternative to AgntID. Stripe-style retry idempotency is a production hardening recommendation; this application avoids automatic retry of live mutations and labels timeouts as potentially unknown outcomes.\n\nThe illustrative reference lane never dispatches a tool. The raw before lane intentionally demonstrates synthetic side effects without runtime protection. The live lane uses only the official SDK and has no raw fallback. Until runtime connection is completed, this is a working application and integration-ready demo—not a completed measured AgntID-enforcement submission.\n\n## References\n\n'''
for number, title, urls in refs:
    body += f'[{number}]: {urls[0]} "{title}"\n'
    for extra in urls[1:]:
        body += f'\nRelated source for [{number}]: [{title}]({extra}).\n'
p.write_text(body)
print(f'Normalized {len(refs)} titled references: {p}')
