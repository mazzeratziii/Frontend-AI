FROM node:24-alpine@sha256:ebfe2f90462722a7a4de65e91990e97fe0d401c70e0e762c5b53302f905ec1c1 AS build
WORKDIR /workspace
RUN corepack enable
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml ./
COPY frontend/starter/package.json frontend/starter/package.json
COPY evaluator/package.json evaluator/package.json
RUN pnpm install --frozen-lockfile --filter frontend-experiment-starter...
COPY frontend/starter frontend/starter
RUN pnpm --dir frontend/starter build

FROM nginx:1.27-alpine@sha256:65645c7bb6a0661892a8b03b89d0743208a18dd2f3f17a54ef4b76fb8e2f2a10
COPY frontend/starter/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /workspace/frontend/starter/dist /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=5s --timeout=2s --retries=10 CMD wget -qO- http://127.0.0.1/healthz || exit 1