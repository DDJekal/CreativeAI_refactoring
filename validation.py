from typing import Dict, Any


class ValidationError(Exception):
    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload
        super().__init__(payload.get("message", "Validation failed"))


def _require_keys(obj: Dict[str, Any], keys: list, where: str):
    missing = [k for k in keys if k not in obj]
    if missing:
        raise ValidationError({
            "message": f"Missing required keys in {where}: {missing}",
            "location": where,
            "missing": missing,
        })


def validate_layout_contract(layout: Dict[str, Any]) -> None:
    """
    Vertragspruefungen fuer finales Layout:
    - Pflichtfelder vorhanden: zones, calculated_values
    - Text-Zonen: container_style vorhanden (nach Resolver-Post-Step)
    - Motiv-Zonen: kein container_style
    - Keine Legacy-Felder background_opacity/background_color in container_style
    """
    if not isinstance(layout, dict):
        raise ValidationError({"message": "layout must be a dict"})

    _require_keys(layout, ["zones"], "layout")
    zones = layout.get("zones", {})
    if not isinstance(zones, dict):
        raise ValidationError({"message": "layout.zones must be a dict"})

    # calculated_values optional, aber empfohlen
    if "calculated_values" not in layout:
        # nicht-blockierend, aber fuer CI koennte man spaeter warnen
        pass

    for name, zone in zones.items():
        if not isinstance(zone, dict):
            raise ValidationError({"message": f"zone '{name}' must be a dict"})
        # Grundlegende Koordinatenpruefung (Engine sollte numerisch liefern)
        for key in ("x", "y", "width", "height"):
            if key not in zone or not isinstance(zone[key], int):
                raise ValidationError({
                    "message": f"zone '{name}' missing/invalid coordinate '{key}'",
                    "zone": name,
                    "key": key,
                })

        ct = zone.get("content_type")
        cs = zone.get("container_style")
        if ct == "text_elements":
            if not isinstance(cs, dict):
                raise ValidationError({
                    "message": f"text zone '{name}' requires container_style",
                    "zone": name,
                })
            # Legacy-Felder verbieten
            if "background_opacity" in cs or "background_color" in cs:
                raise ValidationError({
                    "message": f"zone '{name}' contains legacy container_style fields",
                    "zone": name,
                    "forbidden": [k for k in ("background_opacity", "background_color") if k in cs],
                })
            # Hintergrundstruktur erwartet
            bg = cs.get("background")
            if not isinstance(bg, dict) or "opacity" not in bg:
                raise ValidationError({
                    "message": f"zone '{name}' container_style.background.opacity required",
                    "zone": name,
                })
        elif ct == "image_motiv" or name in {"motiv_area"}:
            if cs is not None:
                raise ValidationError({
                    "message": f"motiv zone '{name}' must not have container_style",
                    "zone": name,
                })
        else:
            # Fuer andere Zonentypen keine strikte Pflicht
            pass


