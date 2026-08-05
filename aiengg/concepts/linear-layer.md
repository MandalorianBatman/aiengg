---
title: "Linear Layer (Unembedding / LM Head)"
tags: [concept, architecture]
---

# Linear Layer (Unembedding / LM Head)

**Category:** 

## Definition

The final layer of the transformer. Maps the D-dimensional vector (e.g., 8192-D) into a probability distribution over the entire vocabulary (e.g., 40,000 tokens). Output: N × vocabulary_size probabilities — one probability per token in the vocabulary.

## Why It Matters

This is the bridge between internal computation and human-readable output. The model doesn't output text — it outputs a probability for every word in its vocabulary, and we pick one.

## Analogy

The linear layer is like a translator at the UN. The transformer does its work in a high-dimensional 'machine language' (8192 numbers). The linear layer translates that into probabilities for every word the model knows — like the translator converting diplomatic nuance into the word most likely to convey it.

## Mentioned In

[LLM Basics & Transformer Internals](../sessions/1-llm-basics.md)

## Related Concepts

- [Vocabulary](vocabulary.md)
- [Transformer](transformer.md)
- [Temperature](temperature.md)

## Further Reading

- [The GPT Architecture (Jay Mody)](https://jaykmody.com/blog/gpt-from-scratch/)
