"""Build a standalone, navigable slide viewer from project/deck.json + project/slides/*.html.

Usage:
    python3 viewer/build.py              # writes presentation.html (open directly in a browser)
    python3 viewer/build.py --fragment OUT
                                         # writes a body-only page (no doctype/head), for publishing as an artifact
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECT = ROOT / "project"
TEMPLATE = Path(__file__).resolve().parent / "template.html"


def render() -> str:
    deck = json.loads((PROJECT / "deck.json").read_text(encoding="utf-8"))
    slides = [(PROJECT / "slides" / f"{sid}.html").read_text(encoding="utf-8").strip() for sid in deck["order"]]
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
    body = render()
    if len(sys.argv) == 3 and sys.argv[1] == "--fragment":
        Path(sys.argv[2]).write_text(body, encoding="utf-8")
        return
    doc = (
        '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        "</head>\n<body>\n" + body + "\n</body>\n</html>\n"
    )
    (ROOT / "presentation.html").write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
