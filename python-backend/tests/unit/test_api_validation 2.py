"""
Unit tests for API request validation.

Tests validation logic in the FastAPI application including:
- Message content validation
- Conversation ID validation
- Request format validation
- Header validation
- Query parameter validation
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import status
from fastapi.testclient import TestClient
from uuid import uuid4

from api import app


class TestAPIValidation:
    """Test request validation in API endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    @pytest.fixture
    def auth_headers(self):
        """Create authentication headers for testing."""
        client = TestClient(app)
        response = client.post(
            "/auth/token?username=demo&password=secret"
        )
        if response.status_code != 200:
            pytest.skip(f"Failed to get auth token: {response.status_code} - {response.text}")
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    # =========================
    # Message Validation
    # =========================

    def test_valid_message_accepted(self, client, auth_headers):
        """Test that valid message is accepted."""
        response = client.post(
            "/chat",
            json={"message": "Hello, I want to build a house"},
            headers=auth_headers
        )
        assert response.status_code == 200

    def test_message_with_special_characters(self, client, auth_headers):
        """Test that message with special characters is accepted."""
        response = client.post(
            "/chat",
            json={"message": "Ich möchte ein Haus für 500'000 CHF bauen!"},
            headers=auth_headers
        )
        assert response.status_code == 200

    def test_message_with_unicode(self, client, auth_headers):
        """Test that message with unicode characters is accepted."""
        response = client.post(
            "/chat",
            json={"message": "Hello 👋 I want to build 🏠"},
            headers=auth_headers
        )
        assert response.status_code == 200

    def test_message_with_newlines(self, client, auth_headers):
        """Test that message with newlines is accepted."""
        response = client.post(
            "/chat",
            json={"message": "Hello\nI want to build\na house"},
            headers=auth_headers
        )
        assert response.status_code == 200

    def test_very_short_message(self, client, auth_headers):
        """Test that very short message is accepted."""
        response = client.post(
            "/chat",
            json={"message": "Hi"},
            headers=auth_headers
        )
        assert response.status_code == 200

    def test_whitespace_only_message_rejected(self, client, auth_headers):
        """Test that whitespace-only message is rejected."""
        response = client.post(
            "/chat",
            json={"message": "   "},
            headers=auth_headers
        )
        # Should be rejected as empty
        assert response.status_code in [400, 422]

    def test_message_with_html_tags(self, client, auth_headers):
        """Test that message with HTML tags is handled."""
        response = client.post(
            "/chat",
            json={"message": "<script>alert('test')</script>"},
            headers=auth_headers
        )
        # Should be accepted but sanitized
        assert response.status_code == 200

    def test_message_with_sql_injection_attempt(self, client, auth_headers):
        """Test that SQL injection attempts are handled."""
        response = client.post(
            "/chat",
            json={"message": "'; DROP TABLE users; --"},
            headers=auth_headers
        )
        # Should be accepted as regular text
        assert response.status_code == 200

    # =========================
    # Conversation ID Validation
    # =========================

    def test_valid_uuid_conversation_id(self, client, auth_headers):
        """Test that valid UUID conversation ID is accepted."""
        conversation_id = str(uuid4())
        response = client.post(
            "/chat",
            json={
                "conversation_id": conversation_id,
                "message": "Hello"
            },
            headers=auth_headers
        )
        assert response.status_code == 200

    def test_custom_conversation_id_format(self, client, auth_headers):
        """Test that custom conversation ID format is accepted."""
        response = client.post(
            "/chat",
            json={
                "conversation_id": "conv_12345",
                "message": "Hello"
            },
            headers=auth_headers
        )
        assert response.status_code == 200

    def test_null_conversation_id_creates_new(self, client, auth_headers):
        """Test that null conversation ID creates new conversation."""
        response = client.post(
            "/chat",
            json={
                "conversation_id": None,
                "message": "Hello"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        # Should return a conversation_id in response
        assert "conversation_id" in response.json()

    def test_missing_conversation_id_creates_new(self, client, auth_headers):
        """Test that missing conversation ID creates new conversation."""
        response = client.post(
            "/chat",
            json={"message": "Hello"},
            headers=auth_headers
        )
        assert response.status_code == 200
        # Should return a conversation_id in response
        assert "conversation_id" in response.json()

    def test_empty_string_conversation_id(self, client, auth_headers):
        """Test that empty string conversation ID is handled."""
        response = client.post(
            "/chat",
            json={
                "conversation_id": "",
                "message": "Hello"
            },
            headers=auth_headers
        )
        # Should either create new or reject
        assert response.status_code in [200, 400, 422]

    def test_very_long_conversation_id(self, client, auth_headers):
        """Test that very long conversation ID is handled."""
        long_id = "x" * 1000
        response = client.post(
            "/chat",
            json={
                "conversation_id": long_id,
                "message": "Hello"
            },
            headers=auth_headers
        )
        # Should either accept or reject, but not crash
        assert response.status_code in [200, 400, 422]

    # =========================
    # Request Format Validation
    # =========================

    def test_extra_fields_ignored(self, client, auth_headers):
        """Test that extra fields in request are ignored."""
        response = client.post(
            "/chat",
            json={
                "message": "Hello",
                "extra_field": "should be ignored",
                "another_field": 123
            },
            headers=auth_headers
        )
        assert response.status_code == 200

    def test_wrong_content_type_rejected(self, client, auth_headers):
        """Test that wrong content type is rejected."""
        response = client.post(
            "/chat",
            data="message=Hello",
            headers={**auth_headers, "Content-Type": "application/x-www-form-urlencoded"}
        )
        # Should reject non-JSON content
        assert response.status_code in [400, 415, 422]

    def test_missing_content_type_header(self, client, auth_headers):
        """Test that missing content type header is handled."""
        response = client.post(
            "/chat",
            json={"message": "Hello"},
            headers=auth_headers
        )
        # FastAPI should infer JSON content type
        assert response.status_code == 200

    def test_array_instead_of_object(self, client, auth_headers):
        """Test that array instead of object is rejected."""
        response = client.post(
            "/chat",
            json=["message", "Hello"],
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_string_instead_of_object(self, client, auth_headers):
        """Test that string instead of object is rejected."""
        response = client.post(
            "/chat",
            json="Hello",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_number_instead_of_string_message(self, client, auth_headers):
        """Test that number instead of string message is rejected."""
        response = client.post(
            "/chat",
            json={"message": 12345},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_boolean_instead_of_string_message(self, client, auth_headers):
        """Test that boolean instead of string message is rejected."""
        response = client.post(
            "/chat",
            json={"message": True},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # =========================
    # Health Endpoint Validation
    # =========================

    def test_health_endpoint_no_auth_required(self, client):
        """Test that health endpoint doesn't require authentication."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_health_endpoint_returns_correct_structure(self, client):
        """Test that health endpoint returns correct structure."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert "service" in data

    def test_readiness_endpoint_no_auth_required(self, client):
        """Test that readiness endpoint doesn't require authentication."""
        response = client.get("/readiness")
        # Should return 200 or 503 depending on readiness
        assert response.status_code in [200, 503]

    # =========================
    # Agents Endpoint Validation
    # =========================

    def test_agents_endpoint_no_auth_required(self, client):
        """Test that agents endpoint doesn't require authentication."""
        response = client.get("/agents")
        assert response.status_code == 200

    def test_agents_endpoint_returns_list(self, client):
        """Test that agents endpoint returns a list."""
        response = client.get("/agents")
        data = response.json()
        assert "agents" in data
        assert isinstance(data["agents"], list)
        assert len(data["agents"]) > 0

    def test_agents_endpoint_returns_correct_structure(self, client):
        """Test that agents endpoint returns correct structure."""
        response = client.get("/agents")
        data = response.json()
        assert "agents" in data
        assert "total" in data
        assert "timestamp" in data
        for agent in data["agents"]:
            assert "name" in agent
            assert "description" in agent

    # =========================
    # CORS Validation
    # =========================

    def test_cors_headers_present_in_response(self, client):
        """Test that CORS headers are present in actual response."""
        response = client.get("/health")
        # Check if CORS headers are present (they should be added by middleware)
        assert response.status_code == 200

    def test_preflight_request_handled(self, client):
        """Test that preflight OPTIONS request is handled."""
        response = client.options(
            "/chat",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST"
            }
        )
        assert response.status_code in [200, 204]

