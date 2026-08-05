---
title: "GPU Orchestration"
tags: [concept, inference]
---

# GPU Orchestration

**Category:** 

## Definition

When an LLM is too large to fit on a single GPU, its layers are distributed across multiple GPUs. An orchestrator manages the flow: forward pass across GPUs in sequence, backward pass in reverse (for training), and result aggregation.

**Pipeline parallelism:** GPU-1 stores and runs layers 1-10, GPU-2 stores 11-20, etc. Data flows sequentially through the pipeline.

## Why It Matters

GPU orchestration is what makes large models possible. A 70B parameter model in FP16 is ~140 GB — far larger than any single GPU's memory (H100: 80 GB). Without orchestration, models above ~30B parameters couldn't run at all.

## Analogy

GPU orchestration is like an assembly line. One worker (GPU) can't build a car alone — it won't fit in their workspace. So the car chassis moves from station to station: Station 1 installs the engine (layers 1-10), Station 2 adds the body (layers 11-20), Station 3 does the interior (layers 21-32). Each station only needs to know its own part.

## Lecture's take

**From [Session 2](../sessions/2-training-pipeline.md):**

> When a model is too large for one GPU, split it across GPUs by layer. An orchestrator passes data between GPUs, layer by layer.

## Mentioned In

- [Training Pipeline & Tool Use](../sessions/2-training-pipeline.md)
- [Week 1 Doubts & Networking](../sessions/3-week-1-doubts.md)

## Related Concepts

- [Model Serving](model-serving.md)
- [Transformer](transformer.md)
- [KV Cache](kv-cache.md)

## Further Reading

- [Model Parallelism (HuggingFace)](https://huggingface.co/docs/transformers/v4.15.0/en/parallelism)
- [ZeRO: Memory Optimizations (DeepSpeed)](https://arxiv.org/abs/1910.02054)
