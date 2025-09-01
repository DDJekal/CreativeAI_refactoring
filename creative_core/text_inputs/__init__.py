"""
- Vorbereitung für Prompt-Generierung
- Erweiterte Texteingabe-Verarbeitung
"""

from .normalize import prepare_texts
from .input_processor import TextInputProcessor, create_text_processor

__all__ = ['prepare_texts', 'TextInputProcessor', 'create_text_processor']
