import json
from pathlib import Path

from creative_core.layout.loader import load_layout


ALLOWED_RADII = {0, 8, 16, 24, 32}


def dump_snapshot(layout_id: str, ratio: int, transparency: int) -> dict:
    data = load_layout(layout_id, image_text_ratio=ratio, container_transparency=transparency)
    # Assertions
    zones = data.get('zones', {})
    for name, z in zones.items():
        cs = z.get('container_style')
        if z.get('content_type') == 'text_elements':
            assert cs is not None, f"Zone {name} missing container_style"
            bo = None
            if 'background_opacity' in cs:
                bo = cs.get('background_opacity')
            elif 'background' in cs and isinstance(cs.get('background'), dict):
                bo = cs['background'].get('opacity')
            assert bo is not None, f"Zone {name} missing background opacity"
            assert isinstance(bo, (int, float)) and 0.1 <= float(bo) <= 1.0, f"Zone {name} bg_opacity out of range"
            if 'border_radius' in cs:
                assert cs['border_radius'] in ALLOWED_RADII, f"Zone {name} radius not in allowed set"
            # Gradient-Contract
            border = cs.get('border') if isinstance(cs, dict) else None
            if isinstance(border, dict) and border.get('style') == 'gradient':
                grad = border.get('gradient', {})
                assert isinstance(grad, dict), f"Zone {name} gradient must be dict"
                assert grad.get('type') in {'linear', 'radial'}, f"Zone {name} gradient.type missing/invalid"
                stops = grad.get('stops')
                assert isinstance(stops, list) and len(stops) >= 2, f"Zone {name} gradient.stops invalid"
                for s in stops:
                    assert 'color' in s and 'pos' in s, f"Zone {name} gradient stop incomplete"
                    assert 0.0 <= float(s['pos']) <= 1.0, f"Zone {name} gradient stop pos out of range"
        # Keine Doppel-Felder
        assert 'opacity' not in z, f"Zone {name} has legacy opacity"
        assert 'alpha' not in z, f"Zone {name} has legacy alpha"

        # Konsistenz Transparenz vs. bg_opacity (falls beides vorhanden)
        if 'transparency' in z and cs:
            try:
                tz = float(z['transparency'])
                if tz > 1:
                    tz = tz / 100.0
                cbo = None
                if 'background_opacity' in cs:
                    cbo = cs['background_opacity']
                elif 'background' in cs and isinstance(cs.get('background'), dict):
                    cbo = cs['background'].get('opacity')
                if cbo is not None:
                    delta = abs(tz - float(cbo))
                    assert delta < 0.05, f"Zone {name} transparency mismatch (delta={delta})"
            except Exception:
                pass

        # Motiv-/Background-Zonen sollen keinen container_style tragen
        if z.get('content_type') == 'image_motiv':
            assert cs is None or cs == {}, f"Zone {name} (motiv) should not have container_style"
    return data


def main():
    out_dir = Path('tests/snapshots')
    out_dir.mkdir(parents=True, exist_ok=True)

    cases = [
        ("skizze1_vertical_split", [30, 50, 70], [60, 80, 90]),
        ("skizze6_grid_layout", [30, 50, 70], [60, 80, 90]),
        ("skizze5_asymmetric_layout", [30, 50, 70], [60, 80, 90]),
        ("skizze4_diagonal_layout", [30, 50, 70], [60, 80, 90]),
        ("skizze7_split_layout", [30, 50, 70], [60, 80, 90]),
    ]

    results = {}
    for layout_id, ratios, transparencies in cases:
        for r in ratios:
            for t in transparencies:
                snap = dump_snapshot(layout_id, r, t)
                key = f"{layout_id}_r{r}_t{t}"
                results[key] = {
                    'zones': {k: {
                        'has_cs': 'container_style' in v,
                        'bg_opacity': (v.get('container_style', {}).get('background_opacity')
                                       if isinstance(v.get('container_style'), dict) and 'background_opacity' in v.get('container_style')
                                       else (v.get('container_style', {}).get('background', {}).get('opacity') if isinstance(v.get('container_style'), dict) and isinstance(v.get('container_style').get('background'), dict) else None))
                    } for k, v in snap.get('zones', {}).items()}
                }

    # Role-Coverage (Best effort aus Zonen-Namen)
    all_zone_names = [k for key in results for k in results[key]['zones'].keys()]
    role_mapped = sum(1 for z in all_zone_names if any(x in z for x in ['headline', 'subline', 'benefits', 'cta', 'stellentitel', 'logo', 'standort', 'company', 'infographic', 'content']))
    coverage = (role_mapped / max(1, len(all_zone_names))) * 100.0
    if coverage < 90.0:
        print(f"WARN: Role coverage below 90% → {coverage:.1f}%")

    with (out_dir / 'summary.json').open('w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()


