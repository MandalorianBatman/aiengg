---
title: "AI Engineering Knowledge Base"
tags: [home]
aliases: [README, README.md]
---

# AI Engineering Knowledge Base

Knowledge artifacts from the **AI Engineering Cohort** (InterviewReady / Gaurav Sen).

## About

This is a personal knowledge base built from the recordings of the AI
Engineering Cohort run by [InterviewReady](https://interviewready.io/) (with
[Gaurav Sen](https://www.youtube.com/@GauravSen) as a long-form instructor).
The goal is to turn lecture audio into durable, interlinked written material
that I can refer back to — and that improves as more sessions are added.

Each recording is processed into three layers:

1. **A session write-up** — chronological narrative of the lecture, with
   concept mentions linked to the concept pages (no duplicated definitions).
2. **A knowledge graph** — Mermaid diagrams of how concepts connect, plus a
   JSON dump for programmatic use.
3. **A concept garden** — each concept gets its own page with canonical
   definition, analogy, Mermaid diagram, related concepts, and an aggregated
   "Lecture's take" section pulling quotes from every session that mentioned
   it. As more recordings are added, concept pages grow richer over time.

The notes are not a transcript. They are cross-checked against the SRT,
corrected where the instructor misspoke (see the [validation log](#validation-status)
at the bottom), and linked together so the [graph view](concepts/index.md)
works as a real index into the material.

This site is built with [Quartz](https://quartz.jzhao.xyz/) (vendored at the
repo root) and deployed via Tailscale. The source lives in
[`MandalorianBatman/aiengg`](https://github.com/MandalorianBatman/aiengg).

## Sessions

| # | Topic | Duration | Instructor |
|---|-------|----------|------------|
| [1](sessions/1-llm-basics.md) | LLM Basics & Transformer Internals | 02:09:55 | Gaurav Sen (Speaker 0) |
| [2](sessions/2-training-pipeline.md) | Training Pipeline & Tool Use | 02:49:25 | Speaker 1 (co-hosts: Tanishk, Ariana, Gaurav) |
| [3](sessions/3-week-1-doubts.md) | Week 1 Doubts & Networking | 01:42:01 | Gaurav Sen (Speaker 7) with Tanishk + Tanishq (co-instructors) |

> **Note on session 2 instructor.** Earlier versions of these notes attributed session 2 to Gaurav Sen. The transcript actually introduces "Gaurav" as a co-host separate from the long-form instructor (Speaker 1). The session 1 instructor *is* Gaurav Sen. See the speakers table in the session 2 write-up.

## Folder Structure

```
aiengg/
├── index.md                                    # This page
├── sessions/
│   ├── index.md                                # Master session list
│   ├── 1-llm-basics.md                         # Session 1 detailed write-up
│   ├── 1-llm-basics-graph.md                   # Session 1 Mermaid + concept tables
│   ├── 1-llm-basics-graph.json                 # Session 1 structured JSON
│   ├── 2-training-pipeline.md                  # Session 2 detailed write-up
│   ├── 2-training-pipeline-graph.md            # Session 2 Mermaid + concept tables
│   ├── 2-training-pipeline-graph.json          # Session 2 structured JSON
│   ├── 3-week-1-doubts.md                      # Session 3 write-up (Q&A)
│   ├── 3-week-1-doubts-graph.md                # Session 3 Mermaid + tables
│   ├── 3-week-1-doubts-graph.json              # Session 3 structured JSON
│   └── combined-knowledge-graph.md             # Cross-session unified view
│
├── concepts/
│   ├── index.md                                # Alphabetical concept index
│   ├── large-language-model.md
│   ├── attention.md
│   ├── kv-cache.md
│   ├── hallucination.md
│   └── ...                                     # ~36 concept pages
│
├── transcripts/                                # Raw SRTs (gitignored)
└── scripts/                                    # Helper scripts (not rendered)
```

## What You'll Find Here

### 📂 Transcripts
The raw, diarized SRT files from `whisper-diarization`. Each subtitle entry has a speaker label and timestamp.

### 📝 Sessions
Chronological narrative of each recording. Each session page has a one-line summary per concept covered, linking to the concept page for depth.

### 🧠 Knowledge Graphs
- **JSON files** for programmatic access (concepts, definitions, relationships, entities)
- **Markdown files** with Mermaid diagrams showing how concepts connect
- **Combined graph** that ties all sessions together

### 🌱 Concept Garden
- Each concept gets a dedicated page with definition, analogy, Mermaid diagram, "Lecture's take" quotes from every session, and backlinks
- Browse by concept across all recordings
- [Browse all concepts »](concepts/index.md)

### 🎯 Quick Start

If you want to **understand LLMs end-to-end**, read in this order:

1. [1. LLM Basics & Transformer Internals](sessions/1-llm-basics.md) — what an LLM *is* (architecture)
2. [2. Training Pipeline & Tool Use](sessions/2-training-pipeline.md) — how an LLM *is built* (training)
3. [3. Week 1 Doubts & Networking](sessions/3-week-1-doubts.md) — common Week 1 confusions resolved (encoder/decoder, embeddings, FFN, hallucination)
4. [Combined knowledge graph](sessions/combined-knowledge-graph.md) — unified mental model

If you want to **dive into a specific concept**, jump to:

- [Concept index](concepts/index.md) — browse all concepts alphabetically
- [Mermaid diagrams for Session 1](sessions/1-llm-basics-graph.md)
- [Mermaid diagrams for Session 2](sessions/2-training-pipeline-graph.md)
- [Mermaid diagrams for Session 3](sessions/3-week-1-doubts-graph.md)

## Key Concepts at a Glance

### Session 1 — Architecture
- LLM = transformer-stack predicting next token autoregressively
- Tokenization (BPE) → Embeddings (768 / 8192-D) → Attention (Q/K/V) → FFN → Linear → Probabilities
- Masked attention gives N training signals per N-token sentence
- KV cache and vocabulary size are critical for cost/performance

### Session 2 — Training
- Pre-training → SFT → Preference Optimization → Serving
- Cross-entropy loss: −log(p_correct) per position
- Tool calling: LLMs emit tokens; server interprets
- Modern preference optimization: GRPO (DeepSeek), DPO, PPO
- KV cache, context window, vocabulary are the key inference knobs

### Session 3 — Doubts
- Modern LLMs are decoder-only; encoder-only lives on as embedding backbones for RAG
- Embeddings live inside model weights as the embedding matrix — *not* in a vector DB
- Backprop updates everything learnable (embeddings + Q/K/V + FFN); tokenizer rules are not learnable
- KV cache ≠ QKV — it is an inference-time optimization caching K and V across generation steps
- Hallucination is structural: BPE decomposes unknown words, the LLM best-guesses
- Pre-training + post-training are both training (weights update). Validation is a held-out data split, not a training phase
- For AI engineering roles, system-level depth (RAG, agents, evals) > frontier-lab ML depth
- Personal brand via published artifacts is the highest-leverage recruiter signal
- Diffusion models and LLMs share the transformer backbone; differ in modality (image vs text)

## Speakers

| Session | Long-form instructor | Co-hosts | Students |
|---------|---------------------|----------|----------|
| 1 | Gaurav Sen (Speaker 0) | — | ~25 (various speaker IDs) |
| 2 | Speaker 1 | Tanishk (IIT Bombay), Ariana (IIT Madras), Gaurav | ~25 (various speaker IDs) |
| 3 | Gaurav Sen (Speaker 7) | Tanishk (Speaker 1), Tanishq (Speaker 4) | ~15 (Abhishek, Abhisit, Deeksha, Panush, Sridhar, Manasi, Poorna, Collier Blake, Sid, Arun, Ayush, Sandeep, …) |

## Sources

- **Course:** AI Engineering Cohort (InterviewReady / Gaurav Sen)
- **Platform:** aiengg.dev
- **Transcripts:** Generated via `whisper-diarization` (medium.en + pyannote)

## Validation Status

Notes were cross-checked against the SRT transcripts and corrected for:
- **PPO** = Proximal **Policy** Optimization (transcript has the instructor misspeaking this as "Proximal Preference Optimization" — corrected with footnote)
- **GRPO** = Group Relative **Policy** Optimization (transcript had "Preference" — corrected)
- **Dimensions** — dropped 12288 (not in transcript; only 768 and 8192 are mentioned)
- **GPT-2 time-query claim** — removed (not in session 2 transcript)
- **Data shortage claim** — kept but tagged as external industry context (Villalobos 2024), not a lecture assertion
- **SWE-rebench** — canonical spelling preserved with footnote that transcript has "sw-rebench"
- **Cross-entropy formula** — both forms documented (lecture shorthand vs. standard canonical form)
- **Sigmoid-as-anchor** — moved to the preference-optimization section where the transcript places it
- **Session 3** — host attribution corrected (Gaurav Sen hosts; Tanishk + Tanishq are co-instructors); not a Gaurav-led long-form lecture despite the volume of dialogue

Per-concept reading links were sourced from: [Vaswani 2017](https://arxiv.org/abs/1706.03762), [Jay Alammar](https://jalammar.github.io/), [Andrej Karpathy](https://www.youtube.com/@AndrejKarpathy), [3Blue1Brown](https://www.3blue1brown.com/), [HuggingFace NLP Course](https://huggingface.co/learn/llm-course), [Lilian Weng](https://lilianweng.github.io/), [Sebastian Raschka](https://sebastianraschka.com/), [Goodfellow — Deep Learning](https://www.deeplearningbook.org/), and the original papers for every algorithm cited.
