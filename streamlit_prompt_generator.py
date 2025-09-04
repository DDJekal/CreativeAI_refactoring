import random
import json
import streamlit as st
from streamlit.components.v1 import html
from entkoppelt_multiprompt.graph import build_app
from entkoppelt_multiprompt.pretty_output import generate_human_readable_output

st.set_page_config(page_title="ChatGPT Prompt Generator", page_icon="🧩", layout="centered")

# Feste Layout-IDs aus deinem Set
ALL_LAYOUTS = [
    "skizze1_vertical_split",
    "skizze2_vertical_split_left",
    "skizze3_centered_layout",
    "skizze4_diagonal_layout",
    "skizze5_asymmetric_layout",
    "skizze6_grid_layout",
    "skizze7_split_layout",
    "skizze8_hero_layout",
    "skizze9_dual_headline_layout",
    "skizze10_modern_split",
    "skizze11_infographic_layout",
    "skizze12_magazine_layout",
    "skizze13_portfolio_layout",
]

# Layouts mit erzwungenem Vollbild-Motiv (100% Bild)
FULL_BG_LAYOUTS = {
    "skizze3_centered_layout",
    "skizze4_diagonal_layout",
    "skizze5_asymmetric_layout",
    "skizze6_grid_layout",
    "skizze9_dual_headline_layout",
}

# Erweiterte Design-Optionen (10 Kategorien)
LAYOUT_STYLE = [
    "Abgerundet Modern", "Scharf & Zeitgemaess", "Organisch & Fliessend", "Geometrisch & Praezise",
    "Neon Tech", "Editorial Clean", "Soft Neumorph", "Glassmorph Minimal", "Clay UI", "Warm Documentary"
]
CONTAINER_SHAPE = [
    "Abgerundet", "Scharf", "Organisch", "Geometrisch", "Capsule", "Ribbon", "Tag"
]
BORDER_STYLE = [
    "Keine", "Weicher Schatten", "Harte Konturen", "Gradient-Rand", "Doppelstrich", 
    "Innenlinie", "Emboss", "Outline-Glow"
]
TEXTURE_STYLE = [
    "Farbverlauf", "GlasEffekt", "Matte Oberflaeche", "Strukturiert", "Paper Grain",
    "Film Grain", "Noise Gradient", "Subtle Pattern", "Soft Neumorph", "Emboss/Deboss"
]
BACKGROUND_TREATMENT = [
    "Transparent", "Vollflaechig", "Gradient", "Subtiles Muster", "Duotone Motivtint",
    "Vignette Soft", "Depth Layers"
]
CORNER_RADIUS = [
    "Klein 8px", "Mittel 16px", "Gross 24px", "Sehr Gross 32px", "Auto-Radius"
]
ACCENT_ELEMENTS = [
    "Modern Minimal", "Sanft Organisch", "Geometrisch Praezise", "Kreativ Verspielt",
    "Micro-Badges", "Divider Dots", "Icon Chips"
]

# Neue Design-Kategorien
TYPOGRAPHY_STYLE = [
    "Humanist Sans", "Grotesk Bold", "Serif Editorial", "Mono Detail", "Rounded Sans"
]
PHOTO_TREATMENT = [
    "Natural Daylight", "Cinematic Warm", "Clean Clinic", "Documentary Soft Grain",
    "Duotone Subtle", "Bokeh Light"
]
DEPTH_STYLE = [
    "Soft Shadow Stack", "Drop + Inner Shadow", "Card Elevation 1", "Card Elevation 2", "Card Elevation 3"
]
MOTIV_QUALITY = ["Authentisch & Warm", "Professionell & Vertrauensvoll", "Einfuehlsam & Menschlich", "Dynamisch & Energetisch", "Ruhig & Beruhigend"]
MOTIV_STYLE = ["Natuerlich & Candid", "Documentary-Stil", "Studio-Professional", "Cinematisch & Dramatisch", "Kuenstlerisch & Kreativ"]
LIGHTING_TYPE = ["Natuerliches Tageslicht", "Studio-Beleuchtung", "Dramatisches Licht", "Sanftes Licht", "Kontrastreiches Licht"]
FRAMING = ["Nahaufnahme", "Halbtotale", "Totale", "Detailaufnahme", "Gruppenaufnahme"]

