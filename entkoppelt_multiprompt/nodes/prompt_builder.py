from typing import Any, Dict
import re


# --- Globale Normalisierung fuer Szene/Licht/Atmosphaere ---
_SCENE_ATMO_MAP = {
    # Lichttypen / generische Begriffe
    "ambient light": "soft side studio light, warm 3200 K, subtle fill",
    "sanftes licht": "soft daylight with broad bounce, 5200–5600 K, controlled highlights",
    "sanftes": "soft daylight with broad bounce, 5200–5600 K, controlled highlights",
    "natuerliches tageslicht": "soft daylight, bounce fill, 5200–5600 K",
    "natürliches tageslicht": "soft daylight, bounce fill, 5200–5600 K",
    "studio-beleuchtung": "soft side studio light with large softbox, warm 3200 K",
    "dramatisches licht": "directional key light, high contrast, 4300 K, controlled spill",
    "kontrastreiches licht": "harder key with controlled fill, 5000 K, defined shadows",
    "neon-beleuchtung": "neon accent lights, cool 6500 K, controlled bloom",
    "kerzenlicht": "practical candlelight, warm 2700–3000 K, soft falloff",
    "mondlicht": "moonlit ambience, cool 7000 K, soft rim",
    "spotlight": "narrow beam spotlight, defined falloff, 5000 K",
    "ambient": "soft overall ambience, gentle fill 5200–5600 K",
    # Atmosphaere generisch
    "organisch-fließende bildsprache": "low-frequency background, gentle curves, no distracting patterns",
    "organisch fliessende bildsprache": "low-frequency background, gentle curves, no distracting patterns",
    "dezent strukturiert": "subtle low-frequency texture, no noise patterns",
    "ruhig & beruhigend": "calm, low contrast background, soft transitions",
    "professionell & vertrauensvoll": "clean clinical grading, neutral balance, midtone separation",
    "authentisch & warm": "documentary soft grain, warm tonal bias +3, subtle vignetting",
}

def _normalize_scene_term(value: str) -> str:
    if not isinstance(value, str):
        return value
    key = value.strip().lower()
    # direkte Treffer
    if key in _SCENE_ATMO_MAP:
        return _SCENE_ATMO_MAP[key]
    # Teilstring-Heuristiken
    if "ambient light" in key:
        return _SCENE_ATMO_MAP["ambient light"]
    if "sanft" in key and "licht" in key:
        return _SCENE_ATMO_MAP["sanftes licht"]
    if "organisch" in key and ("fliess" in key or "fließ" in key):
        return _SCENE_ATMO_MAP["organisch fliessende bildsprache"]
    if "dezent" in key and "struktur" in key:
        return _SCENE_ATMO_MAP["dezent strukturiert"]
    return value


