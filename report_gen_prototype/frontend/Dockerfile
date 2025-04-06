# Stage 1: Build the React app
FROM node:18-alpine AS builder

WORKDIR /app/frontend

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve with Nginx (Production)
FROM nginx:alpine AS production
COPY --from=builder /app/frontend/dist /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]