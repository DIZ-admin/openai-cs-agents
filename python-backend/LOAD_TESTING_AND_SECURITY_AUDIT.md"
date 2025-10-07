# Load Testing and Security Audit Guide

## 📋 Table of Contents

1. [Overview](#overview)
2. [Load Testing](#load-testing)
3. [Security Audit](#security-audit)
4. [Prerequisites](#prerequisites)
5. [Quick Start](#quick-start)
6. [Detailed Instructions](#detailed-instructions)
7. [Interpreting Results](#interpreting-results)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This guide provides comprehensive instructions for conducting load testing and security audits on the ERNI Gruppe Building Agents project before production deployment.

### Goals

**Load Testing:**
- Verify system can handle expected production traffic
- Identify performance bottlenecks
- Determine system breaking points
- Validate resource utilization

**Security Audit:**
- Identify security vulnerabilities
- Verify authentication and authorization
- Test input validation and guardrails
- Scan dependencies for known vulnerabilities
- Ensure compliance with security best practices

---

## 🚀 Load Testing

### Test Scenarios

| Scenario | Users | Duration | Purpose |
|----------|-------|----------|---------|
| **Baseline** | 10 | 5 min | Establish performance baseline |
| **Normal Load** | 50 | 15 min | Simulate typical production traffic |
| **Peak Load** | 100 | 10 min | Test peak hour capacity |
| **Stress Test** | 200+ | 10 min | Find breaking point |
| **Endurance** | 50 | 2 hours | Check for memory leaks |

### Key Metrics

- **Response Time:** P50, P95, P99 latencies
- **Throughput:** Requests per second
- **Error Rate:** Target < 1%
- **Resource Utilization:** CPU, memory, database connections

### Acceptance Criteria

✅ System handles 100 concurrent users with < 2s average response time  
✅ Error rate stays below 1% under normal load  
✅ No memory leaks during endurance test  
✅ Database connection pool doesn't exhaust  

---

## 🔒 Security Audit

### Audit Components

1. **Code Security Review**
   - Authentication and authorization code
   - SQL injection vulnerabilities
   - Input validation
   - Hardcoded secrets

2. **Dependency Security Scan**
   - Python packages (pip-audit)
   - npm packages (npm audit)
   - Known vulnerabilities

3. **API Security Testing**
   - Rate limiting
   - CORS configuration
   - JWT token validation
   - Injection attacks (SQL, XSS)
   - Guardrail bypass attempts

4. **Infrastructure Security**
   - Docker container security
   - Database security
   - Redis authentication
   - Environment variable management

5. **Data Protection**
   - PII guardrail effectiveness
   - Encryption at rest and in transit
   - Logging security

---

## 📦 Prerequisites

### Required Tools

**For Load Testing:**
```bash
# Install Locust
pip install locust

# Verify installation
locust --version
```

**For Security Audit:**
```bash
# Install security scanning tools
pip install pip-audit safety

# Verify installations
pip-audit --version
```

### System Requirements

- Python 3.9+
- Node.js 18+ (for npm audit)
- Docker and Docker Compose (for infrastructure tests)
- 8GB RAM minimum (16GB recommended for load testing)
- Backend and frontend services running

---

## ⚡ Quick Start

### 1. Load Testing (Quick)

```bash
# Start backend
cd python-backend
source .venv/bin/activate
uvicorn api:app --host 0.0.0.0 --port 8000

# In another terminal, run baseline test
cd python-backend
locust -f load_testing/locustfile.py \
       --host=http://localhost:8000 \
       --users 10 --spawn-rate 2 --run-time 5m \
       --headless
```

### 2. Security Audit (Quick)

```bash
# Run complete security audit
cd python-backend
chmod +x security_audit/run_security_audit.sh
./security_audit/run_security_audit.sh
```

---

## 📖 Detailed Instructions

### Load Testing - Step by Step

#### 1. Prepare Environment

```bash
# Ensure backend is running
cd python-backend
source .venv/bin/activate
uvicorn api:app --host 0.0.0.0 --port 8000

# Verify backend is healthy
curl http://localhost:8000/health
```

#### 2. Run Baseline Test (10 users, 5 minutes)

```bash
cd python-backend
locust -f load_testing/locustfile.py \
       --host=http://localhost:8000 \
       --users 10 \
       --spawn-rate 2 \
       --run-time 5m \
       --headless \
       --html load_testing/reports/baseline_report.html
```

**Expected Results:**
- Average response time: < 500ms
- P95 response time: < 1000ms
- Error rate: 0%

#### 3. Run Normal Load Test (50 users, 15 minutes)

```bash
locust -f load_testing/locustfile.py \
       --host=http://localhost:8000 \
       --users 50 \
       --spawn-rate 5 \
       --run-time 15m \
       --headless \
       --html load_testing/reports/normal_load_report.html
```

**Expected Results:**
- Average response time: < 1000ms
- P95 response time: < 2000ms
- Error rate: < 1%

#### 4. Run Peak Load Test (100 users, 10 minutes)

```bash
locust -f load_testing/locustfile.py \
       --host=http://localhost:8000 \
       --users 100 \
       --spawn-rate 10 \
       --run-time 10m \
       --headless \
       --html load_testing/reports/peak_load_report.html
```

**Expected Results:**
- Average response time: < 2000ms
- P95 response time: < 5000ms
- Error rate: < 1%

#### 5. Run Stress Test (200+ users until failure)

```bash
locust -f load_testing/locustfile.py \
       --host=http://localhost:8000 \
       --users 200 \
       --spawn-rate 10 \
       --run-time 10m \
       --headless \
       --html load_testing/reports/stress_test_report.html
```

**Goal:** Find the breaking point of the system.

#### 6. Run Endurance Test (50 users, 2 hours)

```bash
locust -f load_testing/locustfile.py \
       --host=http://localhost:8000 \
       --users 50 \
       --spawn-rate 5 \
       --run-time 2h \
       --headless \
       --html load_testing/reports/endurance_test_report.html
```

**Goal:** Detect memory leaks and resource exhaustion.

#### 7. Interactive Load Testing (Web UI)

```bash
# Start Locust web UI
locust -f load_testing/locustfile.py --host=http://localhost:8000

# Open browser to http://localhost:8089
# Configure users and spawn rate in the UI
# Monitor real-time metrics
```

### Security Audit - Step by Step

#### 1. Dependency Vulnerability Scan

```bash
cd python-backend

# Scan Python dependencies
pip-audit -r requirements.txt --format=json > security_audit/reports/python_vulns.json

# Scan npm dependencies (if frontend exists)
cd ../ui
npm audit --json > ../python-backend/security_audit/reports/npm_vulns.json
```

#### 2. Code Security Review

```bash
cd python-backend

# Check for hardcoded secrets
grep -r -i "password\s*=\s*['\"]" --include="*.py" . | grep -v "test"

# Check for SQL injection vulnerabilities
grep -r "execute.*%\|execute.*format" --include="*.py" . | grep -v "test"

# Verify .env is in .gitignore
grep "\.env" ../.gitignore
```

#### 3. API Security Testing

```bash
# Ensure backend is running
curl http://localhost:8000/health

# Run API security tests
cd python-backend/security_audit
python api_security_tests.py http://localhost:8000
```

**Tests Include:**
- Rate limiting enforcement
- CORS configuration
- Authentication validation
- Input validation
- SQL injection protection
- XSS protection
- Guardrail bypass attempts

#### 4. Complete Security Audit

```bash
cd python-backend
chmod +x security_audit/run_security_audit.sh
./security_audit/run_security_audit.sh
```

This runs all security checks and generates a comprehensive report.

---

## 📊 Interpreting Results

### Load Testing Results

**Good Performance Indicators:**
- ✅ P95 response time < 2000ms under normal load
- ✅ Error rate < 1%
- ✅ Throughput > 10 requests/second
- ✅ CPU usage < 70%
- ✅ Memory usage stable (no leaks)

**Warning Signs:**
- ⚠️ P95 response time > 5000ms
- ⚠️ Error rate > 5%
- ⚠️ CPU usage > 90%
- ⚠️ Memory usage increasing over time

**Critical Issues:**
- ❌ System crashes or becomes unresponsive
- ❌ Error rate > 10%
- ❌ Database connection pool exhausted
- ❌ Memory leaks detected

### Security Audit Results

**Severity Levels:**

| Severity | Description | Action Required |
|----------|-------------|-----------------|
| **Critical** | Immediate security risk | Fix before deployment |
| **High** | Significant vulnerability | Fix within 24 hours |
| **Medium** | Moderate risk | Fix within 1 week |
| **Low** | Minor issue | Fix in next sprint |

**Common Findings:**

1. **Vulnerable Dependencies**
   - Action: Update to patched versions
   - If no patch available: Document and implement mitigation

2. **Weak Authentication**
   - Action: Strengthen password requirements
   - Implement MFA if needed

3. **Missing Rate Limiting**
   - Action: Configure rate limits
   - Test effectiveness

4. **Insufficient Input Validation**
   - Action: Add validation for all inputs
   - Test with malicious payloads

---

## 🔧 Troubleshooting

### Load Testing Issues

**Issue: Locust won't start**
```bash
# Solution: Reinstall Locust
pip uninstall locust
pip install locust
```

**Issue: Backend not responding**
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

**Issue: High error rates**
```bash
# Check backend logs for errors
docker-compose logs backend | grep ERROR

# Check database connections
docker exec erni-postgres pg_stat_activity

# Check Redis
docker exec erni-redis redis-cli PING
```

### Security Audit Issues

**Issue: pip-audit not found**
```bash
# Install pip-audit
pip install pip-audit
```

**Issue: npm audit fails**
```bash
# Update npm
npm install -g npm@latest

# Clear cache
npm cache clean --force
```

**Issue: API tests fail to connect**
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check firewall settings
# Ensure port 8000 is open
```

---

## 📝 Reporting

### Load Testing Report Template

```markdown
# Load Testing Report - ERNI Gruppe Building Agents

**Date:** [Date]
**Tester:** [Name]
**Environment:** [Development/Staging/Production]

## Test Configuration
- Users: [Number]
- Duration: [Minutes]
- Spawn Rate: [Users/second]

## Results
- Average Response Time: [ms]
- P95 Response Time: [ms]
- P99 Response Time: [ms]
- Throughput: [req/s]
- Error Rate: [%]

## Resource Utilization
- CPU: [%]
- Memory: [GB]
- Database Connections: [count]

## Issues Found
1. [Issue description]
2. [Issue description]

## Recommendations
1. [Recommendation]
2. [Recommendation]
```

### Security Audit Report Template

```markdown
# Security Audit Report - ERNI Gruppe Building Agents

**Date:** [Date]
**Auditor:** [Name]

## Summary
- Total Vulnerabilities: [count]
- Critical: [count]
- High: [count]
- Medium: [count]
- Low: [count]

## Findings

### Critical
1. **[Vulnerability Name]**
   - Description: [Details]
   - Impact: [Impact]
   - Remediation: [Steps to fix]

### High
[...]

## Recommendations
1. [Recommendation]
2. [Recommendation]

## Next Steps
1. [Action item]
2. [Action item]
```

---

## 🎯 Next Steps

After completing load testing and security audit:

1. **Review Results**
   - Analyze all reports
   - Prioritize findings by severity
   - Create remediation plan

2. **Fix Critical Issues**
   - Address all critical and high-severity findings
   - Re-test after fixes

3. **Optimize Performance**
   - Implement performance improvements
   - Re-run load tests to verify

4. **Update Documentation**
   - Document findings and fixes
   - Update RUNBOOK.md if needed

5. **Schedule Regular Audits**
   - Load testing: Before each major release
   - Security audit: Quarterly

---

**Last Updated:** October 5, 2025  
**Version:** 1.0.0

