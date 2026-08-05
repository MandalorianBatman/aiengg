---
title: "Model Parameters"
tags: [concept, architecture]
---

# Model Parameters

**Category:** 

## Definition

The numbers stored in the weight matrices — 'what is stored on disk' when you download a model. Every Q, K, V matrix, every feed-forward weight, every embedding — these are all parameters. A 7B parameter model literally has 7 billion numbers.

**Not in the lecture but relevant:** Parameters are typically stored as 16-bit floats (FP16/BF16), so a 7B model ≈ 14 GB on disk.

## Why It Matters

Parameter count is the first number you see on HuggingFace. It's a rough proxy for capability but doesn't tell the whole story — architecture, training data quality, and post-training matter enormously. A well-trained 7B can beat a poorly-trained 70B.

## Analogy

Parameters are like the coefficients in a giant polynomial. A 7-billion-parameter model is like a 7-billion-term equation. More terms = more nuance it can express, but also more to store and compute.

## Mentioned In

- [LLM Basics & Transformer Internals](../sessions/1-llm-basics.md)
- [Week 1 Doubts & Networking](../sessions/3-week-1-doubts.md)

## Related Concepts

- [Large Language Model](large-language-model.md)
- [Pre-training](pre-training.md)
- [Transformer](transformer.md)

## Further Reading

- [Chinchilla scaling laws (Hoffmann et al., 2022)](https://arxiv.org/abs/2203.15556)
- [Model sizes across vendors](https://huggingface.co/models)
