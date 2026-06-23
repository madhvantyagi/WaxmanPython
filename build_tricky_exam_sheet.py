from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SECTION_DIR = ROOT / "StudyGuides" / "tricky_sections"
OUTPUT = ROOT / "StudyGuides" / "tricky-python-final-exam-drill.html"

SECTION_ORDER = [
    ("part4_lists_runtime.md", "Lists, Runtime, Aliasing"),
    ("part5_functions_references.md", "Functions and References"),
    ("dicts_sets_charts.md", "Dictionaries, Sets, and Data Views"),
    ("generators.md", "Iterators and Generators"),
    ("decorators.md", "Decorators and Closures"),
    ("oop.md", "Objects and Classes"),
]

ADDITION_DIR = ROOT / "StudyGuides" / "tricky_sections_additions"
ADDITION_ORDER = [
    ("comprehensions_extra_gaps.md", "Comprehensions and Remaining Risk Drills"),
    ("part4_runtime_additions.md", "Part 4 Runtime and Modules"),
    ("part5_sets_unpacking_matrix_additions.md", "Part 5 Sets, Unpacking, and Matrices"),
    ("dicts_data_additions.md", "Dictionary Data Problems"),
    ("generators_design_additions.md", "Generator Design Problems"),
    ("decorators_additions.md", "Decorator Design Problems"),
]


def inline_format(text: str) -> str:
    escaped = html.escape(text)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    in_code = False
    code_lines: list[str] = []
    in_list = False
    in_details = False

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

    def close_details() -> None:
        nonlocal in_details
        if in_details:
            close_list()
            flush_paragraph()
            out.append("</details>")
            in_details = False

    for line in lines:
        stripped = line.rstrip()

        if stripped.startswith("```"):
            if in_code:
                out.append(
                    "<pre><code>"
                    + html.escape("\n".join(code_lines))
                    + "</code></pre>"
                )
                code_lines = []
                in_code = False
            else:
                flush_paragraph()
                close_list()
                in_code = True
            continue

        if in_code:
            code_lines.append(stripped)
            continue

        if not stripped:
            flush_paragraph()
            close_list()
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            text = heading.group(2).strip()
            if re.match(r"^(\[(HIGH|MID|LOW)\]\s*)?\d+\.", text):
                close_details()
                out.append(
                    f"<details class=\"question\"><summary>{inline_format(text)}</summary>"
                )
                in_details = True
            else:
                close_details()
                html_level = min(level + 1, 4)
                out.append(f"<h{html_level}>{inline_format(text)}</h{html_level}>")
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline_format(stripped[2:].strip())}</li>")
            continue

        paragraph.append(stripped)

    if in_code:
        out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
    close_list()
    flush_paragraph()
    close_details()
    return "\n".join(out)


def count_questions(markdown: str) -> int:
    return len(
        re.findall(
            r"^#{2,3}\s+(\[(HIGH|MID|LOW)\]\s*)?\d+\.",
            markdown,
            flags=re.MULTILINE,
        )
    )


