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

### Service Level Objectives (SLOs)

**Availability:**
- Target: 99.9% uptime (8.76 hours downtime/year)
- Measurement: Health endpoint availability over 30-day rolling window

**Performance:**
- P95 Response Time: < 2000ms
- P99 Response Time: < 5000ms
- Measurement: HTTP request duration histogram

**Reliability:**
- Error Rate: < 1% of all requests
- Measurement: 5xx errors / total requests

### Key Metrics to Monitor

#### Application Metrics
- **Request Rate:** Requests per minute
- **Error Rate:** 4xx and 5xx errors
- **Response Time:** P50, P95, P99 latencies
- **Agent Handoffs:** Successful vs failed handoffs
- **Guardrail Triggers:** Relevance, jailbreak, PII blocks
- **OpenAI API Calls:** Rate, latency, errors
- **Authentication:** Login attempts, failures, token expirations

#### Infrastructure Metrics
- **CPU Usage:** < 70% normal, > 90% critical
- **Memory Usage:** < 80% normal, > 95% critical
- **Disk Usage:** < 80% normal, > 90% critical
- **Network I/O:** Bandwidth usage
- **Container Health:** Docker container status

#### Database Metrics
- **Connection Pool:** Active connections (max 100)
- **Query Performance:** Slow queries (> 1s)
- **Replication Lag:** If using replicas
- **Disk I/O:** Read/write operations
- **Table Size:** Growth rate monitoring

#### Redis Metrics
- **Memory Usage:** Current vs max memory
- **Hit Rate:** Cache hit/miss ratio
- **Evictions:** Number of evicted keys
- **Connected Clients:** Active connections

### Prometheus Setup

**Installation:**
```bash
# Add Prometheus to docker-compose.yml
docker-compose up -d prometheus grafana
```

**Configuration (`prometheus.yml`):**
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'erni-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

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

**CPU usage:**
```promql
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

**Memory usage:**
```promql
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100
```

### Grafana Dashboards

**Dashboard Setup:**
1. Access Grafana: `http://localhost:3001`
2. Add Prometheus data source
3. Import dashboard ID: 1860 (Node Exporter Full)
4. Create custom dashboard for ERNI metrics

**Key Panels:**
- Request Rate (line chart)
- Error Rate (line chart with threshold)
- Response Time (heatmap)
- Active Users (gauge)
- Agent Distribution (pie chart)
- Database Connections (gauge)

**Dashboard JSON:** See `monitoring/grafana-dashboard.json`

### Alert Rules

#### Critical Alerts (P0 - Immediate Response)

**Service Down:**
```yaml
- alert: ServiceDown
  expr: up{job="erni-backend"} == 0
  for: 1m
  labels:
    severity: critical
    priority: P0
  annotations:
    summary: "Backend service is down"
    description: "Backend has been down for more than 1 minute"
    runbook: "https://wiki.erni-gruppe.ch/runbook#service-down"
```

**High Error Rate:**
```yaml
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
  for: 5m
  labels:
    severity: critical
    priority: P0
  annotations:
    summary: "Error rate > 5%"
    description: "5xx error rate is {{ $value | humanizePercentage }}"
```

**Database Connection Failed:**
```yaml
- alert: DatabaseConnectionFailed
  expr: pg_up == 0
  for: 1m
  labels:
    severity: critical
    priority: P0
  annotations:
    summary: "Cannot connect to PostgreSQL"
    description: "PostgreSQL database is unreachable"
```

#### High Priority Alerts (P1 - 1 Hour Response)

**High Response Time:**
```yaml
- alert: HighResponseTime
  expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
  for: 10m
  labels:
    severity: high
    priority: P1
  annotations:
    summary: "P95 response time > 2s"
    description: "P95 latency is {{ $value }}s"
```

**High CPU Usage:**
```yaml
- alert: HighCPUUsage
  expr: 100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 90
  for: 10m
  labels:
    severity: high
    priority: P1
  annotations:
    summary: "CPU usage > 90%"
    description: "CPU usage is {{ $value }}%"
```

**High Memory Usage:**
```yaml
- alert: HighMemoryUsage
  expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 95
  for: 10m
  labels:
    severity: high
    priority: P1
  annotations:
    summary: "Memory usage > 95%"
    description: "Memory usage is {{ $value }}%"
```

