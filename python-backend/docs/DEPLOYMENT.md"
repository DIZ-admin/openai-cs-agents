# ERNI Gruppe Building Agents - Production Deployment Guide

## Table of Contents
1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Environment Setup](#environment-setup)
4. [Database Configuration](#database-configuration)
5. [SSL/HTTPS Setup](#sslhttps-setup)
6. [Deployment Options](#deployment-options)
7. [Monitoring & Logging](#monitoring--logging)
8. [Security Best Practices](#security-best-practices)
9. [Performance Optimization](#performance-optimization)
10. [Pre-Deployment Checklist](#pre-deployment-checklist)
11. [Rollback Procedure](#rollback-procedure)
12. [Support & Maintenance](#support--maintenance)

---

## Overview

This guide provides comprehensive instructions for deploying the ERNI Gruppe Building Agents system to a production environment. The system consists of:

- **Backend:** Python FastAPI application with OpenAI Agents SDK
- **Frontend:** Next.js 15 application with React 19
- **Database:** PostgreSQL (recommended) or MySQL for persistent storage
- **Cache:** Redis for session management and rate limiting

---

## System Requirements

### Production Environment

#### Backend (Python)
- **Python:** 3.10+ (recommended 3.11 or 3.12)
- **Memory:** Minimum 2GB RAM, recommended 4GB+
- **CPU:** 2+ cores recommended
- **Storage:** 10GB+ available disk space

#### Frontend (Node.js)
- **Node.js:** 18.x LTS or 20.x LTS
- **npm:** 9.x or higher
- **Memory:** Minimum 1GB RAM, recommended 2GB+
- **CPU:** 2+ cores recommended

#### Database
- **PostgreSQL:** 14+ (recommended) or **MySQL:** 8.0+
- **Memory:** Minimum 2GB RAM
- **Storage:** 20GB+ for production data

#### Cache (Optional but Recommended)
- **Redis:** 6.x or 7.x
- **Memory:** 512MB minimum

### Network Requirements
- **Ports:**
  - Backend: 8000 (or custom)
  - Frontend: 3000 (or custom)
  - Database: 5432 (PostgreSQL) or 3306 (MySQL)
  - Redis: 6379
- **SSL/TLS:** Required for production
- **Firewall:** Configure to allow HTTPS (443) and block direct access to backend ports

---

## Environment Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-org/openai-cs-agents-demo.git
cd openai-cs-agents-demo
git checkout feature/erni-building-agents
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
cd python-backend
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Production Dependencies (Additional)
```bash
pip install gunicorn psycopg2-binary redis python-dotenv
```

### 3. Frontend Setup

#### Install Dependencies
```bash
cd ui
npm ci  # Use 'ci' for production (faster, more reliable)
```

#### Build for Production
```bash
npm run build
```

### 4. Environment Variables

Create `.env` file in `python-backend/` directory:

```bash
cp .env.example .env
```

**Required Variables:**
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-...

# Application Settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/erni_agents
# Or for MySQL:
# DATABASE_URL=mysql://user:password@localhost:3306/erni_agents

# Redis Configuration (for caching and rate limiting)
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here-min-32-chars
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Session Configuration
SESSION_TIMEOUT_MINUTES=30
```

**Frontend Environment Variables** (`.env.local` in `ui/` directory):
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_ENVIRONMENT=production
```

---

## Database Configuration

### PostgreSQL Setup (Recommended)

#### 1. Install PostgreSQL
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql@14
```

#### 2. Create Database and User
```sql
-- Connect to PostgreSQL
sudo -u postgres psql

-- Create database
CREATE DATABASE erni_agents;

-- Create user
CREATE USER erni_user WITH PASSWORD 'secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE erni_agents TO erni_user;

-- Exit
\q
```

#### 3. Initialize Schema
```bash
cd python-backend
python scripts/init_db.py  # Create this script for schema initialization
```

### MySQL Setup (Alternative)

#### 1. Install MySQL
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install mysql-server

# macOS
brew install mysql
```

#### 2. Create Database and User
```sql
-- Connect to MySQL
mysql -u root -p

-- Create database
CREATE DATABASE erni_agents CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user
CREATE USER 'erni_user'@'localhost' IDENTIFIED BY 'secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON erni_agents.* TO 'erni_user'@'localhost';
FLUSH PRIVILEGES;

-- Exit
EXIT;
```

### Database Schema

**Conversations Table:**
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    customer_name VARCHAR(255),
    customer_email VARCHAR(255),
    customer_phone VARCHAR(50),
    project_type VARCHAR(100),
    construction_type VARCHAR(100),
    area_sqm DECIMAL(10, 2),
    budget_chf DECIMAL(12, 2),
    consultation_booked BOOLEAN DEFAULT FALSE,
    specialist_assigned VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active'
);

CREATE INDEX idx_conversations_email ON conversations(customer_email);
CREATE INDEX idx_conversations_created ON conversations(created_at);
```

**Messages Table:**
```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(50) NOT NULL,  -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    agent_name VARCHAR(100),
    tool_calls JSONB
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_created ON messages(created_at);
```

---

## SSL/HTTPS Setup

### Option 1: Let's Encrypt (Free SSL)

#### 1. Install Certbot
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# macOS
brew install certbot
```

#### 2. Obtain Certificate
```bash
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

#### 3. Configure Nginx
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 4. Auto-Renewal
```bash
sudo certbot renew --dry-run
sudo systemctl enable certbot.timer
```

### Option 2: Cloud Provider SSL
- **AWS:** Use AWS Certificate Manager (ACM) with CloudFront or ALB
- **Azure:** Use Azure App Service SSL or Application Gateway
- **GCP:** Use Google-managed SSL certificates with Load Balancer
- **Vercel:** Automatic SSL for custom domains

---

## Deployment Options

### Option 1: Traditional Server (VPS/Dedicated)

#### Backend Deployment with Gunicorn

**1. Create systemd service** (`/etc/systemd/system/erni-backend.service`):
```ini
[Unit]
Description=ERNI Building Agents Backend
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/erni-agents/python-backend
Environment="PATH=/var/www/erni-agents/python-backend/.venv/bin"
ExecStart=/var/www/erni-agents/python-backend/.venv/bin/gunicorn \
    -k uvicorn.workers.UvicornWorker \
    -w 4 \
    -b 127.0.0.1:8000 \
    --timeout 120 \
    --access-logfile /var/log/erni-backend/access.log \
    --error-logfile /var/log/erni-backend/error.log \
    api:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**2. Start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable erni-backend
sudo systemctl start erni-backend
sudo systemctl status erni-backend
```

#### Frontend Deployment with PM2

**1. Install PM2:**
```bash
npm install -g pm2
```

**2. Create ecosystem file** (`ecosystem.config.js`):
```javascript
module.exports = {
  apps: [{
    name: 'erni-frontend',
    cwd: '/var/www/erni-agents/ui',
    script: 'npm',
    args: 'start',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    instances: 2,
    exec_mode: 'cluster',
    max_memory_restart: '1G',
    error_file: '/var/log/erni-frontend/error.log',
    out_file: '/var/log/erni-frontend/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
  }]
};
```

**3. Start with PM2:**
```bash
cd /var/www/erni-agents/ui
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### Option 2: Docker Deployment

See `docker-compose.yml` and `Dockerfile` in the repository.

```bash
docker-compose up -d --build
```

### Option 3: Cloud Platforms

#### Vercel (Frontend Only - Recommended for Next.js)
```bash
cd ui
vercel --prod
```

#### AWS Elastic Beanstalk
```bash
eb init -p python-3.11 erni-agents
eb create erni-agents-prod
eb deploy
```

#### Google Cloud Run
```bash
gcloud run deploy erni-backend --source python-backend --region us-central1
gcloud run deploy erni-frontend --source ui --region us-central1
```

#### Azure App Service
```bash
az webapp up --name erni-agents --runtime "PYTHON:3.11"
```

---

## Monitoring & Logging

### Application Logging

#### Backend Logging Configuration
```python
# python-backend/logging_config.py
import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging(log_level: str = "INFO"):
    """Configure application logging."""

    # Create logger
    logger = logging.getLogger("erni_agents")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)

    # File handler (rotating)
    file_handler = RotatingFileHandler(
        '/var/log/erni-backend/app.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(file_format)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
```

### Monitoring Tools

#### 1. Application Performance Monitoring (APM)

**Sentry (Recommended):**
```bash
pip install sentry-sdk
```

```python
# python-backend/api.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="https://your-sentry-dsn@sentry.io/project-id",
    integrations=[FastApiIntegration()],
    environment="production",
    traces_sample_rate=0.1,
)
```

**New Relic:**
```bash
pip install newrelic
newrelic-admin run-program gunicorn api:app
```

#### 2. Infrastructure Monitoring

**Prometheus + Grafana:**
```bash
# Install prometheus-fastapi-instrumentator
pip install prometheus-fastapi-instrumentator
```

```python
# python-backend/api.py
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)
```

#### 3. Log Aggregation

**ELK Stack (Elasticsearch, Logstash, Kibana):**
- Centralized log collection
- Real-time log analysis
- Custom dashboards

**CloudWatch (AWS):**
```bash
# Install CloudWatch agent
sudo yum install amazon-cloudwatch-agent
```

### Health Checks

The ERNI Building Agents API provides two health check endpoints for monitoring and orchestration:

#### 1. Health Endpoint (`/health`)

**Purpose:** Basic liveness check for load balancers and monitoring systems.

**Endpoint:** `GET /health`

**Response (200 OK):**
```json
{
    "status": "healthy",
    "timestamp": "2025-10-04T09:42:20.160176",
    "version": "1.0.0",
    "environment": "development",
    "service": "ERNI Building Agents API"
}
```

**Usage:**
```bash
# Check if service is alive
curl http://127.0.0.1:8000/health

# In Docker Compose
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

**Characteristics:**
- ✅ No authentication required
- ✅ Fast response (< 50ms)
- ✅ Does not check dependencies
- ✅ Always returns 200 OK if service is running

---

#### 2. Readiness Endpoint (`/readiness`)

**Purpose:** Comprehensive dependency check for Kubernetes readiness probes.

**Endpoint:** `GET /readiness`

**Response (200 OK - All dependencies ready):**
```json
{
    "status": "ready",
    "timestamp": "2025-10-04T09:42:22.644740",
    "checks": {
        "openai_api": true,
        "environment_configured": true
    },
    "version": "1.0.0"
}
```

**Response (503 Service Unavailable - Dependencies not ready):**
```json
{
    "status": "not_ready",
    "timestamp": "2025-10-04T09:42:22.644740",
    "checks": {
        "openai_api": false,
        "environment_configured": true
    },
    "version": "1.0.0"
}
```

**Checks Performed:**
1. **environment_configured** - Verifies OPENAI_API_KEY is set
2. **openai_api** - Tests connectivity to OpenAI API (GET /v1/models)

**Usage:**
```bash
# Check if service is ready to accept traffic
curl http://127.0.0.1:8000/readiness

# In Kubernetes
readinessProbe:
  httpGet:
    path: /readiness
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 5
  failureThreshold: 3
```

**Characteristics:**
- ✅ No authentication required
- ⚠️ Slower response (up to 5 seconds due to OpenAI API check)
- ✅ Checks all critical dependencies
- ✅ Returns 503 if any dependency is unavailable

---

#### Implementation

**Backend Health Endpoints:**
```python
# python-backend/api.py
from fastapi import FastAPI, Response, status
from datetime import datetime
import os
import httpx

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    Returns basic application health status.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "service": "ERNI Building Agents API"
    }

@app.get("/readiness")
async def readiness_check(response: Response):
    """
    Readiness check endpoint for Kubernetes/Docker health checks.
    Verifies that all dependencies are available.
    """
    checks = {
        "openai_api": False,
        "environment_configured": False,
    }

    # Check if OPENAI_API_KEY is configured
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and len(openai_key) > 0:
        checks["environment_configured"] = True

    # Check OpenAI API connectivity
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            headers = {
                "Authorization": f"Bearer {openai_key}",
                "Content-Type": "application/json"
            }
            api_response = await client.get(
                "https://api.openai.com/v1/models",
                headers=headers
            )
            if api_response.status_code == 200:
                checks["openai_api"] = True
    except Exception as e:
        logger.warning(f"OpenAI API check failed: {e}")
        checks["openai_api"] = False

    # Determine overall readiness
    all_ready = all(checks.values())

    if not all_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": "ready" if all_ready else "not_ready",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks,
        "version": "1.0.0"
    }
```

---

## Security Best Practices

### 1. API Key Management

**Never commit API keys to version control:**
```bash
# Verify .env is in .gitignore
grep -q "^\.env$" .gitignore || echo ".env" >> .gitignore
```

**Use environment-specific keys:**
- Development: Limited quota, test mode
- Staging: Separate key with monitoring
- Production: Full quota, strict rate limits

**Rotate keys regularly:**
- Schedule: Every 90 days minimum
- Process: Generate new key → Update .env → Restart services → Revoke old key

### 2. Input Validation

**Backend validation with Pydantic:**
```python
from pydantic import BaseModel, validator, EmailStr

class CustomerContact(BaseModel):
    name: str
    email: EmailStr
    phone: str

    @validator('name')
    def validate_name(cls, v):
        if len(v) < 2 or len(v) > 100:
            raise ValueError('Name must be 2-100 characters')
        return v.strip()

    @validator('phone')
    def validate_phone(cls, v):
        # Swiss phone number format
        import re
        if not re.match(r'^\+41\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}$', v):
            raise ValueError('Invalid Swiss phone number')
        return v
```

### 3. Rate Limiting

**Install dependencies:**
```bash
pip install slowapi redis
```

**Configure rate limiting:**
```python
# python-backend/api.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/chat")
@limiter.limit("60/minute")
async def chat_endpoint(request: Request):
    # ... endpoint logic
    pass
```

### 4. CORS Configuration

**Production CORS settings:**
```python
# python-backend/api.py
from fastapi.middleware.cors import CORSMiddleware
import os

allowed_origins = os.getenv("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Specific domains only
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Limit methods
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,
)
```

### 5. Content Security Policy

**Next.js CSP configuration:**
```javascript
// ui/next.config.js
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-eval' 'unsafe-inline';
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https:;
      font-src 'self' data:;
      connect-src 'self' https://api.yourdomain.com;
      frame-ancestors 'none';
    `.replace(/\s{2,}/g, ' ').trim()
  },
  {
    key: 'X-Frame-Options',
    value: 'DENY'
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'Referrer-Policy',
    value: 'strict-origin-when-cross-origin'
  },
  {
    key: 'Permissions-Policy',
    value: 'camera=(), microphone=(), geolocation=()'
  }
];

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ];
  },
};
```

### 6. Secrets Management

**AWS Secrets Manager:**
```python
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Usage
secrets = get_secret('erni-agents/production')
OPENAI_API_KEY = secrets['OPENAI_API_KEY']
```

**Azure Key Vault:**
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://your-vault.vault.azure.net/", credential=credential)
OPENAI_API_KEY = client.get_secret("OPENAI-API-KEY").value
```

---

## Performance Optimization

### 1. Frontend Optimization

**Next.js Production Build:**
```bash
# Build with optimizations
npm run build

# Analyze bundle size
npm install -g @next/bundle-analyzer
ANALYZE=true npm run build
```

**Image Optimization:**
```javascript
// Use Next.js Image component
import Image from 'next/image';

<Image
  src="/logo.png"
  alt="ERNI Logo"
  width={200}
  height={100}
  priority
/>
```

**Code Splitting:**
```javascript
// Dynamic imports for large components
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <p>Loading...</p>,
  ssr: false
});
```

### 2. Backend Optimization

**Response Compression:**
```python
# python-backend/api.py
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

**Database Connection Pooling:**
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

**Caching with Redis:**
```python
import redis
from functools import wraps

redis_client = redis.from_url(os.getenv("REDIS_URL"))

def cache_response(ttl=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator
```

### 3. CDN Configuration

**CloudFlare:**
- Enable caching for static assets
- Configure page rules for API endpoints
- Enable Brotli compression

**AWS CloudFront:**
```json
{
  "CacheBehaviors": [
    {
      "PathPattern": "/_next/static/*",
      "TargetOriginId": "frontend",
      "ViewerProtocolPolicy": "redirect-to-https",
      "Compress": true,
      "DefaultTTL": 31536000
    }
  ]
}
```

---

## Pre-Deployment Checklist

### Security Checklist
- [ ] All API keys stored in environment variables
- [ ] `.env` file in `.gitignore`
- [ ] HTTPS/SSL configured and tested
- [ ] CORS configured with specific origins
- [ ] Rate limiting enabled
- [ ] Input validation implemented
- [ ] CSP headers configured
- [ ] Security headers enabled (X-Frame-Options, etc.)
- [ ] Database credentials rotated
- [ ] Secrets management configured

### Performance Checklist
- [ ] Frontend production build tested
- [ ] Bundle size analyzed and optimized
- [ ] Images optimized
- [ ] Compression enabled (Gzip/Brotli)
- [ ] CDN configured for static assets
- [ ] Database indexes created
- [ ] Connection pooling configured
- [ ] Caching strategy implemented

### Monitoring Checklist
- [ ] Application logging configured
- [ ] Error tracking enabled (Sentry/New Relic)
- [ ] Health check endpoints implemented
- [ ] Uptime monitoring configured
- [ ] Performance monitoring enabled
- [ ] Log aggregation configured
- [ ] Alerts configured for critical errors
- [ ] Dashboard created for key metrics

### Infrastructure Checklist
- [ ] Database backups configured
- [ ] Auto-scaling configured (if applicable)
- [ ] Load balancer configured
- [ ] Firewall rules configured
- [ ] DNS records configured
- [ ] SSL certificates valid and auto-renewing
- [ ] Disaster recovery plan documented
- [ ] Rollback procedure tested

### Testing Checklist
- [ ] All agents tested in production-like environment
- [ ] Load testing completed
- [ ] Security scanning completed
- [ ] Accessibility testing completed
- [ ] Cross-browser testing completed
- [ ] Mobile responsiveness tested
- [ ] API endpoints tested
- [ ] Error handling tested

---

## Rollback Procedure

### Immediate Rollback (< 5 minutes)

**1. Identify Issue:**
```bash
# Check application logs
sudo journalctl -u erni-backend -n 100 --no-pager
pm2 logs erni-frontend --lines 100

# Check system resources
htop
df -h
```

**2. Rollback Backend:**
```bash
# Stop current version
sudo systemctl stop erni-backend

# Restore previous version
cd /var/www/erni-agents/python-backend
git checkout <previous-commit-hash>
source .venv/bin/activate
pip install -r requirements.txt

# Restart service
sudo systemctl start erni-backend
```

**3. Rollback Frontend:**
```bash
# Stop current version
pm2 stop erni-frontend

# Restore previous version
cd /var/www/erni-agents/ui
git checkout <previous-commit-hash>
npm ci
npm run build

# Restart service
pm2 restart erni-frontend
```

**4. Verify Rollback:**
```bash
curl -I https://yourdomain.com
curl https://api.yourdomain.com/health
```

### Database Rollback

**1. Restore from Backup:**
```bash
# PostgreSQL
pg_restore -U erni_user -d erni_agents /backups/erni_agents_backup.dump

# MySQL
mysql -u erni_user -p erni_agents < /backups/erni_agents_backup.sql
```

**2. Verify Data Integrity:**
```sql
SELECT COUNT(*) FROM conversations;
SELECT COUNT(*) FROM messages;
```

---

## Support & Maintenance

### Support Contacts

**Technical Support:**
- **Email:** tech-support@erni-gruppe.ch
- **Phone:** +41 41 757 30 30
- **On-Call:** Available 24/7 for critical issues

**Development Team:**
- **Lead Developer:** [Name] - [email]
- **DevOps Engineer:** [Name] - [email]
- **Project Manager:** [Name] - [email]

### Maintenance Windows

**Regular Maintenance:**
- **Schedule:** Every Sunday 02:00-04:00 CET
- **Notification:** 48 hours advance notice
- **Duration:** Maximum 2 hours

**Emergency Maintenance:**
- **Trigger:** Critical security issues or system failures
- **Notification:** Immediate via email and SMS
- **Duration:** As needed

### Backup Schedule

**Database Backups:**
- **Full Backup:** Daily at 01:00 CET
- **Incremental:** Every 6 hours
- **Retention:** 30 days
- **Location:** Encrypted cloud storage + off-site

**Application Backups:**
- **Code:** Git repository (GitHub/GitLab)
- **Configuration:** Encrypted backup daily
- **Logs:** Retained for 90 days

### Monitoring Alerts

**Critical Alerts (Immediate Response):**
- Application down (> 1 minute)
- Database connection failure
- SSL certificate expiration (< 7 days)
- Disk space > 90% full
- Memory usage > 95%

**Warning Alerts (Response within 1 hour):**
- High error rate (> 5% of requests)
- Slow response time (> 2 seconds average)
- High CPU usage (> 80% for 10 minutes)
- Failed backup

### Post-Deployment Monitoring

**First 24 Hours:**
- Monitor error rates every hour
- Check performance metrics every 2 hours
- Review user feedback
- Verify all integrations working

**First Week:**
- Daily review of logs and metrics
- Monitor user adoption
- Collect feedback from ERNI team
- Address any issues promptly

**Ongoing:**
- Weekly performance review
- Monthly security audit
- Quarterly capacity planning
- Annual disaster recovery drill

---

## Additional Resources

- **OpenAI Agents SDK:** https://openai.github.io/openai-agents-python/
- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **Next.js Documentation:** https://nextjs.org/docs
- **ERNI Gruppe Website:** https://www.erni-gruppe.ch/
- **Project Documentation:** See [AGENTS.md](../../AGENTS.md) and [planning.md](../../planning.md)

---

## License

This deployment guide is part of the ERNI Gruppe Building Agents project. See LICENSE file for details.

**Last Updated:** January 2025
**Version:** 1.0.0
