---
title: "Recording 52 — LLM Training Pipeline, Tool Use & Fine-Tuning"
tags: [session, r52, training]
---

# Recording 52 — LLM Training Pipeline, Tool Use & Fine-Tuning

**Source:** [`transcripts/recording-52.srt`](transcripts/recording-52.srt)
**Cohort:** AI Engineering Cohort (InterviewReady / Gaurav Sen)
**Instructor:** Speaker 1 (not Gaurav Sen — see "Speakers" below)
**Co-hosts:** Tanishk (IIT Bombay), Ariana (IIT Madras), Gaurav
**Duration:** 02:49:25
**Speakers:** 25 · **Segments:** 2559

> **Note on attribution.** The R51 lecture has Gaurav Sen as the long-form instructor (Speaker 0). In R52 the transcript introduces "Gaurav" as a co-host separate from Speaker 1, so the long-form instructor of R52 is Speaker 1 (likely Tanishk or Ariana). The earlier version of these notes mis-attributed R52 to Gaurav Sen.

## Speakers (per transcript)

| Role | Transcript ID | Notes |
|------|---------------|-------|
| Instructor | **Speaker 1** | Delivers the long-form teaching content |
| Co-host | "Tanishk" | IIT Bombay — AI engineer, healthcare-startup background |
| Co-host | "Ariana" | IIT Madras |
| Co-host | "Gaurav" | AI engineer (the Gaurav Sen of the cohort, separate from the R52 instructor) |
| Students | Speaker 2–25 | Various short questions and clarifications |

## Agenda

1. Pre-training (how a base model is built)
2. Post-training / Supervised Fine-Tuning (SFT)
3. Tool calling / function calls
4. Model serving
5. Survey of preference optimization algorithms (GRPO, DPO, PPO)

## The LLM Training Pipeline

```
Pre-training → Base Model → SFT → Format-Aligned Model → Preference Optimization → Final Model → Serving
```

| Stage | What happens | Output |
|-------|--------------|--------|
| **Pre-training** | Massive public datasets → tokenize → predict next token at every position → cross-entropy loss → backprop | Base model |
| **SFT** | Use-case-specific data (e.g., sales calls) → human-written input/output pairs → fine-tune | Format-aligned model |
| **Preference Optimization** | RLHF algorithms (GRPO, DPO, PPO) refine behavior using preference signals | Final model |
| **Serving** | Freeze weights → deploy to GPUs → inference | Running model |

> *"Most of the intelligence is here [pre-training]. Most of the behavior or the way of speaking, format, tone is built here [post-training]."*

## Pre-training in Detail

### Pre-training
> **Lecture's take:** The first training stage. The model sees a massive corpus of public text, predicts the next token at every position, takes the cross-entropy loss, back-propagates, and updates its weights. This is where the model's "intelligence" — language, grammar, world knowledge — comes from.

**Canonical definition.** Pre-training is the initial, self-supervised training pass over a huge corpus, with the only objective being next-token prediction. Once finished, the resulting **base model** can complete text but does not yet follow instructions or chat reliably.

**Key insight.** Pre-training is by far the most compute-expensive stage — easily 90%+ of the total training FLOPs. Post-training is cheap by comparison. This is also why almost all the "intelligence" of an LLM is locked in at this stage: post-training mostly teaches *style*, *format*, and *alignment*, not new knowledge.

