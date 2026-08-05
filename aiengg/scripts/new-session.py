#!/usr/bin/env python3
"""Extract metadata from an SRT transcript and generate template files for a new session."""

import re, sys, json, os
from datetime import timedelta
from pathlib import Path

def parse_srt(path):
    segments = []
    with open(path) as f:
        content = f.read()

    pattern = re.compile(
        r'(\d+)\n'
        r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})\n'
        r'(.*?)(?=\n\d+\n|\Z)',
        re.DOTALL
    )

    for m in pattern.finditer(content):
        idx = int(m.group(1))
        start = timedelta(hours=int(m.group(2)), minutes=int(m.group(3)),
                          seconds=int(m.group(4)), milliseconds=int(m.group(5)))
        end = timedelta(hours=int(m.group(6)), minutes=int(m.group(7)),
                        seconds=int(m.group(8)), milliseconds=int(m.group(9)))
        text = m.group(10).strip()
        speaker = "Unknown"
        speaker_match = re.match(r'Speaker (\d+):\s*(.*)', text, re.DOTALL)
        if speaker_match:
            speaker = f"Speaker {speaker_match.group(1)}"
            text = speaker_match.group(2).strip()
        segments.append({
            "index": idx, "start": start, "end": end, "text": text, "speaker": speaker
        })
    return segments

