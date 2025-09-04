import argparse
import sys
from pathlib import Path
from typing import Any, Dict

import yaml

from .forbidden_fields import FORBIDDEN_ZONE_KEYS, FORBIDDEN_TOPLEVEL_KEYS


def remove_forbidden(obj: Any, removed: Dict[str, int]) -> Any:
    if isinstance(obj, dict):
        # Remove forbidden top-level keys
        for k in list(obj.keys()):
            if k in FORBIDDEN_TOPLEVEL_KEYS:
                removed[k] = removed.get(k, 0) + 1
                obj.pop(k, None)
        # Zones cleanup
        if 'zones' in obj and isinstance(obj['zones'], dict):
            for zname, z in obj['zones'].items():
                if isinstance(z, dict):
                    for k in list(z.keys()):
                        if k in FORBIDDEN_ZONE_KEYS:
                            removed[f"zone:{k}"] = removed.get(f"zone:{k}", 0) + 1
                            z.pop(k, None)
        # Recurse
        for k, v in list(obj.items()):
            obj[k] = remove_forbidden(v, removed)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            obj[i] = remove_forbidden(v, removed)
    return obj


def find_yaml_files(root: Path) -> list[Path]:
    globs = ["input_config/layouts/skizze*_*.yaml"]
    files: list[Path] = []
    for g in globs:
        files.extend(root.glob(g))
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean layout templates from style/legacy keys")
    parser.add_argument("--check", action="store_true", help="Only check; non-zero exit if changes would be made")
    parser.add_argument("--fix", action="store_true", help="Write cleaned YAMLs back to disk")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[2]
    files = find_yaml_files(root)

    would_change = False
    for fp in files:
        text = fp.read_text(encoding="utf-8")
        data = yaml.safe_load(text)
        removed: Dict[str, int] = {}
        cleaned = remove_forbidden(data, removed)
        if removed:
            would_change = True
            summary = ", ".join([f"{k}:{v}" for k, v in sorted(removed.items())])
            print(f"CLEAN {fp}: {summary}")
            if args.fix:
                fp.write_text(yaml.safe_dump(cleaned, allow_unicode=True, sort_keys=False), encoding="utf-8")
    if args.check and would_change:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())


