---
title: "Input vs Output Tokens"
tags: [concept, architecture]
---

# Input vs Output Tokens

**Category:** 

## Definition

Input tokens = context the model receives (documents, search results, conversation history). Output tokens = what the model generates. In typical applications, input tokens > output tokens (you send a 2000-word document and get a 100-word summary).

**Pricing:** Most APIs charge more for output tokens because they're generated sequentially (expensive) while input tokens can be processed in parallel.

## Why It Matters

Understanding the input/output split is critical for cost estimation and prompt engineering. Every token you include in your prompt costs money. Every token the model generates also costs money. For RAG applications, input tokens dominate.

## Analogy

Input tokens are like the ingredients you give a chef. Output tokens are the dish they prepare. You pay for both — the ingredients (just scanning them) and the cooking (the actual work of generating each new token).

## Lecture's take

**From [Session 1](../sessions/1-llm-basics.md):**

> **Input tokens** are the context the model receives (docs, search results, chat history); **output tokens** are what the model generates. In typical apps, input tokens > output tokens.

## Mentioned In

[LLM Basics & Transformer Internals](../sessions/1-llm-basics.md)

## Related Concepts

- [Token](token.md)
- [Context Window](context-window.md)
- [KV Cache](kv-cache.md)

## Further Reading

- [OpenAI pricing](https://openai.com/pricing)
- [Anthropic pricing](https://www.anthropic.com/pricing)
