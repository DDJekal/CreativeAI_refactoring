from typing import Dict, Any
import logging


RADIUS_MAP: Dict[str, int] = {
    "Klein 8px": 8,
    "Mittel 16px": 16,
    "Gross 24px": 24,
    "Sehr Gross 32px": 32,
    "Auto-Radius": 16,  # Wird dynamisch berechnet
}

# Erweiterte Design-Kategorien
LAYOUT_STYLES = {
    "abgerundet_modern": {"name": "Abgerundet Modern", "description": "freundlich, weich"},
    "scharf_zeitgemaess": {"name": "Scharf & Zeitgemäß", "description": "klar, techy"},
    "organisch_fliessend": {"name": "Organisch & Fließend", "description": "wellig, human"},
    "geometrisch_praezise": {"name": "Geometrisch & Präzise", "description": "Grid, Ratio"},
    "neon_tech": {"name": "Neon Tech", "description": "Glow, High-Contrast"},
    "editorial_clean": {"name": "Editorial Clean", "description": "viel Negativraum, Typo-Fokus"},
    "soft_neumorph": {"name": "Soft Neumorph", "description": "sanfte Erhebungen/Vertiefungen"},
    "glassmorph_minimal": {"name": "Glassmorph Minimal", "description": "Frosted + Subtle Shadow"},
    "clay_ui": {"name": "Clay UI", "description": "plastisch, matte Flächen"},
    "warm_documentary": {"name": "Warm Documentary", "description": "analoge Anmutung, Filmgrain"},
}

CONTAINER_SHAPES = {
    "abgerundet": {"name": "Abgerundet", "radius": 16},
    "scharf": {"name": "Scharf", "radius": 0},
    "organisch": {"name": "Organisch", "radius": "variable"},
    "geometrisch": {"name": "Geometrisch", "radius": 8},
    "capsule": {"name": "Capsule", "radius": 50},
    "ribbon": {"name": "Ribbon", "radius": 4},
    "tag": {"name": "Tag", "radius": 12},
}

BORDER_STYLES = {
    "keine": {"border": None, "shadow": None},
    "weicher_schatten": {"border": None, "shadow": {"blur": 16, "opacity": 0.12, "dx": 0, "dy": 4}},
    "harte_konturen": {"border": {"style": "solid", "width": 2}, "shadow": {"blur": 6, "opacity": 0.20, "dx": 0, "dy": 2}},
    "gradient_rand": {"border": {"style": "gradient", "width": 2}, "shadow": {"blur": 10, "opacity": 0.12, "dx": 0, "dy": 3}},
    "doppelstrich": {"border": {"style": "double", "width": 3}, "shadow": {"blur": 8, "opacity": 0.15, "dx": 0, "dy": 2}},
    "innenlinie": {"border": {"style": "inset", "width": 1}, "shadow": {"blur": 4, "opacity": 0.10, "dx": 0, "dy": 1}},
    "emboss": {"border": {"style": "ridge", "width": 2}, "shadow": {"blur": 6, "opacity": 0.25, "dx": 0, "dy": 2}},
    "outline_glow": {"border": {"style": "solid", "width": 1}, "shadow": {"blur": 12, "opacity": 0.30, "dx": 0, "dy": 0}},
}

TEXTURE_STYLES = {
    "farbverlauf": {"type": "gradient", "intensity": "medium"},
    "glaseffekt": {"type": "glass", "intensity": "high"},
    "matte_oberflaeche": {"type": "matte", "intensity": "low"},
    "strukturiert": {"type": "pattern", "intensity": "medium"},
    "paper_grain": {"type": "paper_grain", "intensity": "low"},
    "film_grain": {"type": "film_grain", "intensity": "low"},
    "noise_gradient": {"type": "noise", "intensity": "low"},
    "subtle_pattern": {"type": "dots", "intensity": "very_low"},
    "soft_neumorph": {"type": "neumorph", "intensity": "medium"},
    "emboss_deboss": {"type": "relief", "intensity": "high"},
}