#### Medium Priority Alerts (P2 - 4 Hour Response)

**Disk Space Low:**
```yaml
- alert: DiskSpaceLow
  expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 < 20
  for: 30m
  labels:
    severity: medium
    priority: P2
  annotations:
    summary: "Disk space < 20%"
    description: "Available disk space is {{ $value }}%"
```

**Redis Memory High:**
```yaml
- alert: RedisMemoryHigh
  expr: redis_memory_used_bytes / redis_memory_max_bytes > 0.9
  for: 15m
  labels:
    severity: medium
    priority: P2
  annotations:
    summary: "Redis memory usage > 90%"
```

### Alert Notification Channels

**Slack Integration:**
```yaml
receivers:
  - name: 'slack-critical'
    slack_configs:
      - api_url: $SLACK_WEBHOOK_URL
        channel: '#erni-alerts-critical'
        title: '🚨 {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'slack-high'
    slack_configs:
      - api_url: $SLACK_WEBHOOK_URL
        channel: '#erni-alerts-high'
        title: '⚠️ {{ .GroupLabels.alertname }}'
```

**Email Integration:**
```yaml
  - name: 'email-oncall'
    email_configs:
      - to: 'oncall@erni-gruppe.ch'
        from: 'alerts@erni-gruppe.ch'
        smarthost: 'smtp.erni-gruppe.ch:587'
        auth_username: 'alerts@erni-gruppe.ch'
        auth_password: $SMTP_PASSWORD
```

**PagerDuty Integration:**
```yaml
  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: $PAGERDUTY_SERVICE_KEY
        description: '{{ .GroupLabels.alertname }}: {{ .Annotations.summary }}'
```

### On-Call Rotation

**Schedule:**
- **Primary On-Call:** Rotates weekly (Monday 09:00 - Monday 09:00)
- **Secondary On-Call:** Backup for primary
- **Escalation:** After 15 minutes if no response

**Current Rotation:** See PagerDuty schedule or `monitoring/oncall-schedule.md`

**Responsibilities:**
- Monitor alerts 24/7
- Respond within SLA (P0: 15min, P1: 1hr, P2: 4hr)
- Escalate if unable to resolve
- Document incidents in post-mortem

---

## 💾 Backup & Recovery

### Backup Strategy Overview

**Backup Objectives:**
- **RPO (Recovery Point Objective):** 24 hours (maximum data loss acceptable)
- **RTO (Recovery Time Objective):** 4 hours (maximum downtime acceptable)
- **Retention Policy:**
  - Daily backups: 30 days
  - Weekly backups: 3 months
  - Monthly backups: 1 year

### Database Backups

#### Automated Daily Backups

**Schedule:** Daily at 02:00 UTC (off-peak hours)

**Cron Configuration:**
```bash
# Add to crontab (crontab -e)
0 2 * * * /opt/erni-agents/scripts/backup-database.sh >> /var/log/erni-backup.log 2>&1
```

**Backup Script (`scripts/backup-database.sh`):**
```bash
#!/bin/bash
set -e

# Configuration
BACKUP_DIR="/backups/postgres"
S3_BUCKET="s3://erni-agents-backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
DAY_OF_WEEK=$(date +%u)  # 1=Monday, 7=Sunday
DAY_OF_MONTH=$(date +%d)
BACKUP_FILE="$BACKUP_DIR/erni_agents_$DATE.sql"
RETENTION_DAYS=30
RETENTION_WEEKS=90
RETENTION_MONTHS=365

# Create backup directory
mkdir -p $BACKUP_DIR

# Create backup
echo "Starting backup at $(date)"
docker exec erni-postgres pg_dump -U erni_user -Fc erni_agents > $BACKUP_FILE

# Compress
gzip $BACKUP_FILE
BACKUP_FILE="${BACKUP_FILE}.gz"

# Verify backup
if [ -f "$BACKUP_FILE" ]; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "Backup created: $BACKUP_FILE ($SIZE)"
else
    echo "ERROR: Backup failed!"
    exit 1
fi

# Upload to S3 (if configured)
if command -v aws &> /dev/null; then
    aws s3 cp "$BACKUP_FILE" "$S3_BUCKET/daily/" --storage-class STANDARD_IA
    echo "Uploaded to S3: $S3_BUCKET/daily/"
fi

# Weekly backup (Sunday)
if [ "$DAY_OF_WEEK" -eq 7 ]; then
    cp "$BACKUP_FILE" "$BACKUP_DIR/weekly_$(date +%Y%W).sql.gz"
    if command -v aws &> /dev/null; then
        aws s3 cp "$BACKUP_FILE" "$S3_BUCKET/weekly/" --storage-class GLACIER
    fi
    echo "Weekly backup created"
fi

# Monthly backup (1st of month)
if [ "$DAY_OF_MONTH" -eq 01 ]; then
    cp "$BACKUP_FILE" "$BACKUP_DIR/monthly_$(date +%Y%m).sql.gz"
    if command -v aws &> /dev/null; then
        aws s3 cp "$BACKUP_FILE" "$S3_BUCKET/monthly/" --storage-class DEEP_ARCHIVE
    fi
    echo "Monthly backup created"
fi

# Delete old backups
find $BACKUP_DIR -name "erni_agents_*.sql.gz" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "weekly_*.sql.gz" -mtime +$RETENTION_WEEKS -delete
find $BACKUP_DIR -name "monthly_*.sql.gz" -mtime +$RETENTION_MONTHS -delete

echo "Backup completed at $(date)"
```

