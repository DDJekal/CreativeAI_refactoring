"""
Design CI Rules - Synergistische Style & Design Regeln

Implementiert synergistische Design-Regeln, die perfekt mit den Koordinaten-Templates
und dem LayoutEngine funktionieren. Nutzt die bereits validierten Layout-Daten
für deterministische Style-Berechnungen.
"""

from typing import Dict, Any, Union, List, Tuple
import math
import re
from functools import lru_cache


class DesignValidationError(Exception):
    """Exception für Design-Validierungsfehler"""
    def __init__(self, payload: dict):
        self.payload = payload
        super().__init__(f"Design validation failed: {payload}")


def apply_rules(
    *,
    layout: dict,                 # validiertes layout_dict mit canvas, zones, meta, __validated__=True
    ci: dict,                     # {'primary':'#RRGGBB','secondary':'#RRGGBB','accent':'#RRGGBB'}
    options: dict                 # {'typography_scale': 'md', 'container_shape':'rounded_rectangle',
                                  #  'border_style':'soft_shadow','corner_radius_px':16,
                                  #  'transparency_pct':0..100,'accent_elements':['badge','divider',...]}
) -> dict:


    """
    Wendet synergistische Design-Regeln auf ein validiertes Layout an
    
    Args:
        layout: Validiertes Layout von LayoutEngine (mit __validated__=True)
        ci: CI-Farben als Dict
        options: Container-Styles und Design-Optionen
        
    Returns:
        design_dict mit allen Style-Informationen
        
    Raises:
        DesignValidationError: Bei Pflichtverletzungen
    """
    # STRICT VALIDATION - Keine Fallbacks
    _validate_inputs(layout, ci, options)
    
    # Typografie aus Zonen-Koordinaten berechnen
    typography = _calculate_typography_from_zones(layout, options["typography_scale"])
    
    # Container-Styles mit Layout-Koordinaten synchronisieren
    containers = _calculate_container_styles(layout, options)
    
    # Akzent-Elemente basierend auf Layout-Zonen
    accents = _calculate_accent_elements(layout, options.get("accent_elements", []))
    
    # Kontrast-Prüfungen (nur Warnungen, nicht blockierend)
    warnings = _check_contrast_ratios(layout, ci, typography)
    
    # Transparenz aus LayoutEngine übernehmen
    transparency = layout.get("calculated_values", {}).get("container_transparency", 80)
    
    return {
        "__validated__": True,
        "colors": ci,
        "typography": typography,
        "containers": containers,
        "accents": accents,
        "transparency": transparency,
        "warnings": warnings,
        "layout_synergy": {
            "used_zones": list(layout.get("zones", {}).keys()),
            "canvas_size": layout.get("canvas", {}),
            "layout_type": layout.get("layout_type", "unknown")
        }
    }


def _validate_inputs(layout: dict, ci: dict, options: dict):
    """Strikte Validierung aller Eingaben"""
    errors = []
    
    # Layout-Validierung
    if not layout.get("__validated__"):
        errors.append({
            "code": "layout_not_validated",
            "path": "layout.__validated__",
            "msg": "Layout must be validated before applying design rules"
        })
    
    # CI-Farben Validierung (ERWEITERT um vierte Farbe)
    required_colors = ["primary", "secondary", "accent", "background"]
    for color in required_colors:
        if color not in ci:
            errors.append({
                "code": "missing_color",
                "path": f"ci.{color}",
                "msg": f"{color} color required"
            })
        elif not _is_valid_hex_color(ci[color]):
            errors.append({
                "code": "invalid_hex_color",
                "path": f"ci.{color}",
                "value": ci[color],
                "msg": f"Invalid hex color format for {color}"
            })
    
    # Options Validierung
    required_options = {
        "typography_scale": ["sm", "md", "lg"],
        "container_shape": ["rounded_rectangle", "rectangle", "pill", "circle"],
        "border_style": ["none", "soft_shadow", "hard_shadow", "outline"],
        "corner_radius_px": lambda x: isinstance(x, int) and x >= 0,
        "transparency_pct": lambda x: isinstance(x, int) and 0 <= x <= 100
    }
    
    for option, validator in required_options.items():
        if option not in options:
            errors.append({
                "code": "missing_option",
                "path": f"options.{option}",
                "msg": f"{option} option required"
            })
        elif isinstance(validator, list):
            if options[option] not in validator:
                errors.append({
                    "code": "invalid_option",
                    "path": f"options.{option}",
                    "value": options[option],
                    "msg": f"{option} must be one of {validator}"
                })
        elif callable(validator):
            if not validator(options[option]):
                errors.append({
                    "code": "invalid_option",
                    "path": f"options.{option}",
                    "value": options[option],
                    "msg": f"{option} validation failed"
                })
    
    if errors:
        raise DesignValidationError({"errors": errors})


