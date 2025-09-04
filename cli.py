import json
import sys
import argparse
import logging
from typing import Optional, Dict, Any

from pipeline import run_pipeline, PipelineSettings
from validation import ValidationError


def make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser("creative-cli")
    sub = p.add_subparsers(dest="cmd", required=True)

    runp = sub.add_parser("run", help="run pipeline for a layout id")
    runp.add_argument("layout_id")
    runp.add_argument("--ratio", type=int, default=50)
    runp.add_argument("--transparency", type=int, default=60)
    runp.add_argument("--seed", type=int, default=None)
    runp.add_argument("--out", type=str, default=None)
    runp.add_argument("--diagnostics", type=str, default=None)
    runp.add_argument("--no-validate", action="store_true")
    runp.add_argument("--log-level", default="INFO")

    runp.add_argument("--summary", action="store_true")
    runp.add_argument("--snapshot", type=str, default=None)
    return p


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    args = make_parser().parse_args(argv)

    # Logging nur hier konfigurieren
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(levelname)s %(message)s",
    )

    settings = PipelineSettings(
        image_text_ratio=args.ratio,
        container_transparency=args.transparency,
        seed=args.seed,
        validate=not args.no_validate,
    )

    try:
        layout = run_pipeline(args.layout_id, settings=settings)
    except ValidationError as e:
        logging.error("validation failed: %s", e)
        return 2
    except Exception:
        logging.exception("pipeline error")
        return 1

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(layout, f, ensure_ascii=False, indent=2)

    if args.diagnostics:
        diags = {
            "layout_id": args.layout_id,
            "ratio": args.ratio,
            "transparency": args.transparency,
            "seed": args.seed,
            "zone_count": len(layout.get("zones", {})),
        }
        with open(args.diagnostics, "w", encoding="utf-8") as f:
            json.dump(diags, f, ensure_ascii=False, indent=2)

    # Optional: Debug-Ausgaben
    if args.summary or args.snapshot:
        try:
            from debug_tools import print_summary, dump_snapshot
            if args.summary:
                print_summary(layout)
            if args.snapshot:
                dump_snapshot(layout, args.snapshot)
        except Exception:
            logging.exception("debug tools failed")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