BACKGROUND_TREATMENTS = {
    "transparent": {"type": "transparent", "opacity": 0.0},
    "vollflaechig": {"type": "solid", "opacity": 1.0},
    "gradient": {"type": "gradient", "opacity": 0.9},
    "subtiles_muster": {"type": "pattern", "opacity": 0.8},
    "duotone_motivtint": {"type": "duotone", "opacity": 0.85},
    "vignette_soft": {"type": "vignette", "opacity": 0.9},
    "depth_layers": {"type": "layered", "opacity": 0.8},
}

TYPOGRAPHY_STYLES = {
    "humanist_sans": {"family": "humanist", "weight": "normal", "style": "sans"},
    "grotesk_bold": {"family": "grotesk", "weight": "bold", "style": "sans"},
    "serif_editorial": {"family": "serif", "weight": "normal", "style": "serif"},
    "mono_detail": {"family": "monospace", "weight": "normal", "style": "mono"},
    "rounded_sans": {"family": "rounded", "weight": "normal", "style": "sans"},
}

PHOTO_TREATMENTS = {
    "natural_daylight": {"contrast": "soft", "temperature": "neutral", "grain": "none"},
    "cinematic_warm": {"contrast": "medium", "temperature": "warm", "grain": "light"},
    "clean_clinic": {"contrast": "high", "temperature": "cool", "grain": "none"},
    "documentary_soft_grain": {"contrast": "soft", "temperature": "neutral", "grain": "medium"},
    "duotone_subtle": {"contrast": "medium", "temperature": "custom", "grain": "none"},
    "bokeh_light": {"contrast": "soft", "temperature": "neutral", "grain": "none"},
}

DEPTH_STYLES = {
    "soft_shadow_stack": {"shadows": 2, "opacity": 0.18, "blur": 16},
    "drop_inner_shadow": {"shadows": 2, "opacity": 0.25, "blur": 12},
    "card_elevation_1": {"shadows": 1, "opacity": 0.12, "blur": 8},
    "card_elevation_2": {"shadows": 1, "opacity": 0.16, "blur": 12},
    "card_elevation_3": {"shadows": 1, "opacity": 0.20, "blur": 16},
}

BORDER_PRESETS: Dict[str, Dict[str, Any]] = {
    "Weicher Schatten": {"border": None, "shadow": {"blur": 16, "opacity": 0.12, "dx": 0, "dy": 4}},
    "Harte Konturen": {"border": {"style": "solid", "width": 2}, "shadow": {"blur": 6, "opacity": 0.20, "dx": 0, "dy": 2}},
    "Keine Grenzen": {"border": None, "shadow": {"blur": 8, "opacity": 0.10, "dx": 0, "dy": 2}},
    "Gradient-Rand": {"border": {"style": "gradient", "width": 2}, "shadow": {"blur": 10, "opacity": 0.12, "dx": 0, "dy": 3}},
}

ZONE_ROLE_MAP: Dict[str, str] = {
    "headline_block": "headline",
    "headline_1_block": "headline",
    "headline_2_block": "headline",
    "subline_block": "subline",
    "benefits_block": "benefits",
    "cta_block": "cta",
    "stellentitel_block": "title",
    "logo_block": "logo",
    "standort_block": "meta",
    "company_block": "meta",
    "infographic_block": "data",
    "content_block": "content",
}

FORCE_OVERRIDE_ROLES = {"headline", "subline", "benefits", "title", "cta"}


