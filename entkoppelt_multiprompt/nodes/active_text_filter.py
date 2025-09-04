from typing import Dict, Any, List


def ActiveTextFilter(state: Dict[str, Any]) -> Dict[str, Any]:
    """Bestimmt aktive Text-Rollen basierend auf gelieferten USER-Texten.

    - Dual-Headline hat Vorrang vor Single-Headline
    - Nur vorhandene Felder werden als aktive Rollen markiert
    - Speichert Rollenliste in spec.meta.active_roles
    """
    spec = state.get("spec") or {}
    ut = spec.get("user_texts", {}) or {}
    meta = spec.get("meta") or {}

    has_dual = bool((ut.get("headline_1") or "").strip() and (ut.get("headline_2") or "").strip())
    has_single = bool((ut.get("headline") or "").strip()) or has_dual

    active_roles: List[str] = []
    if has_dual:
        active_roles += ["headline_1", "headline_2"]
    elif has_single:
        active_roles += ["headline"]

    if (ut.get("subline") or "").strip():
        active_roles.append("subline")
    if isinstance(ut.get("benefits"), list) and len(ut.get("benefits")) > 0:
        active_roles.append("benefits")
    if (ut.get("stellentitel") or "").strip():
        active_roles.append("stellentitel")
    if (ut.get("cta") or "").strip():
        active_roles.append("cta")
    if (ut.get("location") or "").strip():
        active_roles.append("standort")

    meta["active_roles"] = active_roles
    spec["meta"] = meta
    state["spec"] = spec
    return state


