# 🚀 ERNI Gruppe Building Agents - Staging Deployment Guide

**Version:** 1.0.0-staging  
**Date:** October 4, 2025  
**Status:** Ready for Staging Deployment

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Deployment Steps](#deployment-steps)
4. [Health Checks](#health-checks)
5. [Testing](#testing)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)
8. [Rollback Procedure](#rollback-procedure)

---

## 🔧 Prerequisites

### Required Software
- **Python:** 3.9 or higher
- **pip:** Latest version
- **Git:** For version control
- **OpenAI API Key:** Staging environment key

### System Requirements
- **RAM:** Minimum 2GB (4GB recommended)
- **CPU:** 2 cores minimum
- **Disk:** 1GB free space
- **Network:** HTTPS access to OpenAI API

### Access Requirements
- SSH access to staging server
- OpenAI API key with sufficient credits
- Staging domain configured (e.g., `staging.erni-gruppe.ch`)

---

## ⚙️ Environment Setup

### Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/your-org/erni-building-agents.git
cd erni-building-agents/python-backend

# Checkout staging branch (if exists)
git checkout staging
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -E "fastapi|openai|slowapi"
```

### Step 4: Configure Environment Variables

```bash
# Copy staging environment template
cp .env.staging .env

# Edit .env file and configure:
nano .env  # or use your preferred editor
```

**Required configurations:**
1. **OPENAI_API_KEY:** Your staging OpenAI API key
2. **CORS_ORIGINS:** Your staging domain (e.g., `https://staging.erni-gruppe.ch`)
3. **SECRET_KEY:** Generate with `openssl rand -hex 32`

**Example:**
```env
OPENAI_API_KEY=sk-proj-abc123...
CORS_ORIGINS=https://staging.erni-gruppe.ch
SECRET_KEY=a1b2c3d4e5f6...
```

---

## 🚀 Deployment Steps

### Step 1: Run Tests

```bash
# Run all tests to ensure everything works
python -m pytest tests/ -v

# Expected output:
# ===== 228 passed in X.XXs =====
```

### Step 2: Start the Server

**Option A: Development Server (for testing)**
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --env-file .env
```

**Option B: Production Server (recommended for staging)**
```bash
# Using Gunicorn with Uvicorn workers
gunicorn api:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  --log-level info
```

**Option C: Background Process**
```bash
# Run in background with nohup
nohup uvicorn api:app --host 0.0.0.0 --port 8000 --env-file .env > logs/app.log 2>&1 &

# Save process ID
echo $! > server.pid
```

### Step 3: Verify Server Started

```bash
# Check if process is running
ps aux | grep uvicorn

# Check logs
tail -f logs/app.log

# Expected output:
# INFO: Started server process [PID]
# INFO: Application startup complete.
# INFO: Uvicorn running on http://0.0.0.0:8000
```

---

## ✅ Health Checks

### Basic Health Check

```bash
# Health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","timestamp":"2025-10-04T..."}
```

### Readiness Check

```bash
# Readiness endpoint
curl http://localhost:8000/readiness

# Expected response:
# {"status":"ready","checks":{"openai":"ok","storage":"ok"}}
```

### Agents List

```bash
# Get all available agents
curl http://localhost:8000/agents | python -m json.tool

# Expected response: List of 6 agents
# - triage_agent
# - faq_agent
# - project_information_agent
# - cost_estimation_agent
# - project_status_agent
# - appointment_booking_agent
```

---

## 🧪 Testing

### Test 1: Simple Chat Request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, I want to build a house",
    "conversation_id": "test-001"
  }' | python -m json.tool
```

**Expected:** Response from triage_agent with welcome message

### Test 2: Rate Limiting

```bash
# Send 12 requests rapidly (limit is 10/minute)
for i in {1..12}; do
  echo "Request $i:"
  curl -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d "{\"message\":\"Test $i\",\"conversation_id\":\"test-$i\"}" \
    -w "\nHTTP Status: %{http_code}\n\n"
  sleep 0.5
done
```

**Expected:** 
- Requests 1-10: HTTP 200
- Requests 11-12: HTTP 429 (Too Many Requests)

### Test 3: Agent Handoff

```bash
# Test handoff from triage to cost estimation
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need a cost estimate for a house",
    "conversation_id": "test-handoff"
  }' | python -m json.tool
```

**Expected:** Handoff event to `cost_estimation_agent`

### Test 4: Guardrails

```bash
# Test relevance guardrail (should be blocked)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Write a poem about strawberries",
    "conversation_id": "test-guardrail"
  }' | python -m json.tool
```

**Expected:** Refusal message about building-related topics only

---

## 📊 Monitoring

### Check Logs

```bash
# Real-time logs
tail -f logs/app.log

# Search for errors
grep -i error logs/app.log

# Search for warnings
grep -i warning logs/app.log
```

### Monitor Memory Usage

```bash
# Check memory usage of Python process
ps aux | grep uvicorn | awk '{print $4, $11}'

# Monitor in real-time
watch -n 5 'ps aux | grep uvicorn'
```

### Monitor Conversation Storage

```bash
# Check number of active conversations (requires Python)
python -c "
from api import conversation_store
print(f'Active conversations: {len(conversation_store._conversations)}')
print(f'Timestamps: {len(conversation_store._timestamps)}')
"
```

---

## 🔧 Troubleshooting

### Issue 1: Server Won't Start

**Symptoms:** `uvicorn` command fails or exits immediately

**Solutions:**
```bash
# Check Python version
python --version  # Should be 3.9+

# Check if port is already in use
lsof -i :8000
# If occupied, kill the process or use different port

# Check environment variables
cat .env | grep OPENAI_API_KEY
# Ensure API key is set

# Check dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue 2: OpenAI API Errors

**Symptoms:** 401 Unauthorized or 429 Rate Limit errors

**Solutions:**
```bash
# Verify API key is valid
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Check API key in .env
grep OPENAI_API_KEY .env

# Check OpenAI account credits
# Visit: https://platform.openai.com/account/usage
```

### Issue 3: CORS Errors

**Symptoms:** Browser shows CORS policy errors

**Solutions:**
```bash
# Check CORS configuration
grep CORS_ORIGINS .env

# Ensure staging domain is included
# Example: CORS_ORIGINS=https://staging.erni-gruppe.ch

# Restart server after changing .env
pkill -f uvicorn
uvicorn api:app --host 0.0.0.0 --port 8000 --env-file .env
```

### Issue 4: Rate Limiting Too Strict

**Symptoms:** Legitimate requests getting 429 errors

**Solutions:**
```bash
# Increase rate limit in .env
echo "RATE_LIMIT_PER_MINUTE=30" >> .env

# Or modify in api.py (line 190)
# @limiter.limit("30/minute")

# Restart server
```

### Issue 5: Memory Leak

**Symptoms:** Memory usage grows continuously

**Solutions:**
```bash
# Check conversation count
python -c "from api import conversation_store; print(len(conversation_store._conversations))"

# If > 1000, cleanup should trigger automatically
# If not, check TTL settings in .env

# Manual cleanup (restart server)
pkill -f uvicorn
uvicorn api:app --host 0.0.0.0 --port 8000 --env-file .env
```

---

## ⏮️ Rollback Procedure

### Quick Rollback

```bash
# Stop current server
pkill -f uvicorn

# Checkout previous version
git checkout <previous-commit-hash>

# Reinstall dependencies (if changed)
pip install -r requirements.txt

# Restart server
uvicorn api:app --host 0.0.0.0 --port 8000 --env-file .env
```

### Full Rollback

```bash
# 1. Stop server
pkill -f uvicorn

# 2. Backup current state
cp -r . ../backup-$(date +%Y%m%d-%H%M%S)

# 3. Restore from backup
cp -r ../previous-backup/* .

# 4. Restore environment
cp .env.backup .env

# 5. Restart server
source .venv/bin/activate
uvicorn api:app --host 0.0.0.0 --port 8000 --env-file .env
```

---

## 📞 Support

**Issues:** Create an issue on GitHub  
**Email:** support@erni-gruppe.ch  
**Documentation:** See README.md and AGENTS.md

---

**Last Updated:** October 4, 2025  
**Maintained By:** ERNI Gruppe Development Team

