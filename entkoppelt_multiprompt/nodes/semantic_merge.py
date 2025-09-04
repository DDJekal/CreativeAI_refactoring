from typing import Any, Dict, List


def _merge_positioning_logic(a: List[str], b: List[str]) -> List[str]:
    out = []
    for r in a + b:
        if r and r not in out:
            out.append(r)
    return out


def SemanticMerger(state: Dict[str, Any]) -> Dict[str, Any]:
    heur = state.get("semantics_heur") or {}
    llm = state.get("semantics_llm") or {}

    merged = dict(heur)  # Heuristik dominiert harte Regeln

    # positioning_logic union
    a = heur.get("positioning_logic") or []
    b = llm.get("positioning_logic") or []
    merged["positioning_logic"] = _merge_positioning_logic(a, b)

    # text_areas: Notizen aus llm hinzufuegen pro Rolle
    llm_by_role = {x.get("role"): x for x in (llm.get("text_areas") or []) if isinstance(x, dict)}
    out_areas = []
    for area in (heur.get("text_areas") or []):
        role = area.get("role")
        if role in llm_by_role:
            llm_notes = llm_by_role[role].get("notes")
            if llm_notes:
                area = dict(area)
                area["notes"] = (area.get("notes", "") + "; " + llm_notes).strip("; ") if area.get("notes") else llm_notes
        out_areas.append(area)
    merged["text_areas"] = out_areas

    state["semantics"] = merged
    return state


