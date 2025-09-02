#!/usr/bin/env python3
"""
Script zum Aktualisieren der main.py für Layout-Engine Integration
"""

import os
import sys

def update_main_frontend():
    """Aktualisiert die main.py für Layout-Engine Integration"""
    
    main_file = os.path.join(os.path.dirname(__file__), '..', 'main.py')
    
    # Lese die aktuelle Datei
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Korrigiere Layout-Namen
    old_layout2_dict = '''        'skizze2_horizontal_split': {
            'description': 'Horizontal geteiltes Layout mit klarer Trennung',
            'features': ['horizontal division', 'clear separation', 'balanced sections', 'organized layout'],
            'visual_style': 'Klare, organisierte Aufteilung'
        },'''
    
    new_layout2_dict = '''        'skizze2_vertical_split_left': {
            'description': 'Vertikales Split-Layout mit Motiv links und Text rechts',
            'features': ['vertical division', 'motiv left', 'text right', 'balanced layout'],
            'visual_style': 'Klare, vertikale Aufteilung'
        },'''
    
    if old_layout2_dict in content:
        content = content.replace(old_layout2_dict, new_layout2_dict)
        print("✅ Layout 2 Dictionary korrigiert")
    else:
        print("❌ Konnte Layout 2 Dictionary nicht finden")
    
    # 2. Korrigiere Layout-Liste
    old_layout2_list = '''    {
        "id": "skizze2_horizontal_split",
        "name": "Horizontal Split", 
        "description": "Oben Text, unten Motiv",
        "sketch": original_sketches.get("Skizze2"),
        "template": "skizze2_horizontal_split",
        "render_command": "finale Werbebild jetzt direkt rendern und ausgeben"
    },'''
    
    new_layout2_list = '''    {
        "id": "skizze2_vertical_split_left",
        "name": "Vertikaler Split (Motiv Links)", 
        "description": "Motiv links, Text rechts",
        "sketch": original_sketches.get("Skizze2"),
        "template": "skizze2_vertical_split_left",
        "render_command": "finale Werbebild jetzt direkt rendern und ausgeben"
    },'''
    
    if old_layout2_list in content:
        content = content.replace(old_layout2_list, new_layout2_list)
        print("✅ Layout 2 Liste korrigiert")
    else:
        print("❌ Konnte Layout 2 Liste nicht finden")
    
    # 3. Füge Layout-Engine Import hinzu
    old_imports = "import streamlit as st"
    new_imports = '''import streamlit as st
from creative_core.layout import load_layout'''
    
    if old_imports in content and "from creative_core.layout import load_layout" not in content:
        content = content.replace(old_imports, new_imports)
        print("✅ Layout-Engine Import hinzugefügt")
    else:
        print("ℹ️ Layout-Engine Import bereits vorhanden oder nicht gefunden")
    
    # 4. Füge Layout-Engine Integration hinzu
    # Suche nach dem Bereich, wo das Layout verwendet wird
    old_layout_usage = "# Layout-Engine Integration fehlt noch"
    new_layout_usage = '''# Layout-Engine Integration
def load_layout_with_sliders(layout_id, layout_composition, container_transparency):
    """
    Lädt Layout mit Slider-Werten über den Layout-Engine
    
    Args:
        layout_id: ID des Layouts (z.B. 'skizze1_vertical_split')
        layout_composition: Slider-Wert 0.1-0.9 (wird zu 30-70% konvertiert)
        container_transparency: Slider-Wert 0.1-0.9 (wird zu 0-100% konvertiert)
    
    Returns:
        Layout-Dictionary mit berechneten Koordinaten
    """
    try:
        # Konvertiere Slider-Werte zu Layout-Engine Format
        # layout_composition: 0.1-0.9 -> 30-70%
        image_text_ratio = int(30 + (layout_composition - 0.1) * 50)  # 0.1->30, 0.9->70
        
        # container_transparency: 0.1-0.9 -> 0-100%
        transparency_percent = int((container_transparency - 0.1) * 125)  # 0.1->0, 0.9->100
        
        # Lade Layout über Layout-Engine
        layout_data = load_layout(
            layout_id,
            image_text_ratio=image_text_ratio,
            container_transparency=transparency_percent
        )
        
        return layout_data
        
    except Exception as e:
        st.error(f"❌ Fehler beim Laden des Layouts: {e}")
        return None'''
    
    # Füge die Funktion nach den Imports hinzu
    import_section = "from creative_core.layout import load_layout"
    if import_section in content and "def load_layout_with_sliders" not in content:
        # Füge die Funktion nach dem Import hinzu
        content = content.replace(import_section, import_section + "\n\n" + new_layout_usage)
        print("✅ Layout-Engine Integration hinzugefügt")
    else:
        print("ℹ️ Layout-Engine Integration bereits vorhanden oder Import nicht gefunden")
    
    # 5. Füge Layout-Engine Aufruf in der Hauptfunktion hinzu
    # Suche nach dem Bereich, wo das Layout verwendet wird
    old_layout_call = "# Layout-Engine Aufruf fehlt noch"
    new_layout_call = '''# Layout-Engine Aufruf
        layout_data = load_layout_with_sliders(
            selected_layout_id, 
            layout_composition, 
            container_transparency
        )
        
        if layout_data:
            st.success(f"✅ Layout geladen: {layout_data.get('name', 'Unbekannt')}")
            st.caption(f"📐 Berechnete Werte: {layout_data.get('calculated_values', {})}")
        else:
            st.warning("⚠️ Layout konnte nicht geladen werden")'''
    
    # Schreibe die aktualisierte Datei
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ main.py erfolgreich aktualisiert!")
    return True

if __name__ == "__main__":
    update_main_frontend()
