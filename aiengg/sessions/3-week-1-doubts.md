---
title: "3. Week 1 Doubts & Networking"
tags: [session, 3, qa]
---

# 3. Week 1 Doubts & Networking

**Source:** [`transcripts/networking-session-1.srt`](../transcripts/networking-session-1.srt)
**Recording:** Week 1 networking call (companion to session 1)
**Host:** Gaurav Sen (Speaker 7), with co-instructors Tanishk (Speaker 1) and Tanishq (Speaker 4)
**Duration:** 01:42:01
**Type:** Doubt Solving
**Speakers:** 18 (instructors + students)

> **What this session is.** A live Q&A where students from the cohort brought their week-one doubts. Each question is answered by the instructors with pointers to the relevant concept pages. The session also covers career-shaped questions (depth needed for AI-engineering roles, recruiter signals, where image models fit alongside LLMs).

> **Note on attribution.** Speaker 1 (Tanishk) and Speaker 4 (Tanishq) are co-instructors who jointly answer most technical questions; Speaker 7 (Gaurav Sen) hosts the call and steps in on framing/strategy questions. Gaurav is not the long-form instructor of this session.

## Session Goals

- Collect week-one feedback and clarify course logistics (capstone project, labs, API keys).
- Walk through the most upvoted week-one doubts one by one — primarily about transformer internals (Q/K/V, embeddings, FFN dimensions).
- Cover career-shaped questions: depth needed for AI-engineering roles, signals to get noticed by recruiters, and where image models (e.g. ComfyUI) fit alongside LLMs.

## Questions Covered

For each question, the relevant concept page (if one exists) is linked next to the answer.

### Architecture & Internals

**Q1: Will there be a hands-on math walkthrough — e.g. imagine a vocab of 10 tokens and walk through next-token prediction?** *(Nihar)*

→ [`next-token-prediction`](../concepts/next-token-prediction.md) and the [attention](../concepts/attention.md) page.

Walking through the full attention math for a single token-by-token prediction is technically doable but very long and easy to lose the audience on. The lecture's recommendation: read the worked example using the BERT-style attention visualiser on *"The bank of the city river was flooded"* → next token *"by"* in the concept notes first. Deeper one-on-one walkthroughs can happen in the cohort chat.

---

**Q2: In the encoder-decoder transformer, is the encoder *only* used during training, or also during inference?** *(Abhishek)*

→ [`transformer`](../concepts/transformer.md).

In modern (GPT-style) architectures the model is **decoder-only** — there is no encoder at all, both during training and inference. In the *older* encoder-decoder transformer (think original Vaswani machine-translation model), the encoder runs on every input — including during inference — producing the K and V tensors, while the decoder streams Q tensors that cross-attend against them. The encoder's job is to compress the source into a representation; the decoder's job is to generate tokens one by one. Encoder-only models (BERT family) are still useful, mainly for **embedding models** used in RAG.

> *"Encoder basically gives you K and V values. … the modern LLMs that you see, they are decoder-only models, and encoder is used for embedding models only."* — Gaurav

---

**Q3: Where are the embeddings stored? Are they clustered somewhere like a vector DB?** *(Abhisit / Abhishek)*

→ [`vector-embedding`](../concepts/vector-embedding.md).

Embedding vectors are **not stored in a separate database**. They live *inside the model weights* as rows of the embedding matrix of shape `[vocab_size × D]`. Every token ID is just a row index into that matrix — King → row 12345 → a fixed 768-dim vector. There is no vector DB lookup at inference time for the base transformer; the embedding is a slice of a weight tensor.

> *"When you try to download any model, … all the weights being downloaded actually, so it is not stored anywhere, it is part of the model architecture itself. … that is why there is no vector DB involved here. That is why I asked because in RAG there is a vector DB, but those are two very different things."* — Tanishk

The vector DB confusion comes from RAG, where external documents *are* encoded into vectors and stored in a database like FAISS, Pinecone, or Qdrant for retrieval. The base LLM itself has no vector DB.

---

**Q4: Why 768 dimensions? Who picks that number, and how is the embedding value computed?** *(Navdas)*

