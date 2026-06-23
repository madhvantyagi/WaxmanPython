from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

import pdfplumber


ROOT = Path(__file__).resolve().parent
DEFAULT_PDF_DIR = ROOT / "Classes PDF"
DEFAULT_OUTPUT_DIR = ROOT / "extracted_pdf_text"


@dataclass
class PdfExtractionSummary:
    source_pdf: str
    output_dir: str
    combined_text_file: str
    page_count: int
    character_count: int
    word_count: int
    pages_with_no_text: list[int]


def slugify(name: str) -> str:
    value = name.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "pdf"


def clean_page_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf(pdf_path: Path, output_root: Path) -> PdfExtractionSummary:
    slug = slugify(pdf_path.stem)
    pdf_output_dir = output_root / slug
    pages_dir = pdf_output_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    combined_parts: list[str] = []
    pages_with_no_text: list[int] = []

    with pdfplumber.open(pdf_path) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            raw_text = page.extract_text(x_tolerance=1, y_tolerance=3) or ""
            page_text = clean_page_text(raw_text)
            if not page_text:
                pages_with_no_text.append(index)

            page_header = f"\n\n--- PAGE {index} ---\n\n"
            combined_parts.append(page_header + page_text)
            (pages_dir / f"page-{index:03d}.txt").write_text(
                page_text + "\n",
                encoding="utf-8",
            )

        page_count = len(pdf.pages)

    combined_text = "".join(combined_parts).strip() + "\n"
    combined_file = pdf_output_dir / "combined.txt"
    combined_file.write_text(combined_text, encoding="utf-8")

    summary = PdfExtractionSummary(
        source_pdf=str(pdf_path.relative_to(ROOT)),
        output_dir=str(pdf_output_dir.relative_to(ROOT)),
        combined_text_file=str(combined_file.relative_to(ROOT)),
        page_count=page_count,
        character_count=len(combined_text),
        word_count=len(re.findall(r"\b\w+\b", combined_text)),
        pages_with_no_text=pages_with_no_text,
    )

    (pdf_output_dir / "metadata.json").write_text(
        json.dumps(asdict(summary), indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract text from each class PDF into one folder per PDF."
    )
    parser.add_argument(
        "--pdf-dir",
        type=Path,
        default=DEFAULT_PDF_DIR,
        help="Folder containing source PDFs.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Folder to write extracted text and metadata.",
    )
    args = parser.parse_args()

    pdf_dir = args.pdf_dir.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(pdf_dir.glob("*.pdf"))
    if not pdfs:
        raise SystemExit(f"No PDFs found in {pdf_dir}")

    summaries = [extract_pdf(pdf_path, output_dir) for pdf_path in pdfs]
    index_file = output_dir / "index.json"
    index_file.write_text(
        json.dumps([asdict(summary) for summary in summaries], indent=2) + "\n",
        encoding="utf-8",
    )

    for summary in summaries:
        print(
            f"{summary.source_pdf}: {summary.page_count} pages, "
            f"{summary.word_count} words -> {summary.combined_text_file}"
        )
        if summary.pages_with_no_text:
            print(f"  pages with no extracted text: {summary.pages_with_no_text}")
    print(f"\nWrote extraction index: {index_file.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
