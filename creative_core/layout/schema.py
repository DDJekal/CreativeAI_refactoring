
"""
Layout Schema - Einheitliche Datenstrukturen und Validierung

Definiert das einheitliche Zonen-Schema und Layout-Validierung
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class Canvas:
    """Canvas-Dimensionen"""
    width: int
    height: int


@dataclass
class Zone:
    """Einheitliche Zone-Definition"""
    x: int
    y: int
    width: int
    height: int
    z: int = 0
    content_type: Optional[str] = None
    description: Optional[str] = None


class LayoutValidationError(Exception):
    """Exception für Layout-Validierungsfehler"""
    def __init__(self, payload: dict):
        self.payload = payload
        super().__init__(f"Layout validation failed: {payload}")


# Layout-Typ-spezifische Zone-Anforderungen
LAYOUT_TYPE_REQUIREMENTS = {
    "dynamic_vertical_split": {
        "required": ["headline_block", "subline_block", "benefits_block"],
        "optional": ["logo_area", "cta_block", "company_block", "standort_block", "motiv_area", "stellentitel_block"]
    },
    "dynamic_horizontal_split": {
        "required": ["headline_block", "subline_block", "benefits_block"],
        "optional": ["logo_area", "cta_block", "company_block", "standort_block", "motiv_block", "stellentitel_block"]
    },
    "dynamic_centered_layout": {
        "required": ["headline_block", "subline_block", "benefits_block"],
        "optional": ["logo_area", "cta_block", "company_block", "standort_block", "motiv_block"]
    },
    "dynamic_diagonal_layout": {
        "required": ["headline_block", "subline_block", "benefits_block"],
        "optional": ["logo_area", "cta_block", "company_block", "standort_block", "motiv_block"]
    },
    "dynamic_asymmetric_layout": {
        "required": ["headline_block", "subline_block", "benefits_block"],
        "optional": ["logo_area", "cta_block", "company_block", "standort_block", "motiv_block"]
    },
    "dynamic_grid_layout": {
        "required": ["headline_block", "subline_block", "benefits_block"],
        "optional": ["logo_area", "cta_block", "company_block", "standort_block", "motiv_block"]
    },
    "dynamic_minimalist_layout": {
        "required": ["headline_block", "subline_block"],
        "optional": ["logo_area", "cta_block", "motiv_block"]
    },
    "dynamic_hero_layout": {
        "required": ["hero_headline", "hero_subline"],
        "optional": ["logo_area", "cta_block", "hero_motiv"]
    },
    "dynamic_storytelling_layout": {
        "required": ["story_headline", "story_opening", "story_development"],
        "optional": ["logo_area", "cta_block", "story_motiv", "story_conclusion"]
    },
    "dynamic_modern_split": {
        "required": ["headline_block", "benefits_block"],
        "optional": ["logo_area", "cta_block", "standort_block", "motiv_area", "stellentitel_block"]
    },
    "dynamic_infographic_layout": {
        "required": ["info_headline", "data_block_1"],
        "optional": ["logo_area", "cta_block", "info_motiv", "data_block_2", "data_block_3", "data_block_4"]
    },
    "dynamic_magazine_layout": {
        "required": ["magazine_headline", "magazine_content"],
        "optional": ["logo_area", "cta_block", "magazine_motiv", "magazine_subline"]
    },
    "dynamic_portfolio_layout": {
        "required": ["portfolio_headline", "portfolio_subline", "showcase_1"],
        "optional": ["logo_area", "cta_block", "portfolio_motiv", "showcase_2", "showcase_3"]
    }
}

# Fallback für unbekannte Layout-Typen
DEFAULT_REQUIREMENTS = {
    "required": ["headline_block", "subline_block"],
    "optional": ["logo_area", "cta_block", "benefits_block", "company_block", "standort_block", "motiv_block"]
}


def validate_layout(layout: dict) -> List[dict]:
    """
    Validiert ein Layout und gibt Liste der Fehler zurück
    
    Args:
        layout: Layout-Dictionary
        
    Returns:
        Liste der Validierungsfehler (leer = valide)
    """
    # Da wir jetzt feste Koordinaten verwenden, brauchen wir keine Validierung mehr
    # Alle Layouts sind valide
    return []


def _validate_zone_flexible(zone_name: str, zone_data: dict, canvas: dict) -> List[dict]:
    """Validiert eine einzelne Zone (flexibel für Platzhalter)"""
    errors = []
    
    # Prüfe ob Zone ein Dictionary ist
    if not isinstance(zone_data, dict):
        errors.append({
            "code": "invalid_zone_structure",
            "path": f"zones.{zone_name}",
            "msg": f"Zone '{zone_name}' must be a dictionary"
        })
        return errors
    
    # Prüfe ob Zone eine position hat (kann Platzhalter sein)
    if 'position' in zone_data:
        position = zone_data['position']
        if isinstance(position, str):
            # Platzhalter sind erlaubt
            if position.startswith('{') and position.endswith('}'):
                # Platzhalter - keine weiteren Validierungen
                pass
            else:
                # Versuche als Koordinaten zu parsen
                coords = convert_position_string_to_coords(position)
                if not coords:
                    errors.append({
                        "code": "invalid_position_format",
                        "path": f"zones.{zone_name}.position",
                        "value": position,
                        "msg": f"Zone '{zone_name}' position must be valid coordinates or placeholder"
                    })
    
    # Prüfe Z-Index
    if 'z' in zone_data and not isinstance(zone_data['z'], int):
        errors.append({
            "code": "invalid_z_index",
            "path": f"zones.{zone_name}.z",
            "value": zone_data['z'],
            "msg": f"Zone '{zone_name}' z-index must be integer"
        })
    
    return errors


def _validate_zone(zone_name: str, zone_data: dict, canvas: dict) -> List[dict]:
    """Validiert eine einzelne Zone (strikt für numerische Koordinaten)"""
    errors = []
    
    # Prüfe ob Zone numerische Koordinaten hat
    required_coords = ['x', 'y', 'width', 'height']
    for coord in required_coords:
        if coord not in zone_data:
            errors.append({
                "code": "missing_coordinate",
                "path": f"zones.{zone_name}.{coord}",
                "msg": f"Zone '{zone_name}' missing coordinate '{coord}'"
            })
        elif not isinstance(zone_data[coord], int):
            errors.append({
                "code": "invalid_coordinate_type",
                "path": f"zones.{zone_name}.{coord}",
                "value": zone_data[coord],
                "msg": f"Zone '{zone_name}' coordinate '{coord}' must be integer"
            })
    
    # Prüfe Koordinaten-Werte
    if all(coord in zone_data and isinstance(zone_data[coord], int) for coord in required_coords):
        x, y, width, height = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
        
        # Negative Koordinaten
        if x < 0:
            errors.append({
                "code": "negative_x_coordinate",
                "path": f"zones.{zone_name}.x",
                "value": x,
                "msg": f"Zone '{zone_name}' x coordinate cannot be negative"
            })
        
        if y < 0:
            errors.append({
                "code": "negative_y_coordinate",
                "path": f"zones.{zone_name}.y", 
                "value": y,
                "msg": f"Zone '{zone_name}' y coordinate cannot be negative"
            })
        
        # Ungültige Dimensionen
        if width <= 0:
            errors.append({
                "code": "invalid_width",
                "path": f"zones.{zone_name}.width",
                "value": width,
                "msg": f"Zone '{zone_name}' width must be positive"
            })
        
        if height <= 0:
            errors.append({
                "code": "invalid_height",
                "path": f"zones.{zone_name}.height",
                "value": height,
                "msg": f"Zone '{zone_name}' height must be positive"
            })
        
        # Außerhalb Canvas
        canvas_width = canvas.get('width', 0)
        canvas_height = canvas.get('height', 0)
        
        if x + width > canvas_width:
            errors.append({
                "code": "zone_outside_canvas_x",
                "path": f"zones.{zone_name}",
                "value": f"x={x}, width={width}, canvas_width={canvas_width}",
                "msg": f"Zone '{zone_name}' extends beyond canvas width"
            })
        
        if y + height > canvas_height:
            errors.append({
                "code": "zone_outside_canvas_y",
                "path": f"zones.{zone_name}",
                "value": f"y={y}, height={height}, canvas_height={canvas_height}",
                "msg": f"Zone '{zone_name}' extends beyond canvas height"
            })
    
    # Z-Index Validierung
    if 'z' in zone_data and not isinstance(zone_data['z'], int):
        errors.append({
            "code": "invalid_z_index",
            "path": f"zones.{zone_name}.z",
            "value": zone_data['z'],
            "msg": f"Zone '{zone_name}' z-index must be integer"
        })
    
    return errors


def convert_position_string_to_coords(position: str) -> Optional[Dict[str, int]]:
    """
    Konvertiert einen position-String zu numerischen Koordinaten
    
    Args:
        position: String im Format "x,y,width,height" oder "x,y,width,height,z"
        
    Returns:
        Dictionary mit x, y, width, height, z oder None bei Fehler
    """
    try:
        parts = position.split(',')
        if len(parts) < 4:
            return None
        
        coords = {
            'x': int(parts[0]),
            'y': int(parts[1]), 
            'width': int(parts[2]),
            'height': int(parts[3])
        }
        
        # Optionaler Z-Index
        if len(parts) >= 5:
            coords['z'] = int(parts[4])
        else:
            coords['z'] = 0
            
        return coords
        
    except (ValueError, IndexError):
        return None


def ensure_numerical_zones(layout_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Stellt sicher, dass alle Zonen numerische Koordinaten haben
    
    Args:
        layout_dict: Layout-Dictionary (enthält zones und andere Metadaten)
        
    Returns:
        Layout-Dictionary mit numerischen Koordinaten für alle Zonen
    """
    # Da wir jetzt feste Koordinaten verwenden, geben wir das Layout unverändert zurück
    return layout_dict.copy()


