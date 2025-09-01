"""
Motive Inputs Module - Motiv-Spezifikationen und -Verarbeitung

Verantwortlich für:
- Motiv-Spezifikation und -Generierung
- Visuelle Parameter-Verarbeitung
- Automatische Motiv-Erstellung
- Bildkontext-Integration
"""

from .spec import build_motive_spec
from .processor import MotifInputProcessor, create_motif_processor

__all__ = ['build_motive_spec', 'MotifInputProcessor', 'create_motif_processor']