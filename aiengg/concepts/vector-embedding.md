---
title: "Vector (Embedding)"
tags: [concept, architecture]
---

# Vector (Embedding)

**Category:** 

## Definition

A coordinate in a multi-dimensional space assigned to each token. Each token is represented as a vector of numbers (e.g., 768 numbers in GPT-2, 8192 in modern models). Each dimension conceptually represents a 'feature' the model has learned.

**Dimension examples:** 768 (GPT-2), 8192 (modern large models)

## Why It Matters

Embeddings are how LLMs represent meaning mathematically. Words that are semantically similar have vectors that are close together in this space. This is the bridge between human language and machine computation.

## Analogy

Imagine a map where every word is a city. "King" and "Queen" are close together (royalty region). "Paris" and "France" are nearby (geography region). But the trick is: king − man + woman ≈ queen. The directions *between* cities encode relationships. An embedding space works the same way: the vector difference captures meaning.

## Lecture's take

**From [Session 1](../sessions/1-llm-basics.md):**

> A coordinate in a multi-dimensional space assigned to each token. Common dimensions: **768, 8192**. Each dimension is conceptually a "feature" the model has learned (e.g., "how south is this city from Delhi"). In reality, the model is just predicting the next token — we don't know what each dimension truly represents.

## Mentioned In

- [LLM Basics & Transformer Internals](../sessions/1-llm-basics.md)
- [Week 1 Doubts & Networking](../sessions/3-week-1-doubts.md)

## Related Concepts

- [Token](token.md)
- [Attention](attention.md)
- [Transformer](transformer.md)

## Further Reading

- [Word Embeddings (3Blue1Brown)](https://www.youtube.com/watch?v=wjZofJX0v4M)
- [The Illustrated Word2vec (Jay Alammar)](https://jalammar.github.io/illustrated-word2vec/)
