#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
evaluation/weighted_generator.py

Gewichtete Element-Generierung basierend auf Bewertungen
"""

import random
from typing import List, Dict, Any
from .database import ElementEvaluationDB

class WeightedElementGenerator:
    """Generator für gewichtete Element-Auswahl basierend auf Bewertungen"""
    
    def __init__(self, db: ElementEvaluationDB):
        self.db = db
    
    def get_weighted_layout_style(self) -> str:
        """Gewichtete Auswahl für Layout-Style"""
        choices = [
            "abgerundet_modern", "scharf_zeitgemaess", "organisch_fliessend", 
            "geometrisch_praezise", "neon_tech", "editorial_clean", 
            "soft_neumorph", "glassmorph_minimal", "clay_ui", "warm_documentary"
        ]
        return self.db.get_weighted_choice("layout_style", choices)
    
    def get_weighted_container_shape(self) -> str:
        """Gewichtete Auswahl für Container-Form"""
        choices = [
            "abgerundet", "scharf", "organisch", "geometrisch", "capsule", 
            "ribbon", "tag", "asymmetrisch", "hexagon", "diamond", "pill",
            "rounded_square", "soft_rectangle", "wave", "cloud", "bubble"
        ]
        return self.db.get_weighted_choice("container_shape", choices)
    
    def get_weighted_border_style(self) -> str:
        """Gewichtete Auswahl für Rahmen-Style"""
        choices = [
            "keine", "weicher_schatten", "harte_konturen", "gradient_rand",
            "doppelstrich", "innenlinie", "emboss", "outline_glow"
        ]
        return self.db.get_weighted_choice("border_style", choices)
    
    def get_weighted_texture_style(self) -> str:
        """Gewichtete Auswahl für Textur-Style"""
        choices = [
            "farbverlauf", "glaseffekt", "matte_oberflaeche", "strukturiert",
            "paper_grain", "film_grain", "noise_gradient", "subtle_pattern",
            "soft_neumorph", "emboss_deboss"
        ]
        return self.db.get_weighted_choice("texture_style", choices)
    
    def get_weighted_background_treatment(self) -> str:
        """Gewichtete Auswahl für Hintergrund-Behandlung"""
        choices = [
            "transparent", "vollflaechig", "gradient", "subtiles_muster",
            "duotone_motivtint", "vignette_soft", "depth_layers"
        ]
        return self.db.get_weighted_choice("background_treatment", choices)
    
    def get_weighted_corner_radius(self) -> str:
        """Gewichtete Auswahl für Ecken-Radius"""
        choices = [
            "klein_8px", "mittel_16px", "gross_24px", "sehr_gross_32px",
            "auto_radius", "minimal_4px", "extra_gross_40px", "asymmetrisch",
            "variable", "organic", "sharp_corners", "mixed_radius"
        ]
        return self.db.get_weighted_choice("corner_radius", choices)
    
    def get_weighted_accent_elements(self) -> str:
        """Gewichtete Auswahl für Akzent-Elemente"""
        choices = [
            "modern_minimal", "sanft_organisch", "geometrisch_praezise", 
            "kreativ_verspielt", "micro_badges", "divider_dots", "icon_chips"
        ]
        return self.db.get_weighted_choice("accent_elements", choices)
    
    def get_weighted_typography_style(self) -> str:
        """Gewichtete Auswahl für Typografie-Style"""
        choices = [
            "humanist_sans", "grotesk_bold", "serif_editorial", 
            "mono_detail", "rounded_sans"
        ]
        return self.db.get_weighted_choice("typography_style", choices)
    
    def get_weighted_photo_treatment(self) -> str:
        """Gewichtete Auswahl für Foto-Behandlung"""
        choices = [
            "natural_daylight", "cinematic_warm", "clean_clinic", 
            "documentary_soft_grain", "duotone_subtle", "bokeh_light"
        ]
        return self.db.get_weighted_choice("photo_treatment", choices)
    
    def get_weighted_depth_style(self) -> str:
        """Gewichtete Auswahl für Tiefen-Style"""
        choices = [
            "soft_shadow_stack", "drop_inner_shadow", "card_elevation_1",
            "card_elevation_2", "card_elevation_3"
        ]
        return self.db.get_weighted_choice("depth_style", choices)
    
    def get_weighted_motiv_quality(self) -> str:
        """Gewichtete Auswahl für Motiv-Qualität"""
        choices = [
            "authentisch_warm", "professionell_vertrauensvoll", "einfuehlsam_menschlich",
            "dynamisch_energetisch", "ruhig_beruhigend", "inspirierend_motivierend",
            "vertrauensvoll_serioes", "freundlich_einladend", "modern_zeitgemaess"
        ]
        return self.db.get_weighted_choice("motiv_quality", choices)
    
    def get_weighted_motiv_style(self) -> str:
        """Gewichtete Auswahl für Motiv-Style"""
        choices = [
            "natuerlich_candid", "documentary_stil", "studio_professional", 
            "cinematisch_dramatisch", "kuenstlerisch_kreativ"
        ]
        return self.db.get_weighted_choice("motiv_style", choices)
    
    def get_weighted_lighting_type(self) -> str:
        """Gewichtete Auswahl für Beleuchtung"""
        choices = [
            "natuerliches_tageslicht", "studio_beleuchtung", "dramatisches_licht", 
            "sanftes_licht", "kontrastreiches_licht"
        ]
        return self.db.get_weighted_choice("lighting_type", choices)
    
    def get_weighted_framing(self) -> str:
        """Gewichtete Auswahl für Framing"""
        choices = [
            "nahaufnahme", "halbtotale", "totale", "detailaufnahme", "gruppenaufnahme"
        ]
        return self.db.get_weighted_choice("framing", choices)
    
    def generate_weighted_elements(self) -> Dict[str, str]:
        """Generiert alle Elemente mit gewichteter Auswahl"""
        return {
            'layout_style': self.get_weighted_layout_style(),
            'container_shape': self.get_weighted_container_shape(),
            'border_style': self.get_weighted_border_style(),
            'texture_style': self.get_weighted_texture_style(),
            'background_treatment': self.get_weighted_background_treatment(),
            'corner_radius': self.get_weighted_corner_radius(),
            'accent_elements': self.get_weighted_accent_elements(),
            'typography_style': self.get_weighted_typography_style(),
            'photo_treatment': self.get_weighted_photo_treatment(),
            'depth_style': self.get_weighted_depth_style(),
            'motiv_quality': self.get_weighted_motiv_quality(),
            'motiv_style': self.get_weighted_motiv_style(),
            'lighting_type': self.get_weighted_lighting_type(),
            'framing': self.get_weighted_framing()
        }
