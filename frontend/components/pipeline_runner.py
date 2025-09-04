"""
Pipeline-Runner Komponente
Handles backend integration and pipeline execution
"""

import streamlit as st
import json
import logging
from pipeline import run_pipeline
from creative_core.layout import load_layout
from creative_core.design_ci import apply_rules
from creative_core.text_inputs import prepare_texts
from creative_core.motive_inputs import build_motive_spec
from creative_core.prompt_composer import compose

# Logging konfigurieren
logger = logging.getLogger(__name__)

def render_pipeline_runner(layout_data, design_data, text_data, motif_data):
    """Renders the pipeline execution interface"""
    
    st.header("🚀 Pipeline-Ausführung")
    
    # Pipeline-Status
    st.subheader("📊 Pipeline-Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        layout_status = "✅" if layout_data else "❌"
        st.metric("Layout", layout_status)
    
    with col2:
        design_status = "✅" if design_data else "❌"
        st.metric("Design", design_status)
    
    with col3:
        text_status = "✅" if text_data else "❌"
        st.metric("Texte", text_status)
    
    with col4:
        motif_status = "✅" if motif_data else "❌"
        st.metric("Motiv", motif_status)
    
    # Pipeline-Ausführung
    if layout_data and design_data and text_data and motif_data:
        st.success("✅ Alle Komponenten bereit für Pipeline-Ausführung!")
        
        # Ausführungs-Optionen
        col1, col2 = st.columns(2)
        
        with col1:
            execution_mode = st.radio(
                "Ausführungs-Modus:",
                ["🚀 Vollständige Pipeline", "🔧 Einzelne Komponenten testen"],
                help="Wähle wie die Pipeline ausgeführt werden soll"
            )
        
        with col2:
            enable_validation = st.checkbox(
                "Validierung aktivieren",
                value=True,
                help="Aktiviere strikte Validierung aller Komponenten"
            )
        
        # Pipeline ausführen
        if st.button("🚀 Pipeline ausführen", type="primary"):
            if execution_mode == "🚀 Vollständige Pipeline":
                execute_full_pipeline(layout_data, design_data, text_data, motif_data, enable_validation)
            else:
                test_individual_components(layout_data, design_data, text_data, motif_data, enable_validation)
    
    else:
        st.warning("⚠️ Bitte fülle alle Komponenten aus, bevor du die Pipeline ausführst.")
        
        # Fehlende Komponenten anzeigen
        missing_components = []
        if not layout_data:
            missing_components.append("Layout")
        if not design_data:
            missing_components.append("Design")
        if not text_data:
            missing_components.append("Texte")
        if not motif_data:
            missing_components.append("Motiv")
        
        st.write(f"**Fehlende Komponenten:** {', '.join(missing_components)}")

def execute_full_pipeline(layout_data, design_data, text_data, motif_data, enable_validation):
    """Executes the full pipeline"""
    
    with st.spinner("🔄 Führe vollständige Pipeline aus..."):
        try:
            # Eingabedaten zusammenstellen
            input_data = {
                'headline': text_data.get('headline', ''),
                'subline': text_data.get('subline', ''),
                'company': text_data.get('company', ''),
                'stellentitel': text_data.get('stellentitel', ''),
                'location': text_data.get('location', ''),
                'cta': text_data.get('cta', ''),
                'benefits': text_data.get('benefits', []),
                'motiv_prompt': motif_data.get('motiv_prompt', ''),
                'visual_style': motif_data.get('visual_style', ''),
                'lighting_type': motif_data.get('lighting_type', ''),
                'framing': motif_data.get('framing', '')
            }
            
            # CI-Farben
            ci_colors = {
                'primary': design_data.get('primary_color', '#005EA5'),
                'secondary': design_data.get('secondary_color', '#B4D9F7'),
                'accent': design_data.get('accent_color', '#FFC20E'),
                'background': design_data.get('background_color', '#FFFFFF')
            }
            
            # Pipeline ausführen (zusätzliche Optionen aus Session State)
            result = run_pipeline(
                layout_id=layout_data['layout_id'],
                image_text_ratio=int(30 + (layout_data['layout_composition'] - 0.1) * 50),
                container_transparency=int(layout_data['container_transparency'] * 100),
                design={
                    **input_data,
                    'layout_style': st.session_state.get('layout_style', ('rounded_modern', '🔵 Abgerundet & Modern')),
                    'container_shape': st.session_state.get('container_shape', ('rounded_rectangle', '📱 Abgerundet')),
                    'border_style': st.session_state.get('border_style', ('soft_shadow', '🌫️ Weicher Schatten')),
                    'texture_style': st.session_state.get('texture_style', ('gradient', '🌈 Farbverlauf')),
                    'background_treatment': st.session_state.get('background_treatment', ('subtle_pattern', '🌸 Subtiles Muster')),
                    'corner_radius': st.session_state.get('corner_radius', ('medium', '⌜ Mittel')),
                    'accent_elements': st.session_state.get('accent_elements', ('modern_minimal', '⚪ Modern Minimal')),
                    'element_spacing': st.session_state.get('element_spacing', 30),
                    'container_padding': st.session_state.get('container_padding', 20),
                    'shadow_intensity': st.session_state.get('shadow_intensity', 0.3)
                },
                ci_colors=ci_colors,
                validate=enable_validation
            )
            
            st.success("✅ Pipeline erfolgreich ausgeführt!")
            
            # Ergebnisse anzeigen
            display_pipeline_results(result)
            
        except Exception as e:
            st.error(f"❌ Fehler bei Pipeline-Ausführung: {e}")
            logger.error(f"Pipeline-Fehler: {e}", exc_info=True)

def test_individual_components(layout_data, design_data, text_data, motif_data, enable_validation):
    """Tests individual components"""
    
    with st.spinner("🔧 Teste einzelne Komponenten..."):
        try:
            # 1. Layout laden
            st.subheader("1️⃣ Layout laden")
            layout = load_layout(layout_data['layout_id'])
            st.success(f"✅ Layout geladen: {layout.get('layout_id')}")
            
            # 2. Texte verarbeiten
            st.subheader("2️⃣ Texte verarbeiten")
            texts = prepare_texts({
                'headline': text_data.get('headline', ''),
                'subline': text_data.get('subline', ''),
                'company': text_data.get('company', ''),
                'stellentitel': text_data.get('stellentitel', ''),
                'location': text_data.get('location', ''),
                'cta': text_data.get('cta', ''),
                'benefits': text_data.get('benefits', [])
            })
            st.success(f"✅ Texte verarbeitet: {len(texts)} Felder")
            
            # 3. Motiv spezifizieren
            st.subheader("3️⃣ Motiv spezifizieren")
            motive = build_motive_spec({
                'motiv_prompt': motif_data.get('motiv_prompt', ''),
                'visual_style': motif_data.get('visual_style', ''),
                'lighting_type': motif_data.get('lighting_type', ''),
                'framing': motif_data.get('framing', '')
            })
            st.success(f"✅ Motiv spezifiziert: {motive.get('motiv_prompt')}")
            
            # 4. Design-Regeln anwenden
            st.subheader("4️⃣ Design-Regeln anwenden")
            design = apply_rules(
                layout=layout,
                ci={
                    'primary': design_data.get('primary_color', '#005EA5'),
                    'secondary': design_data.get('secondary_color', '#B4D9F7'),
                    'accent': design_data.get('accent_color', '#FFC20E'),
                    'background': design_data.get('background_color', '#FFFFFF')
                },
                options={
                    'typography_scale': 'md',
                    'container_shape': 'rounded_rectangle',
                    'border_style': 'soft_shadow',
                    'corner_radius_px': 16,
                    'transparency_pct': int(layout_data['container_transparency'] * 100),
                    'accent_elements': ['badge', 'divider']
                }
            )
            st.success(f"✅ Design-Regeln angewendet: {len(design.get('typography', {}))} Typografie-Zonen")
            
            # 5. Prompt komponieren
            st.subheader("5️⃣ Prompt komponieren")
            final_prompt = compose(layout, design, texts, motive)
            st.success(f"✅ Prompt komponiert: {len(final_prompt)} Zeichen")
            
            # Finaler Prompt anzeigen
            st.subheader("🎯 Finaler Prompt")
            st.code(final_prompt, language="text")
            
            # Prompt kopieren
            if st.button("📋 Prompt kopieren"):
                st.write("Prompt in Zwischenablage kopiert!")
            
        except Exception as e:
            st.error(f"❌ Fehler beim Komponenten-Test: {e}")
            logger.error(f"Komponenten-Test-Fehler: {e}", exc_info=True)

def display_pipeline_results(result):
    """Displays pipeline results"""
    
    st.subheader("📊 Pipeline-Ergebnisse")
    
    # Layout-Info
    if 'layout' in result:
        layout_info = result['layout']
        st.write("**Layout-Informationen:**")
        st.json({
            'layout_id': layout_info.get('layout_id'),
            'layout_type': layout_info.get('layout_type'),
            'canvas_size': layout_info.get('canvas'),
            'zones_count': len(layout_info.get('zones', {})),
            'validated': layout_info.get('__validated__')
        })
    
    # Design-Info
    if 'design' in result:
        design_info = result['design']
        st.write("**Design-Informationen:**")
        st.json({
            'colors': design_info.get('colors'),
            'typography_zones': len(design_info.get('typography', {})),
            'container_styles': design_info.get('containers', {}).get('all', {}),
            'accent_elements': design_info.get('accents', {}).get('elements', [])
        })
    
    # Finaler Prompt
    if 'final_prompt' in result:
        st.subheader("🎯 Finaler Prompt")
        st.code(result['final_prompt'], language="text")
        
        # Prompt kopieren
        if st.button("📋 Prompt kopieren"):
            st.write("Prompt in Zwischenablage kopiert!")
    
    # Debug-Informationen
    with st.expander("🔍 Debug-Informationen"):
        st.json(result)

def render_pipeline_status():
    """Renders pipeline status information"""
    
    st.subheader("📊 Pipeline-Status")
    
    # Backend-Verfügbarkeit prüfen
    backend_status = check_backend_availability()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Layout-Engine", "✅" if backend_status['layout_engine'] else "❌")
    
    with col2:
        st.metric("Style-Resolver", "✅" if backend_status['style_resolver'] else "❌")
    
    with col3:
        st.metric("Text-Processor", "✅" if backend_status['text_processor'] else "❌")
    
    with col4:
        st.metric("Motiv-Processor", "✅" if backend_status['motif_processor'] else "❌")
    
    # Detaillierte Status-Info
    with st.expander("🔍 Detaillierte Status-Informationen"):
        for component, status in backend_status.items():
            st.write(f"**{component.replace('_', ' ').title()}:** {'✅ Verfügbar' if status else '❌ Nicht verfügbar'}")

def check_backend_availability():
    """Checks availability of backend components"""
    
    status = {
        'layout_engine': False,
        'style_resolver': False,
        'text_processor': False,
        'motif_processor': False
    }
    
    try:
        from creative_core.layout import load_layout
        status['layout_engine'] = True
    except ImportError:
        pass
    
    try:
        from creative_core.design_ci import apply_rules
        status['style_resolver'] = True
    except ImportError:
        pass
    
    try:
        from creative_core.text_inputs import prepare_texts
        status['text_processor'] = True
    except ImportError:
        pass
    
    try:
        from creative_core.motive_inputs import build_motive_spec
        status['motif_processor'] = True
    except ImportError:
        pass
    
    return status
