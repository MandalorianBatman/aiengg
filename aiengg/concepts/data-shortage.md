---
title: "Data Shortage"
tags: [concept, training]
---

# Data Shortage

**Category:** 

## Definition

The observation that we are approaching (or have reached) the limit of publicly available high-quality training data. Models are being trained on trillions of tokens — close to the total amount of public text on the internet.

**Future options:** Synthetic data generation (models creating training data for other models), social media data (lower quality), robotics interaction data (new modality), video/audio transcription (untapped but noisy).

## Why It Matters

Data shortage is reshaping the economics of AI. The next frontier isn't better architectures — it's better data. Companies with proprietary data moats (Google Search, Meta social graph, GitHub code) have an advantage. Synthetic data is the most promising path forward but has quality and diversity challenges.

## Analogy

Pre-training is like a library. For years, models could browse new shelves (public data). Now they've read almost everything. The next phase is either writing new books themselves (synthetic data) or finding new libraries (private data, video transcripts, robot interactions).

## Lecture's take

**From [Session 2](../sessions/2-training-pipeline.md):**

> Not asserted in R52 — earlier versions of these notes added it as a takeaway. The "running out of public training data" framing is current industry knowledge (Epoch AI, 2024), not part of the lecture. Listed here for completeness and linked to the source.

## Mentioned In

[Training Pipeline & Tool Use](../sessions/2-training-pipeline.md)

## Related Concepts

- [Pre-training](pre-training.md)
- [Data Pipeline](data-pipeline.md)
- [Fill-in-the-Blank Training](fill-in-the-blank-training.md)

## Further Reading

- [Will We Run Out of Data? (Villalobos et al., 2024)](https://arxiv.org/abs/2211.04325)
- [Synthetic Data for LLMs](https://arxiv.org/abs/2401.12849)