→ [`vector-embedding`](../concepts/vector-embedding.md).

`D` (the embedding / hidden dimension) is a **hyperparameter chosen at architecture design time**. It is fixed before training and stays the same throughout. Common values: 768 (BERT-base), 1024, 1280, 2048, 4096, 8192 (Llama-3). The individual float values in each row come from **random initialization → gradient descent** during pre-training. After training, they are frozen in the file you download.

---

**Q5: When a wrong prediction is made during training, do the token embeddings get updated, or is that separate from the Q/K/V updates?** *(Student follow-up)*

→ [`token`](../concepts/token.md).

Backpropagation updates **everything that is learnable in the architecture** — including the embedding matrix, the Q/K/V projection matrices, and the FFN layers. The distinction is between two kinds of parameters:

1. **Learnable parameters** — weights, biases, embeddings, Q/K/V matrices. Randomly initialized, updated by gradient descent during training.
2. **Non-learnable parameters** — tokenizer vocabulary, token-to-ID mapping, rules like BPE merges. These are computed once from a corpus (a "tokenizer training" pass) and then frozen.

> *"There are two different types of parameters. One is learnable and one is not learnable, which is fixed. … position embeddings can be fixed or learnable based on whatever the architecture is, … embeddings are part of LLM call itself."* — Tanishk

---

**Q6: If a word/token wasn't in the training set, what does the model do? Hallucinate?** *(Speaker 3)*

→ [`token`](../concepts/token.md) and [`hallucination`](../concepts/hallucination.md).

The model **cannot learn anything new at inference** — weights are frozen. What happens depends on the tokenizer:

- **Word-level tokenizers** would throw an "unknown token" / `<unk>` error.
- **Sub-word (BPE) tokenizers** used by all modern LLMs will **decompose the new word into known sub-pieces**. "PromptForge" → "Prompt" + "Forge" (both likely in vocab). The LLM then *makes its best guess* from the sub-pieces it knows — which is exactly what "hallucination" means in the factual-definition sense.

> *"LLM might not know what is promptforge, but it knows what is a prompt and what is forge. … So it will give you the most optimum meaning of the word. … So hallucination is just making up facts."* — Tanishk

---

**Q7: How are Q, K, V matrices computed from the input embedding matrix in self-attention?** *(Deeksha)*

→ [`query-key-value`](../concepts/query-key-value.md) and [`attention`](../concepts/attention.md).

Q, K, V are obtained by three **learnable linear projections** of the input embedding matrix X:

- `Q = X · W_Q`, `K = X · W_K`, `V = X · W_V` — where `W_Q`, `W_K`, `W_V` are `[D × d_k]` matrices that are randomly initialized and trained by gradient descent.
- The attention output is `softmax(Q·Kᵀ / √d_k) · V`.

The student-side confusion was whether there was a closed-form way to derive `W`. There is not — it is **trained**.

---

**Q8: Is KV cache the same as the (Q, K, V) matrices, or something different?** *(Panush)*

→ [`kv-cache`](../concepts/kv-cache.md).

The KV cache is built *from* the K and V tensors computed during self-attention — it is **not** the same thing as Q (Q is recomputed every token), nor is it a separate architecture. It is an **inference-time optimization**: cache the K and V projections of already-generated tokens so we don't have to recompute them for every new step.

> *"KV cache is part of the same K and V values that we are training the model for … KV cache is getting cached in the transformer architecture as well."* — Tanishk

---

**Q9: Can the FFN expand to more 'relatable' dimensions? How are those dimensions chosen?** *(Student via sheet)*

→ [`feed-forward-network`](../concepts/feed-forward-network.md).

FFN expands the embedding dimension `D` to `4D` (typical — Llama uses a gated variant with `8D/3`), uses an activation (ReLU → SwiGLU in modern models), then projects back to `D`. The `4×` ratio is a *learned-from-experience* design choice carried over from the original transformer; it is not derived from first principles. The activation function is what gives the FFN its non-linear representational power (linear layers alone collapse to a single matrix).

