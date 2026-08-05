---
title: "N-gram vs LLM"
tags: [concept, architecture]
---

# N-gram vs LLM

**Category:** Architecture & Internals

## Definition

Both n-gram language models and LLMs compute `P(token_i | context)` — a conditional next-token probability. The difference is the **capacity** of the conditional:

- **N-gram model** estimates the conditional by counting how often each exact `(n−1)`-token context appeared in a corpus. Pure lookup, finite memory.
- **LLM** estimates the same conditional with a learned, deep neural transformation of the entire prior context. Generalises across compositional structure.

## Why It Matters

The shift from "memorise a lookup table" to "compose representations" is the entire reason modern NLP works. N-grams plateau at small context sizes (n ≥ 5 is already data-starved); LLMs generalise from much smaller corpora because they share statistical strength across similar contexts.

## Analogy

An n-gram is a parrot: it memorises phrases it has heard. An LLM is a linguist: it has heard fewer phrases but can recompose them on the fly. Both predict the next word, but the linguist handles a sentence it has never seen before.

## Visual

```mermaid
graph LR
    Corpus[Training corpus] --> Count["Count (n−1)-gram frequencies"]
    Count --> Table[Lookup table<br/>"the cat sat on the ___" → {mat: 0.4, dog: 0.1, ...}]
    Table --> Sample[Sample next token]
    Corpus --> Train[Train transformer]
    Train --> Weights[Learned weights<br/>billions of parameters]
    Weights --> Forward[Forward pass on full context]
    Forward --> Probs[Probability distribution]
    Probs --> Sample2[Sample next token]
```

## Lecture's take

**From [Session 1](../sessions/1-llm-basics.md):**

> Both do next-token prediction. **N-grams** use simple frequency counts; **LLMs** use massive learned transformations. Google has been doing vector-based next-token prediction since 2012.

## Mentioned In

- [LLM Basics & Transformer Internals](../sessions/1-llm-basics.md)

## Related Concepts

- [Next-Token Prediction](next-token-prediction.md)
- [Large Language Model (LLM)](large-language-model.md)

## Further Reading

- [Jurafsky & Martin — "Speech and Language Processing" Ch. 3 (online draft)](https://web.stanford.edu/~jurafsky/slp3/)
- [3Blue1Brown — "But what is a GPT?"](https://www.3blue1brown.com/lessons/gpt/)
