#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

: "${IMAGE:?IMAGE must be set}"

if [ "${SKIP_GIT_SYNC:-false}" != "true" ]; then
  git fetch --prune origin
  git reset --hard origin/main
fi

# Pull the exact SHA-tagged image so we know what's running.
docker pull "$IMAGE"

cd docker
# Use the explicit SHA tag — `--pull never` because we just pulled above
# and don't want compose to chase the `latest` tag and overshoot our SHA.
IMAGE="$IMAGE" docker compose --project-name aiengg up -d \
  --remove-orphans \
  --force-recreate \
  --pull never \
  aiengg-docsify

docker image prune -f
