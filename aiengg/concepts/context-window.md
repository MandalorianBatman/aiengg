---
title: "Context Window"
tags: [concept, inference]
---

# Context Window

**Category:** 

## Definition

The number of tokens the model can attend to at once. Each token's vector gets context from every other token in the window, making the cost O(N²). Larger context = dramatically more compute.

**Extreme example:** 1M token context means 1M × 1M = 1 trillion attention computations per token.

## Why It Matters

Context window is the defining constraint for LLM applications. It determines how much document/code/conversation you can include. The quadratic cost means doubling the window quadruples the compute — this is why KV caching is critical.

## Analogy

A context window is like the size of your desk. A small desk = you can only work with a few pages at once. A huge desk = you can spread out an entire book, but it costs more (bigger room, more lights). KV cache is like keeping your place with sticky notes so you don't have to re-read everything each time you add a new page.

## Lecture's take

**From [Session 1](../sessions/1-llm-basics.md):**

> The number of tokens the model can attend to. **1M context ≠ 1M tokens of info** — every token gets context from the remaining 1M tokens, and this happens 1M times. Dramatic compute cost.

## Mentioned In

- [LLM Basics & Transformer Internals](../sessions/1-llm-basics.md)
- [Training Pipeline & Tool Use](../sessions/2-training-pipeline.md)
- [Week 1 Networking — Doubt-Solving](../sessions/3-week-1-doubts.md)

## Related Concepts

- [KV Cache](kv-cache.md)
- [Attention](attention.md)
- [Input vs Output Tokens](input-vs-output-tokens.md)

## Further Reading

- [Extending Context Windows (Lilian Weng)](https://lilianweng.github.io/posts/2023-10-05-context-eval/)
- [FlashAttention paper](https://arxiv.org/abs/2205.14135)
