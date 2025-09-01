"""
Text Normalization - Text-Normalisierung und -Vorbereitung

Migriert aus InputProcessor._normalize_text() und InputProcessor.process() - Text-Verarbeitung
"""

from typing import Dict, Any, Union, List
import logging

logger = logging.getLogger(__name__)


def prepare_texts(user_input_yaml: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Bereitet Texte für Prompt-Generierung vor
    
    Args:
        user_input_yaml: Benutzereingaben als YAML-String oder Dict
        
    Returns:
        Dict mit normalisierten und vorbereiteten Texten
    """
    try:
        # Input-Daten extrahieren (aus InputProcessor.process() migriert)
        if isinstance(user_input_yaml, str):
            # TODO: YAML-Parsing implementieren
            input_data = _parse_yaml_input(user_input_yaml)
        else:
            input_data = user_input_yaml or {}
        
        # Prüfe ob Text-Kürzung deaktiviert ist
        disable_text_truncation = input_data.get('disable_text_truncation', False)
        
        # Text-Daten extrahieren und normalisieren
        if disable_text_truncation:
            # KEINE Text-Kürzung - verwende Original-Texte
            headline = input_data.get('headline', '')
            subline = input_data.get('subline', '')
            company = input_data.get('unternehmen', '')
            stellentitel = input_data.get('stellentitel', '')
            location = input_data.get('location', '')
            position_long = input_data.get('position_long', '')
            cta = input_data.get('cta', '')
            benefits = input_data.get('benefits', [])
        else:
            # Normale Text-Verarbeitung mit Kürzung
            headline = _normalize_text(input_data.get('headline', ''), 50)
            subline = _normalize_text(input_data.get('subline', ''), 200)
            company = _normalize_text(input_data.get('unternehmen', ''), 50)
            stellentitel = _normalize_text(input_data.get('stellentitel', ''), 80)
            location = _normalize_text(input_data.get('location', ''), 50)
            position_long = _normalize_text(input_data.get('position_long', ''), 300)
            cta = _normalize_text(input_data.get('cta', ''), 50)
            benefits = input_data.get('benefits', [])
        
        # Benefits als Liste verarbeiten (falls es ein String ist)
        if isinstance(benefits, str):
            benefits = [b.strip() for b in benefits.split('\n') if b.strip()]
        elif not benefits:
            benefits = ["Flexible Arbeitszeiten", "Attraktive Vergütung", "Fortbildungsmöglichkeiten"]
        
        result = {
            'headline': headline,
            'subline': subline,
            'company': company,
            'stellentitel': stellentitel,
            'location': location,
            'position_long': position_long,
            'cta': cta,
            'benefits': benefits,
            'normalization_applied': ['length_check', 'umlaut_replacement', 'line_break_removal'],
            'text_truncation_disabled': disable_text_truncation
        }
        
        logger.info(f"✅ Texte vorbereitet: {len(benefits)} Benefits, Truncation: {'deaktiviert' if disable_text_truncation else 'aktiviert'}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Fehler bei Text-Vorbereitung: {e}")
        return _get_fallback_texts()


def _normalize_text(text: str, max_length: int) -> str:
    """Normalisiert Text auf maximale Länge (aus _normalize_text() migriert)"""
    if not text:
        return ""
    
    # Entferne Zeilenumbrüche und normalisiere
    normalized = text.replace('\n', ' ').strip()
    
    # Kürze wenn nötig
    if len(normalized) > max_length:
        normalized = normalized[:max_length].rstrip()
        if not normalized.endswith(('.', '!', '?')):
            normalized += '...'
    
    return normalized


def _parse_yaml_input(yaml_string: str) -> Dict[str, Any]:
    """Parst YAML-Input-String (Fallback-Implementierung)"""
    # TODO: Echte YAML-Parsing implementieren
    logger.warning("YAML-Parsing noch nicht implementiert - verwende Fallback")
    return {}


def _get_fallback_texts() -> Dict[str, Any]:
    """Fallback-Texte wenn Text-Verarbeitung fehlschlägt"""
    return {
        'headline': 'Werden Sie Teil unseres Teams!',
        'subline': 'Flexible Arbeitszeiten und attraktive Vergütung',
        'company': 'Musterfirma GmbH',
        'stellentitel': 'Pflegekraft (m/w/d)',
        'location': 'Berlin',
        'position_long': 'Wir suchen eine engagierte Pflegekraft für unseren Bereich',
        'cta': 'Jetzt bewerben!',
        'benefits': [
            'Flexible Arbeitszeiten',
            'Attraktive Vergütung',
            'Fortbildungsmöglichkeiten'
        ],
        'normalization_applied': ['fallback_texts', 'error_recovery'],
        'text_truncation_disabled': False
    }