def screenshot_topic_map() -> str:
    return """
    <section class="review">
      <h2>Screenshot Topic Map</h2>
      <p>If someone says these are the final topics, this is what each word means and where to drill it in this sheet.</p>
      <ul>
        <li><strong>Dictionaries</strong>: hash-table keys/values, missing-key errors, <code>get</code>, <code>pop</code>, live views, shallow copy, mutation during iteration. Use <a href="#dicts-sets-charts">Dictionaries, Sets, and Data Views</a>.</li>
        <li><strong>Sets</strong>: unique unordered hash-based elements, <code>add</code>, <code>remove</code> vs <code>discard</code>, arbitrary <code>pop</code>, set operations, and unhashable-element traps. Use <a href="#dicts-sets-charts">Dictionaries, Sets, and Data Views</a> and <a href="#part5-functions-references">Functions and References</a>.</li>
        <li><strong>functools</strong>: in our PDFs this mainly means <code>functools.wraps</code> for decorators. It keeps the original function metadata after wrapping. Broader <code>functools</code> tools are summarized below.</li>
        <li><strong>groupby</strong>: <code>itertools.groupby</code> groups consecutive runs only, and each group is a one-pass iterator. Use the <code>groupby</code> drill in <a href="#dicts-sets-charts">Dictionaries, Sets, and Data Views</a>.</li>
        <li><strong>counting</strong>: usually <code>collections.Counter</code> or manual dictionary counting. Watch missing counts, negative counts, and <code>+counter</code>. Use the <code>Counter</code> drill in <a href="#dicts-sets-charts">Dictionaries, Sets, and Data Views</a>.</li>
        <li><strong>inverted index</strong>: a dictionary mapping each word to where it appears, often <code>word -&gt; [(line_number, position), ...]</code> or <code>word -&gt; {'count': n, 'lines': [...]}</code>. It is dictionary/list/defaultdict practice.</li>
        <li><strong>stuff after midterm</strong>: dictionaries, sets, files/pickle, <code>Counter</code>, <code>defaultdict</code>, <code>groupby</code>, generators, decorators, OOP/properties, and 2D-list style tracing from the review.</li>
        <li><strong>data hiding / encapsulation</strong>: OOP idea where outside code should not directly break object state. In Python this is convention plus properties: <code>_name</code>, name mangling with <code>__name</code>, and <code>@property</code> setters. Use <a href="#oop">Objects and Classes</a>.</li>
      </ul>
    </section>
    """


def functools_appendix() -> str:
    return """
    <section id="functools-quick-hit" class="topic">
      <h2>functools Quick Hit</h2>
      <p>The class PDFs explicitly use <code>functools.wraps</code>. If the exam says just "functools", these are the realistic things to recognize.</p>

      <details class="question">
        <summary>functools.wraps keeps metadata after decoration</summary>
        <pre><code>import functools

def deco(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@deco
def add(a, b):
    "adds two numbers"
    return a + b

print(add.__name__)
print(add.__doc__)</code></pre>
        <pre><code>add
adds two numbers</code></pre>
        <p>Behind the scenes: without <code>@functools.wraps(func)</code>, the name <code>add</code> would point to <code>wrapper</code>, so metadata like <code>__name__</code> and <code>__doc__</code> would look like the wrapper's metadata. <code>wraps</code> copies the original metadata onto the wrapper.</p>
      </details>

      <details class="question">
        <summary>functools.reduce consumes left to right</summary>
        <pre><code>from functools import reduce

def f(a, b):
    print("call", a, b)
    return a - b

print(reduce(f, [10, 3, 2]))</code></pre>
        <pre><code>call 10 3
call 7 2
5</code></pre>
        <p>Behind the scenes: <code>reduce</code> keeps an accumulator. First accumulator is <code>10</code>, then it calls <code>f(10, 3)</code> and stores <code>7</code>. Then it calls <code>f(7, 2)</code> and stores <code>5</code>. This is not the same as doing all operations at once.</p>
      </details>

      <details class="question">
        <summary>functools.partial pre-fills arguments</summary>
        <pre><code>from functools import partial

def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
print(square(5))
print(square(base=3))</code></pre>
        <pre><code>25
9</code></pre>
        <p>Behind the scenes: <code>partial</code> creates a new callable that remembers some arguments. Here it remembers <code>exp=2</code>. Calling <code>square(5)</code> is like calling <code>power(5, exp=2)</code>.</p>
      </details>
    </section>
    """


