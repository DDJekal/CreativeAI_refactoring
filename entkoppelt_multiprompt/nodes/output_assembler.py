from typing import Any, Dict


def OutputAssembler(state: Dict[str, Any]) -> Dict[str, Any]:
    meta = state.get("meta") or {"warnings": [], "errors": [], "norm": {}}
    errors = meta.get("errors") or []
    out: Dict[str, Any] = {
        "semantics": state.get("semantics"),
        "meta": meta,
    }
    # Bei Errors Prompt nicht ausgeben
    if not errors:
        out["dalle_prompt"] = state.get("dalle_prompt")
    else:
        out["dalle_prompt"] = None
    return out