# CI-Farben (strict) – Default + Paletten (zufällige Auswahl pro Run)
CI = {
    "primary": "#8E24AA",
    "secondary": "#F3E5F5",
    "accent": "#FFC107",
    "background": "#E8F5E8",
}

CI_PALETTES = [
    {"primary": "#0F62FE", "secondary": "#E0E7FF", "accent": "#FF6F00", "background": "#FFFFFF"},
    {"primary": "#2E7D32", "secondary": "#E8F5E9", "accent": "#FF9800", "background": "#FFFFFF"},
    {"primary": "#6A1B9A", "secondary": "#F3E5F5", "accent": "#FFC107", "background": "#FFFFFF"},
    {"primary": "#1565C0", "secondary": "#E3F2FD", "accent": "#FF7043", "background": "#FFFFFF"},
    {"primary": "#C62828", "secondary": "#FFEBEE", "accent": "#FF9800", "background": "#FFFFFF"},
    {"primary": "#00897B", "secondary": "#E0F2F1", "accent": "#FFB300", "background": "#FFFFFF"},
    {"primary": "#455A64", "secondary": "#ECEFF1", "accent": "#FF6F00", "background": "#FFFFFF"},
    {"primary": "#7B1FA2", "secondary": "#F3E5F5", "accent": "#FF8F00", "background": "#FFFFFF"},
    {"primary": "#1E88E5", "secondary": "#E3F2FD", "accent": "#F50057", "background": "#FFFFFF"},
    {"primary": "#43A047", "secondary": "#E8F5E9", "accent": "#FF5722", "background": "#FFFFFF"},
    {"primary": "#8E24AA", "secondary": "#F3E5F5", "accent": "#26C6DA", "background": "#FFFFFF"},
    {"primary": "#3949AB", "secondary": "#E8EAF6", "accent": "#FFB300", "background": "#FFFFFF"},
    {"primary": "#D81B60", "secondary": "#FCE4EC", "accent": "#00ACC1", "background": "#FFFFFF"},
    {"primary": "#5D4037", "secondary": "#EFEBE9", "accent": "#FF7043", "background": "#FFFFFF"},
    {"primary": "#0097A7", "secondary": "#E0F7FA", "accent": "#FF6F00", "background": "#FFFFFF"},
]

# Templates (Vorlagen) für sofortige Befüllung ohne Eingabe
TEMPLATES = {
    "Braunschweig": {
        "location": "Braunschweig",
        "headline": "Dein Rhythmus. Dein Job.",
        "headline_1": "Dein Rhythmus.",
        "headline_2": "Dein Job.",
        "subline": "Ehrliche Wertschätzung, nicht nur nette Worte",
        "benefit_1": "bis zu 4700 € im Monat",
        "benefit_2": "Flexible Arbeitszeiten",
        "benefit_3": "Unbefristeter Vertrag",
        "stellentitel": "Pflegefachkraft (m/w/d)",
        "cta": "Jetzt bewerben!",
    },
}

def rand_int(a, b):
    return random.randint(a, b)

def choose(arr):
    return random.choice(arr)

