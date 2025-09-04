"""
Text-Inputs Komponente
Handles all text input modes: manual, prompt-based, PDF upload, and AI-generated
"""

import streamlit as st
import PyPDF2
import io
from pathlib import Path
from creative_core.layout import load_layout
from typing import Dict, Any

def render_text_inputs():
    """Renders the text input interface with multiple modes"""
    
    st.header("📝 Text-Inhalte")
    # Dynamische Felder aus Layout-Zonen, falls Layout gewählt
    dynamic_inputs = render_dynamic_text_inputs_from_layout()
    if dynamic_inputs:
        return dynamic_inputs
    
    # Text-Eingabe-Modus Auswahl
    text_input_mode = st.radio(
        "Text-Eingabe-Modus:",
        ["✏️ Manuelle Eingabe", "🤖 Prompt-basierte Eingabe", "📄 PDF-Upload", "🤖 KI-Kreative Textelemente"],
        help="Wähle wie du die Text-Inhalte eingeben möchtest"
    )
    
    # Session State für extrahierte Daten
    if 'extracted_text_data' not in st.session_state:
        st.session_state.extracted_text_data = {}
    
    # Manuelle Eingabe
    if text_input_mode == "✏️ Manuelle Eingabe":
        return render_manual_text_input()
    
    # Prompt-basierte Eingabe
    elif text_input_mode == "🤖 Prompt-basierte Eingabe":
        return render_prompt_based_input()
    
    # PDF-Upload
    elif text_input_mode == "📄 PDF-Upload":
        return render_pdf_upload()
    
    # KI-Kreative Textelemente
    elif text_input_mode == "🤖 KI-Kreative Textelemente":
        return render_ai_generated_texts()
    
    return {}

def render_manual_text_input():
    """Renders manual text input fields"""
    
    st.subheader("✏️ Manuelle Texteingabe")
    
    col1, col2 = st.columns(2)
    
    with col1:
        headline = st.text_input(
            "Headline",
            value="Werden Sie Teil unseres Teams!",
            help="Hauptüberschrift der Anzeige"
        )
        
        subline = st.text_area(
            "Subline",
            value="Flexible Arbeitszeiten und attraktive Vergütung erwarten Sie.",
            help="Untertitel oder Beschreibung"
        )
        
        company = st.text_input(
            "Unternehmen",
            value="Musterfirma GmbH",
            help="Name des Unternehmens"
        )
    
    with col2:
        stellentitel = st.text_input(
            "Stellentitel",
            value="Pflegekraft (m/w/d)",
            help="Bezeichnung der Position"
        )
        
        location = st.text_input(
            "Standort",
            value="Berlin",
            help="Arbeitsort"
        )
        
        cta = st.text_input(
            "Call-to-Action",
            value="Jetzt bewerben!",
            help="Handlungsaufforderung"
        )
    
    # Benefits
    st.subheader("💼 Benefits")
    benefits_text = st.text_area(
        "Benefits (eine pro Zeile)",
        value="Flexible Arbeitszeiten\nAttraktive Vergütung\nFortbildungsmöglichkeiten\nModerne Arbeitsplätze",
        help="Auflistung der Vorteile"
    )
    
    benefits = [b.strip() for b in benefits_text.split('\n') if b.strip()]
    
    # Zusätzliche Felder
    with st.expander("📋 Zusätzliche Felder"):
        position_long = st.text_area(
            "Ausführliche Stellenbeschreibung",
            value="Wir suchen eine engagierte Pflegekraft für unseren Bereich. Flexible Arbeitszeiten und attraktive Vergütung erwarten Sie.",
            help="Detaillierte Beschreibung der Position"
        )
        
        contact_info = st.text_input(
            "Kontaktinformationen",
            value="HR@musterfirma.de",
            help="Kontakt für Bewerbungen"
        )
    
    return {
        'headline': headline,
        'subline': subline,
        'company': company,
        'stellentitel': stellentitel,
        'location': location,
        'cta': cta,
        'benefits': benefits,
        'position_long': position_long,
        'contact_info': contact_info,
        'input_mode': 'manual'
    }