def resolve_style(
    zone_name: str,
    design: Dict[str, Any],
    ci_colors: Dict[str, str],
    *,
    layout_type: str,
    transparency: float,
    zone_role: str = "generic",
) -> Dict[str, Any]:
    """
    Erzeugt ein konsistentes container_style basierend auf Design-/CI-Parametern.
    Erweiterte Version mit neuen Design-Kategorien.
    """
    # Layout-Style (neue Kategorie)
    layout_style = design.get("layout_style", "abgerundet_modern")
    layout_config = LAYOUT_STYLES.get(layout_style, LAYOUT_STYLES["abgerundet_modern"])
    
    # Container-Form (erweitert)
    container_shape = design.get("container_shape", "abgerundet")
    shape_config = CONTAINER_SHAPES.get(container_shape, CONTAINER_SHAPES["abgerundet"])
    
    # Border-Style (erweitert)
    border_style = design.get("border_style", "weicher_schatten")
    border_config = BORDER_STYLES.get(border_style, BORDER_STYLES["weicher_schatten"])
    
    # Texture-Style (erweitert)
    texture_style = design.get("texture_style", "farbverlauf")
    texture_config = TEXTURE_STYLES.get(texture_style, TEXTURE_STYLES["farbverlauf"])
    
    # Background-Treatment (erweitert)
    background_treatment = design.get("background_treatment", "gradient")
    background_config = BACKGROUND_TREATMENTS.get(background_treatment, BACKGROUND_TREATMENTS["gradient"])
    
    # Corner-Radius (erweitert)
    corner_radius = design.get("corner_radius", "Mittel 16px")
    if corner_radius == "Auto-Radius":
        # Dynamische Berechnung basierend auf Container-Größe
        radius = shape_config.get("radius", 16)
        if radius == "variable":
            radius = 20  # Fallback für organische Formen
    else:
        radius = RADIUS_MAP.get(corner_radius, 16)
    
    # Typography-Style (neu)
    typography_style = design.get("typography_style", "humanist_sans")
    typography_config = TYPOGRAPHY_STYLES.get(typography_style, TYPOGRAPHY_STYLES["humanist_sans"])
    
    # Photo-Treatment (neu)
    photo_treatment = design.get("photo_treatment", "natural_daylight")
    photo_config = PHOTO_TREATMENTS.get(photo_treatment, PHOTO_TREATMENTS["natural_daylight"])
    
    # Depth-Style (neu)
    depth_style = design.get("depth_style", "soft_shadow_stack")
    depth_config = DEPTH_STYLES.get(depth_style, DEPTH_STYLES["soft_shadow_stack"])
    
    # Slider-Parameter (erweitert)
    shadow_intensity = design.get("shadow_intensity", 50) / 100.0  # 0-70 -> 0.0-0.7
    glow_intensity = design.get("glow_intensity", 15) / 100.0  # 0-30 -> 0.0-0.3
    grain_amount = design.get("grain_amount", 5) / 100.0  # 0-25 -> 0.0-0.25
    tint_strength = design.get("tint_strength", 10) / 100.0  # 0-20 -> 0.0-0.2
    elevation_level = design.get("elevation_level", 1)  # 0-3

    base_fill = ci_colors.get("background", "#FFFFFF")
    text_color = ci_colors.get("primary", "#111111")
    
    # Clamp Transparenz 0.1..1.0
    try:
        t = float(transparency)
    except Exception:
        t = 0.8
    if t < 0.1 or t > 1.0:
        logging.getLogger(__name__).warning("background_opacity out of range before clamp: %s", t)
    t = max(0.1, min(1.0, t))

    # Erweiterte Style-Definition
    style: Dict[str, Any] = {
        "shape": str(container_shape).lower(),
        "background": {
            "color": base_fill, 
            "opacity": t,
            "treatment": background_config["type"],
            "treatment_opacity": background_config["opacity"]
        },
        "border_radius": radius,
        "text_color": text_color,
        "border": border_config["border"],
        "shadow": border_config["shadow"],
        "texture": {
            "type": texture_config["type"], 
            "intensity": texture_config["intensity"],
            "grain_amount": grain_amount
        },
        "accent": None,
        "layout_style": layout_config,
        "typography": typography_config,
        "photo_treatment": photo_config,
        "depth": {
            "style": depth_config,
            "shadow_intensity": shadow_intensity,
            "glow_intensity": glow_intensity,
            "elevation_level": elevation_level
        },
        "tint_strength": tint_strength,
    }

    # CTA-Akzente
    if zone_role in {"cta", "cta_block"}:
        style["accent"] = {
            "apply_to": "border", 
            "color": ci_colors.get("accent", "#FFC107"), 
            "width": 2,
            "glow_intensity": glow_intensity
        }

    return style


