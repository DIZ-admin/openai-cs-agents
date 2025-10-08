# ERNI Gruppe Building Agents - Project Planning

## 🎯 Project Vision

AI-powered multi-agent customer service system for ERNI Gruppe, a leading Swiss timber construction company. The system provides intelligent customer support for building projects, cost estimation, project status tracking, and consultation scheduling.

## 🏗️ Architecture Overview

### Technology Stack

**Backend:**
- Python 3.11+ with FastAPI
- OpenAI Agents SDK 0.3.3
- Pydantic for data validation
- Uvicorn/Gunicorn ASGI server

**Frontend:**
- Next.js 15.5.4 with App Router
- React 19
- TypeScript 5.x
- Tailwind CSS

**Infrastructure:**
- Docker & Docker Compose
- PostgreSQL 14+ (production)
- Redis 7.x (caching & rate limiting)
- Nginx reverse proxy

### Multi-Agent System

The system consists of 6 specialized AI agents:

1. **Triage Agent** - Main entry point and intelligent routing
2. **Project Information Agent** - General building and construction information
3. **Cost Estimation Agent** - Preliminary project cost calculations
4. **Project Status Agent** - Real-time project tracking and updates
5. **Appointment Booking Agent** - Consultation scheduling with specialists
6. **FAQ Agent** - Answers to common building questions with website links

### Key Features

- ✅ Intelligent agent routing and handoffs
- ✅ Context preservation across agent transitions
- ✅ Bilingual support (German/English)
- ✅ Input guardrails (relevance & jailbreak protection)
- ✅ Rate limiting and security measures
- ✅ Comprehensive testing (228 tests, 90%+ coverage)
- ✅ Production-ready deployment configuration

## 🚀 Deployment Modes

### Development Mode
- Debug enabled
- Hot reload
- Detailed logging
- Local environment

### Staging Mode
- Production-like configuration
- Reduced debug output
- Rate limiting enabled
- Staging domain CORS

### Production Mode
- Full security measures
- SSL/HTTPS
- Database integration
- Monitoring and logging

## 📋 Project Constraints

1. **API Dependencies:**
   - Requires valid OpenAI API key
   - Vector Store ID for FAQ knowledge base

2. **Environment Variables:**
   - Must be configured before running
   - Different keys for dev/staging/production

3. **System Requirements:**
   - Python 3.9+
   - Node.js 18+
   - 2GB RAM minimum (4GB recommended)

4. **Security:**
   - Never commit API keys to version control
   - Use environment-specific configurations
   - Rotate secrets every 90 days

## 🎯 Current Scope

### In Scope
- Multi-agent conversation system
- Cost estimation for building projects
- Project status tracking
- Consultation booking
- FAQ with website links
- Health checks and monitoring
- Comprehensive testing

### Out of Scope (Future Versions)
- Database integration (v1.1)
- User authentication (v1.1)
- Multi-language support beyond German/English (v1.1)
- Mobile app (v2.0)
- Voice interface (v2.0)
- Document upload and analysis (v2.0)

## 📊 Project Status

**Version:** 1.0.0
**Status:** Ready for Staging Deployment
**Test Coverage:** 90.04% (228 tests passing)
**Last Updated:** October 5, 2025

## 🔗 Key Documentation

- [README.md](README.md) - Quick start and overview
- [AGENTS.md](AGENTS.md) - Complete technical documentation
- [STAGING_DEPLOYMENT.md](python-backend/docs/STAGING_DEPLOYMENT.md) - Staging deployment guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment guide

