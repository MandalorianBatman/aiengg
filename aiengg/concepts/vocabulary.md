# Vocabulary

**Category:** 

## Definition

The set of all tokens the model knows. The output probability distribution has one probability per vocabulary token. Typical sizes: 20k (early models), 50k (GPT-2), 100k+ (modern models). Smaller vocabulary = cheaper to compute the final linear layer.

## Why It Matters

Vocabulary size is a key hyperparameter with real cost implications. The final linear layer maps D → |V|, so a larger vocabulary means more parameters and more compute. But too small a vocabulary means more tokens per sentence (higher cost per text).

## Analogy

Vocabulary size is like the number of keys on a keyboard. More keys = more expressive (you can type in more languages) but the keyboard is bigger and harder to carry. Too few keys = you need multiple keystrokes per character (like old SMS texting).

## Mentioned In

- [LLM Basics & Transformer Internals](../sessions/llm-basics-transformer-internals.md)
- [Training Pipeline & Tool Use](../sessions/llm-training-pipeline-tool-use.md)
- [Week 1 Networking — Doubt-Solving](../sessions/doubts-networking-week-1.md)

## Related Concepts

- [Token](token.md)
- [Byte Pair Encoding](byte-pair-encoding.md)
- [Linear Layer](linear-layer.md)

## Further Reading

- [OpenAI Tokenizer](https://platform.openai.com/tokenizer)
- [SentencePiece paper](https://arxiv.org/abs/1808.06226)
