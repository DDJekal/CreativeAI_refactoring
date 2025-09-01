"""
Motif Input Processor - Erweiterte Motiveingabe und -verarbeitung

Neue Komponente für strukturierte Motiveingabe mit automatischer Generierung
"""

from typing import Dict, Any, List, Optional, Union
import logging
import random

logger = logging.getLogger(__name__)


class MotifInputProcessor:
    """
    Verarbeitet und generiert Motiv-Eingaben für die Bildgenerierung
    """
    
    def __init__(self):
        # Vordefinierte Motivkategorien
        self.motif_categories = {
            'pflege': {
                'keywords': ['pflege', 'krankenhaus', 'klinik', 'patient', 'medizin', 'gesundheit'],
                'base_prompts': [
                    "Professionelle Pflegekraft in modernem Krankenhaus",
                    "Freundliche Krankenschwester im Gespräch mit Patient",
                    "Pflegeteam in heller, moderner Klinik"
                ],
                'environments': ['Krankenhaus', 'Pflegeheim', 'Klinik', 'Praxis'],
                'personas': ['Pflegekraft', 'Krankenschwester', 'Pfleger', 'Stationsleitung']
            },
            'technik': {
                'keywords': ['entwickler', 'programmierer', 'software', 'it', 'digital', 'technologie'],
                'base_prompts': [
                    "Professioneller Entwickler am modernen Arbeitsplatz",
                    "IT-Team in offenem Büro mit Monitoren",
                    "Software-Entwicklerin vor Code-Editor"
                ],
                'environments': ['Büro', 'Coworking Space', 'Tech-Startup', 'Labor'],
                'personas': ['Entwickler', 'Programmiererin', 'IT-Spezialist', 'Tech-Lead']
            },
            'beratung': {
                'keywords': ['berater', 'consulting', 'strategie', 'management', 'planung'],
                'base_prompts': [
                    "Professioneller Berater im Kundengespräch",
                    "Business-Team bei Strategiemeeting",
                    "Consultant vor Präsentation"
                ],
                'environments': ['Konferenzraum', 'Büro', 'Meeting-Raum', 'Coworking'],
                'personas': ['Berater', 'Consultant', 'Manager', 'Strategin']
            }
        }
        
        # Visuelle Stile
        self.visual_styles = {
            'professionell': {
                'lighting': 'Natürlich, professionell',
                'mood': 'Vertrauensvoll, kompetent',
                'colors': 'Dezente, professionelle Farben'
            },
            'modern': {
                'lighting': 'Helles, modernes Licht',
                'mood': 'Dynamisch, innovativ',
                'colors': 'Moderne, frische Farben'
            },
            'freundlich': {
                'lighting': 'Warmes, einladendes Licht',
                'mood': 'Freundlich, zugänglich',
                'colors': 'Warme, einladende Farben'
            }
        }
    
    def process_motif_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verarbeitet Motiv-Eingaben und generiert vollständige Motiv-Spezifikation
        
        Args:
            input_data: Dictionary mit Motiv-Eingaben und Kontext
            
        Returns:
            Vollständige Motiv-Spezifikation
        """
        try:
            logger.info("🎨 Starte Motiv-Verarbeitung...")
            
            # 1. Eingabetyp bestimmen
            input_type = self._determine_input_type(input_data)
            
            # 2. Motiv generieren basierend auf Eingabetyp
            if input_type == 'text_description':
                motif_spec = self._process_text_description(input_data)
            elif input_type == 'auto_generate':
                motif_spec = self._auto_generate_motif(input_data)
            elif input_type == 'image_upload':
                motif_spec = self._process_image_upload(input_data)
            else:
                motif_spec = self._get_default_motif()
            
            # 3. Visuelle Parameter hinzufügen
            motif_spec = self._add_visual_parameters(motif_spec, input_data)
            
            # 4. Qualität bewerten
            quality_score = self._evaluate_quality(motif_spec)
            motif_spec['quality_score'] = quality_score
            
            # 5. Status setzen
            motif_spec['ready_for_generation'] = quality_score >= 70
            motif_spec['processing_success'] = True
            
            logger.info(f"✅ Motiv-Verarbeitung abgeschlossen. Qualität: {quality_score}%")
            return motif_spec
            
        except Exception as e:
            logger.error(f"❌ Fehler bei Motiv-Verarbeitung: {e}")
            return self._get_error_result(str(e))
    
    def _determine_input_type(self, input_data: Dict[str, Any]) -> str:
        """Bestimmt den Eingabetyp für die Motiv-Generierung"""
        if input_data.get('uploaded_image'):
            return 'image_upload'
        elif input_data.get('motiv_prompt'):
            return 'text_description'
        else:
            return 'auto_generate'
    
    def _process_text_description(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verarbeitet manuelle Text-Beschreibungen"""
        motiv_prompt = input_data.get('motiv_prompt', '')
        
        # Kategorie basierend auf Stellentitel bestimmen
        category = self._determine_category(input_data.get('stellentitel', ''))
        
        return {
            'motiv_prompt': motiv_prompt,
            'category': category,
            'generation_method': 'text_description',
            'persona': self._extract_persona(input_data.get('stellentitel', '')),
            'environment': self._suggest_environment(category),
            'visual_style': input_data.get('visual_style', 'Professionell'),
            'lighting_type': input_data.get('lighting_type', 'Natürlich'),
            'lighting_mood': input_data.get('lighting_mood', 'Professionell'),
            'framing': input_data.get('framing', 'Medium Shot')
        }
    
    def _auto_generate_motif(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generiert automatisch ein Motiv basierend auf Stellendaten"""
        stellentitel = input_data.get('stellentitel', '').lower()
        company = input_data.get('company', '')
        location = input_data.get('location', '')
        
        # Kategorie bestimmen
        category = self._determine_category(stellentitel)
        
        # Motiv generieren
        if category in self.motif_categories:
            category_data = self.motif_categories[category]
            base_prompt = random.choice(category_data['base_prompts'])
            
            # Kontext hinzufügen
            if company:
                base_prompt += f" bei {company}"
            if location:
                base_prompt += f" in {location}"
            
            return {
                'motiv_prompt': base_prompt,
                'category': category,
                'generation_method': 'auto_generate',
                'persona': random.choice(category_data['personas']),
                'environment': random.choice(category_data['environments']),
                'visual_style': 'Professionell',
                'lighting_type': 'Natürlich',
                'lighting_mood': 'Professionell',
                'framing': 'Medium Shot'
            }
        else:
            return self._get_default_motif()
    
    def _process_image_upload(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verarbeitet hochgeladene Bilder mit zusätzlicher Beschreibung"""
        motiv_prompt = input_data.get('motiv_prompt', '')
        uploaded_image = input_data.get('uploaded_image')
        
        # Basis-Motiv aus Bild + Beschreibung
        if motiv_prompt:
            base_prompt = f"Motiv basierend auf hochgeladenem Bild: {motiv_prompt}"
        else:
            base_prompt = "Professionelles Motiv basierend auf hochgeladenem Bild"
        
        return {
            'motiv_prompt': base_prompt,
            'category': 'custom',
            'generation_method': 'image_upload',
            'persona': self._extract_persona(input_data.get('stellentitel', '')),
            'environment': 'Custom Environment',
            'visual_style': input_data.get('visual_style', 'Professionell'),
            'lighting_type': input_data.get('lighting_type', 'Natürlich'),
            'lighting_mood': input_data.get('lighting_mood', 'Professionell'),
            'framing': input_data.get('framing', 'Medium Shot'),
            'has_uploaded_image': True
        }
    
    def _determine_category(self, stellentitel: str) -> str:
        """Bestimmt die Motiv-Kategorie basierend auf dem Stellentitel"""
        stellentitel_lower = stellentitel.lower()
        
        for category, data in self.motif_categories.items():
            if any(keyword in stellentitel_lower for keyword in data['keywords']):
                return category
        
        return 'allgemein'
    
    def _extract_persona(self, stellentitel: str) -> str:
        """Extrahiert die Persona aus dem Stellentitel"""
        if 'pflege' in stellentitel.lower():
            return 'Pflegekraft'
        elif 'entwickler' in stellentitel.lower() or 'programmierer' in stellentitel.lower():
            return 'Entwickler'
        elif 'berater' in stellentitel.lower():
            return 'Berater'
        else:
            return 'Professioneller Mitarbeiter'
    
    def _suggest_environment(self, category: str) -> str:
        """Schlägt eine passende Umgebung vor"""
        if category in self.motif_categories:
            return random.choice(self.motif_categories[category]['environments'])
        return 'Professionelle Arbeitsumgebung'
    
    def _add_visual_parameters(self, motif_spec: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fügt visuelle Parameter zur Motiv-Spezifikation hinzu"""
        visual_style = input_data.get('visual_style', 'Professionell').lower()
        
        if visual_style in self.visual_styles:
            style_data = self.visual_styles[visual_style]
            motif_spec.update({
                'lighting_description': style_data['lighting'],
                'mood_description': style_data['mood'],
                'color_description': style_data['colors']
            })
        
        return motif_spec
    
    def _evaluate_quality(self, motif_spec: Dict[str, Any]) -> int:
        """Bewertet die Qualität der Motiv-Spezifikation"""
        score = 0
        
        # Basis-Punktzahl
        if motif_spec.get('motiv_prompt'):
            score += 30
        
        if motif_spec.get('category'):
            score += 20
        
        if motif_spec.get('persona'):
            score += 15
        
        if motif_spec.get('environment'):
            score += 15
        
        if motif_spec.get('visual_style'):
            score += 10
        
        if motif_spec.get('lighting_type'):
            score += 5
        
        if motif_spec.get('framing'):
            score += 5
        
        return min(score, 100)
    
    def _get_default_motif(self) -> Dict[str, Any]:
        """Fallback-Motiv wenn keine spezifischen Daten verfügbar sind"""
        return {
            'motiv_prompt': 'Professioneller Mitarbeiter in moderner Arbeitsumgebung',
            'category': 'allgemein',
            'generation_method': 'default',
            'persona': 'Professioneller Mitarbeiter',
            'environment': 'Moderne Arbeitsumgebung',
            'visual_style': 'Professionell',
            'lighting_type': 'Natürlich',
            'lighting_mood': 'Professionell',
            'framing': 'Medium Shot'
        }
    
    def _get_error_result(self, error_msg: str) -> Dict[str, Any]:
        """Fehler-Ergebnis"""
        return {
            'motiv_prompt': 'Professionelles Motiv (Fehler bei der Verarbeitung)',
            'category': 'allgemein',
            'generation_method': 'error',
            'persona': 'Professioneller Mitarbeiter',
            'environment': 'Arbeitsumgebung',
            'visual_style': 'Professionell',
            'lighting_type': 'Natürlich',
            'lighting_mood': 'Professionell',
            'framing': 'Medium Shot',
            'ready_for_generation': False,
            'processing_success': False,
            'error': error_msg,
            'quality_score': 0
        }


def create_motif_processor() -> MotifInputProcessor:
    """Factory-Funktion für MotifInputProcessor"""
    return MotifInputProcessor()
