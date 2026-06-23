from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SECTION_DIR = ROOT / "StudyGuides" / "final_review_sections"
OUTPUT = ROOT / "StudyGuides" / "python-final-last-hour-review.html"

SECTION_ORDER = [
    ("00_priority_last_hour.md", "Priority Map"),
    ("01_core_runtime_lists.md", "Runtime and Lists"),
    ("02_functions_scope_modules.md", "Functions, Scope, Modules"),
    ("03_dicts_sets_comprehensions.md", "Dicts, Sets, Comprehensions"),
    ("04_iterators_generators.md", "Iterators and Generators"),
    ("05_decorators_oop.md", "Decorators and OOP"),
    ("06_strings_files_csv_matrices.md", "Strings, Files, CSV, Matrices"),
]


def inline_format(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def md_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    in_code = False
    code_lines: list[str] = []
    in_list = False
    in_table = False
    table_rows: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            out.append(f"<p>{inline_format(' '.join(paragraph))}</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    def flush_table() -> None:
        nonlocal in_table, table_rows
        if not in_table:
            return
        out.append("<div class=\"table-wrap\"><table>")
        for idx, row in enumerate(table_rows):
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            if idx == 1 and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                continue
            tag = "th" if idx == 0 else "td"
            out.append("<tr>" + "".join(f"<{tag}>{inline_format(cell)}</{tag}>" for cell in cells) + "</tr>")
        out.append("</table></div>")
        table_rows = []
        in_table = False

    for line in lines:
        stripped = line.rstrip()

        if stripped.startswith("```"):
            flush_paragraph()
            close_list()
            flush_table()
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(stripped)
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            close_list()
            in_table = True
            table_rows.append(stripped)
            continue
        elif in_table:
            flush_table()

        if not stripped:
            flush_paragraph()
            close_list()
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            close_list()
            level = min(len(heading.group(1)) + 1, 4)
            out.append(f"<h{level}>{inline_format(heading.group(2))}</h{level}>")
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline_format(stripped[2:].strip())}</li>")
            continue

        numbered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if numbered:
            flush_paragraph()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline_format(numbered.group(1).strip())}</li>")
            continue

        paragraph.append(stripped)

    if in_code:
        out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
    flush_table()
    close_list()
    flush_paragraph()
    return "\n".join(out)


def section_id(filename: str) -> str:
    return Path(filename).stem.replace("_", "-")


def build() -> str:
    nav = []
    sections = []
    for filename, title in SECTION_ORDER:
        path = SECTION_DIR / filename
        markdown = path.read_text(encoding="utf-8")
        sid = section_id(filename)
        nav.append(f"<a href=\"#{sid}\">{html.escape(title)}</a>")
        sections.append(
            f"<section id=\"{sid}\" class=\"topic\"><h2>{html.escape(title)}</h2>"
            f"<p class=\"source-note\"><code>{html.escape(filename)}</code></p>"
            f"{md_to_html(markdown)}</section>"
        )

    nav_html = "\n".join(nav)
    sections_html = "\n".join(sections)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Python Final Last-Hour Review</title>
  <style>
    :root {{
      --ink: #162027;
      --muted: #5b6670;
      --line: #d9e1e7;
      --panel: #f6f8fa;
      --accent: #0f766e;
      --accent-soft: #e8f4f2;
      --code-bg: #101820;
      --code-fg: #edf4f7;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
      color: var(--ink);
      background: #fff;
      line-height: 1.45;
      font-size: 15px;
    }}
    header {{
      background: var(--accent-soft);
      border-bottom: 1px solid var(--line);
    }}
    .wrap {{
      width: min(1180px, calc(100% - 28px));
      margin: 0 auto;
    }}
    header .wrap {{ padding: 24px 0 18px; }}
    h1 {{
      margin: 0 0 8px;
      font-size: clamp(1.85rem, 3.5vw, 3rem);
      line-height: 1.05;
      letter-spacing: 0;
    }}
    .subtitle {{
      margin: 0;
      max-width: 920px;
      color: var(--muted);
      font-size: 1rem;
    }}
    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 12px;
    }}
    .pill {{
      border: 1px solid var(--line);
      background: #fff;
      border-radius: 999px;
      padding: 4px 9px;
      font-size: 0.84rem;
      font-weight: 800;
      color: #31414d;
    }}
    main {{ padding: 18px 0 48px; }}
    .nav {{
      position: sticky;
      top: 0;
      z-index: 2;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 8px;
      padding: 10px 0;
      background: rgba(255,255,255,0.96);
      border-bottom: 1px solid var(--line);
      margin-bottom: 14px;
    }}
    .nav a {{
      border: 1px solid var(--line);
      border-radius: 7px;
      padding: 8px 9px;
      color: #115e59;
      text-decoration: none;
      font-weight: 800;
      background: #fff;
      font-size: 0.9rem;
    }}
    .topic {{
      border-top: 2px solid var(--line);
      padding-top: 12px;
      margin-top: 20px;
    }}
    h2 {{ margin: 0 0 6px; font-size: 1.5rem; }}
    h3 {{ margin: 18px 0 7px; font-size: 1.12rem; color: #17333a; }}
    h4 {{ margin: 14px 0 6px; font-size: 1rem; }}
    .source-note {{ margin: 0 0 10px; color: var(--muted); font-size: 0.86rem; }}
    p {{ margin: 7px 0; }}
    ul {{ margin: 7px 0 10px; padding-left: 22px; }}
    li + li {{ margin-top: 3px; }}
    code {{
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 0.9em;
      background: #eef2f4;
      padding: 1px 4px;
      border-radius: 4px;
    }}
    pre {{
      margin: 8px 0 12px;
      padding: 10px 12px;
      overflow-x: auto;
      border-radius: 7px;
      background: var(--code-bg);
      color: var(--code-fg);
      line-height: 1.38;
    }}
    pre code {{
      background: transparent;
      padding: 0;
      color: inherit;
      font-size: 0.88rem;
    }}
    .table-wrap {{ overflow-x: auto; margin: 8px 0 12px; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.91rem;
    }}
    th, td {{
      border: 1px solid var(--line);
      padding: 7px 8px;
      text-align: left;
      vertical-align: top;
    }}
    th {{ background: var(--panel); }}
    @media print {{
      .nav {{ position: static; }}
      body {{ font-size: 12px; }}
      pre, table {{ break-inside: avoid; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <h1>Python Final Last-Hour Review</h1>
      <p class="subtitle">A compact memory sheet for the last pass before the exam: methods, mutation rules, references, comprehensions, iterators, generators, decorators, files, CSV, matrices, and the common traps that change outputs.</p>
      <div class="meta">
        <span class="pill">last-hour sheet</span>
        <span class="pill">7 compact sections</span>
        <span class="pill">not a question bank</span>
      </div>
    </div>
  </header>
  <main class="wrap">
    <nav class="nav" aria-label="Review sections">
      {nav_html}
    </nav>
    {sections_html}
  </main>
</body>
</html>
"""


def main() -> int:
    OUTPUT.write_text(build(), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
