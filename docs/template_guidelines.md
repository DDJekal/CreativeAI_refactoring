# Template Guidelines (Layouts)

Ziel: YAML-Templates enthalten ausschliesslich Geometrie und Semantik – keine Styles.

## Do
- Zonen-Geometrie angeben: `x`, `y`, `width`, `height`, optional `z`
- Semantik: `content_type` (z. B. `text_elements`, `image_motiv`), `description`
- Klare Zonen-Namen gemaess Rollen-Konvention (z. B. `headline_block`, `subline_block`, `cta_block`)

## Don’t
- Keine Style-Felder in Templates:
  - `style`, `container_style`
  - `opacity`, `alpha`, `transparency`
  - `background_*` (z. B. `background_color`, `background_opacity`)
  - `border`, `shadow`, `radius`, `shape`, `texture`, `accent`
  - `color`, `fill`, `stroke`
- Keine Top-Level-Styles/Themes: `ci_colors`, `design`, `styles`, `theme`

## Hinweise
- Styles werden ausschliesslich zur Laufzeit vom Style-Resolver gesetzt.
- Motiv-Zonen (`image_motiv`, `motiv_area`) werden nicht gestylt; nur Geometrie.
- Zonen-Namen sollten moeglichst der `ZONE_ROLE_MAP` entsprechen, damit Rollen korrekt erkannt werden.

## Beispiele
- Do:
```yaml
zones:
  headline_block:
    x: 40
    y: 120
    width: 400
    height: 100
    content_type: text_elements
    description: Hauptueberschrift
```

- Don’t:
```yaml
zones:
  headline_block:
    x: 40
    y: 120
    width: 400
    height: 100
    content_type: text_elements
    background_color: "#FFFFFF"   # verboten
    container_style: { shadow: ... }  # verboten
```
