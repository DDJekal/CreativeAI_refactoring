#!/usr/bin/env python3
"""
Script zum Aktualisieren des Layout-Engines für vertical_split_left
"""

import os
import sys

# Füge den creative_core Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'creative_core'))

def update_layout_engine():
    """Aktualisiert das Layout-Engine für vertical_split_left"""
    
    engine_file = os.path.join(os.path.dirname(__file__), '..', 'creative_core', 'layout', 'engine.py')
    
    # Lese die aktuelle Datei
    with open(engine_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Füge den neuen Layout-Typ hinzu
    old_line = "        elif layout_type == 'horizontal_split':"
    new_line = """        elif layout_type == 'vertical_split_left':
            result = self._calculate_vertical_split_left(layout_dict, text_width, image_width, container_transparency, image_text_ratio)
        elif layout_type == 'horizontal_split':"""
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        print("✅ Layout-Typ 'vertical_split_left' hinzugefügt")
    else:
        print("❌ Konnte Layout-Typ nicht hinzufügen")
        return False
    
    # Füge die neue Funktion hinzu
    old_function_end = "        return result\n    \n    def _calculate_horizontal_split("
    new_function = """        return result
    
    def _calculate_vertical_split_left(
        self, 
        layout_dict: Dict[str, Any], 
        text_width: int, 
        image_width: int, 
        transparency: int,
        image_text_ratio: int = 50
    ) -> Dict[str, Any]:
        \"\"\"
        Berechnet Koordinaten für vertikale Aufteilung (Motiv links, Text rechts)
        \"\"\"
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
    
    def _calculate_horizontal_split("""
    
    if old_function_end in content:
        content = content.replace(old_function_end, new_function)
        print("✅ Funktion '_calculate_vertical_split_left' hinzugefügt")
    else:
        print("❌ Konnte Funktion nicht hinzufügen")
        return False
    
    # Schreibe die aktualisierte Datei
    with open(engine_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Layout-Engine erfolgreich aktualisiert!")
    return True

if __name__ == "__main__":
    update_layout_engine()
