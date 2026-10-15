"""Build a standalone, navigable slide viewer from a deck folder's project/deck.json + project/slides/*.html.

Usage (from the repo root):
    python3 viewer/build.py <deck-folder>
        writes <deck-folder>/presentation.html (open directly in a browser)
    python3 viewer/build.py <deck-folder> --fragment OUT
        writes a body-only page (no doctype/head) to OUT, for publishing as an artifact
"""
import html
import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent / "template.html"


def render(deck_dir: Path) -> str:
    project = deck_dir / "project"
    deck = json.loads((project / "deck.json").read_text(encoding="utf-8"))
    slides = [(project / "slides" / f"{sid}.html").read_text(encoding="utf-8").strip() for sid in deck["order"]]
    fonts = "\n".join(
        f'<link rel="stylesheet" href="{html.escape(face["href"])}">'
        for face in deck.get("faces", {}).values()
        if face.get("href", "").startswith("https://fonts.googleapis.com/css2?")
    )
    page = TEMPLATE.read_text(encoding="utf-8")
    return (
        page.replace("{{TITLE}}", html.escape(deck["title"]))
        .replace("{{FONTS}}", fonts)
        .replace("{{SLIDES}}", "\n".join(slides))
    )


def main() -> None:
    args = sys.argv[1:]
    if len(args) not in (1, 3) or (len(args) == 3 and args[1] != "--fragment"):
        sys.exit(__doc__)
    deck_dir = Path(args[0]).resolve()
    body = render(deck_dir)
    if len(args) == 3:
        Path(args[2]).write_text(body, encoding="utf-8")
        return
    doc = (
        '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        "</head>\n<body>\n" + body + "\n</body>\n</html>\n"
    )
    (deck_dir / "presentation.html").write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
