from typing import Any, Dict
import re


TEMPLATE = (
    "Szene & Atmosphaere\n"
    "Ein einfühlsames Recruiting-Motiv in {location}. Die Stimmung ist {motiv_quality} mit {motiv_style}er Note. "
    "Sanftes {lighting_type}; {framing} für Nähe und Präsenz. Dezente Struktur unterstützt eine organisch-fließende Bildsprache.\n\n"
    "Komposition & Layout\n"
    "{comp_block}\n"
    "{slider_line}\n\n"
    "Form & Design\n"
    "layout_style: {layout_style}. Container: {container_shape} mit {corner_radius} Ecken. border_style: {border_style} (dezent). "
    "texture_style: {texture_style} (matt, haptisch). background_treatment: {background_treatment}. accent_elements: {accent_elements} (sparsam, rhythmisch entlang der Diagonale). "
    "Standort-Overlay erhaelt ein kleines Standortpin-Icon vor dem Text (Overlay-Icon, kein Text im Motiv).\n\n"
    "Farbwelt & CI\n"
    "Verwende ausschließlich: primary {primary}, secondary {secondary}, accent {accent}, background {background}. "
    "Kontrastreiche Lesbarkeit auf halbtransparenten Containern; natürliche Hauttöne beibehalten; Akzentfarbe nur für minimale Highlights.\n\n"
    "Text & Content (separate_layers)\n"
    "Kein Text im Bild, alle Texte als separate_layers; Umlaute im Overlay als ae/oe/ue/ss.\n"
    "- Standort (klein): \"{location}\"\n"
    "{headline_block}"
    "- Subline (mittel): \"{subline}\"\n"
    "- Benefits (Liste, mittel):\n{benefits_block}"
    "- Stellentitel (sekundär): \"{stellentitel}\"\n"
    "- CTA (hoch sichtbar): \"{cta}\"\n\n"
    "Balance & Wirkung\n"
    "Das Motiv trägt die emotionale Hauptwirkung; Textcontainer schweben leicht darüber. "
    "Halbtransparenz und sanfte Schatten erzeugen Tiefe ohne Dominanz. "
    "Klarer Negativraum und konsistente Abstände sorgen für ruhige, professionelle Wirkung.\n\n"
    "Technische Regeln & Engine-Optimierung\n"
    "text_rendering: \"separate_layers\". 1080×1080, social-ready, keine Rahmen/Wasserzeichen/Logos. "
    "Kein Text im Bild."
)


def _build_headline_block(ut: Dict[str, Any]) -> str:
    h1 = (ut.get("headline_1") or "").strip()
    h2 = (ut.get("headline_2") or "").strip()
    h = (ut.get("headline") or "").strip()
    if h1 and h2:
        return (
            "- Headline (dual, größte Gewichtung):\n"
            f"  - headline_1: \"{h1}\"\n"
            f"  - headline_2: \"{h2}\"\n"
        )
    else:
        return f"- Headline (große Gewichtung): \"{h}\"\n"


def _build_benefits_block(benefits: Any) -> str:
    lines = []
    if isinstance(benefits, list):
        for b in benefits:
            if b is None:
                continue
            s = str(b).strip()
            if not s:
                continue
            lines.append(f"  - \"{s}\"\n")
    return "".join(lines)


def _extend_if_too_short(text: str) -> str:
    # Wenn <2000 Zeichen, ergaenze gezielt Szenen-/Kompositions-/Balance-Saetze.
    if len(text) >= 2000:
        return text
    filler_scene = (
        " Die Stimmung bleibt konzentriert und respektvoll, ohne visuelle Ueberladung. "
        " Dezente Tiefenstaffelung foerdert Lesbarkeit in allen Lichtsituationen."
    )
    filler_comp = (
        " Ueber die Diagonale werden Negativraeume bewusst freigehalten, sodass "
        " zentrale Aussagen klar strukturiert und jederzeit erfassbar sind."
    )
    filler_balance = (
        " Das Zusammenspiel aus Transparenzen und Schatten staerkt Ruhe und Orientierung, "
        " waehrend die dynamische Linie fuer praesente, aber unaufdringliche Aufmerksamkeit sorgt."
    )
    # Fuege nach den jeweiligen Abschnittstiteln an
    text = text.replace("Ein einfühlsames Recruiting-Motiv", "Ein einfühlsames Recruiting-Motiv" + filler_scene, 1)
    text = text.replace("Komposition & Layout\n", "Komposition & Layout\n" + filler_comp, 1)
    text = text.replace("Balance & Wirkung\n", "Balance & Wirkung\n" + filler_balance, 1)
    return text


