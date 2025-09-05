"""
Prompt Composer - Finale Prompt-Komposition

Migriert aus PromptFinalizer._generate_dalle_prompt() und _generate_midjourney_prompt()
"""

from typing import Dict, Any, Tuple
import logging
import re

logger = logging.getLogger(__name__)


# NEGATIVE/Helper
NEGATIVE_LINE = (
    "no text, no words, no letters, no typography, no logo, no watermark, no signature, "
    "no frames, no borders, no captions, blurry, lowres, pixelated, noisy, distorted, "
    "deformed, duplicate, cropped, cut off, cartoon, anime, illustration, painting, sketch, "
    "3d render, cgi, plastic, toy, oversaturated colors, neon, abstract, disfigured, mutated, "
    "bad anatomy, broken hands, extra limbs, creepy, uncanny, dark, gloomy, depressing, violence, "
    "blood, injury, horror, messy background, cluttered, no text-like patterns, no signage, "
    "no UI overlays, no charts/graphs"
)


def compose(layout: Dict[str, Any], design: Dict[str, Any],
            texts: Dict[str, Any], motive: Dict[str, Any], *,
            motiv_agnostic: bool = True,
            strict_layout_mode: bool = False,
            embed_text_in_image: bool = False) -> str:
    """
    Komponiert alle Eingaben zu finalem DALL-E Prompt
    
    Args:
        layout: Layout-Definition und -Metadaten (muss __validated__=True haben)
        design: CI-Farben und Design-Regeln (muss __validated__=True haben)
        texts: Normalisierte und vorbereitete Texte
        motive: Motiv-Spezifikation und Visual-Styles
        
    Returns:
        Finaler DALL-E Prompt als String
        
    Raises:
        ValueError: Wenn Layout oder Design nicht validiert sind
    """
    # COMPOSER-GATE: Strikte Validierung der Eingaben
    if not layout.get("__validated__"):
        raise ValueError("Layout must be validated before composition")
    if not design.get("__validated__"):
        raise ValueError("Design must be validated before composition")
    
    try:
        # EMBED-TEXT MODE: Build copy-paste prompt with actual text strings
        if embed_text_in_image:
            # CI aus design.colors oder direktem design dict lesen
            colors = (design or {}).get('colors') if isinstance(design, dict) else None
            if not colors and isinstance(design, dict):
                colors = {
                    'primary': design.get('primary', '#8E24AA'),
                    'secondary': design.get('secondary', '#F3E5F5'),
                    'accent': design.get('accent', '#FFC107'),
                    'background': design.get('background', '#E8F5E8'),
                }
            ci_primary = colors.get('primary', '#8E24AA')
            ci_secondary = colors.get('secondary', '#F3E5F5')
            ci_accent = colors.get('accent', '#FFC107')
            ci_background = colors.get('background', '#E8F5E8')

            # Semantik/Ableitungen
            canvas = layout.get('canvas', {}) or {}
            aspect_ratio = str(canvas.get('aspect_ratio') or '1:1')
            rel = derive_relative(layout)
            bands = {
                'text': tol(rel.get('text', 41)),
                'image': tol(rel.get('image', 54)),
                'gutter': tol(rel.get('gutter', 5)),
            }
            # Overlay guidance defaults
            common_left_edge_pct = 3.7
            cta_indent_pct = 13.0
            rhythm_pct = 1.9

            # Payload aus texts aufbereiten
            payload = build_overlay_payload(texts or {})

            # SCENE (Embed)
            scene_lines = [
                'SCENE',
                f'- Aspect ratio: {aspect_ratio}',
                f"- Layout intent: text-left {bands['text']}, image-right {bands['image']}, gutter {bands['gutter']}, safe margins 3%",
                '- Composition: rule-of-thirds; clear negative space in the text zones; consistent vertical rhythm; clean split',
            ]
            lt = str(layout.get('layout_type', '')).lower()
            if 'vertical_split' in lt:
                scene_lines.append('- Split-specific: maintain an unobstructed gutter from top to bottom')
            elif 'hero' in lt:
                scene_lines.append('- Hero-specific: pin the top image band to the top edge (band anchoring)')
            scene_lines.extend([
                f'- CI palette: primary {ci_primary}, secondary {ci_secondary}, accent {ci_accent}, background {ci_background}',
                '- Container look: background_opacity 0.84–0.90, corner_radius 16, soft shadow (blur 10–16), subtle gradients or light glass allowed; no hard outlines',
                f'- Overlay guidance: align text containers to a common left edge (~{common_left_edge_pct}%); CTA intentionally indented (~{cta_indent_pct}%); keep rhythm ~{rhythm_pct}%.',
                '- Image coverage: at least 55% width for the main image; full-bleed layouts may require 100%.',
                '- If an optional element is absent, omit it entirely; do not substitute; preserve spacing rhythm and negative space.',
            ])

            # Embed-Text-Zeilen (nur vorhandene)
            scene_lines.extend(build_scene_embed_text(payload))

            # VISUAL / STYLE / TECH (Embed)
            visual_lines = build_visual_embed(motiv_agnostic=motiv_agnostic, strict_layout_mode=strict_layout_mode)
            style_lines = build_style_embed(design or {})
            tech_lines = build_tech_negative_embed()

            final_prompt = "\n".join(scene_lines + ["", *visual_lines, "", *style_lines, "", *tech_lines])
            logger.info(f"Prompt (embed) komponiert: {len(final_prompt)} Zeichen")
            return final_prompt

        # SECTION: Ableitungen fuer SCENE (relative Zonen, CI, Container-Style)
        layout_type = str(layout.get('layout_type', 'unknown'))
        canvas = layout.get('canvas', {}) or {}
        canvas_w = max(1, int(canvas.get('width', 1080) or 1080))
        canvas_h = max(1, int(canvas.get('height', 1080) or 1080))
        aspect_ratio = str(canvas.get('aspect_ratio') or ("1:1" if canvas_w == canvas_h else "16:9"))

        cv = layout.get('calculated_values', {}) or {}
        text_w = _safe_int(cv.get('text_width'))
        image_w = _safe_int(cv.get('image_width'))
        # Falls Engine-Werte fehlen, grob aus Zonen ableiten
        if not text_w or not image_w:
            text_w, image_w = _infer_text_image_widths(layout.get('zones', {}) or {}, canvas_w)

        text_pct = int(round((text_w / canvas_w) * 100)) if text_w else None
        image_pct = int(round((image_w / canvas_w) * 100)) if image_w else None

        # Links/Rechts-Heuristik
        orientation = _infer_orientation(layout.get('zones', {}) or {}, layout_type)

        # CI-Farben aus design.colors (mit Defaults)
        colors = (design or {}).get('colors', {}) or {}
        ci_primary = colors.get('primary') or '#005EA5'
        ci_secondary = colors.get('secondary') or '#B4D9F7'
        ci_accent = colors.get('accent') or '#FFC20E'
        ci_background = colors.get('background') or '#FFFFFF'

        # Container-Style aus einer typischen Text-Zone ableiten
        container_style = _pick_container_style(layout.get('zones', {}) or {})
        bg_opacity = None
        corner_radius = None
        shadow_desc = None
        if isinstance(container_style, dict):
            try:
                bg = container_style.get('background') or {}
                bg_opacity = bg.get('opacity')
                corner_radius = container_style.get('border_radius')
                shadow = container_style.get('shadow') or {}
                # Kompakte Schattierungsbeschreibung
                if isinstance(shadow, dict):
                    blur = shadow.get('blur')
                    op = shadow.get('opacity')
                    shadow_desc = f"shadow blur {blur}, opacity {op}" if blur is not None else None
            except Exception:
                pass

        # SCENE-Block (semantische Kontrolle, NO-TEXT-RENDER, Platzhalter)
        scene_lines = [
            "SCENE",
        ]

        # Aspect ratio
        scene_lines.append(f"- Aspect ratio: {aspect_ratio}")

        # Layout-Intent mit Toleranzen
        rel = derive_relative(layout)
        if orientation == 'text_left_image_right' and rel.get('text') is not None and rel.get('image') is not None:
            scene_lines.append(
                f"- Layout intent: text-left {tol(rel['text'])}, image-right {tol(rel['image'])}, gutter {tol(rel['gutter'])}, safe margins {rel['safe']}%"
            )
        elif orientation == 'image_left_text_right' and rel.get('text') is not None and rel.get('image') is not None:
            scene_lines.append(
                f"- Layout intent: image-left {tol(rel['image'])}, text-right {tol(rel['text'])}, gutter {tol(rel['gutter'])}, safe margins {rel['safe']}%"
            )
        else:
            scene_lines.append(
                f"- Layout intent: split layout {tol(rel['text'])}/{tol(rel['image'])} with gutter {tol(rel['gutter'])}, safe margins {rel['safe']}%"
            )

        # Kompositionsregeln (semantisch, keine Pixel)
        comp_rules = [
            "- Composition: rule-of-thirds; clear negative space in the text column; consistent vertical rhythm; clean separation"
        ]
        if 'vertical_split' in layout_type:
            comp_rules.append("- unobstructed gutter from top to bottom")
        if 'hero' in layout_type:
            comp_rules.append("- pin the top image band to the top edge")
        # Overlay-Semantik (ohne Textinhalte)
        comp_rules.append("- Overlay semantics: shared left edge; CTA indent if present; align to vertical rhythm")
        # Globale Mindestregel fuer Bildanteil (ausser Vollbild-Pfaden)
        comp_rules.append("- Image coverage: maintain at least 55% of the width for the main image; full-bleed layouts may require 100%.")
        scene_lines.extend(comp_rules)

        # CI-Palette und Container-Style
        scene_lines.append(
            f"- CI palette: primary {ci_primary}, secondary {ci_secondary}, accent {ci_accent}, background {ci_background}"
        )

        style_tokens = []
        if bg_opacity is not None:
            style_tokens.append(f"background_opacity {round(float(bg_opacity), 2)}")
        if isinstance(corner_radius, int):
            style_tokens.append(f"corner_radius {corner_radius}")
        if shadow_desc:
            style_tokens.append(shadow_desc)
        if style_tokens:
            scene_lines.append("- Container look: " + ", ".join(style_tokens) + ", optional soft gradients/glass")

        # NO TEXT RENDER + Platzhalter (ohne ASCII/Umlaut-Hinweis)
        scene_lines.append("- NO TEXT IN IMAGE. Use placeholders only: {HEADLINE}, {SUBHEAD}, {CTA}.")
        scene_lines.append("- Conflict rule: if VISUAL conflicts with layout constraints, SCENE overrides.")

        scene_block = "\n".join(scene_lines)

        # VISUAL-Block (motiv-agnostisch)
        visual_lines = ["VISUAL"]
        if strict_layout_mode:
            visual_lines.extend([
                "- Camera/Optics: 35–50 mm, shallow–mid DoF, low distortion, clean micro-contrast, controlled vignetting",
                "- Lighting: soft daylight, broad bounce fill, controlled highlights, 5200–5600 K",
                "- Grading: cinematic neutral, midtone separation, highlight roll-off",
                "- Artefacts: anti-banding/aliasing/moire, no halos/bloom, minimal noise",
            ])
        else:
            visual_lines.extend([
                "- Camera/Optics: 35–50 mm, shallow–mid DoF, low distortion, clean micro-contrast, controlled vignetting",
                "- Lighting: soft daylight, broad bounce fill, controlled highlights, 5200–5600 K",
                "- Grading: cinematic neutral, midtone separation, highlight roll-off",
                "- Artefacts: anti-banding/aliasing/moire, no halos/bloom, minimal noise",
            ])
        visual_block = "\n".join(visual_lines)

        # STYLE-Block (Material, 8k, Kontrast, CI-Harmonie)
        texture_style = (design or {}).get('texture_style') or 'soft gradients'
        container_shape = (design or {}).get('container_shape') or 'rounded modern containers'
        style_lines = [
            "STYLE",
            f"- Materials: glass effect, {texture_style}, {container_shape}",
            "- Rendering: 8k resolution, HDR, nuanced contrast, ultra sharp without edge halos",
            "- Color harmony: aligned to CI; primary for main containers, accent sparingly for CTA, secondary subtle; no neon/oversaturation; natural skintones",
        ]
        style_block = "\n".join(style_lines)

        # TECH & NEGATIVE Block
        tech_lines = [
            "TECH & NEGATIVE",
            "- text_rendering: separate_layers (outside the image)",
            f"- Negative: {NEGATIVE_LINE}",
        ]
        tech_block = "\n".join(tech_lines)

        final_prompt = f"{scene_block}\n\n{visual_block}\n\n{style_block}\n\n{tech_block}"

        logger.info(f"Prompt (hybrid) komponiert: {len(final_prompt)} Zeichen")
        return final_prompt
        
    except Exception as e:
        logger.error(f"Fehler bei Prompt-Komposition: {e}")
        return _get_fallback_prompt()


