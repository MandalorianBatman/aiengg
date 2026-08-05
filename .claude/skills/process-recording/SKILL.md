---
name: process-recording
description: Use when the user provides a class recording URL (typically aiengg.dev/learn/.../class-recording-NN) and wants the lecture turned into a published knowledge-base entry. Triggers on: new recording URL, "process this recording", "ingest new lecture", "add this to notes".
---

# Process a Class Recording

End-to-end pipeline that takes a recording URL through to a git-pushed docsify update. Chains three existing skills and adds the commit/push.

## Pipeline

1. **Download** — invoke the `aiengg-download` skill with the URL. Capture the local `.mp4` path from its one-line summary (e.g. `OK: class-recording-42.mp4 | ...`).
2. **Transcribe** — invoke the `transcribe-recording` skill with the `.mp4` path. It writes `<basename>.txt` and `<basename>.srt` next to the video. Run in the background — GPU-bound, 30-90 min for a 2-hr recording.
3. **Stage the SRT** — copy the SRT into the repo at `aiengg/transcripts/<basename>.srt` so the next step finds it where it expects.
4. **Notes** — invoke the `aiengg-notes` skill with the SRT path. It writes the session summary, knowledge graphs (visual + JSON), concept pages, and updates the indexes, sidebar, and README.
5. **Commit and push** — `git add` the changes under `aiengg/`, commit with a Conventional Commits message, and `git push origin main`.

## Required sub-skills

Each step requires invoking the corresponding skill in turn — read the skill's `SKILL.md` for its flags and gotchas:

- `aiengg-download` — video download
- `transcribe-recording` — speaker-attributed transcript + SRT
- `aiengg-notes` — session summary, knowledge graph, concept pages

If any sub-skill is missing, fails, or produces output you can't validate, abort and surface the error. Do not push a half-finished pipeline.

## Commit message

Use Conventional Commits style:

```
recordings: add <slug> session and <N> new concepts
```

For multiple sessions in one batch, list each slug.

## Gotchas

- The `.mp4` / SRT basename usually matches the URL's `class-recording-NN` number — the `aiengg-notes` skill suggests a topic slug from transcript content, not the URL.
- `transcribe-recording` is slow; verify the GPU is free (`nvidia-smi`) before starting so a stuck container doesn't OOM the run.
- Review the diff before pushing. If concept pages or the combined knowledge graph look off (broken backlinks, fabricated URLs), fix them locally — never push known-bad output.
- The three sub-skills must be invoked in this order. Skipping a step (e.g. generating notes from the raw `.mp4` without an SRT) breaks the chain.