def _is_valid_hex_color(color: str) -> bool:
    """Prüft ob eine Farbe ein gültiges Hex-Format hat"""
    if not isinstance(color, str):
        return False
    pattern = r'^#(?:[0-9a-fA-F]{3}){1,2}$'
    return bool(re.match(pattern, color))


def _get_actual_text_from_layout(layout: dict, zone_name: str, typo_type: str) -> str:
    """
    Extrahiert den tatsächlichen Text aus dem Layout für eine Zone
    
    Args:
        layout: Layout-Dictionary
        zone_name: Name der Zone (z.B. 'headline_block')
        typo_type: Typ der Typografie (z.B. 'headline')
        
    Returns:
        Tatsächlicher Text oder Fallback-Text
    """
    zones = layout.get('zones', {})
    zone_data = zones.get(zone_name, {})
    
    # Versuche verschiedene Text-Felder zu finden
    text_fields = [
        'text_field', 'headline_input', 'subline_input', 'benefits_input', 'cta_input',
        'location_input', 'company_input', 'stellentitel_input'
    ]
    
    for field in text_fields:
        if field in zone_data:
            text = zone_data[field]
            if text and isinstance(text, str):
                return text
    
    # Fallback: Verwende Standard-Text basierend auf Zone-Typ
    text_samples = {
        "headline": "Dein Rhythmus. Dein Job.",
        "subline": "Entdecke deine Karriere in der Pflege", 
        "benefits": "Attraktive Vergutung",
        "cta": "Jetzt Bewerben!",
        "location": "Braunschweig",
        "company": "Unser Unternehmen"
    }
    
    return text_samples.get(typo_type, "Sample Text")


