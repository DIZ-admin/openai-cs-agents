"""
Unit tests for Prometheus metrics.

Tests metric recording and instrumentator setup.
"""

import pytest
from prometheus_client import REGISTRY

from metrics import (
    record_agent_execution,
    record_agent_handoff,
    record_tool_execution,
    record_guardrail_check,
    record_guardrail_cache_hit,
    record_guardrail_cache_miss,
    record_authentication_attempt,
    update_active_sessions,
    record_conversation_started,
    record_message_processed,
    set_app_info,
    get_guardrail_cache_hit_rate,
    create_instrumentator,
    agent_executions_total,
    agent_handoffs_total,
    tool_executions_total,
    guardrail_checks_total,
    authentication_attempts_total,
    active_sessions_gauge,
    conversations_total,
    messages_total,
)


class TestAgentMetrics:
    """Test agent execution metrics."""

    def test_record_agent_execution_success(self):
        """Test recording successful agent execution."""
        initial_value = agent_executions_total.labels(
            agent_name="Test Agent",
            status="success"
        )._value.get()

        record_agent_execution(
            agent_name="Test Agent",
            duration_seconds=1.5,
            status="success",
        )

        final_value = agent_executions_total.labels(
            agent_name="Test Agent",
            status="success"
        )._value.get()

        assert final_value == initial_value + 1

    def test_record_agent_execution_error(self):
        """Test recording failed agent execution."""
        initial_value = agent_executions_total.labels(
            agent_name="Test Agent",
            status="error"
        )._value.get()

        record_agent_execution(
            agent_name="Test Agent",
            duration_seconds=0.5,
            status="error",
        )

        final_value = agent_executions_total.labels(
            agent_name="Test Agent",
            status="error"
        )._value.get()

        assert final_value == initial_value + 1

    def test_record_agent_handoff(self):
        """Test recording agent handoff."""
        initial_value = agent_handoffs_total.labels(
            from_agent="Triage Agent",
            to_agent="Cost Estimation Agent"
        )._value.get()

        record_agent_handoff(
            from_agent="Triage Agent",
            to_agent="Cost Estimation Agent",
        )

        final_value = agent_handoffs_total.labels(
            from_agent="Triage Agent",
            to_agent="Cost Estimation Agent"
        )._value.get()

        assert final_value == initial_value + 1


class TestToolMetrics:
    """Test tool execution metrics."""

    def test_record_tool_execution_success(self):
        """Test recording successful tool execution."""
        initial_value = tool_executions_total.labels(
            tool_name="estimate_project_cost",
            status="success"
        )._value.get()

        record_tool_execution(
            tool_name="estimate_project_cost",
            duration_seconds=0.2,
            status="success",
        )

        final_value = tool_executions_total.labels(
            tool_name="estimate_project_cost",
            status="success"
        )._value.get()

        assert final_value == initial_value + 1

    def test_record_tool_execution_error(self):
        """Test recording failed tool execution."""
        initial_value = tool_executions_total.labels(
            tool_name="get_project_status",
            status="error"
        )._value.get()

        record_tool_execution(
            tool_name="get_project_status",
            duration_seconds=0.1,
            status="error",
        )

        final_value = tool_executions_total.labels(
            tool_name="get_project_status",
            status="error"
        )._value.get()

        assert final_value == initial_value + 1


class TestGuardrailMetrics:
    """Test guardrail metrics."""

    def test_record_guardrail_check_passed(self):
        """Test recording passed guardrail check."""
        initial_value = guardrail_checks_total.labels(
            guardrail_name="relevance_guardrail",
            result="passed"
        )._value.get()

        record_guardrail_check("relevance_guardrail", passed=True)

        final_value = guardrail_checks_total.labels(
            guardrail_name="relevance_guardrail",
            result="passed"
        )._value.get()

        assert final_value == initial_value + 1

    def test_record_guardrail_check_failed(self):
        """Test recording failed guardrail check."""
        initial_value = guardrail_checks_total.labels(
            guardrail_name="jailbreak_guardrail",
            result="failed"
        )._value.get()

        record_guardrail_check("jailbreak_guardrail", passed=False)

        final_value = guardrail_checks_total.labels(
            guardrail_name="jailbreak_guardrail",
            result="failed"
        )._value.get()

        assert final_value == initial_value + 1

    def test_record_guardrail_cache_hit(self):
        """Test recording guardrail cache hit."""
        record_guardrail_cache_hit("test_guardrail")
        # Should not raise error

    def test_record_guardrail_cache_miss(self):
        """Test recording guardrail cache miss."""
        record_guardrail_cache_miss("test_guardrail")
        # Should not raise error

    def test_get_guardrail_cache_hit_rate(self):
        """Test calculating cache hit rate."""
        # This test is basic since we can't easily reset metrics
        rate = get_guardrail_cache_hit_rate("test_guardrail_rate")
        assert 0.0 <= rate <= 1.0


class TestAuthenticationMetrics:
    """Test authentication metrics."""

    def test_record_authentication_attempt_success(self):
        """Test recording successful authentication."""
        initial_value = authentication_attempts_total.labels(
            method="password",
            result="success"
        )._value.get()

        record_authentication_attempt(method="password", success=True)

        final_value = authentication_attempts_total.labels(
            method="password",
            result="success"
        )._value.get()

        assert final_value == initial_value + 1

    def test_record_authentication_attempt_failure(self):
        """Test recording failed authentication."""
        initial_value = authentication_attempts_total.labels(
            method="password",
            result="failure"
        )._value.get()

        record_authentication_attempt(method="password", success=False)

        final_value = authentication_attempts_total.labels(
            method="password",
            result="failure"
        )._value.get()

        assert final_value == initial_value + 1


class TestConversationMetrics:
    """Test conversation metrics."""

    def test_update_active_sessions(self):
        """Test updating active sessions gauge."""
        update_active_sessions(5)

        value = active_sessions_gauge._value.get()
        assert value == 5

        update_active_sessions(10)

        value = active_sessions_gauge._value.get()
        assert value == 10

    def test_record_conversation_started(self):
        """Test recording conversation started."""
        initial_value = conversations_total._value.get()

        record_conversation_started()

        final_value = conversations_total._value.get()
        assert final_value == initial_value + 1

    def test_record_message_processed(self):
        """Test recording message processed."""
        initial_value = messages_total.labels(
            agent_name="Triage Agent"
        )._value.get()

        record_message_processed("Triage Agent")

        final_value = messages_total.labels(
            agent_name="Triage Agent"
        )._value.get()

        assert final_value == initial_value + 1


class TestAppInfo:
    """Test application info metric."""

    def test_set_app_info(self):
        """Test setting application info."""
        set_app_info(version="1.0.0", environment="test")
        # Should not raise error


class TestInstrumentator:
    """Test Prometheus instrumentator."""

    def test_create_instrumentator(self):
        """Test creating instrumentator."""
        instrumentator = create_instrumentator()

        assert instrumentator is not None
        assert instrumentator.should_group_status_codes is True
        assert instrumentator.should_ignore_untemplated is True