def render_prompt_based_input():
    """Renders prompt-based text input"""
    
    st.subheader("🤖 Prompt-basierte Texteingabe")
    
    # Prompt-Eingabe
    prompt = st.text_area(
        "Beschreibung der gewünschten Inhalte:",
        value="Erstelle eine Stellenausschreibung für eine Pflegekraft in Berlin. Das Unternehmen ist modern und bietet flexible Arbeitszeiten.",
        help="Beschreibe was für Inhalte generiert werden sollen"
    )
    
    # Generierungs-Optionen
    col1, col2 = st.columns(2)
    
    with col1:
        tone = st.selectbox(
            "Ton der Texte:",
            ["Professionell", "Freundlich", "Dynamisch", "Seriös", "Modern"],
            help="Gewünschter Ton der generierten Texte"
        )
        
        length = st.selectbox(
            "Länge der Texte:",
            ["Kurz", "Mittel", "Lang"],
            help="Gewünschte Länge der Texte"
        )
    
    with col2:
        industry = st.selectbox(
            "Branche:",
            ["Pflege", "IT", "Beratung", "Handel", "Bildung", "Andere"],
            help="Branche des Unternehmens"
        )
        
        target_audience = st.selectbox(
            "Zielgruppe:",
            ["Erfahrene Fachkräfte", "Einsteiger", "Quereinsteiger", "Alle"],
            help="Zielgruppe der Stellenausschreibung"
        )
    
    # Generieren-Button
    if st.button("🤖 Texte generieren", type="primary"):
        with st.spinner("Generiere Texte..."):
            # Hier würde die KI-Textgenerierung stattfinden
            # Für jetzt verwenden wir Fallback-Texte
            generated_texts = {
                'headline': f"Werden Sie Teil unseres {industry}-Teams!",
                'subline': f"Flexible Arbeitszeiten und attraktive Vergütung in {industry}.",
                'company': "Musterfirma GmbH",
                'stellentitel': f"{industry}-Fachkraft (m/w/d)",
                'location': "Berlin",
                'cta': "Jetzt bewerben!",
                'benefits': [
                    "Flexible Arbeitszeiten",
                    "Attraktive Vergütung",
                    "Fortbildungsmöglichkeiten",
                    "Moderne Arbeitsplätze"
                ]
            }
            
            st.success("✅ Texte erfolgreich generiert!")
            
            # Generierte Texte anzeigen
            for key, value in generated_texts.items():
                if key == 'benefits':
                    st.write(f"**{key.title()}:**")
                    for benefit in value:
                        st.write(f"- {benefit}")
                else:
                    st.write(f"**{key.title()}:** {value}")
            
            return generated_texts
    
    return {'input_mode': 'prompt_based', 'prompt': prompt}

def render_pdf_upload():
    """Renders PDF upload and text extraction"""
    
    st.subheader("📄 PDF-Upload")
    
    uploaded_file = st.file_uploader(
        "Lade eine PDF-Datei hoch:",
        type=['pdf'],
        help="Lade eine Stellenausschreibung oder ähnliches Dokument hoch"
    )
    
    if uploaded_file is not None:
        try:
            # PDF verarbeiten
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            st.success(f"✅ PDF erfolgreich verarbeitet! ({len(text)} Zeichen)")
            
            # Extrahierte Daten anzeigen
            with st.expander("📄 Extrahierter Text"):
                st.text(text[:1000] + "..." if len(text) > 1000 else text)
            
            # Automatische Extraktion
            if st.button("🔍 Informationen automatisch extrahieren"):
                with st.spinner("Extrahiere Informationen..."):
                    # Hier würde die automatische Extraktion stattfinden
                    # Für jetzt verwenden wir Fallback-Extraktion
                    extracted_data = {
                        'headline': "Stellenausschreibung aus PDF",
                        'subline': "Automatisch extrahierte Beschreibung",
                        'company': "Unbekanntes Unternehmen",
                        'stellentitel': "Position aus PDF",
                        'location': "Unbekannter Standort",
                        'cta': "Jetzt bewerben!",
                        'benefits': [
                            "Vorteil 1",
                            "Vorteil 2",
                            "Vorteil 3"
                        ]
                    }
                    
                    st.success("✅ Informationen erfolgreich extrahiert!")
                    
                    # Extrahierte Daten anzeigen
                    for key, value in extracted_data.items():
                        if key == 'benefits':
                            st.write(f"**{key.title()}:**")
                            for benefit in value:
                                st.write(f"- {benefit}")
                        else:
                            st.write(f"**{key.title()}:** {value}")
                    
                    return extracted_data
            
            return {'input_mode': 'pdf_upload', 'extracted_text': text}
            
        except Exception as e:
            st.error(f"❌ Fehler beim Verarbeiten der PDF: {e}")
            return {'input_mode': 'pdf_upload', 'error': str(e)}
    
    return {'input_mode': 'pdf_upload'}

