---
title: "2. Training Pipeline & Tool Use"
tags: [session, 2, training]
---

# 2. Training Pipeline & Tool Use

**Source:** [`transcripts/recording-52.srt`](../transcripts/recording-52.srt)
**Cohort:** AI Engineering Cohort (InterviewReady / Gaurav Sen)
**Instructor:** Speaker 1 (not Gaurav Sen — see "Speakers" below)
**Co-hosts:** Tanishk (IIT Bombay), Ariana (IIT Madras), Gaurav
**Duration:** 02:49:25
**Speakers:** 25 · **Segments:** 2559

> **Note on attribution.** Session 1's long-form instructor is Gaurav Sen (Speaker 0). In session 2 the transcript introduces "Gaurav" as a co-host separate from Speaker 1, so Session 2's long-form instructor is Speaker 1 (likely Tanishk or Ariana). Earlier versions mis-attributed session 2 to Gaurav Sen.

> **What this session is.** A teaching lecture that walks through the full LLM training pipeline: pre-training, SFT, tool calling, preference optimization, and model serving. Anchored by the framing "most of the intelligence is in pre-training; most of the behaviour in post-training."

## Speakers (per transcript)

| Role | Transcript ID | Notes |
|------|---------------|-------|
| Instructor | **Speaker 1** | Delivers the long-form teaching content |
| Co-host | "Tanishk" | IIT Bombay — AI engineer, healthcare-startup background |
| Co-host | "Ariana" | IIT Madras |
| Co-host | "Gaurav" | AI engineer (the Gaurav Sen of the cohort, separate from session 2's instructor) |
| Students | Speaker 2–25 | Various short questions and clarifications |

## Agenda

1. Pre-training (how a base model is built)
2. Post-training / Supervised Fine-Tuning (SFT)
3. Tool calling / function calls
4. Model serving
5. Survey of preference optimization algorithms (GRPO, DPO, PPO)

## The LLM Training Pipeline

```
Pre-training → Base Model → SFT → Format-Aligned Model → Preference Optimization → Final Model → Serving
```

| Stage | What happens | Output |
|-------|--------------|--------|
| **Pre-training** | Massive public datasets → tokenize → predict next token at every position → cross-entropy loss → backprop | Base model |
| **SFT** | Use-case-specific data → human-written input/output pairs → fine-tune | Format-aligned model |
| **Preference Optimization** | RLHF algorithms (GRPO, DPO, PPO) refine behavior using preference signals | Final model |
| **Serving** | Freeze weights → deploy to GPUs → inference | Running model |

> *"Most of the intelligence is here [pre-training]. Most of the behavior or the way of speaking, format, tone is built here [post-training]."*

## Concepts Covered

Each concept below has its own page with the canonical definition, analogy, Mermaid diagram, and the lecture's take quote.

### Training Pipeline

| Concept | One-line summary |
|---|---|
| [Pre-training](../concepts/pre-training.md) | First stage: predict next token over a huge corpus — where the model's "intelligence" lives. |
| [Data Pipeline](../concepts/data-pipeline.md) | Clone source data → filter → near-deduplicate → final training corpus. |
| [Fill-in-the-Blank Training](../concepts/fill-in-the-blank-training.md) | Each sentence = N training questions (one per token); masked attention makes this possible. |
| [Training Loop](../concepts/training-loop.md) | predict → cross-entropy loss → backprop → update every weight in the model. |
| [Cross-Entropy Loss](../concepts/cross-entropy-loss.md) | The objective: `−log(p_correct)` at every position. |
| [Supervised Fine-Tuning](../concepts/supervised-fine-tuning.md) | Format: (instruction, human-written answer) pairs — changes style, not capability. |
| [Preference Optimization](../concepts/preference-optimization.md) | RLHF family: GRPO (math/code, group ranking), DPO (direct pairs), PPO (original RLHF). |

### Capabilities & Trends

| Concept | One-line summary |
|---|---|
| [Tool Calling](../concepts/tool-calling.md) | LLMs can't call functions; they emit a textual template that a server parses and executes. |

### Inference & Optimization

| Concept | One-line summary |
|---|---|
| [Model Serving](../concepts/model-serving.md) | Frozen weights, GPU orchestration, KV-cache memory is the bottleneck. |
| [GPU Orchestration](../concepts/gpu-orchestration.md) | When a model doesn't fit one GPU, split by layer (pipeline parallelism). |
| [Data Shortage](../concepts/data-shortage.md) | Public text will saturate — frontier is curated corpora, synthetic data, inference-time compute. |

## Mermaid Summary

```mermaid
graph LR
    A[Public Datasets] --> B[Tokenize]
    B --> C[Pre-training]
    C --> D[Base Model]
    D --> E[SFT]
    E --> F[Format Model]
    F --> G[Preference Opt]
    G --> H[Final Model]
    H --> I[Freeze + Serve]
    I --> J[User Queries]
```

## Q&A Highlights

| Question | Answer |
|----------|--------|
| Does SFT involve manual annotation? | The output is human-written once, but losses are computed automatically. |
| How do you penalize on tokens with little context? | Deferred — model still gets a loss signal at every position. |
| What is the input/output size of the transformer? | N × D throughout; final linear: N × D → N × \|vocab\|. |
| How does tool calling actually work? | Model outputs a token template; server interprets; result appended to prompt. |
| What are modern preference optimization algorithms? | GRPO (DeepSeek, math/code), DPO, PPO. Sigmoid is the conceptual anchor. |
| Why input tokens > output tokens? | Apps pass documents, search results, page contents as input. |

## Homework / Next Steps

- **Paper on preference optimization** (GRPO/DPO/PPO) — see links in the [Preference Optimization](../concepts/preference-optimization.md) page.
- **Next Sunday:** Coding session — bring laptops, Google Colab links will be shared
- Roadmap: Pre-training → **Fine-tuning** (next week) → RAG → Agents → Capstone project

## Key Takeaways

1. **LLM training = pre-training + post-training + serving**
2. **Pre-training:** tokenize massive data, predict next token at every position, cross-entropy loss
3. **SFT:** human-written QA pairs for format/tone/jargon
4. **Tool calling is a textual convention** — the model emits tokens; the server interprets
5. **Preference optimization** refines behavior with reward signals (GRPO, DPO, PPO)
6. **Model serving** freezes weights; KV cache and vocabulary are key knobs for cost/performance

## Related Materials

- 📄 Raw transcript: [`transcripts/recording-52.srt`](../transcripts/recording-52.srt)
- 🕸️ Knowledge graph (visual): [`sessions/2-training-pipeline-graph.md`](2-training-pipeline-graph.md)
- 🧠 Knowledge graph (JSON): [`sessions/2-training-pipeline-graph.json`](2-training-pipeline-graph.json)
- 🌐 Combined view across all sessions: [`sessions/combined-knowledge-graph.md`](combined-knowledge-graph.md)
- 🌱 Browse concepts: [`../concepts/index.md`](../concepts/index.md)
