"""
Motif-Inputs Komponente
Handles motif input, visual styles, and image generation parameters
"""

import streamlit as st
from PIL import Image

def render_motif_inputs():
    """Renders the motif input interface"""
    
    st.header("🎭 Motiv-Eingaben")
    
    # Motiv-Eingabe-Modus
    motif_input_mode = st.radio(
        "Motiv-Eingabe-Modus:",
        ["✏️ Manuelle Eingabe", "🤖 Auto-Generierung", "📷 Bild-Upload"],
        help="Wähle wie du das Motiv eingeben möchtest"
    )
    
    if motif_input_mode == "✏️ Manuelle Eingabe":
        return render_manual_motif_input()
    elif motif_input_mode == "🤖 Auto-Generierung":
        return render_auto_motif_generation()
    elif motif_input_mode == "📷 Bild-Upload":
        return render_image_upload()
    
    return {}

def render_manual_motif_input():
    """Renders manual motif input fields"""
    
    st.subheader("✏️ Manuelle Motiveingabe")
    
    col1, col2 = st.columns(2)
    
    with col1:
        motiv_prompt = st.text_area(
            "Motiv-Prompt:",
            value="Professionelle Pflegekraft in modernem Krankenhaus",
            help="Beschreibung des gewünschten Motivs"
        )
        
        visual_style = st.selectbox(
            "Visueller Stil:",
            ["Professionell", "Modern", "Freundlich", "Dynamisch", "Seriös"],
            help="Gewünschter visueller Stil"
        )
        
        lighting_type = st.selectbox(
            "Beleuchtung:",
            ["Natürlich", "Künstlich", "Gemischt", "Dramatisch"],
            help="Art der Beleuchtung"
        )
    
    with col2:
        lighting_mood = st.selectbox(
            "Beleuchtungsstimmung:",
            ["Professionell", "Warm", "Kühl", "Dynamisch", "Beruhigend"],
            help="Stimmung der Beleuchtung"
        )
        
        framing = st.selectbox(
            "Framing:",
            ["Close-up", "Medium Shot", "Wide Shot", "Extreme Wide Shot"],
            help="Art der Aufnahme"
        )
        
        shot_type = st.selectbox(
            "Aufnahmetyp:",
            ["Portrait", "Action", "Environmental", "Detail"],
            help="Typ der Aufnahme"
        )
    
    # Zusätzliche Parameter
    with st.expander("🎨 Erweiterte Parameter"):
        col1, col2 = st.columns(2)
        
        with col1:
            persona = st.selectbox(
                "Persona:",
                ["Professionell", "Freundlich", "Autoritativ", "Zugänglich"],
                help="Art der Person"
            )
            
            environment = st.selectbox(
                "Umgebung:",
                ["Büro", "Krankenhaus", "Labor", "Außenbereich", "Konferenzraum"],
                help="Arbeitsumgebung"
            )
        
        with col2:
            camera_angle = st.selectbox(
                "Kamerawinkel:",
                ["Frontal", "Schräg", "Von oben", "Von unten"],
                help="Perspektive der Aufnahme"
            )
            
            composition = st.selectbox(
                "Komposition:",
                ["Zentriert", "Drittel-Regel", "Symmetrisch", "Dynamisch"],
                help="Komposition des Bildes"
            )
    
    return {
        'motiv_prompt': motiv_prompt,
        'visual_style': visual_style,
        'lighting_type': lighting_type,
        'lighting_mood': lighting_mood,
        'framing': framing,
        'shot_type': shot_type,
        'persona': persona,
        'environment': environment,
        'camera_angle': camera_angle,
        'composition': composition,
        'input_mode': 'manual'
    }

def render_auto_motif_generation():
    """Renders auto motif generation based on job data"""
    
    st.subheader("🤖 Auto-Motiv-Generierung")
    
    # Kontext-Eingaben
    col1, col2 = st.columns(2)
    
    with col1:
        stellentitel = st.text_input(
            "Stellentitel:",
            value="Pflegekraft (m/w/d)",
            help="Titel der Position für automatische Motiv-Generierung"
        )
        
        industry = st.selectbox(
            "Branche:",
            ["Pflege", "IT", "Beratung", "Handel", "Bildung", "Technik"],
            help="Branche für Motiv-Kontext"
        )
        
        company_type = st.selectbox(
            "Unternehmensart:",
            ["Startup", "KMU", "Großunternehmen", "Krankenhaus", "Klinik"],
            help="Art des Unternehmens"
        )
    
    with col2:
        location = st.text_input(
            "Standort:",
            value="Berlin",
            help="Standort für Motiv-Kontext"
        )
        
        work_environment = st.selectbox(
            "Arbeitsumgebung:",
            ["Büro", "Krankenhaus", "Labor", "Außenbereich", "Remote"],
            help="Art der Arbeitsumgebung"
        )
        
        team_size = st.selectbox(
            "Team-Größe:",
            ["Einzelarbeit", "Kleines Team", "Großes Team", "Abteilung"],
            help="Größe des Teams"
        )
    
    # Auto-Generierung
    if st.button("🤖 Motiv automatisch generieren", type="primary"):
        with st.spinner("Generiere Motiv basierend auf Kontext..."):
            # Hier würde die automatische Motiv-Generierung stattfinden
            # Für jetzt verwenden wir Fallback-Generierung
            auto_generated = generate_motif_from_context(
                stellentitel, industry, company_type, location, work_environment, team_size
            )
            
            st.success("✅ Motiv erfolgreich generiert!")
            
            # Generiertes Motiv anzeigen
            st.write("**Generiertes Motiv:**")
            st.code(auto_generated['motiv_prompt'], language="text")
            
            # Alle Parameter anzeigen
            with st.expander("🎭 Generierte Parameter"):
                for key, value in auto_generated.items():
                    if key != 'motiv_prompt':
                        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
            
            return auto_generated
    
    return {'input_mode': 'auto_generation'}

