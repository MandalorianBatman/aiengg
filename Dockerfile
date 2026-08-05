# Multi-stage build for the AI Engineering Quartz site.
#
# Stage 1 (builder): install Node deps + Quartz plugins, run `npx quartz build`
# Stage 2 (runtime): nginx serving the static `public/` output.
#
# Build context must include the repo root (quartz/, aiengg/, package.json, ...).
# The Dockerfile path is `docker/Dockerfile` (CI passes it explicitly).

# ---- Builder ---------------------------------------------------------------
FROM node:22-alpine AS builder

# git is needed by `npx quartz plugin install` (resolves git URLs)
RUN apk add --no-cache git

WORKDIR /site

# Install deps first to maximize layer cache across content-only changes
COPY package.json package-lock.json* .npmrc* ./
# Use `npm install` rather than `npm ci` — `npm ci` interacts oddly with
# BuildKit layer caching in this configuration and we've seen it produce
# partial installs that cause the Quartz transpiled-cache loader to fail.
RUN npm install --no-audit --no-fund

# Bring in the Quartz source, the site config, and the content
COPY quartz/ ./quartz/
COPY quartz.ts tsconfig.json .prettier* .node-version globals.d.ts index.d.ts ./
COPY quartz.config.yaml ./
COPY aiengg/ ./aiengg/

# All plugins are npm packages (declared in package.json + installed above).
# We don't use any Git-based plugins, so the install-plugins step is unnecessary
# (and corrupts the plugin index in alpine — it reports 0 plugins despite
# 35 npm packages being available). Skip it.
# RUN ./node_modules/.bin/tsx ./quartz/plugins/loader/install-plugins.ts || true

# Ensure no stale transpiled-cache from a prior build attempt survives.
RUN rm -rf .quartz-cache quartz/.quartz-cache

# Build static site → /site/public. Invoke the bootstrap CLI via node directly
# — `npx quartz` is unreliable inside alpine (busybox env flags, bin lookup).
RUN node ./quartz/bootstrap-cli.mjs build -d aiengg -o public

# ---- Runtime ---------------------------------------------------------------
FROM nginx:1.27-alpine AS runtime

# Custom nginx config: port 3000 + Quartz-style clean URLs
# (Quartz links to /foo/bar but the file is /foo/bar.html).
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

# Static site from the builder
COPY --from=builder /site/public /usr/share/nginx/html

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --retries=5 --start-period=10s \
  CMD wget -q -O- http://127.0.0.1:3000/ >/dev/null || exit 1

CMD ["nginx", "-g", "daemon off;"]
