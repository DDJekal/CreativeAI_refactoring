#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
storyline_midjourney_workflow.py

LangGraph Workflow für Storyline-Generierung und Midjourney-Prompt-Erstellung
📖 Version: 1.0 - Empathische Storyline-Generierung
🎯 Features: Painpoint-Analyse + Emotionale Storyline + Midjourney-Prompt
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

# LangGraph Imports
try:
    from langgraph import StateGraph, END
    from langgraph.graph import START
    from langgraph.checkpoint.memory import MemorySaver
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    from langchain_openai import ChatOpenAI
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    print("⚠️ LangGraph nicht verfügbar - verwende Fallback-Modus")

# Logging konfigurieren
logger = logging.getLogger(__name__)

@dataclass
class StorylineInput:
    """Eingabedaten für die Storyline-Generierung"""
    headline: str
    subline: str
    stellentitel: str
    benefits: List[str]
    location: str
    company: str
    cta: str
    target_audience: str
    industry: str

@dataclass
class StorylineData:
    """Generierte Storyline-Daten"""
    painpoints: List[str]
    emotional_focus: str
    target_audience_analysis: str
    storyline: str
    emotional_impact: str
    visual_elements: List[str]

@dataclass
class MidjourneyPrompt:
    """Generierter Midjourney-Prompt"""
    prompt: str
    emotional_focus: str
    visual_style: str
    lighting_mood: str
    composition: str
    quality_notes: str

class StorylineGenerator:
    """Generiert empathische Storylines basierend auf Texteingaben"""
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if self.openai_api_key and LANGGRAPH_AVAILABLE:
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.8,
                api_key=self.openai_api_key
            )
        else:
            self.llm = None
            logger.warning("OpenAI API nicht verfügbar - verwende Fallback-Modus")
    
    def analyze_painpoints(self, input_data: StorylineInput) -> List[str]:
        """Analysiert Painpoints der Zielgruppe basierend auf den Eingaben"""
        if not self.llm:
            return self._fallback_painpoint_analysis(input_data)
        
        try:
            system_prompt = """Du bist ein empathischer HR-Experte, der die Painpoints von Jobsuchenden versteht.
            
            Analysiere die folgenden Texteingaben und identifiziere die emotionalen und praktischen Painpoints,
            die die Zielgruppe bei der Jobsuche haben könnte.
            
            Fokussiere dich auf:
            - Berufsspezifische Herausforderungen
            - Emotionale Bedürfnisse
            - Praktische Sorgen
            - Karriere-Entwicklungsmöglichkeiten
            
            Gib eine Liste von 5-7 konkreten Painpoints zurück."""
            
            user_prompt = f"""Analysiere diese Job-Anzeige und identifiziere die Painpoints der Zielgruppe:
            
            Headline: {input_data.headline}
            Subline: {input_data.subline}
            Position: {input_data.stellentitel}
            Branche: {input_data.industry}
            Benefits: {', '.join(input_data.benefits)}
            Zielgruppe: {input_data.target_audience}
            
            Welche Painpoints hat diese Zielgruppe bei der Jobsuche?"""
            
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])
            
            # Parse die Antwort in eine Liste von Painpoints
            content = response.content.strip()
            painpoints = [line.strip().lstrip('- ').lstrip('* ').lstrip('• ') 
                         for line in content.split('\n') 
                         if line.strip() and not line.startswith('#')]
            
            return painpoints[:7]  # Maximal 7 Painpoints
            
        except Exception as e:
            logger.error(f"Fehler bei Painpoint-Analyse: {e}")
            return self._fallback_painpoint_analysis(input_data)
    
    def _fallback_painpoint_analysis(self, input_data: StorylineInput) -> List[str]:
        """Fallback-Painpoint-Analyse ohne LLM"""
        fallback_painpoints = [
            "Unsicherheit über Karriere-Entwicklung",
            "Sorge um Work-Life-Balance",
            "Angst vor mangelnder Anerkennung",
            "Ungewissheit über Team-Kultur",
            "Bedenken bezüglich Gehaltsentwicklung"
        ]
        return fallback_painpoints
    
    def generate_storyline(self, input_data: StorylineInput, painpoints: List[str]) -> str:
        """Generiert eine empathische Storyline basierend auf Painpoints"""
        if not self.llm:
            return self._fallback_storyline_generation(input_data, painpoints)
        
        try:
            system_prompt = """Du bist ein kreativer Storyteller, der empathische Geschichten für Job-Anzeigen schreibt.
            
            Erstelle eine Storyline, die:
            - Die Painpoints der Zielgruppe versteht und anspricht
            - Eine emotionale Verbindung herstellt
            - Die Vorteile der Position und des Unternehmens hervorhebt
            - Motivierend und einladend ist
            - Nicht länger als 100 Wörter ist"""
            
            user_prompt = f"""Erstelle eine empathische Storyline für diese Job-Anzeige:
            
            Position: {input_data.stellentitel}
            Headline: {input_data.headline}
            Subline: {input_data.subline}
            Branche: {input_data.industry}
            Benefits: {', '.join(input_data.benefits)}
            
            Identifizierte Painpoints der Zielgruppe:
            {chr(10).join([f"- {painpoint}" for painpoint in painpoints])}
            
            Schreibe eine Storyline, die diese Painpoints versteht und eine Lösung anbietet."""
            
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])
            
            return response.content.strip()
            
        except Exception as e:
            logger.error(f"Fehler bei Storyline-Generierung: {e}")
            return self._fallback_storyline_generation(input_data, painpoints)
    
    def _fallback_storyline_generation(self, input_data: StorylineInput, painpoints: List[str]) -> str:
        """Fallback-Storyline ohne LLM"""
        return f"""Stelle dir vor, du bist {input_data.target_audience} und suchst nach einer neuen Herausforderung. 
        Bei {input_data.company} findest du nicht nur eine Position als {input_data.stellentitel}, sondern eine 
        Umgebung, die deine Karriere-Entwicklung fördert und deine Work-Life-Balance respektiert. 
        Hier wirst du Teil eines Teams, das Innovation schätzt und deine Expertise anerkennt."""

