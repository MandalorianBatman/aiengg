# AI Engineering Docsify Container

Serves the AI Engineering knowledge base as a docsify site, exposed over Tailscale.

> **Content lives in [`aiengg/`](aiengg/README.md)** — session summaries, knowledge graphs, concept pages, and transcripts.

## URL

**Tailnet (private):** https://omarchy.barbel-polaris.ts.net/

## Structure

```
aiengg-docsify/
├── Dockerfile
├── docker-compose.yml
├── README.md               # this file
└── aiengg/                 # mounted at /docs in the container
    ├── sessions/           # lecture summaries + knowledge graphs
    ├── concepts/           # digital garden of interlinked concept pages
    ├── transcripts/        # raw diarized SRT files
    └── scripts/            # new-session.py helper
```

## Usage

```bash
cd /home/zed/aiengg-docsify
docker compose up -d --build
docker logs -f aiengg-docsify
docker compose down
```

## Container details

| Setting | Value |
|---------|-------|
| Image | `node:21-alpine` + `docsify-cli@latest` |
| Port | `3000` (127.0.0.1 only — proxied via Tailscale) |
| Volume | `./aiengg:/docs:ro` |
| Restart | `unless-stopped` |

## Why `--ignore-scripts`?

`docsify-cli`'s post-install runs `opencollective-postinstall && npx husky install`.
`husky` isn't available on Alpine (no bash path in npx context), so the install fails.
The hook is purely a sponsorship nag — the CLI works fine without it.
