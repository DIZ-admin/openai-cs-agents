"""
Structured Logging Configuration for ERNI Gruppe Building Agents.

This module configures structlog for production-ready logging with:
- JSON output for log aggregation systems
- Correlation IDs for request tracing
- Contextual information (agent, conversation_id, user)
- Structured event logging
- Performance metrics
"""

import logging
import os
import sys
from typing import Any, Dict, Optional

import structlog
from structlog.types import EventDict, Processor


# =========================
# Environment Configuration
# =========================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("LOG_FORMAT", "json")  # "json" or "console"
ENABLE_COLORS = os.getenv("ENABLE_LOG_COLORS", "true").lower() == "true"


# =========================
# Custom Processors
# =========================


def add_app_context(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    """
    Add application-level context to all log entries.

    Adds:
    - app_name: Application identifier
    - environment: Deployment environment (dev/staging/production)
    - version: Application version
    """
    event_dict["app_name"] = "erni-building-agents"
    event_dict["environment"] = os.getenv("ENVIRONMENT", "development")
    event_dict["version"] = os.getenv("APP_VERSION", "0.1.0")
    return event_dict


def add_correlation_id(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    """
    Add correlation_id from context if available.

    Correlation IDs enable request tracing across services and agent handoffs.
    """
    # Try to get correlation_id from bound context
    correlation_id = event_dict.get("correlation_id")
    if correlation_id:
        event_dict["correlation_id"] = correlation_id
    return event_dict


def rename_event_key(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    """
    Rename 'event' key to 'message' for better compatibility with log aggregators.
    """
    if "event" in event_dict:
        event_dict["message"] = event_dict.pop("event")
    return event_dict


# =========================
# Logging Configuration
# =========================


def configure_structlog(
    log_level: str = LOG_LEVEL,
    log_format: str = LOG_FORMAT,
    enable_colors: bool = ENABLE_COLORS,
) -> None:
    """
    Configure structlog for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Output format ("json" for production, "console" for development)
        enable_colors: Whether to enable colored output (only for console format)

    Example:
        >>> configure_structlog(log_level="INFO", log_format="json")
    """
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level),
    )

    # Shared processors for all configurations
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        add_app_context,
        add_correlation_id,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
    ]

    # Format-specific processors
    if log_format == "json":
        # Production: JSON output
        processors = shared_processors + [
            rename_event_key,
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ]
    else:
        # Development: Console output with colors
        processors = shared_processors + [
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(colors=enable_colors),
        ]

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


# =========================
# Logger Factory
# =========================


def get_logger(name: Optional[str] = None) -> structlog.stdlib.BoundLogger:
    """
    Get a configured structlog logger.

    Args:
        name: Logger name (usually __name__ of the module)

    Returns:
        Configured structlog logger

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("user_login", user_id="123", method="password")
    """
    return structlog.get_logger(name)


# =========================
# Context Managers
# =========================


def bind_correlation_id(correlation_id: str) -> None:
    """
    Bind a correlation ID to the current context.

    All subsequent log entries will include this correlation_id.

    Args:
        correlation_id: Unique identifier for request tracing

    Example:
        >>> bind_correlation_id("req-abc-123")
        >>> logger.info("processing_request")  # Will include correlation_id
    """
    structlog.contextvars.bind_contextvars(correlation_id=correlation_id)


def bind_conversation_context(conversation_id: str, agent_name: Optional[str] = None) -> None:
    """
    Bind conversation context to current logging context.

    Args:
        conversation_id: Unique conversation identifier
        agent_name: Name of the current agent (optional)

    Example:
        >>> bind_conversation_context("conv-123", "Triage Agent")
        >>> logger.info("agent_started")  # Will include conversation_id and agent_name
    """
    context: Dict[str, Any] = {"conversation_id": conversation_id}
    if agent_name:
        context["agent_name"] = agent_name
    structlog.contextvars.bind_contextvars(**context)


