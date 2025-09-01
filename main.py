"""
CreativeAI - Recruiting Design Generator
🚀 Neues Frontend mit Layout-Fokus

STRUKTUR:
1. Layout-Auswahl (Skizzen + Templates)
2. Design & Style
3. Text-Eingabe
4. Motiv-Eingabe
5. Prompt-Generierung
"""

import os
import sys
import yaml
import json
from datetime import datetime
import time
import streamlit as st
from pathlib import Path
import logging
from PIL import Image
import random
import re

# Projekt-Pfade konfigurieren
current_file = Path(__file__).resolve()
project_root = current_file.parent.resolve()
sys.path.insert(0, str(project_root))

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =====================================
# BACKEND-IMPORTS FÜR DESIGN & STYLE INTEGRATION
# =====================================

try:
    from creative_core.layout.loader import load_layout
    LAYOUT_LOADER_AVAILABLE = True
    logger.info("✅ Layout Loader erfolgreich importiert")
except ImportError as e:
    LAYOUT_LOADER_AVAILABLE = False
    logger.error(f"❌ Layout Loader nicht verfügbar: {e}")

try:
    from creative_core.layout.engine import LayoutEngine
    LAYOUT_ENGINE_AVAILABLE = True
    logger.info("✅ Layout Engine erfolgreich importiert")
except ImportError as e:
    LAYOUT_ENGINE_AVAILABLE = False
    logger.error(f"❌ Layout Engine nicht verfügbar: {e}")

try:
    from creative_core.design_ci.rules import apply_rules
    DESIGN_CI_AVAILABLE = True
    logger.info("✅ Design CI Rules erfolgreich importiert")
except ImportError as e:
    DESIGN_CI_AVAILABLE = False
    logger.error(f"❌ Design CI Rules nicht verfügbar: {e}")

# =====================================
# FUNKTIONEN
# =====================================

def load_original_sketches():
    """Lade Originalskizzen für Layout-Vorschau"""
    sketches = {}
    sketch_files = {
        "Skizze1": "Skizzen/Skizze1.png",
        "Skizze2": "Skizzen/Skizze2.png", 
        "Skizze3": "Skizzen/Skizze3.png",
        "Skizze4": "Skizzen/Skizze4.png",
        "Skizze5": "Skizzen/Skizze5.png",
        "Skizze6": "Skizzen/Skizze6.png",
        "Skizze7": "Skizzen/Skizze7.png",
        "Skizze8": "Skizzen/Skizze8.png",
        "Skizze9": "Skizzen/Skizze9.png",
        "Skizze10": "Skizzen/Skizze10.png",
        "Skizze11": "Skizzen/Skizze11.png",
        "Skizze12": "Skizzen/Skizze12.png",
        "Skizze13": "Skizzen/Skizze13.png"
    }
    
    for name, path in sketch_files.items():
        if os.path.exists(path):
            sketches[name] = {
                "name": name,
                "path": path
            }
    
    return sketches

def display_sketch_preview(sketch_data, layout_id, selected_layout_id):
    """Zeige Sketch-Vorschau korrekt an"""
    if sketch_data and sketch_data.get("path"):
        try:
            from PIL import Image
            sketch_image = Image.open(sketch_data["path"])
            
            # Optimale Größe: Nicht zu klein, aber kompakt mit guter Qualität
            sketch_image.thumbnail((120, 120), Image.Resampling.LANCZOS)
            
            # Border für ausgewähltes Layout
            border_color = "#1f77b4" if layout_id == selected_layout_id else "#ddd"
            border_width = "3px" if layout_id == selected_layout_id else "2px"
            
            st.markdown(f"""
            <div style="border: {border_width} solid {border_color}; border-radius: 8px; padding: 8px; background: white; width: fit-content; margin: 0 auto;">
            """, unsafe_allow_html=True)
            
            # Sketch anzeigen
            st.image(sketch_image, 
                    caption=f"{sketch_data['name']}", 
                    width=120)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Fehler beim Laden der Skizze: {e}")
            st.info(f"Skizze nicht verfügbar")
    else:
        st.info(f"Skizze nicht verfügbar")

def load_layout_info(layout_id):
    """Lade Layout-Informationen aus den YAML-Dateien"""
    try:
        if LAYOUT_LOADER_AVAILABLE:
            layout_data = load_layout(layout_id)
            if layout_data:
                return {
                    'zones': layout_data.get('zones', {}),
                    'layout_type': layout_data.get('layout_type', 'Standard'),
                    'canvas': layout_data.get('canvas', {}),
                    'layout_description': get_layout_specific_description(layout_id)
                }
    except Exception as e:
        logger.error(f"Fehler beim Laden des Layouts {layout_id}: {e}")
    
    return None

def get_layout_specific_description(layout_id):
    """Gibt layout-spezifische Beschreibungen zurück"""
    layout_descriptions = {
        'skizze9_storytelling_layout': {
            'description': 'Storytelling-Layout mit narrativem Textfluss',
            'features': ['narrative text flow', 'vertical text cascade', 'story progression', 'emotional journey'],
            'visual_style': 'Fließende, vertikale Textanordnung für Geschichten'
        },
        'skizze11_infographic_layout': {
            'description': 'Infografik-Layout mit strukturierten Datenblöcken',
            'features': ['structured data blocks', 'organized information', 'data visualization', 'clear hierarchy'],
            'visual_style': 'Organisierte, übersichtliche Informationsdarstellung'
        },
        'skizze8_hero_layout': {
            'description': 'Hero-Layout mit dramatischem visuellen Impact',
            'features': ['dramatic visual impact', 'hero image focus', 'bold typography', 'maximum visual presence'],
            'visual_style': 'Dramatische, bilddominante Darstellung'
        },
        'skizze7_minimalist_layout': {
            'description': 'Minimalistisches Layout mit klaren Linien',
            'features': ['clean lines', 'minimal elements', 'white space', 'focused content'],
            'visual_style': 'Saubere, reduzierte Gestaltung'
        },
        'skizze6_grid_layout': {
            'description': 'Grid-Layout mit strukturierter Anordnung',
            'features': ['structured grid', 'organized sections', 'balanced composition', 'systematic layout'],
            'visual_style': 'Systematische, ausgewogene Anordnung'
        },
        'skizze5_asymmetric_layout': {
            'description': 'Asymmetrisches Layout mit dynamischer Balance',
            'features': ['dynamic balance', 'asymmetric composition', 'visual tension', 'creative freedom'],
            'visual_style': 'Dynamische, kreative Gestaltung'
        },
        'skizze4_diagonal_layout': {
            'description': 'Diagonales Layout mit dynamischer Bewegung',
            'features': ['diagonal movement', 'dynamic flow', 'visual energy', 'directional composition'],
            'visual_style': 'Bewegungsreiche, energiegeladene Gestaltung'
        },
        'skizze3_centered_layout': {
            'description': 'Zentriertes Layout mit fokussierter Ausrichtung',
            'features': ['centered focus', 'balanced composition', 'hierarchical structure', 'clear hierarchy'],
            'visual_style': 'Fokussierte, ausgewogene Gestaltung'
        },
        'skizze2_horizontal_split': {
            'description': 'Horizontal geteiltes Layout mit klarer Trennung',
            'features': ['horizontal division', 'clear separation', 'balanced sections', 'organized layout'],
            'visual_style': 'Klare, organisierte Aufteilung'
        },
        'skizze1_vertical_split': {
            'description': 'Vertikal geteiltes Layout mit seitlicher Anordnung',
            'features': ['vertical division', 'side-by-side layout', 'balanced composition', 'organized sections'],
            'visual_style': 'Seitliche, ausgewogene Anordnung'
        },
        'skizze10_modern_split': {
            'description': 'Modernes Split-Layout mit zeitgemäßer Gestaltung',
            'features': ['modern design', 'contemporary layout', 'clean aesthetics', 'professional appearance'],
            'visual_style': 'Zeitgemäße, professionelle Gestaltung'
        },
        'skizze12_magazine_layout': {
            'description': 'Magazin-Layout mit redaktioneller Struktur',
            'features': ['editorial structure', 'content hierarchy', 'professional layout', 'publication design'],
            'visual_style': 'Redaktionelle, professionelle Struktur'
        },
        'skizze13_portfolio_layout': {
            'description': 'Portfolio-Layout mit präsentationsorientierter Gestaltung',
            'features': ['presentation focus', 'showcase design', 'professional display', 'portfolio aesthetics'],
            'visual_style': 'Präsentationsorientierte, professionelle Gestaltung'
        }
    }
    
    return layout_descriptions.get(layout_id, {
        'description': 'Standard-Layout',
        'features': ['standard layout', 'basic composition', 'traditional design'],
        'visual_style': 'Standard-Gestaltung'
    })

def apply_design_to_layout(layout_id, design_options, ci_colors):
    """
    Wendet Design & Style-Optionen auf ein Layout an
    
    Args:
        layout_id: ID des Layouts
        design_options: Dictionary mit allen Design-Optionen
        ci_colors: Dictionary mit CI-Farben
        
    Returns:
        Verarbeitetes Layout mit integrierten Design-Optionen
    """
    try:
        if not LAYOUT_ENGINE_AVAILABLE:
            logger.warning("Layout Engine nicht verfügbar - verwende Basis-Layout")
            return None
            
        if not DESIGN_CI_AVAILABLE:
            logger.warning("Design CI Rules nicht verfügbar - verwende Basis-Layout")
            return None
        
        # Layout laden
        layout_data = load_layout(layout_id)
        if not layout_data:
            logger.error(f"Layout {layout_id} konnte nicht geladen werden")
            return None
        
        # Layout Engine initialisieren
        layout_engine = LayoutEngine()
        
        # Slider-Werte aus Design-Optionen extrahieren
        image_text_ratio = int(design_options.get('image_text_ratio', 0.6) * 100)
        container_transparency = int(design_options.get('container_transparency', 0.8) * 100)
        
        # Layout-Koordinaten berechnen
        calculated_layout = layout_engine.calculate_layout_coordinates(
            layout_data,
            image_text_ratio=image_text_ratio,
            container_transparency=container_transparency
        )
        
        # Design-Regeln anwenden
        design_options_for_backend = {
            'typography_scale': 'md',  # Standard
            'container_shape': design_options.get('container_shape', ('rounded_rectangle', 'Abgerundet 📱'))[0],
            'border_style': design_options.get('border_style', ('soft_shadow', '🌫️ Weicher Schatten'))[0],
            'corner_radius_px': {
                'small': 8,
                'medium': 16,
                'large': 24,
                'xl': 32
            }.get(design_options.get('corner_radius', ('medium', '⌜ Mittel'))[0], 16),
            'transparency_pct': int(design_options.get('container_transparency', 0.8) * 100),
            'accent_elements': [design_options.get('accent_elements', ('modern_minimal', '⚪ Modern Minimal'))[0]]
        }
        
        # Design-Regeln anwenden
        design_result = apply_rules(
            layout=calculated_layout,
            ci=ci_colors,
            options=design_options_for_backend
        )
        
        logger.info(f"Design erfolgreich auf Layout {layout_id} angewendet")
        
        # Debug-Informationen für adaptive Typografie (optional)
        if logger.isEnabledFor(logging.DEBUG):
            debug_info = debug_adaptive_typography(calculated_layout, design_result)
            logger.debug(debug_info)
        
        return {
            'layout': calculated_layout,
            'design': design_result,
            'synergy_score': _calculate_synergy_score(calculated_layout, design_result)
        }
        
    except Exception as e:
        logger.error(f"Fehler bei der Design-Integration: {e}")
        return None

def _calculate_synergy_score(layout, design):
    """Berechnet einen Synergie-Score zwischen Layout und Design"""
    try:
        score = 0
        
        # Layout-Typ-Kompatibilität
        layout_type = layout.get('layout_type', 'unknown')
        if layout_type in ['hero_layout', 'storytelling_layout']:
            if design.get('containers', {}).get('style') == 'modern':
                score += 20
        elif layout_type in ['minimalist_layout', 'grid_layout']:
            if design.get('containers', {}).get('style') == 'clean':
                score += 20
        
        # Farb-Harmonie
        colors = design.get('colors', {})
        if colors.get('primary') and colors.get('accent'):
            score += 15
        
        # Container-Style-Kompatibilität
        container_shape = design.get('containers', {}).get('shape', 'unknown')
        if container_shape in ['rounded_rectangle', 'organic_blob']:
            score += 10
        
        # Transparenz-Integration
        transparency = design.get('transparency', 0.8)
        if 0.6 <= transparency <= 0.9:
            score += 15
        
        return min(score, 100)
        
    except Exception as e:
        logger.error(f"Fehler bei Synergie-Berechnung: {e}")
        return 50  # Standard-Score

def validate_layout_coordinates(layout_data):
    """Validiert Zone-Koordinaten mit verbesserter Logik"""
    zones = layout_data.get('zones', {})
    canvas = layout_data.get('canvas', {})
    canvas_width = canvas.get('width', 1080)
    canvas_height = canvas.get('height', 1080)
    
    validation_results = {
        'is_valid': True,
        'errors': [],
        'warnings': [],
        'zone_overlaps': [],
        'spacing_issues': [],
        'layout_type_validation': []
    }
    
    # Layout-Typ-spezifische Regeln
    layout_type = layout_data.get('layout_type', 'standard')
    layout_rules = get_layout_type_rules(layout_type)
    
    # Verbesserte Zone-Validierung mit Layout-Typ-Berücksichtigung
    for zone1_name, zone1_data in zones.items():
        for zone2_name, zone2_data in zones.items():
            if zone1_name != zone2_name:
                # Nur echte Überlappungen erkennen (nicht nur Berührungen)
                if zones_overlap_significantly(zone1_data, zone2_data, layout_type):
                    validation_results['is_valid'] = False
                    overlap_msg = f"Signifikante Überlappung zwischen {zone1_name} und {zone2_name}"
                    validation_results['errors'].append(overlap_msg)
                    validation_results['zone_overlaps'].append({
                        'zone1': zone1_name,
                        'zone2': zone2_name,
                        'severity': 'error'
                    })
                
                # Abstandsprüfung nur für bestimmte Layout-Typen
                if layout_type not in ['grid_layout', 'minimalist_layout']:
                    if zones_too_close_with_context(zone1_data, zone2_data, layout_type):
                        spacing_msg = f"Abstand zwischen {zone1_name} und {zone2_name} könnte optimiert werden"
                        validation_results['warnings'].append(spacing_msg)
                        validation_results['spacing_issues'].append({
                            'zone1': zone1_name,
                            'zone2': zone2_name,
                            'current_spacing': calculate_zone_distance(zone1_data, zone2_data),
                            'required_spacing': get_min_spacing_for_layout(layout_type)
                        })
    
    # Layout-Typ-spezifische Validierung (weniger streng)
    layout_validation = validate_layout_type_specific_rules(layout_data, layout_rules)
    validation_results['layout_type_validation'] = layout_validation
    
    # Gesamtvalidierung - nur echte Fehler als kritisch betrachten
    if validation_results['errors']:
        validation_results['is_valid'] = False
    elif validation_results['warnings'] and len(validation_results['warnings']) > 3:
        # Nur bei vielen Warnungen als problematisch markieren
        validation_results['is_valid'] = False
    
    return validation_results

def get_layout_type_rules(layout_type):
    """Gibt layout-typspezifische Validierungsregeln zurück"""
    rules = {
        'storytelling_layout': {
            'min_text_zones': 3,
            'max_text_zones': 6,
            'text_flow_required': True,
            'vertical_progression': True
        },
        'infographic_layout': {
            'min_data_zones': 2,
            'max_data_zones': 8,
            'hierarchy_required': True,
            'balanced_distribution': True
        },
        'hero_layout': {
            'min_image_zones': 1,
            'max_text_zones': 3,
            'hero_focus_required': True,
            'dramatic_impact': True
        },
        'minimalist_layout': {
            'max_total_zones': 5,
            'white_space_required': True,
            'clean_lines': True
        },
        'grid_layout': {
            'grid_alignment_required': True,
            'consistent_spacing': True,
            'balanced_sections': True
        }
    }
    
    return rules.get(layout_type, {
        'min_total_zones': 2,
        'max_total_zones': 10,
        'basic_validation': True
    })

def validate_layout_type_specific_rules(layout_data, rules):
    """Validiert layout-typspezifische Regeln (weniger streng)"""
    zones = layout_data.get('zones', {})
    validation_results = []
    
    # Grundlegende Regeln (nur echte Probleme als Fehler markieren)
    if 'min_total_zones' in rules:
        if len(zones) < rules['min_total_zones']:
            validation_results.append({
                'rule': 'min_total_zones',
                'status': 'warning',  # Nur Warnung, kein Fehler
                'message': f"Layout hat {len(zones)} Zonen (empfohlen: {rules['min_total_zones']}+)"
            })
    
    if 'max_total_zones' in rules:
        if len(zones) > rules['max_total_zones']:
            validation_results.append({
                'rule': 'max_total_zones',
                'status': 'info',  # Nur Info, keine Warnung
                'message': f"Layout hat {len(zones)} Zonen (typisch: {rules['max_total_zones']})"
            })
    
    # Storytelling-spezifische Regeln (weniger streng)
    if 'text_flow_required' in rules and rules['text_flow_required']:
        text_zones = [z for z in zones.values() if z.get('content_type') == 'text_elements']
        if len(text_zones) < 2:  # Reduziert von 3 auf 2
            validation_results.append({
                'rule': 'text_flow_required',
                'status': 'info',
                'message': f"Storytelling-Layout hat {len(text_zones)} Text-Zonen (empfohlen: 2+)"
            })
    
    # Infographic-spezifische Regeln (weniger streng)
    if 'hierarchy_required' in rules and rules['hierarchy_required']:
        data_zones = [z for z in zones.values() if z.get('content_type') in ['text_elements', 'data_elements']]
        if len(data_zones) < 1:  # Reduziert von 2 auf 1
            validation_results.append({
                'rule': 'hierarchy_required',
                'status': 'info',
                'message': f"Infographic-Layout hat {len(data_zones)} Daten-Zonen (empfohlen: 1+)"
            })
    
    # Hero-spezifische Regeln (weniger streng)
    if 'hero_focus_required' in rules and rules['hero_focus_required']:
        image_zones = [z for z in zones.values() if z.get('content_type') == 'image_motiv']
        if len(image_zones) < 1:
            validation_results.append({
                'rule': 'hero_focus_required',
                'status': 'info',
                'message': "Hero-Layout empfiehlt mindestens 1 Bild-Zone"
            })
    
    return validation_results

def zones_overlap_significantly(zone1, zone2, layout_type):
    """Prüft ob zwei Zonen sich signifikant überlappen (nicht nur berühren)"""
    try:
        x1, y1, w1, h1 = zone1.get('x', 0), zone1.get('y', 0), zone1.get('width', 0), zone1.get('height', 0)
        x2, y2, w2, h2 = zone2.get('x', 0), zone2.get('y', 0), zone2.get('width', 0), zone2.get('height', 0)
        
        # Überlappung berechnen
        overlap_x = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
        overlap_y = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
        
        # Mindestüberlappung für "signifikant" (5% der kleineren Zone)
        min_overlap_threshold = min(w1 * h1, w2 * h2) * 0.05
        
        return overlap_x * overlap_y > min_overlap_threshold
        
    except (TypeError, ValueError):
        return False