def extract_metadata(segments, srt_path):
    if not segments:
        print("No segments found."); sys.exit(1)

    duration = segments[-1]["end"]
    hours, remainder = divmod(int(duration.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    speakers = {}
    for seg in segments:
        sp = seg["speaker"]
        speakers[sp] = speakers.get(sp, 0) + 1

    speaker_list = sorted(speakers.items(), key=lambda x: -x[1])

    # Extract early content for topic suggestion
    early_text = " ".join(seg["text"] for seg in segments[:50])

    return {
        "filename": os.path.basename(srt_path),
        "duration": duration_str,
        "speaker_count": len(speakers),
        "segment_count": len(segments),
        "speakers": [{"id": s[0], "segments": s[1]} for s in speaker_list],
        "early_content": early_text[:2000],
    }

def generate_templates(meta, slug, srt_path):
    out_dir = Path("/tmp/aiengg_new_session")
    out_dir.mkdir(exist_ok=True)

    # Session summary template
    summary = f"""# <Session Title>

**Source:** [`transcripts/{meta['filename']}`](../transcripts/{meta['filename']})
**Recording:** <NUMBER>
**Instructor:** <NAME (Speaker ID)>
**Duration:** {meta['duration']}
**Type:** Teaching | Doubt Solving
**Speakers:** {meta['speaker_count']} speakers ({', '.join(s['id'] for s in meta['speakers'][:5])}...)

## Session Goals

- <Goal 1>
- <Goal 2>
- <Goal 3>

## Agenda

1. <Topic>
2. <Topic>

## <Section>

### <Concept Name>

> **Lecture's take:** <What the instructor said>

**Canonical definition:** <From paper/blog>

**Key insight:** <Why this matters>

**📚 Further reading:**
- [<Title>](<URL>)

## Q&A Highlights

| Question | Answer |
|----------|--------|
| <Q> | <A> |

## Key Takeaways

1. <Takeaway>
2. <Takeaway>

## Related Materials

- 🕸️ Knowledge graph (visual): [`{slug}-graph.md`]({slug}-graph.md)
- 🧠 Knowledge graph (JSON): [`{slug}-graph.json`]({slug}-graph.json)
- 🌐 Combined view: [`combined-knowledge-graph.md`](combined-knowledge-graph.md)
- 🌱 Browse concepts: [`../concepts/index.md`](../concepts/index.md)
"""
    (out_dir / f"{slug}.md").write_text(summary)

    # Visual graph template
    graph_md = f"""# Knowledge Graph — <Session Title>

**Source:** [`transcripts/{meta['filename']}`](../transcripts/{meta['filename']})

## Concept Map

```mermaid
graph TD
    <Add your diagram here>
```

## Concept Hierarchy

| Layer | Concept | One-liner | Further Reading |
|-------|---------|-----------|-----------------|
| <Cat> | <Concept> | <One-liner> | [<Title>](<URL>) |

## Key Q&A Recorded

| Question | Answer |
|----------|--------|
| <Q> | <A> |

## Key Takeaways

1. <Takeaway>

## Related Materials

- 📝 Session summary: [`{slug}.md`]({slug}.md)
- 🌱 Browse concepts: [`../concepts/index.md`](../concepts/index.md)
"""
    (out_dir / f"{slug}-graph.md").write_text(graph_md)

    # JSON template
    graph_json = {
        "source": meta["filename"],
        "title": "<Session Title>",
        "instructor": "<NAME>",
        "duration": meta["duration"],
        "speaker_count": meta["speaker_count"],
        "segment_count": meta["segment_count"],
        "cohort": "AI Engineering Cohort (InterviewReady / Gaurav Sen)",
        "session_goals": [],
        "concepts": [],
        "qa_themes": [],
        "key_takeaways": [],
        "entities": {"people": [], "datasets": [], "papers": [], "models_referenced": [], "vendors_mentioned": []}
    }
    json_path = out_dir / f"{slug}-graph.json"
    json_path.write_text(json.dumps(graph_json, indent=2))
    print(f"JSON template → {json_path}")

    print(f"\nTemplates generated in {out_dir}/")
    print(f"  {slug}.md            — session summary")
    print(f"  {slug}-graph.md     — visual knowledge graph")
    print(f"  {slug}-graph.json   — structured knowledge graph")

def suggest_slug(meta):
    text = meta["early_content"].lower()
    keywords = {
        "llm": ["llm", "large language model", "language model"],
        "transformer": ["transformer", "attention", "feed forward", "encoder", "decoder"],
        "training": ["training", "pre-train", "pretrain", "fine-tun", "sft", "supervised"],
        "inference": ["inference", "serving", "deploy", "latency", "throughput"],
        "token": ["token", "bpe", "byte pair", "embedding", "vocabulary"],
        "tool-calling": ["tool call", "function call", "agent", "api call"],
        "preference": ["preference", "rlhf", "dpo", "ppo", "grpo", "reward"],
        "rag": ["rag", "retrieval", "vector db", "embedding"],
        "quantization": ["quantize", "quantization", "int8", "int4", "gguf", "gptq"],
        "evaluation": ["eval", "benchmark", "metric", "accuracy", "perplexity"],
        "data": ["data", "dataset", "pipeline", "filter", "dedup"],
        "prompt": ["prompt", "few-shot", "chain of thought"],
        "multimodal": ["multimodal", "vision", "image", "audio", "video model"],
    }

    scores = {}
    for slug, terms in keywords.items():
        scores[slug] = sum(1 for t in terms if t in text)

    top = sorted(scores.items(), key=lambda x: -x[1])[:3]
    top = [t for t in top if t[1] > 0]

    if top:
        slug = "-".join(t[0] for t in top[:2])
        print(f"\nSuggested slug: {slug} (detected topics: {', '.join(t[0] for t in top)})")
        print("Review and adjust based on the full transcript content.")
        return slug
    else:
        print("\nNo strong topic signals detected. Use a descriptive slug based on the transcript content.")
        return "<descriptive-slug>"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 new-session.py <path/to/transcript.srt> [optional-slug]")
        sys.exit(1)

    srt_path = sys.argv[1]
    if not os.path.exists(srt_path):
        print(f"File not found: {srt_path}"); sys.exit(1)

    print(f"Parsing {srt_path}...")
    segments = parse_srt(srt_path)
    meta = extract_metadata(segments, srt_path)

    print(f"\n=== Metadata ===")
    print(f"  Duration:       {meta['duration']}")
    print(f"  Speakers:       {meta['speaker_count']}")
    print(f"  Segments:       {meta['segment_count']}")
    print(f"\n=== Speaker Breakdown ===")
    for s in meta["speakers"][:10]:
        print(f"  {s['id']:15s} {s['segments']:5d} segments")
    if len(meta["speakers"]) > 10:
        print(f"  ... and {len(meta['speakers']) - 10} more")

    slug = sys.argv[2] if len(sys.argv) > 2 else suggest_slug(meta)

    print(f"\n=== Early Transcript (first 500 chars) ===")
    print(meta["early_content"][:500])

    generate_templates(meta, slug, srt_path)
