# ERNI Gruppe Building Agents - Server Control Guide

## 🚀 Quick Start

### Start Server (Staging Mode)
```bash
cd python-backend
.venv/bin/uvicorn api:app --host 127.0.0.1 --port 8000 --env-file .env --reload
```

### Start Server (Production Mode)
```bash
cd python-backend
.venv/bin/uvicorn api:app --host 0.0.0.0 --port 8000 --env-file .env.production --workers 4
```

## 🛑 Stop Server

### Method 1: Interactive Terminal
If server is running in foreground:
```bash
Press CTRL+C
```

### Method 2: Kill by Port
```bash
kill $(lsof -ti:8000)
```

### Method 3: Kill by Process Name
```bash
pkill -f "uvicorn api:app"
```

## 🔍 Server Status

### Check if Server is Running
```bash
lsof -ti:8000 && echo "Server is running" || echo "Server is not running"
```

### Check Server Health
```bash
curl http://localhost:8000/health
```

### Check Server Readiness
```bash
curl http://localhost:8000/readiness
```

## 📊 Monitoring

### View Real-time Logs
If server is running in background (Terminal ID 293):
```bash
# Use the read-process tool in IDE
# Or check the terminal output directly
```

### Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, I want to build a house"}' | python3 -m json.tool
```

## 🧪 Testing

### Run All Tests
```bash
cd python-backend
.venv/bin/python -m pytest tests/ -v
```

### Run Tests with Coverage
```bash
.venv/bin/python -m pytest tests/ -v --cov=. --cov-report=html
```

### Run Specific Test File
```bash
.venv/bin/python -m pytest tests/integration/test_api_endpoints.py -v
```

## 🌐 Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Main chat endpoint for agent orchestration |
| GET | `/health` | Health check endpoint |
| GET | `/readiness` | Readiness check endpoint |
| GET | `/docs` | OpenAPI documentation (Swagger UI) |
| GET | `/redoc` | ReDoc documentation |

## ⚙️ Configuration

### Environment Files
- `.env` - Current environment (copied from `.env.staging`)
- `.env.staging` - Staging configuration
- `.env.production` - Production configuration (not created yet)

### Key Environment Variables
```bash
ENVIRONMENT=staging
DEBUG=false
LOG_LEVEL=INFO
OPENAI_API_KEY=sk-proj-...
CORS_ORIGINS=https://staging.erni-gruppe.ch
RATE_LIMIT_PER_MINUTE=10
```

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -ti:8000

# Kill the process
kill $(lsof -ti:8000)
```

### Dependencies Not Installed
```bash
cd python-backend
.venv/bin/pip install -r requirements.txt
```

### Virtual Environment Not Found
```bash
cd python-backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### OpenAI API Key Not Set
1. Edit `.env` file
2. Set `OPENAI_API_KEY=sk-proj-your-key-here`
3. Restart server

## 📝 Current Server Status

**Server:** Running ✓  
**Terminal ID:** 293  
**URL:** http://127.0.0.1:8000  
**Port:** 8000  
**Mode:** Staging (with --reload)  
**Process ID:** 87709  

**Health Checks:**
- `/health` → ✓ healthy
- `/readiness` → ✓ ready
- OpenAI API → ✓ connected

**Tests:**
- Total: 228 passed
- Coverage: 90.04%
- Status: ✓ All passing

## 🎯 Next Steps

1. **Open API Documentation:**
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

2. **Test Different Scenarios:**
   ```bash
   # Cost estimation
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "I want a cost estimate for a 150m² house"}'
   
   # Project status
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "What is the status of project 2024-156?"}'
   
   # Book consultation
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "I want to book a consultation with an architect"}'
   ```

3. **Monitor Performance:**
   - Check response times
   - Monitor OpenAI API usage
   - Review logs for errors

4. **Prepare for Production:**
   - Create `.env.production` file
   - Set production CORS origins
   - Configure production database (if needed)
   - Set up proper logging
   - Configure monitoring and alerting

## 📚 Additional Resources

- **Project Documentation:** `README.md`
- **Staging Deployment Guide:** `STAGING_DEPLOYMENT.md`
- **Agent Documentation:** `.augment/rules/AGENTS.md`
- **Test Documentation:** `tests/README.md`
- **Changelog:** `CHANGELOG.md`

---

**Last Updated:** 2025-10-04  
**Server Version:** 1.0.0-staging  
**Python Version:** 3.13  
**OpenAI Agents SDK:** 0.3.3