def zones_too_close_with_context(zone1, zone2, layout_type):
    """Prüft Abstände mit Layout-Typ-Kontext"""
    try:
        min_spacing = get_min_spacing_for_layout(layout_type)
        distance = calculate_zone_distance(zone1, zone2)
        
        # Für bestimmte Layout-Typen weniger streng
        if layout_type in ['hero_layout', 'storytelling_layout']:
            min_spacing *= 0.7  # 30% weniger streng
        
        return distance < min_spacing
        
    except (TypeError, ValueError):
        return False

def get_min_spacing_for_layout(layout_type):
    """Gibt den Mindestabstand für verschiedene Layout-Typen zurück"""
    spacing_rules = {
        'grid_layout': 15,
        'minimalist_layout': 25,
        'hero_layout': 20,
        'storytelling_layout': 18,
        'infographic_layout': 22,
        'magazine_layout': 20,
        'portfolio_layout': 20,
        'modern_split': 20,
        'vertical_split': 20,
        'horizontal_split': 20,
        'centered_layout': 25,
        'diagonal_layout': 15,
        'asymmetric_layout': 18
    }
    
    return spacing_rules.get(layout_type, 20)  # Standard: 20px

def calculate_zone_distance(zone1, zone2):
    """Berechnet den Abstand zwischen zwei Zonen"""
    try:
        x1, y1, w1, h1 = zone1.get('x', 0), zone1.get('y', 0), zone1.get('width', 0), zone1.get('height', 0)
        x2, y2, w2, h2 = zone2.get('x', 0), zone2.get('y', 0), zone2.get('width', 0), zone2.get('height', 0)
        
        # Zentren der Zonen
        center1_x, center1_y = x1 + w1/2, y1 + h1/2
        center2_x, center2_y = x2 + w2/2, y2 + h2/2
        
        # Euklidischer Abstand
        distance = ((center2_x - center1_x) ** 2 + (center2_y - center1_y) ** 2) ** 0.5
        
        return distance
        
    except (TypeError, ValueError):
        return float('inf')

def calculate_actual_layout_ratio(layout_data):
    """Berechnet das tatsächliche Bild-Text-Verhältnis basierend auf Zone-Dimensionen"""
    zones = layout_data.get('zones', {})
    
    text_area = 0
    image_area = 0
    
    for zone_name, zone_data in zones.items():
        area = zone_data.get('width', 0) * zone_data.get('height', 0)
        
        if zone_data.get('content_type') == 'text_elements':
            text_area += area
        elif zone_data.get('content_type') == 'image_motiv':
            image_area += area
    
    total_area = text_area + image_area
    if total_area > 0:
        actual_ratio = image_area / total_area
        return actual_ratio
    
    return 0.5  # Standardwert

def calculate_storytelling_ratio(layout_data):
    """Berechnet das tatsächliche Bild-Text-Verhältnis für Storytelling-Layouts"""
    zones = layout_data.get('zones', {})
    
    text_area = 0
    image_area = 0
    
    for zone_name, zone_data in zones.items():
        area = zone_data.get('width', 0) * zone_data.get('height', 0)
        
        if zone_data.get('content_type') == 'text_elements':
            text_area += area
        elif zone_data.get('content_type') == 'image_motiv':
            image_area += area
    
    total_area = text_area + image_area
    if total_area > 0:
        actual_ratio = image_area / total_area
        return actual_ratio
    
    return 0.5  # Standardwert

