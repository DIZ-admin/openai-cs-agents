# ERNI Gruppe Building Agents - Quick Start Guide

## 🚀 Launch Full Stack Application

### 1. Start Backend (Python/FastAPI)
```bash
cd python-backend
.venv/bin/uvicorn api:app --host 127.0.0.1 --port 8000 --env-file .env --reload
```

**Backend URL:** http://127.0.0.1:8000  
**Terminal ID:** 293 (currently running)

### 2. Start Frontend (Next.js/React)
```bash
cd ui
npm run dev:next
```

**Frontend URL:** http://localhost:3000  
**Terminal ID:** 313 (currently running)

### 3. Open in Browser
The application should automatically open at:
- **http://localhost:3000**

If not, manually navigate to the URL above.

---

## ✅ Current Status

### Running Services
| Service | URL | Terminal | Status |
|---------|-----|----------|--------|
| Frontend | http://localhost:3000 | 313 | ✓ Running |
| Backend | http://127.0.0.1:8000 | 293 | ✓ Running |
| OpenAI API | https://api.openai.com | - | ✓ Connected |

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health
# Returns: {"status":"healthy",...}

# Backend readiness
curl http://localhost:8000/readiness
# Returns: {"status":"ready",...}

# Frontend → Backend proxy
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
# Returns: {"conversation_id":"...","current_agent":"Triage Agent",...}
```

---

## 🎯 How to Use

### Example Conversation Flow

1. **Open the application:** http://localhost:3000

2. **Start with a greeting:**
   ```
   "Hello, I want to build a house"
   ```
   → Triage Agent responds and offers options

3. **Request cost estimate:**
   ```
   "I need a cost estimate for a 150m² Einfamilienhaus"
   ```
   → Handoff to Cost Estimation Agent
   → Agent asks for construction type (Holzbau/Systembau)

4. **Provide details:**
   ```
   "Holzbau please"
   ```
   → Agent calculates estimate
   → Shows price range (CHF 450,000 - 562,500)

5. **Book consultation:**
   ```
   "I want to book a consultation with an architect"
   ```
   → Handoff to Appointment Booking Agent
   → Agent shows available specialists and time slots

6. **Check project status:**
   ```
   "What's the status of project 2024-156?"
   ```
   → Handoff to Project Status Agent
   → Shows current stage, progress, next milestone

---

## 🛑 Stop Services

### Stop Frontend
```bash
# Method 1: Press CTRL+C in terminal 313
# Method 2: Kill by port
kill $(lsof -ti:3000)
```

### Stop Backend
```bash
# Method 1: Press CTRL+C in terminal 293
# Method 2: Kill by port
kill $(lsof -ti:8000)
```

### Stop Both
```bash
kill $(lsof -ti:3000) $(lsof -ti:8000)
```

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Browser (http://localhost:3000)                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Next.js Frontend (React 19)                          │  │
│  │  • Agent Panel (left)                                 │  │
│  │  • Chat Interface (right)                             │  │
│  └───────────────────────────────────────────────────────┘  │
│                    ↓ /chat (Next.js rewrite)                │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  FastAPI Backend (http://127.0.0.1:8000)              │  │
│  │  • 6 Specialized Agents                               │  │
│  │  • Guardrails (Relevance, Jailbreak)                  │  │
│  │  • Context Management                                 │  │
│  └───────────────────────────────────────────────────────┘  │
│                    ↓ OpenAI API                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  OpenAI Platform (gpt-4.1-mini)                       │  │
│  │  • Agent orchestration                                │  │
│  │  • Natural language processing                        │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Troubleshooting

### Frontend not loading
```bash
# Check if port 3000 is free
lsof -ti:3000

# Restart frontend
kill $(lsof -ti:3000)
cd ui && npm run dev:next
```

### Backend not responding
```bash
# Check if port 8000 is free
lsof -ti:8000

# Restart backend
kill $(lsof -ti:8000)
cd python-backend && .venv/bin/uvicorn api:app --host 127.0.0.1 --port 8000 --reload
```

### Chat not working
1. Check browser console (F12) for errors
2. Verify backend is running: `curl http://localhost:8000/health`
3. Check proxy configuration in `ui/next.config.mjs`

---

## 📚 Documentation

- **Frontend Guide:** `ui/FRONTEND_GUIDE.md`
- **Backend Guide:** `python-backend/SERVER_CONTROL.md`
- **Agent Documentation:** `.augment/rules/AGENTS.md`
- **Deployment Guide:** `DEPLOYMENT.md`
- **README:** `README.md`

---

## 🎨 UI Features

### Agent Panel (Left - 60%)
- **Available Agents:** Shows all 6 ERNI agents
- **Guardrails:** Security checks (Relevance, Jailbreak)
- **Context:** Customer and project data
- **Runner Output:** Real-time agent events

### Chat Interface (Right - 40%)
- **Message History:** All conversation messages
- **Input Field:** Type and send messages
- **Loading Indicator:** Shows when agent is processing
- **Markdown Support:** Rich text formatting

---

## 🌟 Key Features

✓ **6 Specialized Agents:**
  - Triage Agent (routing)
  - Project Information Agent
  - Cost Estimation Agent
  - Project Status Agent
  - Appointment Booking Agent
  - FAQ Agent

✓ **Intelligent Routing:**
  - Automatic handoff between agents
  - Context preservation across handoffs

✓ **Security:**
  - Relevance Guardrail (topic filtering)
  - Jailbreak Guardrail (prompt injection protection)

✓ **Bilingual Support:**
  - German and English

✓ **Real-time Updates:**
  - Live agent switching
  - Context updates
  - Event logging

---

**Last Updated:** 2025-10-04  
**Status:** ✅ All systems operational  
**Version:** 1.0.0-staging