def _get_fallback_prompt() -> str:
    """Fallback-Prompt im Hybrid-Format (SCENE/VISUAL/STYLE/TECH)"""
    scene = (
        "SCENE\n"
        "- Aspect ratio: 1:1\n"
        "- Layout intent: text-left 44–46%, image-right 49–51%, gutter 5–6%, safe margins 3%\n"
        "- Composition: rule-of-thirds, clear negative space, consistent vertical rhythm, clean separation\n"
        "- CI palette: primary #0F62FE, secondary #161616, accent #FF6F00, background #FFFFFF\n"
        "- Container look: background_opacity 0.9, corner_radius 16, shadow blur 10, optional soft gradients/glass\n"
        "- NO TEXT IN IMAGE. Use placeholders only: {HEADLINE}, {SUBHEAD}, {CTA}.\n"
        "- Conflict rule: if VISUAL conflicts with layout constraints, SCENE overrides."
    )
    visual = (
        "VISUAL\n"
        "- Camera/Optics: 35–50mm, shallow–mid DoF, low distortion, clean micro-contrast, controlled vignetting\n"
        "- Lighting: soft daylight, broad bounce fill, controlled highlights, 5200–5600 K\n"
        "- Grading: cinematic neutral, midtone separation, highlight roll-off\n"
        "- Artefacts: anti-banding/aliasing/moire, no halos/bloom, minimal noise"
    )
    style = (
        "STYLE\n"
        "- Materials: glass effect, soft gradients, rounded modern containers\n"
        "- Rendering: 8k resolution, HDR, nuanced contrast, ultra sharp without edge halos\n"
        "- Color harmony: aligned to CI; primary for main containers, accent sparingly for CTA, secondary subtle; no neon/oversaturation; natural skintones"
    )
    negatives = (
        "no text, no words, no letters, no typography, no logo, no watermark, no signature, no frames, no borders, no captions, "
        "blurry, lowres, pixelated, noisy, distorted, deformed, duplicate, cropped, cut off, cartoon, anime, illustration, painting, sketch, 3d render, cgi, plastic, toy, "
        "oversaturated colors, neon, abstract, disfigured, mutated, bad anatomy, broken hands, extra limbs, creepy, uncanny, dark, gloomy, depressing, violence, blood, injury, horror, messy background, cluttered, "
        "no text-like patterns, no signage, no UI overlays, no charts/graphs"
    )
    tech = (
        "TECH & NEGATIVE\n"
        "- text_rendering: separate_layers (outside the image)\n"
        f"- Negative: {negatives}"
    )
    return f"{scene}\n\n{visual}\n\n{style}\n\n{tech}"


