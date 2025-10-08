# ERNI Gruppe Building Agents - Docker Deployment Guide

**Complete guide for Docker-based deployment and testing**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Configuration Options](#configuration-options)
4. [Deployment Methods](#deployment-methods)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)
7. [Production Deployment](#production-deployment)

---

## ✅ Prerequisites

### Required Software

- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **OpenAI API Key**

### Verify Installation

```bash
# Check Docker version
docker --version
# Expected: Docker version 20.10.0 or higher

# Check Docker Compose version
docker-compose --version
# Expected: Docker Compose version 2.0.0 or higher

# Verify Docker is running
docker ps
# Should show running containers or empty list (no errors)
```

---

## 🚀 Quick Start

### Step 1: Clone and Navigate

```bash
cd /Users/kostas/Documents/Projects/openai-cs-agents-demo
```

### Step 2: Configure Environment

The `.env` file already exists in `python-backend/.env` with your OpenAI API key.

**Verify it contains:**
```bash
cat python-backend/.env | grep OPENAI_API_KEY
```

**Expected output:**
```
OPENAI_API_KEY=sk-proj-...
```

### Step 3: Build Containers

```bash
# Build all containers (first time or after code changes)
docker-compose -f docker-compose.simple.yml build

# This will take 5-10 minutes on first build
```

### Step 4: Start Services

```bash
# Start all services in foreground (see logs)
docker-compose -f docker-compose.simple.yml up

# OR start in background (detached mode)
docker-compose -f docker-compose.simple.yml up -d
```

### Step 5: Verify Services

**Check container status:**
```bash
docker-compose -f docker-compose.simple.yml ps
```

**Expected output:**
```
NAME              STATUS         PORTS
erni-backend      Up (healthy)   0.0.0.0:8000->8000/tcp
erni-frontend     Up (healthy)   0.0.0.0:3000->3000/tcp
erni-nginx        Up             0.0.0.0:80->80/tcp
```

### Step 6: Access Application

- **Frontend (Next.js):** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Nginx Proxy:** http://localhost

### Step 7: Test FAQ Agent

Open http://localhost:3000 and ask:
```
Где на сайте почитать о ремонте крыши?
```

**Expected:** Response with clickable links in format `[Text](https://www.erni-gruppe.ch/...)`

---

## ⚙️ Configuration Options

### Environment Variables

**Location:** `python-backend/.env`

**Key Variables:**

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | ✅ Yes |
| `ENVIRONMENT` | Environment name | development | No |
| `DEBUG` | Debug mode | false | No |
| `LOG_LEVEL` | Logging level | INFO | No |
| `RATE_LIMIT_PER_MINUTE` | API rate limit | 60 | No |
| `RATE_LIMIT_PER_HOUR` | API rate limit | 1000 | No |

### Docker Compose Files

**Two configurations available:**

1. **`docker-compose.simple.yml`** (Recommended for testing)
   - Backend + Frontend + Nginx
   - No database or Redis
   - Fast startup
   - Ideal for development and testing

2. **`docker-compose.yml`** (Full production setup)
   - Backend + Frontend + Nginx + PostgreSQL + Redis
   - Complete production stack
   - Slower startup
   - Ideal for production deployment

---

## 🔧 Deployment Methods

### Method 1: Simple Deployment (Recommended)

**Use case:** Quick testing, development, FAQ Agent validation

```bash
# Build
docker-compose -f docker-compose.simple.yml build

# Start
docker-compose -f docker-compose.simple.yml up

# Stop
docker-compose -f docker-compose.simple.yml down
```

**Services:**
- ✅ Backend API (port 8000)
- ✅ Frontend (port 3000)
- ✅ Nginx (port 80)

### Method 2: Full Production Deployment

**Use case:** Production environment with database and caching

```bash
# Build
docker-compose build

# Start
docker-compose up -d

# Stop
docker-compose down
```

**Services:**
- ✅ Backend API (port 8000)
- ✅ Frontend (port 3000)
- ✅ Nginx (port 80, 443)
- ✅ PostgreSQL (port 5432)
- ✅ Redis (port 6379)

### Method 3: Development Mode

**Use case:** Active development with hot reload

```bash
# Backend only (with hot reload)
cd python-backend
source .venv/bin/activate
uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Frontend only (with hot reload)
cd ui
npm run dev
```

---

## 🧪 Testing

### 1. Health Checks

**Backend health:**
```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-04T...",
  "version": "1.0.0",
  "environment": "development"
}
```

**Frontend health:**
```bash
curl http://localhost:3000
```

**Expected:** HTML response (Next.js page)

### 2. API Testing

**Test chat endpoint:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Где на сайте почитать о ремонте крыши?",
    "conversation_id": "test-123"
  }'
```

**Expected:** JSON response with FAQ Agent answer including clickable URLs

### 3. FAQ Agent Link Testing

**Test cases:**

1. **Roof maintenance (Russian):**
   ```
   Где на сайте почитать о ремонте крыши?
   ```
   Expected: Links to Dachservice & Unterhalt page

2. **Planning services (German):**
   ```
   Welche Planungsdienstleistungen bietet ERNI an?
   ```
   Expected: Links to Planung pages

3. **Contact (English):**
   ```
   How can I contact ERNI?
   ```
   Expected: Links to contact and location pages

### 4. Container Logs

**View all logs:**
```bash
docker-compose -f docker-compose.simple.yml logs -f
```

**View specific service logs:**
```bash
# Backend logs
docker-compose -f docker-compose.simple.yml logs -f backend

# Frontend logs
docker-compose -f docker-compose.simple.yml logs -f frontend

# Nginx logs
docker-compose -f docker-compose.simple.yml logs -f nginx
```

---

## 🔍 Troubleshooting

### Issue 1: Containers Won't Start

**Symptoms:**
- `docker-compose up` fails
- Containers exit immediately

**Solutions:**

1. **Check Docker is running:**
   ```bash
   docker ps
   ```

2. **Check port conflicts:**
   ```bash
   # Check if ports are already in use
   lsof -i :8000  # Backend
   lsof -i :3000  # Frontend
   lsof -i :80    # Nginx
   ```

3. **Stop conflicting services:**
   ```bash
   # If you have services running from previous tests
   pkill -f uvicorn
   pkill -f "npm run dev"
   ```

4. **Rebuild containers:**
   ```bash
   docker-compose -f docker-compose.simple.yml down
   docker-compose -f docker-compose.simple.yml build --no-cache
   docker-compose -f docker-compose.simple.yml up
   ```

### Issue 2: Backend Health Check Fails

**Symptoms:**
- Backend container shows "unhealthy" status
- Health check endpoint returns errors

**Solutions:**

1. **Check backend logs:**
   ```bash
   docker-compose -f docker-compose.simple.yml logs backend
   ```

2. **Verify OpenAI API key:**
   ```bash
   docker-compose -f docker-compose.simple.yml exec backend env | grep OPENAI_API_KEY
   ```

3. **Test health endpoint manually:**
   ```bash
   docker-compose -f docker-compose.simple.yml exec backend curl http://localhost:8000/health
   ```

4. **Restart backend:**
   ```bash
   docker-compose -f docker-compose.simple.yml restart backend
   ```

### Issue 3: Frontend Build Fails

**Symptoms:**
- Frontend container fails to build
- "Module not found" errors

**Solutions:**

1. **Check Next.js configuration:**
   ```bash
   cat ui/next.config.mjs
   ```
   Should contain: `output: 'standalone'`

2. **Clear build cache:**
   ```bash
   rm -rf ui/.next ui/node_modules
   docker-compose -f docker-compose.simple.yml build --no-cache frontend
   ```

3. **Check Node version:**
   ```bash
   docker-compose -f docker-compose.simple.yml run frontend node --version
   ```
   Should be: v20.x.x

### Issue 4: FAQ Agent Not Providing Links

**Symptoms:**
- FAQ Agent responds but without URLs
- Links are not in markdown format

**Solutions:**

1. **Verify sitemap is in Vector Store:**
   - Check that `erni_sitemap.json` was uploaded to Vector Store
   - Vector Store ID: `vs_68e14a087e3c8191b4b7483ba3cb8d2a`

2. **Check FAQ Agent instructions:**
   ```bash
   grep -A 20 "CRITICAL - PROVIDING WEBSITE LINKS" python-backend/main.py
   ```

3. **Restart backend to reload instructions:**
   ```bash
   docker-compose -f docker-compose.simple.yml restart backend
   ```

4. **Test with explicit question:**
   ```
   Где на сайте почитать о ремонте крыши?
   ```

### Issue 5: Nginx Proxy Not Working

**Symptoms:**
- http://localhost doesn't work
- 502 Bad Gateway errors

**Solutions:**

1. **Check nginx logs:**
   ```bash
   docker-compose -f docker-compose.simple.yml logs nginx
   ```

2. **Verify upstream services are healthy:**
   ```bash
   docker-compose -f docker-compose.simple.yml ps
   ```
   Both backend and frontend should show "Up (healthy)"

3. **Test direct access:**
   ```bash
   curl http://localhost:8000/health  # Backend
   curl http://localhost:3000         # Frontend
   ```

4. **Restart nginx:**
   ```bash
   docker-compose -f docker-compose.simple.yml restart nginx
   ```

### Issue 6: Permission Denied Errors

**Symptoms:**
- "Permission denied" when accessing files
- Container fails to write logs

**Solutions:**

1. **Fix file permissions:**
   ```bash
   chmod -R 755 python-backend
   chmod -R 755 ui
   chmod -R 755 nginx
   ```

2. **Check volume permissions:**
   ```bash
   docker-compose -f docker-compose.simple.yml down -v
   docker-compose -f docker-compose.simple.yml up
   ```

---

## 🚀 Production Deployment

### Prerequisites

1. **SSL Certificates** (for HTTPS)
2. **Domain name** configured
3. **Production environment variables**

### Steps

1. **Update nginx configuration:**
   ```bash
   # Edit nginx/nginx.conf
   # Replace yourdomain.com with your actual domain
   ```

2. **Set production environment:**
   ```bash
   # In python-backend/.env
   ENVIRONMENT=production
   DEBUG=false
   ```

3. **Use full docker-compose:**
   ```bash
   docker-compose build
   docker-compose up -d
   ```

4. **Configure SSL:**
   ```bash
   # Place SSL certificates in nginx/ssl/
   # fullchain.pem
   # privkey.pem
   # chain.pem
   ```

5. **Enable HTTPS:**
   - Nginx will automatically redirect HTTP to HTTPS
   - Access via https://yourdomain.com

---

## 📊 Monitoring

### Container Status

```bash
# Check all containers
docker-compose -f docker-compose.simple.yml ps

# Check resource usage
docker stats
```

### Logs

```bash
# Real-time logs (all services)
docker-compose -f docker-compose.simple.yml logs -f

# Last 100 lines
docker-compose -f docker-compose.simple.yml logs --tail=100

# Specific service
docker-compose -f docker-compose.simple.yml logs -f backend
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost:3000

# Nginx health
curl http://localhost/health
```

---

## 🛑 Stopping Services

### Stop All Services

```bash
# Stop containers (keep data)
docker-compose -f docker-compose.simple.yml down

# Stop and remove volumes (delete all data)
docker-compose -f docker-compose.simple.yml down -v
```

### Stop Specific Service

```bash
docker-compose -f docker-compose.simple.yml stop backend
docker-compose -f docker-compose.simple.yml stop frontend
docker-compose -f docker-compose.simple.yml stop nginx
```

### Restart Service

```bash
docker-compose -f docker-compose.simple.yml restart backend
```

---

## 📝 Common Commands Cheat Sheet

```bash
# Build all containers
docker-compose -f docker-compose.simple.yml build

# Start all services (foreground)
docker-compose -f docker-compose.simple.yml up

# Start all services (background)
docker-compose -f docker-compose.simple.yml up -d

# Stop all services
docker-compose -f docker-compose.simple.yml down

# View logs
docker-compose -f docker-compose.simple.yml logs -f

# Check status
docker-compose -f docker-compose.simple.yml ps

# Rebuild and restart
docker-compose -f docker-compose.simple.yml up --build

# Execute command in container
docker-compose -f docker-compose.simple.yml exec backend bash

# Remove all containers and volumes
docker-compose -f docker-compose.simple.yml down -v
```

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] All containers are running: `docker-compose ps`
- [ ] Backend health check passes: `curl http://localhost:8000/health`
- [ ] Frontend is accessible: `curl http://localhost:3000`
- [ ] Nginx proxy works: `curl http://localhost`
- [ ] FAQ Agent provides links: Test with roof maintenance question
- [ ] Links are clickable markdown format
- [ ] No errors in logs: `docker-compose logs`

---

## 🎯 Next Steps

1. ✅ **Docker setup complete**
2. ⏳ **Test FAQ Agent with sitemap**
3. ⏳ **Validate link functionality**
4. ⏳ **Deploy to production** (if needed)

---

**Deployment ready!** 🚀

For questions or issues, check the troubleshooting section or review container logs.