def build_chatgpt_prompt(payload: dict, fixed_choices: dict, sliders: dict, enforce_full_bg: bool, ci: dict | None = None) -> str:
    # Schlanker, klarer Meta-Prompt für ChatGPT (Deutsch)
    user_texts = f"""- location: {payload.get('location','')}
- headline: {payload.get('headline','')}
- headline_1: {payload.get('headline_1','')}
- headline_2: {payload.get('headline_2','')}
- subline: {payload.get('subline','')}
- benefits:
  - {payload.get('benefit_1','')}
  - {payload.get('benefit_2','')}
  - {payload.get('benefit_3','')}
- stellentitel: {payload.get('stellentitel','')}
- cta: {payload.get('cta','')}"""

    fixed_params = f"""- layout_id: {fixed_choices['layout_id']}
- layout_style: {fixed_choices['layout_style']}
- container_shape: {fixed_choices['container_shape']}
- border_style: {fixed_choices['border_style']}
- texture_style: {fixed_choices['texture_style']}
- background_treatment: {fixed_choices['background_treatment']}
- corner_radius: {fixed_choices['corner_radius']}
- accent_elements: {fixed_choices['accent_elements']}
- typography_style: {fixed_choices.get('typography_style', 'Humanist Sans')}
- photo_treatment: {fixed_choices.get('photo_treatment', 'Natural Daylight')}
- depth_style: {fixed_choices.get('depth_style', 'Soft Shadow Stack')}
- motiv_quality: {fixed_choices['motiv_quality']}
- motiv_style: {fixed_choices['motiv_style']}
- lighting_type: {fixed_choices['lighting_type']}
- framing: {fixed_choices['framing']}"""

    if enforce_full_bg:
        slider_text = f"""- image_text_ratio: 100 % (erzwungen: Vollbild-Hintergrund durch Layout)
- container_transparency: {sliders['container_transparency']} %
- element_spacing: {sliders['element_spacing']} px
- container_padding: {sliders['container_padding']} px
- shadow_intensity: {sliders['shadow_intensity']} %
- grain_amount: {sliders.get('grain_amount', 5)} %
- tint_strength: {sliders.get('tint_strength', 8)} %
- glow_intensity: {sliders.get('glow_intensity', 10)} %
- elevation_level: {sliders.get('elevation_level', 1)}"""
        layout_rule = "- Dieses Layout erzwingt ein Vollbild-Motiv (100 % Bild). Das MUSS beibehalten werden; keinerlei Reduktion."
    else:
        slider_text = f"""- image_text_ratio: {sliders['image_text_ratio']} %
- container_transparency: {sliders['container_transparency']} %
- element_spacing: {sliders['element_spacing']} px
- container_padding: {sliders['container_padding']} px
- shadow_intensity: {sliders['shadow_intensity']} %
- grain_amount: {sliders.get('grain_amount', 5)} %
- tint_strength: {sliders.get('tint_strength', 8)} %
- glow_intensity: {sliders.get('glow_intensity', 10)} %
- elevation_level: {sliders.get('elevation_level', 1)}"""
        layout_rule = "- Motivanteil muss zwischen 55–85 % liegen (≥ 55 %)."

    _ci = ci or CI
    ci_text = f"""- primary: {_ci['primary']}
- secondary: {_ci['secondary']}
- accent: {_ci['accent']}
- background: {_ci['background']}"""

    prompt = f"""Rolle: Du bist Experte fuer DALL·E‑3‑Prompts.
Ziel: Erzeuge einen hochwertigen, deutschsprachigen Prompt im untenstehenden Ziel-Format (2000–3000 Zeichen), text_rendering: "separate_layers". Nur die gelieferten USER‑Texte verwenden, nichts hinzufuegen.

USER‑TEXTE (nur verwenden, nichts hinzuerfinden)
{user_texts}

GEWAEHLTE PARAMETER (fix, nicht erneut randomisieren)
{fixed_params}

SLIDER (fix)
{slider_text}

CI‑COLORS (strict)
{ci_text}

ZIEL‑PROMPT‑FORMAT (genau diese Reihenfolge)
Szene & Atmosphaere
[… abgestimmt auf Motiv …]

Komposition & Layout
[… exakte Anordnung, Bezug auf layout_id, Slider, Hierarchie; Motiv{" = 100 % Vollbild" if enforce_full_bg else " ≥ image_text_ratio"} …]

Form & Design
[… Container-Formen, Border/Shadow/Texture, Eckenradius, Akzente …]

Farbwelt & CI
[… nur obige CI-Codes …]

Text & Content (separate_layers)
[… Standort, Headline/dual Headline, Subline, Benefits, Stellentitel, CTA …]

Balance & Wirkung
[… Wirkung bei Motiv {"= 100 %" if enforce_full_bg else "≥ image_text_ratio"} , Klarheit der Textkontraste …]

Technische Regeln & Engine‑Optimierung
- text_rendering: "separate_layers"
- Umlaute im Overlay als ae/oe/ue/ss; im Bild selbst KEINE Texte/ASCII‑Hinweise
- 1080×1080, social‑ready, keine Rahmen/Wasserzeichen
- Laenge gesamt: 2000–3000 Zeichen
- {layout_rule}

Validierung (vor Ausgabe pruefen)
- Laenge zwischen 2000 und 3000 Zeichen
- Pro Set genau 1 Option (fix vorgegeben)
- Alle Slider gesetzt (fix vorgegeben)
- Keine Inhalte ausserhalb der USER‑Texte
- “separate_layers” vorhanden; KEIN Text im Bild
"""
    return prompt