def _safe_int(value: Any) -> int:
    try:
        if value is None:
            return 0
        return int(value)
    except Exception:
        return 0


def derive_relative(layout: Dict[str, Any]) -> Dict[str, int]:
    cv = layout.get('calculated_values', {}) or {}
    canvas = layout.get('canvas', {}) or {}
    canvas_w = _safe_int(canvas.get('width') or 1080)
    text_w = _safe_int(cv.get('text_width'))
    image_w = _safe_int(cv.get('image_width'))
    gutter_w = max(0, canvas_w - (text_w + image_w))
    def pct(x: int) -> int:
        try:
            return int(round(100 * float(x) / float(canvas_w)))
        except Exception:
            return 0
    return {
        'text': pct(text_w),
        'image': pct(image_w),
        'gutter': pct(gutter_w),
        'safe': 3,
    }


def tol(p: int, d: int = 1) -> str:
    return f"{max(0, p - d)}–{min(100, p + d)}%"


def _infer_text_image_widths(zones: Dict[str, Any], canvas_w: int) -> Tuple[int, int]:
    """Grobe Heuristik: Text-Breite = max Breite einer Textzone; Bild-Breite = restliche Spalte."""
    text_w = 0
    image_w = 0
    for name, z in (zones or {}).items():
        if not isinstance(z, dict):
            continue
        if z.get('content_type') == 'text_elements':
            w = _safe_int(z.get('width'))
            text_w = max(text_w, w)
        if z.get('content_type') in {'image_motiv'} or name in {'motiv_area'}:
            image_w = max(image_w, _safe_int(z.get('width')))
    if not image_w and canvas_w and text_w:
        image_w = max(0, canvas_w - text_w)
    return text_w, image_w


