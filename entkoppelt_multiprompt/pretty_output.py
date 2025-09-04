from typing import Any, Dict, List


SECTION_TITLES: List[str] = [
    "Szene & Atmosphaere",
    "Komposition & Layout",
    "Form & Design",
    "Farbwelt & CI",
    "Text & Content (separate_layers)",
    "Balance & Wirkung",
    "Technische Regeln & Engine-Optimierung",
]


def _as_markdown_headings(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.strip() in SECTION_TITLES:
            lines.append(f"### {line.strip()}")
        else:
            lines.append(line)
    return "\n".join(lines)


def generate_human_readable_output(result: Dict[str, Any], as_markdown: bool = True) -> str:
    meta = result.get("meta") or {}
    errors = meta.get("errors") or []
    prompt = result.get("dalle_prompt") or ""

    if errors:
        # Bei Policyfehlern Prompt nicht vorhanden – liefere kurze Diagnose
        return (
            "Es liegen Policy-Fehler vor; kein Prompt ausgegeben.\n\n"
            f"Fehler: {', '.join(errors)}\n"
        )

    length = len(prompt)
    body = _as_markdown_headings(prompt) if as_markdown else prompt

    header = (
        "Hier ist dein fertiger DALL·E-3-Prompt im gewünschten Ziel-Format, "
        "alle Vorgaben und USER-Texte strikt eingehalten, Länge: ca. "
        f"{length} Zeichen.\n\n---\n\n"
    )
    footer = (
        "\n\n---\n\n"
        "Möchtest du, dass ich dir daraus direkt eine kompakte JSON- oder YAML-Struktur "
        "ableite, die du sofort in dein System einspielen kannst?"
    )
    return f"{header}{body}{footer}"


