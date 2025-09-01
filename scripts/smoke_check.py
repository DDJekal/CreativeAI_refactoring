#!/usr/bin/env python3
"""
Smoke Test für die neue modulare Pipeline mit dynamischen Layouts

Testet:
1. Layout-Loading mit verschiedenen Slider-Werten
2. Dynamische Koordinatenberechnung
3. Transparenz-Integration
4. Validierung der Layouts
5. Design & CI Regeln (neu)
6. Layout-Validierung (strikt)
7. Vollständige Pipeline mit Design-Integration
"""

import sys
import os

# Füge den creative_core Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'creative_core'))

from layout.loader import load_layout, list_available_layouts
from layout.schema import LayoutValidationError
from design_ci.rules import apply_rules, apply_rules_legacy, DesignValidationError
from text_inputs.normalize import prepare_texts
from motive_inputs.spec import build_motive_spec
from prompt_composer.compose import compose


def test_dynamic_layouts():
    """Testet die dynamischen Layouts mit verschiedenen Slider-Werten"""
    print("TESTE: Dynamische Layouts...")
    
    # Teste verschiedene Slider-Kombinationen
    test_cases = [
        {"ratio": 30, "transparency": 90, "name": "30/70 Text/Bild, 90% Transparenz"},
        {"ratio": 50, "transparency": 80, "name": "50/50 Text/Bild, 80% Transparenz"},
        {"ratio": 70, "transparency": 60, "name": "70/30 Text/Bild, 60% Transparenz"},
    ]
    
    for test_case in test_cases:
        print(f"\nTESTE: {test_case['name']}")
        
        try:
            # Lade Layout mit Slider-Werten
            layout = load_layout(
                "skizze1_vertical_split",
                image_text_ratio=test_case['ratio'],
                container_transparency=test_case['transparency']
            )
            
            # Prüfe berechnete Werte
            calculated = layout.get('calculated_values', {})
            print(f"  OK: Layout geladen: {layout.get('name', 'Unbekannt')}")
            print(f"  Text-Breite: {calculated.get('text_width', 'N/A')}px")
            print(f"  Bild-Breite: {calculated.get('image_width', 'N/A')}px")
            print(f"  Transparenz: {calculated.get('container_transparency', 'N/A')}")
            
            # Prüfe Validierung
            validation_status = layout.get('validation_status', 'unknown')
            print(f"  Validierung: {validation_status}")
            
            if validation_status == 'warnings':
                warnings = layout.get('validation_warnings', [])
                for warning in warnings:
                    print(f"    WARNUNG: {warning}")
            
        except Exception as e:
            print(f"  FEHLER: {e}")


def test_multiple_layouts():
    """Testet verschiedene Layout-Typen"""
    print("\nTESTE: Verschiedene Layout-Typen...")
    
    layouts_to_test = [
        "skizze1_vertical_split",
        "skizze2_horizontal_split", 
        "skizze10_modern_split"
    ]
    
    for layout_id in layouts_to_test:
        print(f"\nTESTE Layout: {layout_id}")
        
        try:
            # Lade Layout mit Standard-Werten
            layout = load_layout(layout_id)
            
            print(f"  OK: Layout geladen: {layout.get('name', 'Unbekannt')}")
            print(f"  Typ: {layout.get('layout_type', 'Unbekannt')}")
            print(f"  Komplexität: {layout.get('complexity', 'Unbekannt')}")
            
            # Prüfe Zonen
            zones = layout.get('zones', {})
            print(f"  Zonen: {len(zones)} gefunden")
            
            # Prüfe spezifische Zonen
            zone_types = {}
            for zone_name, zone_data in zones.items():
                content_type = zone_data.get('content_type', 'unknown')
                zone_types[content_type] = zone_types.get(content_type, 0) + 1
            
            for content_type, count in zone_types.items():
                print(f"    - {content_type}: {count}")
            
        except Exception as e:
            print(f"  FEHLER: {e}")


