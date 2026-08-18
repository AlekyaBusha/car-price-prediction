# Deployment Guide

This document covers deployment strategies for the Used Car Price Prediction platform across production environments.

---

## 1. Production Architecture Overview

The system consists of two primary tiers:
1. **Frontend**: Static Single Page Application (SPA) built with React + Vite.
2. **Backend**: Asynchronous REST API service powered by FastAPI and Uvicorn with an in-memory XGBoost model and SHAP TreeExplainer.

```
Client Browser <---> [ Nginx / CDN / Vercel ]
                           │
                           ▼ (Reverse Proxy / CORS)
                     [ FastAPI (Uvicorn) ]
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
       [ XGBoost ]    [ SHAP Tree ]  [ Datasets ]
       (In-Memory)     Explainer     (In-Memory)
```

---

## 2. Docker Deployment

### 2.1 Backend Dockerfile (`backend/Dockerfile`)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code, models, and data
COPY backend/ ./backend/

EXPOSE 8000

CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### 2.2 Frontend Dockerfile (`frontend/Dockerfile`)

```dockerfile
# Stage 1: Build React static bundle
FROM node:18-alpine AS builder
WORKDIR /app
COPY frontend/vite-project/package*.json ./
RUN npm ci
COPY frontend/vite-project/ ./
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 2.3 Docker Compose (`docker-compose.yml`)

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
    restart: always

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: always
```

---

## 3. Cloud Platform Deployment

### 3.1 Backend Deployment (Render / Railway / AWS EC2)

1. **Build Command**: `pip install -r backend/requirements.txt`
2. **Start Command**: `uvicorn backend.api.main:app --host 0.0.0.0 --port $PORT`
3. **Environment Variables**:
   - `PORT=8000`

### 3.2 Frontend Deployment (Vercel / Netlify / Cloudflare Pages)

1. **Root Directory**: `frontend/vite-project`
2. **Build Command**: `npm run build`
3. **Output Directory**: `dist`
4. **Environment Variables**:
   - `VITE_API_URL=https://your-backend-domain.com`

---

## 4. Production Checklist

- [x] CORS configured for production domain in `backend/api/main.py`
- [x] Pre-trained `xgb_model.pkl` loaded into memory at startup (< 500ms startup)
- [x] `npm run build` passes with zero linting errors
- [x] All 44 reference feature columns schema-aligned
