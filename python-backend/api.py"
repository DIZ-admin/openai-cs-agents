import asyncio
import logging
import os
import time
from datetime import datetime
from typing import Annotated, Any, Dict, List, Optional
from uuid import uuid4
from pathlib import Path

# Import structured logging
from logging_config import (
    get_logger,
    events,
    bind_correlation_id,
    bind_conversation_context,
    bind_user_context,
    clear_context,
)

import httpx
from agents import (
    Agent,
    Handoff,
    HandoffOutputItem,
    InputGuardrailTripwireTriggered,
    ItemHelpers,
    MessageOutputItem,
    Runner,
    RunResult,
    SQLiteSession,
    ToolCallItem,
    ToolCallOutputItem,
)
from dotenv import load_dotenv
from fastapi import Body, Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    RetryError,
)
from openai import OpenAIError, APITimeoutError, RateLimitError

# Import session manager
from session_manager import get_session_manager

# Import metrics
from metrics import (
    create_instrumentator,
    record_agent_execution,
    record_agent_handoff,
    record_tool_execution,
    record_guardrail_check,
    record_authentication_attempt,
    update_active_sessions,
    record_conversation_started,
    record_message_processed,
    set_app_info,
)

from main import (
    appointment_booking_agent,
    BuildingProjectContext,
    cost_estimation_agent,
    create_initial_context,
    faq_agent,
    project_information_agent,
    project_status_agent,
    triage_agent,
)

# Authentication
from auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_active_user,
    get_optional_current_user,
    Token,
    User,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

# Load environment variables
load_dotenv()

# Import security validator (will auto-validate on import in production)
from security_validator import ProductionSecurityValidator

# Get structured logger
logger = get_logger(__name__)

# FastAPI app with comprehensive metadata
app = FastAPI(
    title="ERNI Gruppe Building Agents API",
    description="""
## ERNI Gruppe Building Agents - Multi-Agent Customer Service System

A sophisticated multi-agent orchestration platform built on the OpenAI Agents SDK,
providing intelligent customer service for building and construction projects.

### Features

* **6 Specialized Agents** - Each agent handles specific aspects of building projects
* **Intelligent Routing** - Automatic handoff between agents based on customer needs
* **Context Preservation** - Customer information persists across agent transitions
* **Bilingual Support** - German and English language support
* **Safety Guardrails** - Input validation and security checks
* **PII Protection** - Output guardrails prevent exposure of sensitive information

### Agents

1. **Triage Agent** - Main entry point and routing agent
2. **Project Information Agent** - General information about ERNI's services
3. **Cost Estimation Agent** - Preliminary cost estimates for building projects
4. **Project Status Agent** - Status updates for ongoing projects
5. **Appointment Booking Agent** - Schedule consultations with specialists
6. **FAQ Agent** - Answers frequently asked questions

### Use Cases

* Cost estimation for building projects
* Project status inquiries
* Consultation scheduling with specialists
* General building information and FAQ
* Material and process questions

### Authentication

Currently, the API does not require authentication. In production, implement
proper authentication and authorization mechanisms.

### Rate Limiting

The API implements rate limiting to prevent abuse:
* 60 requests per minute per IP
* 1000 requests per hour per IP
* 10000 requests per day per IP

### Support

For support, contact: info@erni-gruppe.ch
Website: https://www.erni-gruppe.ch
    """,
    version="1.0.0",
    terms_of_service="https://www.erni-gruppe.ch/terms",
    contact={
        "name": "ERNI Gruppe Support",
        "url": "https://www.erni-gruppe.ch/contact",
        "email": "info@erni-gruppe.ch",
    },
    license_info={
        "name": "Proprietary",
        "url": "https://www.erni-gruppe.ch/license",
    },
    openapi_tags=[
        {
            "name": "chat",
            "description": "Chat endpoints for interacting with building agents",
        },
        {
            "name": "health",
            "description": "Health check and system status endpoints",
        },
        {
            "name": "agents",
            "description": "Agent information and configuration endpoints",
        },
    ],
)

