#!/usr/bin/env python3
"""
Preview: Zeigt Overlay-Spez der Textzonen und den Hybrid-Prompt (SCENE/VISUAL/STYLE/TECH)
für ausgewählte Layouts.
"""

from typing import Dict, Any

import os
import sys

# Projekt-Root in sys.path aufnehmen
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline import run_pipeline
from creative_core.prompt_composer.compose import compose


def build_design_defaults() -> Dict[str, Any]:
    return {
        "__validated__": True,
        "colors": {
            "primary": "#005EA5",
            "secondary": "#B4D9F7",
            "accent": "#FFC20E",
            "background": "#FFFFFF",
        },
    }


def print_overlay(layout: Dict[str, Any]) -> None:
    zones = layout.get("zones", {})
    print("\n-- OVERLAY (text zones) --")
    for name, z in zones.items():
        if isinstance(z, dict) and z.get("content_type") == "text_elements":
            cs = z.get("container_style", {}) or {}
            bg = cs.get("background", {}) or {}
            print(
                f"{name}: (x={z.get('x')}, y={z.get('y')}) {z.get('width')}x{z.get('height')} "
                f"corner_radius={cs.get('border_radius')} bg_opacity={bg.get('opacity')}"
            )


def preview_layout(layout_id: str, image_text_ratio: int = 50, container_transparency: int = 80) -> None:
    print("\n" + "=" * 88)
    print(f"LAYOUT: {layout_id}  (ratio={image_text_ratio}, transparency={container_transparency})")
    print("=" * 88)

    # 1) Pipeline: Laden + Engine + Style-Resolver + Validation
    layout = run_pipeline(
        layout_id,
        image_text_ratio=image_text_ratio,
        container_transparency=container_transparency,
        validate=True,
    )

    # 2) Overlay-Spezifikation (Textzonen)
    print_overlay(layout)

    # 3) Prompt bauen
    design = build_design_defaults()
    texts: Dict[str, Any] = {"headline": "{HEADLINE}", "subline": "{SUBHEAD}", "cta": "{CTA}"}
    motive: Dict[str, Any] = {}
    prompt = compose(layout, design, texts, motive)

    print("\n-- PROMPT (SCENE/VISUAL/STYLE/TECH) --")
    print(prompt)


def main() -> None:
    # Beispiel-Previews
    preview_layout("skizze1_vertical_split", image_text_ratio=50, container_transparency=80)
    preview_layout("skizze8_hero_layout", image_text_ratio=60, container_transparency=70)


if __name__ == "__main__":
    main()


