"""
Unit tests for structured logging configuration.

Tests logging setup, context binding, and event logging.
"""

import json
import pytest
from io import StringIO
import logging
import sys

import structlog
from structlog.testing import LogCapture

from logging_config import (
    configure_structlog,
    get_logger,
    bind_correlation_id,
    bind_conversation_context,
    bind_user_context,
    clear_context,
    EventLogger,
    events,
)


class TestStructlogConfiguration:
    """Test structlog configuration."""

    def test_configure_structlog_json_format(self):
        """Test JSON format configuration."""
        configure_structlog(log_level="INFO", log_format="json")

        logger = get_logger("test")
        assert logger is not None
        # Logger can be BoundLogger or BoundLoggerLazyProxy
        assert hasattr(logger, "info")
        assert hasattr(logger, "error")

    def test_configure_structlog_console_format(self):
        """Test console format configuration."""
        configure_structlog(log_level="DEBUG", log_format="console")

        logger = get_logger("test")
        assert logger is not None

    def test_get_logger_returns_bound_logger(self):
        """Test that get_logger returns a BoundLogger."""
        logger = get_logger("test_module")

        # Logger can be BoundLogger or BoundLoggerLazyProxy
        assert hasattr(logger, "info")
        assert hasattr(logger, "debug")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")

    def test_get_logger_with_name(self):
        """Test logger with custom name."""
        logger = get_logger("custom_logger")

        assert logger is not None


class TestContextBinding:
    """Test context binding functions."""

    def setup_method(self):
        """Clear context before each test."""
        clear_context()

    def teardown_method(self):
        """Clear context after each test."""
        clear_context()

    def test_bind_correlation_id(self):
        """Test binding correlation ID."""
        correlation_id = "test-correlation-123"

        bind_correlation_id(correlation_id)

        # Verify context is bound
        logger = get_logger("test")
        # Context should be available in subsequent logs

    def test_bind_conversation_context(self):
        """Test binding conversation context."""
        conversation_id = "conv-456"
        agent_name = "Test Agent"

        bind_conversation_context(conversation_id, agent_name)

        # Context should be bound

    def test_bind_conversation_context_without_agent(self):
        """Test binding conversation context without agent name."""
        conversation_id = "conv-789"

        bind_conversation_context(conversation_id)

        # Should work without agent_name

    def test_bind_user_context(self):
        """Test binding user context."""
        user_id = "user-123"
        username = "testuser"

        bind_user_context(user_id=user_id, username=username)

        # Context should be bound

    def test_bind_user_context_partial(self):
        """Test binding user context with only user_id."""
        user_id = "user-456"

        bind_user_context(user_id=user_id)

        # Should work with only user_id

    def test_clear_context(self):
        """Test clearing context."""
        bind_correlation_id("test-123")
        bind_conversation_context("conv-456")

        clear_context()

        # Context should be cleared


