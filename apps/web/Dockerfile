FROM node:22-alpine

WORKDIR /app

COPY apps/web /app/apps/web
COPY package.json /app/package.json
COPY pnpm-workspace.yaml /app/pnpm-workspace.yaml

WORKDIR /app/apps/web

CMD ["sh", "-lc", "pnpm dev --hostname 0.0.0.0 --port 3000"]
