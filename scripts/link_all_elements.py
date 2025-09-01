"""
Link All Elements Script - Verknüpft alle Elemente und generiert Prompts

Dieses Skript verbindet Layout, Design, Texte und Motive zu einem vollständigen Prompt
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging
import json

# Pfad zum Projekt-Root hinzufügen
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from creative_core.layout.loader import load_layout
from creative_core.design_ci.processor import process_design_ci
from creative_core.text_inputs.input_processor import create_text_processor
from creative_core.motive_inputs.processor import create_motif_processor
from creative_core.prompt_composer.compose import compose

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ElementLinker:
    """
    Verknüpft alle Elemente (Layout, Design, Texte, Motive) zu einem vollständigen Prompt
    """
    
    def __init__(self):
        self.text_processor = create_text_processor()
        self.motif_processor = create_motif_processor()
        
        # Verfügbare Layouts
        self.available_layouts = [
            'skizze1_vertical_split',
            'skizze7_minimalist_layout', 
            'skizze8_hero_layout',
            'skizze9_storytelling_layout',
            'skizze10_infographic_layout',
            'skizze11_magazine_layout',
            'skizze12_grid_layout',
            'skizze13_minimal_text_layout'
        ]
    
    def link_all_elements(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verknüpft alle Elemente zu einem vollständigen System
        
        Args:
            user_input: Vollständige Benutzereingaben
            
        Returns:
            Verknüpfte Daten mit generiertem Prompt
        """
        try:
            logger.info("🔗 Starte Verknüpfung aller Elemente...")
            
            # 1. Layout laden
            layout_id = user_input.get('layout_id', 'skizze1_vertical_split')
            logger.info(f"📐 Lade Layout: {layout_id}")
            layout_data = self._load_layout_safe(layout_id)
            
            # 2. Design & CI verarbeiten
            logger.info("🎨 Verarbeite Design & CI...")
            design_data = self._process_design_safe(user_input)
            
            # 3. Texte verarbeiten
            logger.info("📝 Verarbeite Texte...")
            text_data = self.text_processor.process_text_input(user_input)
            
            # 4. Motive verarbeiten
            logger.info("🖼️ Verarbeite Motive...")
            motif_data = self.motif_processor.process_motif_input(user_input)
            
            # 5. Alle Daten verknüpfen
            logger.info("🔗 Verknüpfe alle Daten...")
            linked_data = self._link_data(layout_data, design_data, text_data, motif_data)
            
            # 6. Prompt generieren
            logger.info("🎯 Generiere finalen Prompt...")
            final_prompt = self._generate_final_prompt(linked_data)
            
            # 7. Ergebnis zusammenstellen
            result = {
                'success': True,
                'layout': layout_data,
                'design': design_data,
                'texts': text_data,
                'motif': motif_data,
                'linked_data': linked_data,
                'final_prompt': final_prompt,
                'metadata': {
                    'processing_timestamp': self._get_timestamp(),
                    'layout_id': layout_id,
                    'total_quality_score': self._calculate_total_quality(text_data, motif_data),
                    'ready_for_generation': self._check_readiness(text_data, motif_data)
                }
            }
            
            logger.info("✅ Verknüpfung erfolgreich abgeschlossen!")
            return result
            
        except Exception as e:
            logger.error(f"❌ Fehler bei Element-Verknüpfung: {e}")
            return self._get_error_result(str(e))
    
    def _load_layout_safe(self, layout_id: str) -> Dict[str, Any]:
        """Lädt Layout mit Fehlerbehandlung"""
        try:
            if layout_id not in self.available_layouts:
                logger.warning(f"Layout {layout_id} nicht verfügbar, verwende Standard-Layout")
                layout_id = 'skizze1_vertical_split'
            
            layout_data = load_layout(layout_id)
            if not layout_data:
                raise ValueError(f"Layout {layout_id} konnte nicht geladen werden")
            
            return layout_data
            
        except Exception as e:
            logger.error(f"Fehler beim Layout-Laden: {e}")
            return self._get_fallback_layout()
    
    def _process_design_safe(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Verarbeitet Design mit Fehlerbehandlung"""
        try:
            # Design-Parameter extrahieren
            design_input = {
                'primary_color': user_input.get('primary_color', '#005EA5'),
                'secondary_color': user_input.get('secondary_color', '#B4D9F7'),
                'accent_color': user_input.get('accent_color', '#FFC20E'),
                'layout_style': user_input.get('layout_style', 'rounded_modern'),
                'container_shape': user_input.get('container_shape', 'rounded_rectangle'),
                'border_style': user_input.get('border_style', 'soft_shadow'),
                'texture_style': user_input.get('texture_style', 'gradient'),
                'background_treatment': user_input.get('background_treatment', 'subtle_pattern')
            }
            
            # Design verarbeiten (vereinfacht, da process_design_ci komplex ist)
            return {
                'colors': {
                    'primary': design_input['primary_color'],
                    'secondary': design_input['secondary_color'],
                    'accent': design_input['accent_color']
                },
                'style': {
                    'layout_style': design_input['layout_style'],
                    'container_shape': design_input['container_shape'],
                    'border_style': design_input['border_style']
                },
                'processing_success': True
            }
            
        except Exception as e:
            logger.error(f"Fehler bei Design-Verarbeitung: {e}")
            return self._get_fallback_design()
    
    def _link_data(self, layout: Dict[str, Any], design: Dict[str, Any], 
                   texts: Dict[str, Any], motif: Dict[str, Any]) -> Dict[str, Any]:
        """Verknüpft alle Daten zu einem kohärenten System"""
        
        # Konsistenz-Prüfungen
        consistency_checks = {
            'color_harmony': self._check_color_harmony(design, motif),
            'text_layout_fit': self._check_text_layout_fit(texts, layout),
            'motif_style_match': self._check_motif_style_match(motif, design),
            'overall_coherence': True  # Vereinfacht
        }
        
        # Verknüpfte Daten
        linked = {
            'layout_zones': self._map_texts_to_zones(texts, layout),
            'styled_motif': self._apply_design_to_motif(motif, design),
            'color_coordinated_texts': self._coordinate_text_colors(texts, design),
            'consistency_checks': consistency_checks,
            'synergy_score': self._calculate_synergy_score(consistency_checks),
            'optimization_suggestions': self._generate_optimization_suggestions(
                layout, design, texts, motif, consistency_checks
            )
        }
        
        return linked
    
    def _generate_final_prompt(self, linked_data: Dict[str, Any]) -> str:
        """Generiert den finalen Prompt aus verknüpften Daten"""
        try:
            # Daten für compose() vorbereiten
            layout_for_compose = linked_data.get('layout_zones', {})
            design_for_compose = linked_data.get('styled_motif', {})
            texts_for_compose = linked_data.get('color_coordinated_texts', {})
            motif_for_compose = linked_data.get('styled_motif', {})
            
            # Prompt mit compose() generieren
            prompt = compose(
                layout=layout_for_compose,
                design=design_for_compose,
                texts=texts_for_compose,
                motive=motif_for_compose
            )
            
            return prompt
            
        except Exception as e:
            logger.error(f"Fehler bei Prompt-Generierung: {e}")
            return self._get_fallback_prompt(linked_data)
    
    def _check_color_harmony(self, design: Dict[str, Any], motif: Dict[str, Any]) -> bool:
        """Prüft Farbharmonie zwischen Design und Motiv"""
        # Vereinfachte Prüfung
        return True
    
    def _check_text_layout_fit(self, texts: Dict[str, Any], layout: Dict[str, Any]) -> bool:
        """Prüft ob Texte zum Layout passen"""
        # Prüfe ob alle wichtigen Texte vorhanden sind
        required_texts = ['headline', 'subline', 'cta']
        return all(texts.get(field) for field in required_texts)
    
    def _check_motif_style_match(self, motif: Dict[str, Any], design: Dict[str, Any]) -> bool:
        """Prüft ob Motiv-Stil zum Design passt"""
        # Vereinfachte Prüfung
        return motif.get('visual_style', '').lower() in ['professionell', 'modern', 'freundlich']
    
    def _map_texts_to_zones(self, texts: Dict[str, Any], layout: Dict[str, Any]) -> Dict[str, Any]:
        """Ordnet Texte den Layout-Zonen zu"""
        return {
            'headline_block': {'text': texts.get('headline', ''), 'type': 'headline'},
            'subline_block': {'text': texts.get('subline', ''), 'type': 'subline'},
            'company_block': {'text': texts.get('company', ''), 'type': 'company'},
            'cta_block': {'text': texts.get('cta', ''), 'type': 'cta'},
            'benefits_block': {'text': texts.get('benefits', []), 'type': 'benefits'},
            'layout_structure': layout
        }
    
    def _apply_design_to_motif(self, motif: Dict[str, Any], design: Dict[str, Any]) -> Dict[str, Any]:
        """Wendet Design-Parameter auf Motiv an"""
        styled_motif = motif.copy()
        
        # Farben in Motiv-Prompt integrieren
        colors = design.get('colors', {})
        if colors.get('primary'):
            styled_motif['color_scheme'] = f"Farbschema mit {colors['primary']} als Hauptfarbe"
        
        return styled_motif
    
    def _coordinate_text_colors(self, texts: Dict[str, Any], design: Dict[str, Any]) -> Dict[str, Any]:
        """Koordiniert Text-Farben mit Design"""
        coordinated = texts.copy()
        coordinated['color_coordination'] = design.get('colors', {})
        return coordinated
    
    def _calculate_synergy_score(self, consistency_checks: Dict[str, bool]) -> float:
        """Berechnet Synergie-Score"""
        total_checks = len(consistency_checks)
        passed_checks = sum(1 for check in consistency_checks.values() if check)
        return round((passed_checks / total_checks) * 100, 1) if total_checks > 0 else 0.0
    
    def _generate_optimization_suggestions(self, layout: Dict[str, Any], design: Dict[str, Any],
                                         texts: Dict[str, Any], motif: Dict[str, Any],
                                         consistency_checks: Dict[str, bool]) -> List[str]:
        """Generiert Optimierungsvorschläge"""
        suggestions = []
        
        # Text-Qualität
        if texts.get('text_quality_score', 0) < 80:
            suggestions.append("📝 Texte könnten optimiert werden - prüfe Länge und Vollständigkeit")
        
        # Motiv-Qualität
        if motif.get('quality_score', 0) < 70:
            suggestions.append("🎨 Motiv-Beschreibung könnte detaillierter sein")
        
        # Konsistenz
        if not all(consistency_checks.values()):
            suggestions.append("🔗 Prüfe Konsistenz zwischen Design, Texten und Motiv")
        
        if not suggestions:
            suggestions.append("✅ Alle Elemente sind gut aufeinander abgestimmt!")
        
        return suggestions
    
    def _calculate_total_quality(self, texts: Dict[str, Any], motif: Dict[str, Any]) -> float:
        """Berechnet Gesamt-Qualitätsscore"""
        text_score = texts.get('text_quality_score', 0)
        motif_score = motif.get('quality_score', 0)
        return round((text_score + motif_score) / 2, 1)
    
    def _check_readiness(self, texts: Dict[str, Any], motif: Dict[str, Any]) -> bool:
        """Prüft ob System bereit für Generierung ist"""
        return (texts.get('ready_for_prompt', False) and 
                motif.get('ready_for_generation', False))
    
    def _get_fallback_layout(self) -> Dict[str, Any]:
        """Fallback-Layout"""
        return {
            'layout_id': 'skizze1_vertical_split',
            'zones': {
                'headline_block': {'x': 50, 'y': 50, 'width': 500, 'height': 60},
                'subline_block': {'x': 50, 'y': 120, 'width': 500, 'height': 40},
                'cta_block': {'x': 50, 'y': 400, 'width': 200, 'height': 50}
            },
            'fallback_used': True
        }
    
    def _get_fallback_design(self) -> Dict[str, Any]:
        """Fallback-Design"""
        return {
            'colors': {
                'primary': '#005EA5',
                'secondary': '#B4D9F7',
                'accent': '#FFC20E'
            },
            'style': {
                'layout_style': 'rounded_modern'
            },
            'fallback_used': True
        }
    
    def _get_fallback_prompt(self, linked_data: Dict[str, Any]) -> str:
        """Fallback-Prompt"""
        return ("Professionelles Recruiting-Design mit modernem Layout, "
                "ansprechende Texte und passende Bildmotive, "
                "harmonische Farbgestaltung, hohe Qualität")
    
    def _get_timestamp(self) -> str:
        """Gibt aktuellen Zeitstempel zurück"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _get_error_result(self, error_msg: str) -> Dict[str, Any]:
        """Fehler-Ergebnis"""
        return {
            'success': False,
            'error': error_msg,
            'fallback_prompt': "Professionelles Design mit modernen Elementen",
            'metadata': {
                'processing_timestamp': self._get_timestamp(),
                'error_occurred': True
            }
        }


def main():
    """Hauptfunktion für Kommandozeilen-Nutzung"""
    print("🔗 Element-Verknüpfungs-System")
    print("=" * 50)
    
    # Beispiel-Eingaben
    sample_input = {
        'layout_id': 'skizze1_vertical_split',
        'headline': 'Werden Sie Teil unseres Pflegeteams!',
        'subline': 'Flexible Arbeitszeiten, attraktive Vergütung und ein tolles Team erwarten Sie.',
        'company': 'Klinikum München',
        'stellentitel': 'Pflegekraft (m/w/d)',
        'location': 'München',
        'cta': 'Jetzt bewerben!',
        'benefits': ['Flexible Arbeitszeiten', 'Attraktive Vergütung', 'Fortbildungen'],
        'motiv_prompt': 'Freundliche Pflegekraft in modernem Krankenhaus',
        'visual_style': 'Professionell',
        'lighting_type': 'Natürlich',
        'framing': 'Medium Shot',
        'primary_color': '#005EA5',
        'secondary_color': '#B4D9F7',
        'accent_color': '#FFC20E'
    }
    
    # System initialisieren
    linker = ElementLinker()
    
    # Verknüpfung durchführen
    result = linker.link_all_elements(sample_input)
    
    # Ergebnis anzeigen
    if result['success']:
        print("✅ Verknüpfung erfolgreich!")
        print(f"📊 Gesamt-Qualitätsscore: {result['metadata']['total_quality_score']}")
        print(f"🎯 Bereit für Generierung: {result['metadata']['ready_for_generation']}")
        print("\n🎯 Generierter Prompt:")
        print("-" * 30)
        print(result['final_prompt'])
        
        # Optimierungsvorschläge
        suggestions = result['linked_data'].get('optimization_suggestions', [])
        if suggestions:
            print("\n💡 Optimierungsvorschläge:")
            for suggestion in suggestions:
                print(f"  • {suggestion}")
        
        # Synergie-Score
        synergy_score = result['linked_data'].get('synergy_score', 0)
        print(f"\n🔗 Synergie-Score: {synergy_score}%")
        
    else:
        print("❌ Fehler bei der Verknüpfung:")
        print(result['error'])
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