def _normalize_scene_fields(params: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(params, dict):
        return params
    out = dict(params)
    # Ziel-Felder: lighting_type, mood_atmosphere, season_weather optional
    for fld in ["lighting_type", "mood_atmosphere", "season_weather"]:
        if fld in out and isinstance(out[fld], str):
            out[fld] = _normalize_scene_term(out[fld])
    return out


TEMPLATE = (
    "Szene & Atmosphaere\n"
    "Ein {mood_atmosphere}es Recruiting-Motiv in {location}. Die Stimmung ist {motiv_quality} mit {motiv_style}er Note. "
    "Kunststil: {art_style}. Atmosphäre: {season_weather}. "
    "Sanftes {lighting_type}; {framing} für Nähe und Präsenz. Dezente Struktur unterstützt eine organisch-fließende Bildsprache.\n\n"
    "Komposition & Layout\n"
    "{comp_block}\n"
    "{slider_line}\n\n"
    "Form & Design\n"
    "layout_style: {layout_style}. {container_shape} border_style: {border_style} (dezent). "
    "texture_style: {texture_style} (matt, haptisch). background_treatment: {background_treatment}. accent_elements: {accent_elements} (sparsam, rhythmisch entlang der Diagonale). "
    "Standort-Overlay erhaelt ein kleines Standortpin-Icon vor dem Text (Overlay-Icon, kein Text im Motiv).\n\n"
    "Farbwelt & CI\n"
    "Verwende ausschließlich: primary {primary}, secondary {secondary}, accent {accent}, background {background}. "
    "Kontrastreiche Lesbarkeit auf halbtransparenten Containern; natürliche Hauttöne beibehalten; Akzentfarbe nur für minimale Highlights.\n\n"
    "Text & Content (separate_layers)\n"
    "Alle Textelemente werden ausschließlich als separate Overlays gerendert, nicht im Bildmotiv selbst. Alle Texte als separate_layers; Umlaute im Overlay als ae/oe/ue/ss.\n"
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
    "Alle Textelemente werden ausschließlich als separate Overlays gerendert, nicht im Bildmotiv selbst."
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
    """Baut den Benefits-Block: dedupliziert case-insensitiv und begrenzt auf max. 3 Zeilen."""
    if not isinstance(benefits, list):
        return ""
    lines: list[str] = []
    seen: set[str] = set()
    for b in benefits:
        if b is None:
            continue
        s = str(b).strip()
        if not s:
            continue
        key = s.lower()
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"  - \"{s}\"\n")
        if len(lines) == 3:
            break
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


def _translate_container_shape(container_shape: str) -> str:
    """Übersetzt Container-Shape-IDs in semantische Beschreibungen."""
    translations = {
        "Abgerundet": "Klassisch abgerundete Text-Container mit gleichmäßigen, sanften Ecken und freundlicher, einladender Form. Die Container haben konsistente Rundungen an allen Ecken.",
        "Scharf": "Scharfkantige Text-Container mit präzisen, geraden Linien und moderner, minimalistischer Ästhetik. Die Container haben keine Rundungen, nur scharfe 90-Grad-Ecken.",
        "Organisch": "Organisch geformte Text-Container mit unregelmäßigen, natürlichen Kanten und fließenden, weichen Übergängen. Die Container haben unregelmäßige, organische Formen.",
        "Geometrisch": "Geometrisch präzise Text-Container mit mathematisch exakten Formen und klaren, technischen Linien. Die Container haben präzise geometrische Formen.",
        "Capsule": "Kapselartige Text-Container mit extrem abgerundeten Ecken und sanfter, medizinisch-technischer Form. Die Container sind sehr stark abgerundet, fast oval.",
        "Ribbon": "Bandartige Text-Container mit minimalen Rundungen und schlanker, eleganter Form. Die Container haben sehr subtile Rundungen.",
        "Tag": "Tag-ähnliche Text-Container mit charakteristischer Form und moderner, web-orientierter Ästhetik. Die Container haben eine spezielle Tag-Form.",
        "Asymmetrisch": "Asymmetrische Text-Container mit unregelmäßigen, unkonventionellen Formen und zeitgemäßer, experimenteller Ästhetik. Die Container haben unregelmäßige, asymmetrische Formen.",
        "Hexagon": "Sechseckige (hexagonale) Text-Container mit geometrisch präzisen Kanten und moderner, tech-orientierter Ästhetik. Die Container haben sechs gleichmäßige Seiten mit scharfen, mathematisch exakten Ecken.",
        "Diamond": "Rautenförmige (diamantene) Text-Container mit diagonaler Ausrichtung und dynamischer, energiegeladener Form. Die Container sind als Rauten geformt mit vier gleichmäßigen Seiten.",
        "Pill": "Kapselartige (pill-förmige) Text-Container mit sehr stark abgerundeten Ecken und sanfter, medizinisch-technischer Form. Die Container sind oval-kapselartig geformt.",
        "Rounded Square": "Quadratische Text-Container mit gleichmäßig abgerundeten Ecken und ausgewogener, klassischer Form. Die Container sind quadratisch mit abgerundeten Ecken.",
        "Soft Rectangle": "Sanft abgerundete Rechteck-Container mit weichen Übergängen und freundlicher, einladender Form. Die Container sind rechteckig mit sanften Rundungen.",
        "Wave": "Wellenförmige, organisch fließende Text-Container mit sanften, unregelmäßigen Kanten und natürlicher, flüssiger Form. Die Container haben wellenartige, geschwungene Ränder.",
        "Cloud": "Wolkenartige, weiche Text-Container mit unregelmäßigen, organischen Kanten und sanft geschwungenen Formen. Die Container ähneln Wolken mit weichen, unregelmäßigen Rändern.",
        "Bubble": "Blasenartige, runde Text-Container mit sehr weichen, organischen Kanten und spielerischer, freundlicher Form. Die Container sind sehr rund und blasenartig geformt.",
        "Cut Corner": "Text-Container mit abgeschnittenen Ecken und geometrisch präzisen Schnitten für moderne, technische Optik. Die Container haben abgeschnittene Ecken mit geraden Schnitten.",
        "Notched": "Text-Container mit eingekerbten Seiten und unkonventionellen, modernen Formen. Die Container haben Kerben oder Einbuchtungen in den Seiten.",
        "Floating": "Schwebende Text-Container mit sanften Schatten und leichter, luftiger Erscheinung. Die Container schweben mit sanften Schatten über dem Hintergrund.",
        "Card Stack": "Gestapelte Karten-Container mit mehrschichtiger Tiefe und moderner, hierarchischer Anordnung. Die Container sind wie gestapelte Karten angeordnet.",
    }
    return translations.get(container_shape, f"Container: {container_shape} mit definierten Ecken.")


def PromptBuilder(state: Dict[str, Any]) -> Dict[str, Any]:
    spec = state.get("spec") or {}
    ut = spec.get("user_texts", {})
    p = spec.get("params", {})
    sliders = p.get("sliders", {})
    colors = p.get("ci_colors", {})

    # Zentrale Normalisierung anwenden (nicht-invasiv; nur relevante Felder)
    p = _normalize_scene_fields(p)

    headline_block = _build_headline_block(ut)
    benefits_block = _build_benefits_block(ut.get("benefits"))

    # Komposition zuerst preset-basiert, Prozente nur Fallback
    layout_id = p.get("layout_id", "")
    geometry_preset = (p.get("geometry_preset") or "").strip()
    if geometry_preset:
        preset_desc = {
            "vertical_split": "Zweispaltig: Links Text, rechts Motiv; gemeinsame linke Kante, definierter Gutter, sichere Ränder 3 %.",
            "vertical_split_left": "Zweispaltig: Links Motiv, rechts Text; klare Spaltenkante, definierter Gutter, sichere Ränder 3 %.",
            "centered_overlay": "Zentrierte Container-Gruppe über Vollbildmotiv; ruhige Hierarchie Standort → Headline → Subline → Benefits → Stellentitel → CTA.",
            "diagonal_overlay": "Diagonale Container-Abfolge; CTA links unten, Standort oben rechts.",
            "asymmetric_overlay": "Asymmetrische Containerverteilung mit klarer Leserichtung; CTA rechts außen.",
            "grid_overlay": "Grid-basierte Container-Gruppe; keine Headline, Fokus auf Subline/Stellentitel.",
            "split_layout": "Oberer Bereich Textstapel, unterer Bereich Motiv (Split).",
            "hero_layout": "Hero: Motiv oben als Bühne, Text unten; CTA rechts oben reduziert.",
            "dual_headline_full_bg": "Vollbild-Motiv mit zwei getrennten Headline-Containern; Subline, Titel und CTA darunter.",
            "modern_split": "Moderner Split; großzügige Negativräume; schmale Textspalte.",
            "infographic": "Infografik-Layout; Informationsmodule und CTA klar getrennt.",
            "magazine": "Editorial/Magazine; großzügige Weißräume, klare Typo-Hierarchie.",
            "portfolio": "Portfolio; große Präsentationsflächen, knapper Text, klare CTA.",
            "circular_spotlight": "Zirkulärer Motiv-Schwerpunkt; Text radial angeordnet.",
            "diagonal_cascade": "Diagonale Kaskade; CTA als Ruheanker.",
            "zigzag_flow": "Zickzack-Fluss der Container; gestufte Blickführung.",
            "wave_flow": "Organische Wellenlinie; CTA stabil am Ende.",
            "masonry_layout": "Masonry-Anmutung; konsistente Abstände, klare Priorisierung.",
            "hexagon_grid": "Hexagonales Grid; präzise Kanten, reduzierter CTA.",
            "triangle_grid": "Trianguläres Grid; klare Geometrie, stabile Leserichtung.",
            "magazine_spread": "Doppelseiten-Anmutung; CTA im sichtbaren Drittel.",
            "newspaper_layout": "Zeitungs-Raster; Spaltenlogik, ruhiger CTA.",
            "story_format": "Story-Format; klare Sequenz, CTA im unteren Drittel.",
        }
        comp_block = preset_desc.get(geometry_preset, f"Standardisierte Containeranordnung gemäß Preset {geometry_preset}.")
    else:
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
                f"layout_id: {layout_id}. Bildanteil 100 %, Textanteil 0 %. "
                "Textcontainer liegen als Overlays im Negativraum und folgen der definierten Hierarchie (Standort → Headline → Subline → Benefits → Stellentitel → CTA). "
                "Vertikale Abstände exakt gleich groß; sichere Ränder 3 %."
            )
        else:
            img_pct_target = max(55, min(85, ratio_val if isinstance(ratio_val, int) else 60))
            txt_pct_target = max(0, 100 - img_pct_target)
            comp_block = (
                f"layout_id: {layout_id}. Exaktes Split-Layout: Bildspalte {img_pct_target} %, Textspalte {txt_pct_target} %; "
                "Gutter 5–6 %, sichere Ränder 3 %. Vertikale Abstände exakt gleich groß; "
                "gemeinsame linke Kante für Textcontainer; CTA bewusst eingerückt. Mindestregel: Bildanteil ≥ 55 %."
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

    # Semantische Übersetzung für Container-Shape
    container_shape_desc = _translate_container_shape(p.get("container_shape", ""))

    text = TEMPLATE.format(
        location=ut.get("location", ""),
        mood_atmosphere=p.get("mood_atmosphere", ""),
        motiv_quality=p.get("motiv_quality", ""),
        motiv_style=p.get("motiv_style", ""),
        art_style=p.get("art_style", ""),
        season_weather=p.get("season_weather", ""),
        lighting_type=p.get("lighting_type", ""),
        framing=p.get("framing", ""),
        comp_block=comp_block,
        slider_line=slider_line,
        layout_style=p.get("layout_style", ""),
        container_shape=container_shape_desc,  # Semantische Übersetzung verwenden
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
    # Protokolliere Normalisierung fuer Debug/Transparenz
    meta.setdefault("norm", {}).update({
        "lighting_type": p.get("lighting_type"),
        "mood_atmosphere": p.get("mood_atmosphere"),
        "season_weather": p.get("season_weather"),
    })

    state["dalle_prompt"] = text
    state["meta"] = meta
    return state


