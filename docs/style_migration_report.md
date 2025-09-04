# Style & Transparenz Inventar-Report

Stand: automatischer Scan nach `container_style`, `transparency`, `opacity`, `alpha` im Projekt.

## Fundstellen (Auszug)

```startLine:endLine:creative_core/layout/engine.py
498:                # Container-Style für sichtbare Container
499:                container_style = {
500:                    'background_color': '#FFFFFF',
501:                    'opacity': transparency / 100,
502:                    'border_radius': 16,
503:                    'shadow': '0 4px 8px rgba(0,0,0,0.1)',
504:                    'border': 'none',
505:                    'outline': 'none'
506:                }
```

```startLine:endLine:creative_core/layout/engine.py
644:                # Container-Style für sichtbare Container
645:                container_style = {
646:                    'background_color': '#FFFFFF',
647:                    'opacity': transparency / 100,
648:                    'border_radius': 16,
649:                    'shadow': '0 4px 8px rgba(0,0,0,0.1)',
650:                    'border': 'none',
651:                    'outline': 'none'
652:                }
```

```startLine:endLine:creative_core/layout/engine.py
838:                    'transparency': transparency / 100,
841:                        'background_opacity': transparency / 100,
```

```startLine:endLine:creative_core/layout/engine.py
961:                    'transparency': transparency / 100,
964:                        'background_opacity': transparency / 100,
```

```startLine:endLine:creative_core/layout/engine.py
1081:                    'transparency': transparency / 100,
1084:                        'background_opacity': transparency / 100,
```

```startLine:endLine:creative_core/layout/engine.py
1200:                    'transparency': transparency / 100,
1203:                        'background_opacity': transparency / 100,
```

```startLine:endLine:creative_core/layout/engine.py
1260:                transparency = zone_data.get('transparency', fallback_opacity)
1265:                transparency = max(0.1, min(1.0, transparency))
1269:                zones[zone_name]['opacity'] = transparency
1270:                zones[zone_name]['alpha'] = transparency
```

```startLine:endLine:creative_core/layout/engine.py
1361:                # Container-Style für sichtbare Container (ohne Umrandung)
1362:                container_style = {
1363:                    'background_color': '#FFFFFF',
1364:                    'opacity': container_transparency / 100,
1365:                    'border_radius': 16,
1366:                    'shadow': '0 4px 8px rgba(0,0,0,0.1)',
1367:                    'border': 'none',
1368:                    'outline': 'none'
1369:                }
```

```startLine:endLine:main.py
1044:            container_style_info = zone_data.get('container_style', {})
```

## Bewertung & Risiken

- Harte `container_style`-Bloecke in Engine: Hero, Storytelling, Centered, Diagonal, Asymmetric, Grid, Split.
- Transparenz doppelt: Zonen-Level `transparency` und Engine setzt `opacity`/`alpha`; teils `container_style.opacity`.
- Migrationsbedarf: Vereinheitlichung auf `container_style.background_opacity` als einziges Darstellungsfeld.

## Empfohlene Migration

1. Resolver-Post-Step fuehrt `container_style.background_opacity` ein.
2. `apply_transparency_effects` keine Setzung von `opacity/alpha` mehr, nur Clamp.
3. Hart gesetzte `container_style` in Engine schrittweise entfernen.


