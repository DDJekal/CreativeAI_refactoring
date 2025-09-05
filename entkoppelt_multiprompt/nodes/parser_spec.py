import re
from typing import Any, Dict, List, Optional


HEX_RE = re.compile(r"^#([A-Fa-f0-9]{6})$")


def _strip(s: Optional[str]) -> Optional[str]:
    if s is None:
        return None
    return s.strip()


def _parse_list_block(block: str) -> List[str]:
    lines: List[str] = []
    for line in block.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("- "):
            val = line[2:].strip()
        elif line.startswith("* "):
            val = line[2:].strip()
        else:
            val = line
        if val:
            lines.append(val)
    return lines


def _to_int(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    m = re.findall(r"\d+", value)
    if not m:
        return None
    try:
        return int(m[0])
    except Exception:
        return None


def ParseSpec(state: Dict[str, Any]) -> Dict[str, Any]:
    """Parst einen deutschsprachigen Roh-Block in das Ziel-Schema.

    Erwartet in state["spec"] bereits ein dict ODER in state["spec_raw"] einen String.
    Normalisiert Slider numerisch in meta.norm und validiert CI-Hexe.
    Fehlende Felder werden defensiv als leere Strings/Listen gesetzt.
    """
    meta = state.get("meta") or {"warnings": [], "errors": [], "norm": {}}
    state["meta"] = meta

    if isinstance(state.get("spec"), dict):
        spec = state["spec"]
    else:
        raw = (state.get("spec_raw") or "").replace("\x00", "")

        def _extract(key: str) -> Optional[str]:
            # sucht nach Zeilen wie '- key: value' oder 'key: value'
            pat = re.compile(rf"(^|\n)[- ]*{re.escape(key)}\s*:\s*(.+)")
            m = pat.search(raw)
            return _strip(m.group(2)) if m else None

        def _extract_block(start_key: str, end_keys: List[str]) -> str:
            start = re.search(rf"(^|\n)[- ]*{re.escape(start_key)}\s*:\s*", raw)
            if not start:
                return ""
            start_idx = start.end()
            end_idx = len(raw)
            for k in end_keys:
                m = re.search(rf"\n[- ]*{re.escape(k)}\s*:\s*", raw[start_idx:])
                if m:
                    end_idx = start_idx + m.start()
                    break
            return raw[start_idx:end_idx]

        # USER-TEXTE Felder direkt ziehen
        location = _extract("location") or ""
        headline = _extract("headline") or ""
        headline_1 = _extract("headline_1") or ""
        headline_2 = _extract("headline_2") or ""
        subline = _extract("subline") or ""
        stellentitel = _extract("stellentitel") or ""
        cta = _extract("cta") or ""

        # Benefits-Block (endet vor naechstem Feld oder Abschnitt)
        benefits_block = _extract_block(
            "benefits",
            [
                "stellentitel",
                "cta",
                "GEWAEHLTE PARAMETER",
                "SLIDER",
                "CI-COLORS",
                "CI COLORS",
                "CI COLORS (strict)",
            ],
        )
        benefits = _parse_list_block(benefits_block)

        def _p(key: str) -> str:
            val = _extract(key)
            return val or ""

        layout_id = _p("layout_id")
        layout_style = _p("layout_style")
        geometry_preset = _p("geometry_preset")
        container_shape = _p("container_shape")
        border_style = _p("border_style")
        texture_style = _p("texture_style")
        background_treatment = _p("background_treatment")
        corner_radius = _p("corner_radius")
        accent_elements = _p("accent_elements")
        motiv_quality = _p("motiv_quality")
        motiv_style = _p("motiv_style")
        lighting_type = _p("lighting_type")
        framing = _p("framing")
        art_style = _p("art_style")
        mood_atmosphere = _p("mood_atmosphere")
        season_weather = _p("season_weather")

        # SLIDER Felder direkt ziehen
        image_text_ratio = _extract("image_text_ratio") or ""
        container_transparency = _extract("container_transparency") or ""
        element_spacing = _extract("element_spacing") or ""
        container_padding = _extract("container_padding") or ""
        shadow_intensity = _extract("shadow_intensity") or ""

        # CI COLORS Felder direkt ziehen
        primary = _extract("primary") or ""
        secondary = _extract("secondary") or ""
        accent = _extract("accent") or ""
        background = _extract("background") or ""

        spec = {
            "user_texts": {
                "location": location,
                "headline": headline,
                "headline_1": headline_1,
                "headline_2": headline_2,
                "subline": subline,
                "benefits": benefits or [],
                "stellentitel": stellentitel,
                "cta": cta,
            },
            "params": {
                "layout_id": layout_id,
                "geometry_preset": geometry_preset,
                "layout_style": layout_style,
                "container_shape": container_shape,
                "border_style": border_style,
                "texture_style": texture_style,
                "background_treatment": background_treatment,
                "corner_radius": corner_radius,
                "accent_elements": accent_elements,
                "motiv_quality": motiv_quality,
                "motiv_style": motiv_style,
                "lighting_type": lighting_type,
                "framing": framing,
                "art_style": art_style,
                "mood_atmosphere": mood_atmosphere,
                "season_weather": season_weather,
                "sliders": {
                    "image_text_ratio": image_text_ratio,
                    "container_transparency": container_transparency,
                    "element_spacing": element_spacing,
                    "container_padding": container_padding,
                    "shadow_intensity": shadow_intensity,
                },
                "ci_colors": {
                    "primary": primary,
                    "secondary": secondary,
                    "accent": accent,
                    "background": background,
                },
            },
        }

    # Validierungen/Normalisierung
    # CI Hexe
    for k in ("primary", "secondary", "accent", "background"):
        val = spec["params"]["ci_colors"].get(k) or ""
        if not HEX_RE.match(val):
            meta["errors"].append(f"CI color {k} invalid: {val}")

    # Slider numerisch in meta.norm
    sliders = spec["params"].get("sliders", {})
    norm = meta.get("norm") or {}
    norm["image_text_ratio_pct"] = _to_int(sliders.get("image_text_ratio"))
    norm["container_transparency_pct"] = _to_int(sliders.get("container_transparency"))
    norm["element_spacing_px"] = _to_int(sliders.get("element_spacing"))
    norm["container_padding_px"] = _to_int(sliders.get("container_padding"))
    norm["shadow_intensity_pct"] = _to_int(sliders.get("shadow_intensity"))
    meta["norm"] = norm

    state["spec"] = spec
    state["meta"] = meta
    return state


