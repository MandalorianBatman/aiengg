---
title: "Week 1 Networking — Doubt-Solving Session"
tags: [session, networking, qa]
---

# Week 1 Networking — Doubt-Solving Session

**Source:** [`transcripts/networking-session-1.srt`](../transcripts/networking-session-1.srt)
**Recording:** Week 1 networking call (companion to R51)
**Host:** Gaurav Sen (Speaker 7), with co-instructors Tanishk (Speaker 1) and Tanishq (Speaker 4)
**Duration:** 01:42:01
**Type:** Doubt Solving
**Speakers:** 18 (instructors + students)

## Session Goals

- Collect week-one feedback from the cohort and clarify course logistics (capstone project, labs, API keys).
- Walk through the most upvoted week-one doubts one by one — primarily about transformer internals (Q/K/V, embeddings, FFN dimensions).
- Cover career-shaped questions: depth needed for AI-engineering roles, signals to get noticed by recruiters, and where IMAGE models (e.g. ComfyUI) fit alongside LLMs.

> **Note on attribution.** Speaker 1 (Tanishk) and Speaker 4 (Tanishq) are co-instructors who jointly answer most technical questions; Speaker 7 (Gaurav Sen) hosts the call and steps in on framing/strategy questions. Gaurav is not the long-form instructor of this session.

## Questions Covered

### Q1: "Will there be a hands-on math walkthrough — e.g. imagine a vocab of 10 tokens and walk through next-token prediction?" (Nihar)

> **Student's question:** Could we include a hands-on math example — for instance, a vocabulary of 10 tokens and a step-by-step walkthrough of how an LLM is trained to predict the next token, making the connection between next-token prediction, attention, and the feed-forward block?

**Answer (Tanishq + Gaurav):** Walking through the full attention math for a single token-by-token prediction is technically doable but very long and easy to lose the audience on. The notes already contain a worked example using the BERT-style attention visualiser on the sentence *"The bank of the city river was flooded"* → next token *"by"*. The recommendation is to read those notes first; deeper one-on-one walkthroughs can happen in the cohort chat.

**Key insight:** A 10-token vocabulary example is a great pedagogical device, but the *useful* unit of study is the Q·Kᵀ/√d softmax step on a single head — the rest is repetition across heads and layers. The HuggingFace "LLM Course" attention chapter is the canonical version of this exercise.

