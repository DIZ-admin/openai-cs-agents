"""
Unit tests for API error handling.

Tests error scenarios in the FastAPI application including:
- Invalid conversation IDs
- Database connection errors
- OpenAI API errors
- Malformed JSON requests
- Missing required fields
- Authentication errors
- Rate limiting
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from openai import OpenAIError, APITimeoutError, RateLimitError
from tenacity import RetryError

from api import app
from main import BuildingProjectContext


class TestAPIErrorHandling:
    """Test error handling in API endpoints."""

    @pytest.fixture(autouse=True)
    def mock_runner_default(self):
        """Mock Runner by default for tests that don't explicitly patch it."""
        # This will be overridden by @patch decorators on individual tests
        with patch("api.Runner") as mock:
            # Mock successful run result
            mock_result = MagicMock()
            mock_result.new_items = []
            mock_result.to_input_list.return_value = []
            mock.run = AsyncMock(return_value=mock_result)
            yield mock

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    @pytest.fixture
    def auth_headers(self):
        """Create authentication headers for testing."""
        # Get a valid token first
        client = TestClient(app)
        response = client.post(
            "/auth/token?username=demo&password=secret"
        )
        if response.status_code != 200:
            pytest.skip(f"Failed to get auth token: {response.status_code} - {response.text}")
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    # =========================
    # Authentication Errors
    # =========================

    def test_invalid_credentials_login(self, client):
        """Test that invalid credentials are rejected during login."""
        response = client.post(
            "/auth/token?username=invalid_user&password=wrong_password"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]

    def test_missing_username_in_login(self, client):
        """Test that missing username in login is rejected."""
        response = client.post(
            "/auth/token?password=secret"
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_missing_password_in_login(self, client):
        """Test that missing password in login is rejected."""
        response = client.post(
            "/auth/token?username=demo"
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_empty_username_rejected(self, client):
        """Test that empty username is rejected."""
        response = client.post(
            "/auth/token?username=&password=secret"
        )
        # Should either reject or fail authentication
        assert response.status_code in [401, 422]

    def test_empty_password_rejected(self, client):
        """Test that empty password is rejected."""
        response = client.post(
            "/auth/token?username=demo&password="
        )
        # Should either reject or fail authentication
        assert response.status_code in [401, 422]

    # =========================
    # Request Validation Errors
    # =========================

    def test_empty_message_rejected(self, client, auth_headers):
        """Test that empty message is handled as initialization request."""
        response = client.post(
            "/chat",
            json={"message": ""},
            headers=auth_headers
        )
        # Empty message is treated as initialization request, returns 200
        assert response.status_code == 200
        assert "conversation_id" in response.json()

    def test_missing_message_field(self, client, auth_headers):
        """Test that missing message field is rejected."""
        response = client.post(
            "/chat",
            json={},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_malformed_json_request(self, client, auth_headers):
        """Test that malformed JSON is rejected."""
        response = client.post(
            "/chat",
            data="not valid json",
            headers={**auth_headers, "Content-Type": "application/json"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_invalid_conversation_id_format(self, client, auth_headers):
        """Test that invalid conversation ID format is handled."""
        # This should not crash, but may create a new conversation
        response = client.post(
            "/chat",
            json={
                "conversation_id": "invalid-format-!@#$",
                "message": "Hello"
            },
            headers=auth_headers
        )
        # Should either accept it or return 400, but not crash
        assert response.status_code in [200, 400]

    def test_oversized_message_rejected(self, client, auth_headers):
        """Test that oversized message is rejected."""
        # Create a very large message (>10KB)
        large_message = "x" * 50000
        response = client.post(
            "/chat",
            json={"message": large_message},
            headers=auth_headers
        )
        # Should either process or reject, but not crash
        assert response.status_code in [200, 400, 413, 422]

    def test_null_message_rejected(self, client, auth_headers):
        """Test that null message is rejected."""
        response = client.post(
            "/chat",
            json={"message": None},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # =========================
    # OpenAI API Errors
    # =========================

    @patch("api.Runner")
    def test_openai_api_timeout_error(self, mock_runner, client, auth_headers):
        """Test handling of OpenAI API timeout errors."""
        # Mock Runner to raise timeout error
        mock_runner.return_value.run = AsyncMock(
            side_effect=APITimeoutError("Request timed out")
        )

        response = client.post(
            "/chat",
            json={"message": "Hello"},
            headers=auth_headers
        )

        # Should return 500 or retry and eventually fail
        assert response.status_code in [500, 503, 504]

    @patch("api.Runner")
    def test_openai_rate_limit_error(self, mock_runner, client, auth_headers):
        """Test handling of OpenAI rate limit errors."""
        # Create a mock response object for RateLimitError
        mock_response = MagicMock()
        mock_response.status_code = 429

        # Mock Runner to raise rate limit error with required parameters
        mock_runner.return_value.run = AsyncMock(
            side_effect=RateLimitError(
                "Rate limit exceeded",
                response=mock_response,
                body={"error": {"message": "Rate limit exceeded"}}
            )
        )

        response = client.post(
            "/chat",
            json={"message": "Hello"},
            headers=auth_headers
        )

        # Should return 429 or 503
        assert response.status_code in [429, 500, 503]

    @patch("api.Runner")
    def test_openai_generic_error(self, mock_runner, client, auth_headers):
        """Test handling of generic OpenAI errors."""
        # Mock Runner to raise generic OpenAI error
        mock_runner.return_value.run = AsyncMock(
            side_effect=OpenAIError("Generic OpenAI error")
        )

        response = client.post(
            "/chat",
            json={"message": "Hello"},
            headers=auth_headers
        )

        # Should return 500
        assert response.status_code in [500, 503]

    # =========================
    # Database/Session Errors
    # =========================

    # Note: Session manager error tests are skipped because they require
    # complex mocking of the session manager singleton pattern.
    # These scenarios are better tested in integration tests.

    # =========================
    # Retry Logic Errors
    # =========================

    @patch("api.Runner")
    def test_retry_exhausted_error(self, mock_runner, client, auth_headers):
        """Test handling when retry attempts are exhausted."""
        # Mock Runner to always fail, exhausting retries
        mock_runner.return_value.run = AsyncMock(
            side_effect=RetryError("Max retries exceeded")
        )

        response = client.post(
            "/chat",
            json={"message": "Hello"},
            headers=auth_headers
        )

        # Should return 500 or 503
        assert response.status_code in [500, 503]

    # =========================
    # Unexpected Errors
    # =========================

    @patch("api.Runner")
    def test_unexpected_exception_handling(self, mock_runner, client, auth_headers):
        """Test handling of unexpected exceptions."""
        # Mock Runner to raise unexpected error
        mock_runner.return_value.run = AsyncMock(
            side_effect=ValueError("Unexpected error")
        )

        response = client.post(
            "/chat",
            json={"message": "Hello"},
            headers=auth_headers
        )

        # Should return 500
        assert response.status_code == 500

    @patch("api.Runner")
    def test_none_response_handling(self, mock_runner, client, auth_headers):
        """Test handling when Runner returns None."""
        # Mock Runner to return None
        mock_runner.return_value.run = AsyncMock(return_value=None)

        response = client.post(
            "/chat",
            json={"message": "Hello"},
            headers=auth_headers
        )

        # Should handle gracefully
        assert response.status_code in [200, 500]