def render_image_upload():
    """Renders image upload with description"""
    
    st.subheader("📷 Bild-Upload")
    
    uploaded_image = st.file_uploader(
        "Lade ein Bild hoch:",
        type=['png', 'jpg', 'jpeg'],
        help="Lade ein Referenzbild für das Motiv hoch"
    )
    
    if uploaded_image is not None:
        # Bild anzeigen
        image = Image.open(uploaded_image)
        st.image(image, caption="Hochgeladenes Bild", use_column_width=True)
        
        # Zusätzliche Beschreibung
        st.subheader("📝 Zusätzliche Beschreibung")
        
        col1, col2 = st.columns(2)
        
        with col1:
            image_description = st.text_area(
                "Beschreibe das gewünschte Motiv:",
                value="Professionelle Person in ähnlicher Umgebung",
                help="Beschreibe was du dir für das finale Motiv vorstellst"
            )
            
            style_adjustments = st.multiselect(
                "Style-Anpassungen:",
                ["Professioneller", "Moderner", "Freundlicher", "Dynamischer", "Seriöser"],
                help="Wie soll der Stil angepasst werden?"
            )
        
        with col2:
            lighting_preference = st.selectbox(
                "Beleuchtungs-Präferenz:",
                ["Wie im Bild", "Natürlicher", "Künstlicher", "Dramatischer"],
                help="Gewünschte Beleuchtung"
            )
            
            framing_preference = st.selectbox(
                "Framing-Präferenz:",
                ["Wie im Bild", "Näher", "Weiter", "Anderer Winkel"],
                help="Gewünschtes Framing"
            )
        
        # Verarbeitung
        if st.button("🔄 Bild verarbeiten", type="primary"):
            with st.spinner("Verarbeite Bild und Beschreibung..."):
                # Hier würde die Bildverarbeitung stattfinden
                processed_motif = {
                    'motiv_prompt': f"Motiv basierend auf hochgeladenem Bild: {image_description}",
                    'visual_style': "Professionell",
                    'lighting_type': lighting_preference,
                    'lighting_mood': "Professionell",
                    'framing': framing_preference,
                    'shot_type': "Environmental",
                    'persona': "Professionell",
                    'environment': "Custom Environment",
                    'has_uploaded_image': True,
                    'style_adjustments': style_adjustments,
                    'input_mode': 'image_upload'
                }
                
                st.success("✅ Bild erfolgreich verarbeitet!")
                
                # Verarbeitetes Motiv anzeigen
                st.write("**Verarbeitetes Motiv:**")
                st.code(processed_motif['motiv_prompt'], language="text")
                
                return processed_motif
    
    return {'input_mode': 'image_upload'}

def generate_motif_from_context(stellentitel, industry, company_type, location, work_environment, team_size):
    """Generates motif based on job context"""
    
    # Motiv-Generierung basierend auf Kontext
    if "pflege" in stellentitel.lower():
        base_prompt = "Professionelle Pflegekraft in modernem Krankenhaus"
        environment = "Krankenhaus"
        persona = "Pflegekraft"
    elif "entwickler" in stellentitel.lower() or "programmierer" in stellentitel.lower():
        base_prompt = "Professioneller Entwickler am modernen Arbeitsplatz"
        environment = "Büro"
        persona = "Entwickler"
    elif "berater" in stellentitel.lower():
        base_prompt = "Professioneller Berater im Kundengespräch"
        environment = "Konferenzraum"
        persona = "Berater"
    else:
        base_prompt = "Professioneller Mitarbeiter in moderner Arbeitsumgebung"
        environment = work_environment
        persona = "Professioneller Mitarbeiter"
    
    # Kontext hinzufügen
    if company_type:
        base_prompt += f" bei {company_type}"
    if location:
        base_prompt += f" in {location}"
    
    return {
        'motiv_prompt': base_prompt,
        'visual_style': 'Professionell',
        'lighting_type': 'Natürlich',
        'lighting_mood': 'Professionell',
        'framing': 'Medium Shot',
        'shot_type': 'Environmental',
        'persona': persona,
        'environment': environment,
        'camera_angle': 'Frontal',
        'composition': 'Zentriert',
        'input_mode': 'auto_generation'
    }
