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
        self.min_text_width = 350  # Erhöht von 300
        self.max_text_width = 800
        self.min_image_width = 200
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
            result = self._calculate_vertical_split(layout_dict, text_width, image_width, container_transparency)
        elif layout_type == 'horizontal_split':
            result = self._calculate_horizontal_split(layout_dict, text_width, image_width, container_transparency)
        elif layout_type == 'modern_split':
            result = self._calculate_modern_split(layout_dict, text_width, image_width, container_transparency)
        elif layout_type == 'minimalist':
            result = self._calculate_minimalist_layout(layout_dict, text_width, image_width, container_transparency)
        elif layout_type == 'hero':
            result = self._calculate_hero_layout(layout_dict, text_width, image_width, container_transparency)
        elif layout_type == 'portfolio':
            result = self._calculate_portfolio_layout(layout_dict, text_width, image_width, container_transparency)
        elif layout_type == 'storytelling':
            result = self._calculate_storytelling_layout(layout_dict, text_width, image_width, container_transparency)
        elif layout_type == 'infographic':
            result = self._calculate_infographic_layout(layout_dict, text_width, image_width, container_transparency)
        elif layout_type == 'magazine':
            result = self._calculate_magazine_layout(layout_dict, text_width, image_width, container_transparency)
        else:
            # Fallback: Verwende vertikales Split
            result = self._calculate_vertical_split(layout_dict, text_width, image_width, container_transparency)
        
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
        transparency: int
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für vertikale Aufteilung (Text links, Bild rechts)
        """
        result = layout_dict.copy()
        
        # Berechne Positionen für alle Zonen
        zones = result.get('zones', {})
        
        # Aktualisiere nur die Breiten der Text-Zonen, behalte ursprüngliche Positionen
        text_zones = ['standort_block', 'headline_block', 'subline_block', 'benefits_block', 'company_block', 'cta_block']
        
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
            'image_text_ratio': transparency  # Slider-Wert
        }
        
        return result
    
    def _calculate_horizontal_split(
        self, 
        layout_dict: Dict[str, Any], 
        text_width: int, 
        image_width: int, 
        transparency: int
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
            'image_text_ratio': transparency  # Slider-Wert
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
        transparency: int
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für Hero-Layout
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
        transparency: int
    ) -> Dict[str, Any]:
        """
        Berechnet Koordinaten für Storytelling-Layout
        """
        result = layout_dict.copy()
        
        zones = result.get('zones', {})
        
        # Aktualisiere nur die Breiten der Text-Zonen, behalte ursprüngliche Positionen
        text_zones = ['headline_block', 'subline_block', 'story_block', 'cta_block']
        
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
                
                # Füge CSS-kompatible Transparenz hinzu
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
