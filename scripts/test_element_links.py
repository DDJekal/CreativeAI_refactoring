"""
Test Element Links - Testet die Verknüpfungen zwischen allen Komponenten

Prüft ob alle Module korrekt importiert werden können und zusammenarbeiten
"""

import sys
import os
from pathlib import Path

# Pfad zum Projekt-Root hinzufügen
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Testet alle wichtigen Imports"""
    print("🔍 Teste Imports...")
    
    try:
        # Layout-Module
        from creative_core.layout.loader import load_layout
        from creative_core.layout.engine import LayoutEngine
        print("✅ Layout-Module erfolgreich importiert")
        
        # Design-Module
        from creative_core.design_ci.rules import process_design_ci
        print("✅ Design-Module erfolgreich importiert")
        
        # Text-Module
        from creative_core.text_inputs.input_processor import create_text_processor
        print("✅ Text-Module erfolgreich importiert")
        
        # Motiv-Module
        from creative_core.motive_inputs.processor import create_motif_processor
        print("✅ Motiv-Module erfolgreich importiert")
        
        # Prompt-Composer
        from creative_core.prompt_composer.compose import compose
        print("✅ Prompt-Composer erfolgreich importiert")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import-Fehler: {e}")
        return False

def test_layout_loading():
    """Testet Layout-Laden"""
    print("\n📐 Teste Layout-Laden...")
    
    try:
        from creative_core.layout.loader import load_layout
        
        # Teste verschiedene Layouts
        test_layouts = ['skizze1_vertical_split', 'skizze7_minimalist_layout', 'skizze8_hero_layout']
        
        for layout_id in test_layouts:
            layout = load_layout(layout_id)
            if layout:
                print(f"✅ Layout {layout_id} erfolgreich geladen")
            else:
                print(f"❌ Layout {layout_id} konnte nicht geladen werden")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Layout-Test fehlgeschlagen: {e}")
        return False

def test_text_processing():
    """Testet Text-Verarbeitung"""
    print("\n📝 Teste Text-Verarbeitung...")
    
    try:
        from creative_core.text_inputs.input_processor import create_text_processor
        
        processor = create_text_processor()
        
        test_input = {
            'headline': 'Werden Sie Teil unseres Teams!',
            'subline': 'Flexible Arbeitszeiten und attraktive Vergütung.',
            'company': 'Klinikum München',
            'stellentitel': 'Pflegekraft (m/w/d)',
            'cta': 'Jetzt bewerben!',
            'benefits': ['Flexible Arbeitszeiten', 'Attraktive Vergütung']
        }
        
        result = processor.process_text_input(test_input)
        
        if result and result.get('ready_for_prompt'):
            print(f"✅ Text-Verarbeitung erfolgreich (Score: {result.get('text_quality_score', 0)})")
            return True
        else:
            print("❌ Text-Verarbeitung fehlgeschlagen")
            return False
            
    except Exception as e:
        print(f"❌ Text-Test fehlgeschlagen: {e}")
        return False

def test_motif_processing():
    """Testet Motiv-Verarbeitung"""
    print("\n🎨 Teste Motiv-Verarbeitung...")
    
    try:
        from creative_core.motive_inputs.processor import create_motif_processor
        
        processor = create_motif_processor()
        
        test_input = {
            'stellentitel': 'Pflegekraft (m/w/d)',
            'company': 'Klinikum München',
            'visual_style': 'Professionell',
            'lighting_type': 'Natürlich',
            'framing': 'Medium Shot'
        }
        
        result = processor.process_motif_input(test_input)
        
        if result and result.get('ready_for_generation'):
            print(f"✅ Motiv-Verarbeitung erfolgreich (Score: {result.get('quality_score', 0)})")
            return True
        else:
            print("❌ Motiv-Verarbeitung fehlgeschlagen")
            return False
            
    except Exception as e:
        print(f"❌ Motiv-Test fehlgeschlagen: {e}")
        return False

def test_design_processing():
    """Testet Design-Verarbeitung"""
    print("\n🎨 Teste Design-Verarbeitung...")
    
    try:
        from creative_core.design_ci.rules import process_design_ci
        
        test_input = {
            'primary_color': '#005EA5',
            'secondary_color': '#B4D9F7',
            'accent_color': '#FFC20E',
            'layout_style': 'rounded_modern',
            'container_shape': 'rounded_rectangle',
            'border_style': 'soft_shadow'
        }
        
        result = process_design_ci(test_input)
        
        if result and result.get('processing_success'):
            print("✅ Design-Verarbeitung erfolgreich")
            return True
        else:
            print("❌ Design-Verarbeitung fehlgeschlagen")
            return False
            
    except Exception as e:
        print(f"❌ Design-Test fehlgeschlagen: {e}")
        return False

def test_element_linking():
    """Testet die Verknüpfung aller Elemente"""
    print("\n🔗
