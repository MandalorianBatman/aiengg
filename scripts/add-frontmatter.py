#!/usr/bin/env python3
"""Add YAML frontmatter (title + tags) to all markdown files under aiengg/.

Idempotent: if frontmatter already exists, leaves it alone (just updates title/tags).

Quartz uses frontmatter `title` for the explorer, graph, and breadcrumbs.
Without it, the filename/slug becomes the title and the graph shows weak labels.
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "aiengg"

# Folder → default tags. Concepts get the topic bucket from the index.md groupings.
FOLDER_TAGS = {
    "sessions": ["session"],
    "concepts": ["concept"],
    "transcripts": ["transcript"],
}

# More specific tags per concept file (subset — most are just "concept")
# Inferred from concepts/index.md groupings
CONCEPT_TAGS = {
    # Architecture & Internals
    "large-language-model.md": ["concept", "architecture"],
    "next-token-prediction.md": ["concept", "architecture"],
    "token.md": ["concept", "architecture"],
    "byte-pair-encoding.md": ["concept", "architecture"],
    "vector-embedding.md": ["concept", "architecture"],
    "transformer.md": ["concept", "architecture"],
    "attention.md": ["concept", "architecture"],
    "masked-attention.md": ["concept", "architecture"],
    "feed-forward-network.md": ["concept", "architecture"],
    "linear-layer.md": ["concept", "architecture"],
    "vocabulary.md": ["concept", "architecture"],
    "model-parameters.md": ["concept", "architecture"],
    "input-vs-output-tokens.md": ["concept", "architecture"],
    # Inference & Optimization
    "context-window.md": ["concept", "inference"],
    "kv-cache.md": ["concept", "inference"],
    "temperature.md": ["concept", "inference"],
    "model-serving.md": ["concept", "inference"],
    "gpu-orchestration.md": ["concept", "inference"],
    # Training Pipeline
    "pre-training.md": ["concept", "training"],
    "data-pipeline.md": ["concept", "training"],
    "fill-in-the-blank-training.md": ["concept", "training"],
    "training-loop.md": ["concept", "training"],
    "cross-entropy-loss.md": ["concept", "training"],
    "supervised-fine-tuning.md": ["concept", "training"],
    "preference-optimization.md": ["concept", "training"],
    "data-shortage.md": ["concept", "training"],
    # Capabilities & Trends
    "tool-calling.md": ["concept", "capabilities"],
    "hallucination.md": ["concept", "capabilities"],
}

SESSION_TAGS = {
    "llm-basics-transformer-internals.md": ["session", "r51", "architecture"],
    "llm-basics-transformer-internals-graph.md": ["session", "r51", "graph"],
    "llm-basics-transformer-internals-graph.json": None,  # skip JSON
    "llm-training-pipeline-tool-use.md": ["session", "r52", "training"],
    "llm-training-pipeline-tool-use-graph.md": ["session", "r52", "graph"],
    "llm-training-pipeline-tool-use-graph.json": None,
    "doubts-networking-week-1.md": ["session", "networking", "qa"],
    "doubts-networking-week-1-graph.md": ["session", "networking", "graph"],
    "doubts-networking-week-1-graph.json": None,
    "combined-knowledge-graph.md": ["session", "graph", "all"],
    "index.md": ["session", "index"],
}


def find_h1(content: str) -> str | None:
    """Find the first H1 in the markdown content."""
    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def parse_existing_frontmatter(content: str) -> tuple[dict | None, str]:
    """Return (frontmatter_dict, body_without_frontmatter)."""
    if not content.startswith("---"):
        return None, content
    # Find the closing ---
    lines = content.splitlines(keepends=True)
    if len(lines) < 2 or lines[0].strip() != "---":
        return None, content
    end_idx = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None, content
    yaml_text = "".join(lines[1:end_idx])
    body = "".join(lines[end_idx + 1 :])
    # Tiny YAML parser — only handles the keys we use
    fm = {}
    for line in yaml_text.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            items = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",")]
            fm[key.strip()] = [x for x in items if x]
        else:
            fm[key.strip()] = val.strip('"').strip("'")
    return fm, body


def tags_for(rel_path: Path) -> list[str] | None:
    """Return tags for a file (None = skip this file)."""
    name = rel_path.name
    parent = rel_path.parent.name
    if parent == "concepts":
        return CONCEPT_TAGS.get(name, ["concept"])
    if parent == "sessions":
        return SESSION_TAGS.get(name, ["session"])
    if parent == "." and name == "README.md":
        return ["home"]
    return ["page"]


def process_file(path: Path) -> bool:
    """Process one file. Returns True if changed."""
    rel = path.relative_to(ROOT)
    tags = tags_for(rel)
    if tags is None:
        return False  # skip JSON etc.
    content = path.read_text(encoding="utf-8")
    existing, body = parse_existing_frontmatter(content)
    h1 = find_h1(body)
    title = (existing or {}).get("title") or h1 or rel.stem.replace("-", " ").title()
    fm_lines = ["---", f'title: "{title}"']
    if tags:
        tag_list = ", ".join(tags)
        fm_lines.append(f"tags: [{tag_list}]")
    fm_lines.append("---")
    fm_block = "\n".join(fm_lines) + "\n\n"
    # If existing frontmatter had additional keys we didn't parse, preserve them
    if existing:
        for k, v in existing.items():
            if k not in ("title", "tags"):
                fm_lines.insert(-1, f'{k}: "{v}"' if isinstance(v, str) else f"{k}: {v}")
        fm_block = "\n".join(fm_lines) + "\n\n"
    new_content = fm_block + body.lstrip("\n")
    if new_content == content:
        return False
    path.write_text(new_content, encoding="utf-8")
    return True


def main() -> int:
    changed = 0
    skipped = 0
    for path in ROOT.rglob("*.md"):
        rel = path.relative_to(ROOT)
        tags = tags_for(rel)
        if tags is None:
            skipped += 1
            continue
        if process_file(path):
            changed += 1
            print(f"+ {rel}")
    print(f"\n{changed} files updated, {skipped} skipped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
