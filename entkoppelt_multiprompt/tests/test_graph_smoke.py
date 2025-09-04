from entkoppelt_multiprompt.graph import build_app
from entkoppelt_multiprompt.tests.fixtures import spec_diag_full


def test_graph_smoke():
    app = build_app()
    state = spec_diag_full()
    out = app(state)
    assert isinstance(out, dict)
    assert "meta" in out
    assert out.get("semantics") is not None
    # Bei gueltiger Konfiguration sollte DALL·E-Prompt vorhanden sein (keine Errors)
    assert out.get("dalle_prompt")
    overview = out["semantics"].get("layout_overview", "")
    assert "Diagonal" in overview or "Vollbild" in overview


