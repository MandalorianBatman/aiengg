# AI Engineering Cohort — Recordings 51 & 52

Knowledge artifacts for two foundational classes from the **AI Engineering Cohort** (InterviewReady / Gaurav Sen).

## Sessions

| # | Topic | Duration | Instructor |
|---|-------|----------|------------|
| [51](sessions/llm-basics-transformer-internals.md) | LLM Basics & Transformer Internals | 02:09:55 | Gaurav Sen (Speaker 0) |
| [52](sessions/llm-training-pipeline-tool-use.md) | LLM Training Pipeline, Tool Use & Fine-Tuning | 02:49:25 | Speaker 1 (co-hosts: Tanishk, Ariana, Gaurav) |

> **Note on R52 instructor.** Earlier versions of these notes attributed R52 to Gaurav Sen. The R52 transcript actually introduces "Gaurav" as a co-host separate from the long-form instructor (Speaker 1). The R51 instructor *is* Gaurav Sen. See the speakers table in the R52 lecture summary.

## Folder Structure

```
aiengg/
├── README.md
├── _sidebar.md
├── _coverpage.md
├── index.html
│
├── sessions/
│   ├── index.md                                    # Master session list
│   ├── llm-basics-transformer-internals.md          # R51 detailed summary
│   ├── llm-basics-transformer-internals-graph.md    # R51 Mermaid + concept tables
│   ├── llm-basics-transformer-internals-graph.json  # R51 structured JSON
│   ├── llm-training-pipeline-tool-use.md            # R52 detailed summary
│   ├── llm-training-pipeline-tool-use-graph.md      # R52 Mermaid + concept tables
│   ├── llm-training-pipeline-tool-use-graph.json    # R52 structured JSON
│   └── combined-knowledge-graph.md                  # Cross-session unified view
│
├── concepts/
│   ├── index.md                                    # Alphabetical concept index
│   ├── large-language-model.md
│   ├── attention.md
│   ├── kv-cache.md
│   └── ...                                         # ~25 concept pages
│
├── transcripts/
│   ├── recording-51.srt                            # Raw SRT (1991 segments)
│   └── recording-52.srt                            # Raw SRT (2559 segments)
│
└── scripts/
    └── new-session.py                              # SRT metadata extractor
```

## What You'll Find Here

### 📂 Transcripts
The raw, diarized SRT files from `whisper-diarization`. Each subtitle entry has a speaker label and timestamp.

### 📝 Sessions
Detailed markdown write-ups of each recording. Every concept block contains:
- **Lecture's take** — what the instructor actually said
- **Canonical definition** — web-sourced, drawn from the original paper / canonical blog
- **Key insight** — the "why this matters" deeper point
- **📚 Further reading** — 1-3 high-quality links per concept

### 🧠 Knowledge Graphs
- **JSON files** for programmatic access (concepts, definitions, relationships, entities)
- **Markdown files** with Mermaid diagrams showing how concepts connect, plus a per-concept reading-links table
- **Combined graph** that ties both sessions together

### 🌱 Concept Garden
- Each concept gets a dedicated page with definition, analogies, Mermaid diagrams, and backlinks to every session that mentions it
- Browse by concept across all recordings
- [Browse all concepts »](concepts/index.md)

### 🎯 Quick Start

If you want to **understand LLMs end-to-end**, read in this order:

1. [LLM Basics & Transformer Internals](sessions/llm-basics-transformer-internals.md) — what an LLM *is* (architecture)
2. [Training Pipeline, Tool Use & Fine-Tuning](sessions/llm-training-pipeline-tool-use.md) — how an LLM *is built* (training)
3. [Combined knowledge graph](sessions/combined-knowledge-graph.md) — unified mental model

If you want to **dive into a specific concept**, jump to:

- [Concept index](concepts/index.md) — browse all concepts alphabetically
- [Mermaid diagrams for Session 51](sessions/llm-basics-transformer-internals-graph.md)
- [Mermaid diagrams for Session 52](sessions/llm-training-pipeline-tool-use-graph.md)

## Key Concepts at a Glance

### Recording 51
- LLM = transformer-stack predicting next token autoregressively
- Tokenization (BPE) → Embeddings (768 / 8192-D) → Attention (Q/K/V) → FFN → Linear → Probabilities
- Masked attention gives N training signals per N-token sentence
- KV cache and vocabulary size are critical for cost/performance

### Recording 52
- Pre-training → SFT → Preference Optimization → Serving
- Cross-entropy loss: −log(p_correct) per position
- Tool calling: LLMs emit tokens; server interprets
- Modern preference optimization: GRPO (DeepSeek), DPO, PPO
- KV cache, context window, vocabulary are the key inference knobs

## Speakers

| Recording | Long-form instructor | Co-hosts | Students |
|-----------|---------------------|----------|----------|
| 51 | Gaurav Sen (Speaker 0) | — | ~25 (various speaker IDs) |
| 52 | Speaker 1 | Tanishk (IIT Bombay), Ariana (IIT Madras), Gaurav | ~25 (various speaker IDs) |

## Sources

- **Course:** AI Engineering Cohort (InterviewReady / Gaurav Sen)
- **Platform:** aiengg.dev
- **Transcripts:** Generated via `whisper-diarization` (medium.en + pyannote)

## Validation Status

Notes were cross-checked against the SRT transcripts and corrected for:
- **PPO** = Proximal **Policy** Optimization (transcript has the instructor misspeaking this as "Proximal Preference Optimization" — corrected with footnote)
- **GRPO** = Group Relative **Policy** Optimization (transcript had "Preference" — corrected)
- **Dimensions** — dropped 12288 (not in transcript; only 768 and 8192 are mentioned)
- **GPT-2 time-query claim** — removed (not in R52 transcript)
- **Data shortage claim** — kept but tagged as external industry context (Villalobos 2024), not a lecture assertion
- **SWE-rebench** — canonical spelling preserved with footnote that transcript has "sw-rebench"
- **Cross-entropy formula** — both forms documented (lecture shorthand vs. standard canonical form)
- **Sigmoid-as-anchor** — moved to the preference-optimization section where the transcript places it

Per-concept reading links were sourced from: [Vaswani 2017](https://arxiv.org/abs/1706.03762), [Jay Alammar](https://jalammar.github.io/), [Andrej Karpathy](https://www.youtube.com/@AndrejKarpathy), [3Blue1Brown](https://www.3blue1brown.com/), [HuggingFace NLP Course](https://huggingface.co/learn/llm-course), [Lilian Weng](https://lilianweng.github.io/), [Sebastian Raschka](https://sebastianraschka.com/), [Goodfellow — Deep Learning](https://www.deeplearningbook.org/), and the original papers for every algorithm cited.
