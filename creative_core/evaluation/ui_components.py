#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
evaluation/ui_components.py

Streamlit-Komponenten für das Evaluationssystem
"""

import streamlit as st
from typing import Dict, List, Optional
from .database import ElementEvaluationDB

class EvaluationInterface:
    """Streamlit-Interface für Element-Bewertungen"""
    
    def __init__(self, db: ElementEvaluationDB):
        self.db = db
    
    def show_element_evaluation_form(self, generated_elements: Dict[str, str], 
                                   session_id: str, context: str = None):
        """Bewertungsformular in einem Form-Block: Änderungen lösen keinen Rerun aus,
        erst 'Bewertungen speichern' sendet und persistiert.
        """
        st.subheader("📊 Bewertung (Daumen-Prinzip)")
        st.caption("4 Bereiche des Prompts bewerten: 👎 schlecht, 😐 neutral, 👍 gut")

        category_to_elements = {
            "Szene & Atmosphäre": ["motiv_style", "lighting_type"],
            "Komposition & Layout": ["layout_id"],
            "Form & Design": ["layout_style", "container_shape"],
            "Balance & Wirkung": ["motiv_style", "layout_style"],
        }

        symbol_options = ["👎", "😐", "👍"]
        symbol_to_score = {"👎": 2, "😐": 5, "👍": 9}

        # Defaults im Session State hinterlegen
        for category in category_to_elements.keys():
            st.session_state.setdefault(f"thumbs_sel_{category}_{session_id}", "😐")
        st.session_state.setdefault(f"overall_thumbs_sel_{session_id}", "😐")

        with st.form(f"eval_form_{session_id}"):
            for category, mapped_elements in category_to_elements.items():
                details = []
                for et in mapped_elements:
                    if et in generated_elements and generated_elements.get(et):
                        details.append(f"{et}: {generated_elements.get(et)}")

                cols = st.columns([3, 2])
                with cols[0]:
                    if details:
                        st.write(f"**{category}** – {', '.join(details)}")
                    else:
                        st.write(f"**{category}**")
                with cols[1]:
                    st.radio(
                        label=f"Bewertung – {category}",
                        options=symbol_options,
                        horizontal=True,
                        key=f"thumbs_sel_{category}_{session_id}",
                        index=symbol_options.index(st.session_state[f"thumbs_sel_{category}_{session_id}"])
                    )

            st.divider()
            st.radio(
                label="🎯 Gesamtbewertung",
                options=symbol_options,
                horizontal=True,
                key=f"overall_thumbs_sel_{session_id}",
                index=symbol_options.index(st.session_state[f"overall_thumbs_sel_{session_id}"])
            )

            submitted = st.form_submit_button("💾 Bewertungen speichern", type="primary")

        if submitted:
            for category, mapped_elements in category_to_elements.items():
                sel_symbol = st.session_state.get(f"thumbs_sel_{category}_{session_id}", "😐")
                score = symbol_to_score.get(sel_symbol, 5)
                for et in mapped_elements:
                    if et in generated_elements and generated_elements.get(et):
                        self.db.add_element_rating(
                            element_type=et,
                            element_value=generated_elements[et],
                            rating=score,
                            session_id=session_id,
                            context=context
                        )

            self.db.add_prompt_evaluation(
                session_id=session_id,
                prompt_text=generated_elements.get('prompt_text', ''),
                generated_elements=generated_elements,
                overall_rating=symbol_to_score.get(st.session_state[f"overall_thumbs_sel_{session_id}"], 5)
            )

            st.success("✅ Bewertungen gespeichert – Gewichtungen aktualisiert")

        # Rückgabe: Aktuelle Auswahl (aus Session State)
        return {
            c: st.session_state.get(f"thumbs_sel_{c}_{session_id}", "😐")
            for c in category_to_elements.keys()
        }, st.session_state.get(f"overall_thumbs_sel_{session_id}", "😐")
    
    def show_evaluation_stats(self):
        """Zeigt Statistiken über die Bewertungen"""
        st.subheader("📈 Bewertungsstatistiken")
        
        # Nur die fünf genutzten Element-Typen anzeigen
        element_types = [
            'layout_id', 'layout_style', 'container_shape', 'motiv_style', 'lighting_type'
        ]
        
        selected_type = st.selectbox("Element-Typ auswählen:", element_types)
        
        # Statistiken abrufen und anzeigen
        stats = self.db.get_evaluation_stats(selected_type)
        
        if stats:
            st.write(f"**Statistiken für {selected_type}:**")
            
            for element_value, data in stats.items():
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Element", element_value)
                
                with col2:
                    st.metric("Ø Bewertung", f"{data['average_rating']}/10")
                
                with col3:
                    st.metric("Anzahl Bewertungen", data['total_ratings'])
                
                with col4:
                    probability_percent = data['current_probability'] * 50  # 0.2-2.0 zu 10-100%
                    st.metric("Wahrscheinlichkeit", f"{probability_percent:.1f}%")
        else:
            st.info("Noch keine Bewertungen für diesen Element-Typ vorhanden.")