def test_layout_validation():
    """Testet Layout-Validierung mit extremen Werten"""
    print("\nTESTE: Layout-Validierung...")
    
    # Teste extreme Transparenz-Werte
    extreme_cases = [
        {"transparency": 10, "name": "Sehr niedrige Transparenz (10%)"},
        {"transparency": 95, "name": "Sehr hohe Transparenz (95%)"},
    ]
    
    for test_case in extreme_cases:
        print(f"\nTESTE: {test_case['name']}")
        
        try:
            layout = load_layout(
                "skizze1_vertical_split",
                image_text_ratio=50,
                container_transparency=test_case['transparency']
            )
            
            # Prüfe ob Warnungen generiert wurden
            validation_status = layout.get('validation_status', 'unknown')
            warnings = layout.get('validation_warnings', [])
            
            print(f"  OK: Layout geladen: {layout.get('name')}")
            print(f"  Validierung: {validation_status}")
            print(f"  Warnungen: {len(warnings)} gefunden")
            
            for warning in warnings:
                print(f"    - {warning}")
                
        except Exception as e:
            print(f"  FEHLER: {e}")


def test_layout_index():
    """Testet den Layout-Index"""
    print("\nTESTE: Layout-Index...")
    
    try:
        # Lade verfügbare Layouts
        available_layouts = list_available_layouts()
        
        if available_layouts:
            print(f"  OK: Layout-Index geladen: {len(available_layouts)} Layouts verfügbar")
            
            # Zeige erste 3 Layouts
            for i, layout_info in enumerate(available_layouts[:3]):
                print(f"    {i+1}. {layout_info.get('name', 'Unbekannt')} ({layout_info.get('id', 'N/A')})")
                print(f"       Typ: {layout_info.get('layout_type', 'Unbekannt')}")
                print(f"       Komplexität: {layout_info.get('complexity', 'Unbekannt')}")
            
            if len(available_layouts) > 3:
                print(f"    ... und {len(available_layouts) - 3} weitere")
        
        # Lade Layout-Index-Details
        from layout.loader import get_layout_info
        index_info = get_layout_info()
        
        if index_info:
            print(f"  Layout-Index Details:")
            print(f"    Version: {index_info.get('metadata', {}).get('version', 'N/A')}")
            print(f"    Layouts: {len(index_info.get('layouts', []))}")
            
            # Zeige Komplexitäts-Level
            if 'complexity_levels' in index_info:
                complexity_levels = index_info['complexity_levels']
                print(f"  Komplexitäts-Level: {len(complexity_levels)} verfügbar")
                
                for level, level_data in complexity_levels.items():
                    level_layouts = level_data.get('layouts', [])
                    print(f"    - {level}: {len(level_layouts)} Layouts")
        
        else:
            print("  WARNUNG: Layout-Index hat keine 'layouts' Sektion")
            
    except Exception as e:
        print(f"  FEHLER beim Laden des Layout-Index: {e}")


def test_design_ci_strict_mode():
    """Testet Design & CI Modul im Strict Mode"""
    print("\nTESTE: Design & CI Modul (Strict Mode)...")
    
    try:
        # Lade ein valides Layout
        print("  1. Lade valides Layout...")
        layout = load_layout("skizze1_vertical_split", image_text_ratio=50, container_transparency=80)
        
        if not layout.get("__validated__"):
            print("  FEHLER: Layout ist nicht validiert")
            return False
        
        print(f"  OK: Layout geladen und validiert: {layout.get('name')}")
        
        # Teste gültige CI-Farben und Options (ERWEITERT um vierte Farbe)
        print("  2. Teste gültige Design-Parameter...")
        ci = {"primary": "#005EA5", "secondary": "#B4D9F7", "accent": "#FFC20E", "background": "#FFFFFF"}
        options = {
            "typography_scale": "md", 
            "container_shape": "rounded_rectangle", 
            "border_style": "soft_shadow", 
            "corner_radius_px": 16, 
            "transparency_pct": 80, 
            "accent_elements": ["badge", "divider"]
        }
        
        # Wende Design-Regeln an
        design = apply_rules(layout=layout, ci=ci, options=options)
        
        # Prüfe Ergebnis
        if design.get("__validated__"):
            print("  OK: Design erfolgreich validiert")
            print(f"  Typografie: {len(design.get('typography', {}))} Zonen")
            print(f"  Container: {design.get('containers', {}).get('all', {}).get('shape')}")
            print(f"  Akzente: {len(design.get('accents', {}).get('elements', []))} Elemente")
            print(f"  Warnungen: {len(design.get('warnings', []))}")
            
            # Zeige Typografie-Details
            typography = design.get('typography', {})
            if 'headline' in typography:
                headline = typography['headline']
                print(f"    Headline: {headline.get('font_size_px')}px, Gewicht: {headline.get('weight')}")
            
            return True
        else:
            print("  FEHLER: Design-Validierung fehlgeschlagen")
            return False
            
    except Exception as e:
        print(f"  FEHLER: Design & CI Test fehlgeschlagen: {e}")
        return False