def build() -> str:
    rendered_sections: list[str] = []
    rendered_additions: list[str] = []
    nav_items: list[str] = []
    total_questions = 0

    for filename, title in SECTION_ORDER:
        path = SECTION_DIR / filename
        markdown = path.read_text(encoding="utf-8")
        questions = count_questions(markdown)
        total_questions += questions
        slug = Path(filename).stem.replace("_", "-")
        nav_items.append(
            f"<a href=\"#{slug}\"><span>{html.escape(title)}</span><small>{questions} drills</small></a>"
        )
        rendered_sections.append(
            f"<section id=\"{slug}\" class=\"topic\"><h2>{html.escape(title)}</h2>"
            f"<p class=\"source-note\">Built from <code>{html.escape(filename)}</code> plus the final-review transcript.</p>"
            f"{markdown_to_html(markdown)}</section>"
        )

    additions_total = 0
    for filename, title in ADDITION_ORDER:
        path = ADDITION_DIR / filename
        markdown = path.read_text(encoding="utf-8")
        questions = count_questions(markdown)
        additions_total += questions
        total_questions += questions
        slug = "advanced-" + Path(filename).stem.replace("_", "-")
        nav_items.append(
            f"<a href=\"#{slug}\"><span>{html.escape(title)}</span><small>{questions} advanced</small></a>"
        )
        rendered_additions.append(
            f"<section id=\"{slug}\" class=\"topic advanced\"><h2>{html.escape(title)}</h2>"
            f"<p class=\"source-note\">Advanced gap questions from <code>{html.escape(filename)}</code>. OOP was intentionally left unchanged.</p>"
            f"{markdown_to_html(markdown)}</section>"
        )

    nav_html = "\n".join(nav_items)
    sections_html = "\n".join(rendered_sections)
    additions_html = "\n".join(rendered_additions)
    display_questions = total_questions + 3

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tricky Python Final Exam Drill Sheet</title>
  <style>
    :root {{
      --ink: #172026;
      --muted: #5b6670;
      --line: #d9e1e7;
      --panel: #f6f8fa;
      --panel-strong: #eef5f3;
      --accent: #0f766e;
      --accent-dark: #115e59;
      --danger: #8a3b12;
      --code-bg: #101820;
      --code-fg: #e8eef2;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
      color: var(--ink);
      background: #ffffff;
      line-height: 1.55;
    }}
    header {{
      border-bottom: 1px solid var(--line);
      background: var(--panel-strong);
    }}
    .wrap {{
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
    }}
    header .wrap {{
      padding: 32px 0 26px;
    }}
    h1 {{
      margin: 0 0 10px;
      font-size: clamp(2rem, 4vw, 3.35rem);
      line-height: 1.05;
      letter-spacing: 0;
    }}
    .subtitle {{
      margin: 0;
      max-width: 900px;
      color: var(--muted);
      font-size: 1.06rem;
    }}
    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 16px;
    }}
    .pill {{
      display: inline-flex;
      align-items: center;
      min-height: 28px;
      padding: 4px 9px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #fff;
      color: #31414d;
      font-size: 0.86rem;
      font-weight: 700;
    }}
    main {{
      padding: 24px 0 56px;
    }}
    .how {{
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      margin-bottom: 18px;
    }}
    .how h2, .review h2 {{
      margin-top: 0;
    }}
    .nav {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 10px;
      margin: 16px 0 26px;
    }}
    .nav a {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      padding: 12px 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      text-decoration: none;
      color: var(--accent-dark);
      background: #fff;
      font-weight: 800;
    }}
    .nav small {{
      color: var(--muted);
      font-weight: 700;
      white-space: nowrap;
    }}
    .review {{
      margin: 18px 0 28px;
      padding: 16px;
      border-left: 5px solid var(--accent);
      background: #f8fbfa;
      border-radius: 6px;
    }}
    h2 {{
      margin: 32px 0 10px;
      font-size: 1.6rem;
    }}
    h3 {{
      margin: 24px 0 8px;
      font-size: 1.2rem;
    }}
    h4 {{
      margin: 18px 0 8px;
      font-size: 1.05rem;
    }}
    .topic {{
      border-top: 2px solid var(--line);
      padding-top: 12px;
      margin-top: 22px;
    }}
    .source-note {{
      color: var(--muted);
      margin-top: -4px;
      font-size: 0.92rem;
    }}
    details.question {{
      border: 1px solid var(--line);
      border-radius: 8px;
      margin: 12px 0;
      background: #fff;
      overflow: hidden;
    }}
    details.question summary {{
      cursor: pointer;
      padding: 13px 15px;
      font-weight: 850;
      color: var(--accent-dark);
      background: #f7faf9;
    }}
    details.question[open] summary {{
      border-bottom: 1px solid var(--line);
    }}
    details.question > p,
    details.question > ul,
    details.question > pre {{
      margin-left: 15px;
      margin-right: 15px;
    }}
    ul {{
      padding-left: 24px;
    }}
    li + li {{
      margin-top: 4px;
    }}
    code {{
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 0.92em;
    }}
    pre {{
      overflow-x: auto;
      padding: 13px 14px;
      border-radius: 7px;
      background: var(--code-bg);
      color: var(--code-fg);
      line-height: 1.45;
      tab-size: 4;
    }}
    pre code {{
      color: inherit;
      font-size: 0.91rem;
    }}
    .danger {{
      color: var(--danger);
      font-weight: 800;
    }}
    @media print {{
      .nav {{ display: none; }}
      details.question {{ break-inside: avoid; }}
      details.question:not([open]) > *:not(summary) {{ display: block; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <h1>Tricky Python Final Exam Drill Sheet</h1>
      <p class="subtitle">A combined question sheet focused on the professor-style traps: exact output, exact errors, memory/reference behavior, mutation during loops, iterators, generators, decorators, dictionaries, 2D lists, and objects.</p>
      <div class="meta">
        <span class="pill">{display_questions} collapsible drill blocks</span>
        <span class="pill">6 guide sources</span>
        <span class="pill">{additions_total} advanced gap drills</span>
        <span class="pill">final-review transcript used</span>
        <span class="pill">click questions to expand</span>
      </div>
    </div>
  </header>
  <main class="wrap">
    <section class="how">
      <h2>How To Use This</h2>
      <ul>
        <li>First write the exact output or exact exception without opening the answer.</li>
        <li>Then draw names as arrows to objects: list, dict, object, function frame, generator frame.</li>
        <li>Ask whether the line mutates an existing object or rebinds a name to a new object.</li>
        <li>For loops and generators, track the hidden iterator state. The next value is not guessed; it is stored inside the iterator/generator object.</li>
        <li>Priority labels mean exam risk: <code>[HIGH]</code> first, then <code>[MID]</code>, then <code>[LOW]</code>. The advanced gap drills are designed to cover broader question types, not just printed output.</li>
      </ul>
    </section>

    <section class="review">
      <h2>Final Review Patterns To Prioritize</h2>
      <ul>
        <li>Dictionaries: bracket lookup raises on missing keys; <code>get</code> and <code>pop(default)</code> can avoid that; <code>copy()</code> is shallow.</li>
        <li>Views and grouping: <code>d.keys()</code>/<code>d.items()</code> are live views, and <code>itertools.groupby</code> gives one-pass group iterators that often need <code>list(group)</code>.</li>
        <li>Generators: calling the function makes a generator object; the body runs only when consumed; extra <code>next()</code> raises <code>StopIteration</code>.</li>
        <li>Decorators: the decorator runs when the function is defined, and the wrapper runs later when the decorated name is called. Stacked decorators are a common output-tracing trap.</li>
        <li>2D lists: repeated rows, diagonal extraction, nested loops, and list comprehensions are high-probability final-review material.</li>
        <li>Files/iterators: after a file-like object or iterator is consumed, reading it again from the same position may produce nothing unless you reset or recreate it.</li>
      </ul>
    </section>

    {screenshot_topic_map()}

    <nav class="nav" aria-label="Topics">
      {nav_html}
    </nav>

    {sections_html}
    <section class="review">
      <h2>Advanced Gap Drills Added After Deeper PDF Review</h2>
      <p>These questions target concepts that appeared in the extracted PDFs but were thinner in the first combined sheet. They avoid OOP updates and focus on modules/runtime, sets, unpacking, matrix-style problems, dictionary data problems, generator design, and decorator design.</p>
    </section>
    {additions_html}
    {functools_appendix()}
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
