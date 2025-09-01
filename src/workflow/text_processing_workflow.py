"""
LangGraph Workflow für 3-stufige Textverarbeitung
Schritt 1: Informationsextraktion
Schritt 1.5: KI-Textgenerierung (Headline & Subline)
Schritt 2: Textoptimierung
Schritt 3: Manuelle Eingabe
"""

from typing import Dict, List, Any, TypedDict
try:
    from langgraph import StateGraph, END
    from langgraph.graph import START
    LANGGRAPH_AVAILABLE = True
except ImportError:
    # Fallback für ältere Versionen
    try:
        from langgraph.graph import StateGraph, END, START
        LANGGRAPH_AVAILABLE = True
    except ImportError:
        LANGGRAPH_AVAILABLE = False
        print("⚠️ LangGraph nicht verfügbar - verwende Fallback-Modus")

import streamlit as st
import json

# State Definition
class TextProcessingState(TypedDict):
    """State für den Textverarbeitungs-Workflow"""
    # Input
    raw_text: str
    user_preferences: Dict[str, Any]
    
    # Schritt 1: Extrahierte Informationen
    extracted_data: Dict[str, Any]
    extraction_confidence: float
    
    # Schritt 1.5: KI-generierte Texte
    generated_headline: str
    generated_subline: str
    generation_quality: float
    
    # Schritt 2: Optimierte Texte
    optimized_data: Dict[str, Any]
    optimization_notes: List[str]
    
    # Schritt 3: Finale Eingaben
    final_inputs: Dict[str, Any]
    
    # Workflow Status
    current_step: str
    errors: List[str]
    warnings: List[str]

def create_text_processing_workflow():
    """Erstellt den 3-stufigen Textverarbeitungs-Workflow"""
    
    if not LANGGRAPH_AVAILABLE:
        print("⚠️ LangGraph nicht verfügbar - verwende Fallback-Workflow")
        return None
    
    try:
        # Workflow Graph erstellen
        workflow = StateGraph(TextProcessingState)
        
        # Nodes hinzufügen
        workflow.add_node("extract_information", extract_information_step)
        workflow.add_node("generate_texts", generate_texts_step)
        workflow.add_node("optimize_texts", optimize_texts_step)
        workflow.add_node("prepare_final_inputs", prepare_final_inputs_step)
        
        # Edges definieren
        workflow.add_edge(START, "extract_information")
        workflow.add_edge("extract_information", "generate_texts")
        workflow.add_edge("generate_texts", "optimize_texts")
        workflow.add_edge("optimize_texts", "prepare_final_inputs")
        workflow.add_edge("prepare_final_inputs", END)
        
        # Compile Workflow
        return workflow.compile()
    except Exception as e:
        print(f"❌ Fehler beim Erstellen des LangGraph Workflows: {e}")
        return None

