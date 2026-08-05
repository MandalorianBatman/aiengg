---
title: "Feed-Forward Network (FFN)"
tags: [concept, architecture]
---

# Feed-Forward Network (FFN)

**Category:** 

## Definition

A per-token block inside the transformer that maps D-dimensional vectors to 4D then back to D. Transforms features into more useful features without changing the shape.

**Example from lecture:** Length × breadth = area; ratio of length/breadth. New features derived from old ones.

## Why It Matters

Attention mixes information *between* tokens. The FFN processes each token *individually*, building higher-level features. Together they give the transformer both horizontal (across tokens) and vertical (within a token) processing.

## Analogy

If attention is like asking your teammates for their notes (cross-referencing), the FFN is like sitting alone and deriving insights from the notes you now have — transforming raw data into useful abstractions.

## Lecture's take

**From [Session 1](../sessions/1-llm-basics.md):**

> A per-token block that maps 8192-D → 8192-D but with transformed values. **Analogy:** Just like deriving "area" from "length × breadth" or "ratio" from "length / breadth", the FFN builds new features from old ones. > *"These don't have new information. They are just a transformation, a mapping of our existing features into more useful features."*

## Mentioned In

- [LLM Basics & Transformer Internals](../sessions/1-llm-basics.md)
- [Week 1 Doubts & Networking](../sessions/3-week-1-doubts.md)

## Related Concepts

- [Transformer](transformer.md)
- [Attention](attention.md)
- [Linear Layer](linear-layer.md)

## Further Reading

- [Transformer Feed-Forward Layers (J. Alammar)](https://jalammar.github.io/illustrated-gpt2/)
- [SwiGLU and variants](https://arxiv.org/abs/2002.05202)
