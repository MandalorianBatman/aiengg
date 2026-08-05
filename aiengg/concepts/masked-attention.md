---
title: "Masked Attention (Causal Masking)"
tags: [concept, architecture]
---

# Masked Attention (Causal Masking)

**Category:** 

## Definition

Masks the upper triangle of the attention similarity matrix so each token can only attend to itself and previous tokens — not future tokens. This is called 'causal' masking because the future cannot cause the present.

**Why it matters for training:** A sentence of N tokens gives N training signals (predict token 2 from token 1, token 3 from tokens 1-2, etc.) instead of just 1.

## Why It Matters

Masked attention is what makes LLM pre-training efficient. Without it, you'd get one training signal per sentence. With it, you get N signals — the entire backbone of fill-in-the-blank training.

## Analogy

Like a test where you can't look ahead. On question 5, you can use what you learned from questions 1-4, but you can't peek at question 6. The model learns to predict at every position using only what came before — which is exactly what it needs to do at inference time.

## Visual

```mermaid
graph TD
    T1[Token 1: The] --> P2[Predict 2]
    T2[Token 2: cat] --> P3[Predict 3]
    T3[Token 3: sat] --> P4[Predict 4]
    P2 --> M1[Mask: only see 1]
    P3 --> M2[Mask: only see 1-2]
    P4 --> M3[Mask: only see 1-3]
```

## Lecture's take

**From [Session 1](../sessions/1-llm-basics.md):**

> The upper triangle of the similarity matrix is masked — tokens can't look ahead. **Why?** Because masking turns one sentence into **N training pairs** (one per token), not just one. With N tokens, you get N predictions and N places to compute loss.

## Mentioned In

[LLM Basics & Transformer Internals](../sessions/1-llm-basics.md), [Training Pipeline & Tool Use](../sessions/2-training-pipeline.md)

## Related Concepts

- [Attention](attention.md)
- [Fill-in-the-Blank Training](fill-in-the-blank-training.md)
- [Training Loop](training-loop.md)

## Further Reading

- [The Annotated Transformer (Harvard NLP)](https://nlp.seas.harvard.edu/annotated-transformer/)
- [Causal Attention explained](https://sebastianraschka.com/blog/2023/self-attention-from-scratch.html)
