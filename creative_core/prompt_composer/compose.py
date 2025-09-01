"""
Prompt Composer - Finale Prompt-Komposition

Migriert aus PromptFinalizer._generate_dalle_prompt() und _generate_midjourney_prompt()
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def compose(layout: Dict[str, Any], design: Dict[str, Any], 
            texts: Dict[str, Any], motive: Dict[str, Any]) -> str:
    """
    Komponiert alle Eingaben zu finalem DALL-E Prompt
    
    Args:
        layout: Layout-Definition und -Metadaten (muss __validated__=True haben)
        design: CI-Farben und Design-Regeln (muss __validated__=True haben)
        texts: Normalisierte und vorbereitete Texte
        motive: Motiv-Spezifikation und Visual-Styles
        
    Returns:
        Finaler DALL-E Prompt als String
        
    Raises:
        ValueError: Wenn Layout oder Design nicht validiert sind
    """
    # COMPOSER-GATE: Strikte Validierung der Eingaben
    if not layout.get("__validated__"):
        raise ValueError("Layout must be validated before composition")
    if not design.get("__validated__"):
        raise ValueError("Design must be validated before composition")
    
    try:
        # Neue Reihenfolge: Layout → Design & CI → Texte → Motiv
        prompt_parts = []
        
        # 1. Layout-Informationen (Startpunkt)
        if layout.get('text_areas'):
            prompt_parts.append(f"Layout: {motive.get('layout_id', 'standard')} mit {len(layout['text_areas'])} Text-Bereichen")
        
        # 2. Design & CI-Informationen
        if design.get('colors', {}).get('primary'):
            prompt_parts.append(f"Primärfarbe: {design['colors']['primary']}")
        if design.get('colors', {}).get('secondary'):
            prompt_parts.append(f"Sekundärfarbe: {design['colors']['secondary']}")
        if design.get('colors', {}).get('accent'):
            prompt_parts.append(f"Akzentfarbe: {design['colors']['accent']}")
        
        # 3. Text-Elemente
        if texts.get('headline'):
            prompt_parts.append(f"Headline: {texts['headline']}")
        if texts.get('subline'):
            prompt_parts.append(f"Subline: {texts['subline']}")
        if texts.get('cta'):
            prompt_parts.append(f"CTA: {texts['cta']}")
        if texts.get('benefits'):
            benefits_text = ", ".join(texts['benefits'][:3])  # Max 3 Benefits
            prompt_parts.append(f"Benefits: {benefits_text}")
        
        # 4. Motiv-Spezifikation (Endpunkt)
        prompt_parts.append(motive.get('motiv_prompt', 'Professionelle Person in moderner Umgebung'))
        prompt_parts.append(f"Stil: {motive.get('visual_style', 'Professionell')}")
        prompt_parts.append(f"Beleuchtung: {motive.get('lighting_type', 'Natürlich')}")
        prompt_parts.append(f"Framing: {motive.get('framing', 'Medium Shot')}")
        
        # Zusätzliche Motiv-Details
        if motive.get('persona'):
            prompt_parts.append(f"Persona: {motive['persona']}")
        if motive.get('environment'):
            prompt_parts.append(f"Umgebung: {motive['environment']}")
        
        # Prompt zusammenfügen (aus _generate_dalle_prompt() migriert)
        final_prompt = " | ".join(prompt_parts)
        
        logger.info(f"Prompt komponiert: {len(prompt_parts)} Komponenten, {len(final_prompt)} Zeichen")
        return final_prompt
        
    except Exception as e:
        logger.error(f"Fehler bei Prompt-Komposition: {e}")
        return _get_fallback_prompt()


def _get_fallback_prompt() -> str:
    """Fallback-Prompt wenn Komposition fehlschlägt"""
    return "Professionelle Person in moderner Umgebung | Layout: standard | Stil: Professionell | Beleuchtung: Natürlich | Framing: Medium Shot"
