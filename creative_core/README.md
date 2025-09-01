# CreativeAI Core - Modulare Pipeline

## Architektur & Einstieg

Die neue modulare Pipeline ersetzt das monolithische `MultiPromptSystem` durch 5 spezialisierte Module in der **neuen Reihenfolge**:

### Neue Pipeline-Reihenfolge

```
Layout → Design & CI → Texte → Motiv → PromptComposer
```

### Module

1. **`layout/`** - Layout-Definitionen und -Ladung (Startpunkt)
   - `load_layout(yaml_path: str) -> dict`
   - Migriert aus: `LayoutIntegrator._load_layout_definition()`

2. **`design_ci/`** - CI-Farben und Design-Regeln  
   - `apply_rules(ci_yaml, layout_dict) -> dict`
   - Migriert aus: `LayoutIntegrator.process()` - Farb-Integration

3. **`text_inputs/`** - Text-Normalisierung und -Vorbereitung
   - `prepare_texts(user_input_yaml) -> dict`
   - Migriert aus: `InputProcessor._normalize_text()` und `InputProcessor.process()`

4. **`motive_inputs/`** - Motiv-Spezifikationen
   - `build_motive_spec(user_input_yaml) -> dict`
   - Migriert aus: `InputProcessor.process()` - motiv-bezogene Felder

5. **`prompt_composer/`** - Finale Prompt-Komposition (Endpunkt)
   - `compose(layout, design, texts, motive) -> str`
   - Migriert aus: `PromptFinalizer._generate_dalle_prompt()`

### Verwendung

```python
from creative_core.layout import load_layout
from creative_core.design_ci import apply_rules
from creative_core.text_inputs import prepare_texts
from creative_core.motive_inputs import build_motive_spec
from creative_core.prompt_composer import compose

# Pipeline in neuer Reihenfolge ausführen
layout = load_layout("layout.yaml")           # 1. Layout (Startpunkt)
design = apply_rules("ci.yaml", layout)       # 2. Design & CI
texts = prepare_texts("input.yaml")           # 3. Texte
motive = build_motive_spec("input.yaml")      # 4. Motiv
final_prompt = compose(layout, design, texts, motive)  # 5. Prompt (Endpunkt)
```

### Migration

**✅ Abgeschlossen:** Stub-Implementierungen durch echte Logik ersetzt
**✅ Abgeschlossen:** Pipeline-Reihenfolge optimiert
**🔄 Nächster Schritt:** Restliche Prompt-Finalisierung + Streamlit-Adapter

### Testing

```bash
python scripts/smoke_check.py
```

**Ausgabe:** Testet die komplette Pipeline in der neuen Reihenfolge

## TODO

- [x] Layout-Logik aus `LayoutIntegrator` migrieren
- [x] CI-Farben aus `LayoutIntegrator.process()` migrieren  
- [x] Text-Verarbeitung aus `InputProcessor` migrieren
- [x] Motiv-Generierung aus `InputProcessor.process()` migrieren
- [x] Prompt-Finalisierung aus `PromptFinalizer` migrieren
- [ ] **Nächster Schritt:** Streamlit-Adapter für `prompt_composer.compose()`
- [ ] **Nächster Schritt:** YAML-Parsing für echte Input-Dateien implementieren
