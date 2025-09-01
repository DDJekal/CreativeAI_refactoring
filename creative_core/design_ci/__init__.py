"""
Design CI Module - Synergistische Style & Design Regeln

Verantwortlich für:
- Synergistische Design-Regeln basierend auf Layout-Koordinaten
- CI-Farben und Container-Styles
- Typografie-Berechnung aus Zonen-Dimensionen
- Kontrast-Validierung und Akzent-Elemente
"""

from .rules import apply_rules, apply_rules_legacy, DesignValidationError, process_design_ci

__all__ = ['apply_rules', 'apply_rules_legacy', 'DesignValidationError', 'process_design_ci']