# Rate limiting configuration
# Use very high limit if DISABLE_RATE_LIMIT is set (for testing)
def _compose_rate_limit() -> str:
    """Build SlowAPI limit string from environment variables."""

    if os.getenv("DISABLE_RATE_LIMIT", "false").lower() == "true":
        return "100000/minute"

    direct_limit = os.getenv("RATE_LIMIT")
    if direct_limit:
        return direct_limit

    parts: list[str] = []

    per_minute = os.getenv("RATE_LIMIT_PER_MINUTE")
    if per_minute:
        parts.append(f"{per_minute}/minute")

    per_hour = os.getenv("RATE_LIMIT_PER_HOUR")
    if per_hour:
        parts.append(f"{per_hour}/hour")

    per_day = os.getenv("RATE_LIMIT_PER_DAY")
    if per_day:
        parts.append(f"{per_day}/day")

    if parts:
        return ";".join(parts)

    return "10/minute"


RATE_LIMIT = _compose_rate_limit()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration (from environment variables)
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# Prometheus metrics instrumentation
instrumentator = create_instrumentator()
instrumentator.instrument(app).expose(app, endpoint="/metrics", include_in_schema=True)

# Set application info for metrics
set_app_info(
    version=os.getenv("APP_VERSION", "0.1.0"),
    environment=os.getenv("ENVIRONMENT", "development"),
)


# =========================
# Middleware for Structured Logging
# =========================


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """
    Middleware for structured logging with correlation IDs and request tracking.

    Adds:
    - Correlation ID for request tracing
    - Request/response logging
    - Performance metrics
    - Context cleanup
    """
    # Generate correlation ID
    correlation_id = request.headers.get("X-Correlation-ID", uuid4().hex)
    bind_correlation_id(correlation_id)

    # Log request start
    start_time = time.time()
    logger.info(
        "request_started",
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host if request.client else None,
    )

    try:
        # Process request
        response = await call_next(request)

        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000

        # Log request completion
        events.api_request(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
        )

        # Add correlation ID to response headers
        response.headers["X-Correlation-ID"] = correlation_id

        return response

    except Exception as exc:
        # Log error
        duration_ms = (time.time() - start_time) * 1000
        logger.error(
            "request_failed",
            method=request.method,
            path=request.url.path,
            duration_ms=duration_ms,
            error=str(exc),
            exc_info=True,
        )
        raise

    finally:
        # Clear context to prevent leakage
        clear_context()

