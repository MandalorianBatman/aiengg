# KV Cache

**Category:** 

## Definition

Memoization of Key and Value vectors for previously-seen tokens. When generating new tokens, the model reuses precomputed K and V vectors instead of recomputing the entire N×N attention matrix from scratch.

**Tradeoff:** Saves massive compute (avoids O(N²) recomputation) but is memory-expensive — must store K and V for every token in the context.

## Why It Matters

KV cache is what makes LLM inference practical. Without it, generating a 100-token response to a 1000-token prompt would be prohibitively slow. Every production LLM serving system uses KV caching.

## Analogy

KV cache is like pre-computed answers in a textbook. If you're solving math problems and the book already shows that 7×8=56 in the margin, you don't recompute it every time a problem uses 7×8. You just look it up. The cache stores these 'lookups' — trading memory for speed.

## Mentioned In

[LLM Basics & Transformer Internals](../sessions/llm-basics-transformer-internals.md), [Training Pipeline & Tool Use](../sessions/llm-training-pipeline-tool-use.md)

## Related Concepts

- [Attention](attention.md)
- [Context Window](context-window.md)
- [Model Serving](model-serving.md)

## Further Reading

- [KV Cache explained (HuggingFace)](https://huggingface.co/blog/kv-cache-quantization)
- [vLLM: PagedAttention](https://arxiv.org/abs/2309.06180)
