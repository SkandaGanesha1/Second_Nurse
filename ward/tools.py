"""Raw ward capability functions shared by the before path and MCP server.

These functions are intentionally not an authorization layer. In particular,
``draft_heparin`` has no dose check; the runtime policy owns that control.
"""
from __future__ import annotations
from typing import Any
from .data import PATIENTS, UNITS, POISON_NOTE, Store, get_store

def _bad(message: str) -> dict[str, Any]:
    return {"ok": False, "error": message}

def list_patients() -> dict[str, Any]:
    return {"patients": [{"mrn": p.mrn, "name": p.name, "abo": p.abo} for p in PATIENTS.values()]}

def get_patient(mrn: int) -> dict[str, Any]:
    if not isinstance(mrn, int) or isinstance(mrn, bool) or mrn not in PATIENTS:
        return _bad("unknown mrn")
    p = PATIENTS[mrn]
    return {"mrn": p.mrn, "name": p.name, "abo": p.abo, "weight_kg": p.weight_kg,
            "protocol_min": p.protocol_min, "protocol_max": p.protocol_max}

def get_unit(unit_id: str) -> dict[str, Any]:
    if not isinstance(unit_id, str) or unit_id not in UNITS:
        return _bad("unknown unit")
    u = UNITS[unit_id]
    return {"unit_id": u.unit_id, "abo": u.abo, "volume_ml": u.volume_ml,
            "in_date": u.in_date, "crossmatch_mrn": u.crossmatch_mrn,
            "discarded": u.unit_id in get_store().discarded or unit_id in get_store().discarded}

def get_chart_note(mrn: int) -> dict[str, Any]:
    if not isinstance(mrn, int) or isinstance(mrn, bool) or mrn not in PATIENTS:
        return _bad("unknown mrn")
    return {"mrn": mrn, "note": POISON_NOTE if PATIENTS[mrn].poisoned else PATIENTS[mrn].note,
            "synthetic": True, "untrusted": PATIENTS[mrn].poisoned}

def draft_transfusion(mrn: int, unit_id: str, volume_ml: int) -> dict[str, Any]:
    if not isinstance(mrn, int) or isinstance(mrn, bool) or mrn not in PATIENTS:
        return _bad("unknown mrn")
    if not isinstance(unit_id, str) or unit_id not in UNITS:
        return _bad("unknown unit")
    if not isinstance(volume_ml, int) or isinstance(volume_ml, bool) or volume_ml <= 0:
        return _bad("volume_ml must be a positive integer")
    p, u, store = PATIENTS[mrn], UNITS[unit_id], get_store()
    # Simplified equality-only synthetic check, deliberately not clinical compatibility.
    if p.abo != u.abo:
        return _bad("ABO mismatch: synthetic equality check rejected")
    if not u.in_date or u.unit_id in store.discarded or unit_id in store.discarded:
        return _bad("unit unavailable")
    draft = {"id": store.new_id(), "kind": "transfusion", "mrn": mrn,
             "unit_id": unit_id, "volume_ml": volume_ml, "signed": False}
    store.drafts.append(draft)
    return {"ok": True, "draft_id": draft["id"], "kind": "transfusion", "volume_ml": volume_ml}

def draft_heparin(mrn: int, units: int, route_code: int) -> dict[str, Any]:
    if not isinstance(mrn, int) or isinstance(mrn, bool) or mrn not in PATIENTS:
        return _bad("unknown mrn")
    if not isinstance(units, int) or isinstance(units, bool) or units <= 0:
        return _bad("units must be a positive integer")
    if not isinstance(route_code, int) or isinstance(route_code, bool):
        return _bad("route_code must be an integer")
    store = get_store()
    draft = {"id": store.new_id(), "kind": "heparin", "mrn": mrn,
             "units": units, "route_code": route_code, "signed": False}
    store.drafts.append(draft)
    return {"ok": True, "draft_id": draft["id"], "kind": "heparin", "units": units}

def sign_order(draft_id: int) -> dict[str, Any]:
    store = get_store()
    if not isinstance(draft_id, int) or isinstance(draft_id, bool):
        return _bad("draft_id must be an integer")
    for i, draft in enumerate(store.drafts):
        if draft["id"] == draft_id:
            moved = dict(draft, signed=True)
            store.drafts.pop(i)
            store.signed.append(moved)
            return {"ok": True, "signed_id": draft_id}
    return _bad("unknown draft")

def discard_unit(unit_id: str) -> dict[str, Any]:
    if not isinstance(unit_id, str) or unit_id not in UNITS:
        return _bad("unknown unit")
    store = get_store()
    canonical = UNITS[unit_id].unit_id
    if canonical in store.discarded or unit_id in store.discarded:
        return _bad("unit already discarded")
    store.discarded.append(canonical)
    return {"ok": True, "discarded": canonical}

def message_family(mrn: int, body: str) -> dict[str, Any]:
    if not isinstance(mrn, int) or isinstance(mrn, bool) or mrn not in PATIENTS:
        return _bad("unknown mrn")
    if not isinstance(body, str):
        return _bad("body must be a string")
    # Queue only. Never fetch, render, or send URLs/HTML.
    message = {"id": get_store().new_id(), "mrn": mrn, "body": body}
    get_store().messages.append(message)
    return {"ok": True, "message_id": message["id"], "queued": True}

TOOLS = {
    "list_patients": list_patients, "get_patient": get_patient, "get_unit": get_unit,
    "get_chart_note": get_chart_note, "draft_transfusion": draft_transfusion,
    "draft_heparin": draft_heparin, "sign_order": sign_order,
    "discard_unit": discard_unit, "message_family": message_family,
}
