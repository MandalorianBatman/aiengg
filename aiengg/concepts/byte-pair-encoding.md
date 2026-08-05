---
title: "Byte Pair Encoding (BPE)"
tags: [concept, architecture]
---

# Byte Pair Encoding (BPE)

**Category:** 

## Definition

A tokenization algorithm that splits text into sub-word tokens. Starts with individual characters, then repeatedly merges the most frequent adjacent pairs. Sub-word units like 'coro' + 'nation' are meaningless in isolation but optimized for LLM consumption.

**Examples from the lecture:** coronation → coro + nation, legal → leg + al

## Why It Matters

BPE is the most common tokenization algorithm used by modern LLMs (GPT, Llama, etc.). It solves the vocabulary size tradeoff: too few tokens = lose information, too many = bloated computation. Sub-word tokenization hits the sweet spot.

## Analogy

Think of BPE like a compression algorithm for language. Instead of storing every word ("running", "runs", "run") separately, it learns common pieces ("run", "ning", "s"). This way it can represent any word, even ones it's never seen before, from known pieces.

## Mentioned In

- [LLM Basics & Transformer Internals](../sessions/1-llm-basics.md)
- [Week 1 Networking — Doubt-Solving](../sessions/3-week-1-doubts.md)

## Related Concepts

- [Token](token.md)
- [Vocabulary](vocabulary.md)
- [Large Language Model](large-language-model.md)

## Further Reading

- [BPE paper (Sennrich et al., 2016)](https://arxiv.org/abs/1508.07909)
- [Tokenization in LLMs (HuggingFace)](https://huggingface.co/learn/nlp-course/chapter6/1)
