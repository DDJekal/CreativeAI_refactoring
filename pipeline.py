from typing import Dict, Any, Optional
from dataclasses import dataclass


class PipelineError(Exception):
    pass


class ValidationError(PipelineError):
    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload
        super().__init__(payload.get("message", "Validation failed"))


@dataclass
class PipelineSettings:
    image_text_ratio: int = 50
    container_transparency: int = 60
    design: Optional[Dict[str, Any]] = None
    ci_colors: Optional[Dict[str, str]] = None
    seed: Optional[int] = None
    validate: bool = True


def run_pipeline(
    layout_id: str,
    *,
    image_text_ratio: int = 50,
    container_transparency: int = 60,
    design: Optional[Dict[str, Any]] = None,
    ci_colors: Optional[Dict[str, str]] = None,
    seed: Optional[int] = None,
    validate: bool = True,
    settings: Optional["PipelineSettings"] = None,
) -> Dict[str, Any]:
    """
    Orchestriert Laden, Geometrie und Style-Resolver. Keine Datei-IO, kein Console-Logging.
    Gibt finales Layout-Dict zurueck.
    """
    # Load & geometry via loader/engine
    try:
        from creative_core.layout.loader import load_layout
        from creative_core.design_ci.style_resolver import apply_design_styles  # type: ignore
    except Exception as e:
        raise PipelineError({"message": f"Import error in pipeline: {e}"})

    # Apply settings override if provided
    if settings is not None:
        image_text_ratio = settings.image_text_ratio
        container_transparency = settings.container_transparency
        design = settings.design
        ci_colors = settings.ci_colors
        seed = settings.seed
        validate = settings.validate

    # Load base layout (may include engine calc + built-in defaults)
    layout = load_layout(
        layout_id,
        image_text_ratio=image_text_ratio,
        container_transparency=container_transparency,
    )

    # Apply caller-provided design/ci overrides if present
    if design or ci_colors:
        try:
            layout = apply_design_styles(
                layout,
                design or {},
                ci_colors or {},
                override_existing=True,
            )
        except Exception as e:
            raise PipelineError({"message": f"Style resolver failed: {e}"})

    # Attach seed info (determinism surface). Engine itself is deterministic currently.
    if isinstance(layout, dict):
        cv = dict(layout.get("calculated_values", {}))
        if seed is not None:
            cv["seed"] = seed
        layout["calculated_values"] = cv

    if validate:
        validate_layout(layout)

    return layout


def validate_layout(layout: Dict[str, Any]) -> None:
    """
    Fuehrt Vertragspruefungen aus. Wirft ValidationError bei Fehlern, sonst None.
    """
    try:
        from validation import validate_layout_contract  # local module
    except Exception as e:
        raise PipelineError({"message": f"Cannot import validation: {e}"})

    try:
        validate_layout_contract(layout)
    except Exception as e:
        # Passthrough von bereits strukturierten Fehlern
        if isinstance(e, ValidationError):
            raise e
        raise ValidationError({"message": str(e)})


def derive_relative(layout):
    cv, canvas = layout.get('calculated_values', {}), layout.get('canvas', {})
    w = max(1, int(canvas.get('width', 1080)))
    text_w, img_w = int(cv.get('text_width', 0)), int(cv.get('image_width', 0))
    gutter_w = max(0, w - (text_w + img_w))
    pct = lambda x: round(100 * x / w)
    return dict(text=pct(text_w), image=pct(img_w), gutter=pct(gutter_w), safe=3)

def tol(p, d=1): return f"{p-d}–{p+d}%"

def build_scene(layout, ci, cs, ar="1:1", split=True):
    r = derive_relative(layout)
    intent = f"text-left {tol(r['text'])}, image-right {tol(r['image'])}, gutter {tol(r['gutter'])}, safe margins {r['safe']}%"
    comp = "rule-of-thirds, clear negative space, consistent vertical rhythm, " + ("gutter continuity" if split else "band anchoring")
    lines = [
      "SCENE", f"- Aspect ratio: {ar}", f"- Layout intent: {intent}",
      f"- Composition: {comp}",
      f"- CI palette: primary {ci['primary']}, secondary {ci['secondary']}, accent {ci['accent']}, background {ci['background']}",
      f"- Container look: background_opacity {cs.get('bg_opacity', 0.85)}, corner_radius {cs.get('radius', 16)}, soft shadow (blur {cs.get('blur', 12)})",
      "- NO TEXT IN IMAGE. Use placeholders only: {HEADLINE}, {SUBHEAD}, {CTA}."
    ]
    return "\n".join(lines)

def build_visual_motiv_agnostic(strict=False):
    base = ["VISUAL",
      "- Camera/Optics: 35–50mm, shallow–mid DoF, low distortion, clean micro-contrast, controlled vignetting",
      "- Lighting: soft daylight, broad bounce fill, controlled highlights, 5200–5600 K",
      "- Grading: cinematic neutral, midtone separation, highlight roll-off",
      "- Artefacts: anti-banding/aliasing/moire, no halos/bloom, minimal noise"]
    return "\n".join(base if strict else base)

def build_tech_negative(): return [
  "TECH & NEGATIVE",
  "- text_rendering: separate_layers (outside the image)",
  "- Negative: no text, no words, no letters, no typography, no logo, no watermark, no signature, no frames, no borders, no captions, blurry, lowres, pixelated, noisy, distorted, deformed, duplicate, cropped, cut off, cartoon, anime, illustration, painting, sketch, 3d render, cgi, plastic, toy, oversaturated colors, neon, abstract, disfigured, mutated, bad anatomy, broken hands, extra limbs, creepy, uncanny, dark, gloomy, depressing, violence, blood, injury, horror, messy background, cluttered"
]


