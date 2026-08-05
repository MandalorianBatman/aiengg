---
title: "Pre-training Data Pipeline"
tags: [concept, training]
---

# Pre-training Data Pipeline

**Category:** 

## Definition

The process of preparing training data for pre-training. Steps: clone data sources → filter by license, file type, quality → near-deduplicate (remove copies) → tokenize into the model's vocabulary → feed into training.

**Case study — BigCode:** 220 million GitHub repositories → 102 TB raw → 30% file-type filter → 6.4 TB post-license/dedupe → 3 TB final dataset.

## Why It Matters

Data quality determines model quality. Garbage in = garbage out. The data pipeline is often the most engineering-intensive part of LLM development — more than the model architecture itself. Teams spend months on data filtering and deduplication.

## Analogy

The data pipeline is like preparing ingredients for a massive banquet. You don't just dump everything from the market into the pot. You sort (filter), remove duplicates (someone sent the same ingredient twice), wash and chop (tokenize), and only then cook. The quality of the meal depends more on ingredient prep than on the stove.

## Lecture's take

**From [Session 2](../sessions/2-training-pipeline.md):**

> Clone source data (GitHub archive for code, web crawls for text), filter out low-quality or unlicensed files, near-deduplicate near-copies, and the resulting corpus trains the transformer. Worked example: BigCode — 220M GitHub repos → 102 TB → ~30% keep → 6.4 TB after file selection → license filter + near-dedup → 3 TB final.

## Mentioned In

- [Training Pipeline & Tool Use](../sessions/2-training-pipeline.md)
- [Week 1 Networking — Doubt-Solving](../sessions/3-week-1-doubts.md)

## Related Concepts

- [Pre-training](pre-training.md)
- [Fill-in-the-Blank Training](fill-in-the-blank-training.md)
- [Data Shortage](data-shortage.md)

## Further Reading

- [Dolma: 3 Trillion Token Corpus (Allen AI)](https://arxiv.org/abs/2402.00159)
- [Datacomp for language models](https://arxiv.org/abs/2308.08980)
