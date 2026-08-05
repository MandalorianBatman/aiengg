---
title: "Large Language Model (LLM)"
tags: [concept, architecture]
---

# Large Language Model (LLM)

**Category:** 

## Definition

A neural network trained to predict the next token of an input sequence. Built as a stack of transformer blocks. When you hear "LLM", think "transformer-stack predicting the next token autoregressively."

## Why It Matters

Everything in AI engineering builds on this foundation. Understanding what an LLM actually *is* (not what it appears to be) is the prerequisite for understanding training, fine-tuning, serving, and tool calling.

## Analogy

An LLM is like an extremely well-read friend who, when you hand them a partially-written sentence, can complete it convincingly. They don't "know" facts — they've internalized patterns from reading everything. Ask them "The capital of France is" and they complete "Paris" not because they looked it up, but because they've seen that pattern thousands of times.

## Mentioned In

- [LLM Basics & Transformer Internals](../sessions/1-llm-basics.md)
- [Training Pipeline & Tool Use](../sessions/2-training-pipeline.md)
- [Week 1 Networking — Doubt-Solving](../sessions/3-week-1-doubts.md)

## Related Concepts

- [Byte Pair Encoding](byte-pair-encoding.md)
- [Attention](attention.md)
- [Transformer](transformer.md)
- [Context Window](context-window.md)

## Further Reading

- [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762)
- [The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/)
- [Intro to Large Language Models (Karpathy, 1hr)](https://www.youtube.com/watch?v=zjkBMFhNj_g)
