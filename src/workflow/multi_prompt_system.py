#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
multi_prompt_system.py

🎯 Multi-Prompt-System mit 3-Stufen-Pipeline
📊 Version: 2.0 - Streamlit-Integration
🎨 Features: Layout-Integration + CI-Farben + Text-Optimierung
"""

import os
import sys
import yaml
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import logging

# Logging konfigurieren
logger = logging.getLogger(__name__)

# Dataclasses für strukturierte Daten
from dataclasses import dataclass

@dataclass
class StructuredInput:
    """Strukturierte Eingabedaten für das Multi-Prompt-System"""
    headline: str
    subline: str
    company: str
    stellentitel: str
    location: str
    position_long: str
    cta: str
    benefits: List[str]
    motiv_prompt: str
    visual_style: str
    lighting_type: str
    lighting_mood: str
    framing: str
    layout_id: str
    layout_style: Tuple[str, str]
    container_shape: Tuple[str, str]
    border_style: Tuple[str, str]
    texture_style: Tuple[str, str]
    background_treatment: Tuple[str, str]
    corner_radius: Tuple[str, str]
    accent_elements: Tuple[str, str]
    image_text_ratio: int
    container_transparency: int
    primary_color: str
    secondary_color: str
    accent_color: str

@dataclass
class LayoutIntegratedData:
    """Layout-integrierte Daten nach Stufe 2"""
    structured_input: StructuredInput
    layout_definition: Dict[str, Any]
    text_placements: Dict[str, Dict[str, Any]]
    color_integration: Dict[str, str]
    layout_metadata: Dict[str, Any]

@dataclass
class FinalizedPrompts:
    """Finalisierte Prompts nach Stufe 3"""
    dalle_prompt: str
    midjourney_prompt: str
    cinematic_prompt: Optional[Any] = None
    quality_assessment: Dict[str, Any] = None
    total_processing_time: float = 0.0

@dataclass
class CinematicPromptData:
    """Cinematisch-natürlichsprachlicher Prompt"""
    full_prompt: str
    metadata: Dict[str, Any]

# Hilfsfunktionen
def create_prompt_transformer():
    """Erstellt einen Prompt-Transformer (Fallback)"""
    class FallbackTransformer:
        def transform_to_cinematic_prompt(self, layout_data, enable_text_rendering, quality_level):
            # Fallback-Transformation
            dalle_prompt = layout_data.structured_input.motiv_prompt
            return CinematicPromptData(
                full_prompt=dalle_prompt,
                metadata={'transformation_type': 'fallback', 'quality_level': quality_level}
            )
        
        def get_transformation_stats(self, original, cinematic):
            return {
                'cinematic_length': len(cinematic),
                'reduction_percentage': 0
            }
    
    return FallbackTransformer()

# InputProcessor Klasse
class InputProcessor:
    """Verarbeitet Streamlit-Eingaben zu strukturierten Daten"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        logger.info("📝 InputProcessor initialisiert")
        
    def process(self, streamlit_input: Dict[str, Any]) -> StructuredInput:
        """Verarbeitet Streamlit-Eingaben zu strukturierten Daten"""
        start_time = datetime.now()
        logger.info("🔄 Verarbeite Streamlit-Eingaben...")
        
        try:
            # Prüfe ob Text-Kürzung deaktiviert ist
            disable_text_truncation = streamlit_input.get('disable_text_truncation', False)
            
            # Text-Daten extrahieren und normalisieren (mit oder ohne Kürzung)
            if disable_text_truncation:
                # KEINE Text-Kürzung - verwende Original-Texte
                headline = streamlit_input.get('headline', '')
                subline = streamlit_input.get('subline', '')
                company = streamlit_input.get('unternehmen', '')
                stellentitel = streamlit_input.get('stellentitel', '')
                location = streamlit_input.get('location', '')
                position_long = streamlit_input.get('position_long', '')
                cta = streamlit_input.get('cta', '')
                benefits = streamlit_input.get('benefits', [])
            else:
                # Normale Text-Verarbeitung mit Kürzung
                headline = self._normalize_text(streamlit_input.get('headline', ''), 50)
                subline = self._normalize_text(streamlit_input.get('subline', ''), 200)
                company = self._normalize_text(streamlit_input.get('unternehmen', ''), 50)
                stellentitel = self._normalize_text(streamlit_input.get('stellentitel', ''), 80)
                location = self._normalize_text(streamlit_input.get('location', ''), 50)
                position_long = self._normalize_text(streamlit_input.get('position_long', ''), 300)
                cta = self._normalize_text(streamlit_input.get('cta', ''), 50)
                benefits = streamlit_input.get('benefits', [])
            
            # Weitere Daten extrahieren
            motiv_prompt = streamlit_input.get('motiv_prompt', 'Professionelle Person in moderner Umgebung')
            visual_style = streamlit_input.get('visual_style', 'Professionell')
            lighting_type = streamlit_input.get('lighting_type', 'Natürlich')
            lighting_mood = streamlit_input.get('lighting_mood', 'Professionell')
            framing = streamlit_input.get('framing', 'Medium Shot')
            layout_id = streamlit_input.get('layout_id', 'skizze1_vertical_split')
            
            # Layout-Style-Daten
            layout_style = streamlit_input.get('layout_style', ('rounded_modern', '🔵 Abgerundet & Modern'))
            container_shape = streamlit_input.get('container_shape', ('rounded_rectangle', '📱 Abgerundet'))
            border_style = streamlit_input.get('border_style', ('soft_shadow', '🌫️ Weicher Schatten'))
            texture_style = streamlit_input.get('texture_style', ('gradient', '🌈 Farbverlauf'))
            background_treatment = streamlit_input.get('background_treatment', ('subtle_pattern', '🌸 Subtiles Muster'))
            corner_radius = streamlit_input.get('corner_radius', ('medium', '⌜ Mittel'))
            accent_elements = streamlit_input.get('accent_elements', ('modern_minimal', '⚪ Modern Minimal'))
            
            # Neue Layout-Proportionen
            image_text_ratio = streamlit_input.get('image_text_ratio', 50)
            container_transparency = streamlit_input.get('container_transparency', 0)
            
            # CI-Farben
            primary_color = streamlit_input.get('primary_color', '#005EA5')
            secondary_color = streamlit_input.get('secondary_color', '#B4D9F7')
            accent_color = streamlit_input.get('accent_color', '#FFC20E')
            
            # StructuredInput erstellen
            structured_input = StructuredInput(
                headline=headline,
                subline=subline,
                company=company,
                stellentitel=stellentitel,
                location=location,
                position_long=position_long,
                cta=cta,
                benefits=benefits,
                motiv_prompt=motiv_prompt,
                visual_style=visual_style,
                lighting_type=lighting_type,
                lighting_mood=lighting_mood,
                framing=framing,
                layout_id=layout_id,
                layout_style=layout_style,
                container_shape=container_shape,
                border_style=border_style,
                texture_style=texture_style,
                background_treatment=background_treatment,
                corner_radius=corner_radius,
                accent_elements=accent_elements,
                image_text_ratio=image_text_ratio,
                container_transparency=container_transparency,
                primary_color=primary_color,
                secondary_color=secondary_color,
                accent_color=accent_color
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"✅ Input-Verarbeitung abgeschlossen in {processing_time:.2f}s")
            
            return structured_input
            
        except Exception as e:
            logger.error(f"❌ Fehler bei der Input-Verarbeitung: {e}")
            raise
    
    def _normalize_text(self, text: str, max_length: int) -> str:
        """Normalisiert Text auf maximale Länge"""
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
    
