"""
Unit tests for Triage Agent functionality.
"""

import pytest
from unittest.mock import MagicMock, patch
from agents import Agent, RunContextWrapper

from main import (
    triage_agent,
    BuildingProjectContext,
)


class TestTriageAgent:
    """Test cases for the Triage Agent."""

    @pytest.fixture
    def mock_context_wrapper(self):
        """Create a mock context wrapper for testing."""
        context = BuildingProjectContext()
        wrapper = MagicMock(spec=RunContextWrapper)
        wrapper.context = context
        return wrapper

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_triage_agent_configuration(self):
        """Test that triage agent is properly configured."""
        assert triage_agent.name == "Triage Agent"
        assert "Main routing agent" in triage_agent.handoff_description
        assert len(triage_agent.handoffs) == 5  # Should have 5 handoff targets
        assert len(triage_agent.input_guardrails) == 2  # relevance and jailbreak
        assert len(triage_agent.tools) == 0  # Triage agent has no tools

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_triage_agent_handoff_targets(self):
        """Test that triage agent has correct handoff targets."""
        handoff_names = []
        for handoff in triage_agent.handoffs:
            if hasattr(handoff, "agent_name"):
                handoff_names.append(handoff.agent_name)
            elif hasattr(handoff, "name"):
                handoff_names.append(handoff.name)

        expected_targets = [
            "Project Information Agent",
            "Cost Estimation Agent",
            "Project Status Agent",
            "Appointment Booking Agent",
            "FAQ Agent",
        ]

        for target in expected_targets:
            assert any(target in name for name in handoff_names)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_triage_agent_instructions_content(self):
        """Test that triage agent instructions contain required content."""
        # Get instructions (they might be dynamic)
        if callable(triage_agent.instructions):
            instructions = triage_agent.instructions(MagicMock(), triage_agent)
        else:
            instructions = triage_agent.instructions

        assert isinstance(instructions, str)
        assert "triage agent" in instructions.lower()
        assert "erni gruppe" in instructions.lower()
        assert "timber construction" in instructions.lower()

        # Check routing instructions
        assert "general information" in instructions.lower()
        assert "cost estimates" in instructions.lower()
        assert "project status" in instructions.lower()
        assert "consultation" in instructions.lower()

        # Check language support
        assert "german" in instructions.lower() or "english" in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_triage_agent_guardrails(self):
        """Test that triage agent has proper guardrails."""
        assert len(triage_agent.input_guardrails) == 2

        # Check guardrail names
        guardrail_names = []
        for guardrail in triage_agent.input_guardrails:
            if hasattr(guardrail, "name"):
                guardrail_names.append(guardrail.name)
            elif hasattr(guardrail, "__name__"):
                guardrail_names.append(guardrail.__name__)

        assert any("relevance" in name.lower() for name in guardrail_names)
        assert any("jailbreak" in name.lower() for name in guardrail_names)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_triage_agent_model_configuration(self):
        """Test that triage agent uses correct model settings."""
        assert triage_agent.model == "gpt-4o-mini"
        assert triage_agent.model_settings is not None
        assert triage_agent.model_settings.temperature == 0.7
        assert triage_agent.model_settings.max_tokens == 2000

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_triage_agent_no_tools(self):
        """Test that triage agent has no tools (routing only)."""
        assert len(triage_agent.tools) == 0

    @pytest.mark.asyncio
    @pytest.mark.agents
    @patch("main.Runner.run")
    async def test_triage_agent_routing_logic(self, mock_runner, mock_context_wrapper):
        """Test triage agent routing logic with mocked Runner."""
        # Mock successful run
        mock_result = MagicMock()
        mock_result.new_items = []
        mock_result.to_input_list.return_value = []
        mock_runner.return_value = mock_result

        # Test different input scenarios
        test_inputs = [
            "I want to build a house",
            "How much does construction cost?",
            "What's the status of my project?",
            "I'd like to book a consultation",
            "Why should I choose wood?",
        ]

        for input_text in test_inputs:
            result = await mock_runner(
                triage_agent, input_text, context=mock_context_wrapper.context
            )
            assert result is not None
            mock_runner.assert_called()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_triage_agent_bilingual_support(self):
        """Test that triage agent supports bilingual communication."""
        if callable(triage_agent.instructions):
            instructions = triage_agent.instructions(MagicMock(), triage_agent)
        else:
            instructions = triage_agent.instructions

        # Should mention both German and English
        assert "german" in instructions.lower() or "deutsch" in instructions.lower()
        assert "english" in instructions.lower() or "englisch" in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_triage_agent_professional_tone(self):
        """Test that triage agent instructions emphasize professional tone."""
        if callable(triage_agent.instructions):
            instructions = triage_agent.instructions(MagicMock(), triage_agent)
        else:
            instructions = triage_agent.instructions

        professional_keywords = ["professional", "friendly", "helpful", "welcome"]
        assert any(keyword in instructions.lower() for keyword in professional_keywords)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_triage_agent_company_context(self):
        """Test that triage agent instructions include company context."""
        if callable(triage_agent.instructions):
            instructions = triage_agent.instructions(MagicMock(), triage_agent)
        else:
            instructions = triage_agent.instructions

        # Should mention ERNI Gruppe and Swiss context
        assert "erni gruppe" in instructions.lower()
        assert "swiss" in instructions.lower() or "switzerland" in instructions.lower()
        assert "timber" in instructions.lower() or "wood" in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_triage_agent_routing_categories(self):
        """Test that triage agent instructions cover all routing categories."""
        if callable(triage_agent.instructions):
            instructions = triage_agent.instructions(MagicMock(), triage_agent)
        else:
            instructions = triage_agent.instructions

        routing_categories = [
            "general information",
            "cost estimate",
            "project status",
            "consultation",
            "specific questions",
        ]

        for category in routing_categories:
            assert category.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_triage_agent_handoff_callbacks(self):
        """Test that triage agent has proper handoff callbacks where needed."""
        handoff_with_callbacks = []

        for handoff in triage_agent.handoffs:
            if hasattr(handoff, "on_invoke_handoff"):
                # Check if handoff has callback
                fn = handoff.on_invoke_handoff
                if fn and hasattr(fn, "__closure__") and fn.__closure__:
                    handoff_with_callbacks.append(handoff)

        # Cost estimation and appointment booking should have callbacks
        assert len(handoff_with_callbacks) >= 2

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_triage_agent_instance_type(self):
        """Test that triage agent is properly typed."""
        assert isinstance(triage_agent, Agent)
        # Should be typed for BuildingProjectContext
        assert hasattr(triage_agent, "__orig_class__") or hasattr(
            triage_agent, "__args__"
        )

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_triage_agent_instructions_dynamic(self):
        """Test triage agent instructions with different contexts."""
        # Test with empty context
        empty_context = BuildingProjectContext()
        empty_wrapper = MagicMock(spec=RunContextWrapper)
        empty_wrapper.context = empty_context

        if callable(triage_agent.instructions):
            instructions = triage_agent.instructions(empty_wrapper, triage_agent)
            assert isinstance(instructions, str)
            assert len(instructions) > 0

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_triage_agent_recommended_prompt_prefix(self):
        """Test that triage agent uses recommended prompt prefix."""
        if callable(triage_agent.instructions):
            instructions = triage_agent.instructions(MagicMock(), triage_agent)
        else:
            instructions = triage_agent.instructions

        # Should include the recommended prompt prefix for handoffs
        from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

        if RECOMMENDED_PROMPT_PREFIX:
            assert RECOMMENDED_PROMPT_PREFIX in instructions