# =========================
# Models
# =========================


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.

    Attributes:
        conversation_id: Optional conversation ID to continue existing conversation.
                        If not provided, a new conversation will be created.
        message: User's message to send to the agent.

    Example:
        ```json
        {
            "conversation_id": "conv_123abc",
            "message": "I want to build a house"
        }
        ```
    """
    conversation_id: Optional[str] = None
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "conv_abc123def456",
                "message": "How much would a 150m² house cost?"
            }
        }


class MessageResponse(BaseModel):
    """
    Response message from an agent.

    Attributes:
        content: The message content from the agent.
        agent: Name of the agent that generated this message.
    """
    content: str
    agent: str

    class Config:
        json_schema_extra = {
            "example": {
                "content": "A 150m² house typically costs between CHF 450,000 and CHF 562,500.",
                "agent": "Cost Estimation Agent"
            }
        }


class AgentEvent(BaseModel):
    """
    Event generated during agent execution.

    Attributes:
        id: Unique event identifier.
        type: Event type (e.g., 'handoff', 'tool_call', 'message').
        agent: Name of the agent that generated this event.
        content: Event content or description.
        metadata: Optional additional event metadata.
        timestamp: Unix timestamp when event occurred.
    """
    id: str
    type: str
    agent: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[float] = None


class GuardrailCheck(BaseModel):
    """
    Guardrail check result.

    Attributes:
        id: Unique check identifier.
        name: Name of the guardrail (e.g., 'Relevance Guardrail').
        input: Input text that was checked.
        reasoning: Guardrail's reasoning for the decision.
        passed: Whether the guardrail check passed.
        timestamp: Unix timestamp when check occurred.
    """
    id: str
    name: str
    input: str
    reasoning: str
    passed: bool
    timestamp: float


class ChatResponse(BaseModel):
    """
    Response from chat endpoint.

    Attributes:
        conversation_id: Unique conversation identifier.
        current_agent: Name of the currently active agent.
        messages: List of messages from agents.
        events: List of events that occurred during execution.
        context: Current conversation context (customer info, project details, etc.).
        agents: List of available agents with their descriptions.
        guardrails: List of guardrail checks that were performed.

    Example:
        ```json
        {
            "conversation_id": "conv_abc123",
            "current_agent": "Cost Estimation Agent",
            "messages": [
                {
                    "content": "A 150m² house costs CHF 450,000-562,500",
                    "agent": "Cost Estimation Agent"
                }
            ],
            "events": [],
            "context": {
                "project_type": "Einfamilienhaus",
                "area_sqm": 150.0
            },
            "agents": [
                {"name": "Triage Agent", "description": "Main routing agent"}
            ],
            "guardrails": []
        }
        ```
    """
    conversation_id: str
    current_agent: str
    messages: List[MessageResponse]
    events: List[AgentEvent]
    context: Dict[str, Any]
    agents: List[Dict[str, Any]]
    guardrails: List[GuardrailCheck] = []

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "conv_abc123def456",
                "current_agent": "Triage Agent",
                "messages": [
                    {
                        "content": "Welcome to ERNI Gruppe! How can I help you today?",
                        "agent": "Triage Agent"
                    }
                ],
                "events": [],
                "context": {},
                "agents": [
                    {"name": "Triage Agent", "description": "Main routing agent"}
                ],
                "guardrails": []
            }
        }


# =========================
# Session Management with AgentSessionManager
# =========================

# Initialize global session manager
session_manager = get_session_manager()

# Alias for backward compatibility with tests
conversation_store = session_manager

logger.info(f"Using SQLite sessions database at: {session_manager.db_path}")


def get_session(conversation_id: str) -> SQLiteSession:
    """
    Get or create a SQLiteSession for the given conversation ID.

    Uses the global AgentSessionManager for centralized session management.

    Args:
        conversation_id: Unique conversation identifier

    Returns:
        SQLiteSession instance for managing conversation history
    """
    return session_manager.get_session(conversation_id)


# =========================
# Agent Execution with Retry Logic
# =========================

# Configure timeout and retry settings
AGENT_TIMEOUT_SECONDS = int(os.getenv("AGENT_TIMEOUT_SECONDS", "30"))
AGENT_MAX_RETRIES = int(os.getenv("AGENT_MAX_RETRIES", "3"))

logger.info(
    f"Agent execution configured: timeout={AGENT_TIMEOUT_SECONDS}s, "
    f"max_retries={AGENT_MAX_RETRIES}"
)


@retry(
    stop=stop_after_attempt(AGENT_MAX_RETRIES),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((OpenAIError, APITimeoutError, RateLimitError)),
    reraise=True,
)
async def _run_agent_with_retry_impl(
    agent: Agent,
    input_data: Any,
    context: Any,
    session: SQLiteSession,
) -> RunResult:
    """
    Internal implementation of agent execution with retry logic.

    Retries on OpenAI API errors with exponential backoff.

    Args:
        agent: Agent to run
        input_data: Input message or items
        context: Agent context
        session: SQLite session for conversation history

    Returns:
        RunResult from agent execution

    Raises:
        OpenAIError: If all retries are exhausted
        asyncio.TimeoutError: If execution exceeds timeout
    """
    return await Runner.run(agent, input_data, context=context, session=session)


async def run_agent_with_retry(
    agent: Agent,
    input_data: Any,
    context: Any,
    session: SQLiteSession,
    timeout: Optional[int] = None,
) -> RunResult:
    """
    Run an agent with timeout and retry logic.

    Features:
    - Automatic timeout (default: 30 seconds)
    - Retry on transient OpenAI API errors (max 3 attempts)
    - Exponential backoff between retries (2s, 4s, 8s)
    - Detailed error logging

    Args:
        agent: Agent to run
        input_data: Input message or items
        context: Agent context
        session: SQLite session for conversation history
        timeout: Optional custom timeout in seconds (default: AGENT_TIMEOUT_SECONDS)

    Returns:
        RunResult from agent execution

    Raises:
        HTTPException: 504 on timeout, 503 on API errors, 500 on unexpected errors
    """
    timeout_seconds = timeout or AGENT_TIMEOUT_SECONDS

    try:
        # Execute with timeout
        result = await asyncio.wait_for(
            _run_agent_with_retry_impl(agent, input_data, context, session),
            timeout=timeout_seconds,
        )
        return result

    except asyncio.TimeoutError:
        logger.error(
            f"Agent execution timeout after {timeout_seconds}s for agent: {agent.name}"
        )
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Request timeout after {timeout_seconds} seconds. Please try again.",
        )

    except RetryError as e:
        # All retries exhausted
        original_error = e.last_attempt.exception()
        logger.error(
            f"Agent execution failed after {AGENT_MAX_RETRIES} retries: {original_error}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service temporarily unavailable. Please try again later.",
        )

    except (OpenAIError, APITimeoutError, RateLimitError) as e:
        # Single attempt failed (shouldn't happen due to retry decorator, but handle anyway)
        logger.error(f"OpenAI API error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service temporarily unavailable. Please try again later.",
        )

    except InputGuardrailTripwireTriggered:
        # Guardrail triggered - re-raise to be handled by caller
        raise

    except Exception as e:
        # Unexpected error
        logger.error(f"Unexpected error in agent execution: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later.",
        )

# =========================
# Helpers
# =========================


def _get_agent_by_name(name: str):
    """Return the agent object by name."""
    agents = {
        triage_agent.name: triage_agent,
        faq_agent.name: faq_agent,
        project_information_agent.name: project_information_agent,
        cost_estimation_agent.name: cost_estimation_agent,
        project_status_agent.name: project_status_agent,
        appointment_booking_agent.name: appointment_booking_agent,
    }
    return agents.get(name, triage_agent)


def _get_guardrail_name(g) -> str:
    """Extract a friendly guardrail name."""
    name_attr = getattr(g, "name", None)
    if isinstance(name_attr, str) and name_attr:
        return name_attr
    guard_fn = getattr(g, "guardrail_function", None)
    if guard_fn is not None and hasattr(guard_fn, "__name__"):
        return guard_fn.__name__.replace("_", " ").title()
    fn_name = getattr(g, "__name__", None)
    if isinstance(fn_name, str) and fn_name:
        return fn_name.replace("_", " ").title()
    return str(g)


def _build_agents_list() -> List[Dict[str, Any]]:
    """Build a list of all available agents and their metadata."""

    def make_agent_dict(agent):
        """
        Convert an agent instance to a dictionary representation.

        Args:
            agent: Agent instance to convert

        Returns:
            Dictionary with agent metadata (name, description, handoffs, tools, guardrails)
        """
        return {
            "name": agent.name,
            "description": getattr(agent, "handoff_description", ""),
            "handoffs": [
                getattr(h, "agent_name", getattr(h, "name", ""))
                for h in getattr(agent, "handoffs", [])
            ],
            "tools": [
                getattr(t, "name", getattr(t, "__name__", ""))
                for t in getattr(agent, "tools", [])
            ],
            "input_guardrails": [
                _get_guardrail_name(g) for g in getattr(agent, "input_guardrails", [])
            ],
            "output_guardrails": [
                _get_guardrail_name(g) for g in getattr(agent, "output_guardrails", [])
            ],
        }

    return [
        make_agent_dict(triage_agent),
        make_agent_dict(faq_agent),
        make_agent_dict(project_information_agent),
        make_agent_dict(cost_estimation_agent),
        make_agent_dict(project_status_agent),
        make_agent_dict(appointment_booking_agent),
    ]


# =========================
# Authentication Endpoints
# =========================


@app.post(
    "/auth/token",
    response_model=Token,
    tags=["authentication"],
    summary="Obtain JWT access token",
    description="""