# LayoutIntegrator Klasse
class LayoutIntegrator:
    """Integriert Layout-Definitionen und Text-Positionierung"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        logger.info("🎨 LayoutIntegrator initialisiert")
    
    def process(self, structured_input: StructuredInput) -> LayoutIntegratedData:
        """Integriert Layout-Definitionen und Text-Positionierung"""
        start_time = datetime.now()
        logger.info("🔄 Integriere Layout...")
        
        try:
            # Layout-Definition laden
            layout_definition = self._load_layout_definition(structured_input.layout_id)
            
            # Text-Platzierungen berechnen
            text_placements = self._calculate_text_placements(layout_definition, structured_input)
            
            # Farb-Integration
            color_integration = {
                'primary': structured_input.primary_color,
                'secondary': structured_input.secondary_color,
                'accent': structured_input.accent_color
            }
            
            # Layout-Metadaten
            layout_metadata = {
                'layout_id': structured_input.layout_id,
                'image_text_ratio': structured_input.image_text_ratio,
                'container_transparency': structured_input.container_transparency
            }
            
            layout_data = LayoutIntegratedData(
                structured_input=structured_input,
                layout_definition=layout_definition,
                text_placements=text_placements,
                color_integration=color_integration,
                layout_metadata=layout_metadata
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"✅ Layout-Integration abgeschlossen in {processing_time:.2f}s")
            
            return layout_data
            
        except Exception as e:
            logger.error(f"❌ Fehler bei der Layout-Integration: {e}")
            raise
    
    def _load_layout_definition(self, layout_id: str) -> Dict[str, Any]:
        """Lädt Layout-Definition aus YAML-Datei"""
        try:
            layout_file = self.project_root / "input_config" / "enhanced_layout_definitions.yaml"
            if layout_file.exists():
                with open(layout_file, 'r', encoding='utf-8') as f:
                    layouts = yaml.safe_load(f)
                    return layouts.get(layout_id, {})
            else:
                logger.warning(f"Layout-Datei nicht gefunden: {layout_file}")
                return {}
        except Exception as e:
            logger.error(f"Fehler beim Laden der Layout-Definition: {e}")
            return {}
    
    def _calculate_text_placements(self, layout_def: Dict[str, Any], text_data: StructuredInput) -> Dict[str, Dict[str, Any]]:
        """Berechnet Text-Platzierungen basierend auf Layout-Definition"""
        # Fallback-Text-Platzierungen
        base_layout = {
            'headline': {'x': 100, 'y': 200, 'width': 400, 'height': 100},
            'subline': {'x': 100, 'y': 320, 'width': 400, 'height': 80},
            'company': {'x': 100, 'y': 80, 'width': 200, 'height': 60},
            'location': {'x': 100, 'y': 140, 'width': 200, 'height': 60},
            'cta': {'x': 100, 'y': 600, 'width': 200, 'height': 80},
            'benefits': {'x': 100, 'y': 420, 'width': 400, 'height': 160}
        }
        
        return base_layout

# PromptFinalizer Klasse
class PromptFinalizer:
    """Finalisiert Prompts mit Layout-Integration und Text-Optimierung"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        logger.info("🎯 PromptFinalizer initialisiert")
    
    def process(self, layout_data: LayoutIntegratedData, enable_text_rendering: bool = False) -> FinalizedPrompts:
        """Finalisiert Prompts mit Layout-Integration"""
        start_time = datetime.now()
        logger.info("🔄 Finalisiere Prompts...")
        
        try:
            # DALL-E Prompt generieren
            dalle_prompt = self._generate_dalle_prompt(layout_data, enable_text_rendering)
            
            # Midjourney Prompt generieren
            midjourney_prompt = self._generate_midjourney_prompt(layout_data)
            
            # Qualitätsbewertung
            quality_assessment = self._assess_quality(dalle_prompt, midjourney_prompt)
            
            finalized_prompts = FinalizedPrompts(
                dalle_prompt=dalle_prompt,
                midjourney_prompt=midjourney_prompt,
                quality_assessment=quality_assessment
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"✅ Prompt-Finalisierung abgeschlossen in {processing_time:.2f}s")
            
            return finalized_prompts
            
        except Exception as e:
            logger.error(f"❌ Fehler bei der Prompt-Finalisierung: {e}")
            raise
    
    def _generate_dalle_prompt(self, layout_data: LayoutIntegratedData, enable_text_rendering: bool = False) -> str:
        """Generiert DALL-E Prompt mit Layout-Integration"""
        # Basis-Prompt
        prompt = layout_data.structured_input.motiv_prompt
        
        # Layout-Informationen hinzufügen
        prompt += f"\n\nLayout: {layout_data.structured_input.layout_id}"
        prompt += f"\nStil: {layout_data.structured_input.visual_style}"
        
        # Text-Integration (wenn aktiviert)
        if enable_text_rendering:
            prompt += f"\n\nText-Elemente:"
            prompt += f"\n- Headline: {layout_data.structured_input.headline}"
            prompt += f"\n- Subline: {layout_data.structured_input.subline}"
            prompt += f"\n- CTA: {layout_data.structured_input.cta}"
        
        return prompt
    
    def _generate_midjourney_prompt(self, layout_data: LayoutIntegratedData) -> str:
        """Generiert Midjourney Prompt"""
        # Basis-Prompt
        prompt = layout_data.structured_input.motiv_prompt
        
        # Stil-Informationen
        prompt += f", {layout_data.structured_input.visual_style} style"
        prompt += f", {layout_data.structured_input.lighting_type} lighting"
        prompt += f", {layout_data.structured_input.framing}"
        
        return prompt
    
    def _assess_quality(self, dalle_prompt: str, midjourney_prompt: str) -> Dict[str, Any]:
        """Bewertet die Qualität der generierten Prompts"""
        try:
            # Einfache Qualitätsbewertung basierend auf Länge und Inhalt
            dalle_score = min(100, len(dalle_prompt) // 2)
            midjourney_score = min(100, len(midjourney_prompt) // 2)
            
            overall_score = (dalle_score + midjourney_score) // 2
            
            return {
                'overall_score': overall_score,
                'dalle_score': dalle_score,
                'midjourney_score': midjourney_score,
                'total_length': len(dalle_prompt) + len(midjourney_prompt)
            }
        except Exception as e:
            logger.error(f"❌ Fehler bei Qualitätsbewertung: {e}")
            return {'overall_score': 0, 'error': str(e)}

# MultiPromptSystem Klasse
class MultiPromptSystem:
    """
    🎯 HAUPT-KLASSE: 3-Stufen Multi-Prompt-System
    
    Orchestriert die komplette Pipeline:
    Input-Processor → Layout-Integrator → Prompt-Finalizer
    """
    
    def __init__(self, project_root: Path = None):
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent
        
        self.project_root = project_root
        
        # Initialisiere alle Stufen
        self.input_processor = InputProcessor(project_root)
        self.layout_integrator = LayoutIntegrator(project_root)
        self.prompt_finalizer = PromptFinalizer(project_root)
        
        logger.info("🚀 Multi-Prompt-System initialisiert")
        logger.info(f"   📂 Projekt-Root: {project_root}")
    
    def process_streamlit_input(self, streamlit_input: Dict[str, Any], enable_text_rendering: bool = False) -> FinalizedPrompts:
        """
        Verarbeitet Streamlit-Eingaben durch die komplette 3-Stufen-Pipeline
        
        Args:
            streamlit_input: Dict mit Streamlit-UI-Daten
            enable_text_rendering: Ob Text im DALL-E Bild gerendert werden soll
                                 True = Mit Text (Risiko korrupter deutscher Zeichen)
                                 False = Text-Rendering aktiviert
            
        Returns:
            FinalizedPrompts mit beiden optimierten Prompts
        """
        
        logger.info("🔄 STARTE 3-STUFEN MULTI-PROMPT-PIPELINE")
        logger.info(f"   📝 Text-Rendering: {'AKTIVIERT' if enable_text_rendering else 'DEAKTIVIERT'}")
        if enable_text_rendering:
            logger.warning("   ⚠️ Deutsche Umlaute können als korrupte Zeichen erscheinen")
        else:
            logger.info("   🎨 Layout-Modus: Layout-Bereiche mit Text-Rendering")
        total_start_time = datetime.now()
        
        try:
            # STUFE 1: Input Processing
            structured_input = self.input_processor.process(streamlit_input)
            
            # STUFE 2: Layout Integration
            layout_integrated = self.layout_integrator.process(structured_input)
            
            # STUFE 3: Prompt Finalization
            finalized_prompts = self.prompt_finalizer.process(layout_integrated, enable_text_rendering)
            
            # Gesamt-Processing-Zeit
            total_time = (datetime.now() - total_start_time).total_seconds()
            finalized_prompts.total_processing_time = total_time
            
            logger.info("✅ MULTI-PROMPT-PIPELINE ABGESCHLOSSEN")
            logger.info(f"   ⏱️ Gesamt-Zeit: {total_time:.2f}s")
            logger.info(f"   🎬 Midjourney: {len(finalized_prompts.midjourney_prompt)} chars")
            logger.info(f"   🏗️ DALL-E: {len(finalized_prompts.dalle_prompt)} chars")
            logger.info(f"   📊 Quality: {finalized_prompts.quality_assessment.get('overall_score', 0)}/100")
            
            return finalized_prompts
            
        except Exception as e:
            logger.error(f"❌ Multi-Prompt-Pipeline Fehler: {e}")
            raise
    
    def _generate_cinematic_prompt(self, layout_data: LayoutIntegratedData, enable_text_rendering: bool = False, quality_level: str = "high") -> CinematicPromptData:
        """
        🎭 Generiert cinematisch-natürlichsprachlichen Prompt für optimale OpenAI API Bildgenerierung
        
        Args:
            layout_data: Layout-integrierte Daten
            enable_text_rendering: Ob Text gerendert werden soll
            quality_level: Qualitätsstufe ("basic", "high", "premium")
            
        Returns:
            CinematicPromptData mit transformiertem Prompt
        """
        try:
            # Prompt Transformer initialisieren
            transformer = create_prompt_transformer()
            
            # Transformation durchführen
            cinematic_data = transformer.transform_to_cinematic_prompt(layout_data, enable_text_rendering, quality_level)
            
            # Statistiken loggen
            stats = transformer.get_transformation_stats(
                self.prompt_finalizer._generate_dalle_prompt(layout_data, enable_text_rendering),
                cinematic_data.full_prompt
            )
            
            logger.info(f"🎭 Cinematic Prompt generiert: {stats['cinematic_length']} chars "
                       f"(Reduktion: {stats['reduction_percentage']}%)")
            
            return cinematic_data
            
        except Exception as e:
            logger.error(f"❌ Fehler bei Cinematic Prompt-Generierung: {e}")
            # Fallback: Verwende DALL-E Prompt
            dalle_prompt = self.prompt_finalizer._generate_dalle_prompt(layout_data, enable_text_rendering)
            return CinematicPromptData(
                full_prompt=dalle_prompt,
                metadata={'transformation_type': 'fallback', 'quality_level': quality_level}
            )

# Factory-Funktion
def create_multi_prompt_system(project_root: Path = None) -> MultiPromptSystem:
    """Erstellt eine neue MultiPromptSystem-Instanz"""
    return MultiPromptSystem(project_root)