def _infer_orientation(zones: Dict[str, Any], layout_type: str) -> str:
    """Bestimmt grob die Ausrichtung (Text links/rechts) aus Layout-Typ und Zone-Positionen."""
    lt = (layout_type or '').lower()
    if 'vertical_split_left' in lt:
        return 'image_left_text_right'
    if 'vertical_split' in lt:
        return 'text_left_image_right'
    # Heuristik anhand x-Positionen
    text_min_x = None
    image_min_x = None
    for name, z in (zones or {}).items():
        if not isinstance(z, dict):
            continue
        if z.get('content_type') == 'text_elements':
            x = _safe_int(z.get('x'))
            text_min_x = x if text_min_x is None else min(text_min_x, x)
        if z.get('content_type') in {'image_motiv'} or name in {'motiv_area'}:
            x = _safe_int(z.get('x'))
            image_min_x = x if image_min_x is None else min(image_min_x, x)
    if text_min_x is not None and image_min_x is not None:
        return 'text_left_image_right' if text_min_x < image_min_x else 'image_left_text_right'
    return 'unknown'


def _pick_container_style(zones: Dict[str, Any]) -> Dict[str, Any]:
    """Waehlt eine typische Text-Zone und gibt deren container_style zurueck."""
    preferred_order = [
        'headline_block', 'headline_1_block', 'headline_2_block',
        'subline_block', 'benefits_block', 'cta_block', 'company_block', 'standort_block'
    ]
    for name in preferred_order:
        z = (zones or {}).get(name)
        if isinstance(z, dict) and isinstance(z.get('container_style'), dict):
            return z['container_style']
    # Fallback: erste Textzone
    for _, z in (zones or {}).items():
        if isinstance(z, dict) and z.get('content_type') == 'text_elements' and isinstance(z.get('container_style'), dict):
            return z['container_style']
    return {}


