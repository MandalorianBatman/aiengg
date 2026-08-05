---
title: "Next-Token Prediction"
tags: [concept, architecture]
---

# Next-Token Prediction

**Category:** 

## Definition

The fundamental objective of an LLM. Given an input sequence, predict the most likely next token. The output becomes part of the next input — this is *autoregressive generation*.

**Example:** All that glitters → is → not → gold → .

## Why It Matters

This is the *only* thing an LLM does. Every capability — reasoning, tool calling, code generation — is emergent from next-token prediction. Understanding this constraint explains both the power and the limitations of LLMs.

## Analogy

Like a GPS that only tells you the next turn. You get from Delhi to Mumbai one turn at a time — the GPS never "plans" the whole route, it just predicts the next step given where you are. LLMs write entire essays the same way: one token at a time.

## Mentioned In

[LLM Basics & Transformer Internals](../sessions/1-llm-basics.md)

## Related Concepts

- [Large Language Model](large-language-model.md)
- [Cross-Entropy Loss](cross-entropy-loss.md)
- [Temperature](temperature.md)

## Further Reading

- [The Autoregressive Universe (Lilian Weng)](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/)
- [GPT in 60 Lines of NumPy (Jay Mody)](https://jaykmody.com/blog/gpt-from-scratch/)