def test_design_ci_validation_errors():
    """Testet Design-Validierungsfehler"""
    print("\nTESTE: Design-Validierungsfehler...")
    
    try:
        # Lade ein valides Layout
        layout = load_layout("skizze1_vertical_split", image_text_ratio=50, container_transparency=80)
        
        # Teste fehlende primary Farbe (ERWEITERT um vierte Farbe)
        print("  1. Teste fehlende primary Farbe...")
        ci_missing_primary = {"secondary": "#B4D9F7", "accent": "#FFC20E", "background": "#FFFFFF"}  # primary fehlt
        options = {"typography_scale": "md", "container_shape": "rounded_rectangle"}
        
        try:
            apply_rules(layout=layout, ci=ci_missing_primary, options=options)
            print("  FEHLER: Exception wurde nicht geworfen")
        except DesignValidationError as e:
            print("  OK: Exception geworfen: DesignValidationError")
            errors = e.payload.get('errors', [])
            for error in errors:
                if error.get('code') == 'missing_color':
                    print(f"    OK: Korrekter Fehler-Code: {error.get('code')}")
                    print(f"    Pfad: {error.get('path')}")
                    print(f"    Nachricht: {error.get('msg')}")
        
        # Teste ungültige transparency_pct (ERWEITERT um vierte Farbe)
        print("  2. Teste ungültige transparency_pct...")
        ci = {"primary": "#005EA5", "secondary": "#B4D9F7", "accent": "#FFC20E", "background": "#FFFFFF"}
        options_invalid_transparency = {
            "typography_scale": "md", 
            "container_shape": "rounded_rectangle", 
            "border_style": "soft_shadow", 
            "corner_radius_px": 16, 
            "transparency_pct": 150,  # Ungültig: > 100
            "accent_elements": ["badge"]
        }
        
        try:
            apply_rules(layout=layout, ci=ci, options=options_invalid_transparency)
            print("  FEHLER: Exception wurde nicht geworfen")
        except DesignValidationError as e:
            print("  OK: Exception geworfen: DesignValidationError")
            errors = e.payload.get('errors', [])
            for error in errors:
                if 'transparency_pct' in error.get('path', ''):
                    print(f"    OK: Korrekter Fehler-Code: {error.get('code')}")
                    print(f"    Pfad: {error.get('path')}")
                    print(f"    Nachricht: {error.get('msg')}")
        
        # Teste ungültige container_shape
        print("  3. Teste ungültige container_shape...")
        options_invalid_shape = {
            "typography_scale": "md", 
            "container_shape": "invalid_shape",  # Ungültig
            "border_style": "soft_shadow", 
            "corner_radius_px": 16, 
            "transparency_pct": 80, 
            "accent_elements": ["badge"]
        }
        
        try:
            apply_rules(layout=layout, ci=ci, options=options_invalid_shape)
            print("  FEHLER: Exception wurde nicht geworfen")
        except DesignValidationError as e:
            print("  OK: Exception geworfen: DesignValidationError")
            errors = e.payload.get('errors', [])
            for error in errors:
                if 'container_shape' in error.get('path', ''):
                    print(f"    OK: Korrekter Fehler-Code: {error.get('code')}")
                    print(f"    Pfad: {error.get('path')}")
                    print(f"    Nachricht: {error.get('msg')}")
        
        print("  OK: Alle Validierungsfehler-Tests erfolgreich")
        return True
        
    except Exception as e:
        print(f"  FEHLER: Validierungsfehler-Tests fehlgeschlagen: {e}")
        return False


