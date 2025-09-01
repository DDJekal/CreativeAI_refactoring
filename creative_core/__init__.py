"""
CreativeAI Core - Modularisierte Pipeline für Prompt-Generierung

Dieses Paket enthält die 5 Hauptmodule für die Modularisierung:
- layout: Layout-Definitionen und -Ladung
- design_ci: CI-Farben und Design-Regeln
- text_inputs: Text-Normalisierung und -Vorbereitung
- motive_inputs: Motiv-Spezifikationen
- prompt_composer: Finale Prompt-Komposition
"""

__version__ = "1.0.0"
__author__ = "CreativeAI Team"

# Layout Module
from .layout.loader import (
    load_layout, load_layout_cached, list_available_layouts, 
    get_layout_info, validate_layout_file
)
from .layout.engine import layout_engine, calculate_layout_coordinates_cached

# Design CI Module
from .design_ci.rules import apply_rules, apply_rules_legacy, DesignValidationError

# Text Inputs Module
from .text_inputs.normalize import prepare_texts

# Motive Inputs Module
from .motive_inputs.spec import build_motive_spec

# Prompt Composer Module
from .prompt_composer.compose import compose

__all__ = [
    # Layout
    'load_layout', 'load_layout_cached', 'list_available_layouts', 
    'get_layout_info', 'validate_layout_file', 'layout_engine', 
    'calculate_layout_coordinates_cached',
    
    # Design CI
    'apply_rules', 'apply_rules_legacy', 'DesignValidationError',
    
    # Text Inputs
    'prepare_texts',
    
    # Motive Inputs
    'build_motive_spec',
    
    # Prompt Composer
    'compose'
]
