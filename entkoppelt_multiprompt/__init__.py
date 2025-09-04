"""Entkoppelter Multiprompt-Baukasten.

Dieses Paket erzeugt aus einem deutschsprachigen Roh-Block einen langen
DALL·E-3 Prompt (separate_layers) sowie ein pixel-freies Semantik-JSON.

Die Implementierung ist stand-alone und benoetigt keine vorhandene
Projekt-Pipeline. Zur Minimierung externer Abhaengigkeiten wird eine
kleine Graph-Implementierung in ``langgraph`` als Stub mitgeliefert.
"""

from .graph import build_app  # re-export fuer bequemen Zugriff

__all__ = ["build_app"]


