"""
Layout Loader für dynamische Layouts mit Slider-Integration

Lädt YAML-Layouts und berechnet dynamische Koordinaten basierend auf:
- image_text_ratio Slider (30-70%)
- container_transparency Slider (0-100%)
"""

import yaml
import os
from typing import Dict, Any, Union, Optional
from functools import lru_cache
from .engine import layout_engine
from .schema import ensure_numerical_zones, LayoutValidationError


def load_layout(
    layout_id: str, 
    *, 
    yaml_path: str = "input_config/enhanced_layout_definitions.yaml",
    image_text_ratio: int = 50,
    container_transparency: int = 80
) -> Dict[str, Any]:
    """
    Lädt ein Layout und berechnet dynamische Koordinaten
    
    Args:
        layout_id: ID des zu ladenden Layouts (z.B. "skizze1_vertical_split")
        yaml_path: Pfad zur YAML-Datei (Standard: enhanced_layout_definitions.yaml)
        image_text_ratio: Slider-Wert 30-70 (30% = mehr Text, 70% = mehr Bild)
        container_transparency: Slider-Wert 0-100 (0 = transparent, 100 = undurchsichtig)
        
    Returns:
        Layout-Dictionary mit berechneten Koordinaten
        
    Raises:
        FileNotFoundError: Wenn die YAML-Datei nicht gefunden wird
        KeyError: Wenn das Layout nicht in der YAML-Datei gefunden wird
        LayoutValidationError: Bei Layout-Validierungsfehlern
    """
    # Verwende direkt das Standard-Layout (bis YAML-Dateien korrigiert sind)
    # Lade Layout aus separater YAML-Datei
    layout_dict = _load_from_separate_file(layout_id)
    
    print(f"DEBUG: Layout geladen: {layout_dict.get('name')}")
    print(f"DEBUG: Canvas: {layout_dict.get('canvas')}")
    print(f"DEBUG: Zonen: {list(layout_dict.get('zones', {}).keys())}")
    
    # Konvertiere position-Strings zu numerischen Koordinaten
    layout_dict = ensure_numerical_zones(layout_dict)
    
    # Berechne dynamische Koordinaten mit dem Layout-Engine
    calculated_layout = layout_engine.calculate_layout_coordinates(
        layout_dict, image_text_ratio, container_transparency
    )
    
    # Wende Transparenz-Effekte an
    final_layout = layout_engine.apply_transparency_effects(calculated_layout)
    
    # Validiere das finale Layout (strikt)
    try:
        validated_layout = layout_engine.validate_layout(final_layout)
        return validated_layout
    except LayoutValidationError as e:
        # Layout-Validierung fehlgeschlagen
        raise LayoutValidationError({
            "layout_id": layout_id,
            "errors": e.payload.get("errors", []),
            "message": f"Layout '{layout_id}' failed validation"
        })


