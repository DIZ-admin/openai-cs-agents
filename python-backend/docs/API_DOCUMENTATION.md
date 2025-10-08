# API Documentation

ERNI Gruppe Building Agents API - Complete API Reference

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.erni-gruppe.ch` (example)

## Interactive Documentation

The API provides two interactive documentation interfaces:

- **Swagger UI**: `http://localhost:8000/docs`
  - Interactive API explorer
  - Try out endpoints directly in the browser
  - View request/response schemas
  - See example requests and responses

- **ReDoc**: `http://localhost:8000/redoc`
  - Clean, three-panel documentation
  - Better for reading and understanding
  - Printable documentation
  - Search functionality

## Authentication

Currently, the API does not require authentication. In production, implement proper authentication mechanisms (API keys, OAuth2, JWT, etc.).

## Rate Limiting

All endpoints are rate-limited to prevent abuse:

- **10 requests per minute** per IP address for `/chat` endpoint
- Returns `429 Too Many Requests` if limit exceeded
- Rate limit headers included in response:
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Time when limit resets

## Endpoints

### Chat Endpoints

#### POST /chat

Send a message to the building agents system.

**Request Body:**

```json
{
  "conversation_id": "conv_abc123def456",  // Optional: omit for new conversation
  "message": "I want to build a house"
}
```

**Response (200 OK):**

```json
{
  "conversation_id": "conv_abc123def456",
  "current_agent": "Triage Agent",
  "messages": [
    {
      "content": "Welcome to ERNI Gruppe! How can I help you today?",
      "agent": "Triage Agent"
    }
  ],
  "events": [],
  "context": {
    "inquiry_id": "INQ-12345"
  },
  "agents": [
    {
      "name": "Triage Agent",
      "description": "Main routing agent",
      "handoffs": ["Project Information Agent", "Cost Estimation Agent"],
      "tools": [],
      "guardrails": ["Relevance Guardrail", "Jailbreak Guardrail"]
    }
  ],
  "guardrails": []
}
```

**Error Responses:**

- `400 Bad Request`: Invalid request format
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Unexpected server error
- `503 Service Unavailable`: OpenAI API temporarily unavailable
- `504 Gateway Timeout`: Request took too long (>30 seconds)

**Example Usage (curl):**

```bash
# New conversation
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to build a house"}'

# Continue conversation
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv_abc123def456",
    "message": "How much would it cost?"
  }'
```

**Example Usage (Python):**

```python
import requests

# New conversation
response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "I want to build a house"}
)
data = response.json()
conversation_id = data["conversation_id"]

# Continue conversation
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "conversation_id": conversation_id,
        "message": "How much would it cost?"
    }
)
```

**Example Usage (JavaScript):**

```javascript
// New conversation
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'I want to build a house' })
});
const data = await response.json();
const conversationId = data.conversation_id;

// Continue conversation
const response2 = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    conversation_id: conversationId,
    message: 'How much would it cost?'
  })
});
```

---

### Health Check Endpoints

#### GET /health

Basic health check endpoint.

**Response (200 OK):**

```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00.000Z",
  "version": "1.0.0",
  "environment": "production",
  "service": "ERNI Building Agents API"
}
```

**Example Usage:**

```bash
curl http://localhost:8000/health
```

---

#### GET /readiness

Readiness check endpoint for Kubernetes/Docker.

**Response (200 OK - Ready):**

```json
{
  "status": "ready",
  "timestamp": "2025-01-15T10:30:00.000Z",
  "checks": {
    "openai_api": true,
    "environment_configured": true
  },
  "version": "1.0.0"
}
```

**Response (503 Service Unavailable - Not Ready):**

```json
{
  "status": "not_ready",
  "timestamp": "2025-01-15T10:30:00.000Z",
  "checks": {
    "openai_api": false,
    "environment_configured": true
  },
  "version": "1.0.0"
}
```

**Example Usage:**

```bash
curl http://localhost:8000/readiness
```

---

### Agent Information Endpoints

#### GET /agents

List all available agents with their metadata.

**Response (200 OK):**

```json
{
  "agents": [
    {
      "name": "Triage Agent",
      "description": "A triage agent that can delegate a customer's request to the appropriate agent.",
      "handoffs": [
        "Project Information Agent",
        "Cost Estimation Agent",
        "Project Status Agent",
        "Appointment Booking Agent",
        "FAQ Agent"
      ],
      "tools": [],
      "guardrails": [
        "Relevance Guardrail",
        "Jailbreak Guardrail",
        "PII Guardrail"
      ]
    },
    {
      "name": "Cost Estimation Agent",
      "description": "Provides preliminary cost estimates for building projects.",
      "handoffs": [
        "Triage Agent",
        "Appointment Booking Agent"
      ],
      "tools": [
        "estimate_project_cost"
      ],
      "guardrails": [
        "Relevance Guardrail",
        "Jailbreak Guardrail",
        "PII Guardrail"
      ]
    }
  ],
  "total": 6,
  "timestamp": "2025-01-15T10:30:00.000Z"
}
```

**Example Usage:**

```bash
curl http://localhost:8000/agents
```

---

## Data Models

### ChatRequest

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `conversation_id` | string | No | Conversation ID to continue existing conversation |
| `message` | string | Yes | User's message to send to the agent |

### ChatResponse

| Field | Type | Description |
|-------|------|-------------|
| `conversation_id` | string | Unique conversation identifier |
| `current_agent` | string | Name of currently active agent |
| `messages` | array | List of messages from agents |
| `events` | array | List of events during execution |
| `context` | object | Current conversation context |
| `agents` | array | List of available agents |
| `guardrails` | array | List of guardrail checks performed |

### MessageResponse

| Field | Type | Description |
|-------|------|-------------|
| `content` | string | Message content from agent |
| `agent` | string | Name of agent that generated message |

### AgentEvent

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique event identifier |
| `type` | string | Event type (handoff, tool_call, message) |
| `agent` | string | Agent that generated event |
| `content` | string | Event content or description |
| `metadata` | object | Optional additional metadata |
| `timestamp` | number | Unix timestamp when event occurred |

### GuardrailCheck

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique check identifier |
| `name` | string | Guardrail name |
| `input` | string | Input text that was checked |
| `reasoning` | string | Guardrail's reasoning |
| `passed` | boolean | Whether check passed |
| `timestamp` | number | Unix timestamp when check occurred |

---

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request format or parameters |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | OpenAI API temporarily unavailable |
| 504 | Gateway Timeout | Request took too long (>30 seconds) |

---

## CORS Configuration

The API supports Cross-Origin Resource Sharing (CORS) for web applications.

**Allowed Origins** (configured via `CORS_ORIGINS` environment variable):
- Development: `http://localhost:3000`
- Production: Configure specific domains

**Allowed Methods:**
- `GET`
- `POST`

**Allowed Headers:**
- `Content-Type`
- `Authorization`

---

## Best Practices

1. **Reuse conversation_id** to maintain context across multiple messages
2. **Handle rate limits** gracefully with exponential backoff
3. **Implement timeout handling** for long-running requests
4. **Validate responses** before using data
5. **Log errors** for debugging and monitoring
6. **Use HTTPS** in production
7. **Implement authentication** for production deployments

---

## Support

For API support, contact:
- **Email**: info@erni-gruppe.ch
- **Website**: https://www.erni-gruppe.ch
- **Documentation**: http://localhost:8000/docs (Swagger UI)