class EmotionalStorylineGenerator:
    """Verbessert Storylines mit emotionalem Fokus"""
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if self.openai_api_key and LANGGRAPH_AVAILABLE:
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.7,
                api_key=self.openai_api_key
            )
        else:
            self.llm = None
    
    def enhance_emotional_focus(self, storyline: str, input_data: StorylineInput) -> str:
        """Verbessert die Storyline mit emotionalem Fokus"""
        if not self.llm:
            return storyline
        
        try:
            system_prompt = """Du bist ein Experte für emotionale Kommunikation in der Personalgewinnung.
            
            Verbessere die gegebene Storyline, indem du:
            - Den emotionalen Fokus verstärkst
            - Eine tiefere Verbindung zur Zielgruppe herstellst
            - Die emotionalen Vorteile der Position hervorhebst
            - Eine inspirierende und motivierende Atmosphäre schaffst
            
            Behalte die ursprüngliche Länge bei, aber mache sie emotionaler und ansprechender."""
            
            user_prompt = f"""Verbessere diese Storyline emotional:
            
            Ursprüngliche Storyline:
            {storyline}
            
            Position: {input_data.stellentitel}
            Branche: {input_data.industry}
            Zielgruppe: {input_data.target_audience}
            
            Mache sie emotionaler und ansprechender für die Zielgruppe."""
            
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])
            
            return response.content.strip()
            
        except Exception as e:
            logger.error(f"Fehler bei emotionaler Verbesserung: {e}")
            return storyline
    
    def determine_emotional_focus(self, input_data: StorylineInput) -> str:
        """Bestimmt den emotionalen Fokus basierend auf den Eingaben"""
        if not self.llm:
            return "empathisch"
        
        try:
            system_prompt = """Analysiere die Texteingaben und bestimme den emotionalen Fokus.
            
            Mögliche emotionale Foki:
            - empathisch: Verständnis für Herausforderungen
            - motivierend: Inspiration und Antrieb
            - vertrauensvoll: Sicherheit und Stabilität
            - inspirierend: Kreativität und Innovation
            - unterstützend: Hilfe und Begleitung
            
            Wähle den passendsten emotionalen Fokus basierend auf dem Inhalt."""
            
            user_prompt = f"""Bestimme den emotionalen Fokus für diese Job-Anzeige:
            
            Headline: {input_data.headline}
            Subline: {input_data.subline}
            Position: {input_data.stellentitel}
            Branche: {input_data.industry}
            Benefits: {', '.join(input_data.benefits)}
            Zielgruppe: {input_data.target_audience}
            
            Welcher emotionale Fokus passt am besten?"""
            
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])
            
            content = response.content.strip().lower()
            if "empathisch" in content:
                return "empathisch"
            elif "motivierend" in content:
                return "motivierend"
            elif "vertrauensvoll" in content:
                return "vertrauensvoll"
            elif "inspirierend" in content:
                return "inspirierend"
            elif "unterstützend" in content:
                return "unterstützend"
            else:
                return "empathisch"
                
        except Exception as e:
            logger.error(f"Fehler bei emotionaler Fokus-Bestimmung: {e}")
            return "empathisch"