def _load_from_central_yaml(layout_id: str, yaml_path: str) -> Dict[str, Any]:
    """Lädt ein Layout aus der zentralen YAML-Datei"""
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"Layout-Datei nicht gefunden: {yaml_path}")
    
    with open(yaml_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    
    if 'layouts' not in data:
        raise KeyError(f"Keine 'layouts' Sektion in {yaml_path} gefunden")
    
    if layout_id not in data['layouts']:
        raise KeyError(f"Layout '{layout_id}' nicht in {yaml_path} gefunden")
    
    return data['layouts'][layout_id]


def _load_from_separate_file(layout_id: str) -> Dict[str, Any]:
    """Lädt ein Layout aus einer separaten YAML-Datei"""
    # Konstruiere den Dateipfad basierend auf der Layout-ID
    layout_file = f"input_config/layouts/{layout_id}.yaml"
    
    if not os.path.exists(layout_file):
        raise FileNotFoundError(f"Layout-Datei nicht gefunden: {layout_file}")
    
    with open(layout_file, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def _get_default_layout(layout_id: str) -> Dict[str, Any]:
    """Gibt ein Standard-Layout zurück, falls das gewünschte nicht gefunden wird"""
    # Standard-Layout für vertikale Aufteilung (valides Schema)
    return {
        'layout_id': layout_id,
        'name': f"Standard {layout_id}",
        'layout_type': 'dynamic_vertical_split',
        'complexity': 'medium',
        'canvas': {
            'width': 1080,
            'height': 1080
        },
        'zones': {
            'headline_block': {
                'x': 40, 'y': 40, 'width': 400, 'height': 80, 'z': 1,
                'content_type': 'text_elements',
                'description': 'Hauptheadline in Primärfarbe'
            },
            'subline_block': {
                'x': 40, 'y': 140, 'width': 400, 'height': 80, 'z': 1,
                'content_type': 'text_elements', 
                'description': 'Subline in Sekundärfarbe'
            },
            'benefits_block': {
                'x': 40, 'y': 240, 'width': 400, 'height': 200, 'z': 1,
                'content_type': 'text_elements',
                'description': 'Benefits-Liste in Primärfarbe'
            },
            'cta_block': {
                'x': 40, 'y': 460, 'width': 400, 'height': 100, 'z': 1,
                'content_type': 'text_elements',
                'description': 'CTA-Button in Akzentfarbe'
            },
            'company_block': {
                'x': 40, 'y': 580, 'width': 400, 'height': 60, 'z': 1,
                'content_type': 'text_elements',
                'description': 'Firmenname in Primärfarbe'
            },
            'standort_block': {
                'x': 40, 'y': 660, 'width': 400, 'height': 60, 'z': 1,
                'content_type': 'text_elements',
                'description': 'Standort in Sekundärfarbe'
            },
            'image_motiv': {
                'x': 500, 'y': 40, 'width': 540, 'height': 680, 'z': 0,
                'content_type': 'image_motiv',
                'description': 'Motiv-Bild rechts'
            }
        },
        'validation': {
            'minimums': {
                'text_area_width': 300,
                'image_area_width': 200,
                'container_transparency': 0.3
            },
            'maximums': {
                'text_area_width': 800,
                'image_area_width': 900,
                'container_transparency': 0.9
            }
        },
        'layout_engine': {
            'transparency_handling': {
                'apply_to_zones': ['headline_block', 'subline_block', 'benefits_block', 'cta_block', 'company_block', 'standort_block'],
                'fallback_opacity': 0.8
            }
        }
    }


@lru_cache(maxsize=32)
def load_layout_cached(
    layout_id: str, 
    image_text_ratio: int = 50,
    container_transparency: int = 80
) -> Dict[str, Any]:
    """
    Gecachte Version des Layout-Loaders
    
    Args:
        layout_id: ID des zu ladenden Layouts
        image_text_ratio: Slider-Wert 30-70
        container_transparency: Slider-Wert 0-100
        
    Returns:
        Gecachtes Layout-Dictionary
    """
    return load_layout(
        layout_id, 
        image_text_ratio=image_text_ratio,
        container_transparency=container_transparency
    )


def list_available_layouts(yaml_path: str = "input_config/layout_index.yaml") -> Dict[str, Any]:
    """
    Listet alle verfügbaren Layouts auf
    
    Args:
        yaml_path: Pfad zur Layout-Index-Datei
        
    Returns:
        Dictionary mit allen verfügbaren Layouts
    """
    try:
        with open(yaml_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print(f"Layout-Index nicht gefunden: {yaml_path}")
        return {"layouts": {}, "categories": {}}


def get_layout_info(layout_id: str, yaml_path: str = "input_config/layout_index.yaml") -> Optional[Dict[str, Any]]:
    """
    Gibt Informationen über ein spezifisches Layout zurück
    
    Args:
        layout_id: ID des Layouts
        yaml_path: Pfad zur Layout-Index-Datei
        
    Returns:
        Layout-Informationen oder None, falls nicht gefunden
    """
    try:
        data = list_available_layouts(yaml_path)
        return data.get('layouts', {}).get(layout_id)
    except Exception:
        return None


def validate_layout_file(layout_id: str, yaml_path: str = "input_config/layouts/") -> bool:
    """
    Validiert, ob eine Layout-Datei existiert und gültig ist
    
    Args:
        layout_id: ID des Layouts
        yaml_path: Basis-Pfad zu den Layout-Dateien
        
    Returns:
        True, falls die Datei existiert und gültig ist
    """
    layout_file = os.path.join(yaml_path, f"{layout_id}.yaml")
    
    if not os.path.exists(layout_file):
        return False
    
    try:
        with open(layout_file, 'r', encoding='utf-8') as file:
            yaml.safe_load(file)
        return True
    except yaml.YAMLError:
        return False


# Beispiel für die Verwendung
if __name__ == "__main__":
    # Teste den Layout-Loader
    try:
        # Lade ein Layout mit Standard-Slider-Werten
        layout = load_layout("skizze1_vertical_split")
        print(f"Layout geladen: {layout['name']}")
        print(f"Zonen: {list(layout['zones'].keys())}")
        
        # Lade ein Layout mit angepassten Slider-Werten
        layout_70_30 = load_layout(
            "skizze1_vertical_split",
            image_text_ratio=70,  # 70% Bild, 30% Text
            container_transparency=60  # 60% Transparenz
        )
        print(f"Layout mit 70/30 Ratio geladen")
        print(f"Berechnete Werte: {layout_70_30.get('calculated_values', {})}")
        
        # Liste verfügbare Layouts auf
        available = list_available_layouts()
        print(f"Verfügbare Layouts: {list(available.get('layouts', {}).keys())}")
        
    except Exception as e:
        print(f"Fehler beim Testen des Layout-Loaders: {e}")
