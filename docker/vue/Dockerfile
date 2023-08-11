# Develop stage
FROM node:alpine as develop-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Build stage
FROM develop-stage as build-stage
RUN npm run build

# Production stage
FROM nginx:alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]