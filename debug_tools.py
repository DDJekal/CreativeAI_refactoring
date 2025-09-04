import json
from typing import Dict, Any, Iterable


def print_summary(layout: Dict[str, Any]) -> None:
    zones = layout.get("zones", {})
    txt = sum(1 for z in zones.values() if isinstance(z, dict) and z.get("content_type") == "text_elements")
    mot = sum(1 for z in zones.values() if isinstance(z, dict) and (z.get("content_type") == "image_motiv" or z.get("name") == "motiv_area"))
    cv = layout.get("calculated_values", {})
    print(
        f"zones={len(zones)} text={txt} motive={mot} ratio={cv.get('image_text_ratio')} transparency={cv.get('container_transparency')}"
    )


def dump_snapshot(layout: Dict[str, Any], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(layout, f, ensure_ascii=False, indent=2)


def iter_text_zones(layout: Dict[str, Any]) -> Iterable[str]:
    for name, z in (layout.get("zones") or {}).items():
        if isinstance(z, dict) and z.get("content_type") == "text_elements":
            yield name


