import re
from typing import Any, Dict


HEX_RE = re.compile(r"^#([A-Fa-f0-9]{6})$")


def _has_all_sections(text: str) -> bool:
    sections = [
        "Szene & Atmosphaere",
        "Komposition & Layout",
        "Form & Design",
        "Farbwelt & CI",
        "Text & Content (separate_layers)",
        "Balance & Wirkung",
        "Technische Regeln & Engine-Optimierung",
    ]
    idx = -1
    for s in sections:
        new_idx = text.find(s)
        if new_idx <= idx:
            return False
        idx = new_idx
    return True


def PromptPolicyValidator(state: Dict[str, Any]) -> Dict[str, Any]:
    meta = state.get("meta") or {"warnings": [], "errors": [], "norm": {}}
    text = state.get("dalle_prompt") or ""
    spec = state.get("spec") or {}
    p = spec.get("params", {})

    # Laengencheck
    length_ok = 2000 <= len(text) <= 3000
    if not length_ok:
        meta.setdefault("warnings", []).append(f"length_out_of_range:{len(text)}")

    # Abschnitte in exakter Reihenfolge
    if not _has_all_sections(text):
        meta.setdefault("errors", []).append("sections_order_invalid")

    # separate_layers Flag
    if 'text_rendering: "separate_layers"' not in text:
        meta.setdefault("errors", []).append("separate_layers_missing")

    # CI-Farben gueltig
    colors = p.get("ci_colors", {})
    for k in ("primary", "secondary", "accent", "background"):
        v = colors.get(k, "")
        if not HEX_RE.match(v):
            meta.setdefault("errors", []).append(f"ci_invalid:{k}")

    # Slider vorhanden
    sliders = p.get("sliders", {})
    for k in ("image_text_ratio", "container_transparency", "element_spacing", "container_padding", "shadow_intensity"):
        if not sliders.get(k):
            meta.setdefault("errors", []).append(f"slider_missing:{k}")

    # Vollbild erzwingt 100 %
    itrp = str(sliders.get("image_text_ratio") or "").strip()
    if not itrp.startswith("100"):
        meta.setdefault("errors", []).append("image_text_ratio_not_100")

    # Regel: Alle Textelemente als Overlays, nicht im Bildmotiv
    lowered = text.lower()
    overlay_required = "separate_layers" in lowered or "overlays" in lowered
    if not overlay_required:
        forbidden = [
            "schreibe text ins bild",
            "schrift im motiv",
            "text ins bild",
            "texte ins motiv",
        ]
        if any(f in lowered for f in forbidden):
            meta.setdefault("errors", []).append("text_in_image_forbidden")

    # Headline-Pflicht: entweder headline oder (headline_1 & headline_2)
    ut = spec.get("user_texts", {})
    dual_ok = bool((ut.get("headline_1") or "").strip() and (ut.get("headline_2") or "").strip())
    single_ok = bool((ut.get("headline") or "").strip())
    if not (dual_ok or single_ok):
        meta.setdefault("errors", []).append("headline_missing")

    state["meta"] = meta
    return state


