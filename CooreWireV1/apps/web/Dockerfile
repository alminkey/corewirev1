FROM node:22-alpine

WORKDIR /app/apps/web

COPY apps/web/package.json ./package.json
RUN npm install

COPY apps/web ./

CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0", "--port", "3000"]