def apply_design_styles(
    layout_dict: Dict[str, Any],
    design: Dict[str, Any],
    ci_colors: Dict[str, str],
    *,
    override_existing: bool = True,
    preserve_existing_border: bool = True,
) -> Dict[str, Any]:
    """
    Wendet Resolver-Styles auf alle Zonen eines berechneten Layouts an.
    Entfernt dabei Doppel-Felder (opacity, alpha) auf Zonenebene.
    """
    res: Dict[str, Any] = dict(layout_dict)
    zones: Dict[str, Any] = res.get("zones", {})
    layout_type = res.get("layout_type", "vertical_split")
    calc_t = res.get("calculated_values", {}).get("container_transparency", 0.8)

    logger = logging.getLogger(__name__)
    overrides = 0
    merges = 0
    skipped = 0
    for name, zone in zones.items():
        # Early-Return: Motiv-/Background-Zonen nicht stylen
        if isinstance(zone, dict):
            ct = zone.get("content_type")
            if ct == "image_motiv" or name in {"motiv_area"}:
                zone.pop("container_style", None)
                skipped += 1
                continue
        zt = zone.get("transparency", calc_t)
        if isinstance(zt, (int, float)) and zt > 1:
            zt = zt / 100.0
        try:
            zt_f = float(zt)
        except Exception:
            zt_f = 0.8
        zt_f = max(0.1, min(1.0, zt_f))

        zone_role = ZONE_ROLE_MAP.get(name, "generic")
        resolved = resolve_style(
            name,
            design or {},
            ci_colors or {},
            layout_type=layout_type,
            transparency=zt_f,
            zone_role=zone_role,
        )

        # Warn bei ungemappten Text-Zonen
        if zone_role == "generic" and zone.get("content_type") == "text_elements":
            logger.warning("Zone '%s' has generic role; consider extending ZONE_ROLE_MAP", name)

        existing = zone.get("container_style")
        if override_existing or existing is None:
            zone["container_style"] = resolved
            overrides += 1
        else:
            # Sanfte Merge-Politik fuer nicht-Text-Rollen
            non_text_roles = {"logo", "meta", "generic", "content", "data"}
            if preserve_existing_border and zone_role in non_text_roles and zone_role not in FORCE_OVERRIDE_ROLES:
                keep_keys = {"border", "shadow", "texture", "shape"}
                merged = dict(resolved)
                for k in keep_keys:
                    if isinstance(existing, dict) and k in existing:
                        merged[k] = existing[k]
                # Immer Hintergrund-Opacity/Background aus Resolver setzen
                zone["container_style"] = merged
                # Debug-Log fuer Merge
                logger.debug("Merged existing style for %s (role=%s): kept=%s", name, zone_role, sorted(list(keep_keys)))
                merges += 1
            else:
                # Text-Rollen: Resolver darf ueberschreiben, aber bestehende explizite Werte behalten Vorrang
                zone["container_style"] = {**resolved, **existing}
                logger.debug("Overrode style for %s (role=%s) with resolver defaults", name, zone_role)
                overrides += 1

        # Schema-Normalisierung: falls altes Feld vorhanden, in background uebernehmen
        cs = zone.get("container_style")
        if isinstance(cs, dict):
            if 'background' not in cs and 'background_opacity' in cs:
                bg_color = cs.get('background_color', ci_colors.get('background', '#FFFFFF'))
                cs['background'] = {'color': bg_color, 'opacity': cs['background_opacity']}
            # Doppelte Alt-Felder bereinigen
            for legacy in ('background_opacity', 'background_color'):
                if legacy in cs:
                    cs.pop(legacy, None)

        # Doppelte Transparenzfelder entfernen
        for k in ("opacity", "alpha"):
            zone.pop(k, None)

    # Summary-Logging je Layout
    try:
        layout_id = res.get('layout_id', 'unknown')
        logger.info("Layout %s – overrides=%d, merges=%d, skipped=%d", layout_id, overrides, merges, skipped)
    except Exception:
        pass

    res["zones"] = zones
    return res


