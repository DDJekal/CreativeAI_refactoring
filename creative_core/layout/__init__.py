"""
Layout Module für dynamische Layouts mit Slider-Integration

Dieses Modul bietet:
- Dynamische Layout-Ladung basierend auf Slider-Werten
- Koordinatenberechnung für verschiedene Layout-Typen
- Transparenz-Integration für alle Container
- Layout-Validierung und Fallbacks
"""

from .loader import (
    load_layout,
    load_layout_cached,
    list_available_layouts,
    get_layout_info,
    validate_layout_file
)

from .engine import (
    layout_engine,
    calculate_layout_coordinates_cached
)

__all__ = [
    # Layout-Loader Funktionen
    'load_layout',
    'load_layout_cached',
    'list_available_layouts',
    'get_layout_info',
    'validate_layout_file',
    
    # Layout-Engine
    'layout_engine',
    'calculate_layout_coordinates_cached'
]

__version__ = "1.0.0"
__description__ = "Dynamische Layout-Engine mit Slider-Integration"
