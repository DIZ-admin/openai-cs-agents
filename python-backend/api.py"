import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4
from pathlib import Path

import httpx
from agents import (
    Handoff,
    HandoffOutputItem,
    InputGuardrailTripwireTriggered,
    ItemHelpers,
    MessageOutputItem,
    Runner,
    SQLiteSession,
    ToolCallItem,
    ToolCallOutputItem,
)
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from main import (
    appointment_booking_agent,
    cost_estimation_agent,
    create_initial_context,
    faq_agent,
    project_information_agent,
    project_status_agent,
    triage_agent,
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Rate limiting configuration
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

# =========================
# Models
# =========================


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str


class MessageResponse(BaseModel):
    content: str
    agent: str


class AgentEvent(BaseModel):
    id: str
    type: str
    agent: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[float] = None


class GuardrailCheck(BaseModel):
    id: str
    name: str
    input: str
    reasoning: str
    passed: bool
    timestamp: float


class ChatResponse(BaseModel):
    conversation_id: str
    current_agent: str
    messages: List[MessageResponse]
    events: List[AgentEvent]
    context: Dict[str, Any]
    agents: List[Dict[str, Any]]
    guardrails: List[GuardrailCheck] = []


# =========================
# Session Management with SQLiteSession
# =========================

# Configure SQLite database path
SESSIONS_DB_PATH = Path(os.getenv("SESSIONS_DB_PATH", "data/conversations.db"))
SESSIONS_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

logger.info(f"Using SQLite sessions database at: {SESSIONS_DB_PATH}")


def get_session(conversation_id: str) -> SQLiteSession:
    """
    Get or create a SQLiteSession for the given conversation ID.

    Args:
        conversation_id: Unique conversation identifier

    Returns:
        SQLiteSession instance for managing conversation history
    """
    return SQLiteSession(
        session_id=conversation_id,
        db_path=str(SESSIONS_DB_PATH)
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
# Main Chat Endpoint
# =========================


@app.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat_endpoint(request: Request, req: ChatRequest):
    """
    Main chat endpoint for agent orchestration.
    Handles conversation state, agent routing, and guardrail checks.
    Rate limited to 10 requests per minute per IP.

    Now uses SQLiteSession for production-ready conversation management.
    """
    try:
        # Generate or use existing conversation ID
        # If conversation_id is provided and not empty, use it; otherwise generate new
        if req.conversation_id and req.conversation_id.strip():
            conversation_id = req.conversation_id
        else:
            conversation_id = uuid4().hex

        # Get SQLiteSession for this conversation
        session = get_session(conversation_id)

        # Initialize context (will be updated by agents)
        ctx = create_initial_context()

        # Determine current agent (default to triage for new conversations)
        # In production, you might want to store current_agent in session metadata
        current_agent = triage_agent

        # Handle empty message (initialization request)
        if req.message.strip() == "":
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
            # Run agent with session (automatically manages conversation history)
            result = await Runner.run(
                current_agent,
                req.message,
                context=ctx,
                session=session
            )
        except InputGuardrailTripwireTriggered as e:
            failed = e.guardrail_result.guardrail
            gr_output = e.guardrail_result.output.output_info
            gr_reasoning = getattr(gr_output, "reasoning", "")
            gr_input = req.message
            gr_timestamp = time.time() * 1000
            for g in current_agent.input_guardrails:
                guardrail_checks.append(
                    GuardrailCheck(
                        id=uuid4().hex,
                        name=_get_guardrail_name(g),
                        input=gr_input,
                        reasoning=(gr_reasoning if g == failed else ""),
                        passed=(g != failed),
                        timestamp=gr_timestamp,
                    )
                )
            refusal = "Sorry, I can only answer questions related to building and construction."
            # Note: With SQLiteSession, the refusal is not added to history automatically
            # The session will be empty for this failed request
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
        events: List[AgentEvent] = []

        for item in result.new_items:
            if isinstance(item, MessageOutputItem):
                text = ItemHelpers.text_message_output(item)
                messages.append(MessageResponse(content=text, agent=item.agent.name))
                events.append(
                    AgentEvent(
                        id=uuid4().hex,
                        type="message",
                        agent=item.agent.name,
                        content=text,
                    )
                )
            # Handle handoff output and agent switching
            elif isinstance(item, HandoffOutputItem):
                # Record the handoff event
                events.append(
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
                            events.append(
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
                events.append(
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
                events.append(
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
            events.append(
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

        # Build guardrail results: mark failures (if any), and any others as passed
        final_guardrails: List[GuardrailCheck] = []
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
                        input=req.message,
                        reasoning="",
                        passed=True,
                        timestamp=time.time() * 1000,
                    )
                )

        return ChatResponse(
            conversation_id=conversation_id,
            current_agent=current_agent.name,
            messages=messages,
            events=events,
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


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    Returns basic application health status.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "service": "ERNI Building Agents API",
    }


@app.get("/readiness")
async def readiness_check(response: Response):
    """
    Readiness check endpoint for Kubernetes/Docker health checks.
    Verifies that all dependencies are available.
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