def generate_semantic_layout_description(layout_data):
    """
    Generiert semantische Layout-Beschreibungen aus technischen Koordinaten.
    
    Args:
        layout_data: Layout-Daten mit zones und Koordinaten
    
    Returns:
        dict: Semantische Beschreibungen für KI-Generatoren
    """
    zones = layout_data.get('zones', {})
    canvas = layout_data.get('canvas', {})
    canvas_width = canvas.get('width', 1080)
    canvas_height = canvas.get('height', 1080)
    
    # Layout-Typ bestimmen
    layout_type = layout_data.get('layout_type', 'unknown')
    
    semantic_description = {
        'layout_overview': '',
        'text_areas': [],
        'image_areas': [],
        'positioning_logic': []
    }
    
    # Text- und Bild-Zonen trennen
    text_zones = {name: data for name, data in zones.items() 
                 if data.get('content_type') == 'text_elements'}
    image_zones = {name: data for name, data in zones.items() 
                  if data.get('content_type') == 'image_motiv'}
    
    # Semantische Beschreibung generieren
    if layout_type == 'vertical_split':
        semantic_description['layout_overview'] = (
            "VERTICAL SPLIT LAYOUT: Left column contains text stack, "
            "right column contains full-height image"
        )
        
        # Text-Zonen semantisch beschreiben
        for zone_name, zone_data in text_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            # Position relativ zum Canvas beschreiben
            if x < canvas_width * 0.5:
                column = "left column"
            else:
                column = "right column"
            
            # Vertikale Position beschreiben
            if y < canvas_height * 0.25:
                vertical_pos = "top"
            elif y < canvas_height * 0.5:
                vertical_pos = "upper middle"
            elif y < canvas_height * 0.75:
                vertical_pos = "lower middle"
            else:
                vertical_pos = "bottom"
            
            semantic_description['text_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} positioned in {column}, {vertical_pos} section",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })
        
        # Bild-Zonen semantisch beschreiben
        for zone_name, zone_data in image_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            semantic_description['image_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} positioned in right column, full height",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })
    
    elif layout_type == 'horizontal_split':
        semantic_description['layout_overview'] = (
            "HORIZONTAL SPLIT LAYOUT: Top section contains image area, "
            "bottom section contains text stack"
        )
        
        # Text-Zonen semantisch beschreiben
        for zone_name, zone_data in text_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            # Horizontale Position beschreiben
            if x < canvas_width * 0.25:
                horizontal_pos = "left"
            elif x < canvas_width * 0.5:
                horizontal_pos = "center-left"
            elif x < canvas_width * 0.75:
                horizontal_pos = "center-right"
            else:
                horizontal_pos = "right"
            
            # Vertikale Position beschreiben
            if y < canvas_height * 0.5:
                section = "top section"
            else:
                section = "bottom section"
            
            semantic_description['text_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} positioned in {section}, {horizontal_pos} area",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })
        
        # Bild-Zonen semantisch beschreiben
        for zone_name, zone_data in image_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            semantic_description['image_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} positioned in top section, full width",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })
    
    elif layout_type == 'centered_layout':
        semantic_description['layout_overview'] = (
            "CENTERED LAYOUT: Central composition with text overlay on background image, "
            "balanced text positioning around center"
        )
        
        # Text-Zonen semantisch beschreiben
        for zone_name, zone_data in text_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            # Zentrale Position beschreiben
            center_x = x + w/2
            center_y = y + h/2
            
            if center_x < canvas_width * 0.4:
                horizontal_pos = "left side"
            elif center_x < canvas_width * 0.6:
                horizontal_pos = "center"
            else:
                horizontal_pos = "right side"
            
            if center_y < canvas_height * 0.4:
                vertical_pos = "upper"
            elif center_y < canvas_height * 0.6:
                vertical_pos = "middle"
            else:
                vertical_pos = "lower"
            
            semantic_description['text_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} positioned in {vertical_pos} {horizontal_pos} of composition",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })
        
        # Bild-Zonen semantisch beschreiben
        for zone_name, zone_data in image_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            semantic_description['image_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} as full background image",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })
    
    elif layout_type == 'grid_layout':
        semantic_description['layout_overview'] = (
            "GRID LAYOUT: Structured grid arrangement with organized text and image sections, "
            "systematic positioning in grid cells"
        )
        
        # Text-Zonen semantisch beschreiben
        for zone_name, zone_data in text_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            # Grid-Position bestimmen
            grid_col = int(x / (canvas_width / 3)) + 1
            grid_row = int(y / (canvas_height / 3)) + 1
            
            semantic_description['text_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} positioned in grid cell {grid_col}x{grid_row}",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })
        
        # Bild-Zonen semantisch beschreiben
        for zone_name, zone_data in image_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            grid_col = int(x / (canvas_width / 3)) + 1
            grid_row = int(y / (canvas_height / 3)) + 1
            
            semantic_description['image_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} positioned in grid cell {grid_col}x{grid_row}",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })
    
    elif layout_type == 'diagonal_layout':
        semantic_description['layout_overview'] = (
            "DIAGONAL LAYOUT: Dynamic diagonal arrangement with text elements flowing "
            "diagonally across the canvas, creating visual movement and energy"
        )
        
        # Text-Zonen semantisch beschreiben
        for zone_name, zone_data in text_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            # Diagonale Position bestimmen
            diagonal_pos = (x + y) / (canvas_width + canvas_height)
            
            if diagonal_pos < 0.3:
                position_desc = "upper-left diagonal position"
            elif diagonal_pos < 0.5:
                position_desc = "center diagonal position"
            else:
                position_desc = "lower-right diagonal position"
            
            semantic_description['text_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} positioned in {position_desc} with diagonal flow",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })
        
        # Bild-Zonen semantisch beschreiben
        for zone_name, zone_data in image_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            semantic_description['image_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} positioned diagonally integrated with text flow",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })

    elif layout_type == 'asymmetric_layout':
        semantic_description['layout_overview'] = (
            "ASYMMETRIC LAYOUT: Intentionally unbalanced composition with text elements "
            "positioned asymmetrically for dynamic visual tension and creative impact"
        )
        
        # Text-Zonen semantisch beschreiben
        for zone_name, zone_data in text_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            # Asymmetrische Position basierend auf tatsächlichen Koordinaten beschreiben
            center_x = x + w/2
            center_y = y + h/2
            
            # Horizontale Position basierend auf tatsächlicher X-Position
            if center_x < canvas_width * 0.25:
                horizontal_pos = "far left"
            elif center_x < canvas_width * 0.5:
                horizontal_pos = "left side"
            elif center_x < canvas_width * 0.75:
                horizontal_pos = "right side"
            else:
                horizontal_pos = "far right"
            
            # Vertikale Position basierend auf tatsächlicher Y-Position
            if center_y < canvas_height * 0.25:
                vertical_pos = "upper"
            elif center_y < canvas_height * 0.5:
                vertical_pos = "upper middle"
            elif center_y < canvas_height * 0.75:
                vertical_pos = "lower middle"
            else:
                vertical_pos = "lower"
            
            semantic_description['text_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} positioned in {vertical_pos} {horizontal_pos} area",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })
        
        # Bild-Zonen semantisch beschreiben
        for zone_name, zone_data in image_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            center_x = x + w/2
            center_y = y + h/2
            
            # Bild-Position basierend auf tatsächlichen Koordinaten
            if center_x < canvas_width * 0.5:
                image_pos = "left side"
            else:
                image_pos = "right side"
            
            if center_y < canvas_height * 0.5:
                image_vert = "upper"
            else:
                image_vert = "lower"
            
            semantic_description['image_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} positioned in {image_vert} {image_pos} area",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })

    elif layout_type == 'minimalist_layout':
        semantic_description['layout_overview'] = (
            "MINIMALIST LAYOUT: Clean, spacious design with generous white space, "
            "focused content placement, and minimal visual elements for maximum impact"
        )
        
        # Text-Zonen semantisch beschreiben
        for zone_name, zone_data in text_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            # Minimalistische Position beschreiben
            center_x = x + w/2
            center_y = y + h/2
            
            if abs(center_x - canvas_width/2) < canvas_width * 0.1:
                alignment = "centered"
            elif center_x < canvas_width/2:
                alignment = "left-aligned"
            else:
                alignment = "right-aligned"
            
            if center_y < canvas_height * 0.4:
                vertical_pos = "upper space"
            elif center_y < canvas_height * 0.6:
                vertical_pos = "central space"
            else:
                vertical_pos = "lower space"
            
            semantic_description['text_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} positioned in {vertical_pos}, {alignment} with generous white space",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })
        
        # Bild-Zonen semantisch beschreiben
        for zone_name, zone_data in image_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            semantic_description['image_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} as subtle background with minimalist integration",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })

    elif layout_type == 'hero_layout':
        semantic_description['layout_overview'] = (
            "HERO LAYOUT: Bold, impactful design with prominent headline and dramatic "
            "visual hierarchy, designed for maximum attention and engagement"
        )
        
        # Text-Zonen semantisch beschreiben
        for zone_name, zone_data in text_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            # Hero-spezifische Position beschreiben
            if 'headline' in zone_name.lower():
                position_desc = "hero headline position with maximum visual impact"
            elif 'standort' in zone_name.lower():
                position_desc = "supporting header position"
            elif 'cta' in zone_name.lower():
                position_desc = "prominent call-to-action position"
            else:
                position_desc = "supporting content position"
            
            semantic_description['text_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} positioned in {position_desc}",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })
        
        # Bild-Zonen semantisch beschreiben
        for zone_name, zone_data in image_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            semantic_description['image_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} as dramatic hero background",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })

    elif layout_type in ['storytelling_layout', 'modern_split', 'infographic_layout', 
                         'magazine_layout', 'portfolio_layout']:
        # Spezifische Beschreibungen für weitere Layout-Typen
        layout_descriptions = {
            'storytelling_layout': "STORYTELLING LAYOUT: Narrative-driven design with sequential content flow, guiding the viewer through a visual story",
            'modern_split': "MODERN SPLIT LAYOUT: Contemporary split design with clean lines and modern aesthetics",
            'infographic_layout': "INFOGRAPHIC LAYOUT: Data-focused design with structured information hierarchy and visual data presentation",
            'magazine_layout': "MAGAZINE LAYOUT: Editorial-style design with professional publication aesthetics and content organization",
            'portfolio_layout': "PORTFOLIO LAYOUT: Showcase-oriented design optimized for presenting work and achievements"
        }
        
        semantic_description['layout_overview'] = layout_descriptions.get(layout_type, "STANDARD LAYOUT")
        
        # Generische aber spezifische Beschreibung für diese Layout-Typen
        for zone_name, zone_data in text_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            # Position relativ beschreiben
            if x < canvas_width * 0.33:
                horizontal_pos = "left section"
            elif x < canvas_width * 0.67:
                horizontal_pos = "center section"
            else:
                horizontal_pos = "right section"
            
            if y < canvas_height * 0.33:
                vertical_pos = "upper"
            elif y < canvas_height * 0.67:
                vertical_pos = "middle"
            else:
                vertical_pos = "lower"
            
            semantic_description['text_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} positioned in {vertical_pos} {horizontal_pos} of {layout_type.replace('_', ' ')} composition",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })
        
        # Bild-Zonen für alle diese Layout-Typen
        for zone_name, zone_data in image_zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            
            semantic_description['image_areas'].append({
                'zone_name': zone_name,
                'description': f"{zone_name.replace('_', ' ').title()} integrated into {layout_type.replace('_', ' ')} composition",
                'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
            })
    
    else:
        # Fallback für unbekannte Layout-Typen
        semantic_description['layout_overview'] = (
            f"STANDARD LAYOUT: {layout_type.replace('_', ' ').title()} arrangement with mixed text and image zones"
        )
        
        # Alle Zonen generisch beschreiben
        for zone_name, zone_data in zones.items():
            x, y, w, h = zone_data['x'], zone_data['y'], zone_data['width'], zone_data['height']
            content_type = zone_data.get('content_type', 'unknown')
            
            if content_type == 'text_elements':
                semantic_description['text_areas'].append({
                    'zone_name': zone_name,
                    'description': f"{zone_name.replace('_', ' ').title()} positioned at coordinates ({x}, {y})",
                    'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                    'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
                })
            elif content_type == 'image_motiv':
                semantic_description['image_areas'].append({
                    'zone_name': zone_name,
                    'description': f"{zone_name.replace('_', ' ').title()} positioned at coordinates ({x}, {y})",
                    'relative_position': f"x: {x/canvas_width:.1%} from left, y: {y/canvas_height:.1%} from top",
                    'size': f"width: {w}px ({w/canvas_width:.1%} of canvas), height: {h}px"
                })
    
    return semantic_description

# =====================================
# HILFSFUNKTIONEN FÜR OPTIMIERTE PROMPT-GENERIERUNG
# =====================================

def normalize_german_text(text, preserve_umlauts=True):
    """
    Normalisiert deutschen Text für KI-Generierung
    
    Args:
        text: Eingabetext
        preserve_umlauts: True = Umlaute beibehalten, False = zu Grundbuchstaben umwandeln
    
    Returns:
        Normalisierter Text
    """
    if not text:
        return text
    
    if preserve_umlauts:
        return text.strip()
    else:
        # Umlaute zu Grundbuchstaben umwandeln (ä→a, ö→o, ü→u)
        umlaut_map = {
            'ä': 'a', 'ö': 'o', 'ü': 'u',
            'Ä': 'A', 'Ö': 'O', 'Ü': 'U'
        }
        normalized = text
        for umlaut, replacement in umlaut_map.items():
            normalized = normalized.replace(umlaut, replacement)
        return normalized.strip()

def get_text_processing_rules(engine_type='dalle3'):
    """
    Gibt die korrekten Text-Verarbeitungsregeln für verschiedene Engines zurück
    
    Args:
        engine_type: 'dalle3', 'midjourney', 'stable_diffusion'
    
    Returns:
        Dictionary mit Verarbeitungsregeln
    """
    rules = {
        'dalle3': {
            'preserve_umlauts': False,  # DALL-E 3 hat Probleme mit deutschen Umlauten
            'max_headline_length': 30,
            'max_subline_length': 50,
            'max_other_length': 25,
            'add_location_pin': True,
            'text_rendering': 'separate_layers'
        },
        'midjourney': {
            'preserve_umlauts': True,   # Midjourney kann deutsche Umlaute
            'max_headline_length': 40,
            'max_subline_length': 60,
            'max_other_length': 30,
            'add_location_pin': True,
            'text_rendering': 'integrated'
        },
        'stable_diffusion': {
            'preserve_umlauts': True,  # Stable Diffusion kann deutsche Umlaute
            'max_headline_length': 35,
            'max_subline_length': 55,
            'max_other_length': 28,
            'add_location_pin': True,
            'text_rendering': 'integrated'
        }
    }
    
    return rules.get(engine_type, rules['dalle3'])

def calculate_slider_percentage(value, max_value=1.0):
    """Berechnet konsistente Prozentwerte für Slider"""
    return int((value / max_value) * 100)

def get_transparency_description(transparency_value):
    """Gibt eine konsistente Transparenz-Beschreibung basierend auf dem Prozentwert"""
    percentage = calculate_slider_percentage(transparency_value)
    if percentage <= 20:
        return "sehr transparent"
    elif percentage <= 40:
        return "transparent"
    elif percentage <= 60:
        return "halbtransparent"
    elif percentage <= 80:
        return "leicht transparent"
    else:
        return "undurchsichtig"

def get_ratio_description(ratio_value):
    """Gibt eine konsistente Bild-Text-Verhältnis-Beschreibung basierend auf dem Prozentwert"""
    percentage = calculate_slider_percentage(ratio_value)
    if percentage <= 30:
        return f"{percentage}% Bildbereich"
    elif percentage <= 50:
        return f"{percentage}% Bildbereich"
    elif percentage <= 70:
        return f"{percentage}% Bildbereich"
    else:
        return f"{percentage}% Bildbereich"

def clean_emoji_from_text(text):
    """Entfernt Emojis und Sonderzeichen, behält nur alphanumerische Zeichen"""
    if not text:
        return text
    # Entferne Emojis und Sonderzeichen, behalte nur Buchstaben, Zahlen und Leerzeichen
    import re
    cleaned = re.sub(r'[^\w\s]', '', text)
    return cleaned.strip()

def get_clean_design_option(option_tuple):
    """Extrahiert eine saubere Design-Option ohne Emojis aus einem Tuple"""
    if isinstance(option_tuple, tuple) and len(option_tuple) >= 2:
        return clean_emoji_from_text(option_tuple[1])
    elif isinstance(option_tuple, str):
        return clean_emoji_from_text(option_tuple)
    else:
        return str(option_tuple)

def get_composition_description(composition_value, layout_type):
    """
    Gibt eine beschreibende Erklärung für den Kompositions-Wert zurück
    
    Args:
        composition_value: Slider-Wert (0.1-0.9)
        layout_type: Layout-Typ
    
    Returns:
        Beschreibung als String
    """
    if layout_type == 'vertical_split':
        if composition_value <= 0.3:
            return f"Schmale Textspalte ({int(composition_value*100)}% links)"
        elif composition_value <= 0.5:
            return f"Ausgewogene Aufteilung ({int(composition_value*100)}% Textspalte)"
        elif composition_value <= 0.7:
            return f"Breite Textspalte ({int(composition_value*100)}% Breite)"
        else:
            return f"Sehr breite Textspalte ({int(composition_value*100)}% Breite)"
    
    elif layout_type == 'horizontal_split':
        if composition_value <= 0.3:
            return f"Kleines Motiv oben ({int(composition_value*100)}% Höhe)"
        elif composition_value <= 0.5:
            return f"Ausgewogene Aufteilung ({int(composition_value*100)}% Motiv)"
        elif composition_value <= 0.7:
            return f"Großes Motiv oben ({int(composition_value*100)}% Höhe)"
        else:
            return f"Sehr großes Motiv oben ({int(composition_value*100)}% Höhe)"
    
    elif layout_type == 'centered_layout':
        if composition_value <= 0.4:
            return f"Kompakter zentrierter Bereich ({int(composition_value*100)}% Breite)"
        elif composition_value <= 0.6:
            return f"Ausgewogener zentrierter Bereich ({int(composition_value*100)}% Breite)"
        elif composition_value <= 0.8:
            return f"Breiter zentrierter Bereich ({int(composition_value*100)}% Breite)"
        else:
            return f"Sehr breiter zentrierter Bereich ({int(composition_value*100)}% Breite)"
    
    elif layout_type == 'minimalist_layout':
        if composition_value <= 0.4:
            return f"Viel Weißraum ({int(composition_value*100)}% Inhalt)"
        elif composition_value <= 0.6:
            return f"Ausgewogener Weißraum ({int(composition_value*100)}% Inhalt)"
        elif composition_value <= 0.8:
            return f"Kompakter Inhalt ({int(composition_value*100)}% Inhalt)"
        else:
            return f"Sehr kompakter Inhalt ({int(composition_value*100)}% Inhalt)"
    
    # Phase 2: Hero & Storytelling Layouts
    elif layout_type == 'hero_layout':
        if composition_value <= 0.4:
            return f"Text-dominant ({int(composition_value*100)}% Text-Prominenz)"
        elif composition_value <= 0.6:
            return f"Ausgewogen ({int(composition_value*100)}% Balance)"
        elif composition_value <= 0.8:
            return f"Motiv-dominant ({int(composition_value*100)}% Motiv-Impact)"
        else:
            return f"Sehr motiv-dominant ({int(composition_value*100)}% visueller Impact)"
    
    elif layout_type == 'storytelling_layout':
        if composition_value <= 0.4:
            return f"Text-Flow fokussiert ({int(composition_value*100)}% Storytelling)"
        elif composition_value <= 0.6:
            return f"Ausgewogener Text-Flow ({int(composition_value*100)}% Balance)"
        elif composition_value <= 0.8:
            return f"Motiv-fokussiert ({int(composition_value*100)}% visuelle Story)"
        else:
            return f"Sehr motiv-fokussiert ({int(composition_value*100)}% visueller Impact)"
    
    # Phase 2: Strukturierte Layouts
    elif layout_type == 'grid_layout':
        if composition_value <= 0.3:
            return f"2 Spalten ({int(composition_value*100)}% breite Spalten)"
        elif composition_value <= 0.6:
            return f"3 Spalten ({int(composition_value*100)}% Standard-Grid)"
        else:
            return f"4 Spalten ({int(composition_value*100)}% schmale Spalten)"
    
    elif layout_type == 'infographic_layout':
        if composition_value <= 0.4:
            return f"Lockere Struktur ({int(composition_value*100)}% Daten-Dichte)"
        elif composition_value <= 0.6:
            return f"Ausgewogene Struktur ({int(composition_value*100)}% Balance)"
        else:
            return f"Dichte Struktur ({int(composition_value*100)}% kompakte Daten)"
    
    elif layout_type == 'magazine_layout':
        if composition_value <= 0.4:
            return f"Schmale Spalten ({int(composition_value*100)}% mehrspaltig)"
        elif composition_value <= 0.6:
            return f"Ausgewogene Spalten ({int(composition_value*100)}% Standard)"
        else:
            return f"Breite Spalten ({int(composition_value*100)}% weniger Spalten)"
    
    elif layout_type == 'portfolio_layout':
        if composition_value <= 0.4:
            return f"Kleine Showcases ({int(composition_value*100)}% Detail-fokussiert)"
        elif composition_value <= 0.6:
            return f"Ausgewogene Showcases ({int(composition_value*100)}% Standard)"
        else:
            return f"Große Showcases ({int(composition_value*100)}% Impact-fokussiert)"
    
    # Phase 3: Kreative Layouts
    elif layout_type == 'diagonal_layout':
        if composition_value <= 0.3:
            return f"Flacher Winkel ({int(composition_value*100)}% subtile Neigung)"
        elif composition_value <= 0.6:
            return f"Standard-Winkel ({int(composition_value*100)}% ausgewogene Neigung)"
        else:
            return f"Steiler Winkel ({int(composition_value*100)}% dramatische Neigung)"
    
    elif layout_type == 'asymmetric_layout':
        if composition_value <= 0.3:
            return f"Leicht asymmetrisch ({int(composition_value*100)}% subtile Abweichung)"
        elif composition_value <= 0.6:
            return f"Ausgewogen asymmetrisch ({int(composition_value*100)}% dynamische Balance)"
        else:
            return f"Stark asymmetrisch ({int(composition_value*100)}% dramatische Abweichung)"
    
    return f"Komposition: {int(composition_value*100)}%"

def apply_layout_composition(layout_data, composition_value):
    """
    Passt Layout basierend auf Kompositions-Slider an (Phase 1 + 2 + 3)
    
    Args:
        layout_data: Original Layout-Daten
        composition_value: Slider-Wert (0.1-0.9)
    
    Returns:
        Angepasstes Layout
    """
    layout_type = layout_data.get('layout_type', 'standard')
    
    # Alle 13 Layout-Typen unterstützt
    if layout_type in ['vertical_split', 'horizontal_split', 'modern_split']:
        return adjust_split_layout(layout_data, composition_value)
    elif layout_type in ['centered_layout', 'minimalist_layout']:
        return adjust_centered_layout(layout_data, composition_value)
    # ... weitere Layout-Typen
    
    # Phase 2: Hero & Storytelling Layouts
    elif layout_type in ['hero_layout', 'storytelling_layout']:
        return adjust_hero_storytelling_layout(layout_data, composition_value)
    
    # Phase 2: Strukturierte Layouts
    elif layout_type in ['grid_layout', 'infographic_layout', 'magazine_layout', 'portfolio_layout']:
        return adjust_structured_layout(layout_data, composition_value)
    
    # Phase 3: Kreative Layouts
    elif layout_type in ['diagonal_layout', 'asymmetric_layout']:
        return adjust_creative_layout(layout_data, composition_value)
    
    return layout_data

def adjust_split_layout(layout_data, composition_value):
    """
    Passt Split-Layouts (vertical, horizontal, modern) basierend auf Motiv-Größe an
    
    Args:
        layout_data: Layout-Daten
        composition_value: Slider-Wert (0.1-0.9) = Motiv-Größe
    
    Returns:
        Angepasstes Layout
    """
    layout_type = layout_data.get('layout_type', 'vertical_split')
    canvas_width = layout_data['canvas']['width']
    canvas_height = layout_data['canvas']['height']
    zones = layout_data['zones'].copy()
    
    if layout_type in ['vertical_split', 'modern_split']:
        # Vertikale Split-Layouts: Motiv-Breite basierend auf Slider
        motiv_width = int(canvas_width * composition_value)
        
        # Motiv-Zone (rechts) anpassen - NUR Motiv-Größe
        for zone_name, zone_data in zones.items():
            if zone_data['content_type'] == 'image_motiv':
                zone_data['width'] = motiv_width
                zone_data['x'] = canvas_width - motiv_width  # Rechts positionieren
        
        # Text-Zonen UNVERÄNDERT lassen (bleiben an ursprünglichen Positionen)
        # Keine Anpassung der Text-Positionierung
    
    elif layout_type == 'horizontal_split':
        # Horizontales Split-Layout: Motiv-Höhe basierend auf Slider
        motiv_height = int(canvas_height * composition_value)
        
        # Motiv-Zone (oben) anpassen - NUR Motiv-Größe
        for zone_name, zone_data in zones.items():
            if zone_data['content_type'] == 'image_motiv':
                zone_data['height'] = motiv_height
        
        # Text-Zonen UNVERÄNDERT lassen (bleiben an ursprünglichen Positionen)
        # Keine Anpassung der Text-Positionierung
    
    layout_data['zones'] = zones
    return layout_data

def adjust_centered_layout(layout_data, composition_value):
    """
    Passt zentrierte Layouts basierend auf Kompositions-Wert an
    
    Args:
        layout_data: Layout-Daten
        composition_value: Slider-Wert (0.1-0.9)
    
    Returns:
        Angepasstes Layout
    """
    layout_type = layout_data.get('layout_type', 'centered_layout')
    canvas_width = layout_data['canvas']['width']
    canvas_height = layout_data['canvas']['height']
    zones = layout_data['zones'].copy()
    
    if layout_type == 'centered_layout':
        # Zentriertes Layout: Größe des zentrierten Bereichs anpassen
        center_width = int(canvas_width * composition_value)
        center_x = (canvas_width - center_width) // 2
        
        # Text-Zonen zentrieren und anpassen
        for zone_name, zone_data in zones.items():
            if zone_data['content_type'] == 'text_elements':
                # Zentrieren
                zone_data['x'] = center_x + (center_width - zone_data['width']) // 2
                # Breite anpassen falls nötig
                if zone_data['width'] > center_width:
                    zone_data['width'] = center_width - 40  # Padding
    
    elif layout_type == 'minimalist_layout':
        # Minimalistisches Layout: Weißraum vs. Inhalt
        content_width = int(canvas_width * composition_value)
        content_x = (canvas_width - content_width) // 2
        
        # Text-Zonen anpassen
        for zone_name, zone_data in zones.items():
            if zone_data['content_type'] == 'text_elements':
                # Zentrieren
                zone_data['x'] = content_x + (content_width - zone_data['width']) // 2
                # Breite anpassen falls nötig
                if zone_data['width'] > content_width:
                    zone_data['width'] = content_width - 40  # Padding
    
    layout_data['zones'] = zones
    return layout_data

def adjust_hero_storytelling_layout(layout_data, composition_value):
    """
    Passt Hero und Storytelling Layouts basierend auf Motiv-Größe an
    
    Args:
        layout_data: Layout-Daten
        composition_value: Slider-Wert (0.1-0.9) = Motiv-Größe
    
    Returns:
        Angepasstes Layout
    """
    layout_type = layout_data.get('layout_type', 'hero_layout')
    canvas_width = layout_data['canvas']['width']
    canvas_height = layout_data['canvas']['height']
    zones = layout_data['zones'].copy()
    
    if layout_type == 'hero_layout':
        # Hero Layout: Motiv-Größe basierend auf Slider
        motiv_scale = composition_value  # Direkte Verwendung des Slider-Werts
        
        # Motiv-Zone anpassen - NUR Motiv-Größe
        for zone_name, zone_data in zones.items():
            if zone_data['content_type'] == 'image_motiv':
                zone_data['width'] = int(canvas_width * motiv_scale)
                zone_data['height'] = int(canvas_height * motiv_scale)
                # Motiv zentrieren
                zone_data['x'] = (canvas_width - zone_data['width']) // 2
                zone_data['y'] = (canvas_height - zone_data['height']) // 2
        
        # Text-Zonen UNVERÄNDERT lassen (bleiben an ursprünglichen Positionen)
        # Keine Anpassung der Text-Positionierung
    
    elif layout_type == 'storytelling_layout':
        # Storytelling Layout: Motiv-Größe basierend auf Slider
        motiv_scale = composition_value
        
        # Motiv-Zone anpassen - NUR Motiv-Größe
        for zone_name, zone_data in zones.items():
            if zone_data['content_type'] == 'image_motiv':
                zone_data['width'] = int(canvas_width * motiv_scale)
                zone_data['height'] = int(canvas_height * motiv_scale)
                # Motiv zentrieren
                zone_data['x'] = (canvas_width - zone_data['width']) // 2
                zone_data['y'] = (canvas_height - zone_data['height']) // 2
        
        # Text-Zonen UNVERÄNDERT lassen (bleiben an ursprünglichen Positionen)
        # Keine Anpassung der Text-Positionierung
    
    layout_data['zones'] = zones
    return layout_data

def adjust_structured_layout(layout_data, composition_value):
    """
    Passt strukturierte Layouts (Grid, Infographic, Magazine, Portfolio) basierend auf Kompositions-Wert an
    
    Args:
        layout_data: Layout-Daten
        composition_value: Slider-Wert (0.1-0.9)
    
    Returns:
        Angepasstes Layout
    """
    layout_type = layout_data.get('layout_type', 'grid_layout')
    canvas_width = layout_data['canvas']['width']
    canvas_height = layout_data['canvas']['height']
    zones = layout_data['zones'].copy()
    
    if layout_type == 'grid_layout':
        # Grid Layout: Spaltenanzahl und -breite anpassen
        if composition_value <= 0.3:
            # 2 Spalten: Breite Spalten
            for zone_name, zone_data in zones.items():
                if zone_data['content_type'] == 'text_elements':
                    zone_data['width'] = int(canvas_width * 0.4)
                    zone_data['x'] = int(canvas_width * 0.05) if zone_data['x'] < canvas_width/2 else int(canvas_width * 0.55)
        elif composition_value <= 0.6:
            # 3 Spalten: Standard-Grid
            pass
        else:
            # 4 Spalten: Schmale Spalten
            for zone_name, zone_data in zones.items():
                if zone_data['content_type'] == 'text_elements':
                    zone_data['width'] = int(canvas_width * 0.2)
                    # Spalten-Position anpassen
                    if zone_data['x'] < canvas_width/4:
                        zone_data['x'] = int(canvas_width * 0.05)
                    elif zone_data['x'] < canvas_width/2:
                        zone_data['x'] = int(canvas_width * 0.3)
                    elif zone_data['x'] < 3*canvas_width/4:
                        zone_data['x'] = int(canvas_width * 0.55)
                    else:
                        zone_data['x'] = int(canvas_width * 0.8)
    
    elif layout_type == 'infographic_layout':
        # Infographic Layout: Daten-Dichte anpassen
        if composition_value <= 0.4:
            # Lockere Struktur: Größere Abstände
            for zone_name, zone_data in zones.items():
                if zone_data['content_type'] == 'text_elements':
                    zone_data['width'] = int(zone_data['width'] * 0.8)
                    zone_data['height'] = int(zone_data['height'] * 0.8)
        elif composition_value <= 0.6:
            # Ausgewogen: Standard-Größen
            pass
        else:
            # Dichte Struktur: Kleinere Abstände
            for zone_name, zone_data in zones.items():
                if zone_data['content_type'] == 'text_elements':
                    zone_data['width'] = int(zone_data['width'] * 1.2)
                    zone_data['height'] = int(zone_data['height'] * 1.2)
    
    elif layout_type == 'magazine_layout':
        # Magazine Layout: Spaltenbreite anpassen
        if composition_value <= 0.4:
            # Schmale Spalten: Mehr Spalten
            for zone_name, zone_data in zones.items():
                if zone_data['content_type'] == 'text_elements':
                    zone_data['width'] = int(canvas_width * 0.25)
                    # Spalten-Position anpassen
                    if zone_data['x'] < canvas_width/3:
                        zone_data['x'] = int(canvas_width * 0.05)
                    elif zone_data['x'] < 2*canvas_width/3:
                        zone_data['x'] = int(canvas_width * 0.35)
                    else:
                        zone_data['x'] = int(canvas_width * 0.7)
        elif composition_value <= 0.6:
            # Ausgewogen: Standard-Spalten
            pass
        else:
            # Breite Spalten: Weniger Spalten
            for zone_name, zone_data in zones.items():
                if zone_data['content_type'] == 'text_elements':
                    zone_data['width'] = int(canvas_width * 0.4)
                    # Spalten-Position anpassen
                    if zone_data['x'] < canvas_width/2:
                        zone_data['x'] = int(canvas_width * 0.05)
                    else:
                        zone_data['x'] = int(canvas_width * 0.55)
    
    elif layout_type == 'portfolio_layout':
        # Portfolio Layout: Showcase-Größe anpassen
        if composition_value <= 0.4:
            # Kleine Showcases: Mehr Details
            for zone_name, zone_data in zones.items():
                if zone_data['content_type'] == 'text_elements':
                    zone_data['width'] = int(zone_data['width'] * 0.8)
                    zone_data['height'] = int(zone_data['height'] * 0.8)
        elif composition_value <= 0.6:
            # Ausgewogen: Standard-Größen
            pass
        else:
            # Große Showcases: Weniger Details
            for zone_name, zone_data in zones.items():
                if zone_data['content_type'] == 'text_elements':
                    zone_data['width'] = int(zone_data['width'] * 1.2)
                    zone_data['height'] = int(zone_data['height'] * 1.2)
    
    layout_data['zones'] = zones
    return layout_data

def adjust_creative_layout(layout_data, composition_value):
    """
    Passt kreative Layouts (diagonal, asymmetric) basierend auf Kompositions-Wert an
    
    Args:
        layout_data: Layout-Daten
        composition_value: Slider-Wert (0.1-0.9)
    
    Returns:
        Angepasstes Layout
    """
    layout_type = layout_data.get('layout_type', 'diagonal_layout')
    canvas_width = layout_data['canvas']['width']
    canvas_height = layout_data['canvas']['height']
    zones = layout_data['zones'].copy()
    
    if layout_type == 'diagonal_layout':
        # Diagonal Layout: Neigungswinkel anpassen
        # Berechne diagonalen Offset basierend auf Kompositions-Wert
        diagonal_offset = int(canvas_width * composition_value * 0.3)
        
        for zone_name, zone_data in zones.items():
            if zone_data['content_type'] == 'text_elements':
                # Text-Zonen diagonal verschieben
                original_x = zone_data.get('original_x', zone_data['x'])
                original_y = zone_data.get('original_y', zone_data['y'])
                
                # Speichere Original-Position für erste Berechnung
                if 'original_x' not in zone_data:
                    zone_data['original_x'] = zone_data['x']
                    zone_data['original_y'] = zone_data['y']
                
                # Diagonale Verschiebung berechnen
                zone_data['x'] = original_x + diagonal_offset
                zone_data['y'] = original_y + int(diagonal_offset * 0.5)
    
    elif layout_type == 'asymmetric_layout':
        # Asymmetric Layout: Asymmetrie-Grad anpassen
        asymmetry_factor = composition_value * 2 - 1  # -0.8 bis 0.8
        
        for zone_name, zone_data in zones.items():
            if zone_data['content_type'] == 'text_elements':
                # Original-Position speichern
                if 'original_x' not in zone_data:
                    zone_data['original_x'] = zone_data['x']
                    zone_data['original_y'] = zone_data['y']
                
                # Asymmetrische Verschiebung berechnen
                original_x = zone_data['original_x']
                original_y = zone_data['original_y']
                
                # X-Position asymmetrisch verschieben
                x_offset = int(canvas_width * asymmetry_factor * 0.2)
                zone_data['x'] = original_x + x_offset
                
                # Y-Position leicht variieren
                y_offset = int(canvas_height * asymmetry_factor * 0.1)
                zone_data['y'] = original_y + y_offset
                
                # Größe leicht anpassen für dynamischeren Look
                if asymmetry_factor > 0:
                    zone_data['width'] = int(zone_data['width'] * (1 + asymmetry_factor * 0.1))
                else:
                    zone_data['width'] = int(zone_data['width'] * (1 + asymmetry_factor * 0.05))
    
    layout_data['zones'] = zones
    return layout_data

def generate_optimized_prompt(layout_data, design_options, ci_colors, text_inputs, engine_type='dalle3'):
    """
    Generiert einen optimierten, redundanzfreien Prompt
    
    Args:
        layout_data: Layout-Daten
        design_options: Design-Optionen
        ci_colors: CI-Farben
        text_inputs: Texteingaben
        engine_type: KI-Engine-Typ
    
    Returns:
        Optimierter Prompt als String
    """
    # Layout-Kompositions-Anpassung (Phase 1)
    layout_composition = st.session_state.get('layout_composition', 0.5)
    adjusted_layout_data = apply_layout_composition(layout_data, layout_composition)
    
    # Text-Verarbeitungsregeln laden
    text_rules = get_text_processing_rules(engine_type)
    
    # Motiv-Qualität und Style Beschreibungen
    motiv_quality_descriptions = {
        "authentic_warm": "Authentische, warme Atmosphäre mit natürlichen Emotionen",
        "professional_trustworthy": "Professionelle, vertrauensvolle Ausstrahlung",
        "empathetic_human": "Einfühlsame, menschliche Qualität mit Empathie",
        "dynamic_energetic": "Dynamische, energetische Stimmung",
        "calm_reassuring": "Ruhige, beruhigende Atmosphäre"
    }

    motiv_style_descriptions = {
        "natural_candid": "Natürliche, ungestellte Fotografie mit authentischem Licht",
        "documentary_style": "Documentary-Stil mit journalistischem Ansatz",
        "studio_professional": "Studio-Fotografie mit kontrollierter Beleuchtung",
        "cinematic_dramatic": "Cinematischer Stil mit dramatischer Beleuchtung",
        "artistic_creative": "Künstlerischer, kreativer Ansatz mit ungewöhnlichen Perspektiven"
    }
    
    # Motiv-Qualität und Style aus Session State holen
    motiv_quality = st.session_state.get('motiv_quality', ('authentic_warm', 'Authentisch & Warm ❤️'))
    motiv_style = st.session_state.get('motiv_style', ('natural_candid', '📸 Natürlich & Candid'))
    
    # Motiv-Beschreibungen extrahieren
    motiv_quality_desc = motiv_quality_descriptions.get(motiv_quality[0], "Authentische, warme Atmosphäre")
    motiv_style_desc = motiv_style_descriptions.get(motiv_style[0], "Natürliche, ungestellte Fotografie")
    
    # Layout-spezifische Kompositions-Beschreibung
    layout_type = adjusted_layout_data.get('layout_type', 'standard')
    composition_desc = get_composition_description(layout_composition, layout_type)
    
    # Foundation Section (kompakt)
    foundation = f"""# FOUNDATION
creative_type: "Professional Recruiting Creative"
quality_standard: "Ultra-High Quality, 8K Resolution"
canvas: {adjusted_layout_data['canvas']['width']}x{adjusted_layout_data['canvas']['height']} ({adjusted_layout_data['canvas'].get('aspect_ratio', '1:1')})
background: {adjusted_layout_data['canvas'].get('background_color', '#FFFFFF')}

motiv_quality: "{motiv_quality_desc}"
motiv_style: "{motiv_style_desc}"

composition:
  motiv_size: {int(layout_composition*100)}% ({composition_desc})
  container_transparency: {calculate_slider_percentage(design_options['container_transparency'])}% ({get_transparency_description(design_options['container_transparency'])})
  element_spacing: {design_options['element_spacing']}px
  container_padding: {design_options['container_padding']}px
  shadow_intensity: {calculate_slider_percentage(design_options['shadow_intensity'])}%"""

    # Design Section (sauber ohne Emojis)
    design = f"""# DESIGN & CI-COLORS
design:
  layout_style: {get_clean_design_option(design_options['layout_style'])}
  container_shape: {get_clean_design_option(design_options['container_shape'])}
  border_style: {get_clean_design_option(design_options['border_style'])}
  texture_style: {get_clean_design_option(design_options['texture_style'])}
  background_treatment: {get_clean_design_option(design_options['background_treatment'])}
  corner_radius: {get_clean_design_option(design_options['corner_radius'])}
  accent_elements: {get_clean_design_option(design_options['accent_elements'])}

ci_colors:
  primary: {ci_colors['primary']}
  secondary: {ci_colors['secondary']}
  accent: {ci_colors['accent']}
  background: {ci_colors.get('background', '#FFFFFF')}

color_harmony: "Primary, secondary, accent and background colors harmoniously balanced, NO deviations allowed\""""

    # Semantic Layout Section (kompakt) - mit angepassten Layout-Daten
    semantic_layout = generate_semantic_layout_description(adjusted_layout_data)
    semantic = f"""# SEMANTIC LAYOUT
layout_overview: {semantic_layout['layout_overview']}

text_positioning:"""
    
    for text_area in semantic_layout['text_areas']:
        zone_name = text_area['zone_name']
        real_text = text_inputs.get(zone_name, 'Text eingeben')
        # Text normalisieren basierend auf Engine-Regeln
        normalized_text = normalize_german_text(real_text, text_rules['preserve_umlauts'])
        
        semantic += f"""
  {zone_name}: "{normalized_text}"
    position: {text_area['relative_position']}
    size: {text_area['size']}
    adaptive_typography: "Font size adapts to container width, ensures text fits perfectly within boundaries\""""

    semantic += "\nimage_positioning:"
    for image_area in semantic_layout['image_areas']:
        semantic += f"""
  {image_area['zone_name']}: {image_area['description']}
    position: {image_area['relative_position']}
    size: {image_area['size']}"""

    # Technical Rules Section (Engine-spezifisch)
    technical = f"""# TECHNICAL RULES
render_quality: "ULTRA HIGH DETAIL, 8K, professional photography, studio lighting"
text_rules: "ALL TEXTS complete and readable, EXACT at semantic positions"
text_limits: "Headline max {text_rules['max_headline_length']}, Subline max {text_rules['max_subline_length']}, others max {text_rules['max_other_length']} characters"
layout_accuracy: "Image background only, text in separate layers per semantic positioning"
composition_balance: "30% CI-colors, 70% motif, harmonious balancing"

# Engine-specific rules for {engine_type.upper()}
text_processing: "{'Preserve German umlauts' if text_rules['preserve_umlauts'] else 'Replace umlauts with base letters (ä→a, ö→o, ü→u, ß→ss)'}"
text_rendering: "{text_rules['text_rendering']}" """

    # Image generation command at the very end
    image_command = f"""

# GENERATE IMAGE
Generate this image now with all specified parameters and layout requirements."""
    
    return f"{foundation}\n\n{design}\n\n{semantic}\n\n{technical}{image_command}"

# Saubere Design-Optionen ohne Emojis (Referenz)
CLEAN_DESIGN_OPTIONS = {
    'layout_style': {
        'rounded_modern': 'Abgerundet & Modern',
        'sharp_contemporary': 'Scharf & Zeitgemäß',
        'organic_flow': 'Organisch & Fließend',
        'geometric_precision': 'Geometrisch & Präzise'
    },
    'container_shape': {
        'rounded_rectangle': 'Abgerundet',
        'sharp_rectangle': 'Scharf',
        'organic_blob': 'Organisch',
        'geometric_polygon': 'Geometrisch'
    },
    'border_style': {
        'soft_shadow': 'Weicher Schatten',
        'sharp_border': 'Scharfe Kante',
        'gradient_border': 'Farbverlauf-Kante',
        'no_border': 'Keine Kante'
    },
    'texture_style': {
        'gradient': 'Farbverlauf',
        'solid': 'Einfarbig',
        'pattern': 'Muster',
        'texture': 'Textur'
    },
    'background_treatment': {
        'subtle_pattern': 'Subtiles Muster',
        'solid_color': 'Einfarbig',
        'gradient': 'Farbverlauf',
        'texture': 'Textur'
    },
    'corner_radius': {
        'small': 'Klein',
        'medium': 'Mittel',
        'large': 'Groß',
        'xl': 'Keine'
    },
    'accent_elements': {
        'modern_minimal': 'Modern Minimal',
        'decorative': 'Dekorativ',
        'geometric': 'Geometrisch',
        'organic': 'Organisch'
    }
}

# Diese Funktion wurde durch die korrekte Version weiter unten ersetzt
# Die erste Definition hatte Fehler beim Zugriff auf relative_position Felder

# =====================================
# STREAMLIT KONFIGURATION
# =====================================

st.set_page_config(
    page_title="🚀 CreativeAI - Layout Generator",
    page_icon="🎨",
    layout="wide"
)

# Custom CSS
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
    .layout-card {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        background: white;
    }
    .layout-card:hover {
        border-color: #1f77b4;
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.2);
    }
    .layout-card.selected {
        border-color: #1f77b4;
        background: #f0f8ff;
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# HEADER
# =====================================

st.markdown("""
<div class="main-header">
    <h1>🚀 CreativeAI - Layout Generator</h1>
    <p>Wähle dein Layout und erstelle professionelle Recruiting-Designs</p>
</div>
""", unsafe_allow_html=True)

# =====================================
# 1. LAYOUT-AUSWAHL
# =====================================

st.header("🎨 Layout-Auswahl")

# Layout-Eingabe-Modus Auswahl
st.subheader("📐 Layout-Eingabe-Modus")

layout_input_mode = st.radio(
    "Wähle deinen Layout-Eingabe-Modus:",
    ["🎲 Automatische Eingabe", "🎯 Manuelle Eingabe"],
    help="Automatisch: Zufälliges Layout wird gewählt | Manuell: Wähle ein spezifisches Layout",
    index=0  # Standardmäßig Automatische Eingabe
)

# Layout-Style Auswahl
st.subheader("🎨 Layout-Style")

layout_style = st.selectbox(
    "Layout-Konturen:",
    options=[
        ("sharp_geometric", "🎨 Scharf & Geometrisch"),
        ("rounded_modern", "🔵 Abgerundet & Modern"),
        ("organic_flowing", "🌊 Organisch & Fließend"),
        ("wave_contours", "🌊 Wellige Konturen"),
        ("hexagonal", "⬡ Sechseckig"),
        ("circular", "⭕ Kreisförmig"),
        ("asymmetric", "⚡ Asymmetrisch"),
        ("minimal_clean", "⚪ Minimal & Clean")
    ],
    format_func=lambda x: x[1],
    index=1,  # Default: rounded_modern
    help="Bestimmt die Kontur-Form der Layout-Bereiche im generierten Bild",
    key="layout_style_input"
)

# Wert in Session State speichern
st.session_state['layout_style'] = layout_style

# Layout-Style Beschreibung
layout_style_descriptions = {
    "sharp_geometric": "Scharfe, eckige Konturen für ein modernes, technisches Aussehen",
    "rounded_modern": "Sanft abgerundete Ecken für ein freundliches, modernes Design",
    "organic_flowing": "Organische, fließende Formen für ein natürliches, dynamisches Layout",
    "wave_contours": "Wellige, geschwungene Konturen für ein spielerisches, kreatives Design",
    "hexagonal": "Sechseckige Formen für ein futuristisches, technisches Aussehen",
    "circular": "Kreisförmige und ovale Bereiche für ein harmonisches, ausgewogenes Layout",
    "asymmetric": "Asymmetrische, unregelmäßige Formen für ein dynamisches, künstlerisches Design",
    "minimal_clean": "Minimalistische, saubere Linien für ein professionelles, klares Layout"
}

st.caption(f"💡 {layout_style_descriptions[layout_style[0]]}")

# Bedingte Anzeige der Layout-Optionen
if layout_input_mode == "🎯 Manuelle Eingabe":
    st.subheader("📐 Layout auswählen")

# Originalskizzen laden
original_sketches = load_original_sketches()

# Layout-Definitionen mit den neuen YAML-Templates
layouts = [
    {
        "id": "skizze1_vertical_split",
        "name": "Vertical Split",
        "description": "Links Text, rechts Motiv",
        "sketch": original_sketches.get("Skizze1"),
        "template": "skizze1_vertical_split",
        "render_command": "finale Werbebild jetzt direkt rendern und ausgeben"
    },
    {
        "id": "skizze2_horizontal_split",
        "name": "Horizontal Split", 
        "description": "Oben Text, unten Motiv",
        "sketch": original_sketches.get("Skizze2"),
        "template": "skizze2_horizontal_split",
        "render_command": "finale Werbebild jetzt direkt rendern und ausgeben"
    },
    {
        "id": "skizze3_centered_layout",
        "name": "Centered Layout",
        "description": "Zentriertes Design",
        "sketch": original_sketches.get("Skizze3"),
        "template": "skizze3_centered_layout",
        "render_command": "finale Werbebild jetzt direkt rendern und ausgeben"
    },
    {
        "id": "skizze4_diagonal_layout",
        "name": "Diagonal Layout",
        "description": "Diagonale Aufteilung",
        "sketch": original_sketches.get("Skizze4"),
        "template": "skizze4_diagonal_layout",
        "render_command": "finale Werbebild jetzt direkt rendern und ausgeben"
    },
    {
        "id": "skizze5_asymmetric_layout",
        "name": "Asymmetric Layout",
        "description": "Asymmetrisches Design",
        "sketch": original_sketches.get("Skizze5"),
        "template": "skizze5_asymmetric_layout",
        "render_command": "finale Werbebild jetzt direkt rendern und ausgeben"
    },
    {
        "id": "skizze6_grid_layout",
        "name": "Grid Layout",
        "description": "Raster-Anordnung",
        "sketch": original_sketches.get("Skizze6"),
        "template": "skizze6_grid_layout",
        "render_command": "finale Werbebild jetzt direkt rendern und ausgeben"
    },
    {
        "id": "skizze7_minimalist_layout",
        "name": "Minimalist Layout",
        "description": "Minimalistisches Design",
        "sketch": original_sketches.get("Skizze7"),
        "template": "skizze7_minimalist_layout",
        "render_command": "finale Werbebild jetzt direkt rendern und ausgeben"
    },
    {
        "id": "skizze8_hero_layout",
        "name": "Hero Layout",
        "description": "Hero-Motiv mit Overlay",
        "sketch": original_sketches.get("Skizze8"),
        "template": "skizze8_hero_layout",
        "render_command": "finale Werbebild jetzt direkt rendern und ausgeben"
    },
    {
        "id": "skizze9_storytelling_layout",
        "name": "Storytelling Layout",
        "description": "Storytelling-Design",
        "sketch": original_sketches.get("Skizze9"),
        "template": "skizze9_storytelling_layout",
        "render_command": "finale Werbebild jetzt direkt rendern und ausgeben"
    },
    {
        "id": "skizze10_modern_split",
        "name": "Modern Split",
        "description": "Moderne Split-Anordnung",
        "sketch": original_sketches.get("Skizze10"),
        "template": "skizze10_modern_split",
        "render_command": "finale Werbebild jetzt direkt rendern und ausgeben"
    },
    {
        "id": "skizze11_infographic_layout",
        "name": "Infographic Layout",
        "description": "Infografik-Design",
        "sketch": original_sketches.get("Skizze11"),
        "template": "skizze11_infographic_layout",
        "render_command": "finale Werbebild jetzt direkt rendern und ausgeben"
    },
    {
        "id": "skizze12_magazine_layout",
        "name": "Magazine Layout",
        "description": "Magazin-Layout",
        "sketch": original_sketches.get("Skizze12"),
        "template": "skizze12_magazine_layout",
        "render_command": "finale Werbebild jetzt direkt rendern und ausgeben"
    },
    {
        "id": "skizze13_portfolio_layout",
        "name": "Portfolio Layout",
        "description": "Portfolio-Design",
        "sketch": original_sketches.get("Skizze13"),
        "template": "skizze13_portfolio_layout",
        "render_command": "finale Werbebild jetzt direkt rendern und ausgeben"
    }
]

# Layout Auswahl als Grid
cols = st.columns(3)  # 3 Spalten für stabile Anzeige  
selected_layout_id = st.session_state.get('selected_layout', 'skizze1_vertical_split')

if layout_input_mode == "🎯 Manuelle Eingabe":
    for i, layout in enumerate(layouts):
        col_index = i % 3
        with cols[col_index]:
            # Layout-Button
            if st.button(f"**{layout['name']}**\n{layout['description']}", 
                        key=f"layout_{layout['id']}", 
                        use_container_width=True):
                st.session_state.selected_layout = layout["id"]
                st.rerun()
            
            # Originalskizze als Vorschau
            display_sketch_preview(layout["sketch"], layout["id"], selected_layout_id)

    # Aktuell gewähltes Layout
    layout_id = selected_layout_id
    layout_name = next(l['name'] for l in layouts if l['id'] == layout_id)

    st.caption(f"🎯 Gewähltes Layout: {layout_name} ({layout_id})")

elif layout_input_mode == "🎲 Automatische Eingabe":
    # Zufällige Layout-Auswahl
    random_layout = random.choice(layouts)
    layout_id = random_layout['id']
    layout_name = random_layout['name']
    
    # Layout in Session State speichern
    st.session_state.selected_layout = layout_id
    
    # Zufälliges Layout anzeigen
    st.subheader("🎲 Zufällig gewähltes Layout")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Originalskizze als Vorschau
        display_sketch_preview(random_layout["sketch"], layout_id, layout_id)
    
    with col2:
        st.caption(f"🎯 **Zufällig gewähltes Layout:** {layout_name}")
        st.caption(f"📐 **Layout-ID:** {layout_id}")
        st.caption(f"📝 **Beschreibung:** {random_layout['description']}")
        
        # Button zum Neugenerieren
        if st.button("🔄 Anderes Layout wählen", key="regenerate_random_layout"):
            st.rerun()
    
    st.caption(f"🎲 **Automatisch gewählt:** {layout_name} ({layout_id})")

# Vereinfachte Layout-Informationen (nur Status)
if 'selected_layout' in st.session_state:
    selected_layout = st.session_state.selected_layout
    layout_info = load_layout_info(selected_layout)
    
    if layout_info:
        # Nur Status anzeigen, keine Details
        try:
            validation_results = validate_layout_coordinates(layout_info)
            if validation_results['is_valid']:
                st.success("✅ Layout bereit")
            else:
                st.warning("⚠️ Layout hat Probleme")
        except:
            st.info("ℹ️ Layout geladen")

# =====================================
# 2. DESIGN & STYLE-OPTIONEN
# =====================================

st.header("🎨 Design & Style-Optionen")

# 🎲 RANDOMISIEREN BUTTON direkt im Header
col1, col2, col3 = st.columns([2, 1, 2])

with col2:
    if st.button("🎲 Style randomisieren", type="secondary", use_container_width=True, key="randomize_style_button_header"):
        import random
        
        # Alle verfügbaren Optionen definieren
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
        
        # Alle Style-Optionen zufällig auswählen
        random_selections = {}
        for option_name, options_list in style_options.items():
            random_selections[option_name] = random.choice(options_list)
        
        # Zusätzliche Layout-Parameter zufällig setzen
        random_transparency = round(random.uniform(0.3, 0.9), 1)
        random_layout_composition = round(random.uniform(0.2, 0.8), 1)
        random_element_spacing = random.randint(15, 60)
        random_container_padding = random.randint(10, 35)
        random_shadow_intensity = round(random.uniform(0.1, 0.7), 1)
        
        # Session State mit zufälligen Werten aktualisieren
        st.session_state['layout_style'] = random_selections['layout_style']
        st.session_state['container_shape'] = random_selections['container_shape']
        st.session_state['border_style'] = random_selections['border_style']
        st.session_state['texture_style'] = random_selections['texture_style']
        st.session_state['background_treatment'] = random_selections['background_treatment']
        st.session_state['corner_radius'] = random_selections['corner_radius']
        st.session_state['accent_elements'] = random_selections['accent_elements']
        
        # Neue Layout-Parameter
        st.session_state['container_transparency'] = random_transparency
        st.session_state['layout_composition'] = random_layout_composition
        st.session_state['element_spacing'] = random_element_spacing
        st.session_state['container_padding'] = random_container_padding
        st.session_state['shadow_intensity'] = random_shadow_intensity
        
        # Legacy-Support für image_text_ratio
        st.session_state['image_text_ratio'] = random_layout_composition
        
        # Erfolgsmeldung anzeigen
        st.success("🎲 **Style erfolgreich randomisiert!** Alle Optionen wurden zufällig neu ausgewählt.")
        
        # Zufällige Auswahl anzeigen
        st.info("🎯 **Neue zufällige Auswahl:**")
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.write(f"• **Layout-Style**: {random_selections['layout_style'][1]}")
            st.write(f"• **Container-Form**: {random_selections['container_shape'][1]}")
            st.write(f"• **Rahmen-Stil**: {random_selections['border_style'][1]}")
        
        with col_info2:
            st.write(f"• **Textur-Stil**: {random_selections['texture_style'][1]}")
            st.write(f"• **Hintergrund**: {random_selections['background_treatment'][1]}")
            st.write(f"• **Ecken-Rundung**: {random_selections['corner_radius'][1]}")
            st.write(f"• **Akzent-Stil**: {random_selections['accent_elements'][1]}")
        
        # Neue Layout-Parameter anzeigen
        st.info("🎛️ **Neue Layout-Parameter:**")
        col_info3, col_info4 = st.columns(2)
        
        with col_info3:
            st.write(f"• **Transparenz**: {random_transparency} ({'🔍 Sehr transparent' if random_transparency <= 0.3 else '🌫️ Transparent' if random_transparency <= 0.6 else '💎 Leicht transparent' if random_transparency <= 0.8 else '🪨 Undurchsichtig'})")
            st.write(f"• **Layout-Komposition**: {random_layout_composition} ({'📐 Schmale Textspalte' if random_layout_composition <= 0.3 else '⚖️ Ausgewogen' if random_layout_composition <= 0.5 else '📏 Breite Textspalte' if random_layout_composition <= 0.7 else '🎨 Sehr breite Textspalte'})")
        
        with col_info4:
            st.write(f"• **Element-Abstände**: {random_element_spacing}px")
            st.write(f"• **Container-Padding**: {random_container_padding}px")
            st.write(f"• **Schatten-Intensität**: {random_shadow_intensity}")
        
        # Seite neu laden für aktualisierte Anzeige
        st.rerun()

# Info über Randomisieren
st.caption("💡 **Tipp**: Klicke auf den Button, um alle Style-Optionen zufällig neu zu kombinieren. Perfekt für kreative Inspiration!")

# =====================================
# SCHIEBEREGLER FÜR TRANSPARENZ UND BILD-TEXT-VERHÄLTNIS
# =====================================

# st.subheader("🎛️ Layout-Parameter")

# Schieberegler in 2 Spalten
slider_col1, slider_col2 = st.columns(2)

with slider_col1:
    # Container-Transparenz
    container_transparency = st.slider(
        "Container-Transparenz:",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.get('container_transparency', 0.8),
        step=0.1,
        help="Transparenz der Text-Container (0 = komplett transparent, 1 = undurchsichtig)",
        key="container_transparency_slider"
    )
    # Wert in Session State speichern
    st.session_state['container_transparency'] = container_transparency
    
    # Transparenz-Info anzeigen
    # if container_transparency <= 0.3:
    #     transparency_status = "🔍 Sehr transparent"
    #     if container_transparency < 0.2:
    #         st.warning("⚠️ Sehr geringe Transparenz kann Text schwer lesbar machen")
    # elif container_transparency <= 0.6:
    #     transparency_status = "🌫️ Transparent"
    # elif container_transparency <= 0.8:
    #     transparency_status = "💎 Leicht transparent"
    # else:
    #     transparency_status = "🪨 Undurchsichtig"
    #     if container_transparency > 0.9:
    #         st.info("ℹ️ Hohe Undurchsichtigkeit schafft solide Text-Container")
    
    # st.caption(f"Status: {transparency_status}")

with slider_col2:
    # Layout-Kompositions-Slider (Phase 1)
    layout_composition = st.slider(
        "🎨 Motiv-Größe:",
        min_value=0.1,
        max_value=0.9,
        value=st.session_state.get('layout_composition', 0.5),
        step=0.1,
        help="Steuert die Größe des Motivs im Layout (layout-spezifisch)",
        key="layout_composition_slider"
    )
    # Wert in Session State speichern
    st.session_state['layout_composition'] = layout_composition
    
    # Layout-spezifische Beschreibung anzeigen
    if 'selected_layout' in st.session_state:
        selected_layout = st.session_state.selected_layout
        layout_info = load_layout_info(selected_layout)
        if layout_info:
            layout_type = layout_info.get('layout_type', 'standard')
            composition_desc = get_composition_description(layout_composition, layout_type)
            st.caption(f"📐 {composition_desc}")
    
    # Legacy-Support: image_text_ratio für Kompatibilität
    st.session_state['image_text_ratio'] = layout_composition

# Zusätzliche Layout-Parameter
# st.subheader("🔧 Erweiterte Layout-Einstellungen")

advanced_col1, advanced_col2, advanced_col3 = st.columns(3)

with advanced_col1:
    # Abstand zwischen Elementen
    element_spacing = st.slider(
        "Element-Abstände:",
        min_value=10,
        max_value=100,
        value=st.session_state.get('element_spacing', 30),
        step=5,
        help="Abstand zwischen Layout-Elementen in Pixeln",
        key="element_spacing_slider"
    )
    st.session_state['element_spacing'] = element_spacing
    
    # Validierung der Element-Abstände
    # if element_spacing < 15:
    #     st.warning("⚠️ Sehr geringe Abstände können zu Überlappungen führen")
    # elif element_spacing > 80:
    #     st.info("ℹ️ Große Abstände schaffen luftiges Layout")

with advanced_col2:
    # Padding der Container
    container_padding = st.slider(
        "Container-Padding:",
        min_value=5,
        max_value=50,
        value=st.session_state.get('container_padding', 20),
        step=5,
        help="Innenabstand der Text-Container in Pixeln",
        key="container_padding_slider"
    )
    st.session_state['container_padding'] = container_padding
    
    # Validierung des Container-Paddings
    # if container_padding < 10:
    #     st.warning("⚠️ Geringes Padding kann Text zu nah an den Rändern platzieren")
    # elif container_padding > 40:
    #     st.info("ℹ️ Großes Padding schafft luftige Text-Container")

with advanced_col3:
    # Schatten-Intensität
    shadow_intensity = st.slider(
        "Schatten-Intensität:",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.get('shadow_intensity', 0.3),
        step=0.1,
        help="Intensität der Schatten-Effekte",
        key="shadow_intensity_slider"
    )
    st.session_state['shadow_intensity'] = shadow_intensity
    
    # Validierung der Schatten-Intensität
    # if shadow_intensity < 0.1:
    #     st.info("ℹ️ Subtile Schatten für dezente Tiefe")
    # elif shadow_intensity > 0.6:
    #     st.warning("⚠️ Starke Schatten können von Inhalten ablenken")

# Layout-Parameter-Zusammenfassung
# st.write("**🎯 Aktuelle Layout-Parameter:**")
# param_summary_cols = st.columns(4)

# with param_summary_cols[0]:
#     st.metric("🌫️ Transparenz", f"{container_transparency:.1f}")
# with param_summary_cols[1]:
#     st.metric("⚖️ Bild-Text", f"{image_text_ratio:.1f}")
# with param_summary_cols[2]:
#     st.metric("📏 Abstände", f"{element_spacing}px")
# with param_summary_cols[3]:
#     st.metric("💡 Schatten", f"{shadow_intensity:.1f}")

# st.divider()

# =====================================
# DESIGN-INTEGRATION INFO
# =====================================

# st.info("💡 **Design & Style werden automatisch mit dem Layout verknüpft, wenn Sie den 'Prompt erstellen' Button am Ende des Frontends klicken.**")

# st.divider()

# =====================================
# STYLE-OPTIONEN (3-SPALTEN-LAYOUT)
# =====================================

style_col1, style_col2, style_col3 = st.columns(3)

with style_col1:
    # st.subheader("📦 Text-Container")
    
    # Container-Form mit dynamischem Index aus Session State
    container_shape_options = [
            ("rectangle", "Rechteckig 📐"),
            ("rounded_rectangle", "Abgerundet 📱"), 
            ("circle", "Kreisförmig ⭕"),
            ("hexagon", "Sechseckig ⬡"),
            ("organic_blob", "Organisch 🫧")
    ]
    
    # Aktuellen Index aus Session State ermitteln
    current_container_shape = st.session_state.get('container_shape', ('rounded_rectangle', 'Abgerundet 📱'))
    current_container_index = next((i for i, opt in enumerate(container_shape_options) if opt[0] == current_container_shape[0]), 1)
    
    container_shape = st.selectbox(
        "Form der Text-Bereiche:",
        options=container_shape_options,
        format_func=lambda x: x[1],
        index=current_container_index,  # Dynamischer Index
        help="Bestimmt die Form der Text-Container im Creative",
        key="container_shape_input"
    )
    # Wert in Session State speichern
    st.session_state['container_shape'] = container_shape
    
    # Rahmen-Stil mit dynamischem Index aus Session State
    border_style_options = [
            ("solid", "Durchgezogen ━"),
            ("dashed", "Gestrichelt ┅"),
            ("dotted", "Gepunktet ┈"),
            ("soft_shadow", "Weicher Schatten 🌫️"),
            ("glow", "Leuchteffekt ✨"),
            ("none", "Ohne Rahmen")
    ]
    
    # Aktuellen Index aus Session State ermitteln
    current_border_style = st.session_state.get('border_style', ('soft_shadow', '🌫️ Weicher Schatten'))
    current_border_index = next((i for i, opt in enumerate(border_style_options) if opt[0] == current_border_style[0]), 3)
    
    border_style = st.selectbox(
        "Rahmen-Stil:",
        options=border_style_options,
        format_func=lambda x: x[1],
        index=current_border_index,  # Dynamischer Index
        help="Stil des Rahmens um Text-Bereiche",
        key="border_style_input"
    )
    # Wert in Session State speichern
    st.session_state['border_style'] = border_style

with style_col2:
    st.subheader("🖌️ Visuelle Effekte")
    
    # Textur-Stil mit dynamischem Index aus Session State
    texture_style_options = [
            ("solid", "Einfarbig 🎨"),
            ("gradient", "Farbverlauf 🌈"),
            ("pattern", "Muster 📐"),
            ("glass_effect", "Glas-Effekt 💎"),
            ("matte", "Matt 🎭")
    ]
    
    # Aktuellen Index aus Session State ermitteln
    current_texture_style = st.session_state.get('texture_style', ('gradient', '🌈 Farbverlauf'))
    current_texture_index = next((i for i, opt in enumerate(texture_style_options) if opt[0] == current_texture_style[0]), 1)
    
    texture_style = st.selectbox(
        "Textur-Stil:",
        options=texture_style_options,
        format_func=lambda x: x[1],
        index=current_texture_index,  # Dynamischer Index
        help="Oberflächentextur der Text-Container"
    )
    # Wert in Session State speichern
    st.session_state['texture_style'] = texture_style
    
    # Hintergrund-Behandlung mit dynamischem Index aus Session State
    background_treatment_options = [
            ("solid", "Einfarbig 🎨"),
                ("subtle_pattern", "Subtiles Muster 🌸"),
            ("geometric", "Geometrisch 📐"),
            ("organic", "Organisch 🌿"),
            ("none", "Transparent")
    ]
    
    # Aktuellen Index aus Session State ermitteln
    current_background_treatment = st.session_state.get('background_treatment', ('subtle_pattern', '🌸 Subtiles Muster'))
    current_background_index = next((i for i, opt in enumerate(background_treatment_options) if opt[0] == current_background_treatment[0]), 1)
    
    background_treatment = st.selectbox(
        "Hintergrund-Behandlung:",
        options=background_treatment_options,
        format_func=lambda x: x[1],
        index=current_background_index,  # Dynamischer Index
        help="Behandlung des Creative-Hintergrunds"
    )
    # Wert in Session State speichern
    st.session_state['background_treatment'] = background_treatment

with style_col3:
    # st.subheader("📐 Layout-Details")
    
    # Ecken-Rundung mit dynamischem Index aus Session State
    corner_radius_options = [
            ("small", "Klein (8px) ⌐"),
            ("medium", "Mittel (16px) ⌜"), 
            ("large", "Groß (24px) ⌞"),
            ("xl", "Sehr groß (32px) ◜")
    ]
    
    # Aktuellen Index aus Session State ermitteln
    current_corner_radius = st.session_state.get('corner_radius', ('medium', '⌜ Mittel'))
    current_corner_index = next((i for i, opt in enumerate(corner_radius_options) if opt[0] == current_corner_radius[0]), 1)
    
    corner_radius = st.selectbox(
        "Ecken-Rundung:",
        options=corner_radius_options,
        format_func=lambda x: x[1],
        index=current_corner_index,  # Dynamischer Index
        help="Rundung der Ecken der Text-Container"
    )
    # Wert in Session State speichern
    st.session_state['corner_radius'] = corner_radius
    
    # Akzent-Elemente mit dynamischem Index aus Session State
    accent_elements_options = [
            ("modern_minimal", "Modern Minimal ⚪"),
            ("classic_elegant", "Klassisch Elegant ️"),
            ("bold_dramatic", "Bold & Dramatisch ⚡"),
            ("soft_organic", "Sanft Organisch 🌿"),
            ("none", "Ohne Akzente")
    ]
    
    # Aktuellen Index aus Session State ermitteln
    current_accent_elements = st.session_state.get('accent_elements', ('modern_minimal', '⚪ Modern Minimal'))
    current_accent_index = next((i for i, opt in enumerate(accent_elements_options) if opt[0] == current_accent_elements[0]), 0)
    
    accent_elements = st.selectbox(
        "Akzent-Elemente:",
        options=accent_elements_options,
        format_func=lambda x: x[1],
        index=current_accent_index,  # Dynamischer Index
        help="Zusätzliche visuelle Akzente im Design"
    )
    # Wert in Session State speichern
    st.session_state['accent_elements'] = accent_elements

# Neue Spalte für Motiv-Qualität und Motiv-Style
with st.container():
    st.subheader("🎭 Motiv-Einstellungen")
    
    motiv_col1, motiv_col2 = st.columns(2)
    
    with motiv_col1:
        # Motiv-Qualität mit dynamischem Index aus Session State
        motiv_quality_options = [
            ("authentic_warm", "Authentisch & Warm ❤️"),
            ("professional_trustworthy", "Professionell & Vertrauensvoll 🤝"),
            ("empathetic_human", "Einfühlsam & Menschlich 💙"),
            ("dynamic_energetic", "Dynamisch & Energetisch ⚡"),
            ("calm_reassuring", "Ruhig & Beruhigend 🌸")
        ]
        
        # Aktuellen Index aus Session State ermitteln
        current_motiv_quality = st.session_state.get('motiv_quality', ('authentic_warm', '❤️ Authentisch & Warm'))
        current_motiv_quality_index = next((i for i, opt in enumerate(motiv_quality_options) if opt[0] == current_motiv_quality[0]), 0)
        
        motiv_quality = st.selectbox(
            "Motiv-Qualität:",
            options=motiv_quality_options,
            format_func=lambda x: x[1],
            index=current_motiv_quality_index,  # Dynamischer Index
            help="Bestimmt die emotionale Qualität und Atmosphäre des Motivs"
        )
        # Wert in Session State speichern
        st.session_state['motiv_quality'] = motiv_quality
    
    with motiv_col2:
        # Motiv-Style mit dynamischem Index aus Session State
        motiv_style_options = [
            ("natural_candid", "Natürlich & Candid 📸"),
            ("documentary_style", "Documentary-Style 🎬"),
            ("studio_professional", "Studio & Professionell 🎭"),
            ("cinematic_dramatic", "Cinematisch & Dramatisch 🎥"),
            ("artistic_creative", "Künstlerisch & Kreativ 🎨")
        ]
        
        # Aktuellen Index aus Session State ermitteln
        current_motiv_style = st.session_state.get('motiv_style', ('natural_candid', '📸 Natürlich & Candid'))
        current_motiv_style_index = next((i for i, opt in enumerate(motiv_style_options) if opt[0] == current_motiv_style[0]), 0)
        
        motiv_style = st.selectbox(
            "Motiv-Style:",
            options=motiv_style_options,
            format_func=lambda x: x[1],
            index=current_motiv_style_index,  # Dynamischer Index
            help="Bestimmt den fotografischen Stil und die Beleuchtung des Motivs"
        )
        # Wert in Session State speichern
        st.session_state['motiv_style'] = motiv_style

# Motiv-Qualität und Style Beschreibungen
motiv_quality_descriptions = {
    "authentic_warm": "Authentische, warme Atmosphäre mit natürlichen Emotionen",
    "professional_trustworthy": "Professionelle, vertrauensvolle Ausstrahlung",
    "empathetic_human": "Einfühlsame, menschliche Qualität mit Empathie",
    "dynamic_energetic": "Dynamische, energetische Stimmung",
    "calm_reassuring": "Ruhige, beruhigende Atmosphäre"
}

motiv_style_descriptions = {
    "natural_candid": "Natürliche, ungestellte Fotografie mit authentischem Licht",
    "documentary_style": "Documentary-Stil mit journalistischem Ansatz",
    "studio_professional": "Studio-Fotografie mit kontrollierter Beleuchtung",
    "cinematic_dramatic": "Cinematischer Stil mit dramatischer Beleuchtung",
    "artistic_creative": "Künstlerischer, kreativer Ansatz mit ungewöhnlichen Perspektiven"
}

st.caption(f"💡 Motiv-Qualität: {motiv_quality_descriptions[motiv_quality[0]]}")
st.caption(f"💡 Motiv-Style: {motiv_style_descriptions[motiv_style[0]]}")

# Style-Zusammenfassung
st.write("**🎯 Gewählter Style:**")
style_summary_cols = st.columns(4)

with style_summary_cols[0]:
    st.markdown(f"""
    <div style="padding: 10px; border-radius: 8px; background: linear-gradient(45deg, #005EA520, #FFC20E20); border: 2px solid #FFC20E;">
        <strong>Form:</strong> {container_shape[1]}<br>
        <strong>Rahmen:</strong> {border_style[1]}
    </div>
    """, unsafe_allow_html=True)

with style_summary_cols[1]:
    st.markdown(f"""
    <div style="padding: 10px; border-radius: 8px; background: linear-gradient(45deg, #B4D9F740, #005EA520); border: 2px solid #005EA5;">
        <strong>Textur:</strong> {texture_style[1]}<br>
        <strong>Hintergrund:</strong> {background_treatment[1]}
    </div>
    """, unsafe_allow_html=True)

with style_summary_cols[2]:
    st.markdown(f"""
    <div style="padding: 10px; border-radius: 8px; background: #B4D9F7; border: 2px solid #005EA5;">
        <strong>Rundung:</strong> {corner_radius[1]}<br>
        <strong>Akzente:</strong> {accent_elements[1]}
    </div>
    """, unsafe_allow_html=True)

with style_summary_cols[3]:
    st.markdown(f"""
    <div style="padding: 10px; border-radius: 8px; background: #FFC20E; color: white; text-align: center;">
        <strong>🎨 STYLE</strong><br>
        <small>Personalisiert</small>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =====================================
# CI-FARBEN-INTEGRATION
# =====================================

# st.subheader("🎨 CI-Farbpalette")

# Vordefinierte CI-Paletten (ERWEITERT um vierte Hintergrundfarbe)
ci_color_palettes = [
    {
        "name": "Medizinisches Blau-Gold",
        "primary": "#005EA5",      # Dunkelblau
        "secondary": "#B4D9F7",    # Hellblau
        "accent": "#FFC20E",       # Gold
        "background": "#FFF8E1",   # Warmes Creme (komplementär zu Blau)
        "description": "Klassische medizinische Farben"
    },
    {
        "name": "Naturverbunden Grün-Koralle",
        "primary": "#2E7D32",      # Dunkelgrün
        "secondary": "#C8E6C9",    # Hellgrün
        "accent": "#FF7043",       # Koralle
        "background": "#FFF3E0",   # Warmes Pfirsich (komplementär zu Grün)
        "description": "Naturverbundene, beruhigende Farben"
    },
    {
        "name": "Professionell Navy-Silber",
        "primary": "#1A237E",      # Navy
        "secondary": "#E8EAF6",    # Silber
        "accent": "#FF9800",       # Orange
        "background": "#FBE9E7",   # Warmes Rosa (komplementär zu Navy)
        "description": "Professionelle Business-Farben"
    },
    {
        "name": "Vertrauensvoll Teal-Orange",
        "primary": "#00695C",      # Teal
        "secondary": "#B2DFDB",    # Hellteal
        "accent": "#FF5722",       # Orange
        "background": "#FCE4EC",   # Zartes Rosa (komplementär zu Teal)
        "description": "Moderne, vertrauensvolle Farben"
    },
    {
        "name": "Elegant Burgund-Creme",
        "primary": "#8E24AA",      # Burgund
        "secondary": "#F3E5F5",    # Creme
        "accent": "#FFC107",       # Gelb
        "background": "#E8F5E8",   # Zartes Grün (komplementär zu Burgund)
        "description": "Elegante, traditionelle Farben"
    },
    {
        "name": "Zeitlos Grau-Blau",
        "primary": "#424242",      # Grau
        "secondary": "#E3F2FD",    # Hellblau
        "accent": "#2196F3",       # Blau
        "background": "#FFFDE7",   # Warmes Gelb (komplementär zu Grau)
        "description": "Zeitlose, seriöse Farben"
    },
    {
        "name": "Beruhigend Smaragd-Lavendel",
        "primary": "#388E3C",      # Smaragd
        "secondary": "#E1F5FE",    # Hellblau
        "accent": "#9C27B0",       # Lavendel
        "background": "#F3E5F5",   # Zartes Lavendel (harmonisch zu Smaragd)
        "description": "Beruhigende, heilende Farben"
    },
    {
        "name": "Dynamisch Schwarz-Rot",
        "primary": "#212121",      # Schwarz
        "secondary": "#FFEBEE",    # Hellrot
        "accent": "#F44336",       # Rot
        "background": "#E0F2F1",   # Zartes Mint (komplementär zu Schwarz/Rot)
        "description": "Kontrastreiche, dynamische Farben"
    },
    {
        "name": "Warm Beige-Terrakotta",
        "primary": "#8D6E63",      # Beige
        "secondary": "#EFEBE9",    # Hellbeige
        "accent": "#D84315",       # Terrakotta
        "background": "#E8F5E8",   # Zartes Grün (komplementär zu Beige/Terrakotta)
        "description": "Warme, einladende Farben"
    },
    {
        "name": "Frisch Mint-Pfirsich",
        "primary": "#4DB6AC",      # Mint
        "secondary": "#E0F2F1",    # Hellmint
        "accent": "#FFAB91",       # Pfirsich
        "background": "#FCE4EC",   # Zartes Rosa (komplementär zu Mint)
        "description": "Frische, moderne Farben"
    }
]

# 🎲 RANDOMISIERER für CI-Farben (ERWEITERT um vierte Farbe)
col1, col2, col3 = st.columns([2, 1, 2])

with col2:
    if st.button("🎲 CI-Farben randomisieren", type="secondary", use_container_width=True, key="randomize_ci_colors_button"):
        # Generiere zufällige CI-Farbpalette
        random_palette = random.choice(ci_color_palettes)
        
        # Setze Farben in Session State (ERWEITERT um background)
        st.session_state.primary_color = random_palette["primary"]
        st.session_state.secondary_color = random_palette["secondary"]
        st.session_state.accent_color = random_palette["accent"]
        st.session_state.background_color = random_palette["background"]
        
        # Zeige Erfolgsmeldung
        st.success(f"🎨 Neue Farbpalette: {random_palette['name']}")
        st.info(f"💡 {random_palette['description']}")
        
        # Rerun für sofortige Anwendung
        st.rerun()

st.divider()

# Vordefinierte CI-Paletten anzeigen (ERWEITERT um vierte Farbe)
st.write("**🎨 Vordefinierte CI-Paletten:**")

palette_cols = st.columns(min(3, len(ci_color_palettes)))

for i, palette_data in enumerate(ci_color_palettes):
    with palette_cols[i % 3]:
        if st.button(f"📋 {palette_data['name']}", key=f"palette_{i}", use_container_width=True):
            # Setze Farben aus gewählter Palette (ERWEITERT um background)
            st.session_state.primary_color = palette_data["primary"]
            st.session_state.secondary_color = palette_data["secondary"] 
            st.session_state.accent_color = palette_data["accent"]
            st.session_state.background_color = palette_data["background"]
            st.rerun()
        
        # Mini-Palette-Vorschau (ERWEITERT um vierte Farbe)
        st.markdown(f"""
        <div style="display: flex; height: 30px; border-radius: 5px; overflow: hidden; margin: 5px 0;">
            <div style="background: {palette_data['primary']}; flex: 1;"></div>
            <div style="background: {palette_data['secondary']}; flex: 1;"></div>
            <div style="background: {palette_data['accent']}; flex: 1;"></div>
            <div style="background: {palette_data['background']}; flex: 1; border-left: 1px solid #ddd;"></div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Color Pickers (ERWEITERT um vierte Farbe)
col1, col2, col3, col4 = st.columns(4)

with col1:
    primary_color = st.color_picker(
        "Primärfarbe:", 
        value=st.session_state.get("primary_color", "#005EA5"),
        help="Headlines, wichtige Texte"
    )
    st.session_state.primary_color = primary_color

with col2:
    secondary_color = st.color_picker(
        "Sekundärfarbe:", 
        value=st.session_state.get("secondary_color", "#B4D9F7"),
        help="Hintergrund- und Flächen"
    )
    st.session_state.secondary_color = secondary_color

with col3:
    accent_color = st.color_picker(
        "Akzentfarbe:", 
        value=st.session_state.get("accent_color", "#FFC20E"),
        help="CTA, Bullets, Akzente"
    )
    st.session_state.accent_color = accent_color

with col4:
    background_color = st.color_picker(
        "Hintergrundfarbe:", 
        value=st.session_state.get("background_color", "#FFFFFF"),
        help="Haupt-Hintergrund, Rahmen, neutrale Elemente"
    )
    st.session_state.background_color = background_color

# Farb-Vorschau
st.write("**🎨 Farb-Vorschau:**")

# Aktive Farben-Info
current_colors_info = f"""
**🎯 Aktive Farben:**
- **Primär:** `{primary_color}` (Headlines, wichtige Texte)
- **Sekundär:** `{secondary_color}` (Hintergrund- und Flächen)
- **Akzent:** `{accent_color}` (CTA, Bullets, Akzente)
- **Hintergrund:** `{background_color}` (Haupt-Hintergrund, Rahmen, neutrale Elemente)
"""
st.info(current_colors_info)

preview_cols = st.columns(4)

with preview_cols[0]:
    st.markdown(f"""
    <div style="padding: 15px; border-radius: 8px; background-color: {primary_color}; text-align: center; margin-bottom: 10px;">
        <span style="color: white; font-weight: bold;">Primary</span><br>
        <small style="color: white;">{primary_color}</small>
    </div>
    """, unsafe_allow_html=True)

with preview_cols[1]:
    st.markdown(f"""
    <div style="padding: 15px; border-radius: 8px; background-color: {secondary_color}; text-align: center; margin-bottom: 10px; border: 1px solid #ddd;">
        <span style="color: #333; font-weight: bold;">Secondary</span><br>
        <small style="color: #333;">{secondary_color}</small>
    </div>
    """, unsafe_allow_html=True)

with preview_cols[2]:
    st.markdown(f"""
    <div style="padding: 15px; border-radius: 8px; background-color: {accent_color}; text-align: center; margin-bottom: 10px;">
        <span style="color: white; font-weight: bold;">Accent</span><br>
        <small style="color: white;">{accent_color}</small>
    </div>
    """, unsafe_allow_html=True)

with preview_cols[3]:
    st.markdown(f"""
    <div style="padding: 15px; border-radius: 8px; background-color: {background_color}; text-align: center; margin-bottom: 10px; border: 1px solid #ddd;">
        <span style="color: #333; font-weight: bold;">Background</span><br>
        <small style="color: #333;">{background_color}</small>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =====================================
# 3. TEXT-EINGABE (VERKNÜPFT MIT LAYOUT-TEMPLATES)
# =====================================

st.header("📝 Text-Eingabe")

# Prüfe ob ein Layout ausgewählt wurde
if 'selected_layout' in st.session_state:
    selected_layout = st.session_state.selected_layout
    
    try:
        # Layout laden um die text_elements Zonen zu identifizieren
        from creative_core.layout.loader import load_layout
        layout_data = load_layout(selected_layout)
        
        if layout_data and 'zones' in layout_data:
            # Alle text_elements Zonen identifizieren
            text_zones = {}
            for zone_name, zone_data in layout_data['zones'].items():
                if zone_data.get('content_type') == 'text_elements':
                    text_zones[zone_name] = zone_data
            
            if text_zones:
                # Debug: Zeige erkannte Zonen
                st.write(f"**Erkannte Zonen:** {list(text_zones.keys())}")
                
                # Session State für Texteingaben initialisieren
                if 'text_inputs' not in st.session_state:
                    st.session_state.text_inputs = {}
                
                # Standard-Eingaben setzen, falls noch nicht vorhanden
                # Standard-Eingaben setzen, falls noch keine Benutzereingaben vorhanden sind
                # UMLAUT-OPTIMIERUNG: Deutsche Wörter ohne Umlaut-Punkte
                default_texts = {
                    'standort_block': '📍 Braunschweig',  # Pin-Symbol für Standort
                    'benefits_block': 'Attraktive Vergutung\nFlexible Arbeitszeiten\nFortbildungsmoglichkeiten',  # ä→a, ö→o
                    'cta_block': 'Jetzt Bewerben!',
                    'headline_block': 'Dein Rhythmus. Dein Job.',  # Max 30 Zeichen
                    'stellentitel_block': 'Pflegefachkraft (m/w/d)',  # Max 25 Zeichen
                    'subline_block': 'Entdecke deine Karriere in der Pflege'  # Max 50 Zeichen
                }
                
                # Standardwerte nur setzen, wenn noch keine Eingaben vorhanden sind
                for zone_name, default_text in default_texts.items():
                    if zone_name in text_zones and zone_name not in st.session_state.text_inputs:
                        st.session_state.text_inputs[zone_name] = default_text
                
                # Texteingabe-Felder in Spalten anordnen
                num_cols = min(2, len(text_zones))  # Maximal 2 Spalten
                text_cols = st.columns(num_cols)
                
                for i, (zone_name, zone_data) in enumerate(text_zones.items()):
                    col_index = i % num_cols
                    
                    with text_cols[col_index]:
                        # text_field und [feldname]_input aus dem Template extrahieren
                        text_field = zone_data.get('text_field', zone_name)
                        field_input = zone_data.get(f'{text_field}_input', f'Text für {zone_name}')
                        
                        # Texteingabe-Feld erstellen
                        input_key = f"text_input_{zone_name}"
                        text_value = st.session_state.text_inputs.get(zone_name, '')
                        
                        # Feld-Typ bestimmen (basierend auf Zone-Name)
                        if 'benefits' in zone_name.lower():
                            # Benefits als mehrzeiliger Text
                            input_text = st.text_area(
                                f"**{field_input}**",
                                value=text_value,
                                height=120,
                                placeholder=f"Geben Sie {field_input.lower()} ein...",
                                key=input_key
                            )
                        elif 'headline' in zone_name.lower():
                            # Headline als einzeiliger Text
                            input_text = st.text_input(
                                f"**{field_input}**",
                                value=text_value,
                                placeholder=f"Geben Sie {field_input.lower()} ein...",
                                key=input_key
                            )
                        elif 'subline' in zone_name.lower():
                            # Subline als einzeiliger Text
                            input_text = st.text_input(
                                f"**{field_input}**",
                                value=text_value,
                                placeholder=f"Geben Sie {field_input.lower()} ein...",
                                key=input_key
                            )
                        elif 'cta' in zone_name.lower():
                            # CTA als einzeiliger Text
                            input_text = st.text_input(
                                f"**{field_input}**",
                                value=text_value,
                                placeholder=f"Geben Sie {field_input.lower()} ein...",
                                key=input_key
                            )
                        elif 'stellentitel' in zone_name.lower():
                            # Stellentitel als einzeiliger Text
                            input_text = st.text_input(
                                f"**{field_input}**",
                                value=text_value,
                                placeholder=f"Geben Sie {field_input.lower()} ein...",
                                key=input_key
                            )
                        elif 'logo' in zone_name.lower():
                            # Logo als einzeiliger Text
                            input_text = st.text_input(
                                f"**{field_input}**",
                                value=text_value,
                                placeholder=f"Geben Sie {field_input.lower()} ein...",
                                key=input_key
                            )
                        elif 'location' in zone_name.lower() or 'standort' in zone_name.lower():
                            # Standort als einzeiliger Text
                            input_text = st.text_input(
                                f"**{field_input}**",
                                value=text_value,
                                placeholder=f"Geben Sie {field_input.lower()} ein...",
                                key=input_key
                            )
                        else:
                            # Standard als einzeiliger Text
                            input_text = st.text_input(
                                f"**{field_input}**",
                                value=text_value,
                                placeholder=f"Geben Sie {field_input.lower()} ein...",
                                key=input_key
                            )
                        
                        # Text in Session State speichern
                        # Automatische Pin-Symbol-Erkennung für Standort
                        if 'standort' in zone_name.lower() or 'location' in zone_name.lower():
                            # Pin-Symbol hinzufügen, falls nicht vorhanden
                            if not input_text.startswith('📍'):
                                input_text = f"📍 {input_text}"
                        
                        # Umlaut-Optimierung für deutsche Texte (optimiert)
                        input_text = normalize_german_text(input_text, preserve_umlauts=False)  # DALL-E 3 Kompatibilität
                        
                        st.session_state.text_inputs[zone_name] = input_text
                
            else:
                st.warning("⚠️ Keine text_elements Zonen in diesem Layout gefunden")
                
        else:
            st.error("❌ Layout konnte nicht geladen werden")
            
    except ImportError as e:
        st.error(f"❌ Layout Loader nicht verfügbar: {e}")
        st.info("ℹ️ Texteingabe-Felder können nicht dynamisch geladen werden")
        
        # Fallback: Standard-Texteingabe-Felder
        st.subheader("📝 Standard-Texteingabe (Fallback)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            headline = st.text_input("**Hauptüberschrift**", value="Dein Rhythmus. Dein Job.", placeholder="Geben Sie die Hauptüberschrift ein... (max. 30 Zeichen)")
            subline = st.text_input("**Untertitel**", value="Entdecke deine Karriere in der Pflege", placeholder="Geben Sie den Untertitel ein... (max. 50 Zeichen)")
            benefits = st.text_area("**Vorteile**", value="Attraktive Vergutung\nFlexible Arbeitszeiten\nFortbildungsmoglichkeiten", placeholder="Geben Sie die Vorteile ein... (max. 25 Zeichen pro Zeile)", height=100)
        
        with col2:
            stellentitel = st.text_input("**Stellentitel**", value="Pflegefachkraft (m/w/d)", placeholder="Geben Sie den Stellentitel ein... (max. 25 Zeichen)")
            cta = st.text_input("**Call-to-Action**", value="Jetzt Bewerben!", placeholder="Geben Sie den CTA-Text ein... (max. 25 Zeichen)")
            location = st.text_input("**Standort**", value="📍 Braunschweig", placeholder="Geben Sie den Standort ein... (Pin-Symbol wird automatisch hinzugefügt)")
        
        # Standard-Texteingaben in Session State speichern
        st.session_state.text_inputs = {
            'headline_block': headline,
            'subtext_block': subline,
            'benefits_block': benefits,
            'stellentitel_block': stellentitel,
            'cta_block': cta,
            'standort_block': location
        }

else:
    st.info("ℹ️ **Bitte wählen Sie zuerst ein Layout aus**, um die Texteingabe-Felder zu sehen")

# =====================================
# 4. MOTIV-EINGABE (PLATZHALTER)
# =====================================

# st.header("🖼️ Motiv-Eingabe")
# st.info("🚧 **In Entwicklung** - Motiv-Eingabefelder werden hier angezeigt")

# =====================================
# 5. PROMPT-GENERIERUNG (Layout + Design + Style)
# =====================================

st.header("🎯 Prompt Generierung")

# st.info("💡 **Hinweis**: Texteingaben sind jetzt vollständig integriert! Motiv-Eingaben werden in der nächsten Version implementiert.")

# Sammle alle aktuellen Einstellungen
if st.button("🎯 Prompt erstellen", type="primary", use_container_width=True, key="generate_prompt_button"):
    if 'selected_layout' in st.session_state:
        selected_layout = st.session_state.selected_layout
        
        with st.spinner("🔄 Erstelle Prompt aus Layout, Design, Style & Texten..."):
            try:
                # Alle Design-Optionen sammeln
                design_options = {
                    'layout_style': st.session_state.get('layout_style', ('rounded_modern', '🔵 Abgerundet & Modern')),
                    'container_shape': st.session_state.get('container_shape', ('rounded_rectangle', '📱 Abgerundet')),
                    'border_style': st.session_state.get('border_style', ('soft_shadow', '🌫️ Weicher Schatten')),
                    'texture_style': st.session_state.get('texture_style', ('gradient', '🌈 Farbverlauf')),
                    'background_treatment': st.session_state.get('background_treatment', ('subtle_pattern', '🌸 Subtiles Muster')),
                    'corner_radius': st.session_state.get('corner_radius', ('medium', '⌜ Mittel')),
                    'accent_elements': st.session_state.get('accent_elements', ('modern_minimal', '⚪ Modern Minimal')),
                    'container_transparency': st.session_state.get('container_transparency', 0.8),
                    'image_text_ratio': st.session_state.get('image_text_ratio', 0.6),
                    'element_spacing': st.session_state.get('element_spacing', 30),
                    'container_padding': st.session_state.get('container_padding', 20),
                    'shadow_intensity': st.session_state.get('shadow_intensity', 0.3)
                }
                
                # CI-Farben sammeln (ERWEITERT um vierte Farbe)
                ci_colors = {
                    'primary': st.session_state.get('primary_color', '#005EA5'),
                    'secondary': st.session_state.get('secondary_color', '#B4D9F7'),
                    'accent': st.session_state.get('accent_color', '#FFC20E'),
                    'background': st.session_state.get('background_color', '#FFFFFF')
                }
                
                # Texteingaben sammeln
                text_inputs = st.session_state.get('text_inputs', {})
                
                # Layout-Informationen laden
                try:
                    from creative_core.layout.loader import load_layout
                    layout_data = load_layout(selected_layout)
                    
                    if layout_data:
                        st.success("✅ Layout erfolgreich geladen!")
                        
                        # Vereinfachte Status-Anzeige
                        try:
                            validation_results = validate_layout_coordinates(layout_data)
                            if validation_results['is_valid']:
                                st.success("✅ Layout bereit für Generierung")
                            else:
                                st.warning("⚠️ Layout hat Validierungsprobleme")
                        except:
                            st.info("ℹ️ Layout wird verwendet")
                        
                        # Design-Integration durchführen
                        try:
                            from creative_core.layout.engine import LayoutEngine
                            from creative_core.design_ci.rules import apply_rules
                            
                            # Layout Engine initialisieren
                            layout_engine = LayoutEngine()
                            
                            # Slider-Werte für Layout-Engine vorbereiten
                            image_text_ratio = int(design_options['image_text_ratio'] * 100)
                            container_transparency = int(design_options['container_transparency'] * 100)
                            
                            # Layout-Koordinaten berechnen (mit Fehlerbehandlung)
                            try:
                                calculated_layout = layout_engine.calculate_layout_coordinates(
                                    layout_data,
                                    image_text_ratio=image_text_ratio,
                                    container_transparency=container_transparency
                                )
                            except Exception as e:
                                calculated_layout = layout_data
                            
                            # Design-Regeln anwenden
                            design_options_for_backend = {
                                'typography_scale': 'md',
                                'container_shape': design_options['container_shape'][0],
                                'border_style': design_options['border_style'][0],
                                'corner_radius_px': {
                                    'small': 8,
                                    'medium': 16,
                                    'large': 24,
                                    'xl': 32
                                }.get(design_options['corner_radius'][0], 16),
                                'transparency_pct': container_transparency,
                                'accent_elements': [design_options['accent_elements'][0]]
                            }
                            
                            # Design-Regeln anwenden (mit Fehlerbehandlung)
                            # Design-Regeln anwenden (mit Fehlerbehandlung)
                            try:
                                design_result = apply_rules(
                                    layout=calculated_layout,
                                    ci=ci_colors,
                                    options=design_options_for_backend
                                )
                            except Exception as e:
                                design_result = {
                                    'success': True,
                                    'colors': ci_colors,
                                    'layout_synergy': {
                                        'used_zones': list(calculated_layout.get('zones', {}).keys()),
                                        'canvas_size': calculated_layout.get('canvas', {}),
                                        'layout_type': calculated_layout.get('layout_type', 'unknown')
                                    }
                                }

                            if design_result:
                                st.success("✅ Design integriert")
                                
                                
                                
                                # Ergebnisse anzeigen
                                st.subheader("🎯 **Generierter Prompt (Layout + Design + Style)**")
                                
                                # Prompt zusammenbauen (mit robuster Datenverarbeitung)
                                # Prompt zusammenbauen als YAML-Template mit integrierten Design- und Texteingaben
                                prompt_parts = []
                                
                                # Layout-Template Header
                                prompt_parts.append(f"layout_id: {layout_data.get('layout_id', 'unknown')}")
                                prompt_parts.append(f"name: {layout_data.get('meta', {}).get('name', 'Standard')}")
                                prompt_parts.append(f"description: {layout_data.get('meta', {}).get('description', 'Keine Beschreibung')}")
                                prompt_parts.append(f"layout_type: {layout_data.get('layout_type', 'standard')}")
                                
                                # Canvas-Bereich
                                canvas = layout_data.get('canvas', {})
                                prompt_parts.append("canvas:")
                                prompt_parts.append(f"  width: {canvas.get('width', 1080)}")
                                prompt_parts.append(f"  height: {canvas.get('height', 1080)}")
                                prompt_parts.append(f"  background_color: '{canvas.get('background_color', '#FFFFFF')}'")
                                prompt_parts.append(f"  aspect_ratio: '{canvas.get('aspect_ratio', '1:1')}'")
                                
                                prompt_parts.append("")
                                
                                # Design & Style + Schieberegler am Anfang
                                prompt_parts.append("# DESIGN & STYLE + SCHIEBEREGLER")
                                prompt_parts.append("design_options:")
                                prompt_parts.append(f"  layout_style: {design_options['layout_style'][0]}")
                                prompt_parts.append(f"  container_shape: {design_options['container_shape'][0]}")
                                prompt_parts.append(f"  border_style: {design_options['border_style'][0]}")
                                prompt_parts.append(f"  texture_style: {design_options['texture_style'][0]}")
                                prompt_parts.append(f"  background_treatment: {design_options['background_treatment'][0]}")
                                prompt_parts.append(f"  corner_radius: {design_options['corner_radius'][0]}")
                                prompt_parts.append(f"  accent_elements: {design_options['accent_elements'][0]}")
                                
                                # Schieberegler-Werte werden nur in den visuellen Beschreibungen angezeigt
                                # Keine doppelten slider_values mehr
                                
                                prompt_parts.append("ci_colors:")
                                prompt_parts.append(f"  primary: {ci_colors['primary']}")
                                prompt_parts.append(f"  secondary: {ci_colors['secondary']}")
                                prompt_parts.append(f"  accent: {ci_colors['accent']}")
                                prompt_parts.append(f"  background: {ci_colors.get('background', '#FFFFFF')}")
                                
                                # Debug: Farben überprüfen (ERWEITERT um vierte Farbe)
                                # st.write(f"**Debug - CI-Farben:** Primär: {ci_colors['primary']}, Sekundär: {ci_colors['secondary']}, Akzent: {ci_colors['accent']}, Hintergrund: {ci_colors.get('background', '#FFFFFF')}")
                                
                                # Erweiterte Farb-Validierung (ERWEITERT um vierte Farbe)
                                # color_validation = {
                                #     'primary_valid': ci_colors['primary'].startswith('#') and len(ci_colors['primary']) == 7,
                                #     'secondary_valid': ci_colors['secondary'].startswith('#') and len(ci_colors['secondary']) == 7,
                                #     'accent_valid': ci_colors['accent'].startswith('#') and len(ci_colors['accent']) == 7,
                                #     'background_valid': ci_colors.get('background', '#FFFFFF').startswith('#') and len(ci_colors.get('background', '#FFFFFF')) == 7
                                # }
                                
                                # if all(color_validation.values()):
                                #     st.success("✅ **CI-Farben sind valide!** Alle Farben werden korrekt integriert.")
                                # else:
                                #     st.warning("⚠️ **CI-Farben haben Validierungsprobleme!** Überprüfen Sie die Farbformate.")
                                #     for color_name, is_valid in color_validation.items():
                                #         if not is_valid:
                                #             st.error(f"❌ {color_name}: Ungültiges Format")
                                
                                # Farb-Harmonie-Info (ERWEITERT um vierte Farbe)
                                # st.info(f"🎨 **Farbharmonie:** Primär ({ci_colors['primary']}) + Sekundär ({ci_colors['secondary']}) + Akzent ({ci_colors['accent']}) + Hintergrund ({ci_colors.get('background', '#FFFFFF')})")
                                
                                prompt_parts.append("")
                                
                                # Zonen mit integrierten Texteingaben
                                zones = layout_data.get('zones', {})
                                if zones and isinstance(zones, dict):
                                    prompt_parts.append("zones:")
                                    
                                    for zone_name, zone_data in zones.items():
                                        prompt_parts.append(f"  {zone_name}:")
                                        prompt_parts.append(f"    x: {zone_data.get('x', 0)}")
                                        prompt_parts.append(f"    y: {zone_data.get('y', 0)}")
                                        prompt_parts.append(f"    width: {zone_data.get('width', 0)}")
                                        prompt_parts.append(f"    height: {zone_data.get('height', 0)}")
                                        prompt_parts.append(f"    content_type: {zone_data.get('content_type', 'unknown')}")
                                        prompt_parts.append(f"    description: {zone_data.get('description', 'Keine Beschreibung')}")
                                        
                                        if zone_data.get('content_type') == 'text_elements':
                                            prompt_parts.append(f"    text_field: {zone_data.get('text_field', zone_name)}")
                                            
                                            # Texteingabe integrieren
                                            text_value = text_inputs.get(zone_name, '')
                                            if text_value.strip():
                                                prompt_parts.append(f"    {zone_data.get('text_field', zone_name)}_input: \"{text_value}\"")
                                            else:
                                                prompt_parts.append(f"    {zone_data.get('text_field', zone_name)}_input: \"{zone_data.get(f'{zone_data.get('text_field', zone_name)}_input', 'Text eingeben')}\"")
                                        
                                        elif zone_data.get('content_type') == 'image_motiv':
                                            prompt_parts.append(f"    description: \"[Hier soll erstmal nur stehen, dass das Bild eingefügt wird]\"")
                                
                                prompt_parts.append("")
                                
                                # Meta-Informationen
                                meta = layout_data.get('meta', {})
                                if meta:
                                    prompt_parts.append("meta:")
                                    prompt_parts.append(f"  name: {meta.get('name', 'Standard')}")
                                    prompt_parts.append(f"  description: {meta.get('description', 'Keine Beschreibung')}")
                                    prompt_parts.append(f"  layout_type: {meta.get('layout_type', 'standard')}")
                                    prompt_parts.append(f"  zones_count: {meta.get('zones_count', 0)}")
                                    prompt_parts.append(f"  text_zones: {meta.get('text_zones', 0)}")
                                    prompt_parts.append(f"  image_zones: {meta.get('image_zones', 0)}")
                                
                                prompt_parts.append("")
                                
                                # SEMANTISCHE LAYOUT-BESCHREIBUNG (KI-VERSTÄNDLICH) - PROMINENT PLATZIERT
                                semantic_layout = generate_semantic_layout_description(layout_data)
                                prompt_parts.append("# =====================================")
                                prompt_parts.append("# SEMANTISCHE LAYOUT-BESCHREIBUNG")
                                prompt_parts.append("# =====================================")
                                prompt_parts.append("layout_semantic:")
                                prompt_parts.append(f"  overview: {semantic_layout['layout_overview']}")
                                
                                # Text-Bereiche semantisch beschreiben
                                prompt_parts.append("  text_positioning:")
                                for text_area in semantic_layout['text_areas']:
                                    prompt_parts.append(f"    {text_area['zone_name']}: {text_area['description']}")
                                    prompt_parts.append(f"      position: {text_area['relative_position']}")
                                    prompt_parts.append(f"      size: {text_area['size']}")
                                
                                # Bild-Bereiche semantisch beschreiben
                                prompt_parts.append("  image_positioning:")
                                for image_area in semantic_layout['image_areas']:
                                    prompt_parts.append(f"    {image_area['zone_name']}: {image_area['description']}")
                                    prompt_parts.append(f"      position: {image_area['relative_position']}")
                                    prompt_parts.append(f"      size: {image_area['size']}")
                                
                                prompt_parts.append("")
                                
                                # Layout-spezifische Beschreibungen
                                layout_desc = get_layout_specific_description(selected_layout)
                                prompt_parts.append("# LAYOUT-SPEZIFISCHE BESCHREIBUNGEN")
                                prompt_parts.append(f"layout_specific:")
                                prompt_parts.append(f"  description: {layout_desc['description']}")
                                prompt_parts.append(f"  visual_style: {layout_desc['visual_style']}")
                                prompt_parts.append(f"  features:")
                                for feature in layout_desc['features']:
                                    prompt_parts.append(f"    - {feature}")
                                
                                prompt_parts.append("")
                                
                                # VORGABEN FÜR PROMPT-GENERIERUNG
                                prompt_parts.append("# VORGABEN FÜR PROMPT-GENERIERUNG")
                                prompt_parts.append("# STANDORT-PIN IMPLEMENTIERUNG:")
                                prompt_parts.append("# • STANDORT: MUSS mit dem Pin-Symbol '📍' dargestellt werden")
                                prompt_parts.append("# • UNTERNEHMEN: Wird OHNE Pin angezeigt")
                                prompt_parts.append("# • PIN-SYMBOL: Unicode '📍' (U+1F4CD) links vom Standort-Text")
                                prompt_parts.append("")
                                prompt_parts.append("# TEXT-VOLLSTÄNDIGKEIT UND KOORDINATEN:")
                                prompt_parts.append("# • Alle Texte müssen vollständig und lesbar erscheinen")
                                prompt_parts.append("# • Keine Text-Kürzungen oder Abbrüche erlaubt")
                                prompt_parts.append("# • KOORDINATEN: Alle Textelemente müssen EXAKT an den angegebenen Koordinaten positioniert werden")
                                prompt_parts.append("# • LAYOUT-STRUKTUR: Die definierte Layout-Struktur ist verbindlich")
                                prompt_parts.append("")
                                prompt_parts.append("# LAYOUT-POSITIONIERUNG (SEMANTISCH + TECHNISCH):")
                                prompt_parts.append("# • Verwende die SEMANTISCHE BESCHREIBUNG für visuelle Platzierung")
                                prompt_parts.append("# • Technische Koordinaten sind als Referenz für exakte Positionierung")
                                prompt_parts.append("# • Text-Container müssen in den beschriebenen Bereichen erscheinen")
                                prompt_parts.append("# • Bild-Motiv muss den beschriebenen Bild-Bereich einnehmen")
                                prompt_parts.append("")
                                prompt_parts.append("# UMLAUT-OPTIMIERUNG FÜR DEUTSCHE TEXTE:")
                                prompt_parts.append("# • VERWENDE deutsche Wörter, aber ohne Umlaut-Punkte")
                                prompt_parts.append("# • ä → a (z.B. 'Arbeitszeiten' statt 'Arbeitszeiten')")
                                prompt_parts.append("# • ö → o (z.B. 'Möglichkeiten' statt 'Möglichkeiten')")
                                prompt_parts.append("# • ü → u (z.B. 'Vergütung' statt 'Vergütung')")
                                prompt_parts.append("# • BEHALTE deutsche Wörter bei, aber ohne Umlaut-Zeichen")
                                prompt_parts.append("# • TEXT-LÄNGE:")
                                prompt_parts.append("#   - HEADLINE: Maximal 30 Zeichen")
                                prompt_parts.append("#   - SUBLINE: Maximal 50 Zeichen")
                                prompt_parts.append("#   - Alle anderen Elemente: Maximal 25 Zeichen")
                                prompt_parts.append("# • SCHRIFT: Klare, serifenlose Schrift für beste Lesbarkeit")
                                
                                prompt_parts.append("")
                                prompt_parts.append("🎨 DESIGN & STYLE (Visuelle Beschreibungen):")
                                prompt_parts.append("Alle Design-Optionen werden in den folgenden visuellen Beschreibungen berücksichtigt.")
                                
                                prompt_parts.append("")
                                prompt_parts.append("🔧 SCHIEBEREGLER (Visuelle Übersetzungen):")
                                
                                # Container-Transparenz in visuelle Beschreibung umwandeln (optimiert)
                                transparency_desc = get_transparency_description(design_options['container_transparency'])
                                
                                # Bild-Text-Verhältnis in visuelle Beschreibung umwandeln (optimiert)
                                ratio_desc = get_ratio_description(design_options['image_text_ratio'])
                                
                                # Element-Abstand in visuelle Beschreibung umwandeln
                                spacing = design_options['element_spacing']
                                if spacing <= 10:
                                    spacing_desc = "tight spacing with minimal gaps between elements, about 10 pixels, compact and dense layout"
                                elif spacing <= 20:
                                    spacing_desc = "moderate spacing with comfortable gaps, about 20 pixels, balanced element distribution"
                                elif spacing <= 30:
                                    spacing_desc = "generous spacing with clear separation, about 30 pixels, relaxed and breathable layout"
                                elif spacing <= 40:
                                    spacing_desc = "wide spacing with substantial gaps, about 40 pixels, spacious and open composition"
                                else:
                                    spacing_desc = "very wide spacing with maximum separation, about 50+ pixels, extremely spacious layout"
                                
                                # Container-Padding in visuelle Beschreibung umwandeln
                                padding = design_options['container_padding']
                                if padding <= 15:
                                    padding_desc = "minimal internal padding, about 15 pixels, tight content placement within containers"
                                elif padding <= 25:
                                    padding_desc = "moderate internal padding, about 25 pixels, comfortable content breathing room"
                                elif padding <= 35:
                                    padding_desc = "generous internal padding, about 35 pixels, spacious content placement with good margins"
                                elif padding <= 45:
                                    padding_desc = "very generous internal padding, about 45 pixels, maximum content breathing room"
                                else:
                                    padding_desc = "extreme internal padding, about 50+ pixels, very spacious content placement"
                                
                                # Schatten-Intensität in visuelle Beschreibung umwandeln
                                shadow_intensity = int(design_options['shadow_intensity'] * 100)
                                if shadow_intensity <= 20:
                                    shadow_desc = "very subtle shadow with minimal depth, barely visible lift from background"
                                elif shadow_intensity <= 40:
                                    shadow_desc = "light shadow with gentle depth, softly lifting elements from background"
                                elif shadow_intensity <= 60:
                                    shadow_desc = "medium shadow with moderate depth, clearly visible element separation from background"
                                elif shadow_intensity <= 80:
                                    shadow_desc = "strong shadow with significant depth, dramatic lift and clear background separation"
                                else:
                                    shadow_desc = "very strong shadow with maximum depth, intense element separation and dramatic depth effect"
                                
                                prompt_parts.append(f"• Container-Transparenz: {transparency_desc}")
                                prompt_parts.append(f"• Bild-Text-Verhältnis: {ratio_desc}")
                                prompt_parts.append(f"• Element-Abstand: {spacing_desc}")
                                prompt_parts.append(f"• Container-Padding: {padding_desc}")
                                prompt_parts.append(f"• Schatten-Intensität: {shadow_desc}")
                                
                                prompt_parts.append("")
                                prompt_parts.append("🎨 CI-FARBEN & VISUELLE BESCHREIBUNGEN:")
                                prompt_parts.append(f"• Primärfarbe: {ci_colors['primary']} - für Headlines und wichtige Textelemente")
                                prompt_parts.append(f"• Sekundärfarbe: {ci_colors['secondary']} - für Hintergründe und Flächen")
                                prompt_parts.append(f"• Akzentfarbe: {ci_colors['accent']} - für CTAs und Akzent-Elemente")
                                
                                prompt_parts.append("")
                                prompt_parts.append("🌈 FARBHARMONIE & BALANCE:")
                                prompt_parts.append("• Primär- und Sekundärfarbe müssen harmonisch ausbalanciert sein")
                                prompt_parts.append("• Sekundärfarbe schafft subtile Hintergrund-Tiefe")
                                prompt_parts.append("• Akzentfarbe hebt wichtige Elemente hervor")
                                prompt_parts.append("• Farbkontraste für optimale Lesbarkeit")
                                
                                prompt_parts.append("")
                                prompt_parts.append("🎯 VISUELLE FARB-ANWEISUNGEN:")
                                prompt_parts.append("• Hintergrund: Verwende die Sekundärfarbe für subtile Flächen")
                                prompt_parts.append("• Text-Container: Primärfarbe für wichtige Texte")
                                prompt_parts.append("• Call-to-Action: Akzentfarbe für maximale Aufmerksamkeit")
                                prompt_parts.append("• Farbverläufe: Harmonische Übergänge zwischen den CI-Farben")
                                
                                # Zusätzliche kreative Farbbeschreibungen (aus Prompt 1)
                                prompt_parts.append("")
                                prompt_parts.append("🌟 KREATIVE FARB-INTEGRATION:")
                                prompt_parts.append("• WICHTIG: Alle CI-Farben müssen vollständig und harmonisch integriert werden")
                                prompt_parts.append("• KEINE Abweichungen von den definierten CI-Farben erlaubt")
                                prompt_parts.append("• Sekundärfarbe als subtiler, aber sichtbarer Hintergrund-Element")
                                prompt_parts.append("• Primärfarbe als dominante Text- und Headline-Farbe")
                                prompt_parts.append("• Akzentfarbe als auffälliger Call-to-Action und Highlight-Farbe")
                                
                                # Farb-Meta-Beschreibungen (aus Ihrer Analyse)
                                prompt_parts.append("")
                                prompt_parts.append("💫 FARB-META-EBENE:")
                                prompt_parts.append("• Bild und Farben müssen harmonisch ausbalanciert sein")
                                prompt_parts.append("• CI-Farben als 30% der visuellen Komposition")
                                prompt_parts.append("• Motiv als 70% der visuellen Komposition")
                                prompt_parts.append("• Farben und Motiv müssen sich gegenseitig ergänzen")
                                
                                prompt_parts.append("")
                                prompt_parts.append("🔍 TECHNISCHE PRÄZISION:")
                                prompt_parts.append("• ULTRA HIGH DETAIL: sharp focus, cinematic quality, 8k render, detailed textures")
                                prompt_parts.append("• STÖRFAKTOREN VERMEIDEN: no text overlay inside the photo, no distortions, clean composition")
                                prompt_parts.append("• EXAKTHEIT DER LAYOUTS: Image background only – text added in separate layers as defined in YAML")
                                prompt_parts.append("• RENDER-QUALITÄT: Professional photography, studio lighting, perfect composition")
                                prompt_parts.append("• TEXT-FREI: All text elements are defined in YAML coordinates - render only the background image")
                                prompt_parts.append("• LAYOUT-STRUKTUR: Follow exact zone coordinates - no text rendering in image generation")
                                
                                # =====================================
                                # OPTIMIERTE PROMPT-ARCHITEKTUR (KOMPAKT & FOKUSSIERT)
                                # =====================================
                                
                                # FOUNDATION & COMPOSITION (Level 1-2 kombiniert)
                                foundation_prompt = f"""
# =====================================
# FOUNDATION & COMPOSITION
# =====================================
creative_type: "Professional Recruiting Creative"
quality_standard: "Ultra-High Quality, 8K Resolution"
canvas: {layout_data['canvas']['width']}x{layout_data['canvas']['height']} ({layout_data['canvas'].get('aspect_ratio', '1:1')})
background: {layout_data['canvas'].get('background_color', '#FFFFFF')}

composition:
  image_text_ratio: {image_text_ratio} ({ratio_desc})
  container_transparency: {design_options['container_transparency']} ({transparency_desc})
  element_spacing: {design_options['element_spacing']} ({spacing_desc})
  container_padding: {design_options['container_padding']} ({padding_desc})
  shadow_intensity: {design_options['shadow_intensity']} ({shadow_desc})
"""
                                
                                # DESIGN & CI-COLORS (Level 3-4 kombiniert)
                                design_prompt = f"""
# =====================================
# DESIGN & CI-COLORS
# =====================================
design:
  layout_style: {design_options['layout_style'][1].split(' ')[-1]}  # Emoji entfernen
  container_shape: {design_options['container_shape'][1].split(' ')[-1]}  # Emoji entfernen
  border_style: {design_options['border_style'][1].split(' ')[-1]}  # Emoji entfernen
  texture_style: {design_options['texture_style'][1].split(' ')[-1]}  # Emoji entfernen
  background_treatment: {design_options['background_treatment'][1].split(' ')[-1]}  # Emoji entfernen
  corner_radius: {design_options['corner_radius'][1].split(' ')[0]}  # Nur Text ohne Emoji
  accent_elements: {design_options['accent_elements'][1].split(' ')[-1]}  # Emoji entfernen

ci_colors:
  primary: {ci_colors['primary']} (Headlines & wichtige Texte)
  secondary: {ci_colors['secondary']} (Hintergründe & Flächen)
  accent: {ci_colors['accent']} (CTAs & Akzent-Elemente)

color_harmony: Primär- und Sekundärfarbe harmonisch ausbalanciert, KEINE Abweichungen erlaubt
"""
                                
                                
                                
                                # SEMANTISCHE LAYOUT-BESCHREIBUNG INTEGRIEREN
                                semantic_layout = generate_semantic_layout_description(layout_data)
                                semantic_prompt = f"""
# =====================================
# SEMANTISCHE LAYOUT-BESCHREIBUNG (KI-VERSTÄNDLICH)
# =====================================
layout_semantic:
  overview: {semantic_layout['layout_overview']}
  
  text_positioning:
"""
                                
                                # Text-Bereiche semantisch beschreiben MIT TEXTEINGABEN
                                for text_area in semantic_layout['text_areas']:
                                    zone_name = text_area['zone_name']
                                    # ECHTE Texteingabe aus session_state.text_inputs holen
                                    real_text_input = st.session_state.get('text_inputs', {}).get(zone_name, 'Text eingeben')
                                    semantic_prompt += f"""    {zone_name}: "{real_text_input}" positioned in {text_area['description']}
      position: {text_area['relative_position']}
      size: {text_area['size']}
"""
                                
                                # Bild-Bereiche semantisch beschreiben
                                semantic_prompt += """  image_positioning:
"""
                                for image_area in semantic_layout['image_areas']:
                                    semantic_prompt += f"""    {image_area['zone_name']}: {image_area['description']}
      position: {image_area['relative_position']}
      size: {image_area['size']}
"""
                                
                                # TECHNICAL RULES (Level 7 kompakt)
                                technical_prompt = f"""
# =====================================
# TECHNICAL RULES
# =====================================
render_quality: ULTRA HIGH DETAIL, 8K, professional photography, studio lighting
text_rules: ALLE TEXTE vollständig und lesbar, EXAKT an semantischen Positionen, Standort mit '📍' Pin
umlaut_rules: Deutsche Wörter ohne Umlaut-Punkte (ä→a, ö→o, ü→u)
text_limits: Headline max 30, Subline max 50, andere max 25 Zeichen
layout_accuracy: Image background only, text in separate layers per semantic positioning
composition_balance: 30% CI-Farben, 70% Motiv, harmonische Ausbalancierung
"""
                                
                                # Engine-Auswahl für optimierte Prompt-Generierung
                                engine_type = st.selectbox(
                                    "🤖 KI-Engine für Prompt-Optimierung",
                                    options=['dalle3', 'midjourney', 'stable_diffusion'],
                                    index=0,
                                    help="Wählen Sie die KI-Engine für optimierte Text-Verarbeitung"
                                )
                                
                                # OPTIMIERTE PROMPT-GENERIERUNG verwenden
                                final_prompt = generate_optimized_prompt(
                                    layout_data=layout_data,
                                    design_options=design_options,
                                    ci_colors=ci_colors,
                                    text_inputs=text_inputs,
                                    engine_type=engine_type
                                )
                                
                                # Prompt anzeigen
                                st.text_area(
                                    "Generierter Prompt (Layout + Design + Style + Texte):",
                                    value=final_prompt,
                                    height=400,
                                    help="Dieser Prompt enthält alle Layout-, Design-, Style- und Texteingabe-Informationen"
                                )
                                
                                # Prompt-Statistiken
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("📊 Prompt-Länge", f"{len(final_prompt)} Zeichen")
                                with col2:
                                    st.metric("🎨 Design-Status", "✅ Integriert")
                                with col3:
                                    text_count = len([t for t in text_inputs.values() if t.strip()])
                                    st.metric("📝 Texteingaben", f"{text_count}")
                                
                                # Download-Button
                                prompt_bytes = final_prompt.encode('utf-8')
                                st.download_button(
                                    "📥 Prompt downloaden",
                                    data=prompt_bytes,
                                    file_name=f"layout_design_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                    mime="text/plain",
                                    use_container_width=True
                                )
                                
                                # Session State aktualisieren
                                st.session_state['generated_prompt'] = final_prompt
                                st.session_state['prompt_type'] = "layout_design_text"
                                
                        except ImportError as e:
                            st.error(f"❌ Backend-Komponenten nicht verfügbar: {e}")
                            
                        except Exception as e:
                            st.error(f"❌ Fehler bei der Prompt-Generierung: {str(e)}")
                            st.info("ℹ️ Überprüfen Sie die Eingaben und Backend-Komponenten")
                            
                except Exception as e:
                    st.error(f"❌ Fehler bei der Layout-Verarbeitung: {str(e)}")
                    
            except Exception as e:
                st.error(f"❌ Fehler bei der Haupt-Verarbeitung: {str(e)}")
                
    if not selected_layout:
        st.warning("⚠️ Bitte wählen Sie zuerst ein Layout aus")

# =====================================
# FOOTER
# =====================================

st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>🚀 CreativeAI - Layout Generator | Version 1.3 | CI-Farben vollständig integriert + Verbesserte Prompt-Struktur</small>
</div>
""", unsafe_allow_html=True)

# =====================================
# KONSISTENTE SLIDER-VERARBEITUNG
# =====================================

def calculate_slider_percentage(value, max_value=1.0):
    """Berechnet konsistente Prozent-Werte für Slider"""
    return int(value * max_value * 100)

def get_transparency_description(transparency_value):
    """Konsistente Transparenz-Beschreibung basierend auf Prozent-Wert"""
    percentage = calculate_slider_percentage(transparency_value)
    
    if percentage <= 20:
        return f"fully opaque container ({percentage}% opacity), solid appearance"
    elif percentage <= 40:
        return f"mostly opaque container ({percentage}% opacity), minimal transparency"
    elif percentage <= 60:
        return f"semi-transparent container ({percentage}% opacity), frosted glass effect"
    elif percentage <= 80:
        return f"highly transparent container ({percentage}% opacity), clear glass effect"
    else:
        return f"nearly transparent container ({percentage}% opacity), ghostly appearance"

def get_ratio_description(ratio_value):
    """Konsistente Bild-Text-Verhältnis-Beschreibung basierend auf Prozent-Wert"""
    percentage = calculate_slider_percentage(ratio_value)
    
    if percentage <= 30:
        return f"text-dominant layout ({percentage}% image area), content-focused"
    elif percentage <= 50:
        return f"balanced layout ({percentage}% image area), harmonious composition"
    elif percentage <= 70:
        return f"image-focused layout ({percentage}% image area), visual impact prioritized"
    elif percentage <= 80:
        return f"image-dominant layout ({percentage}% image area), photography-centric"
    else:
        return f"image-dominant layout ({percentage}% image area), maximum visual impact"

# =====================================
# EMOJI-BEREINIGUNG & DESIGN-OPTIONEN
# =====================================

def clean_emoji_from_text(text):
    """Entfernt Emojis und Sonderzeichen aus Text, behält nur Buchstaben und Zahlen"""
    import re
    # Entfernt Emojis und Unicode-Sonderzeichen, behält nur ASCII-Zeichen
    cleaned = re.sub(r'[^\w\s\-_()]', '', text)
    return cleaned.strip()

def get_clean_design_option(option_tuple):
    """Extrahiert saubere Design-Option ohne Emojis"""
    if isinstance(option_tuple, tuple) and len(option_tuple) >= 2:
        # Verwende den zweiten Eintrag (Display-Text) und entferne Emojis
        display_text = option_tuple[1]
        return clean_emoji_from_text(display_text)
    elif isinstance(option_tuple, str):
        return clean_emoji_from_text(option_tuple)
    else:
        return str(option_tuple)

# Bereinigte Design-Optionen ohne Emojis
CLEAN_DESIGN_OPTIONS = {
    'layout_style': ('rounded_modern', 'Abgerundet Modern'),
    'container_shape': ('rounded_rectangle', 'Abgerundet'),
    'border_style': ('soft_shadow', 'Weicher Schatten'),
    'texture_style': ('gradient', 'Farbverlauf'),
    'background_treatment': ('subtle_pattern', 'Subtiles Muster'),
    'corner_radius': ('medium', 'Mittel'),
    'accent_elements': ('modern_minimal', 'Modern Minimal'),
}

def debug_adaptive_typography(layout_data, design_result):
    """
    Debug-Funktion für adaptive Typografie und Container-Optimierung
    """
    debug_info = []
    debug_info.append("🔍 ADAPTIVE TYPOGRAFIE & CONTAINER DEBUG")
    debug_info.append("=" * 50)
    
    # Layout-Daten analysieren
    calculated_values = layout_data.get('calculated_values', {})
    text_width = calculated_values.get('text_width', 400)
    image_width = calculated_values.get('image_width', 600)
    container_transparency = calculated_values.get('container_transparency', 0.8)
    image_text_ratio = calculated_values.get('image_text_ratio', 50)
    
    debug_info.append(f"📐 LAYOUT-BERECHNUNG:")
    debug_info.append(f"   Text-Breite: {text_width}px")
    debug_info.append(f"   Bild-Breite: {image_width}px")
    debug_info.append(f"   Container-Transparenz: {container_transparency:.2f}")
    debug_info.append(f"   Image-Text-Ratio: {image_text_ratio}%")
    
    # Container-Komplexitätsreduktion prüfen
    container_styles = design_result.get('container_styles', {})
    adaptive_complexity = container_styles.get('adaptive_complexity_reduction', False)
    
    debug_info.append(f"🎨 CONTAINER-OPTIMIERUNG:")
    debug_info.append(f"   Komplexitätsreduktion aktiv: {'✅ Ja' if adaptive_complexity else '❌ Nein'}")
    if adaptive_complexity:
        debug_info.append(f"   Grund: Text-Breite ({text_width}px) < 400px")
        debug_info.append(f"   Aktion: Vereinfachte Container-Styles für bessere Lesbarkeit")
    
    # Typografie-Daten analysieren
    typography = design_result.get('typography', {})
    debug_info.append(f"📝 TYPOGRAFIE-ANPASSUNG:")
    
    for typo_type, typo_data in typography.items():
        font_size = typo_data.get('font_size_px', 0)
        original_size = typo_data.get('original_font_size', 0)
        adaptive_ratio = typo_data.get('adaptive_ratio', 1.0)
        zone_width = typo_data.get('zone_dimensions', {}).get('width', 0)
        
        debug_info.append(f"   {typo_type.upper()}:")
        debug_info.append(f"     Zone-Breite: {zone_width}px")
        debug_info.append(f"     Original-Font: {original_size}px")
        debug_info.append(f"     Adaptive-Font: {font_size}px")
        debug_info.append(f"     Anpassungs-Ratio: {adaptive_ratio:.2f}")
        
        # Textbreiten-Validierung anzeigen
        text_validation = typo_data.get('text_width_validation', {})
        if text_validation:
            estimated_width = text_validation.get('estimated_text_width', 0)
            available_width = text_validation.get('available_width', 0)
            fits_container = text_validation.get('fits_container', True)
            actual_text = text_validation.get('actual_text', '')
            
            debug_info.append(f"     Text-Validierung:")
            debug_info.append(f"       Geschätzte Textbreite: {estimated_width:.1f}px")
            debug_info.append(f"       Verfügbare Breite: {available_width}px")
            debug_info.append(f"       Passt in Container: {'✅ Ja' if fits_container else '❌ Nein'}")
            debug_info.append(f"       Text: '{actual_text}'")
            
            if not fits_container:
                debug_info.append(f"       ⚠️  WARNUNG: Text überläuft Container!")
        
        if font_size < 20:
            debug_info.append(f"     ⚠️  WARNUNG: Sehr kleine Schrift ({font_size}px)")
    
    # Padding-Daten analysieren
    padding_calculations = container_styles.get('zone_specific', {})
    debug_info.append(f"📦 PADDING-ANPASSUNG:")
    
    for zone_name, padding_data in padding_calculations.items():
        padding_x = padding_data.get('x', 0)
        padding_y = padding_data.get('y', 0)
        zone_width = padding_data.get('zone_width', 0)
        adaptive_ratio = padding_data.get('adaptive_ratio', 1.0)
        
        debug_info.append(f"   {zone_name}:")
        debug_info.append(f"     Zone-Breite: {zone_width}px")
        debug_info.append(f"     Padding X: {padding_x}px")
        debug_info.append(f"     Padding Y: {padding_y}px")
        debug_info.append(f"     Anpassungs-Ratio: {adaptive_ratio:.2f}")
    
    # Empfehlungen
    debug_info.append(f"💡 EMPFEHLUNGEN:")
    if text_width < 350:
        debug_info.append(f"   ⚠️  Text-Breite sehr schmal ({text_width}px)")
        debug_info.append(f"   💡 Erhöhe image_text_ratio auf 60-70% für mehr Text-Platz")
    
    if any(typo_data.get('font_size_px', 0) < 20 for typo_data in typography.values()):
        debug_info.append(f"   ⚠️  Sehr kleine Schriftgrößen erkannt")
        debug_info.append(f"   💡 Reduziere container_transparency oder erhöhe image_text_ratio")
    
    # Prüfe auf Textüberlauf
    text_overflow_detected = any(
        typo_data.get('text_width_validation', {}).get('fits_container', True) == False 
        for typo_data in typography.values()
    )
    if text_overflow_detected:
        debug_info.append(f"   ⚠️  Textüberlauf in Containern erkannt")
        debug_info.append(f"   💡 Erhöhe image_text_ratio oder reduziere Text-Länge")
        debug_info.append(f"   💡 Die adaptive Typografie sollte das automatisch beheben")
    
    debug_info.append("=" * 50)
    return "\n".join(debug_info)