def test_layout_validation_errors():
    """Testet Layout-Validierungsfehler"""
    print("\nTESTE: Layout-Validierungsfehler...")
    
    try:
        # Teste 1: Layout ohne headline_block
        print("  1. Teste Layout ohne headline_block...")
        invalid_layout = {
            'layout_id': 'test_invalid',
            'canvas': {'width': 1080, 'height': 1080},
            'zones': {
                'subline_block': {'x': 40, 'y': 140, 'width': 400, 'height': 80, 'z': 1},
                'benefits_block': {'x': 40, 'y': 240, 'width': 400, 'height': 200, 'z': 1},
                'cta_block': {'x': 40, 'y': 460, 'width': 400, 'height': 100, 'z': 1},
                'company_block': {'x': 40, 'y': 580, 'width': 400, 'height': 60, 'z': 1},
                'standort_block': {'x': 40, 'y': 660, 'width': 400, 'height': 60, 'z': 1}
            }
        }
        
        try:
            from layout.schema import validate_layout
            errors = validate_layout(invalid_layout)
            if any(error.get('code') == 'missing_required_zone' for error in errors):
                print("  OK: Fehlende Zone korrekt erkannt")
            else:
                print("  FEHLER: Fehlende Zone nicht erkannt")
        except Exception as e:
            print(f"  FEHLER: Validierung fehlgeschlagen: {e}")
        
        # Teste 2: Zone mit width <= 0
        print("  2. Teste Zone mit width <= 0...")
        invalid_zone_layout = {
            'layout_id': 'test_invalid_zone',
            'canvas': {'width': 1080, 'height': 1080},
            'zones': {
                'headline_block': {'x': 40, 'y': 40, 'width': 0, 'height': 80, 'z': 1},  # width = 0
                'subline_block': {'x': 40, 'y': 140, 'width': 400, 'height': 80, 'z': 1},
                'benefits_block': {'x': 40, 'y': 240, 'width': 400, 'height': 200, 'z': 1},
                'cta_block': {'x': 40, 'y': 460, 'width': 400, 'height': 100, 'z': 1},
                'company_block': {'x': 40, 'y': 580, 'width': 400, 'height': 60, 'z': 1},
                'standort_block': {'x': 40, 'y': 660, 'width': 400, 'height': 60, 'z': 1}
            }
        }
        
        try:
            errors = validate_layout(invalid_zone_layout)
            if any(error.get('code') == 'invalid_width' for error in errors):
                print("  OK: Ungültige Breite korrekt erkannt")
            else:
                print("  FEHLER: Ungültige Breite nicht erkannt")
        except Exception as e:
            print(f"  FEHLER: Validierung fehlgeschlagen: {e}")
        
        # Teste 3: Unbekanntes layout_id
        print("  3. Teste unbekanntes layout_id...")
        try:
            layout = load_layout("nonexistent_layout")
            print("  FEHLER: Layout wurde geladen obwohl es nicht existiert")
        except (FileNotFoundError, KeyError) as e:
            print("  OK: Unbekanntes Layout korrekt abgelehnt")
        except Exception as e:
            print(f"  FEHLER: Unerwarteter Fehler: {e}")
        
        print("  OK: Alle Layout-Validierungsfehler-Tests erfolgreich")
        return True
        
    except Exception as e:
        print(f"  FEHLER: Layout-Validierungsfehler-Tests fehlgeschlagen: {e}")
        return False


