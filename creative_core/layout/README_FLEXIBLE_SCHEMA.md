# 🔧 Flexibles Layout-Schema

## Übersicht

Das neue flexible Layout-Schema ermöglicht es verschiedenen Layout-Typen, unterschiedliche Zonen zu haben, ohne dass alle Layouts alle möglichen Zonen implementieren müssen.

## 🎯 Problem gelöst

**Vorher:** Alle Layouts mussten alle möglichen Zonen haben:
- `headline_block`, `subline_block`, `benefits_block`, `cta_block`, `company_block`, `standort_block`

**Jetzt:** Jeder Layout-Typ definiert seine eigenen Anforderungen:
- **Erforderliche Zonen:** Müssen vorhanden sein
- **Optionale Zonen:** Können vorhanden sein, sind aber nicht erforderlich

## 📋 Layout-Typ-spezifische Anforderungen

### Traditionelle Layouts (Skizze 1-6, 9-10)
```yaml
required: ["headline_block", "subline_block", "benefits_block"]
optional: ["logo_area", "cta_block", "company_block", "standort_block", "motiv_block"]
```

### Minimalistisches Layout (Skizze 7)
```yaml
required: ["headline_block", "subline_block"]
optional: ["logo_area", "cta_block", "motiv_block"]
```

### Hero Layout (Skizze 8)
```yaml
required: ["hero_headline", "hero_subline"]
optional: ["logo_area", "cta_block", "motiv_block"]
```

### Portfolio Layout (Skizze 13)
```yaml
required: ["portfolio_headline", "portfolio_subline", "showcase_1"]
optional: ["logo_area", "cta_block", "motiv_block", "showcase_2", "showcase_3"]
```

## 🚀 Verwendung

### 1. Standard-Validierung (mit Warnungen)
```python
from creative_core.layout.schema import validate_layout_with_warnings

result = validate_layout_with_warnings(layout_dict)
errors = result['errors']      # Kritische Fehler
warnings = result['warnings']  # Warnungen (verhindern nicht die Verarbeitung)
```

### 2. Strikte Validierung (nur Fehler)
```python
from creative_core.layout.schema import validate_layout_strict

errors = validate_layout_strict(layout_dict)  # Nur kritische Fehler
```

### 3. Zone-Anforderungen abfragen
```python
from creative_core.layout.schema import get_layout_zone_requirements

requirements = get_layout_zone_requirements("dynamic_minimalist_layout")
print(f"Erforderlich: {requirements['required']}")
print(f"Optional: {requirements['optional']}")
```

### 4. Prüfen ob Zone erforderlich ist
```python
from creative_core.layout.schema import is_zone_required

is_required = is_zone_required("dynamic_minimalist_layout", "benefits_block")
# False - benefits_block ist nicht erforderlich für minimalistisches Layout
```

## 🔍 Validierungslogik

### Erforderliche Zonen
- **Müssen** im Layout vorhanden sein
- Fehlen führt zu einem **Validierungsfehler**
- Layout kann nicht verarbeitet werden

### Optionale Zonen
- **Können** im Layout vorhanden sein
- Fehlen führt zu **keinem Fehler**
- Layout wird normal verarbeitet

### Unerwartete Zonen
- Zonen, die weder erforderlich noch optional sind
- Führen zu einer **Warnung** (kein Fehler)
- Layout wird trotzdem verarbeitet

## 📝 Beispiel-Validierung

```python
# Minimalistisches Layout (Skizze 7)
layout = {
    "layout_type": "dynamic_minimalist_layout",
    "zones": {
        "headline_block": {...},      # ✅ Erforderlich
        "subline_block": {...},       # ✅ Erforderlich
        "logo_area": {...},           # ✅ Optional
        "cta_block": {...},           # ✅ Optional
        # "benefits_block" fehlt      # ✅ Nicht erforderlich
        # "company_block" fehlt       # ✅ Nicht erforderlich
        # "standort_block" fehlt      # ✅ Nicht erforderlich
    }
}


elif layout_type == 'dynamic_portfolio_layout':
    return self._calculate_portfolio_layout(
        layout_dict, text_width, image_width, container_transparency
    )
elif layout_type == 'dynamic_storytelling_layout':
    return self._calculate_storytelling_layout(
        layout_dict, text_width, image_width, container_transparency
    )
elif layout_type == 'dynamic_infographic_layout':
    return self._calculate_infographic_layout(
        layout_dict, text_width, image_width, container_transparency
    )
elif layout_type == 'dynamic_magazine_layout':
    return self._calculate_magazine_layout(
        layout_dict, text_width, image_width, container_transparency
    )
else:
    # Fallback auf vertikale Aufteilung
    return self._calculate_vertical_split(
        layout_dict, text_width, image_width, container_transparency
    )

    
# Validierung erfolgreich! ✅
```

## 🛠️ Layout-Engine Integration

Der Layout-Engine unterstützt jetzt:

```python
from creative_core.layout.engine import LayoutEngine

engine = LayoutEngine()

# Mit Warnungen (Standard)
result = engine.calculate_layout_coordinates(layout_dict, strict_validation=False)

# Strikte Validierung
result = engine.calculate_layout_coordinates(layout_dict, strict_validation=True)
```

## 🧪 Testen

```bash
# Teste das flexible Schema
python scripts/test_flexible_schema.py
```

## 📊 Vorteile

1. **Flexibilität:** Jedes Layout kann seine eigenen Zonen definieren
2. **Klarheit:** Klare Unterscheidung zwischen erforderlichen und optionalen Zonen
3. **Wartbarkeit:** Einfach neue Layout-Typen hinzufügen
4. **Rückwärtskompatibilität:** Bestehende Layouts funktionieren weiterhin
5. **Warnungen:** Benutzer werden über unerwartete Zonen informiert

## 🔮 Zukunft

Das Schema kann einfach erweitert werden:

```python
LAYOUT_TYPE_REQUIREMENTS["neuer_layout_typ"] = {
    "required": ["neue_erforderliche_zone"],
    "optional": ["neue_optionale_zone"]
}
```
