#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CreativeAI - Modulares Frontend
Haupt-Streamlit-App die alle Komponenten zusammenführt
"""

import streamlit as st
import sys
from pathlib import Path

# Projekt-Pfade konfigurieren
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.resolve()
sys.path.insert(0, str(project_root))

# Komponenten importieren
from frontend.components.layout_selector import render_layout_selector
from frontend.components.design_style import render_design_style
from frontend.components.text_inputs import render_text_inputs
from frontend.components.motif_inputs import render_motif_inputs
from frontend.components.pipeline_runner import render_pipeline_runner, render_pipeline_status
from frontend.utils.ui_helpers import apply_custom_css, create_header, create_footer

# Page Config
st.set_page_config(
    page_title="🎨 CreativeAI - Modulares Frontend",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS anwenden
apply_custom_css()

# Header
create_header(
    "🎨 CreativeAI - Modulares Frontend",
    "Teste die neue modulare Pipeline mit Layout-Engine + Style-Resolver"
)

# Sidebar für Navigation
st.sidebar.title("🧭 Navigation")
st.sidebar.markdown("---")

# Navigation
nav_options = [
    "🏠 Übersicht",
    "🎨 Layout-Auswahl",
    "🎭 Design & Style",
    "📝 Text-Eingaben",
    "🎭 Motiv-Eingaben",
    "🚀 Pipeline-Ausführung",
    "📊 Status"
]

selected_nav = st.sidebar.radio("Wähle einen Bereich:", nav_options)

# Session State initialisieren
if 'layout_data' not in st.session_state:
    st.session_state.layout_data = None
if 'design_data' not in st.session_state:
    st.session_state.design_data = None
if 'text_data' not in st.session_state:
    st.session_state.text_data = None
if 'motif_data' not in st.session_state:
    st.session_state.motif_data = None

# Hauptinhalt basierend auf Navigation
if selected_nav == "🏠 Übersicht":
    render_overview()
elif selected_nav == "🎨 Layout-Auswahl":
    st.session_state.layout_data = render_layout_selector()
elif selected_nav == "🎭 Design & Style":
    st.session_state.design_data = render_design_style()
elif selected_nav == "📝 Text-Eingaben":
    st.session_state.text_data = render_text_inputs()
elif selected_nav == "🎭 Motiv-Eingaben":
    st.session_state.motif_data = render_motif_inputs()
elif selected_nav == "🚀 Pipeline-Ausführung":
    render_pipeline_runner(
        st.session_state.layout_data,
        st.session_state.design_data,
        st.session_state.text_data,
        st.session_state.motif_data
    )
elif selected_nav == "📊 Status":
    render_pipeline_status()

# Sidebar-Status
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Aktueller Status")

# Status-Anzeige
layout_status = "✅" if st.session_state.layout_data else "❌"
design_status = "✅" if st.session_state.design_data else "❌"
text_status = "✅" if st.session_state.text_data else "❌"
motif_status = "✅" if st.session_state.motif_data else "❌"

st.sidebar.write(f"**Layout:** {layout_status}")
st.sidebar.write(f"**Design:** {design_status}")
st.sidebar.write(f"**Texte:** {text_status}")
st.sidebar.write(f"**Motiv:** {motif_status}")

# Gesamtstatus
total_components = 4
completed_components = sum([
    bool(st.session_state.layout_data),
    bool(st.session_state.design_data),
    bool(st.session_state.text_data),
    bool(st.session_state.motif_data)
])

st.sidebar.progress(completed_components / total_components)
st.sidebar.write(f"**Fortschritt:** {completed_components}/{total_components}")

# Footer
create_footer()

def render_overview():
    """Renders the overview page"""
    
    # Struktur wie in main.py: 1. Layout-Auswahl, 2. Design & Style, 3. Text-Eingabe, 4. Motiv-Eingabe, 5. Prompt-Generierung
    st.header("🏠 Übersicht")
    
    st.subheader("1. Layout-Auswahl (Skizzen + Templates)")
    st.caption("Auswahl eines Layouts und Grundkomposition via Schieberegler")
    st.divider()
    
    st.subheader("2. Design & Style")
    st.caption("CI-Farben, Container-Formen, Rahmen, Texturen, Akzente")
    st.divider()
    
    st.subheader("3. Text-Eingabe")
    st.caption("Manuell, Prompt-basiert, PDF-Upload oder KI-generiert")
    st.divider()
    
    st.subheader("4. Motiv-Eingabe")
    st.caption("Manuell, auto-generiert aus Kontext oder Bild-Upload")
    st.divider()
    
    st.subheader("5. Prompt-Generierung")
    st.caption("Komposition: Layout → Design → Texte → Motiv → finaler Prompt")
    st.divider()

def load_example_data():
    """Loads example data for testing"""
    
    # Beispiel-Layout-Daten
    st.session_state.layout_data = {
        'layout_id': 'skizze1_vertical_split',
        'layout_composition': 0.5,
        'container_transparency': 0.6,
        'layout_data': {
            'layout_id': 'skizze1_vertical_split',
            'layout_type': 'vertical_split',
            'canvas': {'width': 1080, 'height': 1080},
            'zones': {'headline_block': {}, 'subline_block': {}, 'cta_block': {}},
            '__validated__': True
        }
    }
    
    # Beispiel-Design-Daten
    st.session_state.design_data = {
        'primary_color': '#005EA5',
        'secondary_color': '#B4D9F7',
        'accent_color': '#FFC20E',
        'background_color': '#FFFFFF',
        'layout_style': ('rounded_modern', '🔵 Abgerundet & Modern'),
        'container_shape': ('rounded_rectangle', '📱 Abgerundet'),
        'border_style': ('soft_shadow', '🌫️ Weicher Schatten'),
        'texture_style': ('gradient', '🌈 Farbverlauf'),
        'background_treatment': ('subtle_pattern', '🌸 Subtiles Muster'),
        'corner_radius': ('medium', '⌜ Mittel'),
        'accent_elements': [('badge', '🏷️ Badge'), ('divider', '➖ Trennlinie')]
    }
    
    # Beispiel-Text-Daten
    st.session_state.text_data = {
        'headline': 'Werden Sie Teil unseres Teams!',
        'subline': 'Flexible Arbeitszeiten und attraktive Vergütung erwarten Sie.',
        'company': 'Musterfirma GmbH',
        'stellentitel': 'Pflegekraft (m/w/d)',
        'location': 'Berlin',
        'cta': 'Jetzt bewerben!',
        'benefits': [
            'Flexible Arbeitszeiten',
            'Attraktive Vergütung',
            'Fortbildungsmöglichkeiten',
            'Moderne Arbeitsplätze'
        ],
        'input_mode': 'manual'
    }
    
    # Beispiel-Motiv-Daten
    st.session_state.motif_data = {
        'motiv_prompt': 'Professionelle Pflegekraft in modernem Krankenhaus',
        'visual_style': 'Professionell',
        'lighting_type': 'Natürlich',
        'lighting_mood': 'Professionell',
        'framing': 'Medium Shot',
        'shot_type': 'Environmental',
        'persona': 'Professionell',
        'environment': 'Krankenhaus',
        'input_mode': 'manual'
    }

if __name__ == "__main__":
    # Zusätzliche Konfiguration für lokale Entwicklung
    st.markdown("""
    <style>
        .stApp {
            max-width: 1200px;
        }
    </style>
    """, unsafe_allow_html=True)
