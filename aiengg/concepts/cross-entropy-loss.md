# Cross-Entropy Loss

**Category:** 

## Definition

The loss function used in LLM training. Measures how far the model's prediction is from the correct answer.

**Formula:** Loss = −log(p_correct). If the model assigns probability 1.0 to the correct token → loss = 0. If it assigns near-zero probability → loss → ∞. The term 'cross-entropy' comes from information theory: it measures the 'surprise' of seeing the correct answer given the model's predictions.

**Sigmoid (conceptual anchor):** Used in class as teaching tool. Sigmoid of +20 ≈ 1, sigmoid of −20 ≈ 0. In production, modern algorithms (GRPO, DPO, PPO) replace this.

## Why It Matters

Loss is the signal that drives all learning. Every weight update during training is trying to reduce this number. Understanding loss helps you debug training (loss not decreasing = something wrong), detect overfitting, and interpret training curves.

## Analogy

Cross-entropy loss is like a strict teacher grading your exam. If you say 'I'm 100% sure the answer is Paris' and it IS Paris → perfect score. If you say 'I'm 100% sure it's London' but the answer is Paris → you fail catastrophically. The loss penalizes confidence in wrong answers much more than uncertainty.

## Mentioned In

- [Training Pipeline & Tool Use](../sessions/llm-training-pipeline-tool-use.md)
- [Week 1 Networking — Doubt-Solving](../sessions/doubts-networking-week-1.md)

## Related Concepts

- [Training Loop](training-loop.md)
- [Fill-in-the-Blank Training](fill-in-the-blank-training.md)
- [Pre-training](pre-training.md)

## Further Reading

- [Cross-Entropy explained (towardsdatascience)](https://towardsdatascience.com/cross-entropy-loss-function-f38c4ec8643e)
- [Deep Learning Book, Ch. 6 (Goodfellow)](https://www.deeplearningbook.org/contents/mlp.html)
