# Environment Variables Documentation

This document describes all environment variables used by the ERNI Gruppe Building Agents API.

## Table of Contents

- [Required Variables](#required-variables)
- [OpenAI Configuration](#openai-configuration)
- [Agent Configuration](#agent-configuration)
- [Server Configuration](#server-configuration)
- [Database Configuration](#database-configuration)
- [Security Configuration](#security-configuration)
- [Performance Configuration](#performance-configuration)
- [Development Configuration](#development-configuration)

---

## Required Variables

These variables **must** be set for the application to function:

### `OPENAI_API_KEY`

- **Description**: OpenAI API key for accessing GPT models
- **Required**: Yes
- **Format**: `sk-proj-...` (starts with `sk-proj-` or `sk-`)
- **Example**: `sk-proj-abc123def456...`
- **Where to get**: https://platform.openai.com/api-keys
- **Security**: Never commit this to version control!

### `OPENAI_VECTOR_STORE_ID`

- **Description**: Vector Store ID for FAQ Agent knowledge base
- **Required**: Yes
- **Format**: `vs_...` (starts with `vs_`)
- **Example**: `vs_68e14a087e3c8191b4b7483ba3cb8d2a`
- **Where to get**: https://platform.openai.com/storage/vector_stores
- **Note**: Must be created and populated before starting the application

---

## OpenAI Configuration

### `OPENAI_ORG_ID`

- **Description**: OpenAI organization ID (if using organization account)
- **Required**: No
- **Default**: None
- **Format**: `org-...`
- **Example**: `org-abc123def456`

### `OPENAI_MAIN_AGENT_MODEL`

- **Description**: Model name for main agents
- **Required**: No
- **Default**: `gpt-4.1-mini`
- **Options**: `gpt-4o`, `gpt-4.1-mini`, `gpt-4-turbo`
- **Note**: Affects cost and performance

### `OPENAI_GUARDRAIL_MODEL`

- **Description**: Model name for guardrail agents
- **Required**: No
- **Default**: `gpt-4.1-mini`
- **Options**: `gpt-4o`, `gpt-4.1-mini`, `gpt-4-turbo`
- **Note**: Guardrails use simpler models for cost efficiency

---

## Agent Configuration

### `AGENT_TIMEOUT_SECONDS`

- **Description**: Maximum time (in seconds) for agent execution
- **Required**: No
- **Default**: `30`
- **Range**: `10` - `120`
- **Example**: `30`
- **Note**: Requests exceeding this timeout return 504 Gateway Timeout

### `AGENT_MAX_RETRIES`

- **Description**: Maximum retry attempts for OpenAI API calls
- **Required**: No
- **Default**: `3`
- **Range**: `1` - `5`
- **Example**: `3`
- **Note**: Uses exponential backoff between retries

### `GUARDRAIL_CACHE_TTL`

- **Description**: Time-to-live (in seconds) for guardrail cache entries
- **Required**: No
- **Default**: `3600` (1 hour)
- **Range**: `60` - `86400`
- **Example**: `3600`
- **Note**: Longer TTL = better performance, but stale results

### `GUARDRAIL_CACHE_SIZE`

- **Description**: Maximum number of entries in guardrail cache
- **Required**: No
- **Default**: `1000`
- **Range**: `100` - `10000`
- **Example**: `1000`
- **Note**: Higher size = more memory usage

---

## Server Configuration

### `HOST`

- **Description**: Server host address
- **Required**: No
- **Default**: `0.0.0.0`
- **Example**: `0.0.0.0` (all interfaces) or `127.0.0.1` (localhost only)

### `PORT`

- **Description**: Server port number
- **Required**: No
- **Default**: `8000`
- **Range**: `1024` - `65535`
- **Example**: `8000`

### `ENVIRONMENT`

- **Description**: Application environment
- **Required**: No
- **Default**: `development`
- **Options**: `development`, `staging`, `production`
- **Example**: `production`

### `DEBUG`

- **Description**: Enable debug mode
- **Required**: No
- **Default**: `true`
- **Options**: `true`, `false`
- **Example**: `false` (for production)

### `LOG_LEVEL`

- **Description**: Logging level
- **Required**: No
- **Default**: `INFO`
- **Options**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Example**: `INFO`

---

## Database Configuration

### `SESSIONS_DB_PATH`

- **Description**: Path to SQLite database for conversation sessions
- **Required**: No
- **Default**: `data/conversations.db`
- **Format**: Relative or absolute path
- **Example**: `data/conversations.db`
- **Note**: Directory will be created automatically if it doesn't exist

---

## Security Configuration

### `CORS_ORIGINS`

- **Description**: Comma-separated list of allowed CORS origins
- **Required**: No
- **Default**: `http://localhost:3000`
- **Format**: Comma-separated URLs
- **Example**: `http://localhost:3000,https://yourdomain.com,https://www.yourdomain.com`
- **Note**: Set to specific domains in production, not `*`

### `SECRET_KEY`

- **Description**: Secret key for session encryption
- **Required**: No (but recommended for production)
- **Format**: Random string (minimum 32 characters)
- **Example**: `your-secret-key-here-minimum-32-characters-long`
- **Generate**: `openssl rand -hex 32`

---

## Performance Configuration

### `RATE_LIMIT_PER_MINUTE`

- **Description**: Maximum requests per minute per IP
- **Required**: No
- **Default**: `60`
- **Range**: `1` - `1000`
- **Example**: `60`

### `RATE_LIMIT_PER_HOUR`

- **Description**: Maximum requests per hour per IP
- **Required**: No
- **Default**: `1000`
- **Range**: `10` - `100000`
- **Example**: `1000`

### `RATE_LIMIT_PER_DAY`

- **Description**: Maximum requests per day per IP
- **Required**: No
- **Default**: `10000`
- **Range**: `100` - `1000000`
- **Example**: `10000`

---

## Development Configuration

### `AUTO_RELOAD`

- **Description**: Enable auto-reload on code changes
- **Required**: No
- **Default**: `true`
- **Options**: `true`, `false`
- **Example**: `true` (development only)

---

## Example Configuration Files

### Minimal Configuration (Development)

```bash
# .env
OPENAI_API_KEY=sk-proj-your-api-key-here
OPENAI_VECTOR_STORE_ID=vs_your-vector-store-id-here
```

### Full Configuration (Production)

```bash
# .env
# OpenAI
OPENAI_API_KEY=sk-proj-your-api-key-here
OPENAI_VECTOR_STORE_ID=vs_your-vector-store-id-here
OPENAI_MAIN_AGENT_MODEL=gpt-4.1-mini
OPENAI_GUARDRAIL_MODEL=gpt-4.1-mini

# Agent Configuration
AGENT_TIMEOUT_SECONDS=30
AGENT_MAX_RETRIES=3
GUARDRAIL_CACHE_TTL=3600
GUARDRAIL_CACHE_SIZE=1000

# Server
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Database
SESSIONS_DB_PATH=data/conversations.db

# Security
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
SECRET_KEY=your-secret-key-here-minimum-32-characters-long

# Performance
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
RATE_LIMIT_PER_DAY=10000
```

---

## Security Best Practices

1. **Never commit `.env` file** to version control
2. **Use different API keys** for development, staging, and production
3. **Rotate secrets regularly** (every 90 days recommended)
4. **Set restrictive CORS origins** in production (not `*`)
5. **Use strong SECRET_KEY** (generate with `openssl rand -hex 32`)
6. **Enable HTTPS** in production
7. **Monitor API usage** to detect anomalies

---

## Troubleshooting

### "OPENAI_VECTOR_STORE_ID environment variable is required"

**Solution**: Set `OPENAI_VECTOR_STORE_ID` in your `.env` file. Get the ID from https://platform.openai.com/storage/vector_stores

### "OpenAI API check failed"

**Solution**: Verify `OPENAI_API_KEY` is correct and has sufficient credits. Check https://platform.openai.com/account/usage

### "Request timeout after 30 seconds"

**Solution**: Increase `AGENT_TIMEOUT_SECONDS` or optimize agent prompts to reduce execution time

### "Rate limit exceeded"

**Solution**: Increase `RATE_LIMIT_PER_MINUTE` or implement authentication to allow higher limits for authenticated users

---

## Additional Resources

- **OpenAI API Documentation**: https://platform.openai.com/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **OpenAI Agents SDK**: https://openai.github.io/openai-agents-python/
- **ERNI Gruppe Website**: https://www.erni-gruppe.ch