Authenticate with username and password to obtain a JWT access token.

**Token Usage:**
Include the token in subsequent requests using the `Authorization` header:
```
Authorization: Bearer <your_token_here>
```

**Token Expiration:**
Tokens expire after {ACCESS_TOKEN_EXPIRE_MINUTES} minutes. Request a new token when expired.

**Note:** For development/testing purposes, use the `/auth/demo/token` endpoint.
    """,
)
async def login(username: str, password: str) -> Token:
    """
    Authenticate user and return JWT access token.

    Args:
        username: User's username
        password: User's password

    Returns:
        Token object with access_token and expiration info

    Raises:
        HTTPException: If credentials are invalid
    """
    user = authenticate_user(username, password)

    if not user:
        # Log and record failed authentication
        events.authentication_attempt(
            username=username,
            success=False,
            method="password",
        )
        record_authentication_attempt(method="password", success=False)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Log and record successful authentication
    events.authentication_attempt(
        username=username,
        success=True,
        method="password",
    )
    record_authentication_attempt(method="password", success=True)

    # Create access token with user data
    access_token = create_access_token(
        data={"sub": user.username, "roles": user.roles}
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
    )


# Demo login endpoint - DEVELOPMENT ONLY
if os.getenv("ENVIRONMENT") == "development":
    @app.post(
        "/auth/demo/token",
        response_model=Token,
        tags=["authentication", "development"],
        summary="Demo login (DEVELOPMENT ONLY)",
        description="""
        **⚠️ DEVELOPMENT ONLY - This endpoint is disabled in production**

        Demo credentials for testing:
        - Username: `demo` / Password: `secret` (User role)
        - Username: `admin` / Password: `secret` (Admin role)

        This endpoint provides quick access tokens for development and testing purposes.
        It is automatically disabled when ENVIRONMENT is set to 'production'.
        """,
    )
    async def demo_login(username: str = "demo", password: str = "secret") -> Token:
        """
        Demo login endpoint - DEVELOPMENT ONLY.

        Args:
            username: Demo username (default: "demo")
            password: Demo password (default: "secret")

        Returns:
            Token object with access_token

        Raises:
            HTTPException: If credentials are invalid
        """
        user = authenticate_user(username, password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid demo credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token = create_access_token(
            data={"sub": user.username, "roles": user.roles}
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )


@app.get(
    "/auth/me",
    response_model=User,
    tags=["authentication"],
    summary="Get current user information",
    description="Retrieve information about the currently authenticated user.",
)
async def read_users_me(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Get current authenticated user's information.

    Args:
        current_user: Current user from JWT token (injected by dependency)

    Returns:
        User object with user information
    """
    return current_user


