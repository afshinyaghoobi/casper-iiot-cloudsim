#!/usr/bin/env python3
"""Reproducible, non-submitting Word export for the SIMPAT v2.9 author-review package.

Inputs remain the original Markdown sources in this repository. Requires
pandoc, python-docx and cairosvg. Does not change experimental inputs/outputs.
This is an AUTHOR-REVIEW export, not journal submission or DOI deposit.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

import cairosvg
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

FILES = {
    "SIMPAT_Manuscript_v29_AUTHOR_REVIEW.docx":
        "SIMPAT_MANUSCRIPT_V29_CLEAN_PROFESSOR_REVIEW_2026-11-19.md",
    "SIMPAT_Supplementary_AUTHOR_REVIEW.docx":
        "SIMPAT_V24_SUPPLEMENTARY_EXTENDED_RESULTS_2026-11-18.md",
    "SIMPAT_Highlights_AUTHOR_REVIEW.docx":
        "SIMPAT_V25_SUBMISSION_HIGHLIGHTS_2026-11-18.md",
    "SIMPAT_Cover_Letter_AUTHOR_REVIEW.docx":
        "SIMPAT_V29_CLEAN_COVER_LETTER_FOR_PROFESSOR_2026-11-19.md",
}
FIGURE = "figure_a2_24_case_native_vs_fifo_2026-11-18.svg"
TITLE = "Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation"


def reference_doc(path: Path) -> None:
    d = Document()
    sec = d.sections[0]
    sec.page_width = Inches(8.5)
    sec.page_height = Inches(11)
    sec.top_margin = Inches(.84)
    sec.bottom_margin = Inches(.76)
    sec.left_margin = Inches(.80)
    sec.right_margin = Inches(.80)
    styles = d.styles
    n = styles["Normal"]
    n.font.name = "Times New Roman"
    n.font.size = Pt(10)
    n.paragraph_format.space_after = Pt(5)
    for name, size in [("Title", 15), ("Heading 1", 12), ("Heading 2", 11),
                       ("Heading 3", 10)]:
        st = styles[name]
        st.font.name = "Times New Roman"
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = RGBColor(0, 0, 0)
        st.paragraph_format.space_before = Pt(9)
        st.paragraph_format.space_after = Pt(4)
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("AUTHOR-REVIEW DRAFT — verify metadata and declarations before submission")
    for run in footer.runs:
        run.font.size = Pt(7)
        run.font.color.rgb = RGBColor(95, 95, 95)
    d.save(path)


def format_docx(path: Path, *, main: bool = False) -> dict:
    d = Document(path)
    all_text = "\n".join(p.text for p in d.paragraphs)
    if not all_text.strip():
        raise RuntimeError(f"Empty Word export: {path}")
    if main:
        if TITLE not in all_text:
            raise RuntimeError("Locked title missing from Word")
        for name in ["Afshin Yaghoobi", "Mahsa Nazemi Harandi", "0009-0006-4695-6018", "0009-0000-5395-5394", "axyaghoobi@shockers.wichita.edu", "This research did not receive any specific grant", "The authors declare that they have no known competing financial", "available from the corresponding author upon reasonable request", "Writing – review and editing"]:
            if name not in all_text:
                raise RuntimeError(f"Missing supplied author/ORCID field: {name}")
        for term in ["86/288", "107/288", "250/288", "SIMPAT", "FAILED"]:
            text_all = all_text + "\n" + "\n".join(
                cell.text for table in d.tables for row in table.rows for cell in row.cells
            )
            if term not in text_all:
                raise RuntimeError(f"Key claim absent from Word: {term}")
        if not d.inline_shapes:
            raise RuntimeError("No embedded primary A2 figure in Word")
        if len(d.tables) < 2:
            raise RuntimeError("Expected the RQ matrix and 24-case data table")
    for table in d.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.font.size = Pt(8)
    d.save(path)
    return {"name": path.name, "bytes": path.stat().st_size,
            "paragraphs": len(d.paragraphs), "tables": len(d.tables),
            "embedded_figures": len(d.inline_shapes)}


def validate_primary_table(markdown: str) -> None:
    """Recompute Table 1 column totals from the submitted main-text source."""
    lines = markdown.splitlines()
    rows = []
    for line in lines:
        if line.startswith("| BURSTY_") or line.startswith("| STAGGERED_"):
            columns = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(columns) != 4:
                raise RuntimeError(f"Unexpected Table 1 column count: {line}")
            rows.append((columns[0], float(columns[1]), int(columns[2]), int(columns[3])))
    if len(rows) != 24 or len({row[0] for row in rows}) != 24:
        raise RuntimeError(f"Primary A2 table must have 24 unique cases, saw {len(rows)}")
    d25, d50 = sum(r[2] for r in rows), sum(r[3] for r in rows)
    maxgap = max(r[1] for r in rows)
    if (d25, d50, maxgap) != (86, 107, 246):
        raise RuntimeError(f"Primary Table 1 mismatch: {d25}, {d50}, {maxgap}")
    refs = re.findall(r"^\\[(\\d+)\\] ", markdown, flags=re.MULTILINE)
    if refs != [str(i) for i in range(1, 13)]:
        raise RuntimeError("The original 12-item reference sequence has changed")
    if "### Data availability" not in markdown or "### CRediT author statement" not in markdown:
        raise RuntimeError("Required author-provided declarations are absent")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jpdc", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--outdir", type=Path, required=True)
    args = ap.parse_args()
    root = args.jpdc.resolve()
    out = args.outdir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    for name in FILES.values():
        if not (root / name).is_file():
            raise RuntimeError(f"Missing source document: {name}")
    if not (root / FIGURE).is_file():
        raise RuntimeError(f"Missing original Figure 1: {FIGURE}")
    with tempfile.TemporaryDirectory(prefix="simpat-docx-") as tmp:
        t = Path(tmp)
        reference_doc(t / "reference.docx")
        cairosvg.svg2png(url=str(root / FIGURE), write_to=str(t / "figure_a2.png"),
                         output_width=1900)
        shutil.copy2(root / FIGURE, out / FIGURE)
        shutil.copy2(t / "figure_a2.png", out / "Figure_1_A2_full_factorial.png")
        reports = []
        for target, original in FILES.items():
            body = (root / original).read_text(encoding="utf-8")
            if original.startswith("SIMPAT_MANUSCRIPT"):
                validate_primary_table(body)
            if original.startswith("SIMPAT_MANUSCRIPT"):
                if body.splitlines()[0] != "# " + TITLE:
                    raise RuntimeError("Locked title has been changed")
                # Work around Pandoc/Word SVG compatibility without changing Git source.
                body = body.replace(f"({FIGURE})", "(figure_a2.png)")
            temporary_md = t / (Path(original).stem + ".md")
            temporary_md.write_text(body, encoding="utf-8")
            cmd = ["pandoc", "--from", "markdown+pipe_tables+tex_math_dollars",
                   "--to", "docx", "--standalone",
                   "--reference-doc", str(t / "reference.docx"),
                   "--resource-path", f"{t}:{root}", str(temporary_md),
                   "-o", str(out / target)]
            subprocess.run(cmd, check=True)
            reports.append(format_docx(out / target,
                                      main=original.startswith("SIMPAT_MANUSCRIPT")))
        summary = "\n".join(str(x) for x in reports) + "\n"
        (out / "EXPORT_QA.txt").write_text(
            "SIMPAT v2.9 Word package; not submitted or author approved.\n" + summary,
            encoding="utf-8")
        print(summary)


if __name__ == "__main__":
    main()