**Make script executable:**
```bash
chmod +x /opt/erni-agents/scripts/backup-database.sh
```

#### Manual Backup

**Create immediate backup:**
```bash
/opt/erni-agents/scripts/backup-database.sh
```

**Or using docker directly:**
```bash
docker exec erni-postgres pg_dump -U erni_user -Fc erni_agents | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

#### Backup Verification

**Test backup integrity (monthly):**
```bash
# Extract backup
gunzip -c backup_20250105.sql.gz > backup_test.sql

# Restore to test database
docker exec -i erni-postgres psql -U erni_user -c "CREATE DATABASE test_restore;"
docker exec -i erni-postgres pg_restore -U erni_user -d test_restore < backup_test.sql

# Verify data
docker exec erni-postgres psql -U erni_user -d test_restore -c "SELECT COUNT(*) FROM conversations;"

# Cleanup
docker exec erni-postgres psql -U erni_user -c "DROP DATABASE test_restore;"
rm backup_test.sql
```

### Redis Backups

#### Automated Redis Backups

**Schedule:** Daily at 03:00 UTC

**Cron Configuration:**
```bash
0 3 * * * /opt/erni-agents/scripts/backup-redis.sh >> /var/log/erni-backup.log 2>&1
```

**Backup Script (`scripts/backup-redis.sh`):**
```bash
#!/bin/bash
set -e

BACKUP_DIR="/backups/redis"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/redis_$DATE.rdb"

mkdir -p $BACKUP_DIR

# Trigger Redis save
docker exec erni-redis redis-cli -a ${REDIS_PASSWORD} BGSAVE

# Wait for save to complete
sleep 10

# Copy RDB file
docker cp erni-redis:/data/dump.rdb "$BACKUP_FILE"

# Compress
gzip "$BACKUP_FILE"

# Delete old backups (7 days retention for Redis)
find $BACKUP_DIR -name "redis_*.rdb.gz" -mtime +7 -delete

echo "Redis backup completed: ${BACKUP_FILE}.gz"
```

#### Manual Redis Snapshot

```bash
docker exec erni-redis redis-cli -a ${REDIS_PASSWORD} BGSAVE
docker cp erni-redis:/data/dump.rdb ./redis_backup_$(date +%Y%m%d).rdb
```

### Application Code Backups

**Git Repository (Primary):**
```bash
# All code is version controlled in Git
git push origin main
git push origin --tags
```

**Configuration Backups:**
```bash
# Backup .env files (encrypted)
tar -czf env_backup_$(date +%Y%m%d).tar.gz python-backend/.env
gpg --encrypt --recipient admin@erni-gruppe.ch env_backup_$(date +%Y%m%d).tar.gz
```

### Backup Monitoring

**Verify backups are running:**
```bash
# Check cron logs
tail -f /var/log/erni-backup.log

# Check backup directory
ls -lh /backups/postgres/ | tail -10

# Check S3 backups (if configured)
aws s3 ls s3://erni-agents-backups/postgres/daily/ | tail -10
```

**Alert if backup fails:**
```yaml
# Add to Prometheus alertmanager
- alert: BackupFailed
  expr: time() - backup_last_success_timestamp > 86400
  for: 1h
  labels:
    severity: high
    priority: P1
  annotations:
    summary: "Database backup has not run in 24 hours"
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

