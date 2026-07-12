from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Preformatted, SimpleDocTemplate, Spacer


def markdown_to_pdf(md_path: Path, pdf_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="H1Doc",
            parent=styles["Heading1"],
            fontSize=18,
            leading=22,
            spaceAfter=10,
            textColor=colors.HexColor("#1f3b4d"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2Doc",
            parent=styles["Heading2"],
            fontSize=13,
            leading=17,
            spaceAfter=8,
            textColor=colors.HexColor("#2f5d73"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyDoc",
            parent=styles["BodyText"],
            fontSize=10.5,
            leading=14,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ListDoc",
            parent=styles["BodyText"],
            leftIndent=12,
            bulletIndent=0,
            fontSize=10.5,
            leading=14,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CodeDoc",
            parent=styles["Code"],
            fontName="Courier",
            fontSize=9,
            leading=12,
            backColor=colors.HexColor("#f5f7fa"),
            borderPadding=6,
        )
    )

    story = []
    in_code = False
    code_lines = []

    for raw in lines:
        line = raw.rstrip("\n")

        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                code_lines = []
            else:
                in_code = False
                story.append(Preformatted("\n".join(code_lines), styles["CodeDoc"]))
                story.append(Spacer(1, 0.2 * cm))
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not line.strip():
            story.append(Spacer(1, 0.15 * cm))
            continue

        if line.startswith("# "):
            story.append(Paragraph(line[2:].strip(), styles["H1Doc"]))
            continue

        if line.startswith("## "):
            story.append(Paragraph(line[3:].strip(), styles["H2Doc"]))
            continue

        if line.startswith("### "):
            story.append(Paragraph(line[4:].strip(), styles["BodyDoc"]))
            continue

        if line.lstrip().startswith("- "):
            txt = (
                line.lstrip()[2:]
                .strip()
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            story.append(Paragraph(f"• {txt}", styles["ListDoc"]))
            continue

        safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        story.append(Paragraph(safe, styles["BodyDoc"]))

    if in_code and code_lines:
        story.append(Preformatted("\n".join(code_lines), styles["CodeDoc"]))

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="Documentacion ScrapInfo",
    )
    doc.build(story)


def main() -> None:
    docs_dir = Path(__file__).resolve().parent
    md_path = docs_dir / "Documentacion_ScrapInfo.md"
    pdf_path = docs_dir / "Documentacion_ScrapInfo.pdf"

    if not md_path.exists():
        raise FileNotFoundError(f"No existe el archivo: {md_path}")

    markdown_to_pdf(md_path, pdf_path)
    print(f"PDF generado en: {pdf_path}")


if __name__ == "__main__":
    main()