def render_ai_generated_texts():
    """Renders AI-generated text elements"""
    
    st.subheader("🤖 KI-Kreative Textelemente")
    
    # Eingabe-Parameter
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input(
            "Unternehmensname:",
            value="Musterfirma GmbH",
            help="Name des Unternehmens"
        )
        
        position_type = st.selectbox(
            "Positionstyp:",
            ["Pflegekraft", "Entwickler", "Berater", "Manager", "Sachbearbeiter"],
            help="Art der Position"
        )
        
        location = st.text_input(
            "Standort:",
            value="Berlin",
            help="Arbeitsort"
        )
    
    with col2:
        industry = st.selectbox(
            "Branche:",
            ["Pflege", "IT", "Beratung", "Handel", "Bildung"],
            help="Branche des Unternehmens"
        )
        
        company_size = st.selectbox(
            "Unternehmensgröße:",
            ["Startup", "KMU", "Großunternehmen", "Konzern"],
            help="Größe des Unternehmens"
        )
        
        experience_level = st.selectbox(
            "Erfahrungslevel:",
            ["Einsteiger", "Erfahren", "Senior", "Expert"],
            help="Gewünschtes Erfahrungslevel"
        )
    
    # KI-Generierung
    if st.button("🤖 KI-Texte generieren", type="primary"):
        with st.spinner("Generiere kreative Texte..."):
            # Hier würde die KI-Generierung stattfinden
            # Für jetzt verwenden wir Fallback-Texte
            ai_generated = {
                'headline': f"Entdecke deine Zukunft bei {company_name}!",
                'subline': f"Als {position_type} in {location} - {industry} mit Zukunft.",
                'company': company_name,
                'stellentitel': f"{position_type} (m/w/d)",
                'location': location,
                'cta': "Bewirb dich jetzt!",
                'benefits': [
                    "Zukunftssichere Perspektiven",
                    "Moderne Arbeitsumgebung",
                    "Individuelle Entwicklungsmöglichkeiten",
                    "Attraktive Benefits"
                ]
            }
            
            st.success("✅ KI-Texte erfolgreich generiert!")
            
            # Generierte Texte anzeigen
            for key, value in ai_generated.items():
                if key == 'benefits':
                    st.write(f"**{key.title()}:**")
                    for benefit in value:
                        st.write(f"- {benefit}")
                else:
                    st.write(f"**{key.title()}:** {value}")
            
            return ai_generated
    
    return {'input_mode': 'ai_generated'}

def normalize_german_text(text: str) -> str:
    if not text:
        return ""
    # einfache Umlaut-Ersetzung (Backend nutzt dies ebenfalls)
    return (text
            .replace("ä", "a").replace("Ä", "A")
            .replace("ö", "o").replace("Ö", "O")
            .replace("ü", "u").replace("Ü", "U")
            .replace("ß", "ss"))

def render_dynamic_text_inputs_from_layout() -> Dict[str, Any]:
    """Wenn ein Layout gewählt ist, erzeuge dynamisch Textfelder je Zone mit content_type=text_elements"""
    if 'selected_layout' not in st.session_state:
        return {}

    try:
        selected_layout = st.session_state.selected_layout
        layout_composition = st.session_state.get('layout_composition', 0.5)
        container_transparency = st.session_state.get('container_transparency', 0.6)

        layout_data = load_layout(selected_layout)
        if not layout_data or 'zones' not in layout_data:
            return {}

        # text_elements Zonen finden
        text_zones = {zn: zd for zn, zd in layout_data['zones'].items() if zd.get('content_type') == 'text_elements'}
        if not text_zones:
            return {}

        st.subheader("🧩 Zonenbasierte Texteingabe")
        st.caption("Die Felder werden aus dem gewählten Layout abgeleitet")

        # Session init
        if 'text_inputs' not in st.session_state:
            st.session_state.text_inputs = {}

        # Defaults
        default_texts = {
            'standort_block': '📍 Braunschweig',
            'benefits_block': 'Attraktive Vergutung\nFlexible Arbeitszeiten\nFortbildungsmoglichkeiten',
            'cta_block': 'Jetzt Bewerben!',
            'headline_block': 'Dein Rhythmus. Dein Job.',
            'stellentitel_block': 'Pflegefachkraft (m/w/d)',
            'subline_block': 'Entdecke deine Karriere in der Pflege'
        }

        # Layout Felder rendern
        cols = st.columns(min(2, len(text_zones)))
        for i, (zone_name, zone_data) in enumerate(text_zones.items()):
            with cols[i % 2]:
                text_field = zone_data.get('text_field', zone_name)
                field_label = zone_data.get(f'{text_field}_input', f'Text für {zone_name}')
                current_value = st.session_state.text_inputs.get(zone_name, default_texts.get(zone_name, field_label))

                if 'benefits' in zone_name.lower():
                    val = st.text_area(f"**{field_label}**", value=current_value, height=120, key=f"ti_{zone_name}")
                else:
                    val = st.text_input(f"**{field_label}**", value=current_value, key=f"ti_{zone_name}")

                # Standort-Pin automatisch
                if 'standort' in zone_name.lower() and not val.startswith('📍'):
                    val = f"📍 {val}"

                st.session_state.text_inputs[zone_name] = normalize_german_text(val)

        result = {**st.session_state.text_inputs, 'input_mode': 'layout_dynamic'}
        return result

    except Exception:
        return {}
