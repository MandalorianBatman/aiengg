# Token

**Category:** 

## Definition

A unit of text (word or sub-word) that an LLM consumes and produces. Input text is split into tokens before being passed to the model. Tokens are the atomic unit of LLM computation.

**Example:** "coronation" might split into "coro" + "nation".

## Why It Matters

Tokens determine cost and context. Every API call is priced per token (input + output). The context window is measured in tokens. Understanding tokenization explains why LLMs struggle with certain tasks (counting letters, reversing strings) — they see tokens, not characters.

## Analogy

Tokens are like LEGO bricks for language. "Unbelievable" might need 3 bricks (un + believ + able), while "cat" is just 1 brick. A sentence that's 10 words might be 15 tokens. The model builds meaning from these bricks, not from individual letters.

## Mentioned In

- [LLM Basics & Transformer Internals](../sessions/llm-basics-transformer-internals.md)
- [Week 1 Networking — Doubt-Solving](../sessions/doubts-networking-week-1.md)

## Related Concepts

- [Byte Pair Encoding](byte-pair-encoding.md)
- [Vector (Embedding)](vector-embedding.md)
- [Vocabulary](vocabulary.md)

## Further Reading

- [OpenAI Tokenizer](https://platform.openai.com/tokenizer) — interactive visualizer
- [BPE paper (Sennrich et al., 2016)](https://arxiv.org/abs/1508.07909)
