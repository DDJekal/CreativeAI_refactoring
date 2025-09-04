import json
from typing import Any, Dict


def _llm_extract_semantics(prompt_text: str) -> Dict[str, Any]:
    """Stub fuer LLM-Extraktion. Gibt eine minimale, valide Struktur zurueck.

    In produktiv kann hier ein Aufruf an ein Modell erfolgen, das strikt JSON
    liefert. Bei Fehlern wird eine leere Struktur zurueckgegeben.
    """
    # Minimaler Default ohne echte Extraktion
    return {
        "layout_overview": "Diagonal, Vollbild-Hintergrund (aus Beschreibung)",
        "text_areas": [],
        "image_areas": [{"area": "background", "relative_position": "vollbild"}],
        "positioning_logic": [
            "Leserichtung diagonal",
            "Overlays auf Negativraum platzieren",
        ],
    }


def SemanticFromPrompt(state: Dict[str, Any]) -> Dict[str, Any]:
    text = state.get("dalle_prompt") or ""
    try:
        extracted = _llm_extract_semantics(text)
        state["semantics_llm"] = extracted
    except Exception as exc:  # pragma: no cover - defensive
        meta = state.get("meta") or {"warnings": [], "errors": [], "norm": {}}
        meta.setdefault("warnings", []).append(f"semantics_llm_failed: {exc}")
        state["meta"] = meta
        state["semantics_llm"] = None
    return state