class MidjourneyPromptGenerator:
    """Generiert Midjourney-Prompts basierend auf Storylines"""
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if self.openai_api_key and LANGGRAPH_AVAILABLE:
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.8,
                api_key=self.openai_api_key
            )
        else:
            self.llm = None
    
    def generate_midjourney_prompt(self, storyline_data: StorylineData, input_data: StorylineInput) -> MidjourneyPrompt:
        """Generiert einen Midjourney-Prompt basierend auf der Storyline"""
        if not self.llm:
            return self._fallback_midjourney_prompt(storyline_data, input_data)
        
        try:
            system_prompt = """Du bist ein Experte für Midjourney-Prompt-Erstellung.
            
            Erstelle einen effektiven Midjourney-Prompt, der:
            - Die emotionale Stimmung der Storyline einfängt
            - Klare visuelle Anweisungen gibt
            - Professionell und ansprechend ist
            - Visuelle Elemente beschreibt, die die Zielgruppe ansprechen
            - Nicht länger als 150 Wörter ist
            
            Strukturiere den Prompt mit:
            - Hauptmotiv und Stimmung
            - Visueller Stil und Komposition
            - Beleuchtung und Atmosphäre
            - Qualitätshinweise"""
            
            user_prompt = f"""Erstelle einen Midjourney-Prompt für diese Job-Anzeige:
            
            Storyline: {storyline_data.storyline}
            Emotionaler Fokus: {storyline_data.emotional_focus}
            Visuelle Elemente: {', '.join(storyline_data.visual_elements)}
            
            Job-Details:
            Headline: {input_data.headline}
            Subline: {input_data.subline}
            Position: {input_data.stellentitel}
            Branche: {input_data.industry}
            Benefits: {', '.join(input_data.benefits)}
            
            Erstelle einen emotionalen, professionellen Midjourney-Prompt."""
            
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])
            
            # Parse die Antwort in strukturierte Daten
            prompt_text = response.content.strip()
            
            return MidjourneyPrompt(
                prompt=prompt_text,
                emotional_focus=storyline_data.emotional_focus,
                visual_style="professionell und emotional",
                lighting_mood="warm und einladend",
                composition="zentriert und ausgewogen",
                quality_notes="hohe Qualität, 4K, professionelle Fotografie"
            )
            
        except Exception as e:
            logger.error(f"Fehler bei Midjourney-Prompt-Generierung: {e}")
            return self._fallback_midjourney_prompt(storyline_data, input_data)
    
    def _fallback_midjourney_prompt(self, storyline_data: StorylineData, input_data: StorylineInput) -> MidjourneyPrompt:
        """Fallback-Midjourney-Prompt ohne LLM"""
        fallback_prompt = f"""Professional job advertisement image: {input_data.headline}, {input_data.subline}, Position: {input_data.stellentitel}, Location: {input_data.location}, modern office environment, professional lighting, high quality, 4k, emotional storytelling, {storyline_data.emotional_focus} focus"""
        
        return MidjourneyPrompt(
            prompt=fallback_prompt,
            emotional_focus=storyline_data.emotional_focus,
            visual_style="professionell",
            lighting_mood="professionell",
            composition="zentriert",
            quality_notes="hohe Qualität, 4K"
        )