def get_layout_zone_requirements(layout_type: str) -> Dict[str, List[str]]:
    """
    Gibt die Zone-Anforderungen für einen bestimmten Layout-Typ zurück
    
    Args:
        layout_type: Der Layout-Typ (z.B. 'dynamic_minimalist_layout')
        
    Returns:
        Dictionary mit 'required' und 'optional' Zonen
    """
    return LAYOUT_TYPE_REQUIREMENTS.get(layout_type, DEFAULT_REQUIREMENTS)


def is_zone_required(layout_type: str, zone_name: str) -> bool:
    """
    Prüft ob eine Zone für einen Layout-Typ erforderlich ist
    
    Args:
        layout_type: Der Layout-Typ
        zone_name: Name der Zone
        
    Returns:
        True wenn Zone erforderlich ist, False wenn optional
    """
    requirements = get_layout_zone_requirements(layout_type)
    return zone_name in requirements["required"]


def get_expected_zones_for_layout(layout_type: str) -> List[str]:
    """
    Gibt alle erwarteten Zonen für einen Layout-Typ zurück
    
    Args:
        layout_type: Der Layout-Typ
        
    Returns:
        Liste aller erwarteten Zonen (erforderliche + optionale)
    """
    requirements = get_layout_zone_requirements(layout_type)
    return requirements["required"] + requirements["optional"]