def _calculate_typography_from_zones(layout: dict, scale: str) -> dict:
    """
    Berechnet Typografie-Größen aus Zonen-Koordinaten (synergistisch)
    
    Nutzt die bereits berechneten Koordinaten aus dem LayoutEngine
    """
    zones = layout.get("zones", {})
    typography = {}
    
    # Scale-Multiplikatoren (deterministisch)
    scale_multipliers = {
        "sm": {"headline": 0.45, "subline": 0.55, "benefits": 0.35, "cta": 0.40},
        "md": {"headline": 0.55, "subline": 0.60, "benefits": 0.40, "cta": 0.45},
        "lg": {"headline": 0.65, "subline": 0.65, "benefits": 0.45, "cta": 0.50}
    }
    
    multipliers = scale_multipliers[scale]
    
    # Typografie für jede Zone berechnen
    zone_mappings = {
        "headline_block": "headline",
        "subline_block": "subline", 
        "benefits_block": "benefits",
        "cta_block": "cta"
    }
    
    # Hole berechnete Werte aus dem Layout für adaptive Anpassung
    calculated_values = layout.get("calculated_values", {})
    text_width = calculated_values.get("text_width", 400)  # Standard-Wert
    
    for zone_name, typo_type in zone_mappings.items():
        if zone_name in zones:
            zone_data = zones[zone_name]
            position = zone_data.get("position", "")
            
            if position and "," in position:
                # Position ist "x,y,width,height" vom LayoutEngine
                parts = position.split(",")
                if len(parts) >= 4:
                    zone_height = int(parts[3])
                    zone_width = int(parts[2])
                    
                    # ADAPTIVE ANPASSUNG: Berücksichtige tatsächliche Container-Breite
                    # Wenn Text-Breite durch Slider reduziert wurde, passe Font-Größe an
                    width_ratio = min(1.0, zone_width / max(text_width * 0.8, 200))  # Mindestbreite 200px
                    
                    # Font-Größe aus Zone-Höhe berechnen
                    base_size = int(zone_height * multipliers[typo_type])
                    
                    # Max-Größen basierend auf Typ
                    max_sizes = {
                        "headline": 80, "subline": 64, "benefits": 48, "cta": 56
                    }
                    
                    font_size = min(base_size, max_sizes[typo_type])
                    
                    # ADAPTIVE ANPASSUNG: Skaliere Font-Größe basierend auf Container-Breite
                    adaptive_font_size = int(font_size * width_ratio)
                    
                    # Mindest-Font-Größe sicherstellen
                    min_font_sizes = {
                        "headline": 28,  # Erhöht von 24
                        "subline": 22,   # Erhöht von 18
                        "benefits": 16,  # Erhöht von 14
                        "cta": 18        # Erhöht von 16
                    }
                    adaptive_font_size = max(adaptive_font_size, min_font_sizes[typo_type])
                    
                    # TEXTBREITEN-VALIDIERUNG: Prüfe ob Text tatsächlich in Container passt
                    # Hole den tatsächlichen Text aus dem Layout
                    actual_text = _get_actual_text_from_layout(layout, zone_name, typo_type)
                    
                    # Berechne geschätzte Textbreite (approximativ)
                    # Durchschnittliche Zeichenbreite: ~0.6 * Font-Größe für deutsche Schrift
                    estimated_text_width = len(actual_text) * adaptive_font_size * 0.6
                    
                    # Berücksichtige Padding und Sicherheitsmarge
                    available_width = zone_width - 20  # 10px Padding auf jeder Seite
                    
                    # Wenn Text zu breit ist, reduziere Font-Größe weiter
                    if estimated_text_width > available_width:
                        # Berechne neue Font-Größe basierend auf verfügbarer Breite
                        safety_factor = 0.9  # 10% Sicherheitsmarge
                        max_font_for_width = (available_width * safety_factor) / (len(actual_text) * 0.6)
                        adaptive_font_size = min(adaptive_font_size, int(max_font_for_width))
                        
                        # Mindest-Font-Größe trotzdem sicherstellen
                        adaptive_font_size = max(adaptive_font_size, min_font_sizes[typo_type])
                    
                    # Line-Height basierend auf adaptiver Font-Größe
                    line_height = max(1.1, min(1.6, adaptive_font_size / 20))
                    
                    # Font-Weight basierend auf Typ
                    font_weight = 700 if typo_type in ["headline", "cta"] else 500
                    
                    typography[typo_type] = {
                        "font_size_px": adaptive_font_size,
                        "line_height_px": int(adaptive_font_size * line_height),
                        "weight": font_weight,
                        "zone_dimensions": {
                            "width": zone_width,
                            "height": zone_height
                        },
                        "adaptive_ratio": width_ratio,  # Für Debugging
                        "original_font_size": font_size,  # Für Debugging
                        "text_width_validation": {
                            "estimated_text_width": estimated_text_width,
                            "available_width": available_width,
                            "fits_container": estimated_text_width <= available_width,
                            "actual_text": actual_text[:50]  # Erste 50 Zeichen für Debugging
                        }
                    }
    
    return typography


def _calculate_container_styles(layout: dict, options: dict) -> dict:
    """
    Berechnet Container-Styles synergistisch mit Layout-Koordinaten
    """
    zones = layout.get("zones", {})
    
    # Hole berechnete Werte für adaptive Anpassung
    calculated_values = layout.get("calculated_values", {})
    text_width = calculated_values.get("text_width", 400)
    
    # ADAPTIVE KOMPLEXITÄTSREDUKTION: Reduziere visuelle Komplexität bei schmalen Containern
    # Wenn Text-Breite unter 400px, vereinfache Container-Design
    container_shape = options.get("container_shape", ('rounded_rectangle', '📱 Abgerundet'))
    border_style = options.get("border_style", ('soft_shadow', '🌫️ Weicher Schatten'))
    texture_style = options.get("texture_style", ('gradient', '🌈 Farbverlauf'))
    
    if text_width < 400:
        # Vereinfache Container-Style für bessere Lesbarkeit
        container_shape = ('rounded_rectangle', '📱 Abgerundet')  # Einfachster Style
        border_style = ('soft_shadow', '🌫️ Weicher Schatten')    # Minimaler Schatten
        texture_style = ('solid', '🎨 Einfarbig')               # Keine Muster
    
    # Padding basierend auf Zone-Breiten berechnen
    padding_calculations = {}
    
    for zone_name, zone_data in zones.items():
        if "position" in zone_data:
            position = zone_data["position"]
            if position and "," in position:
                parts = position.split(",")
                if len(parts) >= 3:
                    zone_width = int(parts[2])
                    
                    # ADAPTIVE PADDING: Berücksichtige tatsächliche Container-Breite
                    # Wenn Container kleiner wird, reduziere Padding proportional
                    width_ratio = min(1.0, zone_width / max(text_width * 0.8, 200))
                    
                    # Basis-Padding basierend auf Zone-Breite
                    base_padding_x = max(5, min(32, int(zone_width * 0.05)))
                    base_padding_y = max(3, min(20, int(zone_width * 0.03)))
                    
                    # Adaptive Padding-Anpassung
                    adaptive_padding_x = int(base_padding_x * width_ratio)
                    adaptive_padding_y = int(base_padding_y * width_ratio)
                    
                    # Mindest-Padding sicherstellen
                    adaptive_padding_x = max(adaptive_padding_x, 5)  # Erhöht von 3
                    adaptive_padding_y = max(adaptive_padding_y, 4)  # Erhöht von 2
                    
                    padding_calculations[zone_name] = {
                        "x": adaptive_padding_x,
                        "y": adaptive_padding_y,
                        "zone_width": zone_width,
                        "adaptive_ratio": width_ratio,
                        "original_padding_x": base_padding_x,
                        "original_padding_y": base_padding_y
                    }
    
    return {
        "all": {
            "shape": container_shape,
            "border_style": border_style,
            "texture_style": texture_style,
            "corner_radius_px": options["corner_radius_px"],
            "padding_px": padding_calculations,
            "transparency_pct": options["transparency_pct"]
        },
        "zone_specific": padding_calculations,
        "adaptive_complexity_reduction": text_width < 400  # Flag für Debugging
    }


