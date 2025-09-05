#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
evaluation/database.py

Datenbankmodul für Element-Bewertungen und Wahrscheinlichkeitsanpassung
"""

import sqlite3
import json
import random
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ElementEvaluationDB:
    """Datenbank für Element-Bewertungen und Wahrscheinlichkeitsanpassung"""
    
    def __init__(self, db_path: str = "evaluation_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialisiert die Datenbank mit den notwendigen Tabellen"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabelle für Element-Bewertungen
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS element_ratings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    element_type TEXT NOT NULL,  -- z.B. 'layout_style', 'container_shape'
                    element_value TEXT NOT NULL,  -- z.B. 'abgerundet_modern', 'capsule'
                    rating INTEGER NOT NULL,     -- 1-10 Bewertung
                    session_id TEXT,             -- Session für Gruppierung
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    context TEXT                 -- Zusätzlicher Kontext (Layout-ID, etc.)
                )
            """)
            
            # Tabelle für generierte Prompts und deren Bewertungen
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prompt_evaluations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    prompt_text TEXT NOT NULL,
                    generated_elements TEXT NOT NULL,  -- JSON der generierten Elemente
                    overall_rating INTEGER,            -- Gesamtbewertung des Prompts
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabelle für aktuelle Wahrscheinlichkeiten
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS element_probabilities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    element_type TEXT NOT NULL,
                    element_value TEXT NOT NULL,
                    base_probability REAL DEFAULT 1.0,  -- Basis-Wahrscheinlichkeit
                    current_probability REAL DEFAULT 1.0,  -- Aktuelle Wahrscheinlichkeit
                    total_ratings INTEGER DEFAULT 0,    -- Anzahl Bewertungen
                    average_rating REAL DEFAULT 5.0,    -- Durchschnittsbewertung
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(element_type, element_value)
                )
            """)
            
            conn.commit()
    
    def add_element_rating(self, element_type: str, element_value: str, 
                          rating: int, session_id: str = None, context: str = None):
        """Fügt eine Element-Bewertung hinzu"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO element_ratings 
                (element_type, element_value, rating, session_id, context)
                VALUES (?, ?, ?, ?, ?)
            """, (element_type, element_value, rating, session_id, context))
            conn.commit()
            
            # Wahrscheinlichkeiten aktualisieren
            self._update_probabilities(element_type, element_value)
    
    def add_prompt_evaluation(self, session_id: str, prompt_text: str, 
                             generated_elements: Dict, overall_rating: int = None):
        """Fügt eine Prompt-Bewertung hinzu"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO prompt_evaluations 
                (session_id, prompt_text, generated_elements, overall_rating)
                VALUES (?, ?, ?, ?)
            """, (session_id, prompt_text, json.dumps(generated_elements), overall_rating))
            conn.commit()
    
    def _update_probabilities(self, element_type: str, element_value: str):
        """ULTRA-DEZENTE Wahrscheinlichkeitsanpassung"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT AVG(rating), COUNT(*) 
                FROM element_ratings 
                WHERE element_type = ? AND element_value = ?
            """, (element_type, element_value))
            
            avg_rating, total_ratings = cursor.fetchone()
            avg_rating = avg_rating or 5.0
            total_ratings = total_ratings or 0
            
            # ULTRA-DEZENTE Anpassung
            # 👎 = 2 → 0.85x (15% weniger)
            # 😐 = 5 → 1.0x (neutral)
            # 👍 = 9 → 1.15x (15% mehr)
            
            if avg_rating <= 3:
                probability_multiplier = 0.85
            elif avg_rating <= 7:
                probability_multiplier = 1.0
            else:
                probability_multiplier = 1.15
            
            # Bei sehr wenigen Bewertungen noch konservativer
            if total_ratings < 3:
                probability_multiplier = 1.0  # Keine Änderung bei < 3 Bewertungen
            elif total_ratings < 5:
                probability_multiplier = max(0.9, min(1.1, probability_multiplier))
            
            cursor.execute("""
                INSERT OR REPLACE INTO element_probabilities 
                (element_type, element_value, current_probability, total_ratings, 
                 average_rating, last_updated)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (element_type, element_value, probability_multiplier, total_ratings, avg_rating))
            
            conn.commit()
    
    def get_weighted_choice(self, element_type: str, choices: List[str]) -> str:
        """Wählt ein Element basierend auf gewichteten Wahrscheinlichkeiten"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Wahrscheinlichkeiten für alle verfügbaren Elemente abrufen
            probabilities = {}
            for choice in choices:
                cursor.execute("""
                    SELECT current_probability FROM element_probabilities 
                    WHERE element_type = ? AND element_value = ?
                """, (element_type, choice))
                
                result = cursor.fetchone()
                probabilities[choice] = result[0] if result else 1.0  # Standard-Wahrscheinlichkeit
            
            # Gewichtete Zufallsauswahl
            return self._weighted_random_choice(probabilities)
    
    def _weighted_random_choice(self, probabilities: Dict[str, float]) -> str:
        """Führt eine gewichtete Zufallsauswahl durch"""
        choices = list(probabilities.keys())
        weights = list(probabilities.values())
        
        # Normalisierung der Gewichte
        total_weight = sum(weights)
        if total_weight == 0:
            return random.choice(choices)
        
        normalized_weights = [w / total_weight for w in weights]
        
        # Gewichtete Zufallsauswahl
        return random.choices(choices, weights=normalized_weights)[0]
    
    def get_evaluation_stats(self, element_type: str = None) -> Dict:
        """Gibt Statistiken über die Bewertungen zurück"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if element_type:
                cursor.execute("""
                    SELECT er.element_value, AVG(er.rating), COUNT(*), COALESCE(ep.current_probability, 1.0)
                    FROM element_ratings er
                    LEFT JOIN element_probabilities ep 
                    ON er.element_type = ep.element_type AND er.element_value = ep.element_value
                    WHERE er.element_type = ?
                    GROUP BY er.element_value
                    ORDER BY AVG(er.rating) DESC
                """, (element_type,))
            else:
                cursor.execute("""
                    SELECT er.element_type, er.element_value, AVG(er.rating), COUNT(*), COALESCE(ep.current_probability, 1.0)
                    FROM element_ratings er
                    LEFT JOIN element_probabilities ep 
                    ON er.element_type = ep.element_type AND er.element_value = ep.element_value
                    GROUP BY er.element_type, er.element_value
                    ORDER BY er.element_type, AVG(er.rating) DESC
                """)
            
            results = cursor.fetchall()
            
            stats = {}
            for row in results:
                if element_type:
                    stats[row[0]] = {
                        'average_rating': round(row[1], 2),
                        'total_ratings': row[2],
                        'current_probability': row[3]
                    }
                else:
                    if row[0] not in stats:
                        stats[row[0]] = {}
                    stats[row[0]][row[1]] = {
                        'average_rating': round(row[2], 2),
                        'total_ratings': row[3],
                        'current_probability': row[4]
                    }
            
            return stats
