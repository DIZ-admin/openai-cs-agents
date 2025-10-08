"""
Integration tests for main.py decorated functions.

These tests verify that the actual decorated functions from main.py work correctly
with the OpenAI Agents SDK decorators intact (@function_tool, @input_guardrail).
"""

import pytest
from unittest.mock import MagicMock
from main import (
    # Agents
    triage_agent,
    cost_estimation_agent,
    project_information_agent,
    project_status_agent,
    appointment_booking_agent,
    faq_agent,
    # Guardrails
    relevance_guardrail,
    jailbreak_guardrail,
    # Tools
    faq_lookup_building,
    estimate_project_cost,
    check_specialist_availability,
    book_consultation,
    get_project_status,
    # Context
    BuildingProjectContext,
    # Handoff callbacks
    on_cost_estimation_handoff,
    on_appointment_handoff,
)


@pytest.mark.integration
@pytest.mark.agents
class TestAgentIntegration:
    """Integration tests for agent configurations with decorators."""

    def test_triage_agent_has_correct_handoffs(self):
        """Test that triage agent has all expected handoff targets."""
        assert triage_agent.name == "Triage Agent"

        # Check that agent has handoffs
        # Triage agent should have 5 handoffs (project_info, cost_est, project_status, appointment, faq)
        assert len(triage_agent.handoffs) == 5

        # Extract agent names from handoffs
        # Handoff objects have agent_name attribute
        handoff_agent_names = []
        for h in triage_agent.handoffs:
            assert h is not None
            # Handoff objects have agent_name attribute
            if hasattr(h, "agent_name"):
                handoff_agent_names.append(h.agent_name)
            # Some might be Agent objects with name attribute
            elif hasattr(h, "name"):
                handoff_agent_names.append(h.name)

        # Check all expected agents are present
        assert "Project Information Agent" in handoff_agent_names
        assert "Cost Estimation Agent" in handoff_agent_names
        assert "Project Status Agent" in handoff_agent_names
        assert "Appointment Booking Agent" in handoff_agent_names
        assert "FAQ Agent" in handoff_agent_names

    def test_cost_estimation_agent_has_tools(self):
        """Test that cost estimation agent has the estimate_project_cost tool."""
        assert cost_estimation_agent.name == "Cost Estimation Agent"

        # Check that agent has tools
        assert len(cost_estimation_agent.tools) > 0

        # Check that estimate_project_cost is in tools
        tool_names = [tool.name for tool in cost_estimation_agent.tools]
        assert "estimate_project_cost" in tool_names

    def test_appointment_booking_agent_has_tools(self):
        """Test that appointment booking agent has booking tools."""
        assert appointment_booking_agent.name == "Appointment Booking Agent"

        # Check tools
        tool_names = [tool.name for tool in appointment_booking_agent.tools]
        assert "check_specialist_availability" in tool_names
        assert "book_consultation" in tool_names

    def test_project_status_agent_has_tools(self):
        """Test that project status agent has status tool."""
        assert project_status_agent.name == "Project Status Agent"

        # Check tools
        tool_names = [tool.name for tool in project_status_agent.tools]
        assert "get_project_status" in tool_names

    def test_faq_agent_has_tools(self):
        """Test that FAQ agent has FAQ lookup tool."""
        assert faq_agent.name == "FAQ Agent"

        # Check tools
        tool_names = [tool.name for tool in faq_agent.tools]
        assert "faq_lookup_building" in tool_names

    def test_all_agents_have_guardrails(self):
        """Test that all agents have the required guardrails."""
        agents = [
            triage_agent,
            cost_estimation_agent,
            project_information_agent,
            project_status_agent,
            appointment_booking_agent,
            faq_agent,
        ]

        for agent in agents:
            # Check that agent has input guardrails
            assert len(agent.input_guardrails) > 0, f"{agent.name} has no guardrails"

            # Check that relevance and jailbreak guardrails are present
            guardrail_names = [g.name for g in agent.input_guardrails]
            assert "Relevance Guardrail" in guardrail_names, (
                f"{agent.name} missing Relevance Guardrail"
            )
            assert "Jailbreak Guardrail" in guardrail_names, (
                f"{agent.name} missing Jailbreak Guardrail"
            )


@pytest.mark.integration
@pytest.mark.guardrails
class TestGuardrailIntegration:
    """Integration tests for guardrail functions with decorators."""

    def test_relevance_guardrail_is_input_guardrail(self):
        """Test that relevance_guardrail is an InputGuardrail."""
        from agents import InputGuardrail

        # The decorated function should be an InputGuardrail
        assert isinstance(relevance_guardrail, InputGuardrail)
        assert relevance_guardrail.name == "Relevance Guardrail"

    def test_jailbreak_guardrail_is_input_guardrail(self):
        """Test that jailbreak_guardrail is an InputGuardrail."""
        from agents import InputGuardrail

        # The decorated function should be an InputGuardrail
        assert isinstance(jailbreak_guardrail, InputGuardrail)
        assert jailbreak_guardrail.name == "Jailbreak Guardrail"