st.title("🧩 ChatGPT Prompt Generator (nur Texteingaben)")

# Template-Auswahl und automatische Übernahme in den Session State
template_name = st.selectbox("Vorlage", options=list(TEMPLATES.keys()), index=0)
if st.session_state.get("_applied_template") != template_name:
    for k, v in TEMPLATES[template_name].items():
        st.session_state[k] = v
    st.session_state["_applied_template"] = template_name

# CI-Paletten-Auswahl
st.subheader("🎨 CI-Farbpalette")

# Erstelle Paletten-Optionen mit visueller Darstellung
palette_options = []
palette_names = [
    "🔵 Corporate Blue", "🟢 Nature Green", "🟣 Creative Purple", "🔷 Professional Blue",
    "🔴 Bold Red", "🟢 Teal Modern", "⚫ Industrial Gray", "🟣 Deep Purple",
    "🔵 Sky Blue", "🟢 Success Green", "🟣 Brand Purple", "🔷 Royal Blue",
    "🔴 Pink Accent", "🟤 Earth Brown", "🔵 Ocean Blue"
]

for i, palette in enumerate(CI_PALETTES):
    palette_name = f"{palette_names[i]} ({palette['primary']})"
    palette_options.append((i, palette_name, palette))

# Füge "Zufällig" Option hinzu
palette_options.append((-1, "🎲 Zufällig (Random)", None))

selected_palette_idx = st.selectbox(
    "Wähle eine CI-Farbpalette:",
    options=[opt[0] for opt in palette_options],
    format_func=lambda x: palette_options[x][1],
    index=st.session_state.get("selected_palette_idx", 0),
    key="palette_selector"
)

# Speichere ausgewählte Palette im Session State
st.session_state["selected_palette_idx"] = selected_palette_idx

# Bestimme die tatsächlich zu verwendende Palette
if selected_palette_idx == -1:  # Zufällig
    selected_palette = choose(CI_PALETTES)
    st.session_state["use_random_palette"] = True
    # Reset angepasste Palette bei zufälliger Auswahl
    st.session_state["use_custom_palette"] = False
    st.session_state["custom_palette"] = None
else:
    selected_palette = CI_PALETTES[selected_palette_idx]
    st.session_state["use_random_palette"] = False
    # Reset angepasste Palette bei neuer Palette-Auswahl
    if st.session_state.get("last_selected_palette_idx") != selected_palette_idx:
        st.session_state["use_custom_palette"] = False
        st.session_state["custom_palette"] = None
        st.session_state["last_selected_palette_idx"] = selected_palette_idx

# Direkte Farbanpassung
if selected_palette_idx != -1:  # Nur bei ausgewählter Palette
    # Bestimme die anzuzeigende Palette (berücksichtige angepasste Farben)
    display_palette = selected_palette
    if st.session_state.get("use_custom_palette", False) and st.session_state.get("custom_palette"):
        display_palette = st.session_state.get("custom_palette", selected_palette)
    
    # Direkte Farbanpassung
    st.write("**🎨 Farben individuell anpassen:**")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        # Primary & Secondary Farben
        custom_primary = st.color_picker(
            "Primary-Farbe:", 
            value=display_palette['primary'],
            key="custom_primary"
        )
        custom_secondary = st.color_picker(
            "Secondary-Farbe:", 
            value=display_palette['secondary'],
            key="custom_secondary"
        )
    
    with col_b:
        # Accent & Background Farben
        custom_accent = st.color_picker(
            "Accent-Farbe:", 
            value=display_palette['accent'],
            key="custom_accent"
        )
        custom_background = st.color_picker(
            "Background-Farbe:", 
            value=display_palette['background'],
            key="custom_background"
        )
    
    # Erstelle angepasste Palette und speichere automatisch
    custom_palette = {
        "primary": custom_primary,
        "secondary": custom_secondary,
        "accent": custom_accent,
        "background": custom_background
    }
    
    # Speichere angepasste Palette automatisch im Session State
    st.session_state["custom_palette"] = custom_palette
    st.session_state["use_custom_palette"] = True

