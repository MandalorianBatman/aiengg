# Supervised Fine-Tuning (SFT)

**Category:** 

## Definition

The second stage of LLM training. Use-case-specific data (sales calls, medical transcripts, coding tasks) in input-output pairs. The model learns format, tone, and jargon — 'most of the behavior is here.'

**Data format:** Input (instruction) + Output (human-written answer). The human writes the answer once; losses are computed automatically.

**What changes:** Tone, format, domain jargon. The core intelligence from pre-training is preserved.

## Why It Matters

SFT bridges the gap between 'knowing things' and 'being helpful.' A base model can complete sentences but can't follow instructions. SFT makes it conversational. It's also where domain-specific behavior is installed.

## Analogy

Pre-training gives you a brilliant PhD graduate who's read everything. SFT is like hiring them as a customer service agent — you train them on your specific product, your company's tone, and how to format responses for your CRM system. Same intelligence, different behavior.

## Mentioned In

- [Training Pipeline & Tool Use](../sessions/llm-training-pipeline-tool-use.md)
- [Week 1 Networking — Doubt-Solving](../sessions/doubts-networking-week-1.md)

## Related Concepts

- [Pre-training](pre-training.md)
- [Base Model](base-model.md)
- [Preference Optimization](preference-optimization.md)
- [Post-Training](post-training.md)

## Further Reading

- [InstructGPT paper (OpenAI, 2022)](https://arxiv.org/abs/2203.02155)
- [SFT best practices (Anthropic)](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
