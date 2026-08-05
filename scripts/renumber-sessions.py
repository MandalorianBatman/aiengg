#!/usr/bin/env python3
"""Renumber sessions (51->1, 52->2, networking->3), shorten titles, update tags
and all internal links. Idempotent.

Rename map:
  llm-basics-transformer-internals[-graph]    -> 1-llm-basics[-graph]
  llm-training-pipeline-tool-use[-graph]      -> 2-training-pipeline[-graph]
  doubts-networking-week-1[-graph]            -> 3-week-1-doubts[-graph]

Title map (session files):
  Recording 51 - LLM Basics & Transformer Internals    -> 1. LLM Basics & Transformer Internals
  Recording 52 - LLM Training Pipeline, ...           -> 2. Training Pipeline & Tool Use
  Week 1 Networking - Doubt-Solving Session           -> 3. Week 1 Doubts & Networking

Title map (graph files):
  Knowledge Graph - Recording 51: ...                 -> 1. LLM Basics - Graph
  Knowledge Graph - Recording 52: ...                 -> 2. Training Pipeline - Graph
  Knowledge Graph - Week 1 Networking (...)            -> 3. Week 1 Doubts - Graph

Tag map (frontmatter):
  r51 -> 1
  r52 -> 2
  networking -> 3
"""

import re
from pathlib import Path

ROOT = Path("aiengg")

RENAMES = {
    # main session files
    "llm-basics-transformer-internals": "1-llm-basics",
    "llm-basics-transformer-internals-graph": "1-llm-basics-graph",
    "llm-basics-transformer-internals-graph.json": "1-llm-basics-graph.json",
    # r52
    "llm-training-pipeline-tool-use": "2-training-pipeline",
    "llm-training-pipeline-tool-use-graph": "2-training-pipeline-graph",
    "llm-training-pipeline-tool-use-graph.json": "2-training-pipeline-graph.json",
    # networking
    "doubts-networking-week-1": "3-week-1-doubts",
    "doubts-networking-week-1-graph": "3-week-1-doubts-graph",
    "doubts-networking-week-1-graph.json": "3-week-1-doubts-graph.json",
}

# Sort by length desc so longer matches (graph variants) apply first.
SLUG_PATTERN = re.compile(
    r"\b(" + "|".join(sorted(RENAMES.keys(), key=len, reverse=True)) + r")\b"
)

# Title replacements (matched against the title: line in frontmatter)
TITLE_MAP = {
    "Recording 51 — LLM Basics & Transformer Internals": "1. LLM Basics & Transformer Internals",
    "Recording 52 — LLM Training Pipeline, Tool Use & Fine-Tuning": "2. Training Pipeline & Tool Use",
    "Week 1 Networking — Doubt-Solving Session": "3. Week 1 Doubts & Networking",
    "Knowledge Graph — Recording 51: LLM Basics & Transformer Internals": "1. LLM Basics — Graph",
    "Knowledge Graph — Recording 52: LLM Training, Tool Use & Fine-Tuning": "2. Training Pipeline — Graph",
    "Knowledge Graph — Week 1 Networking (Doubt-Solving)": "3. Week 1 Doubts — Graph",
    "Combined Knowledge Graph — Recordings 51, 52, and Week 1 Networking": "Combined Knowledge Graph — Sessions 1-3",
    "Combined Knowledge Graph": "Combined Knowledge Graph",  # identity
}

# Tag replacements (word-boundary, exact match)
TAG_MAP = {"r51": "1", "r52": "2", "networking": "3"}


def rewrite_links(text: str) -> str:
    """Rewrite bare slug references inside markdown link paths."""

    def repl(m: re.Match) -> str:
        slug = m.group(1)
        return RENAMES[slug]

    return SLUG_PATTERN.sub(repl, text)


def rewrite_title(title: str) -> str:
    if title in TITLE_MAP:
        return TITLE_MAP[title]
    return title


def rewrite_tags_line(line: str) -> str:
    """Rewrite the tags: [foo, bar] line, mapping individual tag values."""
    m = re.match(r"^tags:\s*\[(.+)\]\s*$", line)
    if not m:
        return line
    inner = m.group(1)
    parts = re.findall(r"[^,\s][^,]*[^,\s]|[^,\s]", inner) or [p.strip() for p in inner.split(",")]
    new_parts = []
    for p in parts:
        p_strip = p.strip()
        new_parts.append(TAG_MAP.get(p_strip, p_strip))
    return f"tags: [{', '.join(new_parts)}]"


def rewrite_frontmatter_title_and_tags(text: str) -> str:
    if not text.startswith("---"):
        return text
    lines = text.splitlines(keepends=True)
    end = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            end = i
            break
    if end is None:
        return text
    for i in range(1, end):
        line = lines[i]
        m = re.match(r'^title:\s*"(.+)"\s*$', line)
        if m:
            old_title = m.group(1)
            new_title = rewrite_title(old_title)
            if new_title != old_title:
                lines[i] = f'title: "{new_title}"\n'
        elif line.lstrip().startswith("tags:"):
            lines[i] = rewrite_tags_line(line)
    return "".join(lines)


def process_file(path: Path) -> bool:
    text = path.read_text()
    new_text = rewrite_links(text)
    new_text = rewrite_frontmatter_title_and_tags(new_text)
    if new_text != text:
        path.write_text(new_text)
        return True
    return False


def rename_files():
    moved = []
    for old, new in RENAMES.items():
        for ext in (".md", ".json"):
            src = ROOT / "sessions" / f"{old}{ext}"
            dst = ROOT / "sessions" / f"{new}{ext}"
            if src.exists() and not dst.exists():
                src.rename(dst)
                moved.append((src.relative_to(ROOT), dst.relative_to(ROOT)))
    return moved


def main():
    moved = rename_files()
    print(f"Renamed {len(moved)} files:")
    for src, dst in moved:
        print(f"  {src} -> {dst}")

    print("\nRewriting links / titles / tags...")
    changed = 0
    for p in ROOT.rglob("*.md"):
        if process_file(p):
            print(f"  updated {p.relative_to(ROOT)}")
            changed += 1
    for p in ROOT.rglob("*.json"):
        # JSON graph files also may contain slug refs (in mermaid blocks)
        if process_file(p):
            print(f"  updated {p.relative_to(ROOT)}")
            changed += 1
    print(f"\n{changed} files updated.")


if __name__ == "__main__":
    main()
