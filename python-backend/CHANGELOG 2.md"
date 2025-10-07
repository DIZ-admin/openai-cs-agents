# Changelog

All notable changes to the ERNI Gruppe Building Agents project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0-staging] - 2025-10-04

### 🎉 Initial Staging Release

First staging-ready release of the ERNI Gruppe Building Agents system.

### ✨ Added

#### Phase 1: Critical Fixes
- **CORS Configuration** - Dynamic CORS origins from environment variables
  - Replaced hardcoded `localhost:3000` with `CORS_ORIGINS` from `.env`
  - Restricted allowed methods to `["GET", "POST"]`
  - Restricted allowed headers to `["Content-Type", "Authorization"]`
  - File: `api.py` (lines 46-52)

- **OpenAI Model Updates** - Fixed invalid model names
  - Updated `gpt-5-mini` → `gpt-4o-mini` (main agents)
  - Updated `gpt-5-nano` → `gpt-4o-mini` (guardrails)
  - Updated all test files to expect `gpt-4o-mini`
  - Files: `main.py` (lines 63-65), 6 test files

- **Rate Limiting** - Protection against API abuse
  - Added `slowapi==0.1.9` dependency
  - Configured rate limiter: 10 requests/minute per IP
  - Added `RateLimitExceeded` exception handler
  - Applied `@limiter.limit("10/minute")` to `/chat` endpoint
  - File: `api.py` (lines 47-49, 190)

- **Error Handling** - Comprehensive error management
  - Wrapped `chat_endpoint` in try-except block
  - Added handling for `InputGuardrailTripwireTriggered`
  - Added handling for `HTTPException` (re-raise)
  - Added catch-all `Exception` handler with logging
  - Returns HTTP 500 with user-friendly error message
  - File: `api.py` (lines 197-424)

- **In-Memory Storage Limits** - Memory leak prevention
  - Added `_max_conversations = 1000` limit
  - Added `_ttl_seconds = 3600` (1 hour TTL)
  - Implemented `_cleanup_old_conversations()` method
  - Implemented `_enforce_size_limit()` method
  - Added logging for cleanup operations
  - File: `api.py` (lines 135-188)

#### Phase 2: Important Improvements
- **Code Quality** - Flake8 compliance
  - Moved `load_dotenv()` after all imports
  - Fixed all 15 E402 violations
  - Zero Flake8 errors remaining
  - File: `api.py` (lines 1-38)

- **Documentation** - Added missing docstrings
  - `cost_estimation_instructions` in `main.py`
  - `project_status_instructions` in `main.py`
  - `appointment_booking_instructions` in `main.py`
  - `ConversationStore.get` and `.save` in `api.py`
  - `make_agent_dict` in `api.py`
  - Files: `main.py`, `api.py`

- **Dependencies** - Cleaned up requirements
  - Removed duplicate `httpx==0.28.1` entry
  - File: `requirements.txt`

#### Phase 3: Staging Deployment
- **Environment Configuration**
  - Created `.env.staging` template with staging-specific settings
  - Configured for `ENVIRONMENT=staging`, `DEBUG=false`
  - Added security warnings and setup instructions
  - File: `.env.staging`

- **Deployment Documentation**
  - Created comprehensive `STAGING_DEPLOYMENT.md` guide
  - Includes prerequisites, setup steps, health checks
  - Includes testing procedures and troubleshooting
  - Includes rollback procedures
  - File: `STAGING_DEPLOYMENT.md`

- **Project Documentation**
  - Updated `README.md` with staging deployment section
  - Added testing section (228 tests, 90.04% coverage)
  - Added links to new documentation files
  - File: `README.md`

- **Version History**
  - Created `CHANGELOG.md` for tracking changes
  - File: `CHANGELOG.md` (this file)

### 🔧 Changed
- CORS configuration now uses environment variables instead of hardcoded values
- OpenAI model names updated to valid current models
- Error handling improved with comprehensive try-except blocks
- In-memory storage now has TTL and size limits

### 🐛 Fixed
- Invalid OpenAI model names (`gpt-5-mini`, `gpt-5-nano` don't exist)
- Hardcoded CORS origins (security risk)
- Missing rate limiting (abuse vulnerability)
- Insufficient error handling (poor user experience)
- Unlimited in-memory storage (memory leak risk)
- Flake8 E402 violations (code quality)
- Missing docstrings (documentation gaps)
- Duplicate dependencies in requirements.txt

### 🧪 Testing
- ✅ All 228 tests passing (100%)
- ✅ Code coverage: 90.04% (exceeds 80% requirement)
- ✅ Unit tests: 90-100% coverage
- ✅ Integration tests: 100% coverage
- ✅ Flake8: 0 errors

### 📊 Metrics
- **Test Suite:** 228 tests, 1.07s execution time
- **Code Coverage:** 90.04% (2941 statements, 293 missed)
- **Code Quality:** Flake8 clean, all public functions documented
- **Performance:** Rate limited to 10 req/min per IP

### 🚀 Deployment
- **Status:** Ready for staging deployment
- **Requirements:** Python 3.9+, OpenAI API key
- **Configuration:** See `.env.staging` and `STAGING_DEPLOYMENT.md`
- **Health Checks:** `/health` and `/readiness` endpoints available

### 📝 Notes
- In-memory storage is suitable for staging but NOT for production
- For production, implement Redis or PostgreSQL storage
- Rate limiting is conservative (10/min) - adjust based on usage
- All critical security issues resolved
- All critical functionality tested and working

### 🔗 References
- **Staging Guide:** [STAGING_DEPLOYMENT.md](STAGING_DEPLOYMENT.md)
- **Agent Documentation:** [AGENTS.md](../AGENTS.md)
- **API Documentation:** http://localhost:8000/docs (when running)

---

## [Unreleased]

### Planned for Future Releases

#### v1.1.0 - Production Readiness
- [ ] Replace in-memory storage with Redis
- [ ] Add PostgreSQL for persistent data
- [ ] Implement email notifications for consultations
- [ ] Add Sentry for error tracking
- [ ] Add Prometheus metrics
- [ ] Add Grafana dashboards
- [ ] Implement CI/CD pipeline
- [ ] Add automated deployment scripts

#### v1.2.0 - Enhanced Features
- [ ] Multi-language support (French, Italian)
- [ ] Voice input/output support
- [ ] Document upload for project plans
- [ ] Integration with ERNI's CRM system
- [ ] Advanced analytics and reporting
- [ ] Customer feedback system

#### v2.0.0 - Advanced Capabilities
- [ ] Image recognition for building plans
- [ ] 3D visualization integration
- [ ] Predictive cost modeling with ML
- [ ] Automated project timeline generation
- [ ] Integration with building permit systems

---

## Version History

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| 1.0.0-staging | 2025-10-04 | ✅ Released | Initial staging release |
| 1.0.0 | TBD | 🔄 Planned | Production release |

---

**Maintained by:** ERNI Gruppe Development Team  
**Last Updated:** October 4, 2025