# =========================
# Main Chat Endpoint
# =========================


@app.post(
    "/chat",
    response_model=ChatResponse,
    tags=["chat"],
    summary="Send a message to the building agents",
    description="""
Send a message to ERNI Gruppe's multi-agent system for building and construction inquiries.

The system automatically routes your message to the appropriate specialized agent and maintains
conversation context across multiple messages.
    """,
    responses={
        200: {
            "description": "Successful response with agent messages",
        },
        400: {"description": "Invalid request format"},
        429: {"description": "Rate limit exceeded (10 requests/minute)"},
        500: {"description": "Internal server error"},
        503: {"description": "AI service temporarily unavailable"},
        504: {"description": "Request timeout (>30 seconds)"},
    }
)
@limiter.limit(RATE_LIMIT)
async def chat_endpoint(
    body: ChatRequest,
    request: Request,
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Main chat endpoint for agent orchestration.

    Handles conversation state, agent routing, and guardrail checks.
    Uses SQLiteSession for production-ready conversation management.
    Rate limited to 10 requests per minute per IP.

    **Authentication:**
    - Optional by default (set REQUIRE_AUTH=true to enforce)
    - If authenticated, user info is logged for audit purposes
    """
    # Log authenticated user if present
    if current_user:
        bind_user_context(username=current_user.username)
        logger.info("authenticated_chat_request", username=current_user.username)

    try:
        # Generate or use existing conversation ID
        # If conversation_id is provided and not empty, use it; otherwise generate new
        if body.conversation_id and body.conversation_id.strip():
            conversation_id = body.conversation_id
        else:
            conversation_id = uuid4().hex

        # Bind conversation context for logging
        bind_conversation_context(conversation_id)

        # Record conversation started (for new conversations)
        if not body.conversation_id or not body.conversation_id.strip():
            record_conversation_started()

        # Get SQLiteSession for this conversation
        session = get_session(conversation_id)

        # Backward compatibility: call conversation_store.get() for tests
        conversation_store.get(conversation_id)

        # Update active sessions metric
        update_active_sessions(session_manager.get_active_session_count())

        # Get or initialize context (preserve inquiry_id and other context between requests)
        stored_context = session_manager.get_context(conversation_id)
        if stored_context:
            # Restore context from previous requests
            ctx = BuildingProjectContext(**stored_context)
            logger.debug(f"Restored context for conversation {conversation_id}: inquiry_id={ctx.inquiry_id}")
        else:
            # Initialize new context for first request
            ctx = create_initial_context()
            logger.debug(f"Created new context for conversation {conversation_id}: inquiry_id={ctx.inquiry_id}")

        # Determine current agent (default to triage for new conversations)
        # In production, you might want to store current_agent in session metadata
        current_agent = triage_agent

        # Handle empty message (initialization request)
        if body.message.strip() == "":
            # Save context for initialization request
            session_manager.set_context(conversation_id, ctx.model_dump())

            return ChatResponse(
                conversation_id=conversation_id,
                current_agent=current_agent.name,
                messages=[],
                events=[],
                context=ctx.model_dump(),
                agents=_build_agents_list(),
                guardrails=[],
            )

        # Store old context for change detection
        old_context = ctx.model_dump().copy()
        guardrail_checks: List[GuardrailCheck] = []

        try:
            # Log agent execution start
            agent_start_time = time.time()
            events.agent_started(
                agent_name=current_agent.name,
                conversation_id=conversation_id,
            )

            # Run agent with timeout and retry logic
            result = await run_agent_with_retry(
                agent=current_agent,
                input_data=body.message,
                context=ctx,
                session=session
            )

            # Log and record agent execution completion
            agent_duration_ms = (time.time() - agent_start_time) * 1000
            agent_duration_seconds = agent_duration_ms / 1000
            events.agent_completed(
                agent_name=current_agent.name,
                conversation_id=conversation_id,
                duration_ms=agent_duration_ms,
            )
            record_agent_execution(
                agent_name=current_agent.name,
                duration_seconds=agent_duration_seconds,
                status="success",
            )
            record_message_processed(agent_name=current_agent.name)
        except InputGuardrailTripwireTriggered as e:
            failed = e.guardrail_result.guardrail
            gr_output = e.guardrail_result.output.output_info
            gr_reasoning = getattr(gr_output, "reasoning", "")
            gr_input = body.message
            gr_timestamp = time.time() * 1000
            for g in current_agent.input_guardrails:
                guardrail_name = _get_guardrail_name(g)
                passed = (g != failed)
                guardrail_checks.append(
                    GuardrailCheck(
                        id=uuid4().hex,
                        name=guardrail_name,
                        input=gr_input,
                        reasoning=(gr_reasoning if g == failed else ""),
                        passed=passed,
                        timestamp=gr_timestamp,
                    )
                )
                # Record guardrail check metric
                record_guardrail_check(guardrail_name, passed)
            refusal = "Sorry, I can only answer questions related to building and construction."
            # Note: With SQLiteSession, the refusal is not added to history automatically
            # The session will be empty for this failed request

            # Save context even on guardrail failure (preserve inquiry_id)
            session_manager.set_context(conversation_id, ctx.model_dump())

            return ChatResponse(
                conversation_id=conversation_id,
                current_agent=current_agent.name,
                messages=[MessageResponse(content=refusal, agent=current_agent.name)],
                events=[],
                context=ctx.model_dump(),
                agents=_build_agents_list(),
                guardrails=guardrail_checks,
            )

        messages: List[MessageResponse] = []
        agent_events: List[AgentEvent] = []

        for item in result.new_items:
            if isinstance(item, MessageOutputItem):
                text = ItemHelpers.text_message_output(item)
                messages.append(MessageResponse(content=text, agent=item.agent.name))
                agent_events.append(
                    AgentEvent(
                        id=uuid4().hex,
                        type="message",
                        agent=item.agent.name,
                        content=text,
                    )
                )
            # Handle handoff output and agent switching
            elif isinstance(item, HandoffOutputItem):
                # Log and record structured handoff event
                events.agent_handoff(
                    from_agent=item.source_agent.name,
                    to_agent=item.target_agent.name,
                    conversation_id=conversation_id,
                )
                record_agent_handoff(
                    from_agent=item.source_agent.name,
                    to_agent=item.target_agent.name,
                )

                # Record the handoff event
                agent_events.append(
                    AgentEvent(
                        id=uuid4().hex,
                        type="handoff",
                        agent=item.source_agent.name,
                        content=f"{item.source_agent.name} -> {item.target_agent.name}",
                        metadata={
                            "source_agent": item.source_agent.name,
                            "target_agent": item.target_agent.name,
                        },
                    )
                )
                # If there is an on_handoff callback defined for this handoff, show it as a tool call
                from_agent = item.source_agent
                to_agent = item.target_agent
                # Find the Handoff object on the source agent matching the target
                ho = next(
                    (
                        h
                        for h in getattr(from_agent, "handoffs", [])
                        if isinstance(h, Handoff)
                        and getattr(h, "agent_name", None) == to_agent.name
                    ),
                    None,
                )
                if ho:
                    fn = ho.on_invoke_handoff
                    fv = fn.__code__.co_freevars
                    cl = fn.__closure__ or []
                    if "on_handoff" in fv:
                        idx = fv.index("on_handoff")
                        if idx < len(cl) and cl[idx].cell_contents:
                            cb = cl[idx].cell_contents
                            cb_name = getattr(cb, "__name__", repr(cb))
                            agent_events.append(
                                AgentEvent(
                                    id=uuid4().hex,
                                    type="tool_call",
                                    agent=to_agent.name,
                                    content=cb_name,
                                )
                            )
                current_agent = item.target_agent
            elif isinstance(item, ToolCallItem):
                tool_name = getattr(item.raw_item, "name", None)
                raw_args = getattr(item.raw_item, "arguments", None)
                tool_args: Any = raw_args
                if isinstance(raw_args, str):
                    try:
                        import json

                        tool_args = json.loads(raw_args)
                    except Exception:
                        pass
                agent_events.append(
                    AgentEvent(
                        id=uuid4().hex,
                        type="tool_call",
                        agent=item.agent.name,
                        content=tool_name or "",
                        metadata={"tool_args": tool_args},
                    )
                )
                # Special handling for UI-specific tools (currently none for ERNI)
                # if tool_name == "some_special_tool":
                #     messages.append(
                #         MessageResponse(
                #             content="SPECIAL_ACTION",
                #             agent=item.agent.name,
                #         )
                #     )
            elif isinstance(item, ToolCallOutputItem):
                agent_events.append(
                    AgentEvent(
                        id=uuid4().hex,
                        type="tool_output",
                        agent=item.agent.name,
                        content=str(item.output),
                        metadata={"tool_result": item.output},
                    )
                )

        # Detect context changes
        new_context = ctx.model_dump()
        changes = {
            k: new_context[k]
            for k in new_context
            if old_context.get(k) != new_context[k]
        }
        if changes:
            agent_events.append(
                AgentEvent(
                    id=uuid4().hex,
                    type="context_update",
                    agent=current_agent.name,
                    content="",
                    metadata={"changes": changes},
                )
            )

        # Note: SQLiteSession automatically manages conversation history
        # No need to manually save state - it's handled by the session

        # Backward compatibility: call conversation_store.save() for tests
        conversation_store.save(conversation_id)

        # Build guardrail results: mark failures (if any), and any others as passed
        final_guardrails: List[GuardrailCheck] = []

        # Add input guardrails
        for g in getattr(current_agent, "input_guardrails", []):
            name = _get_guardrail_name(g)
            failed = next((gc for gc in guardrail_checks if gc.name == name), None)
            if failed:
                final_guardrails.append(failed)
            else:
                final_guardrails.append(
                    GuardrailCheck(
                        id=uuid4().hex,
                        name=name,
                        input=body.message,
                        reasoning="",
                        passed=True,
                        timestamp=time.time() * 1000,
                    )
                )

        # Add output guardrails (always passed if no exception was raised)
        for g in getattr(current_agent, "output_guardrails", []):
            name = _get_guardrail_name(g)
            # Output guardrails check agent responses, not user input
            # If we reached here, output guardrails passed (no OutputGuardrailTripwireTriggered)
            final_guardrails.append(
                GuardrailCheck(
                    id=uuid4().hex,
                    name=name,
                    input="",  # Output guardrails don't have user input
                    reasoning="",
                    passed=True,
                    timestamp=time.time() * 1000,
                )
            )

        # Save context for next request (preserve inquiry_id and other context)
        session_manager.set_context(conversation_id, ctx.model_dump())

        return ChatResponse(
            conversation_id=conversation_id,
            current_agent=current_agent.name,
            messages=messages,
            events=agent_events,
            context=ctx.model_dump(),
            agents=_build_agents_list(),
            guardrails=final_guardrails,
        )
    except InputGuardrailTripwireTriggered:
        # Already handled above, re-raise
        raise
    except HTTPException:
        # Re-raise HTTP exceptions (like rate limit)
        raise
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred processing your request. Please try again later.",
        )


# =========================
# Health Check Endpoints
# =========================


@app.get(
    "/health",
    tags=["health"],
    summary="Health check endpoint",
    description="Returns basic application health status for monitoring and load balancers.",
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "timestamp": "2025-01-15T10:30:00.000Z",
                        "version": "1.0.0",
                        "environment": "production",
                        "service": "ERNI Building Agents API"
                    }
                }
            }
        }
    }
)
async def health_check():
    """
    Health check endpoint for monitoring.

    Returns basic application health status including version, environment, and timestamp.
    This endpoint is lightweight and always returns 200 OK if the service is running.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "service": "ERNI Building Agents API",
    }


