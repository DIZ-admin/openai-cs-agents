"""
Prometheus Metrics for ERNI Gruppe Building Agents.

This module provides comprehensive metrics for monitoring and observability:
- HTTP request metrics (requests, latency, errors)
- Agent execution metrics (count, duration, handoffs)
- Tool execution metrics
- Guardrail metrics
- Authentication metrics
"""

from prometheus_client import Counter, Histogram, Gauge, Info
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info as MetricInfo


# =========================
# Custom Metrics
# =========================

# Agent Execution Metrics
agent_executions_total = Counter(
    "agent_executions_total",
    "Total number of agent executions",
    ["agent_name", "status"],  # status: success, error, timeout
)

agent_execution_duration_seconds = Histogram(
    "agent_execution_duration_seconds",
    "Agent execution duration in seconds",
    ["agent_name"],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0),
)

agent_handoffs_total = Counter(
    "agent_handoffs_total",
    "Total number of agent handoffs",
    ["from_agent", "to_agent"],
)

# Tool Execution Metrics
tool_executions_total = Counter(
    "tool_executions_total",
    "Total number of tool executions",
    ["tool_name", "status"],  # status: success, error
)

tool_execution_duration_seconds = Histogram(
    "tool_execution_duration_seconds",
    "Tool execution duration in seconds",
    ["tool_name"],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0),
)

# Guardrail Metrics
guardrail_checks_total = Counter(
    "guardrail_checks_total",
    "Total number of guardrail checks",
    ["guardrail_name", "result"],  # result: passed, failed
)

guardrail_cache_hits_total = Counter(
    "guardrail_cache_hits_total",
    "Total number of guardrail cache hits",
    ["guardrail_name"],
)

guardrail_cache_misses_total = Counter(
    "guardrail_cache_misses_total",
    "Total number of guardrail cache misses",
    ["guardrail_name"],
)

# Authentication Metrics
authentication_attempts_total = Counter(
    "authentication_attempts_total",
    "Total number of authentication attempts",
    ["method", "result"],  # method: password, token; result: success, failure
)

active_sessions_gauge = Gauge(
    "active_sessions",
    "Number of active conversation sessions",
)

# Conversation Metrics
conversations_total = Counter(
    "conversations_total",
    "Total number of conversations started",
)

messages_total = Counter(
    "messages_total",
    "Total number of messages processed",
    ["agent_name"],
)

# Application Info
app_info = Info(
    "app",
    "Application information",
)


# =========================
# Metric Recording Functions
# =========================


def record_agent_execution(
    agent_name: str,
    duration_seconds: float,
    status: str = "success",
) -> None:
    """
    Record agent execution metrics.

    Args:
        agent_name: Name of the agent
        duration_seconds: Execution duration in seconds
        status: Execution status (success, error, timeout)
    """
    agent_executions_total.labels(agent_name=agent_name, status=status).inc()
    agent_execution_duration_seconds.labels(agent_name=agent_name).observe(duration_seconds)


def record_agent_handoff(from_agent: str, to_agent: str) -> None:
    """
    Record agent handoff.

    Args:
        from_agent: Source agent name
        to_agent: Target agent name
    """
    agent_handoffs_total.labels(from_agent=from_agent, to_agent=to_agent).inc()


def record_tool_execution(
    tool_name: str,
    duration_seconds: float,
    status: str = "success",
) -> None:
    """
    Record tool execution metrics.

    Args:
        tool_name: Name of the tool
        duration_seconds: Execution duration in seconds
        status: Execution status (success, error)
    """
    tool_executions_total.labels(tool_name=tool_name, status=status).inc()
    tool_execution_duration_seconds.labels(tool_name=tool_name).observe(duration_seconds)


def record_guardrail_check(guardrail_name: str, passed: bool) -> None:
    """
    Record guardrail check result.

    Args:
        guardrail_name: Name of the guardrail
        passed: Whether the check passed
    """
    result = "passed" if passed else "failed"
    guardrail_checks_total.labels(guardrail_name=guardrail_name, result=result).inc()


def record_guardrail_cache_hit(guardrail_name: str) -> None:
    """
    Record guardrail cache hit.

    Args:
        guardrail_name: Name of the guardrail
    """
    guardrail_cache_hits_total.labels(guardrail_name=guardrail_name).inc()


def record_guardrail_cache_miss(guardrail_name: str) -> None:
    """
    Record guardrail cache miss.

    Args:
        guardrail_name: Name of the guardrail
    """
    guardrail_cache_misses_total.labels(guardrail_name=guardrail_name).inc()


def record_authentication_attempt(method: str, success: bool) -> None:
    """
    Record authentication attempt.

    Args:
        method: Authentication method (password, token)
        success: Whether authentication succeeded
    """
    result = "success" if success else "failure"
    authentication_attempts_total.labels(method=method, result=result).inc()


def update_active_sessions(count: int) -> None:
    """
    Update active sessions gauge.

    Args:
        count: Current number of active sessions
    """
    active_sessions_gauge.set(count)


def record_conversation_started() -> None:
    """Record a new conversation started."""
    conversations_total.inc()


def record_message_processed(agent_name: str) -> None:
    """
    Record a message processed by an agent.

    Args:
        agent_name: Name of the agent that processed the message
    """
    messages_total.labels(agent_name=agent_name).inc()


def set_app_info(version: str, environment: str) -> None:
    """
    Set application information.

    Args:
        version: Application version
        environment: Deployment environment
    """
    app_info.info({"version": version, "environment": environment})


# =========================
# Instrumentator Setup
# =========================


def create_instrumentator() -> Instrumentator:
    """
    Create and configure Prometheus instrumentator for FastAPI.

    Returns:
        Configured Instrumentator instance
    """
    instrumentator = Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        should_respect_env_var=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers=["/metrics", "/health"],
        env_var_name="ENABLE_METRICS",
        inprogress_name="http_requests_inprogress",
        inprogress_labels=True,
    )

    # Add default metrics
    instrumentator.add(
        metrics.request_size(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
            metric_namespace="http",
            metric_subsystem="",
        )
    )

    instrumentator.add(
        metrics.response_size(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
            metric_namespace="http",
            metric_subsystem="",
        )
    )

    instrumentator.add(
        metrics.latency(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
            metric_namespace="http",
            metric_subsystem="",
            buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0),
        )
    )

    instrumentator.add(
        metrics.requests(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
            metric_namespace="http",
            metric_subsystem="",
        )
    )

    return instrumentator


# =========================
# Helper Functions
# =========================


def get_guardrail_cache_hit_rate(guardrail_name: str) -> float:
    """
    Calculate cache hit rate for a guardrail.

    Args:
        guardrail_name: Name of the guardrail

    Returns:
        Cache hit rate (0.0 to 1.0)
    """
    try:
        hits = guardrail_cache_hits_total.labels(guardrail_name=guardrail_name)._value.get()
        misses = guardrail_cache_misses_total.labels(guardrail_name=guardrail_name)._value.get()
        total = hits + misses
        if total == 0:
            return 0.0
        return hits / total
    except Exception:
        return 0.0

