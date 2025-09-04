"""
Layout-Selector Komponente
Handles layout selection, slider interactions, and layout preview
"""

import streamlit as st
from pathlib import Path
from creative_core.layout import load_layout
from PIL import Image
import random

def render_layout_selector():
    """Renders the layout selection interface"""
    
    st.header("🎨 Layout-Auswahl")
    
    # Layout-Dateien laden
    layouts_dir = Path("input_config/layouts")
    available_layouts = []

    if layouts_dir.exists():
        for layout_file in layouts_dir.glob("*.yaml"):
            if not layout_file.name.endswith(".backup"):
                available_layouts.append(layout_file.stem)

    if not available_layouts:
        st.error("❌ Keine Layout-Dateien gefunden!")
        return None

    # Eingabemodus Auto/Manuell
    st.subheader("📐 Layout-Eingabe-Modus")
    layout_input_mode = st.radio(
        "Wähle deinen Layout-Eingabe-Modus:",
        ["🎲 Automatische Eingabe", "🎯 Manuelle Eingabe"],
        help="Automatisch: Zufälliges Layout | Manuell: Auswahl aus Liste",
        index=0
    )

    selected_layout = None

    if layout_input_mode == "🎯 Manuelle Eingabe":
        # Layout-Auswahl
        col1, col2 = st.columns([2, 1])

        with col1:
            selected_layout = st.selectbox(
                "Wähle ein Layout:",
                available_layouts,
                index=0,
                help="Wähle das gewünschte Layout-Template"
            )

        with col2:
            if selected_layout:
                preview_path = Path(f"Skizzen/{selected_layout.replace('skizze', 'Skizze')}.png")
                if preview_path.exists():
                    preview_image = Image.open(preview_path)
                    st.image(preview_image, width=150, caption=f"Vorschau: {selected_layout}")
    else:
        # Zufällige Auswahl mit Vorschau
        random_layout = random.choice(available_layouts)
        selected_layout = random_layout

        col1, col2 = st.columns([1, 2])
        with col1:
            preview_path = Path(f"Skizzen/{selected_layout.replace('skizze', 'Skizze')}.png")
            if preview_path.exists():
                preview_image = Image.open(preview_path)
                st.image(preview_image, width=160, caption=f"Zufällig: {selected_layout}")
        with col2:
            st.caption(f"🎯 Zufällig gewähltes Layout: {selected_layout}")
            if st.button("🔄 Anderes Layout wählen", key="regenerate_random_layout"):
                st.rerun()

    # Slider-Interaktion
    st.subheader("🎛️ Layout-Anpassung")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📐 Image-Text-Ratio**")
        layout_composition = st.slider(
            "Verhältnis Bild zu Text",
            min_value=0.1,
            max_value=0.9,
            value=0.5,
            step=0.1,
            help="0.1 = Mehr Text, 0.9 = Mehr Bild"
        )

        if layout_composition <= 0.3:
            ratio_description = "📝 Text-lastig"
        elif layout_composition <= 0.4:
            ratio_description = "⚖️ Ausgewogen (Text)"
        elif layout_composition <= 0.6:
            ratio_description = "⚖️ Ausgewogen"
        elif layout_composition <= 0.7:
            ratio_description = "⚖️ Ausgewogen (Bild)"
        else:
            ratio_description = "🖼️ Bild-lastig"
        st.write(f"**Aktuell:** {ratio_description}")

    with col2:
        st.markdown("**🌫️ Container-Transparenz**")
        container_transparency = st.slider(
            "Transparenz der Container",
            min_value=0.1,
            max_value=0.9,
            value=0.6,
            step=0.1,
            help="0.1 = Sehr transparent, 0.9 = Vollständig sichtbar"
        )

        if container_transparency <= 0.2:
            transparency_description = "👻 Sehr transparent"
        elif container_transparency <= 0.4:
            transparency_description = "🌫️ Transparent"
        elif container_transparency <= 0.6:
            transparency_description = "⚖️ Ausgewogen"
        elif container_transparency <= 0.8:
            transparency_description = "🔍 Sichtbar"
        else:
            transparency_description = "🎯 Vollständig sichtbar"
        st.write(f"**Aktuell:** {transparency_description}")

    # Layout-Info anzeigen
    try:
        layout_data = load_layout(selected_layout)
        st.success(f"✅ Layout '{selected_layout}' geladen")

        with st.expander("📊 Layout-Details"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write(f"**Typ:** {layout_data.get('layout_type', 'N/A')}")
                st.write(f"**Canvas:** {layout_data.get('canvas', {}).get('width', 'N/A')}x{layout_data.get('canvas', {}).get('height', 'N/A')}")
            with c2:
                st.write(f"**Zonen:** {len(layout_data.get('zones', {}))}")
                st.write(f"**Validierung:** {'✅' if layout_data.get('__validated__') else '❌'}")
            with c3:
                st.write(f"**Image-Ratio:** {int(30 + (layout_composition - 0.1) * 50)}%")
                st.write(f"**Transparenz:** {int(container_transparency * 100)}%")

        # Session State setzen (für andere Komponenten)
        st.session_state.selected_layout = selected_layout
        st.session_state.layout_composition = layout_composition
        st.session_state.container_transparency = container_transparency

        return {
            'layout_id': selected_layout,
            'layout_composition': layout_composition,
            'container_transparency': container_transparency,
            'layout_data': layout_data
        }

    except Exception as e:
        st.error(f"❌ Fehler beim Laden des Layouts: {e}")
        return None
    
    return None
