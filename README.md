# AI Engineering Quartz Site

AI Engineering knowledge base, built with [Quartz 5](https://quartz.jzhao.xyz/) and
served as a static site over Tailscale.

> **Content lives in [`aiengg/`](aiengg/README.md)** — session summaries, knowledge graphs, and concept pages.

## URL

**Tailnet (private):** https://aiengg.kasat.xyz

## Structure

```
aiengg-docsify/
├── Dockerfile                 # multi-stage: Node builder → nginx runtime
├── docker-compose.yml         # local dev (builds from repo root)
├── docker/
│   ├── Dockerfile             # CI uses this (same as top-level)
│   └── docker-compose.yml     # production compose (pulls pre-built image)
├── quartz/                    # Quartz source (vendored from jackyzha0/quartz@v5)
├── quartz.config.yaml         # site config (title, baseUrl, plugins, layout)
├── package.json               # npm scripts (`npm run build` → static site)
├── aiengg/                    # Quartz content directory (passed via `-d aiengg`)
│   ├── README.md              # homepage
│   ├── sessions/              # lecture summaries + Mermaid knowledge graphs
│   ├── concepts/              # digital garden of interlinked concept pages
│   ├── transcripts/           # raw SRT (gitignored, not rendered)
│   └── scripts/               # new-session.py helper (not rendered)
└── scripts/
    ├── add-frontmatter.py     # one-shot helper to add YAML frontmatter
    └── deploy.sh              # called by GitHub Actions deploy workflow
```

## Local dev

```bash
npm install
npm run serve     # hot-reload preview at http://localhost:8080
npm run build     # one-shot build → ./public
```

Or via Docker (matches production):
```bash
docker compose up -d --build
docker logs -f aiengg-quartz
docker compose down
```

## Deployment

CI builds the image on every push to `main` and pushes to GHCR:

- `ci.yml` — builds `docker/Dockerfile` from repo root (context: `.`) with the
  Quartz content + config baked in. Image tag: `ghcr.io/mandalorianbatman/aiengg-docsify:${{ github.sha }}`.
- `deploy.yml` — pulls the new image and runs `scripts/deploy.sh`, which restarts
  the container via `docker/docker-compose.yml` (proxied via Tailscale).

## Interlinking & graph

Each session/concept page uses standard Markdown links (`[Text](other-page.md)`).
Quartz's **Backlinks** and **Graph** plugins pick these up automatically and render
the interactive graph view in the right sidebar of every page. To group notes for
the Explorer / tag pages, each file carries YAML frontmatter (`title`, `tags`).
Run `python3 scripts/add-frontmatter.py` to (re)generate it across `aiengg/`.

## Container details

| Setting | Value |
|---------|-------|
| Builder | `node:22-alpine` (Quartz build → `public/`) |
| Runtime | `nginx:1.27-alpine` (serves `public/` on port 3000) |
| Port | `3000` (Tailscale proxy) |
| Volume | none — content baked into the image at build time |
| Restart | `unless-stopped` |
