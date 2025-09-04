import re

from creative_core.prompt_composer.compose import compose


def _sample_layout():
    return {
        "__validated__": True,
        "layout_type": "vertical_split",
        "canvas": {"width": 1080, "height": 1080, "aspect_ratio": "1:1"},
        "zones": {
            "headline_block": {"content_type": "text_elements", "x": 40, "y": 120, "width": 400, "height": 100,
                                 "container_style": {"background": {"opacity": 0.86}, "border_radius": 16}},
            "subline_block": {"content_type": "text_elements", "x": 40, "y": 240, "width": 400, "height": 80,
                                "container_style": {"background": {"opacity": 0.86}, "border_radius": 16}},
            "benefits_block": {"content_type": "text_elements", "x": 40, "y": 340, "width": 400, "height": 200,
                                  "container_style": {"background": {"opacity": 0.86}, "border_radius": 16}},
            "cta_block": {"content_type": "text_elements", "x": 140, "y": 680, "width": 300, "height": 80,
                           "container_style": {"background": {"opacity": 0.86}, "border_radius": 16}},
            "standort_block": {"content_type": "text_elements", "x": 40, "y": 40, "width": 300, "height": 60,
                                 "container_style": {"background": {"opacity": 0.86}, "border_radius": 16}},
            "stellentitel_block": {"content_type": "text_elements", "x": 40, "y": 560, "width": 400, "height": 100,
                                     "container_style": {"background": {"opacity": 0.86}, "border_radius": 16}},
            "image_motiv": {"content_type": "image_motiv", "x": 500, "y": 40, "width": 540, "height": 680}
        },
        "calculated_values": {"text_width": 440, "image_width": 540},
    }


def test_embed_prompt_contains_user_texts_and_policies():
    layout = _sample_layout()
    design = {"__validated__": True, "colors": {
        "primary": "#8E24AA", "secondary": "#F3E5F5", "accent": "#FFC107", "background": "#E8F5E8"
    }}
    user_inputs = {
        "headline": "Pflegefachkraft (m/w/d)",
        "subline": "Herz. Team. Wirkung. Starte bei uns durch!",
        "cta": "Jetzt bewerben",
        "benefits": ["30 Urlaubstage","Tarifgehalt + Zuschläge","Fort- & Weiterbildung","Jobrad"],
        "stellentitel": "Exam. Pflegefachkraft",
        "location": "München",
    }

    prompt = compose(layout, design, user_inputs, {}, embed_text_in_image=True)

    # 6 Embed-Zeilen vorhanden (enthalten deine Strings)
    assert '• LOCATION: "München"' in prompt
    assert '• HEADLINE: "Pflegefachkraft (m/w/d)"' in prompt
    assert '• SUBHEAD: "Herz. Team. Wirkung. Starte bei uns durch!"' in prompt
    assert "• BENEFITS (bulleted, up to 4): ['30 Urlaubstage', 'Tarifgehalt + Zuschläge', 'Fort- & Weiterbildung', 'Jobrad']" in prompt
    assert '• JOB TITLE: "Exam. Pflegefachkraft"' in prompt
    assert '• CTA: "Jetzt bewerben"' in prompt

    # Keine NO TEXT IN IMAGE-Zeile
    assert 'NO TEXT IN IMAGE' not in prompt

    # TECH-Zeile korrekt
    assert 'Render exactly and only these text strings' in prompt

    # Negativliste: eine Zeile und enthält Schlagworte
    m = re.search(r"- Negative: (.+)", prompt)
    assert m is not None
    neg = m.group(1)
    assert "\n" not in neg
    for kw in ["no extra text", "UI overlays", "charts/graphs"]:
        assert kw in neg

    # VISUAL motiv-agnostisch
    forbidden_visual = re.search(r"(person|model|face|smile|pose|wardrobe|emotion)", prompt, flags=re.IGNORECASE)
    assert not forbidden_visual

    # Optional: Prozent-Bänder vorhanden
    assert re.search(r"\b\d{1,2}–\d{1,2}%", prompt)