### Team Structure

#### Development Team

| Role | Name | Email | Phone | Slack | Availability |
|------|------|-------|-------|-------|--------------|
| **Tech Lead** | TBD | tech.lead@erni-gruppe.ch | +41 XX XXX XX XX | @tech-lead | Mon-Fri 09:00-18:00 CET |
| **Backend Lead** | TBD | backend.lead@erni-gruppe.ch | +41 XX XXX XX XX | @backend-lead | Mon-Fri 09:00-18:00 CET |
| **Frontend Lead** | TBD | frontend.lead@erni-gruppe.ch | +41 XX XXX XX XX | @frontend-lead | Mon-Fri 09:00-18:00 CET |
| **DevOps Engineer** | TBD | devops@erni-gruppe.ch | +41 XX XXX XX XX | @devops | Mon-Fri 09:00-18:00 CET |
| **QA Lead** | TBD | qa@erni-gruppe.ch | +41 XX XXX XX XX | @qa-lead | Mon-Fri 09:00-18:00 CET |

#### Management

| Role | Name | Email | Phone | Escalation Level |
|------|------|-------|-------|------------------|
| **Engineering Manager** | TBD | eng.manager@erni-gruppe.ch | +41 XX XXX XX XX | Level 3 |
| **CTO** | TBD | cto@erni-gruppe.ch | +41 XX XXX XX XX | Level 4 |
| **Product Owner** | TBD | product@erni-gruppe.ch | +41 XX XXX XX XX | Business decisions |

### On-Call Rotation

**Schedule:** Weekly rotation (Monday 09:00 - Monday 09:00 CET)

**Current Week (Week of Jan 6, 2025):**

| Position | Name | Phone | Email | Slack |
|----------|------|-------|-------|-------|
| **Primary On-Call** | TBD | +41 XX XXX XX XX | oncall.primary@erni-gruppe.ch | @oncall-primary |
| **Secondary On-Call** | TBD | +41 XX XXX XX XX | oncall.secondary@erni-gruppe.ch | @oncall-secondary |

**Rotation Schedule:** See PagerDuty or `monitoring/oncall-schedule.md`

**On-Call Responsibilities:**
- Monitor alerts 24/7 during on-call period
- Respond to incidents within SLA:
  - P0 (Critical): 15 minutes
  - P1 (High): 1 hour
  - P2 (Medium): 4 hours
  - P3 (Low): Next business day
- Escalate to secondary if unable to resolve within 30 minutes
- Document all incidents in incident log
- Write post-mortem for P0/P1 incidents within 48 hours

**On-Call Compensation:**
- On-call allowance: CHF 200/week
- Incident response: CHF 100/hour (minimum 1 hour)
- Weekend/holiday incidents: 1.5x rate

### Escalation Path

**Incident Severity Levels:**

| Level | Severity | Response Time | Escalation After | Example |
|-------|----------|---------------|------------------|---------|
| **P0** | Critical | 15 minutes | 30 minutes | Service completely down |
| **P1** | High | 1 hour | 2 hours | Major feature broken |
| **P2** | Medium | 4 hours | 8 hours | Minor feature affected |
| **P3** | Low | Next business day | 2 business days | Cosmetic issue |

**Escalation Procedure:**