@pytest.mark.integration
@pytest.mark.tools
class TestToolIntegration:
    """Integration tests for tool functions with decorators."""

    def test_faq_lookup_building_is_function_tool(self):
        """Test that faq_lookup_building is a FunctionTool."""
        from agents import FunctionTool

        # The decorated function should be a FunctionTool
        assert isinstance(faq_lookup_building, FunctionTool)
        assert faq_lookup_building.name == "faq_lookup_building"

    def test_estimate_project_cost_is_function_tool(self):
        """Test that estimate_project_cost is a FunctionTool."""
        from agents import FunctionTool

        assert isinstance(estimate_project_cost, FunctionTool)
        assert estimate_project_cost.name == "estimate_project_cost"

    def test_check_specialist_availability_is_function_tool(self):
        """Test that check_specialist_availability is a FunctionTool."""
        from agents import FunctionTool

        assert isinstance(check_specialist_availability, FunctionTool)
        assert check_specialist_availability.name == "check_specialist_availability"

    def test_book_consultation_is_function_tool(self):
        """Test that book_consultation is a FunctionTool."""
        from agents import FunctionTool

        assert isinstance(book_consultation, FunctionTool)
        assert book_consultation.name == "book_consultation"

    def test_get_project_status_is_function_tool(self):
        """Test that get_project_status is a FunctionTool."""
        from agents import FunctionTool

        assert isinstance(get_project_status, FunctionTool)
        assert get_project_status.name == "get_project_status"


@pytest.mark.integration
@pytest.mark.agents
class TestHandoffCallbacks:
    """Integration tests for agent handoff callbacks."""

    @pytest.mark.asyncio
    async def test_on_cost_estimation_handoff_initializes_inquiry_id(self):
        """Test that cost estimation handoff callback sets inquiry_id."""
        context = BuildingProjectContext()

        # Initially no inquiry_id
        assert context.inquiry_id is None

        # Create a RunContextWrapper
        run_context = MagicMock()
        run_context.context = context

        # Call the handoff callback (it's async)
        await on_cost_estimation_handoff(run_context)

        # Now inquiry_id should be set
        assert context.inquiry_id is not None
        assert isinstance(context.inquiry_id, str)
        assert len(context.inquiry_id) > 0

    @pytest.mark.asyncio
    async def test_on_appointment_handoff_initializes_inquiry_id(self):
        """Test that appointment handoff callback sets inquiry_id."""
        context = BuildingProjectContext()

        # Initially no inquiry_id
        assert context.inquiry_id is None

        # Create a RunContextWrapper
        run_context = MagicMock()
        run_context.context = context

        # Call the handoff callback (it's async)
        await on_appointment_handoff(run_context)

        # Now inquiry_id should be set
        assert context.inquiry_id is not None
        assert isinstance(context.inquiry_id, str)
        assert len(context.inquiry_id) > 0

    @pytest.mark.asyncio
    async def test_handoff_callbacks_preserve_existing_inquiry_id(self):
        """Test that handoff callbacks don't overwrite existing inquiry_id."""
        context = BuildingProjectContext()
        context.inquiry_id = "existing-id-123"

        # Create a RunContextWrapper
        run_context = MagicMock()
        run_context.context = context

        # Call callbacks
        await on_cost_estimation_handoff(run_context)

        # inquiry_id should remain unchanged
        assert context.inquiry_id == "existing-id-123"

        # Same for appointment handoff
        context2 = BuildingProjectContext()
        context2.inquiry_id = "existing-id-456"
        run_context2 = MagicMock()
        run_context2.context = context2
        await on_appointment_handoff(run_context2)
        assert context2.inquiry_id == "existing-id-456"


@pytest.mark.integration
@pytest.mark.agents
class TestAgentInstructions:
    """Integration tests for agent instruction functions."""

    def test_triage_agent_instructions_are_string(self):
        """Test that triage agent has instructions as a string."""
        # Instructions can be a string or a callable
        # In main.py, triage_agent uses a static string
        assert isinstance(triage_agent.instructions, str)
        assert len(triage_agent.instructions) > 0
        # Updated: Now "routing agent" instead of "triage agent"
        assert "routing" in triage_agent.instructions.lower() or "transfer" in triage_agent.instructions.lower()

    def test_cost_estimation_agent_instructions_are_callable(self):
        """Test that cost estimation agent instructions are callable."""
        # Cost estimation agent uses a function for dynamic instructions
        assert callable(cost_estimation_agent.instructions)

        # Create a mock run context
        context = BuildingProjectContext()
        context.inquiry_id = "test-inquiry-123"
        run_context = MagicMock()
        run_context.context = context

        # Call the instructions function
        instructions = cost_estimation_agent.instructions(
            run_context, cost_estimation_agent
        )

        assert isinstance(instructions, str)
        assert "test-inquiry-123" in instructions

    def test_appointment_booking_agent_instructions_are_callable(self):
        """Test that appointment booking agent instructions are callable."""
        # Appointment booking agent uses a function for dynamic instructions
        assert callable(appointment_booking_agent.instructions)

        # Create a mock run context
        context = BuildingProjectContext()
        context.consultation_booked = True
        run_context = MagicMock()
        run_context.context = context

        # Call the instructions function
        instructions = appointment_booking_agent.instructions(
            run_context, appointment_booking_agent
        )

        assert isinstance(instructions, str)
        assert "true" in instructions.lower() or "yes" in instructions.lower()