**📚 Further reading:**
- [3Blue1Brown — Attention, transformer networks](https://www.3blue1brown.com/topics/neural-networks)
- [HF NLP Course — Transformers, attention](https://huggingface.co/learn/llm-course/chapter2)

---

### Q2: "In the encoder-decoder transformer, is the encoder *only* used during training, or also during inference?" (Abhishek)

> **Student's question:** We have both encoder and decoder in the architecture. My understanding is that the decoder is what we use for inference — is the encoder only needed for training?

**Answer (Tanishq + Gaurav + Tanishk):** In modern (GPT-style) architectures the model is **decoder-only** — there is no encoder at all, both during training and inference. In the *older* encoder-decoder transformer (think original Vaswani machine-translation model), the encoder runs on every input — including during inference — producing the K and V tensors, while the decoder streams Q tensors that cross-attend against them. The encoder's job is to compress the source into a representation; the decoder's job is to generate tokens one by one. Encoder-only models (BERT family) are still useful, mainly for **embedding models** used in RAG.

> **Lecture's take (Gaurav):** *"Encoder basically gives you K and V values. … the modern LLMs that you see, they are decoder-only models, and encoder is used for embedding models only."*

**Key insight:** Modern LLMs are decoder-only **because** generation is auto-regressive — the model only ever needs to look back at tokens it has already produced. An encoder's job (build a bidirectional representation of an entire sequence) matters more for embedding/retrieval use cases than for generation.

**📚 Further reading:**
- [Vaswani et al., 2017 — Attention Is All You Need](https://arxiv.org/abs/1706.03762) (original encoder-decoder)
- [Alammar — The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)

---

### Q3: "Where are the embeddings stored? Are they clustered somewhere like a vector DB?" (Abhisit / Abhishek)

> **Student's question:** Vectors get 'clustered together' — where are they physically stored, and what is the mechanism of clustering?

**Answer (Tanishq + Tanishk + Gaurav):** Embedding vectors are **not stored in a separate database**. They live *inside the model weights* as rows of the embedding matrix of shape `[vocab_size × D]`. Every token ID is just a row index into that matrix — King → row 12345 → a fixed 768-dim vector. There is no vector DB lookup at inference time for the base transformer; the embedding is a slice of a weight tensor.

> **Lecture's take (Tanishk):** *"When you try to download any model, … all the weights being downloaded actually, so it is not stored anywhere, it is part of the model architecture itself. … that is why there is no vector DB involved here. That is why I asked because in RAG there is a vector DB, but those are two very different things."*

The vector DB confusion comes from RAG, where external documents *are* encoded into vectors and stored in a database like FAISS, Pinecone, or Qdrant for retrieval. The base LLM itself has no vector DB.

**📚 Further reading:**
- [Mikolov 2013 — Word2Vec (original "similar words cluster" intuition)](https://arxiv.org/abs/1301.3781)
- [HF NLP Course — Loading models](https://huggingface.co/learn/llm-course/chapter2)

---

### Q4: "Why 768 dimensions? Who picks that number, and how is the embedding value computed?" (Navdas)

> **Student's question:** Can you please explain more about the 768-dimension embedding — how is the dimension chosen, and how is each embedding value computed?

**Answer (Tanishq):** `D` (the embedding / hidden dimension) is a **hyperparameter chosen at architecture design time**. It is fixed before training and stays the same throughout. Common values: 768 (BERT-base), 1024, 1280, 2048, 4096, 8192 (Llama-3). The individual float values in each row come from **random initialization → gradient descent** during pre-training. After training, they are frozen in the file you download.

**Key insight:** `D` is one of the most consequential decisions in model design — it dominates the parameter count of the embedding table (`|V| × D`) and the FFN expansion (`4D`). Increasing `D` improves expressivity roughly per the scaling-laws curve but costs memory linearly in attention layers and quadratically in attention compute.

**📚 Further reading:**
- [Kaplan et al., 2020 — Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)
- [HF NLP Course — Configuring a model](https://huggingface.co/learn/llm-course/chapter2)

---

### Q5: "When a wrong prediction is made during training, do the token embeddings get updated, or is that separate from the Q/K/V updates?" (Student follow-up)

> **Student's question:** During training, if the decoder predicts a wrong token, the loss is computed and backprop updates the weights of the decoder/encoder. Does it *also* update the token-to-vector (embedding) mappings, or is that a separate process?

**Answer (Tanishk):** Backpropagation updates **everything that is learnable in the architecture** — including the embedding matrix, the Q/K/V projection matrices, and the FFN layers. There is a distinction, though, between two kinds of parameters:

1. **Learnable parameters** — weights, biases, embeddings, Q/K/V matrices. Randomly initialized, updated by gradient descent during training.
2. **Non-learnable parameters** — tokenizer vocabulary, token-to-ID mapping, rules like BPE merges. These are computed once from a corpus (a "tokenizer training" pass) and then frozen.

> **Lecture's take (Tanishk):** *"There are two different types of parameters. One is learnable and one is not learnable, which is fixed. … position embeddings can be fixed or learnable based on whatever the architecture is, … embeddings are part of LLM call itself."*

**Key insight:** The Chinese-whispers analogy used in the session — once a token is wrong at the end, the gradient propagates *backwards through the entire network*, nudging every weight (including the lookup row for that token) by a small amount. This is what makes "the model learning language" possible at all.

**📚 Further reading:**
- [Goodfellow et al. — Deep Learning Ch. 8 (Optimization & Backprop)](https://www.deeplearningbook.org/)
- [Karpathy — Let's build GPT: backprop walkthrough](https://www.youtube.com/watch?v=kCc8FmEb1nY)

---

### Q6: "If a word/token wasn't in the training set, what does the model do? Hallucinate?" (Speaker 3)

> **Student's question:** Suppose my LLM was trained on 1 billion tokens and you give it a brand-new token at inference time. What happens — does the model learn it on the fly, or does it hallucinate?

**Answer (Tanishk + Tanishq):** The model **cannot learn anything new at inference** — weights are frozen. What happens depends on the tokenizer:

- **Word-level tokenizers** would throw an "unknown token" / `<unk>` error.
- **Sub-word (BPE) tokenizers** used by all modern LLMs will **decompose the new word into known sub-pieces**. "PromptForge" → "Prompt" + "Forge" (both likely in vocab). The LLM then *makes its best guess* from the sub-pieces it knows — which is exactly what "hallucination" means in the factual-definition sense: confidently outputting something plausible that may not be true.

> **Lecture's take (Tanishk):** *"LLM might not know what is promptforge, but it knows what is a prompt and what is forge. … So it will give you the most optimum meaning of the word. … So hallucination is just making up facts."*

**Key insight:** Hallucination is structural, not a bug — it is the model doing its job (predict the next token) with imperfect information. Techniques like RAG (give it the right docs), fine-tuning (bake corrections into weights), or tool calling (let it call a database) all chip away at the same root cause.

**📚 Further reading:**
- [Sennrich et al., 2016 — BPE for OOV handling](https://arxiv.org/abs/1508.07909)
- [Ji et al., 2023 — Survey of Hallucination in NLG](https://arxiv.org/abs/2202.03629)

---

### Q7: "How are Q, K, V matrices computed from the input embedding matrix in self-attention?" (Deeksha)

> **Student's question:** Can you explain how the QKV matrices are computed from the input embedding matrix in the self-attention mechanism? How is the projection matrix `W` itself computed?

**Answer (Tanishq + Tanishk):** Q, K, V are obtained by three **learnable linear projections** of the input embedding matrix X:

- `Q = X · W_Q`, `K = X · W_K`, `V = X · W_V` — where `W_Q`, `W_K`, `W_V` are `[D × d_k]` matrices that are randomly initialized and trained by gradient descent.
- The attention output is `softmax(Q·Kᵀ / √d_k) · V`.

The student-side confusion was whether there was a closed-form way to derive `W`. There is not — it is **trained**. The shared notes (linked by Tanishk in the group) show the full numerical computation for one attention head. Worth reading the notes end-to-end before the next session.

**Key insight:** The "Q, K, V" labels are mnemonic — they stand for Query, Key, Value — borrowed from information retrieval. The model learns to use K and V as content-addressable "what does this token represent?" lookup, and Q as the "what am I asking about?" token. The cross-attention to a vector DB works on exactly the same principle.

**📚 Further reading:**
- [Vaswani et al., 2017 — Attention Is All You Need (§3.2)](https://arxiv.org/abs/1706.03762)
- [Alammar — The Illustrated GPT-2 (Q/K/V visuals)](https://jalammar.github.io/illustrated-gpt2/)

---

### Q8: "Is KV cache the same as the (Q, K, V) matrices, or something different?" (Panush)

> **Student's question:** Is the KV cache the same as QKV, or is it completely different? Modern stuff is evolving — is this something we'll cover later?

**Answer (Tanishk):** The KV cache is built *from* the K and V tensors computed during self-attention — it is **not** the same thing as Q (Q is recomputed every token), nor is it a separate architecture. It is an **inference-time optimization**: cache the K and V projections of already-generated tokens so we don't have to recompute them for every new step.

> **Lecture's take (Tanishk):** *"KV cache is part of the same K and V values that we are training the model for … KV cache is getting cached in the transformer architecture as well."*

**Key insight:** The KV cache is what makes auto-regressive generation feasible at all. Without it, generating the 1000th token would require recomputing attention across all 999 prior tokens *and* their Q/K/V projections. With KV cache, each new step only computes Q for the new token and reuses the cached K and V from past tokens.

**📚 Further reading:**
- [HF — KV cache documentation](https://huggingface.co/docs/transformers/en/kv_cache)
- [Pope et al., 2023 — Efficiently Scaling Transformer Inference (No. 5 in ML theses)](https://arxiv.org/abs/2211.05102)

---

### Q9: "Can the FFN expand to more 'relatable' dimensions? How are those dimensions chosen?" (Student via sheet)

> **Student's question:** The feed-forward layer is transformed to more 'relatable' dimensions. How does it know or calculate the relative dimensions?

**Answer (Tanishq):** FFN expands the embedding dimension `D` to `4D` (typical — Llama uses a gated variant with `8D/3`), uses an activation (ReLU → SwiGLU in modern models), then projects back to `D`. The `4×` ratio is a *learned-from-experience* design choice carried over from the original transformer; it is not derived from first principles. The activation function is what gives the FFN its non-linear representational power (linear layers alone collapse to a single matrix).

> **Lecture's take (Tanishq):** *"Feed-forward layer just uses an activation function to expand the dimensions and get more features out of it. … from the input side, in the feed-forward network, when you give it D dimensions, then it expands into 4D dimensions. And then from the 4D dimension, the knowledge it gained, it again distills it to D dimension."*

**Key insight:** The FFN is where most of a transformer's parameters actually live (~⅔). Each FFN row can be loosely interpreted as a "detector" for a particular pattern; the attention layer decides which detectors to read from, the FFN applies them. This is one of the reasons models are so big — `4·D·D` is huge even for modest `D`.

**📚 Further reading:**
- [Vaswani et al., 2017 — §3.3 position-wise FFN](https://arxiv.org/abs/1706.03762)
- [Shazeer 2020 — GLU Variants Improve Transformer (SwiGLU)](https://arxiv.org/abs/2002.05202)

---

### Q10: "After the cohort, will I be ready to apply for FDE roles, or only contribute to my existing project?" (Sridhar)

> **Student's question:** After completing this cohort, will we be ready to fit into Forward Deployed Engineer (FDE) roles, or only to contribute to AI ideas within our existing project? Can I apply for new roles elsewhere?

**Answer (Tanishk):** Both. The target of the cohort is fundamentals broad enough for (a) interviews, (b) building systems at the current job, and (c) switching to a new role. Past cohorts have alumni who switched jobs *and* alumni who got internal funding for new AI projects at their existing company. Going forward, the cohort will share interview-question lists in the resource docs.

**📚 Further reading:**
- [Cohort One alumni outcomes & capstone highlights — sample: Shazeer 2020 (GLU Variants) was first-authored by an industry-practitioner track, illustrating the FDE/R&D overlap.]

---

### Q11: "How deep will EVALs and Guardrails be covered? Will it be a low-level example or a high-level explanation?" (Sridhar follow-up)

> **Student's question:** Will you cover low-level implementation of EVAL/Guardrails, or is it a high-level explanation? I want to know if I need to learn elsewhere.

**Answer (Tanishk):** Coverage will be **architecturally agnostic** and metric-driven — exact RAG-specific metrics, exact agent-specific metrics, exact multi-agent metrics. You'll get enough to apply these anywhere regardless of which framework you use.

**Key insight:** Modern EVAL suites are emerging as a category of their own (RAGAS, DeepEval, Phoenix, LangSmith Evals). The cohort will teach you *what to measure* (faithfulness, answer relevancy, context precision/recall, tool-call accuracy) rather than which vendor to use.

**📚 Further reading:**
- [Es et al., 2024 — RAGAS: Automated Evaluation of Retrieval Augmented Language Models](https://arxiv.org/abs/2309.15217)
- [Confident AI — DeepEval docs (open-source EVAL framework)](https://docs.confident-ai.com/)

---

### Q12: "What signals should I create to get noticed by AI recruiters, and which platform should I use?" (Collier Blake, JP Morgan)

> **Student's question:** What signals should I create to get noticed by AI recruiters, and which platform should I use to apply for remote AI jobs?

**Answer (Tanishk):** The advice generalises (LinkedIn is fine). The durable signal is **personal brand via public artifacts**:

1. Write blog posts distilling what you learn each week (week 1 done? → publish a blog about week 1).
2. Open-source repos with thoughtful READMEs ("here's what I was thinking when I built it").
3. Connect with the right people — quality of network > platform.

> **Lecture's take (Tanishk):** *"I have seen people getting job roles through their GitHub repos. So they have shared their GitHub repos, open-sourced, … and through that they were getting some job roles, right?"*

**Key insight:** For AI engineers in particular, the *demonstrable artifact* (a working RAG/agent project, a published eval harness, a 30-line LoRA you fine-tuned) is the densest signal — it filters for skill faster than a CV ever can.

---

### Q13: "How much transformer-internals depth is needed for AI engineering in practice?" (Poorna)

> **Student's question:** Which transformer architecture is used by major model providers? As a developer, how much depth should I know — will we implement any of this in production (agents, RAG) at software companies?

**Answer (Tanishk):** Basic understanding of how attention works is **beyond what is required** for most AI-engineering jobs. In practice you almost always use an API-hosted LLM and build **systems around it** (RAG, agents, evals, orchestration) — not models from scratch. Multi-agents are theoretically interesting but not widely used in production yet. The course covers RAG, agents, and multi-agents in depth.

**Key insight:** The bar for *frontier-lab* ML engineer is much higher than for an AI engineer shipping production apps. The cohort is calibrated for the latter — a working knowledge of the transformer (one layer + one head is enough), plus operational excellence around it.

---

### Q14: "If OpenAI upgrades from GPT-3.5 to GPT-5, do they train from scratch?" (Abhishek)

> **Student's question:** Once a model is trained and parameters are frozen, when the lab upgrades to the next version (GPT-3.5 → GPT-5), do they train from scratch again, or is it more like adding new libraries to existing software?

**Answer (Tanishk):** Labs **do not train from scratch** between versions (cost prohibitive). They run a **post-training cycle** — same base, additional SFT and preference-optimization passes on new data. Pre-training teaches language; post-training teaches conversation and instruction-following.

> **Lecture's take (Tanishk):** *"Inference is asking the question… post-training is the training phase."* **On the analogy:** *"When you are training a baby, the baby is only learning the language — words, how to build sentences. Those are part of pretraining. What happens in post-training is conversation, instruction-following — if someone asks me a question, I need to answer it."*

**Key insight:** Validation is *not* the same as post-training. Validation = the data split you hold out during a training run to estimate generalization. Post-training = the entire second stage (SFT + preference opt) that turns a base model into a chat/instruction model.

**📚 Further reading:**
- [Ouyang et al., 2022 — InstructGPT (RLHF pipeline)](https://arxiv.org/abs/2203.02155)
- [Raschka — Understanding the LLM Training Pipeline](https://sebastianraschka.com/blog/2023/llm-training-and-evaluation.html)

---

### Q15: "Is post-training and validation the same thing?" (Manasi)

> **Student's question:** Is post-training the same as validation?

**Answer (Tanishk):** **No.** Validation is the practice of holding out a fraction of the training data (typically 10–20%) to check generalization. Post-training is the second training stage (SFT + preference-opt) on curated data. Different concepts, different points in the pipeline.

> **Lecture's take (Tanishk):** *"Validation is just part of a data sampling thing. A post-training is like when we are training the model to do for a particular task, like conversation or anything else."*

**Key insight:** The classic test-set analogy: if your teacher gives you the exam questions in advance, you'll score 100% — but that doesn't mean you learned anything. Hold out a test set to avoid this "cheating."

---

### Q16: "How is orchestration used during training — Spark or something GPU-specific?" (Speaker 11, data-eng background)

> **Student's question:** In class we talked about orchestration. I'm from a data-engineering background — is Spark used to orchestrate model training, and how does that fit with the training infra we discussed?

**Answer (Tanishk):** There are **two kinds of orchestration** in this stack:

1. **Data orchestration (pre-training):** Spark (or Beam, Spark, Ray) used to scrape/curate/clean/PII-strip the trillion-token training corpus. *This* is the data-engineering angle.
2. **GPU/training orchestration:** distributing a single training run across thousands of GPUs (data/tensor/pipeline parallelism). This is a separate deep topic that will not be covered in this cohort (it would be its own full course).

---

### Q17: "How similar are diffusion / image models (ComfyUI) to LLMs?" (Sid + Arun)

> **Student's question:** How do diffusion models (ComfyUI in particular) relate to LLMs? Is there a similar Q/K/V + attention pipeline?

**Answer (Arun + Tanishk):** Diffusers and LLMs share the **transformer backbone + attention mechanism**. The differences:

- **Inputs:** LLMs process discrete text tokens; diffusion models process image patches (or VAE-encoded latent tokens).
- **Output:** LLMs produce next text token; diffusion models iteratively denoise a noise image into a clear image.
- **Adapters/LoRA:** LoRA on a diffusion model = fine-tune it to a specific character/style with curated image datasets; LoRA on an LLM = fine-tune it for a domain (legal / medical). Different mechanics, same overall goal.

> **Lecture's take (Arun):** *"Diffusion models are very similar to large language models. … the core architecture is not different, but the only thing is that we process and create data sets as images in the pixel space."*

**Key insight:** Sid's follow-up — *"can we have a subset of the neural network that understands one language and another subset that predicts upcoming tokens, plus extend the model by adding part of a neural network?"* — is the LoRA / adapter idea. In diffusion, character-LoRAs do exactly this (you keep the base model frozen and train a small adapter for "this character"). In LLMs, LoRA works the same way for domain adaptation. But mixing *vocabulary components* (DeepSeek tokenizer + Gemma attention) does not work, because each model's embedding table is trained against its own K/V projections.

**📚 Further reading:**
- [Ho et al., 2020 — Denoising Diffusion Probabilistic Models (DDPM)](https://arxiv.org/abs/2006.11239)
- [Rombach et al., 2021 — Latent Diffusion (Stable Diffusion)](https://arxiv.org/abs/2112.10752)
- [Hu et al., 2021 — LoRA: Low-Rank Adaptation](https://arxiv.org/abs/2106.09685)

---

### Q18: "If a system adapts to my preferences over a session, does it fine-tune itself?" (Ayush)

> **Student's question:** When I ask an LLM to not use emojis and it complies, is there some kind of penalisation happening under the hood? What's actually changing?

**Answer (Tanishk):** No fine-tuning at inference. The behaviour adapts because **either**:

1. **It's not an LLM, it's an agent** — modern apps (ChatGPT, Claude) are agents with external memory (CLAUDE.md, project skills, custom user preferences) that get re-injected into every call.
2. **Or the chat thread's prior messages are included in the context window** — so when you say "no emojis" mid-conversation, all subsequent messages include that instruction implicitly.

> **Lecture's take (Tanishk):** *"All of these are actually agents. They are no longer simple LLMs. They have an external memory, external context, which they are maintaining."*

**Key insight:** This is the central boundary between "LLM" and "agent system." A bare LLM has no persistent memory and never learns during inference. Anything that *seems* to remember preferences is an application-layer wrapper around the LLM (memory, skills, system prompts, RAG) feeding it context on every call.

---

### Q19: "How do you build a personal mind-map / flow-chart for the week-1 lectures?" (Ayush)

> **Student's question:** I've read the notes; how do I best connect the dots (basics of transformer architecture → training → …) into a single mind-map?

**Answer (Tanishk):** A practical workflow that works for him:

1. Collect a curated list of resources (papers, blogs, official docs).
2. Hand them to an LLM (Claude is recommended) with a structured prompt asking for a mind-map organised by topic.
3. Iterate — usually 2-3 rounds of "tighten this section" — to converge on a usable doc.
4. For visuals, enable the **Excalidraw MCP** in Claude to generate diagrams alongside.

> **Lecture's take (Tanishk):** *"I collect a bunch of good resources, … give it to Claude and I write a very structured prompt, can you help me build a structured mind map through all the topics which are mentioned there."*

**📚 Further reading:**
- [Anthropic — Claude with MCP tools (Excalidraw)](https://docs.anthropic.com/en/docs/build-with-claude/mcp)

---

## Key Themes

- **Architecture clarity.** The cohort needed to firm up the distinction between encoder/decoder, where embeddings live, what the KV cache is, and why FFN dimension is `4×`. → These ground Week 1's mental model of "what an LLM actually is."
- **Training-vs-inference confusion.** Several students conflated post-training with inference, and validation with post-training. → Worth surfacing explicitly even in well-prepared cohorts.
- **Hallucination as a structural feature.** Halting is not a bug, it is what an LLM does when given inputs it can't evaluate; the solution is more context (RAG, fine-tuning, tool calling).
- **Career outcomes / role calibration.** The cohort was reassured that fundamentals + portfolio artifacts are enough for either internal projects or job-switching, without needing to match frontier-lab ML depth.
- **Diffusion models as cousins, not strangers.** ComfyUI and LLMs share a transformer backbone, differ in input/output modalities. This previews the image-model content the cohort will hit later.

## Homework / Next Steps

- Read the **QKV math notes** linked by Tanishk before next week (the worked example for `W_Q`, `W_K`, `W_V` on a real sentence is referenced in this doubt session).
- Send any **persistent questions** to the cohort sheet; they will be picked up next networking call.
- Use the **resource doc** Tanishk mentioned for depth on RAG/agents/evals.
- Watch for the upcoming **fine-tuning lecture (Saturday / Sunday)** which will cover embedding updates, new-token handling, and post-training in detail.

## Key Takeaways

1. **Modern LLMs are decoder-only**; encoder-only models live on as embedding backbones for RAG; encoder-decoder is mostly historical (machine-translation-era).
2. **Embeddings are not stored in a vector DB** — they live inside the model weights as the embedding table. Vector DBs appear in RAG, which is a *separate* concept.
3. **Backprop updates everything learnable** — embeddings, Q/K/V matrices, FFN weights — during every training step. Tokenizer mappings are not learnable.
4. **KV cache ≠ QKV.** It is an inference-time optimization that caches previously-computed K and V tensors so each new token only recomputes Q.
5. **Hallucination = best-guess from subwords.** BPE tokenizers decompose unknown words into known pieces, and the model answers based on what it knows about the pieces.
6. **Pre-training teaches language; post-training teaches conversation.** Both are training (weights change). Validation is a held-out data split, *not* a separate training phase.
7. **For AI engineering roles, system-level depth matters more than transformer-internals depth.** API-hosted LLMs + a strong portfolio of RAG/agent/eval projects beat rewriting attention math from first principles.
8. **Personal brand via published artifacts** (blogs, open-source repos) is the highest-leverage signal to recruiters.

## Related Materials

- 📄 Raw transcript: [`transcripts/networking-session-1.srt`](../transcripts/networking-session-1.srt)
- 🕸️ Knowledge graph (visual): [`doubts-networking-week-1-graph.md`](doubts-networking-week-1-graph.md)
- 🧠 Knowledge graph (JSON): [`doubts-networking-week-1-graph.json`](doubts-networking-week-1-graph.json)
- 🌐 Combined view: [`combined-knowledge-graph.md`](combined-knowledge-graph.md)
- 🌱 Browse concepts: [`../concepts/index.md`](../concepts/index.md)
- 📝 Related teaching sessions: [R51 — LLM Basics & Transformer Internals](llm-basics-transformer-internals.md), [R52 — Training Pipeline, Tool Use & Fine-Tuning](llm-training-pipeline-tool-use.md)
