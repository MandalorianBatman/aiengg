#!/usr/bin/env python3
"""Aggregate 'Lecture's take' quotes from session files and add them as a
'## Lecture's take' section to the matching concept page.

Idempotent: re-running replaces the section in place.
"""

import re
from pathlib import Path

ROOT = Path("aiengg")

# Map session concept H3 headings -> concept page slug (manual overrides
# for fuzzy-match failures or sub-concepts folded into parents).
H3_TO_SLUG = {
    # session 1
    "Large Language Model (LLM)": "large-language-model",
    "Token": "token",
    "Byte Pair Encoding (BPE)": "byte-pair-encoding",
    "Vector (Embedding)": "vector-embedding",
    "Transformer": "transformer",
    "Positional encoding": "positional-encoding",
    "Layer normalization (and RMSNorm)": "layer-normalization",
    "Attention": "attention",
    "Q, K, V (Query, Key, Value)": "query-key-value",
    "Multi-head attention": "attention",  # sub-concept, attribute to parent
    "Masked attention (causal masking)": "masked-attention",
    "Feed-forward network (FFN)": "feed-forward-network",
    "Linear layer / Unembedding (LM head)": "linear-unembedding",
    "Vocabulary": "vocabulary",
    "N-grams vs LLMs": "n-gram-vs-llm",
    "Context window": "context-window",
    "KV cache": "kv-cache",
    "Input vs Output tokens": "input-vs-output-tokens",
    # session 2
    "Pre-training": "pre-training",
    "Data Pipeline": "data-pipeline",
    "Fill-in-the-Blank Training": "fill-in-the-blank-training",
    "Training Loop": "training-loop",
    "Cross-entropy loss": "cross-entropy-loss",
    "Sigmoid": "preference-optimization",  # fold into parent
    "Tool calling": "tool-calling",
    "Reinforcement Learning from Human Feedback (RLHF)": "preference-optimization",
    "PPO — Proximal Policy Optimization": "preference-optimization",
    "DPO — Direct Preference Optimization": "preference-optimization",
    "GRPO — Group Relative Policy Optimization": "preference-optimization",
    "Model serving": "model-serving",
    "Pipeline parallelism (GPU orchestration)": "gpu-orchestration",
    "Data shortage": "data-shortage",
    # session 3 — these map to Q&A anchors, not concept pages
    # (Q&A structure is kept in session file, not surfaced as concepts)
}


SESSION_TITLE = {
    "1-llm-basics": "1. LLM Basics & Transformer Internals",
    "2-training-pipeline": "2. Training Pipeline & Tool Use",
    "3-week-1-doubts": "3. Week 1 Doubts & Networking",
}


def parse_session(path: Path):
    """Yield (h3_title, lecture_take_text, session_slug)."""
    text = path.read_text()
    slug = path.stem
    # Split on H3 boundaries
    parts = re.split(r"^### (.+)$", text, flags=re.MULTILINE)
    # parts[0] is preamble, then alternating title/body
    for i in range(1, len(parts), 2):
        h3 = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        # Match the lecture's take blockquote
        # Patterns seen in the corpus:
        #   > **Lecture's take:** ...
        #   > **Lecture's take (Gaurav):** ...
        # Multi-line blockquote.
        m = re.search(
            r"> \*\*Lecture's take:\*\* (.+?)\n\n\*\*",
            body,
            re.DOTALL,
        )
        if not m:
            # Try alternative phrasing with parens like (Gaurav)
            m = re.search(
                r"> \*\*Lecture's take \([^)]+\):\*\* (.+?)\n\n\*\*",
                body,
                re.DOTALL,
            )
        if not m:
            continue
        quote = m.group(1).strip()
        # Collapse internal newlines into spaces
        quote = re.sub(r"\s*\n\s*", " ", quote)
        quote = re.sub(r"\s+", " ", quote)
        if not quote:
            continue
        yield h3, quote, slug


def aggregate():
    by_slug: dict[str, list[tuple[str, str, str]]] = {}  # slug -> [(quote, h3, session_slug)]
    for session in ["1-llm-basics", "2-training-pipeline", "3-week-1-doubts"]:
        path = ROOT / "sessions" / f"{session}.md"
        if not path.exists():
            continue
        for h3, quote, slug in parse_session(path):
            target = H3_TO_SLUG.get(h3)
            if not target:
                continue
            by_slug.setdefault(target, []).append((quote, h3, slug))
    return by_slug


def update_concept_page(slug: str, entries: list[tuple[str, str, str]]):
    path = ROOT / "concepts" / f"{slug}.md"
    if not path.exists():
        print(f"  no concept page for slug={slug} ({entries[0][1]!r})")
        return
    text = path.read_text()
    # Build new section
    lines = ["## Lecture's take", ""]
    for quote, h3, sess in entries:
        title = SESSION_TITLE.get(sess, sess)
        session_link = f"../sessions/{sess}.md"
        # Convert title like "1. LLM Basics & Transformer Internals" -> "Session 1"
        # The title[0] is "1" / "2" / "3"
        lines.append(f"**From [Session {title[0]}]({session_link}):**")
        lines.append("")
        # Blockquote the quote; collapse internal whitespace to single block
        lines.append(f"> {quote}")
        lines.append("")
    section = "\n".join(lines).rstrip() + "\n"

    # Replace existing section if present
    pattern = re.compile(
        r"^## Lecture['']s take\s*\n(?:.*?\n)*?(?=^## |\Z)",
        re.MULTILINE,
    )
    if pattern.search(text):
        new_text = pattern.sub(section + "\n", text, count=1)
    else:
        # Insert before "## Mentioned In" section (or at end before Further Reading)
        anchor = re.search(r"^## Mentioned In", text, re.MULTILINE)
        if anchor:
            new_text = text[: anchor.start()] + section + "\n" + text[anchor.start():]
        else:
            # Fall back: append before Further Reading
            anchor = re.search(r"^## Further Reading", text, re.MULTILINE)
            if anchor:
                new_text = text[: anchor.start()] + section + "\n" + text[anchor.start():]
            else:
                new_text = text.rstrip() + "\n\n" + section

    path.write_text(new_text)
    print(f"  updated {path.relative_to(ROOT)} ({len(entries)} entries)")


def main():
    aggregated = aggregate()
    print(f"Aggregated {sum(len(v) for v in aggregated.values())} lecture takes across {len(aggregated)} concept pages.\n")
    for slug, entries in sorted(aggregated.items()):
        update_concept_page(slug, entries)


if __name__ == "__main__":
    main()