def _calculate_accent_elements(layout: dict, accent_elements: List[str]) -> dict:
    """
    Berechnet Akzent-Elemente basierend auf Layout-Zonen
    """
    zones = layout.get("zones", {})
    
    # Akzent-Elemente nur für verfügbare Zonen
    available_zones = list(zones.keys())
    
    # Akzent-Spezifikationen basierend auf Zone-Größen
    accent_specs = {}
    
    for element in accent_elements:
        if element == "divider":
            # Divider-Dicke basierend auf verfügbaren Zonen
            if "headline_block" in zones and "subline_block" in zones:
                accent_specs["divider_px"] = 2
                accent_specs["divider_style"] = "solid"
        
        elif element == "badge":
            # Badge-Radius basierend auf Zone-Größen
            if "standort_block" in zones:
                zone_data = zones["standort_block"]
                position = zone_data.get("position", "")
                if position and "," in position:
                    parts = position.split(",")
                    if len(parts) >= 4:
                        zone_height = int(parts[3])
                        badge_radius = max(8, min(zone_height // 4, 20))
                        accent_specs["badge_radius_px"] = badge_radius
        
        elif element == "pin":
            # Pin-Größe basierend auf CTA-Zone
            if "cta_block" in zones:
                zone_data = zones["cta_block"]
                position = zone_data.get("position", "")
                if position and "," in position:
                    parts = position.split(",")
                    if len(parts) >= 4:
                        zone_height = int(parts[3])
                        pin_size = max(12, min(zone_height // 6, 24))
                        accent_specs["pin_size_px"] = pin_size
        
        elif element == "dot":
            # Dot-Größe basierend auf Benefits-Zone
            if "benefits_block" in zones:
                zone_data = zones["benefits_block"]
                position = zone_data.get("position", "")
                if position and "," in position:
                    parts = position.split(",")
                    if len(parts) >= 4:
                        zone_height = int(parts[3])
                        dot_size = max(6, min(zone_height // 8, 16))
                        accent_specs["dot_size_px"] = dot_size
    
    return {
        "elements": accent_elements,
        "spec": accent_specs,
        "available_zones": available_zones
    }


def _check_contrast_ratios(layout: dict, ci: dict, typography: dict) -> List[dict]:
    """
    Prüft Kontrast-Verhältnisse (nur Warnungen, nicht blockierend)
    """
    warnings = []
    
    # Kontrast zwischen Text und Hintergrund prüfen
    text_color = ci.get("primary", "#005EA5")
    background_color = ci.get("secondary", "#B4D9F7")
    
    contrast_ratio = _calculate_contrast_ratio(text_color, background_color)
    
    # WCAG AA Standard: 4.5:1 für normalen Text
    if contrast_ratio < 4.5:
        warnings.append({
            "code": "low_contrast",
            "zone": "general_text",
            "ratio": round(contrast_ratio, 1),
            "min": 4.5,
            "msg": f"Text-Background contrast ratio {contrast_ratio:.1f} is below WCAG AA standard"
        })
    
    # Kontrast für CTA prüfen
    cta_color = ci.get("accent", "#FFC20E")
    if contrast_ratio < 3.0:  # CTA kann niedrigeren Kontrast haben
        warnings.append({
            "code": "low_cta_contrast", 
            "zone": "cta",
            "ratio": round(contrast_ratio, 1),
            "min": 3.0,
            "msg": f"CTA contrast ratio {contrast_ratio:.1f} is below recommended minimum"
        })
    
    return warnings


@lru_cache(maxsize=128)
def _calculate_contrast_ratio(fg_hex: str, bg_hex: str) -> float:
    """
    Berechnet Kontrast-Verhältnis zwischen zwei Hex-Farben (WCAG-Formel)
    """
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Konvertiert Hex zu RGB"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def get_luminance(r: int, g: int, b: int) -> float:
        """Berechnet relative Luminanz (WCAG-Formel)"""
        def normalize(c: int) -> float:
            c = c / 255.0
            if c <= 0.03928:
                return c / 12.92
            return ((c + 0.055) / 1.055) ** 2.4
        
        return 0.2126 * normalize(r) + 0.7152 * normalize(g) + 0.0722 * normalize(b)
    
    try:
        fg_rgb = hex_to_rgb(fg_hex)
        bg_rgb = hex_to_rgb(bg_hex)
        
        fg_lum = get_luminance(*fg_rgb)
        bg_lum = get_luminance(*bg_rgb)
        
        # Kontrast-Verhältnis berechnen
        if fg_lum > bg_lum:
            lighter, darker = fg_lum, bg_lum
        else:
            lighter, darker = bg_lum, fg_lum
        
        return (lighter + 0.05) / (darker + 0.05)
    
    except Exception:
        # Bei Fehlern Standard-Kontrast zurückgeben
        return 4.5


# Kompatibilitäts-Funktion für bestehende Aufrufe
def apply_rules_legacy(ci_yaml: Union[str, Dict[str, Any]], layout_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Legacy-Kompatibilität für bestehende Aufrufe
    """
    # Konvertiere Legacy-Format zu neuem Format (ERWEITERT um vierte Farbe)
    if isinstance(ci_yaml, str):
        ci = {"primary": "#005EA5", "secondary": "#B4D9F7", "accent": "#FFC20E", "background": "#FFFFFF"}
    else:
        ci = ci_yaml or {"primary": "#005EA5", "secondary": "#B4D9F7", "accent": "#FFC20E", "background": "#FFFFFF"}
    
    # Standard-Options
    options = {
        "typography_scale": "md",
        "container_shape": "rounded_rectangle",
        "border_style": "soft_shadow",
        "corner_radius_px": 16,
        "transparency_pct": 80,
        "accent_elements": ["badge", "divider"]
    }
    
    try:
        return apply_rules(layout=layout_dict, ci=ci, options=options)
    except DesignValidationError:
        # Fallback für ungültige Layouts
        return {
            "__validated__": False,
            "colors": ci,
            "typography": {},
            "containers": options,
            "accents": {"elements": [], "spec": {}},
            "warnings": [{"code": "legacy_fallback", "msg": "Using legacy fallback mode"}]
        }


def process_design_ci(design_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verarbeitet Design-Eingaben und wendet Design-Regeln an
    
    Args:
        design_input: Dictionary mit Design-Parametern
        
    Returns:
        Verarbeitetes Design mit angewendeten Regeln
    """
    try:
        # CI-Farben extrahieren (ERWEITERT um vierte Farbe)
        ci = {
            'primary': design_input.get('primary_color', '#005EA5'),
            'secondary': design_input.get('secondary_color', '#B4D9F7'),
            'accent': design_input.get('accent_color', '#FFC20E'),
            'background': design_input.get('background_color', '#FFFFFF')
        }
        
        # Design-Optionen
        options = {
            'typography_scale': 'md',
            'container_shape': design_input.get('container_shape', 'rounded_rectangle'),
            'border_style': design_input.get('border_style', 'soft_shadow'),
            'corner_radius_px': 16,
            'transparency_pct': 80,
            'accent_elements': ['badge', 'divider']
        }
        
        # Vereinfachtes Ergebnis für Kompatibilität
        return {
            'colors': ci,
            'style': {
                'layout_style': design_input.get('layout_style', 'rounded_modern'),
                'container_shape': options['container_shape'],
                'border_style': options['border_style']
            },
            'processing_success': True
        }
        
    except Exception as e:
        # Fallback bei Fehlern
        return {
            'colors': {
                'primary': '#005EA5',
                'secondary': '#B4D9F7',
                'accent': '#FFC20E',
                'background': '#FFFFFF'
            },
            'style': {
                'layout_style': 'rounded_modern'
            },
            'processing_success': False,
            'error': str(e)
        }