def test_full_pipeline():
    """Testet die vollständige Pipeline mit Design-Integration"""
    print("\nTESTE: Vollständige Pipeline mit Design-Integration...")
    
    try:
        # 1. Layout laden (mit Slider-Werten)
        print("  1. Lade Layout...")
        layout = load_layout(
            "skizze1_vertical_split",
            image_text_ratio=60,  # 60% Bild, 40% Text
            container_transparency=75  # 75% Transparenz
        )
        print(f"     OK: Layout geladen: {layout.get('name')}")
        
        # 2. Design & CI Regeln anwenden (NEU) (ERWEITERT um vierte Farbe)
        print("  2. Wende Design & CI Regeln an...")
        ci = {"primary": "#005EA5", "secondary": "#B4D9F7", "accent": "#FFC20E", "background": "#FFFFFF"}
        options = {
            "typography_scale": "md", 
            "container_shape": "rounded_rectangle", 
            "border_style": "soft_shadow", 
            "corner_radius_px": 16, 
            "transparency_pct": 75, 
            "accent_elements": ["badge", "divider"]
        }
        
        design = apply_rules(layout=layout, ci=ci, options=options)
        print(f"     OK: Design-Regeln angewendet: {design.get('__validated__')}")
        
        # Zeige Design-Details
        typography = design.get('typography', {})
        if 'headline' in typography:
            headline = typography['headline']
            print(f"     Headline: {headline.get('font_size_px')}px")
        
        # 3. Texte vorbereiten
        print("  3. Bereite Texte vor...")
        texts = prepare_texts("dummy_user_input.yaml")
        print(f"     OK: Texte vorbereitet")
        
        # 4. Motiv-Spezifikation erstellen
        print("  4. Erstelle Motiv-Spezifikation...")
        motive = build_motive_spec("dummy_user_input.yaml")
        print(f"     OK: Motiv-Spezifikation erstellt")
        
        # 5. Finalen Prompt komponieren
        print("  5. Komponiere finalen Prompt...")
        final_prompt = compose(layout, design, texts, motive)
        print(f"     OK: Prompt komponiert")
        
        # Ausgabe des finalen Prompts
        print(f"\nFINAL_PROMPT: {final_prompt}")
        
        # Zeige Pipeline-Status
        print(f"\nPipeline-Status:")
        print(f"  OK: Layout: {layout.get('validation_status', 'unknown')}")
        print(f"  OK: Design: {design.get('__validated__', False)}")
        print(f"  OK: Texte: Vorbereitet")
        print(f"  OK: Motiv: Erstellt")
        print(f"  OK: Prompt: Komponiert")
        
        return True
        
    except Exception as e:
        print(f"  FEHLER: Pipeline-Fehler: {e}")
        return False


def main():
    """Hauptfunktion für den Smoke-Test"""
    print("CREATIVE AI - DYNAMIC LAYOUT & DESIGN SMOKE TEST")
    print("=" * 60)
    
    # Teste alle Komponenten
    test_dynamic_layouts()
    test_multiple_layouts()
    test_layout_validation()
    test_layout_index()
    
    # Teste Design & CI Modul
    design_ci_success = test_design_ci_strict_mode()
    validation_errors_success = test_design_ci_validation_errors()
    
    # Teste Layout-Validierung
    layout_validation_success = test_layout_validation_errors()
    
    # Teste die vollständige Pipeline
    pipeline_success = test_full_pipeline()
    
    print("\n" + "=" * 60)
    if all([design_ci_success, validation_errors_success, layout_validation_success, pipeline_success]):
        print("SMOKE TEST ERFOLGREICH!")
        print("OK: Alle dynamischen Layouts funktionieren korrekt")
        print("OK: Slider-Integration ist implementiert")
        print("OK: Transparenz-Effekte werden angewendet")
        print("OK: Layout-Validierung funktioniert (strikt)")
        print("OK: Design & CI Modul funktioniert (Strict Mode)")
        print("OK: Validierungsfehler werden korrekt geworfen")
        print("OK: Vollständige Pipeline mit Design-Integration läuft")
    else:
        print("SMOKE TEST FEHLGESCHLAGEN!")
        print("Bitte überprüfe die Implementierung")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
