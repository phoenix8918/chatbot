# Stage 1: Build
FROM node:20-alpine AS build
WORKDIR /app

# Optional: environment variable
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# 1️⃣ Copy package files and install deps (including Tailwind)
COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps --no-audit --no-fund

# 2️⃣ Copy the source
COPY . .

# 3️⃣ Build the app
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