def _trim_if_too_long(text: str) -> str:
    if len(text) <= 3000:
        return text
    # Straffe Adjektivketten/Redundanzen in den 3 Bloecken, simple Heuristik via Ersetzungen
    replacements = {
        "organisch-fließende ": "organische ",
        "ruhig und professionell": "professionell",
        "Kontrastreiche ": "Klare ",
        "sanfte Schatten": "Schatten",
    }
    for a, b in replacements.items():
        text = text.replace(a, b)
        if len(text) <= 3000:
            break
    # Falls immer noch zu lang, hart kuerzen am Ende
    return text[:3000]


def PromptBuilder(state: Dict[str, Any]) -> Dict[str, Any]:
    spec = state.get("spec") or {}
    ut = spec.get("user_texts", {})
    p = spec.get("params", {})
    sliders = p.get("sliders", {})
    colors = p.get("ci_colors", {})

    headline_block = _build_headline_block(ut)
    benefits_block = _build_benefits_block(ut.get("benefits"))

    # Komposition & Slider dynamisch je nach Layout/Slider
    layout_id = p.get("layout_id", "")
    ratio_raw = sliders.get("image_text_ratio", "")
    m = re.search(r"\d+", str(ratio_raw))
    ratio_val = int(m.group(0)) if m else None
    full_bg_ids = {
        "skizze3_centered_layout",
        "skizze4_diagonal_layout",
        "skizze5_asymmetric_layout",
        "skizze6_grid_layout",
        "skizze9_dual_headline_layout",
    }
    if layout_id in full_bg_ids or ratio_val == 100:
        comp_block = (
            f"layout_id: {layout_id}. Das Motiv füllt 100 % der Leinwand als Vollbild-Hintergrund; "
            "Textcontainer folgen der definierten Hierarchie (Headline → Subline → Benefits → Stellentitel → CTA → Standort)."
        )
    else:
        comp_block = (
            f"layout_id: {layout_id}. Klares Split-Layout gemäß Slider: ausgewogene Text-/Bildspalte, "
            "konsistente Abstände und sauberer Negativraum; Hierarchie: Headline → Subline → Benefits → Stellentitel → CTA → Standort."
        )

    slider_line = (
        "Slider (fix): "
        f"container_transparency {sliders.get('container_transparency', '')}, "
        f"element_spacing {sliders.get('element_spacing', '')}, "
        f"container_padding {sliders.get('container_padding', '')}, "
        f"shadow_intensity {sliders.get('shadow_intensity', '')}, "
        f"image_text_ratio {sliders.get('image_text_ratio', '')}."
    )

    # Standort-Platzierungsempfehlung (oben links als Default; diagonal → oben rechts)
    loc_guidance = "top-left; single line; high contrast"
    if isinstance(layout_id, str) and "diagonal" in layout_id:
        loc_guidance = "top-right; single line; high contrast"

    text = TEMPLATE.format(
        location=ut.get("location", ""),
        motiv_quality=p.get("motiv_quality", ""),
        motiv_style=p.get("motiv_style", ""),
        lighting_type=p.get("lighting_type", ""),
        framing=p.get("framing", ""),
        comp_block=comp_block,
        slider_line=slider_line,
        layout_style=p.get("layout_style", ""),
        container_shape=p.get("container_shape", ""),
        corner_radius=p.get("corner_radius", ""),
        border_style=p.get("border_style", ""),
        texture_style=p.get("texture_style", ""),
        background_treatment=p.get("background_treatment", ""),
        accent_elements=p.get("accent_elements", ""),
        primary=colors.get("primary", ""),
        secondary=colors.get("secondary", ""),
        accent=colors.get("accent", ""),
        background=colors.get("background", ""),
        headline_block=headline_block,
        subline=ut.get("subline", ""),
        benefits_block=benefits_block,
        stellentitel=ut.get("stellentitel", ""),
        cta=ut.get("cta", ""),
        # Zusatz für Standort-Zeile via nachfolgendem Replace (einfachster Eingriff)
    )

    # Standort-Zeile mit Positionshinweis ergänzen
    text = text.replace(
        f'- Standort (klein): "{ut.get("location", "")}"',
        f'- Standort (klein): "{ut.get("location", "")}" — {loc_guidance}'
    )

    text = _extend_if_too_short(text)
    text = _trim_if_too_long(text)

    meta = state.get("meta") or {"warnings": [], "errors": [], "norm": {}}
    meta["length_ok"] = 2000 <= len(text) <= 3000
    if not meta["length_ok"]:
        meta.setdefault("warnings", []).append(f"Prompt length={len(text)}")

    state["dalle_prompt"] = text
    state["meta"] = meta
    return state


