FROM node:24-bookworm-slim@sha256:0e0ff40c39bc087845bfb27465a0df4ea419520094bc35842ff83dd8cbe6f9b6
WORKDIR /workspace
ENV PLAYWRIGHT_CHROMIUM_EXECUTABLE=/usr/bin/chromium
RUN apt-get update     && apt-get install -y --no-install-recommends chromium ca-certificates fonts-liberation     && rm -rf /var/lib/apt/lists/*
RUN corepack enable
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml ./
COPY frontend/starter/package.json frontend/starter/package.json
COPY evaluator/package.json evaluator/package.json
RUN pnpm install --frozen-lockfile --filter frontend-experiment-evaluator...
COPY evaluator evaluator
CMD ["pnpm", "--dir", "evaluator", "test"]