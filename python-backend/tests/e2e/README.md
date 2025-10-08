# E2E Tests for ERNI Gruppe Building Agents

## Overview

This directory contains end-to-end (E2E) tests for the complete ERNI Gruppe Building Agents application stack, including both backend API and frontend integration.

## Test Coverage

### 1. Basic Triage Agent Conversation
- Verifies greeting and initial response
- Checks conversation ID creation
- Validates context initialization

### 2. Cost Estimation Flow
- Tests agent handoff to Cost Estimation Agent
- Validates multi-step conversation
- Checks context updates (project_type, construction_type, area_sqm, budget_chf)

### 3. Project Status Flow
- Tests project status inquiry
- Validates agent handoff to Project Status Agent
- Checks project information retrieval

### 4. Appointment Booking Flow
- Tests consultation booking request
- Validates agent handoff to Appointment Booking Agent
- Checks specialist availability display

### 5. Guardrails
- **Relevance Guardrail:** Blocks off-topic messages
- **Jailbreak Guardrail:** Blocks prompt injection attempts

### 6. Frontend Integration
- Tests Next.js proxy functionality
- Validates frontend-backend communication
- Checks CORS configuration

### 7. Performance
- Measures response times
- Validates performance benchmarks (< 10s)

### 8. Multi-turn Conversation
- Tests context preservation across multiple turns
- Validates conversation continuity

## Prerequisites

### Running Services
- Backend server running on `http://127.0.0.1:8000`
- Frontend server running on `http://localhost:3000`

### Dependencies
- Python 3.9+
- pytest
- requests

## Running Tests

### Quick Start
```bash
# From project root
./run_e2e_tests.sh
```

### Manual Execution
```bash
# Run all E2E tests
cd python-backend
.venv/bin/pytest tests/e2e/ -v

# Run specific test class
.venv/bin/pytest tests/e2e/test_e2e_full_stack.py::TestTriageAgent -v

# Run specific test
.venv/bin/pytest tests/e2e/test_e2e_full_stack.py::TestTriageAgent::test_basic_greeting -v

# Run with detailed output
.venv/bin/pytest tests/e2e/ -vv --tb=long

# Run without coverage check
.venv/bin/pytest tests/e2e/ -v --no-cov
```

### Skip Specific Tests
```bash
# Skip multi-turn test (if rate limiting is an issue)
.venv/bin/pytest tests/e2e/ -k "not multi_turn" -v
```

## Configuration

### Rate Limiting
The tests may trigger rate limiting (10 requests/minute by default). To avoid this:

1. **Increase rate limit in `.env`:**
   ```bash
   RATE_LIMIT_PER_MINUTE=100
   ```

2. **Add delays between tests:**
   ```python
   import time
   time.sleep(6)  # Wait for rate limit to reset
   ```

3. **Run tests separately:**
   ```bash
   pytest tests/e2e/test_e2e_full_stack.py::TestTriageAgent -v
   sleep 60
   pytest tests/e2e/test_e2e_full_stack.py::TestCostEstimation -v
   ```

### Environment Variables
Tests use the following configuration:
- `BACKEND_URL`: http://127.0.0.1:8000
- `FRONTEND_URL`: http://localhost:3000
- `TIMEOUT`: 30 seconds

## Test Structure

```
tests/e2e/
├── __init__.py              # Package initialization
├── conftest.py              # Pytest configuration
├── test_e2e_full_stack.py   # Main E2E test suite
└── README.md                # This file
```

## Helper Functions

### `send_chat_message(message, conversation_id=None)`
Sends a chat message to the backend API.

**Parameters:**
- `message` (str): The message to send
- `conversation_id` (str, optional): Existing conversation ID

**Returns:**
- `dict`: Response JSON containing conversation_id, current_agent, messages, context

### `send_chat_via_frontend(message, conversation_id=None)`
Sends a chat message via the frontend proxy.

**Parameters:**
- Same as `send_chat_message`

**Returns:**
- Same as `send_chat_message`

### `check_health(url)`
Checks if a service is healthy.

**Parameters:**
- `url` (str): Service URL

**Returns:**
- `bool`: True if healthy, False otherwise

## Fixtures

### `verify_services` (session-scoped, autouse)
Automatically verifies that both backend and frontend are running before any tests execute.

### `test_start_time`
Tracks and reports test execution time.

## Expected Results

### Success Criteria
- All tests pass (or 8/9 if rate limiting occurs)
- Response times < 10 seconds
- All agent handoffs working
- Context properly updated
- Guardrails blocking invalid inputs

### Known Issues
- **Test 8 (Multi-turn Conversation)** may fail with 429 error due to rate limiting
  - This is expected behavior, not a bug
  - Rate limiting is working correctly
  - Solution: Increase rate limit or add delays

## Troubleshooting

### Backend Not Running
```bash
# Check backend status
curl http://localhost:8000/health

# Start backend
cd python-backend
.venv/bin/uvicorn api:app --host 127.0.0.1 --port 8000 --reload
```

### Frontend Not Running
```bash
# Check frontend status
curl http://localhost:3000

# Start frontend
cd ui
npm run dev:next
```

### Rate Limiting Errors (429)
```bash
# Option 1: Increase rate limit in .env
echo "RATE_LIMIT_PER_MINUTE=100" >> python-backend/.env

# Option 2: Wait between test runs
sleep 60

# Option 3: Run tests individually
pytest tests/e2e/ -k "test_basic_greeting" -v
```

### Timeout Errors
```bash
# Increase timeout in test file
TIMEOUT = 60  # Change from 30 to 60 seconds
```

## Reports

After running tests, the following reports are generated:

- `e2e_test_log.txt` - Full test output
- `e2e_test_report.md` - Summary report
- `E2E_TEST_REPORT_DETAILED.md` - Detailed analysis

## Performance Benchmarks

| Test | Expected Duration | Status |
|------|-------------------|--------|
| Basic Greeting | < 3s | Excellent |
| Cost Estimation | < 10s | Acceptable |
| Project Status | < 5s | Good |
| Appointment Booking | < 5s | Good |
| Relevance Guardrail | < 3s | Excellent |
| Jailbreak Guardrail | < 3s | Excellent |
| Frontend Proxy | < 3s | Excellent |
| Performance Test | < 3s | Excellent |
| Multi-turn | < 5s | Good |

## Contributing

When adding new E2E tests:

1. Follow the existing test structure
2. Use descriptive test names
3. Add proper assertions
4. Document expected behavior
5. Update this README

## Example Test

```python
def test_new_feature(self, test_start_time):
    """Test new feature description."""
    print("\n" + "="*80)
    print("TEST: NEW FEATURE")
    print("="*80)
    
    # Send message
    message = "Test message"
    print(f"\n📤 Sending: '{message}'")
    
    response = send_chat_message(message)
    
    # Verify response
    assert "conversation_id" in response
    assert response["current_agent"] == "Expected Agent"
    
    print(f"✓ Test passed")
    print("\n✅ TEST PASSED")
```

## CI/CD Integration

To integrate with CI/CD:

```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Start services
        run: |
          docker-compose up -d
      - name: Run E2E tests
        run: |
          ./run_e2e_tests.sh
      - name: Upload reports
        uses: actions/upload-artifact@v2
        with:
          name: e2e-reports
          path: |
            e2e_test_log.txt
            E2E_TEST_REPORT_DETAILED.md
```

---

**Last Updated:** 2025-10-04  
**Version:** 1.0.0

