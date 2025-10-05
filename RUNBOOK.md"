# ERNI Gruppe Building Agents - Operational Runbook

## 📋 Table of Contents

1. [Service Overview](#service-overview)
2. [Common Operations](#common-operations)
3. [Troubleshooting Guide](#troubleshooting-guide)
4. [Incident Response](#incident-response)
5. [Monitoring & Alerting](#monitoring--alerting)
6. [Backup & Recovery](#backup--recovery)
7. [Deployment Procedures](#deployment-procedures)
8. [Rollback Procedures](#rollback-procedures)
9. [Emergency Contacts](#emergency-contacts)

---

## 🎯 Service Overview

### Architecture
- **Backend:** Python FastAPI application (port 8000)
- **Frontend:** Next.js application (port 3000)
- **Database:** PostgreSQL 15 (port 5432)
- **Cache:** Redis 7 (port 6379)
- **Reverse Proxy:** Nginx (ports 80, 443)

### Service Dependencies
```
Frontend → Backend → PostgreSQL
                  → Redis
                  → OpenAI API
```

### Health Check Endpoints
- **Backend Health:** `http://localhost:8000/health`
- **Backend Readiness:** `http://localhost:8000/readiness`
- **Frontend:** `http://localhost:3000`

---

## 🔧 Common Operations

### Starting Services

#### Development Mode (Local)

**Backend:**
```bash
cd python-backend
source .venv/bin/activate
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd ui
npm run dev:next
```

**Both (Concurrent):**
```bash
cd ui
npm run dev
```

#### Docker Mode

**Start all services:**
```bash
docker-compose up -d
```

**Start specific service:**
```bash
docker-compose up -d backend
docker-compose up -d frontend
docker-compose up -d postgres
```

**View logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stopping Services

#### Development Mode
- Press `Ctrl+C` in the terminal running the service

#### Docker Mode

**Stop all services:**
```bash
docker-compose down
```

**Stop specific service:**
```bash
docker-compose stop backend
docker-compose stop frontend
```

**Stop and remove volumes (⚠️ WARNING: Deletes all data):**
```bash
docker-compose down -v
```

### Restarting Services

#### Development Mode
1. Stop the service (`Ctrl+C`)
2. Start it again

#### Docker Mode

**Restart all services:**
```bash
docker-compose restart
```

**Restart specific service:**
```bash
docker-compose restart backend
docker-compose restart frontend
```

**Rebuild and restart (after code changes):**
```bash
docker-compose up -d --build
```

### Checking Service Status

#### Docker Mode
```bash
# List all containers
docker-compose ps

# Check container health
docker inspect erni-backend --format='{{.State.Health.Status}}'
docker inspect erni-frontend --format='{{.State.Health.Status}}'
docker inspect erni-postgres --format='{{.State.Health.Status}}'
```

#### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Backend readiness
curl http://localhost:8000/readiness

# Frontend
curl http://localhost:3000
```

### Viewing Logs

#### Development Mode
Logs appear in the terminal where the service is running.

#### Docker Mode

**Real-time logs:**
```bash
# All services
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

**Log files (if configured):**
```bash
# Backend logs
docker exec erni-backend cat /var/log/erni-backend/app.log

# Nginx logs
docker exec erni-nginx cat /var/log/nginx/access.log
docker exec erni-nginx cat /var/log/nginx/error.log
```

### Database Operations

#### Connect to PostgreSQL

**Via Docker:**
```bash
docker exec -it erni-postgres psql -U erni_user -d erni_agents
```

**Via local psql:**
```bash
psql -h localhost -p 5432 -U erni_user -d erni_agents
```

#### Common Database Queries

**Check conversations:**
```sql
SELECT id, customer_name, customer_email, status, created_at 
FROM conversations 
ORDER BY created_at DESC 
LIMIT 10;
```

**Check messages:**
```sql
SELECT m.id, m.role, m.agent_name, m.created_at, LEFT(m.content, 50) as content_preview
FROM messages m
JOIN conversations c ON m.conversation_id = c.id
ORDER BY m.created_at DESC
LIMIT 20;
```

**Check projects:**
```sql
SELECT project_number, project_type, status, progress, current_stage
FROM projects
ORDER BY created_at DESC;
```

**Check consultations:**
```sql
SELECT specialist_type, specialist_name, consultation_date, consultation_time, status
FROM consultations
ORDER BY consultation_date DESC;
```

#### Database Backup

**Manual backup:**
```bash
docker exec erni-postgres pg_dump -U erni_user erni_agents > backup_$(date +%Y%m%d_%H%M%S).sql
```

**Restore from backup:**
```bash
docker exec -i erni-postgres psql -U erni_user erni_agents < backup_20250105_120000.sql
```

### Redis Operations

#### Connect to Redis

**Via Docker:**
```bash
docker exec -it erni-redis redis-cli -a ${REDIS_PASSWORD}
```

#### Common Redis Commands

**Check keys:**
```bash
KEYS *
```

**Get cache statistics:**
```bash
INFO stats
```

**Clear all cache (⚠️ Use with caution):**
```bash
FLUSHALL
```

**Check specific key:**
```bash
GET guardrail:relevance:abc123
```

---

## 🔍 Troubleshooting Guide

### Backend Issues

#### Issue: Backend won't start

**Symptoms:**
- Error: "Address already in use"
- Error: "OPENAI_API_KEY not found"

**Solutions:**

1. **Port already in use:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

2. **Missing environment variables:**
```bash
# Check .env file exists
ls -la python-backend/.env

# Verify required variables
grep OPENAI_API_KEY python-backend/.env
grep OPENAI_VECTOR_STORE_ID python-backend/.env
grep SECRET_KEY python-backend/.env
```

3. **Dependencies not installed:**
```bash
cd python-backend
source .venv/bin/activate
pip install -r requirements.txt
```

#### Issue: Backend returns 500 errors

**Symptoms:**
- HTTP 500 Internal Server Error
- Errors in logs

**Solutions:**

1. **Check logs:**
```bash
docker-compose logs backend | tail -50
```

2. **Check OpenAI API key:**
```bash
# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

3. **Check database connection:**
```bash
docker exec erni-backend python -c "import psycopg2; print('DB OK')"
```

4. **Restart backend:**
```bash
docker-compose restart backend
```

#### Issue: Guardrails not working

**Symptoms:**
- Irrelevant queries accepted
- Jailbreak attempts succeed

**Solutions:**

1. **Check guardrail configuration:**
```bash
# Verify guardrails are enabled in main.py
grep "input_guardrails" python-backend/main.py
```

2. **Clear guardrail cache:**
```bash
docker exec -it erni-redis redis-cli -a ${REDIS_PASSWORD} KEYS "guardrail:*"
docker exec -it erni-redis redis-cli -a ${REDIS_PASSWORD} DEL "guardrail:*"
```

3. **Check OpenAI API quota:**
- Guardrails use OpenAI API calls
- Verify you haven't exceeded rate limits

### Frontend Issues

#### Issue: Frontend won't start

**Symptoms:**
- Error: "Port 3000 already in use"
- Error: "Module not found"

**Solutions:**

1. **Port already in use:**
```bash
# Find process using port 3000
lsof -i :3000

# Kill the process
kill -9 <PID>
```

2. **Dependencies not installed:**
```bash
cd ui
npm install
```

3. **Clear Next.js cache:**
```bash
cd ui
rm -rf .next
npm run build
npm run dev:next
```

#### Issue: Frontend can't connect to backend

**Symptoms:**
- "Failed to fetch" errors
- CORS errors in browser console

**Solutions:**

1. **Check backend is running:**
```bash
curl http://localhost:8000/health
```

2. **Check CORS configuration:**
```bash
# Verify CORS_ORIGINS in .env
grep CORS_ORIGINS python-backend/.env
```

3. **Check API URL in frontend:**
```bash
# Should be http://localhost:8000 or http://backend:8000
grep NEXT_PUBLIC_API_URL ui/.env.local
```

### Database Issues

#### Issue: PostgreSQL won't start

**Symptoms:**
- Container exits immediately
- "database system was shut down" in logs

**Solutions:**

1. **Check logs:**
```bash
docker-compose logs postgres
```

2. **Check disk space:**
```bash
df -h
```

3. **Remove corrupted data (⚠️ WARNING: Deletes all data):**
```bash
docker-compose down -v
docker volume rm openai-cs-agents-demo_postgres_data
docker-compose up -d postgres
```

4. **Restore from backup:**
```bash
# After recreating database
docker exec -i erni-postgres psql -U erni_user erni_agents < backup.sql
```

#### Issue: Database connection errors

**Symptoms:**
- "could not connect to server"
- "password authentication failed"

**Solutions:**

1. **Check PostgreSQL is running:**
```bash
docker-compose ps postgres
```

2. **Verify credentials:**
```bash
# Check DB_PASSWORD in .env
grep DB_PASSWORD python-backend/.env
```

3. **Test connection:**
```bash
docker exec erni-postgres pg_isready -U erni_user
```

### Redis Issues

#### Issue: Redis connection errors

**Symptoms:**
- "Connection refused"
- "NOAUTH Authentication required"

**Solutions:**

1. **Check Redis is running:**
```bash
docker-compose ps redis
```

2. **Verify password:**
```bash
# Check REDIS_PASSWORD in .env
grep REDIS_PASSWORD python-backend/.env
```

3. **Test connection:**
```bash
docker exec erni-redis redis-cli -a ${REDIS_PASSWORD} PING
```

### Performance Issues

#### Issue: Slow response times

**Symptoms:**
- Requests take > 5 seconds
- Timeouts

**Solutions:**

1. **Check resource usage:**
```bash
docker stats
```

2. **Check database performance:**
```sql
-- Find slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

3. **Check Redis cache hit rate:**
```bash
docker exec erni-redis redis-cli -a ${REDIS_PASSWORD} INFO stats | grep keyspace
```

4. **Increase resources:**
```yaml
# In docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

---

## 🚨 Incident Response

### Severity Levels

| Level | Description | Response Time | Example |
|-------|-------------|---------------|---------|
| **P0 - Critical** | Service completely down | < 15 minutes | All services unavailable |
| **P1 - High** | Major functionality broken | < 1 hour | Backend down, frontend works |
| **P2 - Medium** | Partial functionality affected | < 4 hours | One agent not working |
| **P3 - Low** | Minor issues, workaround available | < 24 hours | Slow performance |

### Incident Response Procedure

#### 1. Detection & Triage (0-5 minutes)

**Actions:**
1. Confirm the incident
2. Assess severity
3. Create incident ticket
4. Notify team

**Commands:**
```bash
# Quick health check
curl http://localhost:8000/health
curl http://localhost:3000

# Check all services
docker-compose ps

# Check logs for errors
docker-compose logs --tail=100 | grep ERROR
```

#### 2. Investigation (5-30 minutes)

**Actions:**
1. Gather logs
2. Identify root cause
3. Document findings

**Commands:**
```bash
# Collect logs
docker-compose logs > incident_logs_$(date +%Y%m%d_%H%M%S).txt

# Check resource usage
docker stats --no-stream

# Check database
docker exec erni-postgres pg_isready
```

#### 3. Mitigation (Immediate)

**Quick Fixes:**

**Service restart:**
```bash
docker-compose restart backend
```

**Clear cache:**
```bash
docker exec erni-redis redis-cli -a ${REDIS_PASSWORD} FLUSHALL
```

**Rollback deployment:**
```bash
git checkout <previous-commit>
docker-compose up -d --build
```

#### 4. Resolution (30 minutes - 4 hours)

**Actions:**
1. Implement fix
2. Test thoroughly
3. Deploy to production
4. Monitor

#### 5. Post-Incident (24-48 hours)

**Actions:**
1. Write post-mortem
2. Identify improvements
3. Update runbook
4. Implement preventive measures

---

## 📊 Monitoring & Alerting

### Key Metrics to Monitor

#### Application Metrics
- **Request Rate:** Requests per minute
- **Error Rate:** 4xx and 5xx errors
- **Response Time:** P50, P95, P99 latencies
- **Agent Handoffs:** Successful vs failed handoffs
- **Guardrail Triggers:** Relevance, jailbreak, PII blocks

#### Infrastructure Metrics
- **CPU Usage:** < 70% normal, > 90% critical
- **Memory Usage:** < 80% normal, > 95% critical
- **Disk Usage:** < 80% normal, > 90% critical
- **Network I/O:** Bandwidth usage

#### Database Metrics
- **Connection Pool:** Active connections
- **Query Performance:** Slow queries (> 1s)
- **Replication Lag:** If using replicas
- **Disk I/O:** Read/write operations

### Prometheus Queries

**Request rate:**
```promql
rate(http_requests_total[5m])
```

**Error rate:**
```promql
rate(http_requests_total{status=~"5.."}[5m])
```

**Response time (P95):**
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

### Alert Rules

#### Critical Alerts

**Service Down:**
```yaml
- alert: ServiceDown
  expr: up{job="erni-backend"} == 0
  for: 1m
  annotations:
    summary: "Backend service is down"
```

**High Error Rate:**
```yaml
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
  for: 5m
  annotations:
    summary: "Error rate > 5%"
```

**Database Connection Issues:**
```yaml
- alert: DatabaseConnectionFailed
  expr: pg_up == 0
  for: 1m
  annotations:
    summary: "Cannot connect to PostgreSQL"
```

---

## 💾 Backup & Recovery

### Backup Strategy

#### Database Backups

**Automated daily backup (cron):**
```bash
# Add to crontab
0 2 * * * /path/to/backup-script.sh
```

**Backup script (`backup-script.sh`):**
```bash
#!/bin/bash
BACKUP_DIR="/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/erni_agents_$DATE.sql"

# Create backup
docker exec erni-postgres pg_dump -U erni_user erni_agents > $BACKUP_FILE

# Compress
gzip $BACKUP_FILE

# Delete backups older than 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE.gz"
```

#### Redis Backups

**Manual snapshot:**
```bash
docker exec erni-redis redis-cli -a ${REDIS_PASSWORD} BGSAVE
```

**Copy RDB file:**
```bash
docker cp erni-redis:/data/dump.rdb ./redis_backup_$(date +%Y%m%d).rdb
```

#### Application Code Backups

**Git repository:**
```bash
# Ensure all changes are committed
git status
git add .
git commit -m "Backup before deployment"
git push origin main
```

### Recovery Procedures

#### Database Recovery

**From SQL backup:**
```bash
# Stop backend to prevent connections
docker-compose stop backend

# Restore database
docker exec -i erni-postgres psql -U erni_user erni_agents < backup_20250105.sql

# Start backend
docker-compose start backend
```

#### Redis Recovery

**From RDB file:**
```bash
# Stop Redis
docker-compose stop redis

# Copy RDB file
docker cp redis_backup_20250105.rdb erni-redis:/data/dump.rdb

# Start Redis
docker-compose start redis
```

#### Full System Recovery

**From complete failure:**
```bash
# 1. Clone repository
git clone https://github.com/DIZ-admin/openai-cs-agents.git
cd openai-cs-agents

# 2. Restore .env file
cp /backup/.env python-backend/.env

# 3. Start services
docker-compose up -d

# 4. Wait for PostgreSQL to be ready
docker-compose logs -f postgres

# 5. Restore database
docker exec -i erni-postgres psql -U erni_user erni_agents < /backup/latest.sql

# 6. Verify services
curl http://localhost:8000/health
curl http://localhost:3000
```

---

## 🔐 Key Rotation Policy

To maintain a strong security posture, rotate all sensitive credentials at least every 90 days and immediately after any suspected compromise.

**Scope:**
- `OPENAI_API_KEY`, `OPENAI_VECTOR_STORE_ID`
- `SECRET_KEY`, `JWT_SECRET_KEY`
- `DB_PASSWORD` (PostgreSQL) and `REDIS_PASSWORD`
- SSL/TLS certificates stored in `nginx/ssl`

**Rotation Checklist:**
1. Generate new values (`openssl rand -hex 32` or cloud secret manager).
2. Update centralized secret storage (AWS Secrets Manager / Azure Key Vault / HashiCorp Vault).
3. Update GitHub Actions secrets (`Settings → Secrets and variables → Actions`).
4. Update `python-backend/.env` (or secret manager templates) on all runtime hosts.
5. Run `python scripts/preflight_check.py` to validate configuration.
6. Redeploy via `docker-compose.prod.yml` (rolling restart recommended).
7. Verify health endpoints and review logs for authentication errors.
8. Revoke previous credentials and document the rotation (date, operator, reason).

**Emergency Rotation:**
- Trigger immediately when compromise is suspected.
- Notify on-call engineer and security lead.
- Follow the checklist above, then create an incident ticket and capture a postmortem.

**Automation Recommendations:**
- Store last-rotation timestamps in an operations dashboard.
- Schedule quarterly reminders (calendar/Jira recurring tasks).
- Evaluate automatic rotation options provided by your secret manager.

---

## 🚀 Deployment Procedures

### Staging Deployment

**Prerequisites:**
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Environment variables configured
- [ ] Database migrations ready

**Steps:**

1. **Prepare environment:**
```bash
cd python-backend
cp .env.staging .env
```

2. **Run tests:**
```bash
python -m pytest tests/ -v
```

3. **Build Docker images:**
```bash
docker-compose build
```

4. **Deploy to staging:**
```bash
docker-compose up -d
```

5. **Run smoke tests:**
```bash
curl http://staging.erni-gruppe.ch/health
curl http://staging.erni-gruppe.ch/readiness
```

6. **Monitor logs:**
```bash
docker-compose logs -f
```

### Production Deployment

**Prerequisites:**
- [ ] Staging deployment successful
- [ ] Load testing completed
- [ ] Security audit passed
- [ ] Backup created
- [ ] Rollback plan ready

**Steps:**

1. **Create backup:**
```bash
./scripts/backup-production.sh
```

2. **Notify team:**
```
Deployment starting at [TIME]
Expected duration: 15 minutes
```

3. **Deploy:**
```bash
# Pull latest code
git pull origin main

# Validate secrets
python scripts/preflight_check.py

# Build images
docker-compose -f docker-compose.prod.yml build

# Deploy with zero downtime
docker-compose -f docker-compose.prod.yml up -d --no-deps --build backend
docker-compose -f docker-compose.prod.yml up -d --no-deps --build frontend
```

4. **Verify deployment:**
```bash
curl https://erni-gruppe.ch/health
curl https://erni-gruppe.ch/readiness
```

5. **Monitor metrics:**
- Check error rates
- Check response times
- Check resource usage

6. **Notify team:**
```
Deployment completed successfully
All services healthy
```

---

## ⏮️ Rollback Procedures

### When to Rollback

- Critical bugs in production
- Performance degradation > 50%
- Data corruption detected
- Security vulnerability discovered

### Quick Rollback (< 5 minutes)

**Using Docker tags:**
```bash
# Rollback to previous version
docker-compose -f docker-compose.prod.yml down
docker tag erni-backend:latest erni-backend:rollback
docker tag erni-backend:previous erni-backend:latest
docker-compose -f docker-compose.prod.yml up -d
```

**Using Git:**
```bash
# Revert to previous commit
git revert HEAD
docker-compose up -d --build
```

### Database Rollback

**If migrations were applied:**
```bash
# Restore from backup
docker exec -i erni-postgres psql -U erni_user erni_agents < backup_pre_deployment.sql
```

### Verification After Rollback

```bash
# Check services
curl https://erni-gruppe.ch/health

# Check logs
docker-compose logs --tail=100

# Monitor metrics
# - Error rate should decrease
# - Response time should improve
```

---

## 📞 Emergency Contacts

### On-Call Rotation

| Role | Name | Phone | Email | Backup |
|------|------|-------|-------|--------|
| **DevOps Lead** | TBD | +41 XX XXX XX XX | devops@erni-gruppe.ch | TBD |
| **Backend Lead** | TBD | +41 XX XXX XX XX | backend@erni-gruppe.ch | TBD |
| **Frontend Lead** | TBD | +41 XX XXX XX XX | frontend@erni-gruppe.ch | TBD |

### Escalation Path

1. **Level 1:** On-call engineer (15 min response)
2. **Level 2:** Team lead (30 min response)
3. **Level 3:** Engineering manager (1 hour response)
4. **Level 4:** CTO (2 hour response)

### External Contacts

| Service | Contact | Purpose |
|---------|---------|---------|
| **OpenAI Support** | support@openai.com | API issues |
| **Cloud Provider** | TBD | Infrastructure issues |
| **DNS Provider** | TBD | Domain issues |

---

## 📝 Appendix

### Useful Commands Cheat Sheet

```bash
# Quick health check
curl http://localhost:8000/health && curl http://localhost:3000

# Restart all services
docker-compose restart

# View all logs
docker-compose logs -f

# Database backup
docker exec erni-postgres pg_dump -U erni_user erni_agents > backup.sql

# Clear Redis cache
docker exec erni-redis redis-cli -a ${REDIS_PASSWORD} FLUSHALL

# Check resource usage
docker stats --no-stream

# Find process on port
lsof -i :8000

# Test OpenAI API
curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Log Locations

| Service | Location |
|---------|----------|
| **Backend** | `docker-compose logs backend` |
| **Frontend** | `docker-compose logs frontend` |
| **PostgreSQL** | `docker-compose logs postgres` |
| **Redis** | `docker-compose logs redis` |
| **Nginx** | `docker-compose logs nginx` |

---

**Last Updated:** October 5, 2025  
**Version:** 1.0.0  
**Maintained by:** ERNI Gruppe DevOps Team
