"""
Motive Specification - Motiv-Spezifikationen und -Prompts

Migriert aus InputProcessor.process() - motiv-bezogene Felder und Visual-Styles
"""

from typing import Dict, Any, Union
import logging

logger = logging.getLogger(__name__)


def build_motive_spec(user_input_yaml: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Erstellt Motiv-Spezifikation für Bildgenerierung
    
    Args:
        user_input_yaml: Benutzereingaben als YAML-String oder Dict
        
    Returns:
        Dict mit Motiv-Spezifikation und Visual-Styles
    """
    try:
        # Input-Daten extrahieren (aus InputProcessor.process() migriert)
        if isinstance(user_input_yaml, str):
            # TODO: YAML-Parsing implementieren
            input_data = _parse_yaml_input(user_input_yaml)
        else:
            input_data = user_input_yaml or {}
        
        # Motiv-bezogene Felder extrahieren (aus InputProcessor.process() migriert)
        motiv_prompt = input_data.get('motiv_prompt', 'Professionelle Person in moderner Umgebung')
        visual_style = input_data.get('visual_style', 'Professionell')
        lighting_type = input_data.get('lighting_type', 'Natürlich')
        lighting_mood = input_data.get('lighting_mood', 'Professionell')
        framing = input_data.get('framing', 'Medium Shot')
        layout_id = input_data.get('layout_id', 'skizze1_vertical_split')
        
        # Layout-Style-Daten (aus InputProcessor.process() migriert)
        layout_style = input_data.get('layout_style', ('rounded_modern', '🔵 Abgerundet & Modern'))
        container_shape = input_data.get('container_shape', ('rounded_rectangle', '📱 Abgerundet'))
        border_style = input_data.get('border_style', ('soft_shadow', '🌫️ Weicher Schatten'))
        texture_style = input_data.get('texture_style', ('gradient', '🌈 Farbverlauf'))
        background_treatment = input_data.get('background_treatment', ('subtle_pattern', '🌸 Subtiles Muster'))
        corner_radius = input_data.get('corner_radius', ('medium', '⌜ Mittel'))
        accent_elements = input_data.get('accent_elements', ('modern_minimal', '⚪ Modern Minimal'))
        
        # Neue Layout-Proportionen (aus InputProcessor.process() migriert)
        image_text_ratio = input_data.get('image_text_ratio', 50)
        container_transparency = input_data.get('container_transparency', 0)
        
        # Zusätzliche Motiv-Felder mit Defaults
        persona = input_data.get('persona', 'professionell')
        shot_type = input_data.get('shot_type', 'medium_close')
        environment = input_data.get('environment', 'modern_office')
        
        result = {
            'motiv_prompt': motiv_prompt,
            'visual_style': visual_style,
            'lighting_type': lighting_type,
            'lighting_mood': lighting_mood,
            'framing': framing,
            'layout_id': layout_id,
            'layout_style': layout_style,
            'container_shape': container_shape,
            'border_style': border_style,
            'texture_style': texture_style,
            'background_treatment': background_treatment,
            'corner_radius': corner_radius,
            'accent_elements': accent_elements,
            'image_text_ratio': image_text_ratio,
            'container_transparency': container_transparency,
            'persona': persona,
            'shot_type': shot_type,
            'environment': environment
        }
        
        logger.info(f"✅ Motiv-Spezifikation erstellt: {visual_style} Style, {lighting_type} Lighting, {framing}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Fehler bei Motiv-Spezifikation: {e}")
        return _get_fallback_motive()


def _parse_yaml_input(yaml_string: str) -> Dict[str, Any]:
    """Parst YAML-Input-String (Fallback-Implementierung)"""
    # TODO: Echte YAML-Parsing implementieren
    logger.warning("YAML-Parsing noch nicht implementiert - verwende Fallback")
    return {}


def _get_fallback_motive() -> Dict[str, Any]:
    """Fallback-Motiv wenn Motiv-Spezifikation fehlschlägt"""
    return {
        'motiv_prompt': 'Professionelle Person in moderner Umgebung',
        'visual_style': 'Professionell',
        'lighting_type': 'Natürlich',
        'lighting_mood': 'Professionell',
        'framing': 'Medium Shot',
        'layout_id': 'skizze1_vertical_split',
        'layout_style': ('rounded_modern', '🔵 Abgerundet & Modern'),
        'container_shape': ('rounded_rectangle', '📱 Abgerundet'),
        'border_style': ('soft_shadow', '🌫️ Weicher Schatten'),
        'texture_style': ('gradient', '🌈 Farbverlauf'),
        'background_treatment': ('subtle_pattern', '🌸 Subtiles Muster'),
        'corner_radius': ('medium', '⌜ Mittel'),
        'accent_elements': ('modern_minimal', '⚪ Modern Minimal'),
        'image_text_ratio': 50,
        'container_transparency': 0,
        'persona': 'professionell',
        'shot_type': 'medium_close',
        'environment': 'modern_office'
    }