# Zeige alle verfügbaren Paletten in einem Expander
with st.expander("🎨 Alle verfügbaren CI-Paletten anzeigen"):
    st.write("**Übersicht aller 15 CI-Farbpaletten:**")
    
    # Erstelle eine Grid-Darstellung der Paletten
    cols = st.columns(3)
    for i, palette in enumerate(CI_PALETTES):
        col_idx = i % 3
        with cols[col_idx]:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin-bottom: 10px; background: white;">
                <div style="font-weight: bold; margin-bottom: 8px;">{palette_names[i]}</div>
                <div style="display: flex; flex-direction: column; gap: 4px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="width: 20px; height: 15px; background-color: {palette['primary']}; border-radius: 3px; border: 1px solid #ccc;"></div>
                        <span style="font-size: 11px;">{palette['primary']}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="width: 20px; height: 15px; background-color: {palette['secondary']}; border-radius: 3px; border: 1px solid #ccc;"></div>
                        <span style="font-size: 11px;">{palette['secondary']}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="width: 20px; height: 15px; background-color: {palette['accent']}; border-radius: 3px; border: 1px solid #ccc;"></div>
                        <span style="font-size: 11px;">{palette['accent']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.divider()

with st.form("text_inputs"):
    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("Standort", key="location", value=st.session_state.get("location", ""))
        headline = st.text_input("Headline (Single)", key="headline", value=st.session_state.get("headline", ""))
        subline = st.text_input("Subline", key="subline", value=st.session_state.get("subline", ""))
        benefit_1 = st.text_input("Benefit 1", key="benefit_1", value=st.session_state.get("benefit_1", ""))
        stellentitel = st.text_input("Stellentitel", key="stellentitel", value=st.session_state.get("stellentitel", ""))
    with col2:
        headline_1 = st.text_input("Headline 1 (Dual)", key="headline_1", value=st.session_state.get("headline_1", ""))
        headline_2 = st.text_input("Headline 2 (Dual)", key="headline_2", value=st.session_state.get("headline_2", ""))
        benefit_2 = st.text_input("Benefit 2", key="benefit_2", value=st.session_state.get("benefit_2", ""))
        benefit_3 = st.text_input("Benefit 3", key="benefit_3", value=st.session_state.get("benefit_3", ""))
        cta = st.text_input("CTA", key="cta", value=st.session_state.get("cta", ""))

    generate = st.form_submit_button("Prompt generieren")

if generate:
    # Randomisierte Wahl der nicht-textlichen Parameter
    layout_id = choose(ALL_LAYOUTS)
    enforce_full_bg = layout_id in FULL_BG_LAYOUTS

    fixed_choices = {
        "layout_id": layout_id,
        "layout_style": choose(LAYOUT_STYLE),
        "container_shape": choose(CONTAINER_SHAPE),
        "border_style": choose(BORDER_STYLE),
        "texture_style": choose(TEXTURE_STYLE),
        "background_treatment": choose(BACKGROUND_TREATMENT),
        "corner_radius": choose(CORNER_RADIUS),
        "accent_elements": choose(ACCENT_ELEMENTS),
        "typography_style": choose(TYPOGRAPHY_STYLE),
        "photo_treatment": choose(PHOTO_TREATMENT),
        "depth_style": choose(DEPTH_STYLE),
        "motiv_quality": choose(MOTIV_QUALITY),
        "motiv_style": choose(MOTIV_STYLE),
        "lighting_type": choose(LIGHTING_TYPE),
        "framing": choose(FRAMING),
    }

    if enforce_full_bg:
        sliders = {
            "image_text_ratio": 100,  # festgenagelt auf 100 % (Vollbild)
            "container_transparency": rand_int(10, 90),
            "element_spacing": rand_int(12, 56),
            "container_padding": rand_int(16, 40),
            "shadow_intensity": rand_int(0, 70),
            "grain_amount": rand_int(0, 25),
            "tint_strength": rand_int(0, 20),
            "glow_intensity": rand_int(0, 30),
            "elevation_level": rand_int(0, 3),
        }
    else:
        sliders = {
            "image_text_ratio": rand_int(55, 85),
            "container_transparency": rand_int(10, 90),
            "element_spacing": rand_int(12, 56),
            "container_padding": rand_int(16, 40),
            "shadow_intensity": rand_int(0, 70),
            "grain_amount": rand_int(0, 25),
            "tint_strength": rand_int(0, 20),
            "glow_intensity": rand_int(0, 30),
            "elevation_level": rand_int(0, 3),
        }

    # ALTEN Workflow (Roh-Block) erzeugen → dient als spec_raw für den neuen Workflow
    payload = {
        "location": location,
        "headline": headline,
        "headline_1": headline_1,
        "headline_2": headline_2,
        "subline": subline,
        "benefit_1": benefit_1,
        "benefit_2": benefit_2,
        "benefit_3": benefit_3,
        "stellentitel": stellentitel,
        "cta": cta,
    }
    # Bestimme die zu verwendende CI-Palette
    if st.session_state.get("use_custom_palette", False):
        # Angepasste Palette
        chosen_ci = st.session_state.get("custom_palette", CI_PALETTES[0])
        palette_name = "🎨 Angepasste Palette"
    elif st.session_state.get("use_random_palette", False):
        # Zufällige Palette
        chosen_ci = choose(CI_PALETTES)
        palette_name = "🎲 Zufällig gewählt"
    else:
        # Manuell ausgewählte Palette
        selected_palette_idx = st.session_state.get("selected_palette_idx", 0)
        chosen_ci = CI_PALETTES[selected_palette_idx]
        palette_name = palette_names[selected_palette_idx]
    
    # Zeige Info über verwendete CI-Palette
    st.info(f"🎨 **Verwendete CI-Palette:** {palette_name} - Primary: {chosen_ci['primary']}, Accent: {chosen_ci['accent']}")
    
    chatgpt_raw_block = build_chatgpt_prompt(payload, fixed_choices, sliders, enforce_full_bg, ci=chosen_ci)
    with st.expander("Roh-Block (alt) – Input für neuen Workflow"):
        st.code(chatgpt_raw_block, language="text")

    # Neuen Workflow ausführen (Parsing des Roh-Blocks) und formatiert anzeigen
    app = build_app()
    result = app({"spec_raw": chatgpt_raw_block})
    st.success("Prompt generiert (neuer Workflow).")

    # Nur den Prompt des zweiten Workflows anzeigen, mit Abschlussbefehl
    raw_prompt = result.get("dalle_prompt") or ""
    final_prompt = raw_prompt + ("\n\nBitte jetzt das Bild generieren." if raw_prompt else "")
    st.code(final_prompt, language="text")

    # Icon-Only Copy-Button wie im Screenshot (Clipboard)
    copy_js = json.dumps(final_prompt)
    html(
        f"""
        <div style='display:flex;justify-content:flex-end;margin-top:-8px;margin-bottom:8px;'>
          <button id='copy-btn' title='Prompt kopieren' style='background:transparent;border:none;cursor:pointer;font-size:18px;'>📋</button>
        </div>
        <script>
        const COPY_TEXT = {copy_js};
        const btn = document.getElementById('copy-btn');
        btn.addEventListener('click', async () => {{
          try {{
            await navigator.clipboard.writeText(COPY_TEXT);
            const old = btn.textContent;
            btn.textContent = '✅';
            setTimeout(() => btn.textContent = old, 900);
          }} catch (e) {{
            btn.textContent = '⚠️';
          }}
        }});
        </script>
        """,
        height=40,
    )

st.caption("Hinweis: Nicht‑textliche Parameter werden bei jeder Generierung zufaellig bestimmt. Vollbild‑Layouts behalten 100% Bild bei.")