from typing import Any, Dict


def IngestSpec(state: Dict[str, Any]) -> Dict[str, Any]:
    """Uebernimmt spec_raw oder spec und initialisiert meta.

    - Wenn ``spec`` bereits ein dict ist: uebernehmen.
    - Wenn ``spec_raw`` gesetzt ist: als String belassen; das Parsen erfolgt in ParseSpec.
    - Initialisiert ``meta`` mit leeren warnings/errors und norm-dict.
    """
    meta = state.get("meta") or {"warnings": [], "errors": [], "norm": {}}
    state["meta"] = meta

    # Wenn spec bereits ein Dict ist, uebernehmen; spec_raw ggf. auch behalten
    spec = state.get("spec")
    if isinstance(spec, dict):
        state["spec"] = spec
        return state

    # spec_raw bleibt String (wird in ParseSpec verarbeitet)
    if "spec_raw" not in state:
        state["spec_raw"] = None

    return state