class StorylineMidjourneyWorkflow:
    """Hauptklasse für den Storyline-Midjourney-Workflow"""
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        
        # Initialisiere alle Komponenten
        self.storyline_generator = StorylineGenerator(openai_api_key)
        self.emotional_generator = EmotionalStorylineGenerator(openai_api_key)
        self.midjourney_generator = MidjourneyPromptGenerator(openai_api_key)
            
        # LangGraph Workflow (falls verfügbar)
        if LANGGRAPH_AVAILABLE:
            self.workflow = self._create_langgraph_workflow()
        else:
            self.workflow = None
            logger.warning("LangGraph nicht verfügbar - verwende Fallback-Workflow")
    
    def _create_langgraph_workflow(self):
        """Erstellt den LangGraph Workflow"""
        try:
            # Definiere den Workflow-Graphen
            workflow = StateGraph(StorylineData)
            
            # Definiere die Knoten
            workflow.add_node("analyze_painpoints", self._analyze_painpoints_node)
            workflow.add_node("generate_storyline", self._generate_storyline_node)
            workflow.add_node("enhance_emotion", self._enhance_emotion_node)
            workflow.add_node("create_midjourney", self._create_midjourney_node)
            
            # Definiere den Ablauf
            workflow.set_entry_point("analyze_painpoints")
            workflow.add_edge("analyze_painpoints", "generate_storyline")
            workflow.add_edge("generate_storyline", "enhance_emotion")
            workflow.add_edge("enhance_emotion", "create_midjourney")
            workflow.add_edge("create_midjourney", END)
            
            # Kompiliere den Workflow
            return workflow.compile()
        
        except Exception as e:
            logger.error(f"Fehler beim Erstellen des LangGraph Workflows: {e}")
            return None
    
    def _analyze_painpoints_node(self, state: StorylineData, input_data: StorylineInput) -> StorylineData:
        """LangGraph-Knoten für Painpoint-Analyse"""
        painpoints = self.storyline_generator.analyze_painpoints(input_data)
        return StorylineData(
            painpoints=painpoints,
            emotional_focus="",
            target_audience_analysis="",
            storyline="",
            emotional_impact="",
            visual_elements=[]
        )
    
    def _generate_storyline_node(self, state: StorylineData, input_data: StorylineInput) -> StorylineData:
        """LangGraph-Knoten für Storyline-Generierung"""
        storyline = self.storyline_generator.generate_storyline(input_data, state.painpoints)
        return StorylineData(
            painpoints=state.painpoints,
            emotional_focus=state.emotional_focus,
            target_audience_analysis=state.target_audience_analysis,
            storyline=storyline,
            emotional_impact=state.emotional_impact,
            visual_elements=state.visual_elements
        )
    
    def _enhance_emotion_node(self, state: StorylineData, input_data: StorylineInput) -> StorylineData:
        """LangGraph-Knoten für emotionale Verbesserung"""
        emotional_focus = self.emotional_generator.determine_emotional_focus(input_data)
        enhanced_storyline = self.emotional_generator.enhance_emotional_focus(state.storyline, input_data)
        
        # Generiere visuelle Elemente basierend auf der Storyline
        visual_elements = self._extract_visual_elements(enhanced_storyline, input_data)
        
        return StorylineData(
            painpoints=state.painpoints,
            emotional_focus=emotional_focus,
            target_audience_analysis=state.target_audience_analysis,
            storyline=enhanced_storyline,
            emotional_impact=f"Emotionaler Fokus: {emotional_focus}",
            visual_elements=visual_elements
        )
    
    def _create_midjourney_node(self, state: StorylineData, input_data: StorylineInput) -> StorylineData:
        """LangGraph-Knoten für Midjourney-Prompt-Erstellung"""
        # Hier würde der Midjourney-Prompt generiert werden
        # Für jetzt geben wir den State zurück
        return state
    
    def _extract_visual_elements(self, storyline: str, input_data: StorylineInput) -> List[str]:
        """Extrahiert visuelle Elemente aus der Storyline"""
        visual_elements = []
        
        # Füge branchenspezifische visuelle Elemente hinzu
        if "office" in storyline.lower() or "büro" in storyline.lower():
            visual_elements.append("modern office environment")
        if "team" in storyline.lower():
            visual_elements.append("collaborative workspace")
        if "innovation" in storyline.lower():
            visual_elements.append("creative atmosphere")
        if "professional" in storyline.lower():
            visual_elements.append("professional setting")
        
        # Standard-Elemente
        visual_elements.extend([
            "professional lighting",
            "high quality",
            "4k resolution",
            "emotional storytelling"
        ])
        
        return visual_elements
    
    def run_storyline_generation(self, input_data: StorylineInput) -> StorylineData:
        """Führt die Storyline-Generierung aus (mit oder ohne LangGraph)"""
        try:
            if self.workflow and LANGGRAPH_AVAILABLE:
                logger.info("🔄 Starte LangGraph Workflow")
                # LangGraph Workflow ausführen
                result = self.workflow.invoke({
                    "input_data": input_data
                })
                return result
            else:
                logger.info("🔄 Starte Fallback-Workflow")
                return self._run_fallback_workflow(input_data)
                
        except Exception as e:
            logger.error(f"Fehler im Storyline-Workflow: {e}")
            return self._run_fallback_workflow(input_data)
    
    def _run_fallback_workflow(self, input_data: StorylineInput) -> StorylineData:
        """Fallback-Workflow ohne LangGraph"""
        try:
            # 1. Painpoints analysieren
            logger.info("🔄 Starte Storyline-Generierung")
            painpoints = self.storyline_generator.analyze_painpoints(input_data)
            logger.info(f"✅ Painpoints identifiziert: {len(painpoints)}")
            
            # 2. Storyline generieren
            storyline = self.storyline_generator.generate_storyline(input_data, painpoints)
            logger.info("✅ Storyline generiert")
            
            # 3. Emotionalen Fokus bestimmen
            emotional_focus = self.emotional_generator.determine_emotional_focus(input_data)
            logger.info(f"✅ Emotionaler Fokus: {emotional_focus}")
            
            # 4. Storyline emotional verbessern
            enhanced_storyline = self.emotional_generator.enhance_emotional_focus(storyline, input_data)
            logger.info("✅ Storyline emotional verbessert")
            
            # 5. Visuelle Elemente extrahieren
            visual_elements = self._extract_visual_elements(enhanced_storyline, input_data)
            
            # 6. Target Audience Analysis
            target_audience_analysis = f"Zielgruppe: {input_data.target_audience}, Branche: {input_data.industry}"
            
            logger.info("✅ Storyline-Generierung abgeschlossen")
            
            return StorylineData(
                painpoints=painpoints,
                emotional_focus=emotional_focus,
                target_audience_analysis=target_audience_analysis,
                storyline=enhanced_storyline,
                emotional_impact=f"Emotionaler Fokus: {emotional_focus}",
                visual_elements=visual_elements
            )
            
        except Exception as e:
            logger.error(f"Fehler im Fallback-Workflow: {e}")
            # Rückgabe von Standard-Daten
            return StorylineData(
                painpoints=["Standard-Painpoint"],
                emotional_focus="empathisch",
                target_audience_analysis="Standard-Analyse",
                storyline="Standard-Storyline",
                emotional_impact="Standard-Impact",
                visual_elements=["professional setting"]
            )
    
    def run_midjourney_generation(self, storyline_data: StorylineData, input_data: StorylineInput) -> MidjourneyPrompt:
        """Generiert den Midjourney-Prompt basierend auf der Storyline"""
        try:
            logger.info("🎨 Starte Midjourney-Prompt-Generierung")
            return self.midjourney_generator.generate_midjourney_prompt(storyline_data, input_data)
        except Exception as e:
            logger.error(f"❌ Fehler bei Midjourney-Prompt-Generierung: {e}")
            return self.midjourney_generator._fallback_midjourney_prompt(storyline_data, input_data)

