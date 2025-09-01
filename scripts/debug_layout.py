#!/usr/bin/env python3
"""
Debug Script für Layout-Problem
"""

import sys
import os

# Füge den creative_core Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'creative_core'))

from layout.loader import load_layout, _get_default_layout
from layout.engine import layout_engine
from layout.schema import validate_layout

def debug_layout_loading():
    """Debug Layout Loading"""
    print("=== DEBUG LAYOUT LOADING ===")
    
    # 1. Teste Standard-Layout
    print("\n1. Standard-Layout:")
    default_layout = _get_default_layout("test_layout")
    print(f"Canvas: {default_layout.get('canvas')}")
    print(f"Zonen: {list(default_layout.get('zones', {}).keys())}")
    
    # 2. Teste Layout-Engine
    print("\n2. Layout-Engine:")
    calculated = layout_engine.calculate_layout_coordinates(default_layout, 50, 80)
    print(f"Canvas nach Engine: {calculated.get('canvas')}")
    print(f"Zonen nach Engine: {list(calculated.get('zones', {}).keys())}")
    
    # 3. Teste Transparenz-Effekte
    print("\n3. Transparenz-Effekte:")
    with_transparency = layout_engine.apply_transparency_effects(calculated)
    print(f"Canvas nach Transparenz: {with_transparency.get('canvas')}")
    print(f"Zonen nach Transparenz: {list(with_transparency.get('zones', {}).keys())}")
    
    # 4. Teste Validierung direkt
    print("\n4. Direkte Validierung:")
    errors = validate_layout(with_transparency)
    print(f"Validierungsfehler: {len(errors)}")
    for error in errors[:3]:  # Zeige nur erste 3
        print(f"  - {error}")
    
    # 5. Teste Layout-Engine Validierung
    print("\n5. Layout-Engine Validierung:")
    try:
        validated = layout_engine.validate_layout(with_transparency)
        print(f"Validierung erfolgreich: {validated.get('__validated__')}")
    except Exception as e:
        print(f"Validierung fehlgeschlagen: {e}")

if __name__ == "__main__":
    debug_layout_loading()
