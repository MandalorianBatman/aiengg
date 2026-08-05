#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

: "${IMAGE:?IMAGE must be set}"

if [ "${SKIP_GIT_SYNC:-false}" != "true" ]; then
  git fetch --prune origin
  git reset --hard origin/main
fi

docker pull "$IMAGE"

cd docker
docker compose pull
IMAGE="$IMAGE" docker compose up -d --remove-orphans

docker image prune -f
