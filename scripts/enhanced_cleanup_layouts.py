#!/usr/bin/env python3
"""
Enhanced Layout Cleanup Script
Behebt Kompatibilitätsprobleme mit dem neuen Pipeline-System
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any

# Verbotene Felder, die vom Style-Resolver gesetzt werden
FORBIDDEN_ZONE_KEYS = {
    'transparency', 'container_style', 'opacity', 'alpha',
    'background_opacity', 'background_color'
}

# Layout-Typ-Mapping für Engine-Kompatibilität
LAYOUT_TYPE_MAPPING = {
    'vertical_split': 'vertical_split',
    'vertical_split_left': 'vertical_split_left', 
    'centered_layout': 'centered_layout',
    'diagonal_layout': 'diagonal_layout',
    'asymmetric_layout': 'asymmetric_layout',
    'grid_layout': 'grid_layout',
    'split_layout': 'split_layout',
    'hero_layout': 'hero_layout',
    'modern_split': 'modern_split',
    'infographic_layout': 'infographic_layout',
    'magazine_layout': 'magazine_layout',
    'portfolio_layout': 'portfolio_layout',
    'storytelling_layout': 'storytelling_layout',
    'dual_headline_layout': 'storytelling_layout',  # Alias
}

def cleanup_zone(zone_data: Dict[str, Any], zone_name: str) -> Dict[str, Any]:
    """Bereinigt eine einzelne Zone"""
    cleaned = zone_data.copy()
    
    # Entferne verbotene Felder
    removed_fields = []
    for key in FORBIDDEN_ZONE_KEYS:
        if key in cleaned:
            removed_fields.append(key)
            del cleaned[key]
    
    if removed_fields:
        print(f"  🧹 Removed forbidden fields from '{zone_name}': {removed_fields}")
    
    # Stelle sicher, dass z-Index vorhanden ist
    if 'z' not in cleaned:
        if cleaned.get('content_type') == 'image_motiv':
            cleaned['z'] = 0  # Motiv im Hintergrund
        else:
            cleaned['z'] = 1  # Text-Elemente im Vordergrund
        print(f"  ➕ Added z-index to '{zone_name}': {cleaned['z']}")
    
    # Validiere Koordinaten
    required_coords = ['x', 'y', 'width', 'height']
    for coord in required_coords:
        if coord not in cleaned:
            print(f"  ⚠️ Zone '{zone_name}' missing coordinate '{coord}'")
        elif not isinstance(cleaned[coord], int):
            print(f"  ⚠️ Zone '{zone_name}' coordinate '{coord}' is not integer: {cleaned[coord]}")
    
    return cleaned

def cleanup_layout(layout_data: Dict[str, Any]) -> Dict[str, Any]:
    """Bereinigt ein komplettes Layout"""
    cleaned = layout_data.copy()
    
    # Normalisiere layout_type
    old_type = cleaned.get('layout_type', '')
    new_type = LAYOUT_TYPE_MAPPING.get(old_type, old_type)
    if old_type != new_type:
        print(f"  🔄 Mapped layout_type '{old_type}' -> '{new_type}'")
        cleaned['layout_type'] = new_type
    
    # Bereinige Zonen
    if 'zones' in cleaned:
        cleaned_zones = {}
        for zone_name, zone_data in cleaned['zones'].items():
            cleaned_zones[zone_name] = cleanup_zone(zone_data, zone_name)
        cleaned['zones'] = cleaned_zones
    
    # Entferne verbotene Top-Level-Felder
    for key in ['transparency', 'container_style']:
        if key in cleaned:
            del cleaned[key]
            print(f"  🧹 Removed forbidden top-level field: {key}")
    
    return cleaned

def process_layout_file(file_path: Path) -> bool:
    """Verarbeitet eine einzelne Layout-Datei"""
    print(f"🔄 Processing: {file_path.name}")
    
    try:
        # Lade Layout
        with open(file_path, 'r', encoding='utf-8') as f:
            layout_data = yaml.safe_load(f)
        
        if not layout_data:
            print(f"❌ Could not load {file_path.name}")
            return False
        
        # Erstelle Backup
        backup_path = file_path.with_suffix('.yaml.backup')
        if not backup_path.exists():
            with open(backup_path, 'w', encoding='utf-8') as f:
                yaml.dump(layout_data, f, default_flow_style=False, allow_unicode=True)
            print(f"  💾 Created backup: {backup_path.name}")
        
        # Bereinige Layout
        cleaned_data = cleanup_layout(layout_data)
        
        # Schreibe bereinigte Version
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(cleaned_data, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        print(f"✅ {file_path.name} - cleaned successfully")
        return True
        
    except Exception as e:
        print(f"❌ {file_path.name} - error: {e}")
        return False

def main():
    """Hauptfunktion"""
    layouts_dir = Path("input_config/layouts")
    
    if not layouts_dir.exists():
        print(f"❌ Layouts directory not found: {layouts_dir}")
        return
    
    print("🧹 Enhanced Layout Cleanup Script")
    print("=" * 50)
    print("Fixes compatibility issues with new pipeline system:")
    print("- Removes forbidden fields (transparency, container_style)")
    print("- Adds missing z-index values")
    print("- Normalizes layout_type values")
    print("- Validates coordinates")
    print("=" * 50)
    
    success_count = 0
    total_count = 0
    
    for yaml_file in layouts_dir.glob("*.yaml"):
        if yaml_file.name.endswith('.backup'):
            continue
            
        total_count += 1
        if process_layout_file(yaml_file):
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"✅ Successfully processed {success_count}/{total_count} files")
    print("📁 Backups created with .backup extension")
    print()
    print("🧪 Test with: python cli.py run skizze1_vertical_split --ratio 50 --transparency 60")

if __name__ == "__main__":
    main()
