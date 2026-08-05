---
title: "Linear Layer (Unembedding / LM Head)"
tags: [concept, architecture]
---

# Linear Layer (Unembedding / LM Head)

**Category:** Architecture & Internals

## Definition

The final linear layer `W_U ∈ ℝ^{D × |V|}` that maps each contextualized D-dimensional vector to a logit over the entire vocabulary. A softmax over those logits gives the next-token probability distribution. Also called the **LM head** or **unembedding matrix**.

## Why It Matters

The unembedding matrix is one of the two largest weight matrices in the model (the other is the embedding matrix). Together they account for a substantial fraction of total parameters. **Weight tying** — sharing the unembedding matrix with the embedding matrix — halves this cost with minimal quality loss and is standard practice.

## Analogy

The unembedding is the voting step. Each token's contextualized vector casts a vote over every possible next word, weighted by how compatible it is with that word. The softmax picks the winner.

## Visual

```mermaid
graph LR
    Hidden[Hidden state<br/>N × D] --> W_U["W_U<br/>D × |V|"]
    W_U --> Logits[Logits<br/>N × |V|]
    Logits --> LastPos[Take last row]
    LastPos --> Softmax[softmax]
    Softmax --> Probs[Probability over vocab<br/>1 × |V|]
    Probs --> Sample[Sample / argmax]
    Sample --> Token[Next token ID]
```

## Lecture's take

**From [Session 1](../sessions/1-llm-basics.md):**

> The final linear layer maps the contextualized N × D vectors to N × \|vocab\| probabilities. The argmax (or sample) over the row at the last position is the predicted next token.

## Mentioned In

- [LLM Basics & Transformer Internals](../sessions/1-llm-basics.md)

## Related Concepts

- [Vocabulary](vocabulary.md)
- [Next-Token Prediction](next-token-prediction.md)
- [Transformer](transformer.md)

## Further Reading

- [Jay Alammar — "Illustrated GPT-2"](https://jalammar.github.io/illustrated-gpt2/)
- [Sebastian Raschka — "Build a Large Language Model (From Scratch)" — LM head chapter](https://www.manning.com/books/build-a-large-language-model-from-scratch)