def bind_user_context(user_id: Optional[str] = None, username: Optional[str] = None) -> None:
    """
    Bind user context to current logging context.

    Args:
        user_id: User identifier
        username: Username

    Example:
        >>> bind_user_context(user_id="user-456", username="john@example.com")
        >>> logger.info("user_action")  # Will include user_id and username
    """
    context: Dict[str, Any] = {}
    if user_id:
        context["user_id"] = user_id
    if username:
        context["username"] = username
    if context:
        structlog.contextvars.bind_contextvars(**context)


def clear_context() -> None:
    """
    Clear all bound context variables.

    Useful at the end of request processing to prevent context leakage.

    Example:
        >>> bind_correlation_id("req-123")
        >>> # ... process request ...
        >>> clear_context()  # Clean up for next request
    """
    structlog.contextvars.clear_contextvars()


# =========================
# Structured Event Logging
# =========================


class EventLogger:
    """
    Helper class for logging structured events with consistent format.

    Example:
        >>> events = EventLogger()
        >>> events.agent_started("Triage Agent", conversation_id="conv-123")
        >>> events.agent_handoff("Triage Agent", "Cost Estimation Agent")
        >>> events.tool_executed("estimate_project_cost", duration_ms=150)
    """

    def __init__(self, logger: Optional[structlog.stdlib.BoundLogger] = None):
        """Initialize event logger."""
        self.logger = logger or get_logger("events")

    def agent_started(
        self,
        agent_name: str,
        conversation_id: str,
        **extra: Any,
    ) -> None:
        """Log agent execution start."""
        self.logger.info(
            "agent_started",
            agent_name=agent_name,
            conversation_id=conversation_id,
            **extra,
        )

    def agent_completed(
        self,
        agent_name: str,
        conversation_id: str,
        duration_ms: float,
        **extra: Any,
    ) -> None:
        """Log agent execution completion."""
        self.logger.info(
            "agent_completed",
            agent_name=agent_name,
            conversation_id=conversation_id,
            duration_ms=duration_ms,
            **extra,
        )

    def agent_handoff(
        self,
        from_agent: str,
        to_agent: str,
        conversation_id: str,
        **extra: Any,
    ) -> None:
        """Log agent handoff."""
        self.logger.info(
            "agent_handoff",
            from_agent=from_agent,
            to_agent=to_agent,
            conversation_id=conversation_id,
            **extra,
        )

    def tool_executed(
        self,
        tool_name: str,
        duration_ms: float,
        success: bool = True,
        **extra: Any,
    ) -> None:
        """Log tool execution."""
        self.logger.info(
            "tool_executed",
            tool_name=tool_name,
            duration_ms=duration_ms,
            success=success,
            **extra,
        )

    def guardrail_triggered(
        self,
        guardrail_name: str,
        passed: bool,
        conversation_id: str,
        **extra: Any,
    ) -> None:
        """Log guardrail check."""
        self.logger.info(
            "guardrail_triggered",
            guardrail_name=guardrail_name,
            passed=passed,
            conversation_id=conversation_id,
            **extra,
        )

    def authentication_attempt(
        self,
        username: str,
        success: bool,
        method: str = "password",
        **extra: Any,
    ) -> None:
        """Log authentication attempt."""
        level = "info" if success else "warning"
        getattr(self.logger, level)(
            "authentication_attempt",
            username=username,
            success=success,
            method=method,
            **extra,
        )

    def api_request(
        self,
        method: str,
        path: str,
        status_code: int,
        duration_ms: float,
        **extra: Any,
    ) -> None:
        """Log API request."""
        self.logger.info(
            "api_request",
            method=method,
            path=path,
            status_code=status_code,
            duration_ms=duration_ms,
            **extra,
        )


# =========================
# Initialize on Import
# =========================

# Configure structlog when module is imported
configure_structlog()

# Create global event logger instance
events = EventLogger()

