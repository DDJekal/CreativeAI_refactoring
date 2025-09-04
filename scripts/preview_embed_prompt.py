#!/usr/bin/env python3
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline import run_pipeline
from creative_core.prompt_composer.compose import compose


def main():
    layout = run_pipeline("skizze1_vertical_split", image_text_ratio=50, container_transparency=80)

    design = {
        "__validated__": True,
        "colors": {
            "primary":"#8E24AA","secondary":"#F3E5F5","accent":"#FFC107","background":"#E8F5E8"
        },
        "background_opacity":"0.84–0.90","corner_radius":16,"shadow_blur":"10–16"
    }
    user_inputs = {
        "headline": "Pflegefachkraft (m/w/d)",
        "subline":  "Herz. Team. Wirkung. Starte bei uns durch!",
        "cta":      "Jetzt bewerben",
        "benefits": ["30 Urlaubstage","Tarifgehalt + Zuschläge","Fort- & Weiterbildung","Jobrad"],
        "stellentitel": "Exam. Pflegefachkraft",
        "location": "München"
    }

    prompt = compose(layout, design, user_inputs, {}, embed_text_in_image=True)
    print(prompt)


if __name__ == "__main__":
    main()


