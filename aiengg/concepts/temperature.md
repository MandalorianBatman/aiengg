---
title: "Temperature / Sampling"
tags: [concept, inference]
---

# Temperature / Sampling

**Category:** 

## Definition

Strategies for picking from the output probability distribution. Greedy decoding always picks the highest-probability token (deterministic, boring). Temperature scales the distribution: high temperature (>1) flattens it (more random), low temperature (<1) sharpens it (more deterministic).

**Top-k:** Only consider the top k tokens. **Top-p (nucleus):** Consider tokens until cumulative probability ≥ p.

## Why It Matters

Temperature is the primary knob for controlling creativity vs. reliability. Code generation uses low temperature (0-0.3). Creative writing uses higher (0.7-1.0). An API that gives identical responses every time is likely using temperature=0.

## Analogy

Temperature is like the 'creativity slider' on a music app. At 0, it plays the most predictable note every time (boring but correct). At 1, it occasionally surprises you. At 2, it plays jazz.

## Mentioned In

[LLM Basics & Transformer Internals](../sessions/1-llm-basics.md)

## Related Concepts

- [Next-Token Prediction](next-token-prediction.md)
- [Large Language Model](large-language-model.md)
- [Linear Layer](linear-layer.md)

## Further Reading

- [How to generate text (HuggingFace)](https://huggingface.co/blog/how-to-generate)
- [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751)