# ===== EMBED MODE HELPERS =====
def _sanitize_text(s: str, limit: int) -> str:
    try:
        s = re.sub(r"\s+", " ", (s or "")).strip()
    except Exception:
        s = str(s or "").strip()
    return s[:limit]


def build_overlay_payload(user_inputs: Dict[str, Any]) -> Dict[str, Any]:
    benefits_list = user_inputs.get("benefits") or []
    if not isinstance(benefits_list, list):
        benefits_list = []
    return {
        "headline": _sanitize_text(user_inputs.get("headline", ""), 30),
        "subhead": _sanitize_text(user_inputs.get("subline", ""), 50),
        "cta": _sanitize_text(user_inputs.get("cta", ""), 25),
        "benefits": [_sanitize_text(b, 48) for b in benefits_list][:4],
        "stellentitel": _sanitize_text(user_inputs.get("stellentitel", ""), 38),
        "standort": _sanitize_text(user_inputs.get("location", ""), 30),
    }


NEGATIVE_LINE_EMBED = (
    "no extra text, no random signage, no logos, no watermarks, no captions, "
    "no frames, no borders, blurry, lowres, pixelated, noisy, distorted, deformed, "
    "duplicate, cropped, cut off, cartoon, anime, illustration-only, painting-only, "
    "sketchy, 3d render toy look, plastic feel, oversaturated colors, neon, abstract clutter, "
    "disfigured, uncanny, dark, gloomy mood, violence, blood, injury, messy background, "
    "UI overlays, charts/graphs"
)


