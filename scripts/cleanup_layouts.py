#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Layout Cleanup Script
Bereinigt alle YAML-Layout-Dateien und entfernt dynamische Elemente
"""

import os
import yaml
from pathlib import Path

def create_clean_layout_template(layout_id, name, description, layout_type, zones):
    """Erstellt ein sauberes Layout-Template"""
    
    template = {
        'layout_id': layout_id,
        'name': name,
        'description': description,
        'layout_type': layout_type,
        
        'canvas': {
            'width': 1080,
            'height': 1080,
            'background_color': '#FFFFFF',
            'aspect_ratio': '1:1'
        },
        
        'zones': zones,
        
        'meta': {
            'name': name,
            'description': description,
            'layout_type': layout_type,
            'zones_count': len(zones),
            'text_zones': len([z for z in zones.values() if z.get('content_type') == 'text_elements']),
            'image_zones': len([z for z in zones.values() if z.get('content_type') == 'image_motiv'])
        }
    }
    
    return template

def cleanup_layout_file(file_path):
    """Bereinigt eine einzelne Layout-Datei"""
    
    print(f"🔄 Bereinige: {file_path.name}")
    
    try:
        # Lade ursprüngliche Datei
        with open(file_path, 'r', encoding='utf-8') as f:
            original_data = yaml.safe_load(f)
        
        if not original_data:
            print(f"❌ Konnte {file_path.name} nicht laden")
            return False
        
        # Extrahiere grundlegende Informationen
        layout_id = original_data.get('layout_id', file_path.stem)
        name = original_data.get('name', layout_id.replace('_', ' ').title())
        description = original_data.get('description', f'Feste Aufteilung - {name}')
        layout_type = original_data.get('layout_type', 'standard')
        
        # Extrahiere Zonen (nur x, y, width, height, content_type, description)
        zones = {}
        original_zones = original_data.get('zones', {})
        
        for zone_name, zone_data in original_zones.items():
            if isinstance(zone_data, dict):
                clean_zone = {
                    'x': zone_data.get('x', 0),
                    'y': zone_data.get('y', 0),
                    'width': zone_data.get('width', 100),
                    'height': zone_data.get('height', 100),
                    'content_type': zone_data.get('content_type', 'text_elements'),
                    'description': zone_data.get('description', zone_name.replace('_', ' ').title())
                }
                zones[zone_name] = clean_zone
        
        # Erstelle sauberes Template
        clean_template = create_clean_layout_template(
            layout_id, name, description, layout_type, zones
        )
        
        # Speichere bereinigte Datei
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(clean_template, f, default_flow_style=False, 
                      allow_unicode=True, sort_keys=False, indent=2)
        
        print(f"✅ {file_path.name} erfolgreich bereinigt ({len(zones)} Zonen)")
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei {file_path.name}: {e}")
        return False

def main():
    """Hauptfunktion"""
    
    print("🧹 Layout Cleanup Script")
    print("=" * 50)
    
    # Layout-Verzeichnis
    layouts_dir = Path("input_config/layouts")
    
    if not layouts_dir.exists():
        print(f"❌ Layout-Verzeichnis nicht gefunden: {layouts_dir}")
        return
    
    # Alle YAML-Dateien finden
    yaml_files = list(layouts_dir.glob("*.yaml"))
    
    if not yaml_files:
        print("❌ Keine YAML-Dateien gefunden")
        return
    
    print(f"📁 Gefunden: {len(yaml_files)} Layout-Dateien")
    print()
    
    # Erfolgszähler
    success_count = 0
    total_count = len(yaml_files)
    
    # Alle Dateien bereinigen
    for yaml_file in yaml_files:
        if cleanup_layout_file(yaml_file):
            success_count += 1
        print()
    
    # Zusammenfassung
    print("=" * 50)
    print(f"🎯 Bereinigung abgeschlossen: {success_count}/{total_count} Dateien erfolgreich")
    
    if success_count == total_count:
        print("✅ Alle Layout-Dateien erfolgreich bereinigt!")
    else:
        print(f"⚠️ {total_count - success_count} Dateien konnten nicht bereinigt werden")

if __name__ == "__main__":
    main()
