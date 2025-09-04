import re
from typing import Any, Dict, List, Optional


HEX = re.compile(r"^#([A-Fa-f0-9]{6})$")


def _norm_slider_val(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        m = re.search(r"\d+", str(value))
        return int(m.group(0)) if m else None
    except Exception:
        return None


def _extract_content_block(prompt: str) -> str:
    # Abschnitt "Text & Content (separate_layers)" bis zur nächsten Überschrift
    m = re.search(r"Text\s*&\s*Content\s*\(separate_layers\)(.*?)(?:\n[A-ZÄÖÜa-z].+?\n|$)", prompt, re.S)
    return m.group(1) if m else ""


def _contains_foreign_strings(content_block: str, allowed_strings: List[str]) -> bool:
    quoted = re.findall(r'"([^\"]+)"', content_block)
    allowed = set([s for s in allowed_strings if s])
    return any(q not in allowed for q in quoted)


def PromptPolicyValidator(state: Dict[str, Any]) -> Dict[str, Any]:
    meta = state.setdefault("meta", {"warnings": [], "errors": [], "norm": {}})
    spec = state.get("spec") or {}
    params = spec.get("params", {})
    ut = spec.get("user_texts", {})

    prompt = state.get("dalle_prompt") or ""
    total_length = len(prompt)

    # 1) Länge prüfen
    if total_length < 2000:
        meta.setdefault("warnings", []).append(f"prompt too short ({total_length}); target 2000–3000")
    if total_length > 3000:
        meta.setdefault("warnings", []).append(f"prompt too long ({total_length}); target 2000–3000")

    # 2) separate_layers Pflicht
    if not re.search(r'text_rendering\s*:\s*"?separate_layers"?', prompt):
        meta.setdefault("errors", []).append('missing `text_rendering: "separate_layers"`')

    # 3) CI Hex vorhanden & valide
    ci = params.get("ci_colors", {}) or {}
    for key in ("primary", "secondary", "accent", "background"):
        val = ci.get(key)
        if not val or not HEX.match(val):
            meta.setdefault("errors", []).append(f"invalid CI color for {key}: {val}")

    # 4) Slider vorhanden & numerisch
    sliders = params.get("sliders", {}) or {}
    required_sliders = ["image_text_ratio", "container_transparency", "element_spacing", "container_padding", "shadow_intensity"]
    for key in required_sliders:
        if key not in sliders:
            meta.setdefault("errors", []).append(f"missing slider: {key}")
        else:
            n = _norm_slider_val(sliders.get(key))
            if n is None:
                meta.setdefault("errors", []).append(f"slider not numeric: {key}={sliders.get(key)}")
            else:
                meta.setdefault("norm", {})[key] = n

    # 5) Headline-Pflicht (single ODER dual)
    has_dual = bool((ut.get("headline_1") or "").strip() and (ut.get("headline_2") or "").strip())
    has_single = bool((ut.get("headline") or "").strip())
    if not (has_dual or has_single):
        meta.setdefault("errors", []).append("headline required (single or dual)")

    # 6) Nur USER-Texte im Content-Block
    content_block = _extract_content_block(prompt)
    allowed_strings: List[str] = []
    allowed_strings.extend([
        ut.get("location"), ut.get("headline"), ut.get("headline_1"), ut.get("headline_2"),
        ut.get("subline"), ut.get("stellentitel"), ut.get("cta")
    ])
    benefits = ut.get("benefits") or []
    if isinstance(benefits, list):
        for b in benefits:
            allowed_strings.append(b)
    if _contains_foreign_strings(content_block, allowed_strings):
        meta.setdefault("warnings", []).append("foreign strings detected in content block (only USER-Texte allowed)")

    # 7) Vollbild-Hinweis, wenn Ratio=100
    ratio = meta.get("norm", {}).get("image_text_ratio")
    if ratio == 100:
        if ("Vollbild" not in prompt) and ("fuellt 100 %" not in prompt) and ("füllt 100 %" not in prompt):
            meta.setdefault("warnings", []).append("image_text_ratio=100 but prompt does not explicitly state full-bleed background")

    state["meta"] = meta
    return state