def _present(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return len(value) > 0
    return bool(value)


def build_scene_embed_text(payload: Dict[str, Any]) -> Any:
    lines = [
        "- Overlay semantics (typeset these exact strings into the image, in German):",
    ]
    if _present(payload.get("standort")):
        lines.append(f'  • LOCATION: "{payload["standort"]}" — top-left; single line; high contrast')
    lines.append(f'  • HEADLINE: "{payload["headline"]}" — top-left within the text column (upper third); bold; short line length')
    if _present(payload.get("subhead")):
        lines.append(f'  • SUBHEAD: "{payload["subhead"]}" — directly below; same left edge; keep spacing rhythm')
    if _present(payload.get("benefits")):
        lines.append(f'  • BENEFITS (bulleted, up to 4): {payload["benefits"]} — mid-left; concise items; same left edge')
    if _present(payload.get("stellentitel")):
        lines.append(f'  • JOB TITLE: "{payload["stellentitel"]}" — below benefits; supportive emphasis; same left edge')
    lines.append(f'  • CTA: "{payload["cta"]}" — lower third; intentionally indented; strong legibility; clear separation')
    lines.append("- If an optional element is absent, omit it entirely; preserve spacing rhythm and negative space.")
    lines.append("- Conflict rule: if VISUAL conflicts with layout constraints, SCENE overrides.")
    return lines


def build_visual_embed(motiv_agnostic: bool = True, strict_layout_mode: bool = False) -> Any:
    if strict_layout_mode:
        return [
            "VISUAL",
            "- Technical rendering settings only; prioritize layout constraints from SCENE",
        ]
    return [
        "VISUAL",
        "- Camera/Optics: 35–50 mm, shallow–mid DoF, low distortion, clean micro-contrast, controlled vignetting",
        "- Lighting: soft daylight + broad bounce, neutral white balance 5200–5600 K, controlled highlights",
        "- Grading: cinematic neutral, defined midtone separation, gentle highlight roll-off, no color cast",
        "- Artefacts: anti-banding/aliasing/moire, no halos/bloom, minimal noise",
    ]


def build_style_embed(design: Dict[str, Any]) -> Any:
    return [
        "STYLE",
        "- Materials: modern rounded containers; subtle gradients/glass; soft shadows",
        "- Rendering: 8k target, HDR tonality, nuanced contrast, ultra sharp without edge halos",
        "- Color harmony: align to CI; primary for key containers, accent sparingly for CTA, secondary subtle; avoid neon/oversaturation; keep background under text low-frequency",
    ]


def build_tech_negative_embed() -> Any:
    return [
        "TECH & NEGATIVE",
        "- Render exactly and only these text strings from SCENE. Do not invent extra text, numbers, logos or signage.",
        f"- Negative: {NEGATIVE_LINE_EMBED}",
    ]
