from pathlib import Path
import yaml

from tools.template_lint.forbidden_fields import FORBIDDEN_ZONE_KEYS, FORBIDDEN_TOPLEVEL_KEYS


def iter_templates():
    root = Path(__file__).resolve().parents[1]
    return sorted((root / 'input_config' / 'layouts').glob('skizze*_*.yaml'))


def test_templates_have_no_forbidden_keys():
    bad = []
    for fp in iter_templates():
        data = yaml.safe_load(fp.read_text(encoding='utf-8'))
        # Top-level forbidden
        for k in FORBIDDEN_TOPLEVEL_KEYS:
            if k in data:
                bad.append((str(fp), f'toplevel:{k}'))
        # Zones forbidden
        zones = data.get('zones', {}) or {}
        for zname, z in zones.items():
            if isinstance(z, dict):
                for k in FORBIDDEN_ZONE_KEYS:
                    if k in z:
                        bad.append((str(fp), f'zone:{zname}:{k}'))
    assert not bad, 'Forbidden keys found: ' + ', '.join([f'{f}:{k}' for f, k in bad])


def test_templates_zone_minimum_fields():
    missing = []
    required = {'x', 'y', 'width', 'height', 'content_type'}
    for fp in iter_templates():
        data = yaml.safe_load(fp.read_text(encoding='utf-8'))
        zones = data.get('zones', {}) or {}
        for zname, z in zones.items():
            if isinstance(z, dict):
                present = {k for k in z.keys()}
                if not required.issubset(present):
                    missing.append((str(fp), zname, sorted(list(required - present))))
    assert not missing, 'Zones missing required fields: ' + ', '.join([f'{f}:{z}:{m}' for f, z, m in missing])


