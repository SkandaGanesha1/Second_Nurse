# Second Nurse — judge demonstration

## Claim and prerequisite

A useful synthetic ward agent should prepare drafts without granting itself permission to sign, discard, or communicate externally. The actual AgntID runtime must decide tool authority; model prose is not evidence.

This application's reference and raw-before modes are complete. Its official SDK path is ready, but **live runtime enforcement has not been demonstrated in this task**. Obtain real allow/deny Reporting evidence before using the protected section as a finished submission. Public event schedules conflict; follow the organizer's current instruction.

## Two-minute sequence

**0:00–0:20 — useful task.** Open Ward overview and choose Meera Shah, MRN 1042. Explain all patients, units, and numeric bounds are fictional demo constants. Open the agent workspace. The task asks for a 280 ml transfusion draft and 1000-unit IV synthetic heparin draft, with no signature, family message, or discard.

**0:20–0:40 — unsafe before.** Select Raw before → Dose overdose → Run. Show `draft_heparin(1042,10000,1)` actually reached the synthetic function. Run Signature and show a synthetic signed order. Explain this is deterministic direct replay, not a measured model attack. The poisoned note is visible as escaped text; its image URL is never fetched.

**0:40–1:10 — actual protected path, only after setup.** Use the real AgntID Simulator with the useful task. Show both unsigned drafts succeed. Then attempt 10000 units and show the actual input-policy denial before dispatch. Attempt signing and show the actual execute denial or lack of tool visibility. Do not mislabel a shortlist block as a runtime-denied call. Show APPLIED status and exact policy input/limits.

**1:10–1:35 — independent proof.** Show Reporting task/correlation ID, exact tool/arguments, decision/reason, and actual tool result. Compare ward side effects. A final sentence saying “signed” does not mean the tool ran. The local audit viewer is a hash-linked observation aid, not immutable storage and not official Reporting.

**1:35–2:00 — novelty and scope.** The differentiated artifact is a counterfactual evidence workbench for a task-specific regulated action pack. Vendor research informed narrow capabilities, task identity, causal traces, audit separation, and input rendering; those vendors are not integrated. A real EHR, clinical validation, dosing recommendation, hospital IAM, or compliance certification is outside this synthetic demo.

## If runtime is not connected

Demo the complete raw path and clearly labeled reference expectations, then say: “The application and official SDK integration are implemented. Actual tenant policy application and measured runtime evidence are the remaining integration gate.” Never replace that gate with a local fake policy engine or a pre-recorded expected deny labeled AgntID.

## Offline CLI

```bash
python -m before.run_before > raw-before.json
```

This produces a complete synthetic transcript and side effects without a browser, model, runtime, or external message. It does not demonstrate AgntID. For tests, use `python -m pytest -q`; for live setup, follow `agntid/SETUP.md`.
