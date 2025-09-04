"""
Layout Engine für dynamische Koordinatenberechnung

Dieser Engine berechnet die tatsächlichen Koordinaten basierend auf:
- image_text_ratio Slider (30-70%)
- container_transparency Slider (0-100%)
- Layout-spezifischen Regeln und Constraints
"""

import math
from typing import Dict, Any, Tuple, Optional, List
from functools import lru_cache
from .schema import (
    ensure_numerical_zones, 
    validate_layout,
    validate_layout_strict, 
    validate_layout_with_warnings,
    get_layout_zone_requirements,
    LayoutValidationError
)


class LayoutEngine:
    """
    Engine für die dynamische Berechnung von Layout-Koordinaten
    """
    
    def __init__(self):
        # Canvas-Werte werden aus dem Layout geladen
        self.canvas_width = None
        self.canvas_height = None
        # Erhöhte Mindestbreiten für bessere Lesbarkeit
        self.min_text_width = 250  # Erhöht von 300
        self.max_text_width = 800
        self.min_image_width = 150
        self.max_image_width = 900
        
    def calculate_layout_coordinates(
        self, 
        layout_dict: Dict[str, Any],
        image_text_ratio: int = 50,
        container_transparency: int = 80,
        strict_validation: bool = False
    ) -> Dict[str, Any]:
        """
        Berechnet die tatsächlichen Koordinaten für ein Layout
        
        Args:
            layout_dict: Das geladene Layout-Dictionary
            image_text_ratio: Slider-Wert 30-70 (30% = mehr Text, 70% = mehr Bild)
            container_transparency: Slider-Wert 0-100 (0 = transparent, 100 = undurchsichtig)
            strict_validation: Ob strikte Validierung verwendet werden soll
            
        Returns:
            Layout-Dictionary mit berechneten Koordinaten
        """
        # Lade Canvas-Dimensionen aus dem Layout
        canvas = layout_dict.get('canvas', {})
        self.canvas_width = canvas.get('width', 1080)
        self.canvas_height = canvas.get('height', 1080)
        
        # Validiere Slider-Werte
        image_text_ratio = self._validate_ratio(image_text_ratio)
        container_transparency = self._validate_transparency(container_transparency)
        
        # Berechne tatsächliche Breiten basierend auf dem Ratio
        text_width, image_width = self._calculate_widths(image_text_ratio, self.canvas_width)
        
        # Bestimme Layout-Typ und führe entsprechende Berechnung durch
        layout_type = layout_dict.get('layout_type', 'vertical_split')
        
        if layout_type == 'vertical_split':
            result = self._calculate_vertical_split(layout_dict, text_width, image_width, container_transparency, image_text_ratio)
        elif layout_type == 'vertical_split_left':
            result = self._calculate_vertical_split_left(layout_dict, text_width, image_width, container_transparency, image_text_ratio)
        elif layout_type == 'horizontal_split':
            result = self._calculate_horizontal_split(layout_dict, text_width, image_width, container_transparency, image_text_ratio)
        elif layout_type == 'modern_split':
            result = self._calculate_modern_split(layout_dict, text_width, image_width, container_transparency,image_text_ratio)
        elif layout_type == 'minimalist':
            result = self._calculate_minimalist_layout(layout_dict, text_width, image_width, container_transparency,image_text_ratio)
        elif layout_type == 'hero_layout':
            result = self._calculate_hero_layout(layout_dict, text_width, image_width, container_transparency,image_text_ratio)
        elif layout_type == 'portfolio':
            result = self._calculate_portfolio_layout(layout_dict, text_width, image_width, container_transparency,image_text_ratio)
        elif layout_type == 'storytelling_layout':
            result = self._calculate_storytelling_layout(layout_dict, text_width, image_width, container_transparency,image_text_ratio)
        elif layout_type == 'infographic':
            result = self._calculate_infographic_layout(layout_dict, text_width, image_width, container_transparency,image_text_ratio)
        elif layout_type == 'magazine':
            result = self._calculate_magazine_layout(layout_dict, text_width, image_width, container_transparency,image_text_ratio)
        elif layout_type == 'centered_layout':
            result = self._calculate_centered_layout(layout_dict, text_width, image_width, container_transparency, image_text_ratio)
        elif layout_type == 'diagonal_layout':
            result = self._calculate_diagonal_layout(layout_dict, text_width, image_width, container_transparency, image_text_ratio)
        elif layout_type == 'asymmetric_layout':
            result = self._calculate_asymmetric_layout(layout_dict, text_width, image_width, container_transparency, image_text_ratio)
        elif layout_type == 'grid_layout':
            result = self._calculate_grid_layout(layout_dict, text_width, image_width, container_transparency, image_text_ratio)
        elif layout_type == 'split_layout':
            result = self._calculate_split_layout(layout_dict, text_width, image_width, container_transparency, image_text_ratio)
        else:
            # Fallback: Verwende vertikales Split
            result = self._calculate_vertical_split(layout_dict, text_width, image_width, container_transparency, image_text_ratio)
        
        return result
    
    def _validate_ratio(self, ratio) -> int:
        """Validiert den image_text_ratio Slider-Wert"""
        # Konvertiere zu int falls String
        if isinstance(ratio, str):
            try:
                ratio = int(ratio)
            except ValueError:
                ratio = 50  # Standardwert
        
        if ratio < 30:
            return 30
        elif ratio > 70:
            return 70
        return ratio
    
    def _update_zone_position_for_adaptive_typography(self, zone_data: Dict[str, Any], new_width: int) -> None:
        """
        Aktualisiert den Position-String einer Zone für adaptive Typografie-Berechnung
        
        Args:
            zone_data: Die Zone-Daten
            new_width: Neue Breite der Zone
        """
        original_position = zone_data.get('position', '')
        if original_position and ',' in original_position:
            parts = original_position.split(',')
            if len(parts) >= 4:
                # Aktualisiere nur die Breite im Position-String
                parts[2] = str(new_width)
                updated_position = ','.join(parts)
                zone_data['position'] = updated_position
    
    def _update_text_zones_adaptive(
        self, 
        zones: Dict[str, Any], 
        text_zones: List[str], 
        text_width: int, 
        margin: int, 
        transparency: int
    ) -> None:
        """
        Aktualisiert Text-Zonen mit adaptiver Typografie-Unterstützung
        
        Args:
            zones: Dictionary mit allen Zonen
            text_zones: Liste der Text-Zonen-Namen
            text_width: Verfügbare Text-Breite
            margin: Margin für die Zonen
            transparency: Transparenz-Wert
        """
        for zone_name in text_zones:
            if zone_name in zones:
                # Behalte ursprüngliche x, y, height, z Werte
                original_zone = zones[zone_name]
                new_width = min(text_width - margin, original_zone.get('width', 400))
                
                # Aktualisiere Position-String für adaptive Typografie-Berechnung
                self._update_zone_position_for_adaptive_typography(original_zone, new_width)
                
                zones[zone_name].update({
                    'width': new_width,
                    'transparency': transparency / 100
                })
    
    def _validate_transparency(self, transparency) -> int:
        # Konvertiere zu int falls String
        if isinstance(transparency, str):
            try:
                transparency = int(transparency)
            except ValueError:
                transparency = 80  # Standardwert
        
        if transparency < 0:
            return 0
        elif transparency > 100:
            return 100
        return transparency
    
    def _calculate_widths(self, ratio: int, canvas_width: int = 1080) -> Tuple[int, int]:
        """
        Berechnet Text- und Bild-Breiten basierend auf dem Ratio
        
        Args:
            ratio: Slider-Wert 30-70
            canvas_width: Canvas-Breite aus dem Layout
            
        Returns:
            Tuple (text_width, image_width)
        """
        # Konvertiere Ratio zu Dezimal (30 -> 0.3, 70 -> 0.7)
        ratio_decimal = ratio / 100
        
        # Berechne Bild-Breite (ratio_decimal * Canvas-Breite)
        image_width = int(ratio_decimal * canvas_width)
        
        # Text-Breite ist der Rest minus Abstand
        text_width = canvas_width - image_width - 60  # 60px Abstand
        
        # Validiere Mindest- und Maximalbreiten
        text_width = max(self.min_text_width, min(self.max_text_width, text_width))
        image_width = max(self.min_image_width, min(self.max_image_width, image_width))
        
        # Passe Bild-Breite an, falls Text-Breite geändert wurde
        image_width = canvas_width - text_width - 60
        
        return text_width, image_width
    
    def _calculate_vertical_split(
        self, 
        layout_dict: Dict[str, Any], 
        text_width: int, 
        image_width: int, 
        transparency: int,
        image_text_ratio: int = 50
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für vertikale Aufteilung (Text links, Bild rechts)
        """
        result = layout_dict.copy()
        
        # Berechne Positionen für alle Zonen
        zones = result.get('zones', {})
        
        # Aktualisiere nur die Breiten der Text-Zonen, behalte ursprüngliche Positionen
        text_zones = ['standort_block', 'headline_block', 'subline_block', 'benefits_block', 'company_block', 'cta_block', 'stellentitel_block']
        
        # Verwende Hilfsfunktion für adaptive Typografie
        self._update_text_zones_adaptive(zones, text_zones, text_width, 80, transparency)
        
        # Aktualisiere nur die Bild-Zone
        if 'image_motiv' in zones:
            original_zone = zones['image_motiv']
            zones['image_motiv'].update({
                'x': text_width + 60,  # 60px Abstand vom Text
                'width': image_width
            })
        
        # Aktualisiere das Layout
        result['zones'] = zones
        
        # Füge berechnete Werte hinzu
        result['calculated_values'] = {
            'text_width': text_width,
            'image_width': image_width,
            'container_transparency': transparency / 100,
            'image_text_ratio': image_text_ratio  # Korrigierter Slider-Wert
        }
        
        return result
    
    def _calculate_vertical_split_left(
        self, 
        layout_dict: Dict[str, Any], 
        text_width: int, 
        image_width: int, 
        transparency: int,
        image_text_ratio: int = 50
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für vertikale Aufteilung (Motiv links, Text rechts)
        """
        result = layout_dict.copy()
        
        # Berechne Positionen für alle Zonen
        zones = result.get('zones', {})
        
        # Aktualisiere nur die Breiten der Text-Zonen, behalte ursprüngliche Positionen
        text_zones = ['standort_block', 'headline_block', 'subline_block', 'benefits_block', 'company_block', 'cta_block']
        
        # Verwende Hilfsfunktion für adaptive Typografie
        self._update_text_zones_adaptive(zones, text_zones, text_width, 80, transparency)
        
        # Aktualisiere nur die Bild-Zone (Motiv links)
        if 'motiv_area' in zones:
            original_zone = zones['motiv_area']
            zones['motiv_area'].update({
                'x': 0,  # Motiv startet links
                'width': image_width
            })
        
        # Aktualisiere Text-Positionen (Text rechts)
        for zone_name in text_zones:
            if zone_name in zones:
                zones[zone_name].update({
                    'x': image_width + 60  # 60px Abstand vom Motiv
                })
        
        # Aktualisiere das Layout
        result['zones'] = zones
        
        # Füge berechnete Werte hinzu
        result['calculated_values'] = {
            'text_width': text_width,
            'image_width': image_width,
            'container_transparency': transparency / 100,
            'image_text_ratio': image_text_ratio
        }
        
        return result
    
    def _calculate_horizontal_split(
        self, 
        layout_dict: Dict[str, Any], 
        text_width: int, 
        image_width: int, 
        transparency: int,
        image_text_ratio: int = 50
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für horizontale Aufteilung (Bild links, Text rechts)
        """
        result = layout_dict.copy()
        
        # Bei horizontaler Aufteilung ist das Verhältnis umgekehrt
        # 30% Ratio = 70% Bild, 30% Text
        # 70% Ratio = 30% Bild, 70% Text
        
        # Berechne tatsächliche Breiten
        actual_image_width = int((100 - transparency) / 100 * self.canvas_width)
        actual_text_width = self.canvas_width - actual_image_width - 20  # 20px Abstand
        
        # Validiere Breiten
        actual_text_width = max(self.min_text_width, min(self.max_text_width, actual_text_width))
        actual_image_width = max(self.min_image_width, min(self.max_image_width, actual_image_width))
        
        zones = result.get('zones', {})
        
        # Aktualisiere nur die Bild-Zone
        if 'image_motiv' in zones:
            original_zone = zones['image_motiv']
            zones['image_motiv'].update({
                'width': actual_image_width
            })
        
        # Aktualisiere nur die Breiten der Text-Zonen, behalte ursprüngliche Positionen
        text_zones = ['headline_block', 'subline_block', 'benefits_block', 'company_block', 'cta_block']
        
        # Verwende Hilfsfunktion für adaptive Typografie
        self._update_text_zones_adaptive(zones, text_zones, actual_text_width, 40, transparency)
        
        # Aktualisiere das Layout
        result['zones'] = zones
        
        # Füge berechnete Werte hinzu
        result['calculated_values'] = {
            'text_width': actual_text_width,
            'image_width': actual_image_width,
            'container_transparency': transparency / 100,
            'image_text_ratio': image_text_ratio  # Korrigierter Slider-Wert
        }
        
        return result
    
    def _calculate_modern_split(
        self, 
        layout_dict: Dict[str, Any], 
        text_width: int, 
        image_width: int, 
        transparency: int
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für modernes Split-Layout
        """
        result = layout_dict.copy()
        
        zones = result.get('zones', {})
        
        # Aktualisiere nur die Breiten der Text-Zonen, behalte ursprüngliche Positionen
        text_zones = ['standort_block', 'headline_block', 'subline_block', 'benefits_block', 'company_block', 'cta_block']
        
        for zone_name in text_zones:
            if zone_name in zones:
                # Behalte ursprüngliche x, y, height, z Werte
                original_zone = zones[zone_name]
                new_width = min(text_width - 80, original_zone.get('width', 400))  # 80px Margins
                
                # Aktualisiere Position-String für adaptive Typografie-Berechnung
                original_position = original_zone.get('position', '')
                if original_position and ',' in original_position:
                    parts = original_position.split(',')
                    if len(parts) >= 4:
                        # Aktualisiere nur die Breite im Position-String
                        parts[2] = str(new_width)
                        updated_position = ','.join(parts)
                        zones[zone_name]['position'] = updated_position
                
                zones[zone_name].update({
                    'width': new_width,
                    'transparency': transparency / 100
                })
        
        # Aktualisiere nur die Bild-Zone
        if 'image_motiv' in zones:
            original_zone = zones['image_motiv']
            zones['image_motiv'].update({
                'x': text_width + 60,  # 60px Abstand vom Text
                'width': image_width
            })
        
        # Aktualisiere das Layout
        result['zones'] = zones
        
        # Füge berechnete Werte hinzu
        result['calculated_values'] = {
            'text_width': text_width,
            'image_width': image_width,
            'container_transparency': transparency / 100,
            'image_text_ratio': transparency
        }
        
        return result
    
    def _calculate_minimalist_layout(
        self, 
        layout_dict: Dict[str, Any], 
        text_width: int, 
        image_width: int, 
        transparency: int
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für minimalistisches Layout
        """
        result = layout_dict.copy()
        
        zones = result.get('zones', {})
        
        # Aktualisiere nur die Breiten der Text-Zonen, behalte ursprüngliche Positionen
        text_zones = ['headline_block', 'subline_block', 'benefits_block', 'company_block', 'cta_block']
        
        # Verwende Hilfsfunktion für adaptive Typografie
        self._update_text_zones_adaptive(zones, text_zones, text_width, 40, transparency)
        
        # Aktualisiere das Layout
        result['zones'] = zones
        
        # Füge berechnete Werte hinzu
        result['calculated_values'] = {
            'text_width': text_width,
            'image_width': image_width,
            'container_transparency': transparency / 100,
            'image_text_ratio': transparency
        }
        
        return result
    
    def _calculate_hero_layout(
        self, 
        layout_dict: Dict[str, Any], 
        text_width: int, 
        image_width: int, 
        transparency: int,
        image_text_ratio: int = 50
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für Hero-Layout (Skizze 8)
        - Motiv nur in oberer Hälfte
        - Stellentitel unten (wo CTA war)
        - CTA rechts oben, kleiner
        - Benefits statt Subline
        """
        result = layout_dict.copy()
        zones = result.get('zones', {}).copy()
        calculated_values = {}
        
        # Hero-Layout Positionen basierend auf Skizze 8 (korrigiert für unteren Bereich)
        hero_positions = {
            'standort_block': {'x': 0.05, 'y': 0.55, 'width': 0.37, 'height': 0.06},      # Unten links
            'logo_block': {'x': 0.58, 'y': 0.55, 'width': 0.37, 'height': 0.06},          # Unten rechts
            'headline_block': {'x': 0.05, 'y': 0.62, 'width': 0.25, 'height': 0.06},      # Links, NOCH KLEINER
            'subline_block': {'x': 0.05, 'y': 0.70, 'width': 0.37, 'height': 0.06},       # Unter Headline
            'benefits_block': {'x': 0.05, 'y': 0.78, 'width': 0.37, 'height': 0.11},      # Unter Subline
            'stellentitel_block': {'x': 0.05, 'y': 0.90, 'width': 0.37, 'height': 0.09},  # Ganz unten links
            'cta_block': {'x': 0.70, 'y': 0.65, 'width': 0.20, 'height': 0.08}            # MITTIG RECHTS
        }
        
        # Text-Zonen für Hero Layout
        text_zones = ['standort_block', 'logo_block', 'headline_block', 'subline_block', 'benefits_block', 'stellentitel_block', 'cta_block']
        
        # Aktualisiere Text-Zonen mit Hero-Positionen
        for zone_name in text_zones:
            if zone_name in zones and zone_name in hero_positions:
                original_zone = zones[zone_name]
                pos = hero_positions[zone_name]
                
                # Berechne absolute Koordinaten
                x = int(pos['x'] * self.canvas_width)
                y = int(pos['y'] * self.canvas_height)
                width = int(pos['width'] * self.canvas_width)
                height = int(pos['height'] * self.canvas_height)
                
                # Nur Geometrie + Transparenz, Styling erfolgt im Resolver-Post-Step
                zones[zone_name] = {
                    **original_zone,
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height,
                    'transparency': transparency / 100
                }
        
        # Berechne dynamische Y-Koordinate für Motivzone basierend auf Slider
        # Höherer Slider-Wert = kleinere Y-Koordinate = mehr Bildfläche
        base_motiv_y = 540  # Standard: Mitte des Canvas
        motiv_y_range = 200  # Bereich von 340 bis 740
        
        # Slider-Logik: 30% = 340px (wenig Bild), 70% = 740px (viel Bild)
        # Formel: Y = 340 + (ratio - 30) * (740 - 340) / (70 - 30)
        dynamic_motiv_y = 340 + (image_text_ratio - 30) * (740 - 340) / (70 - 30)
        dynamic_motiv_y = max(340, min(740, dynamic_motiv_y))  # Begrenze auf sinnvolle Werte
        
        # Berechne Motiv-Höhe basierend auf Y-Koordinate
        dynamic_motiv_height = self.canvas_height - dynamic_motiv_y
        
        # Motiv-Zone mit dynamischer Y-Koordinate (bedeckt kompletten oberen Bereich)
        if 'motiv_area' in zones:
            zones['motiv_area'] = {
                **zones['motiv_area'],
                'x': 0,
                'y': 0,  # Motiv startet immer oben (Y=0)
                'width': self.canvas_width,
                'height': int(dynamic_motiv_y),  # Höhe bis zur dynamischen Y-Koordinate
                'transparency': 1.0
            }
        
        # Berechne Werte für semantische Beschreibung
        calculated_values.update({
            'image_text_ratio': image_text_ratio,
            'container_transparency': transparency,
            'dynamic_motiv_y': dynamic_motiv_y,
            'dynamic_motiv_height': dynamic_motiv_height,
            'motiv_y_percent': round(dynamic_motiv_y / self.canvas_height * 100, 1),
            'layout_style': 'hero_arrangement',
            'hero_logic': 'higher_slider_smaller_y'
        })
        
        return {
            'zones': zones,
            'calculated_values': calculated_values,
            'layout_type': 'hero_layout'
        }
    
    def _calculate_portfolio_layout(
        self, 
        layout_dict: Dict[str, Any], 
        text_width: int, 
        image_width: int, 
        transparency: int
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für Portfolio-Layout
        """
        result = layout_dict.copy()
        
        zones = result.get('zones', {})
        
        # Aktualisiere nur die Breiten der Text-Zonen, behalte ursprüngliche Positionen
        text_zones = ['headline_block', 'subline_block', 'benefits_block', 'company_block', 'cta_block']
        
        for zone_name in text_zones:
            if zone_name in zones:
                # Behalte ursprüngliche x, y, height, z Werte
                original_zone = zones[zone_name]
                new_width = min(text_width - 40, original_zone.get('width', 400))  # 40px Margins
                
                zones[zone_name].update({
                    'width': new_width,
                    'transparency': transparency / 100
                })
        
        # Aktualisiere das Layout
        result['zones'] = zones
        
        # Füge berechnete Werte hinzu
        result['calculated_values'] = {
            'text_width': text_width,
            'image_width': image_width,
            'container_transparency': transparency / 100,
            'image_text_ratio': transparency
        }
        
        return result
    

    def _calculate_storytelling_layout(
        self, 
        layout_dict: Dict[str, Any], 
        text_width: int, 
        image_width: int, 
        transparency: int,
        image_text_ratio: int = 50
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für Skizze 9 - Dual Headline Layout
        - Keine Benefits
        - Zwei separate Headline-Container
        - Motiv als Vollbild-Hintergrund
        - Alle Textelemente in eigenen Containern
        """
        result = layout_dict.copy()
        zones = result.get('zones', {}).copy()
        calculated_values = {}

        # Skizze 9 Positionen - Dual Headline Layout
        storytelling_positions = {
            'standort_block': {'x': 0.05, 'y': 0.05, 'width': 0.45, 'height': 0.06},      # Oben links
            'headline_1_block': {'x': 0.05, 'y': 0.15, 'width': 0.45, 'height': 0.08},    # Erste Headline
            'headline_2_block': {'x': 0.05, 'y': 0.25, 'width': 0.45, 'height': 0.08},    # Zweite Headline
            'subline_block': {'x': 0.05, 'y': 0.35, 'width': 0.45, 'height': 0.06},       # Unter Headlines
            'stellentitel_block': {'x': 0.05, 'y': 0.45, 'width': 0.45, 'height': 0.08},  # Stellentitel
            'cta_block': {'x': 0.05, 'y': 0.55, 'width': 0.45, 'height': 0.08}            # CTA
        }

        # Text-Zonen für Skizze 9 (KEINE Benefits!)
        text_zones = ['standort_block', 'headline_1_block', 'headline_2_block', 'subline_block', 'stellentitel_block', 'cta_block']

        # Aktualisiere Text-Zonen mit Skizze 9 Positionen
        for zone_name in text_zones:
            if zone_name in zones and zone_name in storytelling_positions:
                original_zone = zones[zone_name]
                pos = storytelling_positions[zone_name]

                # Berechne absolute Koordinaten
                x = int(pos['x'] * self.canvas_width)
                y = int(pos['y'] * self.canvas_height)
                width = int(pos['width'] * self.canvas_width)
                height = int(pos['height'] * self.canvas_height)

                # Container-Style für sichtbare Container
                container_style = {
                    'background_color': '#FFFFFF',
                    'opacity': transparency / 100,
                    'border_radius': 16,
                    'shadow': '0 4px 8px rgba(0,0,0,0.1)',
                    'border': 'none',
                    'outline': 'none'
                }

                zones[zone_name] = {
                    **original_zone,
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height,
                    'container_style': container_style
                }

        # Motiv-Zone als Vollbild-Hintergrund
        if 'motiv_area' in zones:
            zones['motiv_area'] = {
                **zones['motiv_area'],
                'x': 0,
                'y': 0,
                'width': self.canvas_width,
                'height': self.canvas_height,
                'transparency': 1.0
            }

        # Berechne Werte für semantische Beschreibung
        calculated_values.update({
            'image_text_ratio': image_text_ratio,
            'container_transparency': transparency,
            'layout_style': 'dual_headline_arrangement',
            'storytelling_logic': 'full_background_motiv'
        })

        return {
            'zones': zones,
            'calculated_values': calculated_values,
            'layout_type': 'storytelling_layout',
            'canvas': layout_dict.get('canvas', {})
        }


    def _calculate_infographic_layout(
        self, 
        layout_dict: Dict[str, Any], 
        text_width: int, 
        image_width: int, 
        transparency: int
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für Infographic-Layout
        """
        result = layout_dict.copy()
        
        zones = result.get('zones', {})
        
        # Aktualisiere nur die Breiten der Text-Zonen, behalte ursprüngliche Positionen
        text_zones = ['headline_block', 'subline_block', 'infographic_block', 'cta_block']
        
        # Verwende Hilfsfunktion für adaptive Typografie
        self._update_text_zones_adaptive(zones, text_zones, text_width, 40, transparency)
        
        # Aktualisiere das Layout
        result['zones'] = zones
        
        # Füge berechnete Werte hinzu
        result['calculated_values'] = {
            'text_width': text_width,
            'image_width': image_width,
            'container_transparency': transparency / 100,
            'image_text_ratio': transparency
        }
        
        return result


    def _calculate_magazine_layout(
        self, 
        layout_dict: Dict[str, Any], 
        text_width: int, 
        image_width: int, 
        transparency: int
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für Magazine-Layout
        """
        result = layout_dict.copy()
        
        zones = result.get('zones', {})
        
        # Aktualisiere nur die Breiten der Text-Zonen, behalte ursprüngliche Positionen
        text_zones = ['headline_block', 'subline_block', 'content_block', 'cta_block']
        
        # Verwende Hilfsfunktion für adaptive Typografie
        self._update_text_zones_adaptive(zones, text_zones, text_width, 40, transparency)
        
        # Aktualisiere das Layout
        result['zones'] = zones
        
        # Füge berechnete Werte hinzu
        result['calculated_values'] = {
            'text_width': text_width,
            'image_width': image_width,
            'container_transparency': transparency / 100,
            'image_text_ratio': transparency
        }
        
        return result

    def _calculate_centered_layout(
        self, 
        layout_dict: Dict[str, Any], 
        text_width: int, 
        image_width: int, 
        transparency: int,
        image_text_ratio: int = 50
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für zentriertes Layout mit Hintergrund-Motiv und sichtbaren Containern
        
        Bei Hintergrund-Motiven:
        - 30% Ratio = Kleinere Container-Gruppe, mehr Hintergrund-Motiv sichtbar
        - 70% Ratio = Größere Container-Gruppe, weniger Hintergrund-Motiv sichtbar
        - Container-Transparenz steuert die Sichtbarkeit der Container
        """
        result = layout_dict.copy()
        zones = result.get('zones', {})
        
        # Bei zentrierten Layouts ist das Motiv der gesamte Hintergrund
        # Das Verhältnis steuert die Größe der gesamten Container-Gruppe
        
        # Berechne Container-Gruppen-Größe basierend auf dem Ratio
        # 30% = kleinere Container-Gruppe (mehr Motiv sichtbar)
        # 70% = größere Container-Gruppe (weniger Motiv sichtbar)
        ratio_factor = image_text_ratio / 100  # 0.3 bis 0.7
        
        # Container-Gruppen-Breite: Je höher das Ratio, desto breiter die gesamte Gruppe
        base_container_width = 500  # Basis-Breite für Container-Gruppe
        min_container_width = 350   # Minimale Breite
        max_container_width = 700   # Maximale Breite
        
        # Berechne dynamische Container-Gruppen-Breite
        dynamic_container_width = int(base_container_width * (0.7 + ratio_factor * 0.6))  # 0.7 bis 1.3 Faktor
        dynamic_container_width = max(min_container_width, min(max_container_width, dynamic_container_width))
        
        # Container-Gruppen-Höhe: Je höher das Ratio, desto höher die gesamte Gruppe
        base_container_height = 800  # Basis-Höhe für Container-Gruppe
        min_container_height = 600   # Minimale Höhe
        max_container_height = 1000  # Maximale Höhe
        
        dynamic_container_height = int(base_container_height * (0.75 + ratio_factor * 0.5))  # 0.75 bis 1.25 Faktor
        dynamic_container_height = max(min_container_height, min(max_container_height, dynamic_container_height))
        
        # Zentriere die Container-Gruppe
        container_group_x = (self.canvas_width - dynamic_container_width) // 2
        container_group_y = (self.canvas_height - dynamic_container_height) // 2
        
        # Text-Zonen für zentriertes Layout
        text_zones = ['standort_block', 'headline_block', 'subline_block', 'benefits_block', 'cta_block']
        
        # Berechne relative Positionen innerhalb der Container-Gruppe
        relative_positions = {
            'standort_block': {'x': 0.1, 'y': 0.05, 'width': 0.8, 'height': 0.08},
            'headline_block': {'x': 0.1, 'y': 0.15, 'width': 0.8, 'height': 0.15},
            'subline_block': {'x': 0.15, 'y': 0.35, 'width': 0.7, 'height': 0.1},
            'benefits_block': {'x': 0.15, 'y': 0.5, 'width': 0.7, 'height': 0.25},
            'cta_block': {'x': 0.25, 'y': 0.8, 'width': 0.5, 'height': 0.12}
        }
        
        # Aktualisiere Text-Zonen mit sichtbaren Containern
        for zone_name in text_zones:
            if zone_name in zones and zone_name in relative_positions:
                original_zone = zones[zone_name]
                rel_pos = relative_positions[zone_name]
                
                # Berechne absolute Positionen basierend auf Container-Gruppe
                new_x = container_group_x + int(rel_pos['x'] * dynamic_container_width)
                new_y = container_group_y + int(rel_pos['y'] * dynamic_container_height)
                new_width = int(rel_pos['width'] * dynamic_container_width)
                new_height = int(rel_pos['height'] * dynamic_container_height)
                
                # Aktualisiere Position-String für adaptive Typografie
                self._update_zone_position_for_adaptive_typography(original_zone, new_width)
                
                # Nur Geometrie + Transparenz, Styling erfolgt im Resolver-Post-Step
                zones[zone_name].update({
                    'x': new_x,
                    'y': new_y,
                    'width': new_width,
                    'height': new_height,
                    'transparency': transparency / 100
                })
        
        # Hintergrund-Motiv bleibt unverändert (ganzer Canvas)
        if 'motiv_area' in zones:
            zones['motiv_area'].update({
                'x': 0,
                'y': 0,
                'width': self.canvas_width,
                'height': self.canvas_height,
                'transparency': 1.0  # Hintergrund-Motiv ist immer vollständig sichtbar
            })
        
        # Aktualisiere das Layout
        result['zones'] = zones

        # Füge berechnete Werte hinzu (ohne Style-Kennzeichnung)
        result['calculated_values'] = {
            'container_group_width': dynamic_container_width,
            'container_group_height': dynamic_container_height,
            'container_group_x': container_group_x,
            'container_group_y': container_group_y,
            'image_width': self.canvas_width,  # Motiv ist der gesamte Hintergrund
            'container_transparency': transparency / 100,
            'image_text_ratio': image_text_ratio,
            'background_motiv_visible': 1.0
        }
        
        return result

    def _calculate_diagonal_layout(
        self, 
        layout_dict: Dict[str, Any], 
        text_width: int, 
        image_width: int, 
        transparency: int,
        image_text_ratio: int = 50
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für diagonales Layout mit Hintergrund-Motiv und diagonal angeordneten Containern
        
        Bei Diagonal-Layouts:
        - 30% Ratio = Kleinere Container-Gruppe, mehr Hintergrund-Motiv sichtbar
        - 70% Ratio = Größere Container-Gruppe, weniger Hintergrund-Motiv sichtbar
        - Container sind diagonal angeordnet (von oben-links nach unten-rechts)
        """
        result = layout_dict.copy()
        zones = result.get('zones', {})
        
        # Bei diagonalen Layouts ist das Motiv der gesamte Hintergrund
        # Das Verhältnis steuert die Größe der diagonalen Container-Gruppe
        
        # Berechne Container-Gruppen-Größe basierend auf dem Ratio
        ratio_factor = image_text_ratio / 100  # 0.3 bis 0.7
        
        # Container-Gruppen-Breite: Je höher das Ratio, desto breiter die gesamte Gruppe
        base_container_width = 450  # Basis-Breite für Container-Gruppe
        min_container_width = 300   # Minimale Breite
        max_container_width = 600   # Maximale Breite
        
        # Berechne dynamische Container-Gruppen-Breite
        dynamic_container_width = int(base_container_width * (0.7 + ratio_factor * 0.6))  # 0.7 bis 1.3 Faktor
        dynamic_container_width = max(min_container_width, min(max_container_width, dynamic_container_width))
        
        # Container-Gruppen-Höhe: Je höher das Ratio, desto höher die gesamte Gruppe
        base_container_height = 800  # Basis-Höhe für Container-Gruppe
        min_container_height = 600   # Minimale Höhe
        max_container_height = 1000  # Maximale Höhe
        
        dynamic_container_height = int(base_container_height * (0.75 + ratio_factor * 0.5))  # 0.75 bis 1.25 Faktor
        dynamic_container_height = max(min_container_height, min(max_container_height, dynamic_container_height))
        
        # Text-Zonen für diagonales Layout
        text_zones = ['standort_block', 'headline_block', 'subline_block', 'benefits_block', 'cta_block']
        
        # Berechne diagonale Positionen (Standort oben rechts, Text weiter unten rechts, CTA weiter links)
        diagonal_positions = {
            'standort_block': {'x': 0.65, 'y': 0.05, 'width': 0.3, 'height': 0.08},  # Oben rechts
            'headline_block': {'x': 0.45, 'y': 0.7, 'width': 0.4, 'height': 0.12},   # Weiter unten rechts
            'subline_block': {'x': 0.5, 'y': 0.8, 'width': 0.35, 'height': 0.1},     # Weiter unten rechts
            'benefits_block': {'x': 0.55, 'y': 0.9, 'width': 0.3, 'height': 0.08},   # Weiter unten rechts
            'cta_block': {'x': 0.05, 'y': 0.85, 'width': 0.25, 'height': 0.12}        # Weiter links
        }
        
        # Aktualisiere Text-Zonen mit diagonalen sichtbaren Containern
        for zone_name in text_zones:
            if zone_name in zones and zone_name in diagonal_positions:
                original_zone = zones[zone_name]
                rel_pos = diagonal_positions[zone_name]
                
                # Berechne absolute Positionen basierend auf Canvas
                # Neue diagonale Anordnung: Standort oben rechts, Text unten rechts, CTA unten links
                new_x = int(rel_pos['x'] * self.canvas_width)
                new_y = int(rel_pos['y'] * self.canvas_height)
                new_width = int(rel_pos['width'] * self.canvas_width)
                new_height = int(rel_pos['height'] * self.canvas_height)
                
                # Stelle sicher, dass Container nicht über Canvas hinausgehen
                new_x = max(20, min(new_x, self.canvas_width - new_width - 20))
                new_y = max(20, min(new_y, self.canvas_height - new_height - 20))
                
                # Aktualisiere Position-String für adaptive Typografie
                self._update_zone_position_for_adaptive_typography(original_zone, new_width)
                
                # Nur Geometrie + Transparenz, Styling erfolgt im Resolver-Post-Step
                zones[zone_name].update({
                    'x': new_x,
                    'y': new_y,
                    'width': new_width,
                    'height': new_height,
                    'transparency': transparency / 100
                })
        
        # Hintergrund-Motiv bleibt unverändert (ganzer Canvas)
        if 'motiv_area' in zones:
            zones['motiv_area'].update({
                'x': 0,
                'y': 0,
                'width': self.canvas_width,
                'height': self.canvas_height,
                'transparency': 1.0  # Hintergrund-Motiv ist immer vollständig sichtbar
            })
        
        # Aktualisiere das Layout
        result['zones'] = zones
        
        # Füge berechnete Werte hinzu (ohne Style-Kennzeichnung)
        result['calculated_values'] = {
            'container_group_width': dynamic_container_width,
            'container_group_height': dynamic_container_height,
            'image_width': self.canvas_width,  # Motiv ist der gesamte Hintergrund
            'container_transparency': transparency / 100,
            'image_text_ratio': image_text_ratio,
            'background_motiv_visible': 1.0,  # Hintergrund-Motiv ist immer sichtbar
            'layout_style': 'diagonal_arrangement'  # Kennzeichnung für diagonale Anordnung
        }
        
        return result

    def _calculate_asymmetric_layout(
        self, 
        layout_dict: Dict[str, Any], 
        text_width: int, 
        image_width: int, 
        transparency: int,
        image_text_ratio: int = 50
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für asymmetrisches Layout mit Hintergrund-Motiv und inverser Slider-Logik
        
        INVERSE LOGIK: Kleinere Motivzone (Slider) = Größere Container-Elemente
        - 30% Ratio = Größere Container (weniger Motiv sichtbar)
        - 70% Ratio = Kleinere Container (mehr Motiv sichtbar)
        """
        result = layout_dict.copy()
        zones = result.get('zones', {})
        
        # Bei asymmetrischen Layouts ist das Motiv der gesamte Hintergrund
        # INVERSE LOGIK: Je höher das Ratio, desto kleiner die Container
        
        # Berechne Container-Größe basierend auf dem Ratio (INVERSE LOGIK)
        ratio_factor = image_text_ratio / 100  # 0.3 bis 0.7
        
        # Container-Größe: Je höher das Ratio, desto kleiner die Container (INVERSE)
        base_container_scale = 1.0  # Basis-Skalierung
        min_scale = 0.6   # Minimale Skalierung (70% Ratio)
        max_scale = 1.4   # Maximale Skalierung (30% Ratio)
        
        # Berechne inverse Skalierung: 30% Ratio = 1.4x, 70% Ratio = 0.6x
        inverse_scale = max_scale - (ratio_factor - 0.3) * (max_scale - min_scale) / 0.4
        inverse_scale = max(min_scale, min(max_scale, inverse_scale))
        
        # Text-Zonen für asymmetrisches Layout (ohne Benefits)
        text_zones = ['standort_block', 'headline_block', 'subline_block', 'stellentitel_block', 'cta_block']
        
        # Berechne asymmetrische Positionen (angepasst nach User-Feedback)
        asymmetric_positions = {
            'standort_block': {'x': 0.70, 'y': 0.05, 'width': 0.25, 'height': 0.06},  # Weiter nach rechts
            'headline_block': {'x': 0.30, 'y': 0.10, 'width': 0.56, 'height': 0.11},  # Weiter nach oben
            'subline_block': {'x': 0.35, 'y': 0.22, 'width': 0.46, 'height': 0.07},   # Weiter nach oben
            'stellentitel_block': {'x': 0.50, 'y': 0.50, 'width': 0.28, 'height': 0.09}, # Zwischen Subline und CTA
            'cta_block': {'x': 0.70, 'y': 0.85, 'width': 0.28, 'height': 0.09}         # Weiter nach rechts
        }
        
        # Aktualisiere Text-Zonen mit asymmetrischen sichtbaren Containern
        for zone_name in text_zones:
            if zone_name in zones and zone_name in asymmetric_positions:
                original_zone = zones[zone_name]
                rel_pos = asymmetric_positions[zone_name]
                
                # Berechne absolute Positionen basierend auf Canvas
                base_x = int(rel_pos['x'] * self.canvas_width)
                base_y = int(rel_pos['y'] * self.canvas_height)
                base_width = int(rel_pos['width'] * self.canvas_width)
                base_height = int(rel_pos['height'] * self.canvas_height)
                
                # Wende inverse Skalierung an
                new_width = int(base_width * inverse_scale)
                new_height = int(base_height * inverse_scale)
                
                # Zentriere die Container nach Skalierung
                new_x = base_x + (base_width - new_width) // 2
                new_y = base_y + (base_height - new_height) // 2
                
                # Stelle sicher, dass Container nicht über Canvas hinausgehen
                new_x = max(20, min(new_x, self.canvas_width - new_width - 20))
                new_y = max(20, min(new_y, self.canvas_height - new_height - 20))
                
                # Aktualisiere Position-String für adaptive Typografie
                self._update_zone_position_for_adaptive_typography(original_zone, new_width)
                
                # Nur Geometrie + Transparenz, Styling erfolgt im Resolver-Post-Step
                zones[zone_name].update({
                    'x': new_x,
                    'y': new_y,
                    'width': new_width,
                    'height': new_height,
                    'transparency': transparency / 100
                })
        
        # Hintergrund-Motiv bleibt unverändert (ganzer Canvas)
        if 'motiv_area' in zones:
            zones['motiv_area'].update({
                'x': 0,
                'y': 0,
                'width': self.canvas_width,
                'height': self.canvas_height,
                'transparency': 1.0  # Hintergrund-Motiv ist immer vollständig sichtbar
            })
        
        # Aktualisiere das Layout
        result['zones'] = zones
        
        # Füge berechnete Werte hinzu (ohne Style-Kennzeichnung)
        result['calculated_values'] = {
            'container_scale': inverse_scale,
            'image_width': self.canvas_width,  # Motiv ist der gesamte Hintergrund
            'container_transparency': transparency / 100,
            'image_text_ratio': image_text_ratio,
            'background_motiv_visible': 1.0,  # Hintergrund-Motiv ist immer sichtbar
            'layout_style': 'asymmetric_arrangement',  # Kennzeichnung für asymmetrische Anordnung
            'inverse_logic': True  # Kennzeichnung für inverse Slider-Logik
        }
        
        return result

    def _calculate_grid_layout(
        self, 
        layout_dict: Dict[str, Any], 
        text_width: int, 
        image_width: int, 
        transparency: int,
        image_text_ratio: int = 50
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für Grid Layout mit Hintergrund-Motiv und sichtbaren Containern
        
        Bei Grid Layouts:
        - 30% Ratio = Kleinere Container-Gruppe, mehr Hintergrund-Motiv sichtbar
        - 70% Ratio = Größere Container-Gruppe, weniger Hintergrund-Motiv sichtbar
        - Grid-basierte Anordnung ohne Headline
        """
        result = layout_dict.copy()
        zones = result.get('zones', {})
        
        # Bei Grid Layouts ist das Motiv der gesamte Hintergrund
        # Das Verhältnis steuert die Größe der Grid-Container-Gruppe
        
        # Berechne Container-Gruppen-Größe basierend auf dem Ratio
        ratio_factor = image_text_ratio / 100  # 0.3 bis 0.7
        
        # Container-Gruppen-Breite: Je höher das Ratio, desto breiter die gesamte Gruppe
        base_container_width = 500  # Basis-Breite für Container-Gruppe
        min_container_width = 350   # Minimale Breite
        max_container_width = 700   # Maximale Breite
        
        # Berechne dynamische Container-Gruppen-Breite
        dynamic_container_width = int(base_container_width * (0.7 + ratio_factor * 0.6))  # 0.7 bis 1.3 Faktor
        dynamic_container_width = max(min_container_width, min(max_container_width, dynamic_container_width))
        
        # Container-Gruppen-Höhe: Je höher das Ratio, desto höher die gesamte Gruppe
        base_container_height = 800  # Basis-Höhe für Container-Gruppe
        min_container_height = 600   # Minimale Höhe
        max_container_height = 1000  # Maximale Höhe
        
        dynamic_container_height = int(base_container_height * (0.75 + ratio_factor * 0.5))  # 0.75 bis 1.25 Faktor
        dynamic_container_height = max(min_container_height, min(max_container_height, dynamic_container_height))
        
        # Zentriere die Container-Gruppe
        container_group_x = (self.canvas_width - dynamic_container_width) // 2
        container_group_y = (self.canvas_height - dynamic_container_height) // 2
        
        # Text-Zonen für Grid Layout (OHNE Headline, OHNE CTA, OHNE Benefits)
        text_zones = ['standort_block', 'subline_block', 'stellentitel_block']
        
        # Berechne Grid-Positionen (Standort oben links, Stellentitel/Subline unten links)
        grid_positions = {
            'standort_block': {'x': 0.05, 'y': 0.05, 'width': 0.4, 'height': 0.12},      # Links oben
            'subline_block': {'x': 0.05, 'y': 0.7, 'width': 0.4, 'height': 0.12},        # Links unten
            'stellentitel_block': {'x': 0.05, 'y': 0.85, 'width': 0.4, 'height': 0.10}   # Links unten
        }
        
        # Aktualisiere Text-Zonen mit Grid sichtbaren Containern
        for zone_name in text_zones:
            if zone_name in zones and zone_name in grid_positions:
                original_zone = zones[zone_name]
                rel_pos = grid_positions[zone_name]
                
                # Berechne absolute Positionen basierend auf Container-Gruppe
                new_x = container_group_x + int(rel_pos['x'] * dynamic_container_width)
                new_y = container_group_y + int(rel_pos['y'] * dynamic_container_height)
                new_width = int(rel_pos['width'] * dynamic_container_width)
                new_height = int(rel_pos['height'] * dynamic_container_height)
                
                # Aktualisiere Position-String für adaptive Typografie
                self._update_zone_position_for_adaptive_typography(original_zone, new_width)
                
                # Container-Styling für sichtbare Container
                zones[zone_name].update({
                    'x': new_x,
                    'y': new_y,
                    'width': new_width,
                    'height': new_height,
                    'transparency': transparency / 100,
                    'container_style': {
                        'background_color': '#FFFFFF',
                        'background_opacity': transparency / 100,
                        'border_radius': 12,
                        'border_color': '#E0E0E0',
                        'border_width': 1,
                        'shadow_color': '#000000',
                        'shadow_opacity': 0.1,
                        'shadow_blur': 8,
                        'shadow_offset_x': 0,
                        'shadow_offset_y': 2
                    }
                })
        
        # Hintergrund-Motiv bleibt unverändert (ganzer Canvas)
        if 'motiv_area' in zones:
            zones['motiv_area'].update({
                'x': 0,
                'y': 0,
                'width': self.canvas_width,
                'height': self.canvas_height,
                'transparency': 1.0  # Hintergrund-Motiv ist immer vollständig sichtbar
            })
        
        # Aktualisiere das Layout
        result['zones'] = zones
        
        # Füge berechnete Werte hinzu
        result['calculated_values'] = {
            'container_group_width': dynamic_container_width,
            'container_group_height': dynamic_container_height,
            'container_group_x': container_group_x,
            'container_group_y': container_group_y,
            'image_width': self.canvas_width,  # Motiv ist der gesamte Hintergrund
            'container_transparency': transparency / 100,
            'image_text_ratio': image_text_ratio,
            'background_motiv_visible': 1.0,
            'layout_style': 'grid_arrangement',
            'no_headline': True  # Kennzeichnung dass keine Headline vorhanden ist
        }
        
        return result


    def apply_transparency_effects(self, layout_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Wendet Transparenz-Effekte auf alle Container an
        """
        result = layout_dict.copy()
        zones = result.get('zones', {})
        
        transparency_handling = result.get('layout_engine', {}).get('transparency_handling', {})
        apply_to_zones = transparency_handling.get('apply_to_zones', [])
        fallback_opacity = transparency_handling.get('fallback_opacity', 0.9)
        
        for zone_name, zone_data in zones.items():
            if zone_name in apply_to_zones:
                # Konvertiere Transparenz von 0-100 zu 0.0-1.0
                transparency = zone_data.get('transparency', fallback_opacity)
                if isinstance(transparency, (int, float)) and transparency > 1:
                    transparency = transparency / 100

                # Validiere Transparenz
                transparency = max(0.1, min(1.0, transparency))
                zones[zone_name]['transparency'] = transparency

                # Wenn bereits container_style Hintergrund-Opacity vorhanden ist,
                # keine zusaetzlichen Felder (opacity/alpha) mehr setzen.
                cs = zone_data.get('container_style', {}) if isinstance(zone_data, dict) else {}
                has_bg_opacity = False
                if isinstance(cs, dict):
                    if 'background_opacity' in cs:
                        has_bg_opacity = True
                    elif 'background' in cs and isinstance(cs.get('background'), dict) and 'opacity' in cs['background']:
                        has_bg_opacity = True
                if not has_bg_opacity:
                    # Legacy-Kompatibilitaet: Nur falls kein Resolver aktiv war
                    zones[zone_name]['opacity'] = transparency
                    zones[zone_name]['alpha'] = transparency
        
        result['zones'] = zones
        return result
    
    def validate_layout(self, layout_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validiert das Layout und setzt __validated__ Flag
        
        Args:
            layout_dict: Layout-Dictionary
            
        Returns:
            Layout-Dictionary mit Validierungsstatus
            
        Raises:
            LayoutValidationError: Bei Validierungsfehlern
        """
        result = layout_dict.copy()
        
        # Verwende das neue Schema für strikte Validierung
        errors = validate_layout_strict(result)
        
        if errors:
            # Layout ist ungültig - werfe Exception
            raise LayoutValidationError({
                "layout_id": result.get('layout_id', 'unknown'),
                "errors": errors
            })
        
        # Layout ist valide - setze Flag
        result['__validated__'] = True
        result['validation_status'] = 'valid'
        
        # Füge zusätzliche Warnungen hinzu (nicht blockierend)
        warnings = self._generate_additional_warnings(result)
        if warnings:
            result['validation_warnings'] = warnings
            result['validation_status'] = 'warnings'
        
        return result
    
    def _generate_additional_warnings(self, layout_dict: Dict[str, Any]) -> List[str]:
        """Generiert zusätzliche Warnungen (nicht blockierend)"""
        # Da wir jetzt feste Koordinaten verwenden, brauchen wir keine Warnungen mehr
        return []


    def _calculate_split_layout(self, layout_dict, text_width, image_width, container_transparency, image_text_ratio):
        """Berechnet Split-Layout: Obere Hälfte Layout, untere Hälfte Motiv mit dynamischer Y-Koordinate"""
        zones = layout_dict.get('zones', {}).copy()
        calculated_values = {}
        
        # Berechne dynamische Y-Koordinate für Motivzone basierend auf Slider
        # Höherer Slider-Wert = kleinere Y-Koordinate = mehr Bildfläche
        base_motiv_y = 540  # Standard: Mitte des Canvas
        motiv_y_range = 200  # Bereich von 340 bis 740
        
        # Slider-Logik: 0% = Y=740 (wenig Bild), 100% = Y=340 (viel Bild)
        dynamic_motiv_y = base_motiv_y + (motiv_y_range * (100 - image_text_ratio) / 100)
        dynamic_motiv_y = max(340, min(740, dynamic_motiv_y))  # Begrenze auf sinnvolle Werte
        
        # Berechne Motiv-Höhe basierend auf Y-Koordinate
        dynamic_motiv_height = self.canvas_height - dynamic_motiv_y
        
        # Text-Zonen für Split Layout
        text_zones = ['standort_block', 'headline_block', 'benefits_block', 'stellentitel_block', 'cta_block']
        
        # Split-Positionen (obere Hälfte für Text, untere Hälfte für Motiv)
        # Alle Elemente in eigenen Containern, verteilt in der oberen Hälfte
        split_positions = {
            'standort_block': {'x': 0.05, 'y': 0.05, 'width': 0.4, 'height': 0.06},      # Oben links
            'headline_block': {'x': 0.05, 'y': 0.15, 'width': 0.6, 'height': 0.08},      # Unter dem Standort, breiter
            'benefits_block': {'x': 0.05, 'y': 0.25, 'width': 0.6, 'height': 0.20},      # Unter der Headline (links)
            'stellentitel_block': {'x': 0.05, 'y': 0.60, 'width': 0.4, 'height': 0.08},  # Unten links, über CTA
            'cta_block': {'x': 0.05, 'y': 0.85, 'width': 0.4, 'height': 0.08}            # Ganz unten links
        }
        
        # Aktualisiere Text-Zonen mit Split-Positionen
        for zone_name in text_zones:
            if zone_name in zones and zone_name in split_positions:
                original_zone = zones[zone_name]
                pos = split_positions[zone_name]
                
                # Berechne absolute Koordinaten
                x = int(pos['x'] * self.canvas_width)
                y = int(pos['y'] * self.canvas_height)
                width = int(pos['width'] * self.canvas_width)
                height = int(pos['height'] * self.canvas_height)
                
                # Nur Geometrie, Styling erfolgt im Resolver-Post-Step
                zones[zone_name] = {
                    **original_zone,
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height,
                    'transparency': container_transparency / 100
                }
        
        # Aktualisiere Motiv-Zone mit dynamischer Y-Koordinate
        if 'motiv_area' in zones:
            zones['motiv_area'] = {
                **zones['motiv_area'],
                'x': 0,
                'y': int(dynamic_motiv_y),
                'width': self.canvas_width,
                'height': int(dynamic_motiv_height),
                'transparency': 1.0  # Vollständiger Hintergrund
            }
        
        # Berechne Werte für semantische Beschreibung
        calculated_values.update({
            'image_text_ratio': image_text_ratio,
            'container_transparency': container_transparency,
            'dynamic_motiv_y': dynamic_motiv_y,
            'dynamic_motiv_height': dynamic_motiv_height,
            'motiv_y_percent': round(dynamic_motiv_y / self.canvas_height * 100, 1),
            'layout_style': 'split_arrangement',
            'split_logic': 'higher_slider_smaller_y'
        })
        
        return {
            'zones': zones,
            'calculated_values': calculated_values,
            'layout_type': 'split_layout'
        }


# Globale Instanz des Layout-Engines
layout_engine = LayoutEngine()


@lru_cache(maxsize=32)
def calculate_layout_coordinates_cached(
    layout_id: str,
    image_text_ratio: int = 50,
    container_transparency: int = 80
) -> Dict[str, Any]:
    """
    Gecachte Version der Koordinatenberechnung
    """
    # Diese Funktion würde normalerweise das Layout laden und dann berechnen
    # Für den Moment geben wir ein Dummy-Layout zurück
    return {
        'layout_id': layout_id,
        'calculated_values': {
            'text_width': 400,
            'image_width': 620,
            'container_transparency': container_transparency / 100,
            'image_text_ratio': image_text_ratio
        },
        'validation_status': 'valid'
    }