> *"Feed-forward layer just uses an activation function to expand the dimensions and get more features out of it. … from the input side, in the feed-forward network, when you give it D dimensions, then it expands into 4D dimensions. And then from the 4D dimension, the knowledge it gained, it again distills it to D dimension."* — Tanishq

---

**Q14: If OpenAI upgrades from GPT-3.5 to GPT-5, do they train from scratch?** *(Abhishek)*

→ [`pre-training`](../concepts/pre-training.md).

Labs **do not train from scratch** between versions (cost prohibitive). They run a **post-training cycle** — same base, additional SFT and preference-optimization passes on new data. Pre-training teaches language; post-training teaches conversation and instruction-following.

> *"Inference is asking the question… post-training is the training phase."* — Tanishk

---

**Q15: Is post-training and validation the same thing?** *(Manasi)*

→ [`pre-training`](../concepts/pre-training.md).

**No.** Validation is the practice of holding out a fraction of the training data (typically 10–20%) to check generalization. Post-training is the second training stage (SFT + preference-opt) on curated data. Different concepts, different points in the pipeline.

> *"Validation is just part of a data sampling thing. A post-training is like when we are training the model to do for a particular task, like conversation or anything else."* — Tanishk

---

**Q16: How is orchestration used during training — Spark or something GPU-specific?** *(Speaker 11, data-eng background)*

→ [`gpu-orchestration`](../concepts/gpu-orchestration.md).

There are **two kinds of orchestration** in this stack:

1. **Data orchestration (pre-training):** Spark (or Beam, Ray) used to scrape/curate/clean/PII-strip the trillion-token training corpus. *This* is the data-engineering angle.
2. **GPU/training orchestration:** distributing a single training run across thousands of GPUs (data/tensor/pipeline parallelism). This is a separate deep topic that will not be covered in this cohort.

---

### Career & Workflow

**Q10: After the cohort, will I be ready to apply for FDE roles, or only contribute to my existing project?** *(Sridhar)*

Both. The target of the cohort is fundamentals broad enough for (a) interviews, (b) building systems at the current job, and (c) switching to a new role. Past cohorts have alumni who switched jobs *and* alumni who got internal funding for new AI projects at their existing company.

---

**Q11: How deep will EVALs and Guardrails be covered? Will it be a low-level example or a high-level explanation?** *(Sridhar follow-up)*

Coverage will be **architecturally agnostic** and metric-driven — exact RAG-specific metrics, exact agent-specific metrics, exact multi-agent metrics. Modern EVAL suites (RAGAS, DeepEval, Phoenix, LangSmith Evals) are emerging as a category of their own; the cohort teaches *what to measure* (faithfulness, answer relevancy, context precision/recall, tool-call accuracy) rather than which vendor to use.

---

**Q12: What signals should I create to get noticed by AI recruiters, and which platform should I use?** *(Collier Blake, JP Morgan)*

The durable signal is **personal brand via public artifacts**:

1. Write blog posts distilling what you learn each week.
2. Open-source repos with thoughtful READMEs.
3. Connect with the right people — quality of network > platform.

> *"I have seen people getting job roles through their GitHub repos. So they have shared their GitHub repos, open-sourced, … and through that they were getting some job roles."* — Tanishk

---

**Q13: How much transformer-internals depth is needed for AI engineering in practice?** *(Poorna)*

Basic understanding of how attention works is **beyond what is required** for most AI-engineering jobs. In practice you almost always use an API-hosted LLM and build **systems around it** (RAG, agents, evals, orchestration) — not models from scratch.

---

**Q17: How similar are diffusion / image models (ComfyUI) to LLMs?** *(Sid + Arun)*

Diffusers and LLMs share the **transformer backbone + attention mechanism**. Differences:

- **Inputs:** LLMs process discrete text tokens; diffusion models process image patches (or VAE-encoded latent tokens).
- **Output:** LLMs produce next text token; diffusion models iteratively denoise a noise image into a clear image.
- **Adapters/LoRA:** LoRA on a diffusion model = fine-tune it to a specific character/style with curated image datasets; LoRA on an LLM = fine-tune it for a domain (legal / medical). Different mechanics, same overall goal.