@app.get(
    "/readiness",
    tags=["health"],
    summary="Readiness check endpoint",
    description="""
Kubernetes/Docker readiness probe endpoint.

Verifies that all critical dependencies are available and configured:
- OpenAI API key is set
- OpenAI API is reachable

Returns 200 OK if ready, 503 Service Unavailable if not ready.
    """,
    responses={
        200: {
            "description": "Service is ready to accept requests",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ready",
                        "checks": {
                            "openai_api": True,
                            "environment_configured": True
                        }
                    }
                }
            }
        },
        503: {
            "description": "Service is not ready",
            "content": {
                "application/json": {
                    "example": {
                        "status": "not_ready",
                        "checks": {
                            "openai_api": False,
                            "environment_configured": True
                        }
                    }
                }
            }
        }
    }
)
async def readiness_check(response: Response):
    """
    Readiness check endpoint for Kubernetes/Docker health checks.

    Verifies that all dependencies are available and properly configured.
    Returns 503 if any critical dependency is unavailable.
    """
    checks = {
        "openai_api": False,
        "environment_configured": False,
    }

    # Check if OPENAI_API_KEY is configured
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and len(openai_key) > 0:
        checks["environment_configured"] = True

        # Only check OpenAI API connectivity if key is configured
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Simple check to OpenAI API
                headers = {
                    "Authorization": f"Bearer {openai_key}",
                    "Content-Type": "application/json",
                }
                # Use models endpoint as a lightweight check
                api_response = await client.get(
                    "https://api.openai.com/v1/models", headers=headers
                )
                if api_response.status_code == 200:
                    checks["openai_api"] = True
        except Exception as e:
            logger.warning(f"OpenAI API check failed: {e}")
            checks["openai_api"] = False
    else:
        # No API key configured - skip network check
        logger.warning(
            "OPENAI_API_KEY not configured - skipping API connectivity check"
        )
        checks["openai_api"] = False

    # Determine overall readiness
    all_ready = all(checks.values())

    if not all_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": "ready" if all_ready else "not_ready",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks,
        "version": "1.0.0",
    }