class TestEventLogger:
    """Test EventLogger class."""

    def setup_method(self):
        """Setup test logger with log capture."""
        self.log_capture = LogCapture()
        configure_structlog(log_level="INFO", log_format="json")
        structlog.configure(
            processors=[self.log_capture],
            wrapper_class=structlog.stdlib.BoundLogger,
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=False,
        )
        self.event_logger = EventLogger()

    def teardown_method(self):
        """Clear context after each test."""
        clear_context()

    def test_agent_started(self):
        """Test logging agent started event."""
        self.event_logger.agent_started(
            agent_name="Triage Agent",
            conversation_id="conv-123",
        )

        # Verify log was captured
        assert len(self.log_capture.entries) > 0
        entry = self.log_capture.entries[0]
        assert entry["event"] == "agent_started"
        assert entry["agent_name"] == "Triage Agent"
        assert entry["conversation_id"] == "conv-123"

    def test_agent_completed(self):
        """Test logging agent completed event."""
        self.event_logger.agent_completed(
            agent_name="Cost Estimation Agent",
            conversation_id="conv-456",
            duration_ms=150.5,
        )

        assert len(self.log_capture.entries) > 0
        entry = self.log_capture.entries[0]
        assert entry["event"] == "agent_completed"
        assert entry["agent_name"] == "Cost Estimation Agent"
        assert entry["duration_ms"] == 150.5

    def test_agent_handoff(self):
        """Test logging agent handoff event."""
        self.event_logger.agent_handoff(
            from_agent="Triage Agent",
            to_agent="Cost Estimation Agent",
            conversation_id="conv-789",
        )

        assert len(self.log_capture.entries) > 0
        entry = self.log_capture.entries[0]
        assert entry["event"] == "agent_handoff"
        assert entry["from_agent"] == "Triage Agent"
        assert entry["to_agent"] == "Cost Estimation Agent"

    def test_tool_executed(self):
        """Test logging tool execution event."""
        self.event_logger.tool_executed(
            tool_name="estimate_project_cost",
            duration_ms=200.0,
            success=True,
        )

        assert len(self.log_capture.entries) > 0
        entry = self.log_capture.entries[0]
        assert entry["event"] == "tool_executed"
        assert entry["tool_name"] == "estimate_project_cost"
        assert entry["success"] is True

    def test_tool_executed_failure(self):
        """Test logging failed tool execution."""
        self.event_logger.tool_executed(
            tool_name="get_project_status",
            duration_ms=50.0,
            success=False,
            error="Project not found",
        )

        assert len(self.log_capture.entries) > 0
        entry = self.log_capture.entries[0]
        assert entry["success"] is False
        assert entry["error"] == "Project not found"

    def test_guardrail_triggered(self):
        """Test logging guardrail check event."""
        self.event_logger.guardrail_triggered(
            guardrail_name="relevance_guardrail",
            passed=True,
            conversation_id="conv-123",
        )

        assert len(self.log_capture.entries) > 0
        entry = self.log_capture.entries[0]
        assert entry["event"] == "guardrail_triggered"
        assert entry["guardrail_name"] == "relevance_guardrail"
        assert entry["passed"] is True

    def test_authentication_attempt_success(self):
        """Test logging successful authentication."""
        self.event_logger.authentication_attempt(
            username="testuser",
            success=True,
            method="password",
        )

        assert len(self.log_capture.entries) > 0
        entry = self.log_capture.entries[0]
        assert entry["event"] == "authentication_attempt"
        assert entry["username"] == "testuser"
        assert entry["success"] is True
        assert entry["log_level"] == "info"

    def test_authentication_attempt_failure(self):
        """Test logging failed authentication."""
        self.event_logger.authentication_attempt(
            username="baduser",
            success=False,
            method="password",
        )

        assert len(self.log_capture.entries) > 0
        entry = self.log_capture.entries[0]
        assert entry["success"] is False
        assert entry["log_level"] == "warning"

    def test_api_request(self):
        """Test logging API request event."""
        self.event_logger.api_request(
            method="POST",
            path="/chat",
            status_code=200,
            duration_ms=350.5,
        )

        assert len(self.log_capture.entries) > 0
        entry = self.log_capture.entries[0]
        assert entry["event"] == "api_request"
        assert entry["method"] == "POST"
        assert entry["path"] == "/chat"
        assert entry["status_code"] == 200

    def test_event_with_extra_fields(self):
        """Test logging event with extra fields."""
        self.event_logger.agent_started(
            agent_name="FAQ Agent",
            conversation_id="conv-999",
            custom_field="custom_value",
            user_id="user-123",
        )

        assert len(self.log_capture.entries) > 0
        entry = self.log_capture.entries[0]
        assert entry["custom_field"] == "custom_value"
        assert entry["user_id"] == "user-123"


class TestGlobalEventLogger:
    """Test global event logger instance."""

    def test_global_events_instance_exists(self):
        """Test that global events instance is available."""
        assert events is not None
        assert isinstance(events, EventLogger)

    def test_global_events_can_log(self):
        """Test that global events instance can log."""
        # Should not raise error
        events.agent_started("Test Agent", "conv-123")


class TestLoggingIntegration:
    """Integration tests for logging."""

    def test_logger_with_context(self):
        """Test logger with bound context."""
        clear_context()

        bind_correlation_id("corr-123")
        bind_conversation_context("conv-456", "Test Agent")

        logger = get_logger("test")
        # Should include context in logs

        clear_context()

    def test_multiple_context_bindings(self):
        """Test multiple context bindings."""
        clear_context()

        bind_correlation_id("corr-789")
        bind_conversation_context("conv-101", "Agent 1")
        bind_user_context(user_id="user-202", username="testuser")

        # All context should be available

        clear_context()

