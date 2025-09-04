from entkoppelt_multiprompt.graph import build_app
from entkoppelt_multiprompt.tests.fixtures import spec_diag_full


def test_sections_and_length():
    app = build_app()
    out = app(spec_diag_full())
    text = out.get("dalle_prompt") or ""
    # Abschnitts-Reihenfolge
    order = [
        "Szene & Atmosphaere",
        "Komposition & Layout",
        "Form & Design",
        "Farbwelt & CI",
        "Text & Content (separate_layers)",
        "Balance & Wirkung",
        "Technische Regeln & Engine-Optimierung",
    ]
    last = -1
    for s in order:
        idx = text.find(s)
        assert idx > last
        last = idx
    # Laengencheck: darf Warnung haben, sollte aber > 1500 Zeichen sein als Ausgangsbasis
    assert len(text) > 1500