# =========================
# Agent Information Endpoints
# =========================


@app.get(
    "/agents",
    tags=["agents"],
    summary="List all available agents",
    description="""
Get information about all available agents in the system.

Returns a list of agents with their:
- Name
- Description (handoff description)
- Available handoffs to other agents
- Available tools
- Configured input guardrails (validate user input)
- Configured output guardrails (validate agent responses)

This endpoint is useful for understanding the agent architecture and capabilities.
    """,
    responses={
        200: {
            "description": "List of all agents",
            "content": {
                "application/json": {
                    "example": {
                        "agents": [
                            {
                                "name": "Triage Agent",
                                "description": "Main routing agent",
                                "handoffs": ["Project Information Agent", "Cost Estimation Agent"],
                                "tools": [],
                                "input_guardrails": ["Relevance Guardrail", "Jailbreak Guardrail"],
                                "output_guardrails": ["PII Guardrail"]
                            }
                        ],
                        "total": 6
                    }
                }
            }
        }
    }
)
async def list_agents():
    """
    List all available agents with their metadata.

    Returns information about all 6 specialized agents including their
    capabilities, handoffs, tools, and guardrails.
    """
    agents_list = _build_agents_list()
    return {
        "agents": agents_list,
        "total": len(agents_list),
        "timestamp": datetime.utcnow().isoformat(),
    }
