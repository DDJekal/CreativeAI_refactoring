"""
Design-Style Komponente
Handles CI colors, design styles, and visual customization
"""

import streamlit as st
import yaml
from pathlib import Path
import random

def render_design_style():
    """Renders the design and style interface"""
    
    st.header("🎨 Design & Style")
    
    # CI-Farben laden
    ci_colors_file = Path("input_config/ci_colors.yaml")
    default_colors = {}
    
    if ci_colors_file.exists():
        with open(ci_colors_file, 'r', encoding='utf-8') as f:
            ci_data = yaml.safe_load(f)
        default_colors = ci_data.get('default_colors', {})
    
    # CI-Farben + Randomizer + Paletten
    st.subheader("🎨 CI-Farben")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        primary_color = st.color_picker(
            "Primärfarbe",
            value=default_colors.get('primary', '#005EA5'),
            help="Hauptfarbe für Texte und wichtige Elemente"
        )
        st.markdown(f'<div style="width: 50px; height: 20px; background-color: {primary_color}; border-radius: 5px; margin: 5px;"></div>', unsafe_allow_html=True)
    
    with col2:
        secondary_color = st.color_picker(
            "Sekundärfarbe",
            value=default_colors.get('secondary', '#B4D9F7'),
            help="Sekundärfarbe für Hintergründe"
        )
        st.markdown(f'<div style="width: 50px; height: 20px; background-color: {secondary_color}; border-radius: 5px; margin: 5px;"></div>', unsafe_allow_html=True)
    
    with col3:
        accent_color = st.color_picker(
            "Akzentfarbe",
            value=default_colors.get('accent', '#FFC20E'),
            help="Akzentfarbe für CTAs und Highlights"
        )
        st.markdown(f'<div style="width: 50px; height: 20px; background-color: {accent_color}; border-radius: 5px; margin: 5px;"></div>', unsafe_allow_html=True)
    
    with col4:
        background_color = st.color_picker(
            "Hintergrundfarbe",
            value=default_colors.get('background', '#FFFFFF'),
            help="Haupt-Hintergrundfarbe"
        )
        st.markdown(f'<div style="width: 50px; height: 20px; background-color: {background_color}; border-radius: 5px; margin: 5px;"></div>', unsafe_allow_html=True)
    
    # RANDOMIZER Button wie in main.py
    colr1, colr2, colr3 = st.columns([2, 1, 2])
    with colr2:
        if st.button("🎲 Style randomisieren", type="secondary", use_container_width=True, key="randomize_style_button_header"):
            style_options = {
                'layout_style': [
                    ("sharp_geometric", "🎨 Scharf & Geometrisch"),
                    ("rounded_modern", "🔵 Abgerundet & Modern"),
                    ("organic_flowing", "🌊 Organisch & Fließend"),
                    ("wave_contours", "🌊 Wellige Konturen"),
                    ("hexagonal", "⬡ Sechseckig"),
                    ("circular", "⭕ Kreisförmig"),
                    ("asymmetric", "⚡ Asymmetrisch"),
                    ("minimal_clean", "⚪ Minimal & Clean")
                ],
                'container_shape': [
                    ("rectangle", "Rechteckig 📐"),
                    ("rounded_rectangle", "Abgerundet 📱"),
                    ("circle", "Kreisförmig ⭕"),
                    ("hexagon", "Sechseckig ⬡"),
                    ("organic_blob", "Organisch 🫧")
                ],
                'border_style': [
                    ("solid", "Durchgezogen ━"),
                    ("dashed", "Gestrichelt ┅"),
                    ("dotted", "Gepunktet ┈"),
                    ("soft_shadow", "Weicher Schatten 🌫️"),
                    ("glow", "Leuchteffekt ✨"),
                    ("none", "Ohne Rahmen")
                ],
                'texture_style': [
                    ("solid", "Einfarbig 🎨"),
                    ("gradient", "Farbverlauf 🌈"),
                    ("pattern", "Muster 📐"),
                    ("glass_effect", "Glas-Effekt 💎"),
                    ("matte", "Matt 🎭")
                ],
                'background_treatment': [
                    ("solid", "Einfarbig 🎨"),
                    ("subtle_pattern", "Subtiles Muster 🌸"),
                    ("geometric", "Geometrisch 📐"),
                    ("organic", "Organisch 🌿"),
                    ("none", "Transparent")
                ],
                'corner_radius': [
                    ("small", "Klein (8px) ⌐"),
                    ("medium", "Mittel (16px) ⌜"),
                    ("large", "Groß (24px) ⌞"),
                    ("xl", "Sehr groß (32px) ◜")
                ],
                'accent_elements': [
                    ("classic", "Klassisch 🏛️"),
                    ("modern_minimal", "Modern Minimal ⚪"),
                    ("playful", "Verspielt 🎪"),
                    ("organic", "Organisch 🌱"),
                    ("bold", "Auffällig ⚡")
                ]
            }

            st.session_state['layout_style'] = random.choice(style_options['layout_style'])
            st.session_state['container_shape'] = random.choice(style_options['container_shape'])
            st.session_state['border_style'] = random.choice(style_options['border_style'])
            st.session_state['texture_style'] = random.choice(style_options['texture_style'])
            st.session_state['background_treatment'] = random.choice(style_options['background_treatment'])
            st.session_state['corner_radius'] = random.choice(style_options['corner_radius'])
            st.session_state['accent_elements'] = random.choice(style_options['accent_elements'])

            # Zusätzliche Layout-Parameter
            st.session_state['element_spacing'] = random.randint(15, 60)
            st.session_state['container_padding'] = random.randint(10, 35)
            st.session_state['shadow_intensity'] = round(random.uniform(0.1, 0.7), 1)

            st.success("🎲 Style erfolgreich randomisiert!")
            st.rerun()

    # CI-Paletten aus Datei, falls vorhanden
    palettes = []
    try:
        if ci_colors_file.exists():
            with open(ci_colors_file, 'r', encoding='utf-8') as f:
                ci_yaml = yaml.safe_load(f)
            palettes_yaml = ci_yaml.get('color_schemes', {})
            for name, data in palettes_yaml.items():
                palettes.append({
                    'name': name,
                    'primary': data.get('primary'),
                    'secondary': data.get('secondary'),
                    'accent': data.get('accent'),
                    'background': data.get('background'),
                    'description': data.get('description', '')
                })
    except Exception:
        pass

    # Randomizer für CI-Farben
    colp1, colp2, colp3 = st.columns([2, 1, 2])
    with colp2:
        if palettes and st.button("🎲 CI-Farben randomisieren", type="secondary", use_container_width=True, key="randomize_ci_colors_button"):
            rp = random.choice(palettes)
            st.session_state.primary_color = rp['primary']
            st.session_state.secondary_color = rp['secondary']
            st.session_state.accent_color = rp['accent']
            st.session_state.background_color = rp['background']
            st.success(f"🎨 Neue Farbpalette: {rp['name']}")
            st.rerun()

    if palettes:
        st.caption("Vordefinierte CI-Paletten:")
        cols = st.columns(min(3, len(palettes)))
        for i, p in enumerate(palettes):
            with cols[i % 3]:
                if st.button(f"📋 {p['name']}", key=f"palette_{i}", use_container_width=True):
                    st.session_state.primary_color = p['primary']
                    st.session_state.secondary_color = p['secondary']
                    st.session_state.accent_color = p['accent']
                    st.session_state.background_color = p['background']
                    st.rerun()
                st.markdown(f"""
                <div style="display: flex; height: 30px; border-radius: 5px; overflow: hidden; margin: 5px 0;">
                    <div style="background: {p['primary']}; flex: 1;"></div>
                    <div style="background: {p['secondary']}; flex: 1;"></div>
                    <div style="background: {p['accent']}; flex: 1;"></div>
                    <div style="background: {p['background']}; flex: 1; border-left: 1px solid #ddd;"></div>
                </div>
                """, unsafe_allow_html=True)

    # Design-Styles
    st.subheader("🎭 Design-Styles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        layout_style = st.selectbox(
            "Layout-Style",
            [
                ("rounded_modern", "🔵 Abgerundet & Modern"),
                ("sharp_contemporary", "🔷 Scharf & Zeitgemäß"),
                ("soft_minimal", "🔸 Weich & Minimal"),
                ("bold_dynamic", "🔴 Mutig & Dynamisch")
            ],
            format_func=lambda x: x[1],
            help="Gesamtstil des Layouts"
        )
        
        container_shape = st.selectbox(
            "Container-Form",
            [
                ("rounded_rectangle", "📱 Abgerundet"),
                ("rectangle", "⬜ Rechteckig"),
                ("pill", "💊 Pill-Form"),
                ("circle", "⭕ Rund")
            ],
            format_func=lambda x: x[1],
            help="Form der Container-Elemente"
        )
        
        border_style = st.selectbox(
            "Rahmen-Style",
            [
                ("none", "🚫 Kein Rahmen"),
                ("soft_shadow", "🌫️ Weicher Schatten"),
                ("hard_shadow", "🌑 Harter Schatten"),
                ("outline", "📐 Umriss")
            ],
            format_func=lambda x: x[1],
            help="Art des Rahmens"
        )
    
    with col2:
        texture_style = st.selectbox(
            "Textur-Style",
            [
                ("solid", "🎨 Einfarbig"),
                ("gradient", "🌈 Farbverlauf"),
                ("pattern", "🔳 Muster"),
                ("texture", "🧱 Textur")
            ],
            format_func=lambda x: x[1],
            help="Textur der Container"
        )
        
        background_treatment = st.selectbox(
            "Hintergrund-Behandlung",
            [
                ("solid", "🎨 Einfarbig"),
                ("subtle_pattern", "🌸 Subtiles Muster"),
                ("gradient", "🌈 Farbverlauf"),
                ("texture", "🧱 Textur")
            ],
            format_func=lambda x: x[1],
            help="Behandlung des Hintergrunds"
        )
        
        corner_radius = st.selectbox(
            "Ecken-Rundung",
            [
                ("small", "⌜ Klein"),
                ("medium", "⌜ Mittel"),
                ("large", "⌜ Groß"),
                ("extra_large", "⌜ Extra Groß")
            ],
            format_func=lambda x: x[1],
            help="Stärke der Ecken-Rundung"
        )
    
    # Akzent-Elemente
    st.subheader("✨ Akzent-Elemente")
    
    accent_elements = st.multiselect(
        "Wähle Akzent-Elemente:",
        [
            ("badge", "🏷️ Badge"),
            ("divider", "➖ Trennlinie"),
            ("pin", "📍 Pin"),
            ("dot", "⚫ Punkt"),
            ("icon", "🎯 Icon")
        ],
        default=[("badge", "🏷️ Badge"), ("divider", "➖ Trennlinie")],
        format_func=lambda x: x[1],
        help="Zusätzliche visuelle Elemente"
    )
    
    # Zusätzliche Slider (Spacing, Padding, Shadow)
    st.subheader("🎛️ Zusätzliche Layout-Parameter")
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        element_spacing = st.slider("Element-Abstände (px)", 5, 80, value=int(st.session_state.get('element_spacing', 30)))
    with col_s2:
        container_padding = st.slider("Container-Padding (px)", 5, 40, value=int(st.session_state.get('container_padding', 20)))
    with col_s3:
        shadow_intensity = st.slider("Schatten-Intensität", 0.0, 1.0, value=float(st.session_state.get('shadow_intensity', 0.3)))

    # Werte im Session State persistieren
    st.session_state.element_spacing = element_spacing
    st.session_state.container_padding = container_padding
    st.session_state.shadow_intensity = shadow_intensity

    # Style-Vorschau
    st.subheader("👁️ Style-Vorschau")
    
    style_preview_cols = st.columns(4)
    
    with style_preview_cols[0]:
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 8px; background: {primary_color}; color: white; text-align: center;">
            <strong>🎨 STYLE</strong><br>
            <small>{layout_style[1]}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with style_preview_cols[1]:
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 8px; background: linear-gradient(45deg, {secondary_color}40, {primary_color}20); border: 2px solid {primary_color};">
            <strong>Form:</strong> {container_shape[1]}<br>
            <strong>Rahmen:</strong> {border_style[1]}
        </div>
        """, unsafe_allow_html=True)
    
    with style_preview_cols[2]:
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 8px; background: linear-gradient(45deg, {secondary_color}40, {primary_color}20); border: 2px solid {primary_color};">
            <strong>Textur:</strong> {texture_style[1]}<br>
            <strong>Hintergrund:</strong> {background_treatment[1]}
        </div>
        """, unsafe_allow_html=True)
    
    with style_preview_cols[3]:
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 8px; background: {accent_color}; color: white; text-align: center;">
            <strong>✨ AKZENTE</strong><br>
            <small>{len(accent_elements)} Elemente</small>
        </div>
        """, unsafe_allow_html=True)
    
    return {
        'primary_color': primary_color,
        'secondary_color': secondary_color,
        'accent_color': accent_color,
        'background_color': background_color,
        'layout_style': layout_style,
        'container_shape': container_shape,
        'border_style': border_style,
        'texture_style': texture_style,
        'background_treatment': background_treatment,
        'corner_radius': corner_radius,
        'accent_elements': accent_elements
    }
