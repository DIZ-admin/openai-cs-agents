# JWT Authentication Guide

## Overview

The ERNI Gruppe Building Agents API uses JWT (JSON Web Token) based authentication to secure endpoints. This guide explains how to authenticate and use protected endpoints.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication Flow](#authentication-flow)
3. [API Endpoints](#api-endpoints)
4. [Usage Examples](#usage-examples)
5. [Security Best Practices](#security-best-practices)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start

### 1. Obtain Access Token

**Request:**
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo&password=secret"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 2. Use Token in Requests

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to build a house",
    "conversation_id": ""
  }'
```

---

## Authentication Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Auth Module
    participant Database

    Client->>API: POST /auth/token (username, password)
    API->>Auth Module: authenticate_user()
    Auth Module->>Database: get_user(username)
    Database-->>Auth Module: User data
    Auth Module->>Auth Module: verify_password()
    Auth Module-->>API: User authenticated
    API->>Auth Module: create_access_token()
    Auth Module-->>API: JWT token
    API-->>Client: {access_token, expires_in}
    
    Client->>API: POST /chat (with Authorization header)
    API->>Auth Module: get_current_user()
    Auth Module->>Auth Module: decode_access_token()
    Auth Module-->>API: User object
    API->>API: Process request
    API-->>Client: Response
```

---

## API Endpoints

### POST /auth/token

Authenticate and obtain JWT access token.

**Request:**
- **Method:** POST
- **Content-Type:** application/x-www-form-urlencoded
- **Parameters:**
  - `username` (string, required): User's username
  - `password` (string, required): User's password

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Status Codes:**
- `200 OK` - Authentication successful
- `401 Unauthorized` - Invalid credentials

---

### GET /auth/me

Get current authenticated user's information.

**Request:**
- **Method:** GET
- **Headers:**
  - `Authorization: Bearer <token>`

**Response:**
```json
{
  "username": "demo",
  "email": "demo@erni-gruppe.ch",
  "full_name": "Demo User",
  "disabled": false,
  "roles": ["user"]
}
```

**Status Codes:**
- `200 OK` - User information retrieved
- `401 Unauthorized` - Invalid or expired token
- `403 Forbidden` - User account disabled

---

## Usage Examples

### Python (requests)

```python
import requests

# 1. Obtain token
auth_response = requests.post(
    "http://localhost:8000/auth/token",
    data={"username": "demo", "password": "secret"}
)
token = auth_response.json()["access_token"]

# 2. Use token in requests
headers = {"Authorization": f"Bearer {token}"}
chat_response = requests.post(
    "http://localhost:8000/chat",
    headers=headers,
    json={
        "message": "How much would a 150m² house cost?",
        "conversation_id": ""
    }
)
print(chat_response.json())
```

### JavaScript (fetch)

```javascript
// 1. Obtain token
const authResponse = await fetch('http://localhost:8000/auth/token', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    username: 'demo',
    password: 'secret'
  })
});
const { access_token } = await authResponse.json();

// 2. Use token in requests
const chatResponse = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: 'I want to build a house',
    conversation_id: ''
  })
});
const data = await chatResponse.json();
console.log(data);
```

### cURL

```bash
# 1. Obtain token
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo&password=secret" \
  | jq -r '.access_token')

# 2. Use token
curl -X POST "http://localhost:8000/chat" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What services does ERNI offer?",
    "conversation_id": ""
  }'
```

---

## Demo Credentials

**User Account:**
- Username: `demo`
- Password: `secret`
- Roles: `["user"]`

**Admin Account:**
- Username: `admin`
- Password: `secret`
- Roles: `["admin", "user"]`

⚠️ **WARNING:** Change these credentials in production!

---

## Security Best Practices

### 1. Token Storage

**✅ DO:**
- Store tokens in memory (JavaScript variables)
- Use secure, httpOnly cookies for web applications
- Clear tokens on logout

**❌ DON'T:**
- Store tokens in localStorage (vulnerable to XSS)
- Store tokens in sessionStorage (vulnerable to XSS)
- Include tokens in URLs

### 2. Token Expiration

- Tokens expire after 30 minutes by default
- Request a new token when expired
- Implement automatic token refresh in production

### 3. HTTPS

- **Always use HTTPS in production**
- Never send tokens over unencrypted HTTP
- Set `FORCE_HTTPS=true` in production environment

### 4. Secret Key Management

```bash
# Generate secure secret key
openssl rand -hex 32

# Set in environment variables (NOT in code)
export JWT_SECRET_KEY="your-generated-secret-key-here"
```

### 5. Password Security

- Use strong passwords (minimum 12 characters)
- Implement password complexity requirements
- Enable rate limiting on login endpoint
- Consider implementing 2FA for admin accounts

---

## Configuration

### Environment Variables

```bash
# JWT secret key (REQUIRED in production)
JWT_SECRET_KEY=your-secret-key-here-minimum-32-characters-long

# Token expiration (default: 30 minutes)
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Refresh token expiration (default: 7 days)
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Require authentication for all endpoints (default: false)
REQUIRE_AUTH=false
```

> ℹ️  При `REQUIRE_AUTH=false` токен авторизации остаётся опциональным: если клиент передаёт корректный JWT, сервер распознаёт пользователя и связывает событие с учётной записью, иначе запрос обрабатывается анонимно.

> 💡 Если `JWT_SECRET_KEY` не задан, сервер автоматически использует `SECRET_KEY`. Для production рекомендуется задать оба значения явно и убедиться, что они достаточно длинные (≥32 символов).

### Enforcing Authentication

To require authentication for all endpoints:

```bash
# In .env file
REQUIRE_AUTH=true
```

When `REQUIRE_AUTH=true`:
- All `/chat` requests require valid JWT token
- Unauthenticated requests return `401 Unauthorized`
- `/auth/token` and `/auth/me` remain accessible

---

## Troubleshooting

### Error: "Could not validate credentials"

**Cause:** Invalid or expired token

**Solution:**
1. Check token format: `Bearer <token>`
2. Verify token hasn't expired (30 min default)
3. Request a new token

### Error: "Incorrect username or password"

**Cause:** Invalid credentials

**Solution:**
1. Verify username and password
2. Check for typos
3. Ensure user account exists

### Error: "User account is disabled"

**Cause:** User account has been disabled

**Solution:**
1. Contact administrator
2. Check user status in database

### Token Expiration

**Symptoms:**
- Requests fail with `401 Unauthorized` after 30 minutes
- Previously working token stops working

**Solution:**
```python
# Implement token refresh logic
def get_valid_token():
    if token_expired():
        token = refresh_token()
    return token
```

---

## Production Deployment Checklist

- [ ] Change default passwords
- [ ] Generate secure JWT_SECRET_KEY
- [ ] Set `REQUIRE_AUTH=true`
- [ ] Enable HTTPS
- [ ] Configure rate limiting
- [ ] Implement token refresh mechanism
- [ ] Set up monitoring for failed auth attempts
- [ ] Configure session timeout
- [ ] Enable audit logging
- [ ] Test authentication flow end-to-end

---

## Additional Resources

- [JWT.io](https://jwt.io/) - JWT debugger and documentation
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)

---

## Support

For issues or questions:
- Check [Troubleshooting](#troubleshooting) section
- Review API documentation at `/docs`
- Contact: admin@erni-gruppe.ch
