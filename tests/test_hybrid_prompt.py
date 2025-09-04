import re

from creative_core.prompt_composer.compose import compose


def _make_design_defaults():
    return {
        "__validated__": True,
        "colors": {},
    }


def _make_vertical_split_layout():
    # 1:1 Canvas, text 480px, image 540px, gutter 60px
    layout = {
        "__validated__": True,
        "layout_type": "vertical_split",
        "canvas": {"width": 1080, "height": 1080, "aspect_ratio": "1:1"},
        "zones": {
            "headline_block": {"content_type": "text_elements", "x": 0, "y": 100, "width": 480, "height": 120,
                                 "container_style": {"background": {"opacity": 0.86}, "border_radius": 16,
                                                      "shadow": {"blur": 12, "opacity": 0.14}}},
            "image_motiv": {"content_type": "image_motiv", "x": 540, "y": 0, "width": 540, "height": 1080},
        },
        "calculated_values": {"text_width": 480, "image_width": 540}
    }
    return layout


def _make_hero_layout():
    layout = {
        "__validated__": True,
        "layout_type": "hero_layout",
        "canvas": {"width": 1080, "height": 1080, "aspect_ratio": "1:1"},
        "zones": {
            "motiv_area": {"content_type": "image_motiv", "x": 0, "y": 0, "width": 1080, "height": 540},
            "headline_block": {"content_type": "text_elements", "x": 100, "y": 700, "width": 600, "height": 120}
        },
        "calculated_values": {}
    }
    return layout


def test_vertical_split_prompt_contains_required_clauses():
    layout = _make_vertical_split_layout()
    design = _make_design_defaults()
    texts = {}
    motive = {}

    prompt = compose(layout, design, texts, motive)

    assert "NO TEXT IN IMAGE. Use placeholders only: {HEADLINE}, {SUBHEAD}, {CTA}." in prompt
    assert "text_rendering: separate_layers (outside the image)" in prompt
    assert "unobstructed gutter from top to bottom" in prompt

    # CI palette with four hex values (defaults)
    assert "CI palette: primary #005EA5, secondary #B4D9F7, accent #FFC20E, background #FFFFFF" in prompt

    # Percent bands with ranges at least 3 occurrences
    bands = re.findall(r"\b\d{1,2}–\d{1,2}%", prompt)
    assert len(bands) >= 3

    # No ASCII/umlaut hints
    assert "ASCII" not in prompt
    assert "ae/oe/ue/ss" not in prompt

    # VISUAL must not include subject/person words
    forbidden_visual = re.search(r"(subject|person|model|face|smile|pose|wardrobe|emotion)", prompt, flags=re.IGNORECASE)
    assert not forbidden_visual

    # Negative line must be a single line and contain 'no text-like patterns'
    m = re.search(r"- Negative: (.+)", prompt)
    assert m is not None
    negative_line = m.group(1)
    assert "\n" not in negative_line
    assert "no text-like patterns" in negative_line

    # Optional: sum of mid values approx 100% (±3pp)
    # extract first three ranges after 'Layout intent'
    layout_line = None
    for line in prompt.splitlines():
        if line.strip().startswith("- Layout intent:"):
            layout_line = line
            break
    assert layout_line is not None
    vals = re.findall(r"(\d{1,2})–(\d{1,2})%", layout_line)
    assert len(vals) >= 3
    mids = [(int(a) + int(b)) / 2 for a, b in vals[:3]]
    total = sum(mids)
    assert 97 <= total <= 103


def test_hero_layout_prompt_contains_hero_specific():
    layout = _make_hero_layout()
    design = _make_design_defaults()
    texts = {}
    motive = {}

    prompt = compose(layout, design, texts, motive)
    assert "pin the top image band to the top edge" in prompt
import re


def contains_line(s: str, needle: str) -> bool:
    return needle in s


def test_prompt_tokens_and_negatives():
    from creative_core.prompt_composer.compose import compose

    layout = {
        "__validated__": True,
        "layout_type": "vertical_split",
        "canvas": {"width": 1080, "height": 1080, "aspect_ratio": "1:1"},
        "calculated_values": {"text_width": 470, "image_width": 550},
        "zones": {}
    }
    design = {"__validated__": True, "colors": {"primary": "#005EA5", "secondary": "#B4D9F7", "accent": "#FFC20E", "background": "#FFFFFF"}}
    texts = {}
    motive = {}

    prompt = compose(layout, design, texts, motive, motiv_agnostic=True)

    assert contains_line(prompt, "NO TEXT IN IMAGE. Use placeholders only: {HEADLINE}, {SUBHEAD}, {CTA}.")
    assert contains_line(prompt, "text_rendering: separate_layers (outside the image)")

    neg_required = "no text-like patterns" in prompt and "no signage" in prompt and "no UI overlays" in prompt and "no charts/graphs" in prompt
    assert neg_required, "Required negative tokens missing"

    assert "ASCII" not in prompt and "ae/oe/ue/ss" not in prompt

    # VISUAL darf keine Subjekt-/Pose-/Wardrobe-/Emotion-Trigger enthalten
    forbidden = re.compile(r"\b(subject|person|pose|wardrobe|smile|emotion)\b", re.I)
    visual_section = prompt.split("VISUAL", 1)[-1]
    assert not forbidden.search(visual_section), "VISUAL contains subject-related terms"

    # SCENE enthaelt Prozentbaender
    assert re.search(r"\d+–\d+%", prompt) is not None


