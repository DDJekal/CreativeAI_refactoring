#!/usr/bin/env python3
"""
Script zum Aktualisieren des Frontends für Slider-Integration
"""

import os
import sys

def update_frontend():
    """Aktualisiert das Frontend für Slider-Integration"""
    
    frontend_file = os.path.join(os.path.dirname(__file__), '..', 'streamlit_app_multi_prompt_enhanced_restructured.py')
    
    # Lese die aktuelle Datei
    with open(frontend_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Korrigiere Layout-Namen
    old_layout2 = '''    {
        "id": "skizze2_horizontal",
        "name": "Horizontal Strips", 
        "description": "Horizontale Streifen-Anordnung",
        "sketch": original_sketches.get("Skizze2")
    },'''
    
    new_layout2 = '''    {
        "id": "skizze2_vertical_split_left",
        "name": "Vertikaler Split (Motiv Links)", 
        "description": "Motiv links, Text rechts",
        "sketch": original_sketches.get("Skizze2")
    },'''
    
    if old_layout2 in content:
        content = content.replace(old_layout2, new_layout2)
        print("✅ Layout 2 Namen korrigiert")
    else:
        print("❌ Konnte Layout 2 nicht finden")
    
    # 2. Füge Slider-Integration hinzu
    old_ci_section = "# CI Color Palette\nst.subheader(\"🎨 CI-Farbpalette\")"
    
    new_slider_section = '''# Layout-Slider Integration
st.subheader("🎛️ Layout-Anpassungen")

# Image/Text Ratio Slider
col1, col2 = st.columns(2)

with col1:
    image_text_ratio = st.slider(
        "Bild/Text Verhältnis",
        min_value=30, 
        max_value=70, 
        value=50,
        step=5,
        help="30% = mehr Text, 70% = mehr Bild. Bestimmt das Verhältnis zwischen Motiv- und Text-Bereich."
    )

with col2:
    container_transparency = st.slider(
        "Container Transparenz",
        min_value=0, 
        max_value=100, 
        value=80,
        step=5,
        help="0% = vollständig transparent, 100% = undurchsichtig. Bestimmt die Transparenz der Text-Container."
    )

# Slider-Werte in Session State speichern
st.session_state['image_text_ratio'] = image_text_ratio
st.session_state['container_transparency'] = container_transparency

# Slider-Info anzeigen
st.caption(f"🎯 **Aktuelles Verhältnis:** {image_text_ratio}% Bild, {100-image_text_ratio}% Text")
st.caption(f"🎨 **Container Transparenz:** {container_transparency}%")

# CI Color Palette
st.subheader("🎨 CI-Farbpalette")'''
    
    if old_ci_section in content:
        content = content.replace(old_ci_section, new_slider_section)
        print("✅ Slider-Integration hinzugefügt")
    else:
        print("❌ Konnte CI-Sektion nicht finden")
    
    # 3. Füge Layout-Engine Import hinzu
    old_imports = "import streamlit as st"
    new_imports = '''import streamlit as st
from creative_core.layout import load_layout'''
    
    if old_imports in content and "from creative_core.layout import load_layout" not in content:
        content = content.replace(old_imports, new_imports)
        print("✅ Layout-Engine Import hinzugefügt")
    else:
        print("ℹ️ Layout-Engine Import bereits vorhanden oder nicht gefunden")
    
    # 4. Füge Layout-Loading mit Slider-Werten hinzu
    # Suche nach dem Bereich, wo das Layout verwendet wird
    old_layout_usage = "layout_id = selected_layout_id"
    new_layout_usage = '''# Layout mit Slider-Werten laden
try:
    layout_data = load_layout(
        layout_id, 
        image_text_ratio=st.session_state.get('image_text_ratio', 50),
        container_transparency=st.session_state.get('container_transparency', 80)
    )
    st.session_state['layout_data'] = layout_data
    st.caption(f"✅ Layout geladen: {layout_data.get('name', 'Unbekannt')}")
except Exception as e:
    st.error(f"❌ Fehler beim Laden des Layouts: {e}")
    layout_data = None

layout_id = selected_layout_id'''
    
    if old_layout_usage in content:
        content = content.replace(old_layout_usage, new_layout_usage)
        print("✅ Layout-Loading mit Slider-Werten hinzugefügt")
    else:
        print("❌ Konnte Layout-Usage nicht finden")
    
    # Schreibe die aktualisierte Datei
    with open(frontend_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Frontend erfolgreich aktualisiert!")
    return True

if __name__ == "__main__":
    update_frontend()
