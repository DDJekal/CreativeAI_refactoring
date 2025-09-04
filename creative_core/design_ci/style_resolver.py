from typing import Dict, Any
import logging


RADIUS_MAP: Dict[str, int] = {
    "Klein 8px": 8,
    "Mittel 16px": 16,
    "Gross 24px": 24,
    "Sehr Gross 32px": 32,
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
    Minimal lauffaehige Version fuer erste Integration.
    """
    corner = design.get("corner_radius", "Mittel 16px")
    border_style = design.get("border_style", "Weicher Schatten")
    container_shape = design.get("container_shape", "Abgerundet")
    texture_style = design.get("texture_style", "Farbverlauf")

    base_fill = ci_colors.get("background", "#FFFFFF")
    text_color = ci_colors.get("primary", "#111111")
    preset = BORDER_PRESETS.get(border_style, BORDER_PRESETS["Weicher Schatten"])

    # Clamp Transparenz 0.1..1.0
    try:
        t = float(transparency)
    except Exception:
        t = 0.8
    if t < 0.1 or t > 1.0:
        logging.getLogger(__name__).warning("background_opacity out of range before clamp: %s", t)
    t = max(0.1, min(1.0, t))

    style: Dict[str, Any] = {
        "shape": str(container_shape).lower(),
        "background": {"color": base_fill, "opacity": t},
        "border_radius": RADIUS_MAP.get(corner, 16),
        "text_color": text_color,
        "border": preset["border"],
        "shadow": preset["shadow"],
        "texture": {"type": str(texture_style).lower(), "intensity": "medium"},
        "accent": None,
    }

    if zone_role in {"cta", "cta_block"}:
        style["accent"] = {"apply_to": "border", "color": ci_colors.get("accent", "#FFC107"), "width": 2}

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