def filter_validation_errors(validation_results: List[dict], include_warnings: bool = True) -> Dict[str, List[dict]]:
    """
    Filtert Validierungsergebnisse nach Fehlern und Warnungen
    
    Args:
        validation_results: Liste der Validierungsergebnisse
        include_warnings: Ob Warnungen eingeschlossen werden sollen
        
    Returns:
        Dictionary mit 'errors' und 'warnings' (nur wenn include_warnings=True)
    """
    errors = []
    warnings = []
    
    for result in validation_results:
        if result.get('severity') == 'warning':
            warnings.append(result)
        else:
            errors.append(result)
    
    if include_warnings:
        return {
            'errors': errors,
            'warnings': warnings
        }
    else:
        return {
            'errors': errors
        }


def validate_layout_strict(layout: dict) -> List[dict]:
    """
    Strikte Layout-Validierung (nur Fehler, keine Warnungen)
    
    Args:
        layout: Layout-Dictionary
        
    Returns:
        Liste der Validierungsfehler (leer = valide)
    """
    all_results = validate_layout(layout)
    filtered = filter_validation_errors(all_results, include_warnings=False)
    return filtered['errors']


def validate_layout_with_warnings(layout: dict) -> Dict[str, List[dict]]:
    """
    Layout-Validierung mit separaten Fehlern und Warnungen
    
    Args:
        layout: Layout-Dictionary
        
    Returns:
        Dictionary mit 'errors' und 'warnings'
    """
    all_results = validate_layout(layout)
    return filter_validation_errors(all_results, include_warnings=True)
