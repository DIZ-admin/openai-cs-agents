# ERNI Gruppe Building Agents - Docker Quick Start

**One-command deployment for testing and development**

---

## 🚀 Quick Start (3 Steps)

### Step 1: Build Containers

```bash
./docker-build.sh
```

**What it does:**
- ✅ Checks Docker is running
- ✅ Verifies environment configuration
- ✅ Builds backend container
- ✅ Builds frontend container
- ✅ Pulls nginx image

**Time:** ~5-10 minutes (first time)

---

### Step 2: Start Services

```bash
./docker-start.sh
```

**What it does:**
- ✅ Starts all containers
- ✅ Waits for services to be healthy
- ✅ Shows service status

**Time:** ~30 seconds

---

### Step 3: Test Deployment

```bash
./docker-test.sh
```

**What it does:**
- ✅ Tests backend health
- ✅ Tests frontend accessibility
- ✅ Tests nginx proxy
- ✅ Tests chat API
- ✅ Tests FAQ Agent with sitemap links

**Time:** ~10 seconds

---

## 🌐 Access Points

Once services are running:

- **Frontend (Next.js):** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Nginx Proxy:** http://localhost

---

## 🧪 Testing FAQ Agent

Open http://localhost:3000 and ask:

**Test 1 (Russian):**
```
Где на сайте почитать о ремонте крыши?
```

**Expected:** Response with clickable links like:
```
🔧 [Dachservice & Unterhalt](https://www.erni-gruppe.ch/spenglerei/dachservice-unterhalt)
```

**Test 2 (German):**
```
Welche Planungsdienstleistungen bietet ERNI an?
```

**Expected:** Response with planning service links

**Test 3 (English):**
```
How can I contact ERNI?
```

**Expected:** Response with contact page links

---

## 📊 Useful Commands

### View Logs

```bash
# All services
docker-compose -f docker-compose.simple.yml logs -f

# Specific service
docker-compose -f docker-compose.simple.yml logs -f backend
docker-compose -f docker-compose.simple.yml logs -f frontend
docker-compose -f docker-compose.simple.yml logs -f nginx
```

### Check Status

```bash
docker-compose -f docker-compose.simple.yml ps
```

### Restart Service

```bash
docker-compose -f docker-compose.simple.yml restart backend
docker-compose -f docker-compose.simple.yml restart frontend
docker-compose -f docker-compose.simple.yml restart nginx
```

### Stop All Services

```bash
docker-compose -f docker-compose.simple.yml down
```

### Rebuild After Code Changes

```bash
./docker-build.sh
./docker-start.sh
```

---

## 🔧 Troubleshooting

### Issue: "Docker is not running"

**Solution:**
```bash
# Start Docker Desktop
open -a Docker
# Wait for Docker to start, then try again
```

### Issue: "Port already in use"

**Solution:**
```bash
# Stop any running services
docker-compose -f docker-compose.simple.yml down

# Kill processes using ports
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
lsof -ti:80 | xargs kill -9    # Nginx

# Try again
./docker-start.sh
```

### Issue: "Backend health check failed"

**Solution:**
```bash
# Check backend logs
docker-compose -f docker-compose.simple.yml logs backend

# Verify OpenAI API key
cat python-backend/.env | grep OPENAI_API_KEY

# Restart backend
docker-compose -f docker-compose.simple.yml restart backend
```

### Issue: "FAQ Agent not providing links"

**Solution:**
```bash
# Verify sitemap file exists
ls -la python-backend/data/erni_sitemap.json

# Check FAQ Agent instructions
grep -A 10 "CRITICAL - PROVIDING WEBSITE LINKS" python-backend/main.py

# Rebuild backend
docker-compose -f docker-compose.simple.yml build backend
docker-compose -f docker-compose.simple.yml restart backend
```

---

## 📁 Project Structure

```
openai-cs-agents-demo/
├── docker-compose.simple.yml    # Simplified Docker Compose config
├── docker-build.sh              # Build script
├── docker-start.sh              # Start script
├── docker-test.sh               # Test script
├── python-backend/
│   ├── Dockerfile               # Backend container definition
│   ├── .env                     # Environment variables
│   ├── main.py                  # Agent definitions
│   ├── api.py                   # FastAPI application
│   └── data/
│       ├── erni_knowledge_base.json
│       └── erni_sitemap.json    # Website sitemap
├── ui/
│   ├── Dockerfile               # Frontend container definition
│   └── next.config.mjs          # Next.js config (with standalone output)
└── nginx/
    └── nginx.simple.conf        # Nginx configuration
```

---

## 🎯 What's Included

### Backend (Python/FastAPI)
- ✅ 6 specialized AI agents
- ✅ FAQ Agent with sitemap integration
- ✅ Enhanced instructions for link provision
- ✅ OpenAI Agents SDK
- ✅ Vector Store integration
- ✅ Health check endpoint

### Frontend (Next.js)
- ✅ Modern chat interface
- ✅ Bilingual support (German/English)
- ✅ Standalone build for Docker
- ✅ API proxy configuration

### Nginx
- ✅ Reverse proxy
- ✅ Request routing
- ✅ Static file caching
- ✅ Health check passthrough

---

## 🔐 Environment Variables

**Location:** `python-backend/.env`

**Required:**
- `OPENAI_API_KEY` - Your OpenAI API key

**Optional:**
- `ENVIRONMENT` - Environment name (default: development)
- `DEBUG` - Debug mode (default: false)
- `LOG_LEVEL` - Logging level (default: INFO)
- `RATE_LIMIT_PER_MINUTE` - API rate limit (default: 60)
- `RATE_LIMIT_PER_HOUR` - API rate limit (default: 1000)

---

## 📚 Additional Documentation

- **Full Docker Guide:** `DOCKER_DEPLOYMENT_GUIDE.md`
- **Agent Documentation:** `.augment/rules/AGENTS.md`
- **FAQ Agent Fix:** `FAQ_AGENT_LINK_FIX.md`
- **Testing Guide:** `TESTING_GUIDE.md`
- **Sitemap Integration:** `SITEMAP_INTEGRATION_REPORT.md`

---

## ✅ Success Checklist

After running all scripts, verify:

- [ ] All containers are running: `docker-compose -f docker-compose.simple.yml ps`
- [ ] Backend is healthy: `curl http://localhost:8000/health`
- [ ] Frontend is accessible: `curl http://localhost:3000`
- [ ] Nginx proxy works: `curl http://localhost`
- [ ] FAQ Agent provides links: Test with roof maintenance question
- [ ] Links are in markdown format: `[Text](URL)`
- [ ] No errors in logs: `docker-compose -f docker-compose.simple.yml logs`

---

**Ready to deploy!** 🚀

Run `./docker-build.sh` to get started.