class FallbackStorylineWorkflow:
    """Einfacher Fallback-Workflow ohne externe Abhängigkeiten"""
    
    def __init__(self):
        pass
    
    def generate_storyline(self, input_data: StorylineInput) -> StorylineData:
        """Generiert eine einfache Storyline ohne LLM"""
        painpoints = [
            "Karriere-Entwicklung",
            "Work-Life-Balance",
            "Team-Kultur",
            "Gehaltsentwicklung",
            "Anerkennung"
        ]
        
        storyline = f"""Stelle dir vor, du bist {input_data.target_audience} und suchst nach einer neuen Herausforderung. 
        Bei {input_data.company} findest du nicht nur eine Position als {input_data.stellentitel}, sondern eine 
        Umgebung, die deine Karriere-Entwicklung fördert und deine Work-Life-Balance respektiert. 
        Hier wirst du Teil eines Teams, das Innovation schätzt und deine Expertise anerkennt."""
        
        return StorylineData(
            painpoints=painpoints,
            emotional_focus="empathisch",
            target_audience_analysis=f"Zielgruppe: {input_data.target_audience}",
            storyline=storyline,
            emotional_impact="Empathischer Fokus auf Karriere-Entwicklung",
            visual_elements=["professional office", "collaborative workspace", "modern environment"]
        )
    
    def generate_midjourney_prompt(self, storyline_data: StorylineData, input_data: StorylineInput) -> MidjourneyPrompt:
        """Generiert einen einfachen Midjourney-Prompt"""
        prompt = f"""Professional job advertisement image: {input_data.headline}, {input_data.subline}, 
        Position: {input_data.stellentitel}, Location: {input_data.location}, 
        modern office environment, professional lighting, high quality, 4k, 
        emotional storytelling, {storyline_data.emotional_focus} focus"""
        
        return MidjourneyPrompt(
            prompt=prompt,
            emotional_focus=storyline_data.emotional_focus,
            visual_style="professionell",
            lighting_mood="professionell",
            composition="zentriert",
            quality_notes="hohe Qualität, 4K"
        )

# Export der Hauptklasse
__all__ = ['StorylineMidjourneyWorkflow', 'StorylineInput', 'StorylineData', 'MidjourneyPrompt', 'FallbackStorylineWorkflow']
