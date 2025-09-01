#!/usr/bin/env python3
"""
Test-Script für die semantische Layout-Beschreibung
"""

import sys
import os

# Pfad zum Projekt hinzufügen
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from creative_core.layout.loader import load_layout

def test_semantic_layout_description():
    """Testet die semantische Layout-Beschreibung für skizze1_vertical_split"""
    
    print("🧪 Test: Semantische Layout-Beschreibung")
    print("=" * 50)
    
    # Layout laden
    layout_data = load_layout('skizze1_vertical_split')
    
    if not layout_data:
        print("❌ Fehler: Layout konnte nicht geladen werden")
        return
    
    print(f"✅ Layout geladen: {layout_data.get('layout_id')}")
    print(f"📐 Layout-Typ: {layout_data.get('layout_type')}")
    print(f"🎨 Canvas: {layout_data.get('canvas', {}).get('width')}x{layout_data.get('canvas', {}).get('height')}")
    
    # Semantische Beschreibung generieren
    from main import generate_semantic_layout_description
    
    semantic_layout = generate_semantic_layout_description(layout_data)
    
    print("\n🎯 SEMANTISCHE LAYOUT-BESCHREIBUNG:")
    print("=" * 50)
    print(f"📋 Overview: {semantic_layout['layout_overview']}")
    
    print("\n📝 TEXT-BEREICHE:")
    for text_area in semantic_layout['text_areas']:
        print(f"  • {text_area['zone_name']}: {text_area['description']}")
        print(f"    Position: {text_area['relative_position']}")
        print(f"    Größe: {text_area['size']}")
    
    print("\n🖼️ BILD-BEREICHE:")
    for image_area in semantic_layout['image_areas']:
        print(f"  • {image_area['zone_name']}: {image_area['description']}")
        print(f"    Position: {image_area['relative_position']}")
        print(f"    Größe: {image_area['size']}")
    
    print("\n✅ Test erfolgreich abgeschlossen!")

if __name__ == "__main__":
    test_semantic_layout_description()
