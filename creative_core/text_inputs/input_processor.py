"""
Text Input Processor - Erweiterte Texteingabe und -verarbeitung

Neue Komponente für strukturierte Texteingabe mit Validierung und Formatierung
"""

from typing import Dict, Any, List, Optional
import logging
import re

logger = logging.getLogger(__name__)


class TextInputProcessor:
    """
    Verarbeitet und validiert Texteingaben für die Prompt-Generierung
    """
    
    def __init__(self):
        self.required_fields = ['headline', 'subline', 'company', 'stellentitel', 'cta']
        self.optional_fields = ['location', 'position_long', 'benefits', 'contact_info']
        
        # Validierungsregeln
        self.validation_rules = {
            'headline': {'max_length': 80, 'min_length': 5},
            'subline': {'max_length': 200, 'min_length': 10},
            'company': {'max_length': 50, 'min_length': 2},
            'stellentitel': {'max_length': 100, 'min_length': 5},
            'location': {'max_length': 50, 'min_length': 2},
            'cta': {'max_length': 30, 'min_length': 3},
            'position_long': {'max_length': 500, 'min_length': 20}
        }
    
    def process_text_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verarbeitet Texteingaben und bereitet sie für die Prompt-Generierung vor
        
        Args:
            input_data: Dictionary mit Texteingaben
            
        Returns:
            Verarbeitete und validierte Texte
        """
        try:
            logger.info("🔤 Starte Textverarbeitung...")
            
            # 1. Eingaben extrahieren und normalisieren
            processed_texts = self._extract_and_normalize(input_data)
            
            # 2. Validierung durchführen
            validation_results = self._validate_texts(processed_texts)
            
            # 3. Benefits verarbeiten
            processed_texts['benefits'] = self._process_benefits(input_data.get('benefits', []))
            
            # 4. Metadaten hinzufügen
            processed_texts.update({
                'validation_results': validation_results,
                'processing_timestamp': self._get_timestamp(),
                'text_quality_score': self._calculate_quality_score(processed_texts),
                'ready_for_prompt': validation_results['is_valid']
            })
            
            logger.info(f"✅ Textverarbeitung abgeschlossen. Qualitätsscore: {processed_texts['text_quality_score']}")
            return processed_texts
            
        except Exception as e:
            logger.error(f"❌ Fehler bei Textverarbeitung: {e}")
            return self._get_error_fallback(str(e))
    
    def _extract_and_normalize(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrahiert und normalisiert Texteingaben"""
        processed = {}
        
        for field in self.required_fields + self.optional_fields:
            raw_text = input_data.get(field, '')
            if isinstance(raw_text, str):
                processed[field] = self._normalize_single_text(raw_text, field)
            else:
                processed[field] = str(raw_text) if raw_text else ''
        
        return processed
    
    def _normalize_single_text(self, text: str, field: str) -> str:
        """Normalisiert einen einzelnen Text"""
        if not text:
            return ''
        
        # Grundlegende Normalisierung
        normalized = text.strip()
        normalized = re.sub(r'\s+', ' ', normalized)  # Mehrfache Leerzeichen entfernen
        normalized = normalized.replace('\n', ' ')    # Zeilenumbrüche zu Leerzeichen
        
        # Feldspezifische Normalisierung
        if field in ['headline', 'subline']:
            # Satzzeichen am Ende prüfen
            if normalized and not normalized[-1] in '.!?':
                if field == 'headline':
                    normalized += '!'
                else:
                    normalized += '.'
        
        return normalized
    
    def _validate_texts(self, texts: Dict[str, Any]) -> Dict[str, Any]:
        """Validiert die verarbeiteten Texte"""
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'field_status': {}
        }
        
        # Pflichtfelder prüfen
        for field in self.required_fields:
            text = texts.get(field, '')
            field_valid = True
            field_errors = []
            field_warnings = []
            
            # Länge prüfen
            if field in self.validation_rules:
                rules = self.validation_rules[field]
                
                if len(text) < rules['min_length']:
                    field_errors.append(f"Text zu kurz (min. {rules['min_length']} Zeichen)")
                    field_valid = False
                
                if len(text) > rules['max_length']:
                    field_warnings.append(f"Text sehr lang (max. {rules['max_length']} Zeichen empfohlen)")
            
            # Inhaltliche Prüfung
            if not text.strip():
                field_errors.append("Pflichtfeld ist leer")
                field_valid = False
            
            validation_results['field_status'][field] = {
                'valid': field_valid,
                'errors': field_errors,
                'warnings': field_warnings
            }
            
            if field_errors:
                validation_results['errors'].extend([f"{field}: {err}" for err in field_errors])
                validation_results['is_valid'] = False
            
            if field_warnings:
                validation_results['warnings'].extend([f"{field}: {warn}" for warn in field_warnings])
        
        return validation_results
    
    def _process_benefits(self, benefits_input: Any) -> List[str]:
        """Verarbeitet Benefits-Eingaben"""
        if isinstance(benefits_input, str):
            # String zu Liste konvertieren
            benefits = [b.strip() for b in benefits_input.split('\n') if b.strip()]
        elif isinstance(benefits_input, list):
            benefits = [str(b).strip() for b in benefits_input if str(b).strip()]
        else:
            benefits = []
        
        # Fallback wenn keine Benefits
        if not benefits:
            benefits = [
                "Flexible Arbeitszeiten",
                "Attraktive Vergütung", 
                "Fortbildungsmöglichkeiten"
            ]
        
        # Maximal 5 Benefits, jeweils max. 50 Zeichen
        processed_benefits = []
        for benefit in benefits[:5]:
            if len(benefit) > 50:
                benefit = benefit[:47] + "..."
            processed_benefits.append(benefit)
        
        return processed_benefits
    
    def _calculate_quality_score(self, texts: Dict[str, Any]) -> float:
        """Berechnet einen Qualitätsscore für die Texte"""
        score = 0.0
        max_score = 100.0
        
        # Vollständigkeit (40 Punkte)
        required_filled = sum(1 for field in self.required_fields if texts.get(field, '').strip())
        score += (required_filled / len(self.required_fields)) * 40
        
        # Textlängen (30 Punkte)
        length_scores = []
        for field in ['headline', 'subline']:
            text = texts.get(field, '')
            if field in self.validation_rules:
                rules = self.validation_rules[field]
                ideal_length = (rules['min_length'] + rules['max_length']) / 2
                length_ratio = min(len(text) / ideal_length, 1.0) if ideal_length > 0 else 0
                length_scores.append(length_ratio)
        
        if length_scores:
            score += (sum(length_scores) / len(length_scores)) * 30
        
        # Benefits (20 Punkte)
        benefits = texts.get('benefits', [])
        if benefits and len(benefits) >= 3:
            score += 20
        elif benefits and len(benefits) >= 1:
            score += 10
        
        # Zusätzliche Felder (10 Punkte)
        optional_filled = sum(1 for field in self.optional_fields if texts.get(field, '').strip())
        score += (optional_filled / len(self.optional_fields)) * 10
        
        return round(score, 1)
    
    def _get_timestamp(self) -> str:
        """Gibt aktuellen Zeitstempel zurück"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _get_error_fallback(self, error_msg: str) -> Dict[str, Any]:
        """Fallback bei Fehlern"""
        return {
            'headline': 'Werden Sie Teil unseres Teams!',
            'subline': 'Flexible Arbeitszeiten und attraktive Vergütung.',
            'company': 'Musterfirma GmbH',
            'stellentitel': 'Pflegekraft (m/w/d)',
            'location': 'Berlin',
            'cta': 'Jetzt bewerben!',
            'benefits': ['Flexible Arbeitszeiten', 'Attraktive Vergütung', 'Fortbildungsmöglichkeiten'],
            'validation_results': {
                'is_valid': False,
                'errors': [f'Textverarbeitung fehlgeschlagen: {error_msg}'],
                'warnings': [],
                'field_status': {}
            },
            'text_quality_score': 0.0,
            'ready_for_prompt': False,
            'fallback_used': True
        }


def create_text_processor() -> TextInputProcessor:
    """Factory-Funktion für TextInputProcessor"""
    return TextInputProcessor()