1. **Level 1: Primary On-Call Engineer**
   - First responder for all incidents
   - Response time: As per severity level
   - Actions:
     - Acknowledge alert in PagerDuty
     - Assess severity and impact
     - Begin troubleshooting
     - Update incident status in Slack (#incidents channel)

2. **Level 2: Secondary On-Call Engineer**
   - Escalated after: 30 minutes (P0), 2 hours (P1)
   - Actions:
     - Assist primary on-call
     - Provide second opinion
     - Take over if primary unavailable

3. **Level 3: Engineering Manager**
   - Escalated after: 1 hour (P0), 4 hours (P1)
   - Response time: 1 hour
   - Actions:
     - Coordinate resources
     - Make architectural decisions
     - Communicate with stakeholders
     - Approve emergency changes

4. **Level 4: CTO**
   - Escalated after: 2 hours (P0), 8 hours (P1)
   - Response time: 2 hours
   - Actions:
     - Executive decision making
     - External communication
     - Resource allocation
     - Business continuity decisions

**Escalation Contacts:**
```
Primary On-Call:   +41 XX XXX XX XX (PagerDuty)
Secondary On-Call: +41 XX XXX XX XX (PagerDuty)
Eng Manager:       +41 XX XXX XX XX
CTO:               +41 XX XXX XX XX
Emergency Hotline: +41 XX XXX XX XX (24/7)
```

### External Contacts

#### Service Providers

| Service | Contact | Phone | Email | Support Portal | SLA |
|---------|---------|-------|-------|----------------|-----|
| **OpenAI** | OpenAI Support | - | support@openai.com | https://help.openai.com | 24 hours |
| **Cloud Provider (AWS)** | AWS Support | +1-XXX-XXX-XXXX | - | https://console.aws.amazon.com/support | 1 hour (Business) |
| **DNS Provider (Cloudflare)** | Cloudflare Support | - | support@cloudflare.com | https://dash.cloudflare.com | 2 hours |
| **Monitoring (Datadog)** | Datadog Support | - | support@datadoghq.com | https://app.datadoghq.com/help | 4 hours |

#### Infrastructure

| Component | Provider | Contact | Emergency Procedure |
|-----------|----------|---------|---------------------|
| **Hosting** | TBD | TBD | See hosting provider runbook |
| **Database** | PostgreSQL (self-hosted) | Internal | Escalate to DevOps |
| **CDN** | TBD | TBD | Check CDN provider status page |
| **Email** | TBD | TBD | Use backup SMTP server |

#### Business Contacts

| Role | Name | Email | Phone | Purpose |
|------|------|-------|-------|---------|
| **Product Owner** | TBD | product@erni-gruppe.ch | +41 XX XXX XX XX | Business decisions |
| **Customer Success** | TBD | success@erni-gruppe.ch | +41 XX XXX XX XX | Customer communication |
| **Legal** | TBD | legal@erni-gruppe.ch | +41 XX XXX XX XX | Data breach, compliance |
| **PR/Communications** | TBD | pr@erni-gruppe.ch | +41 XX XXX XX XX | Public incidents |

### Communication Channels

**Internal:**
- **Slack Channels:**
  - `#incidents` - Active incident coordination
  - `#erni-alerts-critical` - P0 alerts
  - `#erni-alerts-high` - P1 alerts
  - `#on-call` - On-call coordination
  - `#engineering` - General engineering discussion

- **PagerDuty:** https://erni-gruppe.pagerduty.com
- **Status Page (Internal):** https://status.erni-gruppe.ch
- **Incident Management:** https://incidents.erni-gruppe.ch

**External:**
- **Status Page (Public):** https://status.erni-agents.com
- **Support Email:** support@erni-gruppe.ch
- **Emergency Hotline:** +41 XX XXX XX XX

### Incident Communication Template

**Initial Alert (within 15 minutes):**
```
🚨 INCIDENT ALERT

Severity: [P0/P1/P2/P3]
Status: Investigating
Impact: [Description of user impact]
Started: [Timestamp]
Incident Commander: [Name]

We are investigating [brief description]. Updates every 30 minutes.

Status Page: https://status.erni-agents.com
```

**Update (every 30 minutes for P0/P1):**
```
📊 INCIDENT UPDATE

Severity: [P0/P1/P2/P3]
Status: [Investigating/Identified/Monitoring/Resolved]
Impact: [Current impact]
Progress: [What we've done, what we're doing next]

Next update: [Timestamp]
```

**Resolution:**
```
✅ INCIDENT RESOLVED

Severity: [P0/P1/P2/P3]
Duration: [Total time]
Root Cause: [Brief description]
Resolution: [What fixed it]

Post-mortem: [Link] (available within 48 hours)
```

### Support Hours

**Business Hours:**
- Monday - Friday: 09:00 - 18:00 CET
- Saturday - Sunday: Closed (on-call only)
- Public Holidays: Closed (on-call only)

**On-Call Coverage:**
- 24/7/365 for P0 and P1 incidents
- P2/P3 incidents handled during business hours

**Response Time SLA:**
- P0 (Critical): 15 minutes (24/7)
- P1 (High): 1 hour (24/7)
- P2 (Medium): 4 hours (business hours)
- P3 (Low): Next business day

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
