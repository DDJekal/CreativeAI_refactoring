"""
UI-Hilfsfunktionen
Utility functions for UI components and data handling
"""

import streamlit as st
import json
from typing import Dict, Any, List
from pathlib import Path

def apply_custom_css():
    """Applies custom CSS styling"""
    
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .color-preview {
            width: 50px;
            height: 20px;
            border-radius: 5px;
            display: inline-block;
            margin: 5px;
            border: 1px solid #ddd;
        }
        .layout-preview {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #e9ecef;
            margin: 0.5rem 0;
        }
        .slider-container {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        .result-box {
            background: #e8f4fd;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #1e40af;
            margin: 1rem 0;
        }
        .component-box {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #e9ecef;
            margin: 1rem 0;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-success {
            background-color: #10b981;
        }
        .status-error {
            background-color: #ef4444;
        }
        .status-warning {
            background-color: #f59e0b;
        }
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #e9ecef;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

def create_header(title: str, subtitle: str = ""):
    """Creates a styled header"""
    
    st.markdown(f"""
    <div class="main-header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title: str, value: str, status: str = "success"):
    """Creates a metric card"""
    
    status_class = f"status-{status}"
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="status-indicator {status_class}"></div>
        <h3>{title}</h3>
        <p>{value}</p>
    </div>
    """, unsafe_allow_html=True)

def create_status_indicator(status: str, text: str):
    """Creates a status indicator"""
    
    status_class = f"status-{status}"
    
    st.markdown(f"""
    <div>
        <span class="status-indicator {status_class}"></span>
        <span>{text}</span>
    </div>
    """, unsafe_allow_html=True)

def create_component_box(title: str, content: str):
    """Creates a component box"""
    
    st.markdown(f"""
    <div class="component-box">
        <h4>{title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

def create_result_box(title: str, content: str):
    """Creates a result box"""
    
    st.markdown(f"""
    <div class="result-box">
        <h4>{title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

def display_json_data(data: Dict[str, Any], title: str = "Daten"):
    """Displays JSON data in a formatted way"""
    
    st.subheader(title)
    st.json(data)

def display_text_data(data: Dict[str, Any], title: str = "Text-Daten"):
    """Displays text data in a formatted way"""
    
    st.subheader(title)
    
    for key, value in data.items():
        if isinstance(value, list):
            st.write(f"**{key.replace('_', ' ').title()}:**")
            for item in value:
                st.write(f"- {item}")
        else:
            st.write(f"**{key.replace('_', ' ').title()}:** {value}")

def create_color_preview(color: str, size: str = "50px"):
    """Creates a color preview"""
    
    st.markdown(f"""
    <div style="width: {size}; height: {size}; background-color: {color}; border-radius: 5px; margin: 5px; border: 1px solid #ddd;"></div>
    """, unsafe_allow_html=True)

def create_style_preview(colors: Dict[str, str], title: str = "Style-Vorschau"):
    """Creates a style preview"""
    
    st.subheader(title)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write("**Primärfarbe**")
        create_color_preview(colors.get('primary', '#005EA5'))
    
    with col2:
        st.write("**Sekundärfarbe**")
        create_color_preview(colors.get('secondary', '#B4D9F7'))
    
    with col3:
        st.write("**Akzentfarbe**")
        create_color_preview(colors.get('accent', '#FFC20E'))
    
    with col4:
        st.write("**Hintergrundfarbe**")
        create_color_preview(colors.get('background', '#FFFFFF'))

def create_layout_preview(layout_data: Dict[str, Any]):
    """Creates a layout preview"""
    
    st.subheader("📐 Layout-Vorschau")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write(f"**Typ:** {layout_data.get('layout_type', 'N/A')}")
        st.write(f"**Canvas:** {layout_data.get('canvas', {}).get('width', 'N/A')}x{layout_data.get('canvas', {}).get('height', 'N/A')}")
    
    with col2:
        st.write(f"**Zonen:** {len(layout_data.get('zones', {}))}")
        st.write(f"**Validierung:** {'✅' if layout_data.get('__validated__') else '❌'}")
    
    with col3:
        st.write(f"**Layout-ID:** {layout_data.get('layout_id', 'N/A')}")
        st.write(f"**Name:** {layout_data.get('name', 'N/A')}")

def create_slider_description(value: float, min_val: float, max_val: float, descriptions: List[str]):
    """Creates a semantic description for slider values"""
    
    # Normalisiere den Wert zwischen 0 und 1
    normalized = (value - min_val) / (max_val - min_val)
    
    # Bestimme die Beschreibung basierend auf dem normalisierten Wert
    if normalized <= 0.2:
        return descriptions[0]
    elif normalized <= 0.4:
        return descriptions[1]
    elif normalized <= 0.6:
        return descriptions[2]
    elif normalized <= 0.8:
        return descriptions[3]
    else:
        return descriptions[4]

def create_progress_bar(current: int, total: int, label: str = "Fortschritt"):
    """Creates a progress bar"""
    
    progress = current / total
    st.progress(progress)
    st.write(f"{label}: {current}/{total} ({progress:.1%})")

def create_error_message(error: str, details: str = ""):
    """Creates an error message"""
    
    st.error(f"❌ {error}")
    if details:
        st.write(f"**Details:** {details}")

def create_success_message(message: str, details: str = ""):
    """Creates a success message"""
    
    st.success(f"✅ {message}")
    if details:
        st.write(f"**Details:** {details}")

def create_warning_message(message: str, details: str = ""):
    """Creates a warning message"""
    
    st.warning(f"⚠️ {message}")
    if details:
        st.write(f"**Details:** {details}")

def create_info_message(message: str, details: str = ""):
    """Creates an info message"""
    
    st.info(f"ℹ️ {message}")
    if details:
        st.write(f"**Details:** {details}")

def create_footer():
    """Creates a footer"""
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🎨 CreativeAI - Modulares Frontend | Version 1.0</p>
        <p>Teste die neue modulare Pipeline mit Layout-Engine + Style-Resolver</p>
    </div>
    """, unsafe_allow_html=True)

def save_data_to_file(data: Dict[str, Any], filename: str):
    """Saves data to a JSON file"""
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Fehler beim Speichern: {e}")
        return False

def load_data_from_file(filename: str) -> Dict[str, Any]:
    """Loads data from a JSON file"""
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Fehler beim Laden: {e}")
        return {}

def validate_input_data(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
    """Validates input data and returns list of missing fields"""
    
    missing_fields = []
    
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
    
    return missing_fields

def create_validation_summary(data: Dict[str, Any], required_fields: List[str]):
    """Creates a validation summary"""
    
    missing_fields = validate_input_data(data, required_fields)
    
    if missing_fields:
        st.warning(f"⚠️ Fehlende Felder: {', '.join(missing_fields)}")
        return False
    else:
        st.success("✅ Alle erforderlichen Felder ausgefüllt!")
        return True