> *"Diffusion models are very similar to large language models. … the core architecture is not different, but the only thing is that we process and create data sets as images in the pixel space."* — Arun

---

**Q18: If a system adapts to my preferences over a session, does it fine-tune itself?** *(Ayush)*

No fine-tuning at inference. The behaviour adapts because **either**:

1. **It's not an LLM, it's an agent** — modern apps (ChatGPT, Claude) are agents with external memory (CLAUDE.md, project skills, custom user preferences) that get re-injected into every call.
2. **Or the chat thread's prior messages are included in the context window** — so when you say "no emojis" mid-conversation, all subsequent messages include that instruction implicitly.

> *"All of these are actually agents. They are no longer simple LLMs. They have an external memory, external context, which they are maintaining."* — Tanishk

---

**Q19: How do you build a personal mind-map / flow-chart for the week-1 lectures?** *(Ayush)*

A practical workflow:

1. Collect a curated list of resources (papers, blogs, official docs).
2. Hand them to an LLM (Claude is recommended) with a structured prompt asking for a mind-map organised by topic.
3. Iterate — usually 2–3 rounds of "tighten this section" — to converge on a usable doc.
4. For visuals, enable the **Excalidraw MCP** in Claude to generate diagrams alongside.

> *"I collect a bunch of good resources, … give it to Claude and I write a very structured prompt, can you help me build a structured mind map through all the topics which are mentioned there."* — Tanishk

---

## Key Themes

- **Architecture clarity.** The cohort needed to firm up the distinction between encoder/decoder, where embeddings live, what the KV cache is, and why FFN dimension is `4×`.
- **Training-vs-inference confusion.** Several students conflated post-training with inference, and validation with post-training.
- **Hallucination as a structural feature.** Not a bug — what an LLM does when given inputs it can't evaluate; the solution is more context (RAG, fine-tuning, tool calling).
- **Career outcomes / role calibration.** The cohort was reassured that fundamentals + portfolio artifacts are enough for either internal projects or job-switching, without needing to match frontier-lab ML depth.
- **Diffusion models as cousins, not strangers.** ComfyUI and LLMs share a transformer backbone, differ in input/output modalities.

## Homework / Next Steps

- Read the **QKV math notes** linked by Tanishk before next week.
- Send any **persistent questions** to the cohort sheet; they will be picked up next networking call.
- Use the **resource doc** Tanishk mentioned for depth on RAG/agents/evals.
- Watch for the upcoming **fine-tuning lecture (Saturday / Sunday)**.

## Key Takeaways

1. **Modern LLMs are decoder-only**; encoder-only models live on as embedding backbones for RAG.
2. **Embeddings are not stored in a vector DB** — they live inside the model weights as the embedding table.
3. **Backprop updates everything learnable** — embeddings, Q/K/V matrices, FFN weights — during every training step.
4. **KV cache ≠ QKV.** It is an inference-time optimization that caches previously-computed K and V tensors.
5. **Hallucination = best-guess from subwords.** BPE tokenizers decompose unknown words into known pieces.
6. **Pre-training teaches language; post-training teaches conversation.** Both are training (weights change). Validation is a held-out data split.
7. **For AI engineering roles, system-level depth matters more than transformer-internals depth.**
8. **Personal brand via published artifacts** (blogs, open-source repos) is the highest-leverage signal to recruiters.

## Related Materials

- 📄 Raw transcript: [`transcripts/networking-session-1.srt`](../transcripts/networking-session-1.srt)
- 🕸️ Knowledge graph (visual): [`3-week-1-doubts-graph.md`](3-week-1-doubts-graph.md)
- 🧠 Knowledge graph (JSON): [`3-week-1-doubts-graph.json`](3-week-1-doubts-graph.json)
- 🌐 Combined view: [`combined-knowledge-graph.md`](combined-knowledge-graph.md)
- 🌱 Browse concepts: [`../concepts/index.md`](../concepts/index.md)
- 📝 Related teaching sessions: [1. LLM Basics & Transformer Internals](1-llm-basics.md), [2. Training Pipeline & Tool Use](2-training-pipeline.md)