**📚 Further reading**
- [Ouyang et al., 2022 — "Training language models to follow instructions with human feedback"](https://arxiv.org/abs/2203.02155) — *the InstructGPT paper; positions pre-training vs. post-training cleanly.*
- [Sebastian Raschka — "LLM Training and Evaluation" (blog, Dec 2023)](https://sebastianraschka.com/blog/2023/llm-training-and-evaluation.html) — *modern overview of the four-stage pipeline.*
- [HuggingFace NLP Course — Chapter 1](https://huggingface.co/learn/llm-course/chapter1) — *hands-on intro to the pre-training objective.*

### Data Pipeline
> **Lecture's take:** Clone source data (GitHub archive for code, web crawls for text), filter out low-quality or unlicensed files, near-deduplicate near-copies, and the resulting corpus trains the transformer. Worked example: BigCode — 220M GitHub repos → 102 TB → ~30% keep → 6.4 TB after file selection → license filter + near-dedup → 3 TB final.

**Canonical definition.** A modern pre-training corpus goes through (1) raw collection (web crawls, code archives, books), (2) quality filtering (heuristics, classifier-based filters, license filters), (3) near-deduplication (MinHash / SimHash to remove near-copies that distort training), (4) optionally PII redaction. The output is what the model actually trains on.

**Key insight.** Quality filtering and near-deduplication are not optional polish — they are the difference between a model that learns useful patterns and one that memorises boilerplate, regurgitates training data, or picks up low-quality biases. The FineWeb2 dataset card documents these choices in detail.

**📚 Further reading**
- [HuggingFace FineWeb2 dataset card](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) — *the most widely-used modern web-corpus pipeline documentation.*
- [Lee et al., 2022 — "Deduplicating Training Data Makes Language Models Better"](https://arxiv.org/abs/2107.06499) — *the empirical case for near-dedup.*
- [BigCode — "The BigCode Project: LLMs for Code"](https://arxiv.org/abs/2211.03027) — *the BigCode pipeline, including the 220M-repo → 3 TB reduction cited in the lecture.*

### Fill-in-the-Blank Training
> **Lecture's take:** Each sentence of N tokens is converted into N training questions. Example: "There is no tomorrow" → "There is no \_\_\_", "There is \_\_\_ tomorrow", "There \_\_\_ tomorrow", "\_\_\_ no tomorrow". N tokens = N training signals per sentence. **Masked attention** makes this possible.

**Canonical definition.** Causal (masked) language modelling turns a single sentence into N supervised prediction problems: for each token position `i`, the model is asked to predict token `i` given tokens `0..i-1`. The total loss is the sum (or mean) of the per-position cross-entropies.

**Key insight.** "Fill-in-the-blank" is the same formulation as the pre-training objective. The point of the lecture's framing is that one sentence gives you N supervised examples for free — which is why labelled-data collection isn't strictly necessary for the *first* training stage.

**📚 Further reading**
- [Vaswani et al., 2017 — §5.4](https://arxiv.org/abs/1706.03762) — *the causal language-modelling objective used to train the original transformer.*
- [Andrej Karpathy — "Let's build GPT"](https://www.youtube.com/watch?v=kCc8FmEb1nY) — *builds the fill-in-the-blank loss from scratch.*

### Training Loop
> **Lecture's take:** `predict token → compare to expected → cross-entropy loss → backprop → update weights`. The weights updated include the embedding, attention, FFN, and the final linear layer — every weight in the model is updated by every gradient step.

**Canonical definition.** A training step consists of a forward pass (compute logits), a loss computation (cross-entropy against the ground-truth next token), a backward pass (compute gradients of the loss w.r.t. every weight), and an optimiser step (Adam/AdamW updates the weights using those gradients).

**Key insight.** Every weight in the model — including embeddings, attention projections, FFN matrices, layer-norm gains, and the unembedding matrix — receives gradients on every step. There is no "frozen" layer during pre-training (frozen layers only appear in parameter-efficient fine-tuning like LoRA).

**📚 Further reading**
- [Goodfellow et al., 2016 — "Deep Learning" Ch. 8 (online)](https://www.deeplearningbook.org/) — *optimisation chapter covering SGD and Adam.*
- [Loshchilov & Hutter, 2019 — "Decoupled Weight Decay Regularization" (AdamW)](https://arxiv.org/abs/1711.05101) — *the optimiser actually used to train modern LLMs.*

### Cross-entropy loss
> **Lecture's take:** The loss function is "log of expected token output probability plus sum of log one minus all other token probabilities" (verbatim from the transcript, which omits leading negatives in the sum). The notes express the same idea as `loss = -log(p_expected) + Σ(-log(1-p_other))`. The standard formulation collapses to just `-log(p_correct)` for a one-hot target, since the other terms contribute `Σ(-log(1-0)) = 0`.

**Canonical definition.** Cross-entropy loss for next-token prediction is `L = -Σ_i log P(token_i | context_i)`. For a one-hot target (exactly one correct next token), this simplifies to `L = -log(p_correct)`. It is the negative log-likelihood of the correct token under the model's predicted distribution.

**Key insight.** Cross-entropy is bounded below by 0 (when `p_correct = 1`) and unbounded above (when `p_correct → 0`, `−log(p) → ∞`). This unboundedness is what makes the loss signal useful — there is always a non-zero gradient pushing the model to assign higher probability to the correct token, no matter how wrong the current prediction is.

**📚 Further reading**
- [Vaswani et al., 2017 — §5.4](https://arxiv.org/abs/1706.03762) — *cross-entropy as the training objective.*
- [Goodfellow et al., 2016 — "Deep Learning" Ch. 4](https://www.deeplearningbook.org/) — *"Information Theory, Cross-Entropy" section.*

### Sigmoid
> **Lecture's take:** Sigmoid is a teaching anchor used in the preference-optimization section (NOT in the cross-entropy discussion — the placement in earlier versions of these notes was incorrect). Sigmoid(20) ≈ 1 and sigmoid(-20) ≈ 0. The lecture later notes that "sigmoid is no longer used" in production preference-optimization algorithms — it's just for ease of understanding.

**Canonical definition.** The sigmoid (logistic) function `σ(x) = 1 / (1 + e^{-x})` maps any real number to the open interval (0, 1). Its derivative is `σ'(x) = σ(x)(1 - σ(x))`, and `log(σ(x))` is the "logit" — the inverse direction of the same map.

**Key insight.** Sigmoid saturates quickly: for `|x| > ~5`, the output is essentially 0 or 1 and the gradient is essentially 0. This saturation is the *reason* PPO was preferred over a naive sigmoid-policy update in early RLHF — and is also *why* DPO/GRPO moved away from explicit sigmoid terms altogether.

**📚 Further reading**
- [Goodfellow et al., 2016 — "Deep Learning" Ch. 3](https://www.deeplearningbook.org/) — *sigmoid and saturation behaviour.*

## Supervised Fine-Tuning (SFT)

> **Lecture's take:** Format: Input (instruction) + Output (human-written answer). What it changes: tone, format, jargon, guardrails. The output is written by a human once at dataset creation time, but the loss is computed automatically at training time.
> Example: Sales call transcripts → input (customer query) + output (salesperson response). Trains the model to respond in that style.

**Canonical definition.** Supervised fine-tuning is the second training stage: the base model is trained on `(instruction, response)` pairs written by humans. The objective is the same cross-entropy on the response tokens (input tokens are masked out of the loss). This is what teaches the model to follow instructions, refuse unsafe requests, and adopt a particular style.

**Key insight.** SFT changes *style*, not *capability*. The base model already knows the facts; SFT just teaches it *when* and *how* to surface them in response to a prompt. This is why catastrophic forgetting is a real risk during SFT — too many gradient steps can erode the capabilities the base model already had.

**📚 Further reading**
- [Ouyang et al., 2022 — InstructGPT](https://arxiv.org/abs/2203.02155) — *the canonical SFT → RM → PPO pipeline.*
- [HuggingFace TRL — SFTTrainer documentation](https://huggingface.co/docs/trl/en/sft_trainer) — *practical SFT setup.*

## Tool Calling / Function Calls

### Tool calling
> **Lecture's take:** **LLMs cannot actually make function calls.** They only output tokens. Fine-tuning teaches the model to emit a textual template (e.g., `time = [calendar][get_current_time][result]`). The server-side parses this, executes the function, and appends the result back into the prompt. The model then continues generating based on the result.

```
User → LLM: "What is the time?"
LLM → Server: template tokens "time = [calendar][get_current_time][result]"
Server → Tool API: get_current_time()
API → Server: 9:35 AM
Server → LLM: append result to prompt
LLM → User: "The time is 9:35 AM"
```

**Canonical definition.** Tool calling (or "function calling") is a fine-tuning convention in which the model is trained to emit a structured text template (modern variants use JSON: `{"name": "get_current_time", "arguments": {}}`) whenever the user request requires an external action. The model never executes anything itself — a server-side harness parses the template, calls the API, and feeds the result back into the prompt.

**Key insight.** The model is not "calling" anything. It's generating tokens whose *convention* triggers an external action. This matters because the same trick works for any text-emitting model, regardless of whether it was explicitly trained for it — and conversely, an LLM can "hallucinate" a tool call that the harness must choose to ignore or reject.

**📚 Further reading**
- [OpenAI — "Function calling and other API updates" (Jun 2023)](https://openai.com/index/function-calling-and-other-api-updates/) — *the canonical industry-launch post.*
- [Schick et al., 2023 — "Toolformer: Language Models Can Teach Themselves to Use Tools"](https://arxiv.org/abs/2302.04761) — *the research-paper treatment of tool learning.*

## Preference Optimization

### Reinforcement Learning from Human Feedback (RLHF)
> **Lecture's take:** Modern RLHF-family algorithms refine the model's behaviour using human preference signals. The lecture surveys three variants: GRPO, DPO, PPO.

**Canonical definition.** RLHF trains a reward model on human `(response_a, response_b, preference)` judgements, then optimises the language-model policy to maximise the reward (regularised to stay close to the SFT model). PPO (Schulman 2017) was the original RL algorithm; DPO and GRPO replace the explicit reward model with a reparameterised loss derived directly from the preference data.

**Key insight.** DPO and GRPO were popularised because they avoid the instability of PPO + a separate reward model — they turn preference learning into a supervised classification problem with a clever log-ratio loss. GRPO in particular (DeepSeek) was designed for math/code tasks where you can sample multiple candidate solutions per prompt and rank them automatically.

**📚 Further reading**
- [Ouyang et al., 2022 — InstructGPT](https://arxiv.org/abs/2203.02155) — *the original PPO-based RLHF for LLMs.*
- [Lilian Weng — "RLHF Reward Hacking"](https://lilianweng.github.io/posts/2024-11-28-reward-hacking-in-rlhf/) — *what goes wrong when you push the reward signal too hard.*

### PPO — Proximal Policy Optimization
> **Lecture's take:** In R52 the instructor misspoke PPO as "Proximal Preference Optimization" — the canonical name is **Proximal Policy Optimization** (Schulman et al., 2017). PPO was the original RL algorithm used for RLHF in InstructGPT.

**Canonical definition.** PPO is a policy-gradient RL algorithm that constrains each update to stay within a "trust region" of the previous policy, using a clipped surrogate objective. For LLM RLHF, PPO maximises the reward model's score while penalising divergence from the SFT reference policy.

**Key insight.** PPO is on-the-shelf stable for RL but famously fiddly in practice — it requires careful reward normalisation, advantage estimation, KL coefficient tuning, and four models in memory (policy, reference, reward, value). This complexity is the main reason DPO/GRPO replaced PPO in most modern LLM pipelines.

**📚 Further reading**
- [Schulman et al., 2017 — "Proximal Policy Optimization Algorithms"](https://arxiv.org/abs/1707.06347) — *the original PPO paper.*
- [Ouyang et al., 2022 — InstructGPT](https://arxiv.org/abs/2203.02155) — *PPO applied to LLM RLHF.*

### DPO — Direct Preference Optimization
> **Lecture's take:** Direct preference pair training. DPO trains the model directly on `(preferred, rejected)` pairs without a separate reward model.

**Canonical definition.** DPO (Rafailov et al., 2023) shows that the PPO objective with a Bradley-Terry reward model has a closed form in terms of the policy and reference log-probabilities. The resulting supervised loss is `L = -log σ(β · (log π(winner) − log π_ref(winner) − log π(loser) + log π_ref(loser)))`.

**Key insight.** DPO turns RLHF into supervised learning — no separate reward model, no online sampling during training, no four-model memory footprint. The trade-off is that DPO is harder to apply when you want to mix preference data with verifiable rewards (e.g., math correctness) — that's where GRPO has an edge.

**📚 Further reading**
- [Rafailov et al., 2023 — "Direct Preference Optimization"](https://arxiv.org/abs/2305.18290) — *the DPO paper.*
- [Rafailov et al., 2023 — NeurIPS OpenReview](https://openreview.net/forum?id=HPuSIXJaa9) — *peer-reviewed version with reviewer discussion.*

### GRPO — Group Relative Policy Optimization
> **Lecture's take:** The lecture names GRPO as the modern preference-optimization algorithm popularised by DeepSeek for math and code. Note: the lecture called it "Group Relative Preference Optimization" — the canonical DeepSeekMath paper defines it as **Group Relative Policy Optimization** (Policy, not Preference).

**Canonical definition.** GRPO (Shao et al., 2024, DeepSeekMath) samples a *group* of candidate completions per prompt, computes the reward for each, and uses the group's relative ranking as the advantage — there is no separate value/critic model. The policy is updated with a clipped surrogate loss plus a KL penalty to the reference.

**Key insight.** GRPO removes PPO's critic network by using group statistics as the baseline, and it rewards on verifiable signals (correctness of the answer, pass-rate on a unit test) rather than a learned reward model. This is why GRPO dominates math/code post-training today.

**📚 Further reading**
- [Shao et al., 2024 — "DeepSeekMath: Pushing the Limits of Mathematical Reasoning"](https://arxiv.org/abs/2402.03300) — *the GRPO paper.*
- [Shao et al., 2024 (HTML readable)](https://arxiv.org/html/2402.03300) — *easier-to-read HTML version.*

## Model Serving

> **Lecture's take:** After post-training: freeze all weights, deploy to GPUs, users send queries → model responds. Internal weights are **not changed** at inference time. A model too large for one GPU must be split: different layers sit on different GPUs, an orchestrator passes data between GPUs, output flows back to the orchestrator → next GPU → final prediction. Critical knobs: KV cache, context window, vocabulary size.

### Model serving
> **Lecture's take:** (paraphrased from the serving discussion) Inference is frozen-weights-only; the same set of weights is queried for every user request.

**Canonical definition.** LLM serving is the operational layer that takes a trained model and answers user queries at scale. The dominant open-source serving system (vLLM) introduced PagedAttention to manage the KV cache like virtual memory, enabling much higher batch sizes and throughput.

**Key insight.** Throughput in LLM serving is dominated by KV-cache memory, not by FLOPs. A single H100 can compute far more tokens than it can store KV-cache for. PagedAttention (vLLM, 2023) was the breakthrough that made high-throughput batched serving practical.

**📚 Further reading**
- [Kwon et al., 2023 — "Efficient Memory Management for Large Language Model Serving with PagedAttention"](https://arxiv.org/abs/2309.06180) — *the vLLM paper.*
- [vLLM blog — "Easy, Fast, and Cheap LLM Serving with PagedAttention" (Jun 2023)](https://vllm.ai/blog/2023-06-20-vllm) — *accessible overview.*

### Pipeline parallelism (GPU orchestration)
> **Lecture's take:** When a model is too large for one GPU, split it across GPUs by layer. An orchestrator passes data between GPUs, layer by layer.

**Canonical definition.** Pipeline parallelism splits the model by *layer*: GPU 0 holds layers 1–k, GPU 1 holds layers k+1–2k, and so on. Activations flow GPU-to-GPU sequentially. The naive version has a "bubble" where idle GPUs wait for the slowest one; GPipe introduced micro-batching to fill the bubble.

**Key insight.** Pipeline parallelism is one of three parallelism strategies; the others are **tensor parallelism** (split each matrix multiplication across GPUs) and **data parallelism** (replicate the model on each GPU, shard the batch). Production training typically combines all three — Megatron-LM (Shoeybi 2019) is the canonical recipe.

**📚 Further reading**
- [Huang et al., 2018 — "GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism"](https://arxiv.org/abs/1811.06965) — *the pipeline-parallelism paper.*
- [Shoeybi et al., 2019 — "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism"](https://arxiv.org/abs/1909.08053) — *the canonical recipe combining pipeline + tensor parallelism.*

### Data shortage
> **Lecture's take:** Not asserted in R52 — earlier versions of these notes added it as a takeaway. The "running out of public training data" framing is current industry knowledge (Epoch AI, 2024), not part of the lecture. Listed here for completeness and linked to the source.

**Canonical definition.** Villalobos et al. (2022/2024, Epoch AI) project that publicly available human-generated text will be exhausted by LLM training demand sometime in the 2020s. This has driven the industry toward synthetic data, licensed data deals, and code/multimodal data.

**Key insight.** "Running out of data" doesn't mean LLMs stop improving — it means the easy gains from scaling up web-text training are saturating. The frontier is now (a) higher-quality curated corpora, (b) synthetic data from stronger models, and (c) inference-time compute.

**📚 Further reading**
- [Villalobos et al., 2022/2024 — "Will we run out of data?"](https://arxiv.org/abs/2211.04325) — *the Epoch AI analysis.*
- [Epoch AI — "Will we run out of data?" (interactive)](https://epochai.org/data/will-we-run-out-of-data) — *live projections.*

## Q&A Highlights

| Question | Answer |
|----------|--------|
| Does SFT involve manual annotation? | The output is human-written once, but losses are computed automatically. |
| How do you penalize on tokens with little context? | Deferred — model still gets a loss signal at every position. |
| What is the input/output size of the transformer? | N × D throughout; final linear: N × D → N × \|vocab\|. |
| How does tool calling actually work? | Model outputs a token template; server interprets; result appended to prompt. |
| What are modern preference optimization algorithms? | GRPO (DeepSeek, math/code), DPO, PPO. Sigmoid is the conceptual anchor. |
| Why input tokens > output tokens? | Apps pass documents, search results, page contents as input. |

## Homework / Next Steps

- **Paper on preference optimization** (GRPO/DPO/PPO) to be shared in the reading material — see links in the Preference Optimization section above.
- **Next Sunday:** Coding session — bring laptops, Google Colab links will be shared
- Roadmap: Pre-training → **Fine-tuning** (next week) → RAG → Agents → Capstone project

## Key Takeaways

1. **LLM training = pre-training + post-training + serving**
2. **Pre-training:** tokenize massive data, predict next token at every position, cross-entropy loss
3. **SFT:** human-written QA pairs for format/tone/jargon
4. **Tool calling is a textual convention** — the model emits tokens; the server interprets
5. **Preference optimization** refines behavior with reward signals (GRPO, DPO, PPO)
6. **Model serving** freezes weights; KV cache and vocabulary are key knobs for cost/performance

## Mermaid Summary Diagram

```mermaid
graph LR
    A[Public Datasets] --> B[Tokenize]
    B --> C[Pre-training]
    C --> D[Base Model]
    D --> E[SFT]
    E --> F[Format Model]
    F --> G[Preference Opt]
    G --> H[Final Model]
    H --> I[Freeze + Serve]
    I --> J[User Queries]
```

---

## Related Materials

- 📄 Raw transcript: [`transcripts/recording-52.srt`](transcripts/recording-52.srt)
- �️ Knowledge graph (visual): [`sessions/llm-training-pipeline-tool-use-graph.md`](sessions/llm-training-pipeline-tool-use-graph.md)
- 🧠 Knowledge graph (structured JSON): [`sessions/llm-training-pipeline-tool-use-graph.json`](sessions/llm-training-pipeline-tool-use-graph.json)
- 🌐 Combined view across both recordings: [`sessions/combined-knowledge-graph.md`](sessions/combined-knowledge-graph.md)
