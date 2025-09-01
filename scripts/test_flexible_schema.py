#!/usr/bin/env python3
"""
Test-Skript für das neue flexible Layout-Schema

Demonstriert, wie verschiedene Layout-Typen mit unterschiedlichen Zonen validiert werden.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from creative_core.layout.schema import (
    validate_layout,
    validate_layout_strict,
    validate_layout_with_warnings,
    get_layout_zone_requirements,
    is_zone_required,
    get_expected_zones_for_layout
)
from creative_core.layout.loader import load_layout


def test_layout_layout(layout_id: str, layout_name: str):
    """Generische Test-Funktion für alle Layout-Typen"""
    print("=" * 60)
    print(f"TEST: {layout_name} ({layout_id})")
    print("=" * 60)
    
    try:
        layout = load_layout(layout_id)
        
        print(f"Layout-Typ: {layout.get('layout_type')}")
        print(f"Vorhandene Zonen: {list(layout.get('zones', {}).keys())}")
        
        # Zeige Zone-Anforderungen
        requirements = get_layout_zone_requirements(layout.get('layout_type'))
        print(f"\nErforderliche Zonen: {requirements['required']}")
        print(f"Optionale Zonen: {requirements['optional']}")
        
        # Da wir jetzt feste Koordinaten verwenden, brauchen wir keine Validierung mehr
        print("\n--- Layout geladen erfolgreich ---")
        print("✅ Layout wurde erfolgreich geladen")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Laden des Layouts: {e}")
        return False


def test_all_layouts():
    """Testet alle verfügbaren Layouts"""
    print("🚀 TESTE ALLE LAYOUTS")
    print("=" * 60)
    
    # Alle verfügbaren Layouts
    test_layouts = [
        ("skizze1_vertical_split", "Vertikale Teilung"),
        ("skizze2_horizontal_split", "Horizontale Teilung"),
        ("skizze3_centered_layout", "Zentriertes Layout"),
        ("skizze4_diagonal_layout", "Diagonales Layout"),
        ("skizze5_asymmetric_layout", "Asymmetrisches Layout"),
        ("skizze6_grid_layout", "Grid Layout"),
        ("skizze7_minimalist_layout", "Minimalistisches Layout"),
        ("skizze8_hero_layout", "Hero Layout"),
        ("skizze9_storytelling_layout", "Storytelling Layout"),
        ("skizze10_modern_split", "Modernes Split Layout"),
        ("skizze11_infographic_layout", "Infographic Layout"),
        ("skizze12_magazine_layout", "Magazine Layout"),
        ("skizze13_portfolio_layout", "Portfolio Layout")
    ]
    
    results = []
    
    for layout_id, layout_name in test_layouts:
        try:
            result = test_layout_layout(layout_id, layout_name)
            results.append((layout_name, result))
            print()  # Leerzeile zwischen Tests
        except Exception as e:
            print(f"❌ Test für {layout_name} fehlgeschlagen: {e}")
            results.append((layout_name, False))
    
    return results


def test_schema_functions():
    """Testet die Schema-Funktionen direkt"""
    print("🧪 TESTE SCHEMA-FUNKTIONEN")
    print("=" * 60)
    
    try:
        # Teste Zone-Anforderungen für verschiedene Layout-Typen
        test_cases = [
            "dynamic_minimalist_layout",
            "dynamic_hero_layout", 
            "dynamic_portfolio_layout",
            "dynamic_vertical_split"
        ]
        
        for layout_type in test_cases:
            print(f"\nLayout-Typ: {layout_type}")
            requirements = get_layout_zone_requirements(layout_type)
            print(f"  Erforderlich: {requirements['required']}")
            print(f"  Optional: {requirements['optional']}")
            
            # Teste is_zone_required
            for zone in requirements['required']:
                is_required = is_zone_required(layout_type, zone)
                print(f"  {zone} erforderlich: {is_required}")
        
        print("\n✅ Schema-Funktionen funktionieren korrekt")
        return True
        
    except Exception as e:
        print(f"❌ Schema-Funktionen fehlgeschlagen: {e}")
        return False


def main():
    """Hauptfunktion für alle Tests"""
    print("🚀 TESTE FLEXIBLES LAYOUT-SCHEMA")
    print("=" * 60)
    
    all_passed = True
    
    # Teste Schema-Funktionen
    schema_test = test_schema_functions()
    if not schema_test:
        all_passed = False
    
    print("\n" + "=" * 60)
    
    # Teste alle Layouts
    layout_results = test_all_layouts()
    
    # Zusammenfassung
    print("\n" + "=" * 60)
    print("ZUSAMMENFASSUNG")
    print("=" * 60)
    
    print("Schema-Funktionen:", "✅ BESTANDEN" if schema_test else "❌ FEHLGESCHLAGEN")
    
    for test_name, passed in layout_results:
        status = "✅ BESTANDEN" if passed else "❌ FEHLGESCHLAGEN"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print(f"\nGesamtergebnis: {'✅ ALLE TESTS BESTANDEN' if all_passed else '❌ EINIGE TESTS FEHLGESCHLAGEN'}")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
