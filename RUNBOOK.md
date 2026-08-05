# aiengg Runbook

## Architecture

```
GitHub push to main
   │
   ├─→ ci.yml      (builds ghcr.io/mandalorianbatman/aiengg-docsify:<sha> + :latest)
   └─→ deploy.yml  (self-hosted runner `batserver-aiengg`)
                     │
                     ▼
              /home/zed/dev/ci-cd/aiengg   ←── syncs repo, runs scripts/deploy.sh
                     │
                     ▼
              aiengg-docsify (container on services_network, port 3000)
                     │
                     ▼
              Traefik (Host: aiengg.kasat.xyz)
                     │
                     ▼
              cloudflared → Cloudflare edge → https://aiengg.kasat.xyz
```

## Deploy

Push to `main` triggers:
1. `.github/workflows/ci.yml` — builds & pushes image.
2. `.github/workflows/deploy.yml` — self-hosted runner pulls image, syncs, runs `scripts/deploy.sh`.

To force a redeploy:
```bash
gh workflow run deploy.yml -R MandalorianBatman/aiengg
```

## Verify

```bash
# Container is up
ssh zed@batserver 'docker ps --filter name=aiengg-docsify --format "{{.Names}} {{.Status}}"'

# Public reachability
curl -fsS https://aiengg.kasat.xyz | head -3
```
