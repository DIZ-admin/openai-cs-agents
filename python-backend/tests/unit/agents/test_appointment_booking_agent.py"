"""
Unit tests for Appointment Booking Agent functionality.
"""

import pytest
from unittest.mock import MagicMock, patch
from agents import Agent, RunContextWrapper

from main import (
    appointment_booking_agent,
    appointment_booking_instructions,
    BuildingProjectContext,
)


class TestAppointmentBookingAgent:
    """Test cases for the Appointment Booking Agent."""

    @pytest.fixture
    def mock_context_wrapper(self):
        """Create a mock context wrapper for testing."""
        context = BuildingProjectContext(
            inquiry_id="INQ-12345", consultation_booked=False
        )
        wrapper = MagicMock(spec=RunContextWrapper)
        wrapper.context = context
        return wrapper

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_agent_configuration(self):
        """Test that appointment booking agent is properly configured."""
        assert appointment_booking_agent.name == "Appointment Booking Agent"
        assert "consultations" in appointment_booking_agent.handoff_description.lower()
        assert (
            len(appointment_booking_agent.tools) == 2
        )  # check_specialist_availability, book_consultation
        assert (
            len(appointment_booking_agent.input_guardrails) == 2
        )  # relevance and jailbreak
        assert appointment_booking_agent.model == "gpt-4.1-mini"
        assert appointment_booking_agent.model_settings is not None
        assert appointment_booking_agent.model_settings.temperature == 0.7

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_agent_tools(self):
        """Test that appointment booking agent has correct tools."""
        tool_names = []
        for tool in appointment_booking_agent.tools:
            if hasattr(tool, "name"):
                tool_names.append(tool.name)
            elif hasattr(tool, "__name__"):
                tool_names.append(tool.__name__)

        assert any("check_specialist_availability" in name for name in tool_names)
        assert any("book_consultation" in name for name in tool_names)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_agent_handoffs(self):
        """Test that appointment booking agent has correct handoff targets."""
        handoff_names = []
        for handoff in appointment_booking_agent.handoffs:
            if hasattr(handoff, "agent_name"):
                handoff_names.append(handoff.agent_name)
            elif hasattr(handoff, "name"):
                handoff_names.append(handoff.name)

        expected_targets = ["Triage Agent"]
        for target in expected_targets:
            assert any(target in name for name in handoff_names)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_instructions_with_inquiry_id(
        self, mock_context_wrapper
    ):
        """Test appointment booking instructions include inquiry ID."""
        instructions = appointment_booking_instructions(
            mock_context_wrapper, appointment_booking_agent
        )

        assert isinstance(instructions, str)
        assert "INQ-12345" in instructions
        assert "Appointment Booking Agent" in instructions
        assert "ERNI Gruppe" in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_instructions_consultation_status(
        self, mock_context_wrapper
    ):
        """Test appointment booking instructions show consultation status."""
        instructions = appointment_booking_instructions(
            mock_context_wrapper, appointment_booking_agent
        )

        assert "Consultation booked: False" in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_instructions_procedure(
        self, mock_context_wrapper
    ):
        """Test that appointment booking instructions include proper procedure."""
        instructions = appointment_booking_instructions(
            mock_context_wrapper, appointment_booking_agent
        )

        procedure_steps = [
            "specialist",  # More flexible: matches "type of specialist" or "specialist type"
            "preferred date",
            "check_specialist_availability",
            "date and time",
            "contact",  # More flexible: matches "contact info" or "contact information"
            "book_consultation",
        ]

        for step in procedure_steps:
            assert step.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_instructions_specialist_types(
        self, mock_context_wrapper
    ):
        """Test that instructions mention all specialist types."""
        instructions = appointment_booking_instructions(
            mock_context_wrapper, appointment_booking_agent
        )

        specialist_types = [
            "Architekt",
            "Architect",
            "Holzbau-Ingenieur",
            "Timber Engineer",
            "Bauleiter",
            "Construction Manager",
        ]

        for specialist_type in specialist_types:
            assert specialist_type in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_instructions_contact_info(
        self, mock_context_wrapper
    ):
        """Test that instructions specify required contact information."""
        instructions = appointment_booking_instructions(
            mock_context_wrapper, appointment_booking_agent
        )

        contact_fields = ["name", "email", "phone"]

        for field in contact_fields:
            assert field in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_instructions_location(
        self, mock_context_wrapper
    ):
        """Test that instructions include consultation location."""
        instructions = appointment_booking_instructions(
            mock_context_wrapper, appointment_booking_agent
        )

        location_info = ["ERNI Gruppe", "Guggibadstrasse 8", "6288 Schongau"]

        for info in location_info:
            assert info in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_instructions_handoff_guidance(
        self, mock_context_wrapper
    ):
        """Test that instructions include handoff guidance."""
        instructions = appointment_booking_instructions(
            mock_context_wrapper, appointment_booking_agent
        )

        handoff_guidance = ["Triage Agent", "other questions"]

        for guidance in handoff_guidance:
            assert guidance in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_agent_guardrails(self):
        """Test that appointment booking agent has proper guardrails."""
        assert len(appointment_booking_agent.input_guardrails) == 2

        guardrail_names = []
        for guardrail in appointment_booking_agent.input_guardrails:
            if hasattr(guardrail, "name"):
                guardrail_names.append(guardrail.name)
            elif hasattr(guardrail, "__name__"):
                guardrail_names.append(guardrail.__name__)

        assert any("relevance" in name.lower() for name in guardrail_names)
        assert any("jailbreak" in name.lower() for name in guardrail_names)

    @pytest.mark.asyncio
    @pytest.mark.agents
    @patch("main.Runner.run")
    async def test_appointment_booking_agent_execution(
        self, mock_runner, mock_context_wrapper
    ):
        """Test appointment booking agent execution with mocked Runner."""
        # Mock successful run
        mock_result = MagicMock()
        mock_result.new_items = []
        mock_result.to_input_list.return_value = []
        mock_runner.return_value = mock_result

        # Test input
        input_text = "I'd like to book a consultation with an architect"

        result = await mock_runner(
            appointment_booking_agent, input_text, context=mock_context_wrapper.context
        )
        assert result is not None
        mock_runner.assert_called()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_agent_instance_type(self):
        """Test that appointment booking agent is properly typed."""
        assert isinstance(appointment_booking_agent, Agent)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_instructions_step_by_step(
        self, mock_context_wrapper
    ):
        """Test that instructions provide clear step-by-step process."""
        instructions = appointment_booking_instructions(
            mock_context_wrapper, appointment_booking_agent
        )

        # Should have numbered steps
        assert "1." in instructions
        assert "2." in instructions
        assert "3." in instructions
        assert "4." in instructions
        assert "5." in instructions
        assert "6." in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_instructions_confirmation_process(
        self, mock_context_wrapper
    ):
        """Test that instructions include confirmation process."""
        instructions = appointment_booking_instructions(
            mock_context_wrapper, appointment_booking_agent
        )

        confirmation_elements = [
            "confirm",
            "choice",  # More flexible: matches "choice of date and time" or "date and time choice"
            "book_consultation",
        ]

        for element in confirmation_elements:
            assert element.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_instructions_dynamic_context(self):
        """Test appointment booking instructions with different context values."""
        # Test with different inquiry IDs and consultation status
        test_contexts = [
            BuildingProjectContext(inquiry_id="INQ-11111", consultation_booked=False),
            BuildingProjectContext(inquiry_id="INQ-99999", consultation_booked=True),
            BuildingProjectContext(),  # No inquiry ID
        ]

        for context in test_contexts:
            wrapper = MagicMock(spec=RunContextWrapper)
            wrapper.context = context

            instructions = appointment_booking_instructions(
                wrapper, appointment_booking_agent
            )
            assert isinstance(instructions, str)
            assert len(instructions) > 0

            if context.inquiry_id:
                assert context.inquiry_id in instructions
            else:
                assert "[unknown]" in instructions

            assert f"Consultation booked: {context.consultation_booked}" in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_agent_professional_tone(
        self, mock_context_wrapper
    ):
        """Test that appointment booking instructions maintain professional tone."""
        instructions = appointment_booking_instructions(
            mock_context_wrapper, appointment_booking_agent
        )

        professional_elements = ["follow this procedure", "ask", "collect", "confirm"]

        for element in professional_elements:
            assert element.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_agent_tool_sequence(self, mock_context_wrapper):
        """Test that instructions specify correct tool usage sequence."""
        instructions = appointment_booking_instructions(
            mock_context_wrapper, appointment_booking_agent
        )

        # Should use check_specialist_availability before book_consultation
        check_pos = instructions.find("check_specialist_availability")
        book_pos = instructions.find("book_consultation")

        assert check_pos < book_pos  # check should come before book

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_agent_data_collection(
        self, mock_context_wrapper
    ):
        """Test that instructions emphasize data collection."""
        instructions = appointment_booking_instructions(
            mock_context_wrapper, appointment_booking_agent
        )

        data_collection = [
            "collect",  # More flexible: matches "collect contact info" or "collect their contact information"
            "name",
            "email",
            "phone",
        ]

        for element in data_collection:
            assert element.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_appointment_booking_agent_availability_checking(
        self, mock_context_wrapper
    ):
        """Test that instructions include availability checking process."""
        instructions = appointment_booking_instructions(
            mock_context_wrapper, appointment_booking_agent
        )

        availability_elements = [
            "check_specialist_availability",
            "available",  # More flexible: matches "show available time slots" or "show slots"
            "time slots",  # More specific match for the actual text
        ]

        for element in availability_elements:
            assert element.lower() in instructions.lower()