def extract_information_step(state) -> dict:
    """Schritt 1: Extrahiert strukturierte Informationen aus dem Rohtext"""
    try:
        from openai import OpenAI
        
        client = OpenAI()
        
        system_prompt = """
        Du bist ein Experte für die Analyse von Stellenausschreibungen und Job-Beschreibungen.
        Extrahiere aus dem gegebenen Text die folgenden Informationen und gib sie als JSON zurück:
        
        {
            "headline": "Hauptüberschrift für die Stellenausschreibung",
            "subline": "Untertitel oder kurze Beschreibung",
            "unternehmen": "Name des Unternehmens",
            "stellentitel": "Bezeichnung der Stelle (z.B. 'Pflegekraft (m/w/d)')",
            "location": "Standort oder Arbeitsort",
            "position_long": "Detaillierte Beschreibung der Position",
            "cta": "Call-to-Action (z.B. 'Jetzt bewerben!')",
            "benefits": ["Benefit 1", "Benefit 2", "Benefit 3"],
            "job_type": "Art der Stelle (Vollzeit, Teilzeit, etc.)",
            "experience_level": "Erfahrungslevel (Einsteiger, erfahren, etc.)"
        }
        
        Wichtige Regeln:
        - Wenn Informationen fehlen, setze sie auf null
        - Stelle sicher, dass der Stellentitel das Format "Beruf (m/w/d)" hat
        - Benefits sollten als Liste von Strings zurückgegeben werden
        - Verwende deutsche Texte
        - Bewerte deine Extraktion mit einem Confidence-Score (0-1)
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": state["raw_text"]}
            ],
            temperature=0.1
        )
        
        # JSON aus der Antwort extrahieren
        result_text = response.choices[0].message.content
        extracted_data = json.loads(result_text)
        
        # Confidence Score extrahieren (falls vorhanden)
        confidence = extracted_data.pop('confidence', 0.8) if 'confidence' in extracted_data else 0.8
        
        return {
            **state,
            "extracted_data": extracted_data,
            "extraction_confidence": confidence,
            "current_step": "Schritt 1: Informationsextraktion abgeschlossen",
            "errors": [],
            "warnings": []
        }
        
    except Exception as e:
        return {
            **state,
            "errors": [f"Fehler bei der Informationsextraktion: {str(e)}"],
            "current_step": "Schritt 1: Fehler bei der Informationsextraktion"
        }

def generate_texts_step(state) -> dict:
    """Schritt 1.5: Generiert emotionalisierende Headline und Subline"""
    try:
        from openai import OpenAI
        
        client = OpenAI()
        
        # Extrahiere relevante Informationen für die Textgenerierung
        extracted = state["extracted_data"]
        company = extracted.get('unternehmen', 'Unternehmen')
        job_title = extracted.get('stellentitel', 'Stelle')
        location = extracted.get('location', 'Standort')
        benefits = extracted.get('benefits', [])
        
        system_prompt = """
        Du bist ein kreativer Texter für Stellenausschreibungen. 
        Erstelle eine kurze, prägnante und emotionalisierende Headline und Subline.
        
        Regeln:
        - Headline: Max. 50 Zeichen, emotionalisierend, prägnant
        - Subline: Max. 100 Zeichen, unterstützend, motivierend
        - Verwende deutsche Texte
        - Sei kreativ aber professionell
        - Berücksichtige die Branche und Art der Stelle
        """
        
        user_prompt = f"""
        Erstelle Headline und Subline für:
        - Unternehmen: {company}
        - Stelle: {job_title}
        - Standort: {location}
        - Benefits: {', '.join(benefits[:3])}
        
        Gib die Antwort als JSON zurück:
        {{
            "headline": "Deine Headline",
            "subline": "Deine Subline",
            "generation_notes": "Kurze Erklärung der kreativen Entscheidungen"
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        
        result_text = response.choices[0].message.content
        generated_data = json.loads(result_text)
        
        # Quality Score basierend auf Länge und Kreativität
        headline_quality = min(1.0, 50 / len(generated_data['headline'])) if generated_data['headline'] else 0.5
        subline_quality = min(1.0, 100 / len(generated_data['subline'])) if generated_data['subline'] else 0.5
        overall_quality = (headline_quality + subline_quality) / 2
        
        return {
            **state,
            "generated_headline": generated_data['headline'],
            "generated_subline": generated_data['subline'],
            "generation_quality": overall_quality,
            "current_step": "Schritt 1.5: KI-Textgenerierung abgeschlossen",
            "warnings": [f"Generierungsnotizen: {generated_data.get('generation_notes', 'Keine')}"]
        }
        
    except Exception as e:
        return {
            **state,
            "errors": [f"Fehler bei der Textgenerierung: {str(e)}"],
            "current_step": "Schritt 1.5: Fehler bei der Textgenerierung"
        }

def optimize_texts_step(state) -> dict:
    """Schritt 2: Optimiert und verkürzt alle Texte für bessere Creatives"""
    try:
        extracted = state["extracted_data"]
        generated_headline = state["generated_headline"]
        generated_subline = state["generated_subline"]
        
        optimization_notes = []
        optimized_data = {}
        
        # Headline optimieren (verwende KI-generierte oder extrahierte)
        if generated_headline and len(generated_headline) <= 50:
            optimized_data['headline'] = generated_headline
            optimization_notes.append("✅ KI-generierte Headline verwendet")
        elif extracted.get('headline') and len(extracted['headline']) <= 50:
            optimized_data['headline'] = extracted['headline']
            optimization_notes.append("✅ Extrahierte Headline verwendet")
        else:
            # Fallback: Kürze vorhandene Headline
            fallback_headline = extracted.get('headline', 'Stelle gesucht')
            if len(fallback_headline) > 50:
                optimized_data['headline'] = fallback_headline[:47] + "..."
                optimization_notes.append(f"⚠️ Headline gekürzt: {len(fallback_headline)} → {len(optimized_data['headline'])} Zeichen")
            else:
                optimized_data['headline'] = fallback_headline
        
        # Subline optimieren
        if generated_subline and len(generated_subline) <= 100:
            optimized_data['subline'] = generated_subline
            optimization_notes.append("✅ KI-generierte Subline verwendet")
        elif extracted.get('subline') and len(extracted['subline']) <= 100:
            optimized_data['subline'] = extracted['subline']
            optimization_notes.append("✅ Extrahierte Subline verwendet")
        else:
            # Fallback: Kürze vorhandene Subline
            fallback_subline = extracted.get('subline', 'Interessante Stelle mit tollen Benefits')
            if len(fallback_subline) > 100:
                optimized_data['subline'] = fallback_subline[:97] + "..."
                optimization_notes.append(f"⚠️ Subline gekürzt: {len(fallback_subline)} → {len(optimized_data['subline'])} Zeichen")
            else:
                optimized_data['subline'] = fallback_subline
        
        # CTA optimieren (max. 3 Wörter)
        if extracted.get('cta'):
            cta_words = extracted['cta'].split()
            if len(cta_words) > 3:
                optimized_data['cta'] = ' '.join(cta_words[:3])
                optimization_notes.append(f"⚠️ CTA gekürzt: {len(cta_words)} → 3 Wörter")
            else:
                optimized_data['cta'] = extracted['cta']
                optimization_notes.append("✅ CTA unverändert (bereits optimal)")
        
        # Benefits filtern (max. 3 wichtigste)
        if extracted.get('benefits') and isinstance(extracted['benefits'], list):
            benefits = extracted['benefits']
            if len(benefits) > 3:
                # Priorisiere Benefits nach Wichtigkeit
                priority_keywords = ['gehalt', 'vergütung', 'lohn', 'zeit', 'flexibel', 'fortbildung', 'team', 'arbeiten']
                
                # Bewerte Benefits nach Priorität
                scored_benefits = []
                for benefit in benefits:
                    score = 0
                    benefit_lower = benefit.lower()
                    
                    # Höchste Priorität: Gehalt/Vergütung
                    if any(keyword in benefit_lower for keyword in ['gehalt', 'vergütung', 'lohn', '€', 'euro']):
                        score += 10
                    
                    # Hohe Priorität: Zeit/Flexibilität
                    if any(keyword in benefit_lower for keyword in ['zeit', 'flexibel', 'arbeit']):
                        score += 8
                    
                    # Mittlere Priorität: Fortbildung/Entwicklung
                    if any(keyword in benefit_lower for keyword in ['fortbildung', 'weiterbildung', 'entwicklung']):
                        score += 6
                    
                    # Niedrige Priorität: Zusatzleistungen
                    if any(keyword in benefit_lower for keyword in ['team', 'kooperation', 'werkstatt']):
                        score += 4
                    
                    scored_benefits.append((benefit, score))
                
                # Sortiere nach Score und wähle Top 3
                scored_benefits.sort(key=lambda x: x[1], reverse=True)
                optimized_data['benefits'] = [benefit for benefit, score in scored_benefits[:3]]
                optimization_notes.append(f"⚠️ Benefits gefiltert: {len(benefits)} → 3 wichtigste")
            else:
                optimized_data['benefits'] = benefits
                optimization_notes.append("✅ Benefits unverändert (bereits optimal)")
        
        # Weitere Felder übernehmen
        for key in ['unternehmen', 'stellentitel', 'location', 'position_long']:
            if extracted.get(key):
                optimized_data[key] = extracted[key]
        
        return {
            **state,
            "optimized_data": optimized_data,
            "optimization_notes": optimization_notes,
            "current_step": "Schritt 2: Textoptimierung abgeschlossen"
        }
        
    except Exception as e:
        return {
            **state,
            "errors": [f"Fehler bei der Textoptimierung: {str(e)}"],
            "current_step": "Schritt 2: Fehler bei der Textoptimierung"
        }

def prepare_final_inputs_step(state) -> dict:
    """Schritt 3: Bereitet finale Eingaben für die manuelle Bearbeitung vor"""
    try:
        optimized = state["optimized_data"]
        
        # Finale Eingaben vorbereiten
        final_inputs = {
            'headline': optimized.get('headline', ''),
            'subline': optimized.get('subline', ''),
            'unternehmen': optimized.get('unternehmen', ''),
            'stellentitel': optimized.get('stellentitel', ''),
            'location': optimized.get('location', ''),
            'position_long': optimized.get('position_long', ''),
            'cta': optimized.get('cta', ''),
            'benefits': optimized.get('benefits', [])
        }
        
        # Workflow-Status aktualisieren
        workflow_summary = {
            'extraction_confidence': state.get('extraction_confidence', 0),
            'generation_quality': state.get('generation_quality', 0),
            'optimization_notes': state.get('optimization_notes', []),
            'total_optimizations': len(state.get('optimization_notes', []))
        }
        
        return {
            **state,
            "final_inputs": final_inputs,
            "current_step": "Schritt 3: Finale Eingaben vorbereitet",
            "workflow_summary": workflow_summary
        }
        
    except Exception as e:
        return {
            **state,
            "errors": [f"Fehler bei der Vorbereitung der finalen Eingaben: {str(e)}"],
            "current_step": "Schritt 3: Fehler bei der Vorbereitung"
        }

# Workflow Factory
def get_text_processing_workflow():
    """Gibt den kompilierten Workflow zurück"""
    return create_text_processing_workflow()

# Fallback-Workflow ohne LangGraph
def run_fallback_workflow(raw_text: str, user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
    """Fallback-Workflow ohne LangGraph - führt alle Schritte sequenziell aus"""
    
    if user_preferences is None:
        user_preferences = {}
    
    # Initial State
    state = {
        "raw_text": raw_text,
        "user_preferences": user_preferences,
        "extracted_data": {},
        "extraction_confidence": 0.0,
        "generated_headline": "",
        "generated_subline": "",
        "generation_quality": 0.0,
        "optimized_data": {},
        "optimization_notes": [],
        "final_inputs": {},
        "current_step": "Fallback-Workflow gestartet",
        "errors": [],
        "warnings": []
    }
    
    try:
        # Schritt 1: Informationsextraktion
        state = extract_information_step(state)
        if state.get('errors'):
            return state
        
        # Schritt 1.5: KI-Textgenerierung
        state = generate_texts_step(state)
        if state.get('errors'):
            return state
        
        # Schritt 2: Textoptimierung
        state = optimize_texts_step(state)
        if state.get('errors'):
            return state
        
        # Schritt 3: Finale Eingaben
        state = prepare_final_inputs_step(state)
        
        return state
        
    except Exception as e:
        state['errors'].append(f"Fehler im Fallback-Workflow: {str(e)}")
        return state

# Streamlit Integration
def run_text_processing_workflow(raw_text: str, user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
    """Führt den Textverarbeitungs-Workflow aus"""
    
    if user_preferences is None:
        user_preferences = {}
    
    # Versuche LangGraph Workflow
    workflow = get_text_processing_workflow()
    
    if workflow is not None:
        try:
            # Initial State als Dictionary (nicht TypedDict)
            initial_state = {
                "raw_text": raw_text,
                "user_preferences": user_preferences,
                "extracted_data": {},
                "extraction_confidence": 0.0,
                "generated_headline": "",
                "generated_subline": "",
                "generation_quality": 0.0,
                "optimized_data": {},
                "optimization_notes": [],
                "final_inputs": {},
                "current_step": "LangGraph Workflow gestartet",
                "errors": [],
                "warnings": []
            }
            
            # Workflow ausführen
            final_state = workflow.invoke(initial_state)
            return dict(final_state)
            
        except Exception as e:
            print(f"❌ LangGraph Workflow fehlgeschlagen: {e}")
            print("🔄 Verwende Fallback-Workflow...")
    
    # Fallback: Verwende sequenziellen Workflow
    print("🔄 Verwende Fallback-Workflow ohne LangGraph...")
    return run_fallback_workflow(raw_text, user_preferences)
