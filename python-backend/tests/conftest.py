"""
Pytest configuration and shared fixtures for ERNI Gruppe Building Agents tests.
"""

import asyncio
import os
from typing import AsyncGenerator, Dict, Any
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from agents import Agent, RunContextWrapper
from fastapi.testclient import TestClient

# Import the main application components
from main import (
    BuildingProjectContext,
    create_initial_context,
    triage_agent,
    project_information_agent,
    cost_estimation_agent,
    project_status_agent,
    appointment_booking_agent,
    faq_agent,
)
from api import app


# ============================================================================
# Environment Setup
# ============================================================================

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    os.environ["OPENAI_API_KEY"] = "test-api-key"
    os.environ["ENVIRONMENT"] = "test"
    os.environ["DEBUG"] = "true"


# ============================================================================
# Context Fixtures
# ============================================================================

@pytest.fixture
def empty_context() -> BuildingProjectContext:
    """Create an empty BuildingProjectContext for testing."""
    return BuildingProjectContext()


@pytest.fixture
def sample_context() -> BuildingProjectContext:
    """Create a sample BuildingProjectContext with test data."""
    return BuildingProjectContext(
        customer_name="Hans Müller",
        customer_email="hans.mueller@example.com",
        customer_phone="+41 79 123 45 67",
        project_number="2024-156",
        project_type="Einfamilienhaus",
        construction_type="Holzbau",
        area_sqm=150.0,
        location="Muri",
        budget_chf=450000.0,
        preferred_start_date="2025-05-01",
        consultation_booked=False,
        specialist_assigned=None,
        inquiry_id="INQ-12345",
    )


@pytest.fixture
def context_wrapper(sample_context) -> RunContextWrapper[BuildingProjectContext]:
    """Create a RunContextWrapper with sample context."""
    wrapper = MagicMock(spec=RunContextWrapper)
    wrapper.context = sample_context
    return wrapper


# ============================================================================
# Agent Fixtures
# ============================================================================

@pytest.fixture
def mock_agents():
    """Mock all agents for testing."""
    return {
        "triage": triage_agent,
        "project_info": project_information_agent,
        "cost_estimation": cost_estimation_agent,
        "project_status": project_status_agent,
        "appointment_booking": appointment_booking_agent,
        "faq": faq_agent,
    }


# ============================================================================
# API Client Fixtures
# ============================================================================

@pytest.fixture
def test_client() -> TestClient:
    """Create a test client for FastAPI application."""
    return TestClient(app)


@pytest.fixture
async def async_test_client():
    """Create an async test client for FastAPI application."""
    from httpx import AsyncClient
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# ============================================================================
# Mock Fixtures
# ============================================================================

@pytest.fixture
def mock_openai_runner():
    """Mock the OpenAI Runner for testing."""
    with patch("main.Runner") as mock_runner:
        # Mock successful run result
        mock_result = MagicMock()
        mock_result.final_output_as.return_value = MagicMock(
            reasoning="Test reasoning",
            is_relevant=True,
            is_safe=True
        )
        mock_result.new_items = []
        mock_result.to_input_list.return_value = []
        
        mock_runner.run = AsyncMock(return_value=mock_result)
        yield mock_runner


@pytest.fixture
def mock_conversation_store():
    """Mock conversation store for testing."""
    store = {}
    
    def get_conversation(conversation_id: str):
        return store.get(conversation_id)
    
    def save_conversation(conversation_id: str, state: Dict[str, Any]):
        store[conversation_id] = state
    
    with patch("api.conversation_store") as mock_store:
        mock_store.get = MagicMock(side_effect=get_conversation)
        mock_store.save = MagicMock(side_effect=save_conversation)
        yield mock_store


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_chat_request():
    """Sample chat request data."""
    return {
        "conversation_id": str(uuid4()),
        "message": "Hello, I want to build a house"
    }


@pytest.fixture
def sample_project_data():
    """Sample project data for testing tools."""
    return {
        "project_type": "Einfamilienhaus",
        "area_sqm": 150.0,
        "construction_type": "Holzbau",
        "location": "Muri"
    }


@pytest.fixture
def sample_specialist_data():
    """Sample specialist data for appointment booking."""
    return {
        "specialist_type": "Architekt",
        "preferred_date": "next Tuesday",
        "date": "Tuesday, May 15",
        "time": "14:00"
    }


# ============================================================================
# Utility Functions
# ============================================================================

def create_mock_agent(name: str, description: str = "") -> Agent:
    """Create a mock agent for testing."""
    agent = MagicMock(spec=Agent)
    agent.name = name
    agent.handoff_description = description
    agent.tools = []
    agent.input_guardrails = []
    agent.handoffs = []
    return agent


def create_test_message(content: str, role: str = "user") -> Dict[str, Any]:
    """Create a test message dictionary."""
    return {
        "content": content,
        "role": role
    }
