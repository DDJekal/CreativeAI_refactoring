def generate_semantic_layout_description(layout_data):
    """
    Generiert proportionale, semantische Layout-Beschreibungen ohne Pixelangaben.

    Args:
        layout_data: Layout-Daten mit zones und Canvas

    Returns:
        dict: Semantische Beschreibungen für KI-Generatoren (sprachlich, relativ)
    """
    zones = layout_data.get('zones', {})
    canvas = layout_data.get('canvas', {})
    canvas_width = max(1, canvas.get('width', 1080))
    canvas_height = max(1, canvas.get('height', 1080))

    layout_type = (layout_data.get('layout_type') or 'unknown').lower()

    semantic_description = {
        'layout_overview': '',
        'text_areas': [],
        'image_areas': [],
        'positioning_logic': []
    }

    # Helper zur relativen Einordnung
    def _pct(val, total):
        try:
            return max(0, min(100, round(100.0 * float(val) / float(total))))
        except Exception:
            return 0

    def _column_side(x):
        # Grobe Heuristik: < 45% = links, > 55% = rechts, sonst zentriert
        px = _pct(x, canvas_width)
        if px <= 45:
            return 'left'
        if px >= 55:
            return 'right'
        return 'center'

    text_zones = {n: z for n, z in zones.items() if isinstance(z, dict) and z.get('content_type') == 'text_elements'}
    image_zones = {n: z for n, z in zones.items() if isinstance(z, dict) and (z.get('content_type') == 'image_motiv' or n == 'motiv_area')}

    # Relative Spaltenproportionen abschaetzen
    text_max_w = 0
    image_max_w = 0
    for z in text_zones.values():
        text_max_w = max(text_max_w, int(z.get('width', 0)))
    for z in image_zones.values():
        image_max_w = max(image_max_w, int(z.get('width', 0)))
    text_pct = _pct(text_max_w, canvas_width)
    image_pct = _pct(image_max_w, canvas_width)

    if 'vertical_split_left' in layout_type:
        semantic_description['layout_overview'] = (
            f"VERTICAL SPLIT LEFT: image-left ~{image_pct}% width, text-right ~{text_pct}% width; clear gutter"
        )
    elif 'vertical_split' in layout_type:
        semantic_description['layout_overview'] = (
            f"VERTICAL SPLIT: text-left ~{text_pct}% width, image-right ~{image_pct}% width; clear gutter"
        )
    elif 'centered' in layout_type:
        semantic_description['layout_overview'] = (
            "CENTERED: text containers grouped centrally over full-background image; generous negative space"
        )
    else:
        semantic_description['layout_overview'] = (
            f"{layout_type.upper().replace('_', ' ')}: semantic arrangement with proportional columns/areas"
        )

    # Textbereiche beschreiben (ohne Pixel)
    for zone_name, z in text_zones.items():
        side = _column_side(int(z.get('x', 0)))
        w_pct = _pct(int(z.get('width', 0)), canvas_width)
        h_pct = _pct(int(z.get('height', 0)), canvas_height)
        y_pct = _pct(int(z.get('y', 0)), canvas_height)

        description = f"{zone_name.replace('_', ' ').title()} in {side} column"
        rel_pos = f"{side} column, approx {y_pct}% from top"
        size = f"approx {w_pct}% width, {h_pct}% height"

        semantic_description['text_areas'].append({
            'zone_name': zone_name,
            'description': description,
            'relative_position': rel_pos,
            'size': size
        })

    # Bildbereiche beschreiben (ohne Pixel)
    for zone_name, z in image_zones.items():
        side = _column_side(int(z.get('x', 0)))
        w_pct = _pct(int(z.get('width', 0)), canvas_width)
        h_pct = _pct(int(z.get('height', 0)), canvas_height)
        y_pct = _pct(int(z.get('y', 0)), canvas_height)

        description = (
            f"Full-height image area on {side} side if split; no frames; fills its reserved area; text overlays kept separate"
        )
        rel_pos = f"{side} side, approx {y_pct}% from top"
        size = f"approx {w_pct}% canvas width, {h_pct}% canvas height"

        semantic_description['image_areas'].append({
            'zone_name': zone_name,
            'description': description,
            'relative_position': rel_pos,
            'size': size
        })

    # Positionierungslogik (sprachlich)
    semantic_description['positioning_logic'] = [
        'Use rule-of-thirds and balanced negative space for visual hierarchy',
        'Keep text containers aligned to a clear column; preserve consistent gutter',
        'Do not render actual text inside the image; reserve clean overlay regions only'
    ]

    return semantic_description


