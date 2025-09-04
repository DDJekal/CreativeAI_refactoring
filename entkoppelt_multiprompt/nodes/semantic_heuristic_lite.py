from typing import Any, Dict, List


def _heur_text_areas(has_dual: bool) -> List[Dict[str, str]]:
    if has_dual:
        return [
            {"role": "headline_1", "relative_position": "oben links", "size_hint": "gross", "notes": "diagonal start"},
            {"role": "headline_2", "relative_position": "oben mitte", "size_hint": "gross", "notes": "diagonal fortsetzung"},
            {"role": "subline", "relative_position": "mitte links", "size_hint": "mittel"},
            {"role": "benefits", "relative_position": "mitte mitte", "size_hint": "mittel"},
            {"role": "stellentitel", "relative_position": "unten mitte", "size_hint": "mittel"},
            {"role": "cta", "relative_position": "unten rechts", "size_hint": "gross", "notes": "sichtbarkeit"},
            {"role": "standort", "relative_position": "oben rechts", "size_hint": "klein", "notes": "standortpin-icon vor text"},
        ]
    return [
        {"role": "headline", "relative_position": "oben links", "size_hint": "gross", "notes": "diagonal start"},
        {"role": "subline", "relative_position": "mitte links", "size_hint": "mittel"},
        {"role": "benefits", "relative_position": "mitte mitte", "size_hint": "mittel"},
        {"role": "stellentitel", "relative_position": "unten mitte", "size_hint": "mittel"},
        {"role": "cta", "relative_position": "unten rechts", "size_hint": "gross", "notes": "sichtbarkeit"},
        {"role": "standort", "relative_position": "oben rechts", "size_hint": "klein", "notes": "standortpin-icon vor text"},
    ]


def SemanticHeuristicLite(state: Dict[str, Any]) -> Dict[str, Any]:
    spec = state.get("spec") or {}
    p = spec.get("params", {})
    ut = spec.get("user_texts", {})
    layout_id = (p.get("layout_id") or "").lower()
    has_dual = bool((ut.get("headline_1") or "").strip() and (ut.get("headline_2") or "").strip())

    overview = "Diagonal, Vollbild-Hintergrund, Text entlang Diagonale" if "diagonal" in layout_id else "Vollbild-Hintergrund, strukturierte Overlays"
    semantics = {
        "layout_overview": overview,
        "text_areas": _heur_text_areas(has_dual),
        "image_areas": [{"area": "background", "relative_position": "vollbild"}],
        "positioning_logic": [
            "diagonale Leserichtung",
            "Negativraum fuer Lesbarkeit",
            "konsistente Abstaende laut Slider",
            "CTA nicht ueber komplexem Motiv",
        ],
    }
    state["semantics_heur"] = semantics
    return state


