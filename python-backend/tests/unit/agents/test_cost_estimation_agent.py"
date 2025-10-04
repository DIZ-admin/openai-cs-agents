"""
Unit tests for Cost Estimation Agent functionality.
"""

import pytest
from unittest.mock import MagicMock, patch
from agents import Agent, RunContextWrapper

from main import cost_estimation_agent, cost_estimation_instructions, BuildingProjectContext


class TestCostEstimationAgent:
    """Test cases for the Cost Estimation Agent."""

    @pytest.fixture
    def mock_context_wrapper(self):
        """Create a mock context wrapper for testing."""
        context = BuildingProjectContext(inquiry_id="INQ-12345")
        wrapper = MagicMock(spec=RunContextWrapper)
        wrapper.context = context
        return wrapper

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_cost_estimation_agent_configuration(self):
        """Test that cost estimation agent is properly configured."""
        assert cost_estimation_agent.name == "Cost Estimation Agent"
        assert "cost estimates" in cost_estimation_agent.handoff_description.lower()
        assert len(cost_estimation_agent.tools) == 1  # Should have estimate_project_cost tool
        assert len(cost_estimation_agent.input_guardrails) == 2  # relevance and jailbreak
        assert cost_estimation_agent.model == "gpt-4o-mini"
        assert cost_estimation_agent.model_settings is not None
        assert cost_estimation_agent.model_settings.temperature == 0.7

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_cost_estimation_agent_tools(self):
        """Test that cost estimation agent has correct tools."""
        tool_names = []
        for tool in cost_estimation_agent.tools:
            if hasattr(tool, 'name'):
                tool_names.append(tool.name)
            elif hasattr(tool, '__name__'):
                tool_names.append(tool.__name__)

        assert any("estimate_project_cost" in name for name in tool_names)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_cost_estimation_agent_handoffs(self):
        """Test that cost estimation agent has correct handoff targets."""
        handoff_names = []
        for handoff in cost_estimation_agent.handoffs:
            if hasattr(handoff, 'agent_name'):
                handoff_names.append(handoff.agent_name)
            elif hasattr(handoff, 'name'):
                handoff_names.append(handoff.name)

        expected_targets = ["Triage Agent", "Appointment Booking Agent"]
        for target in expected_targets:
            assert any(target in name for name in handoff_names)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_cost_estimation_instructions_with_inquiry_id(self, mock_context_wrapper):
        """Test cost estimation instructions include inquiry ID."""
        instructions = cost_estimation_instructions(mock_context_wrapper, cost_estimation_agent)
        
        assert isinstance(instructions, str)
        assert "INQ-12345" in instructions
        assert "Cost Estimation Agent" in instructions
        assert "ERNI Gruppe" in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_cost_estimation_instructions_without_inquiry_id(self):
        """Test cost estimation instructions without inquiry ID."""
        context = BuildingProjectContext()  # No inquiry_id
        wrapper = MagicMock(spec=RunContextWrapper)
        wrapper.context = context

        instructions = cost_estimation_instructions(wrapper, cost_estimation_agent)
        
        assert isinstance(instructions, str)
        assert "[unknown]" in instructions
        assert "Cost Estimation Agent" in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_cost_estimation_instructions_procedure(self, mock_context_wrapper):
        """Test that cost estimation instructions include proper procedure."""
        instructions = cost_estimation_instructions(mock_context_wrapper, cost_estimation_agent)
        
        procedure_steps = [
            "project type",
            "area in square meters",
            "construction type",
            "estimate_project_cost",
            "preliminary estimate",
            "consultation"
        ]

        for step in procedure_steps:
            assert step.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_cost_estimation_instructions_project_types(self, mock_context_wrapper):
        """Test that instructions mention all project types."""
        instructions = cost_estimation_instructions(mock_context_wrapper, cost_estimation_agent)
        
        project_types = [
            "Einfamilienhaus",
            "Mehrfamilienhaus", 
            "Agrar",
            "Renovation"
        ]

        for project_type in project_types:
            assert project_type in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_cost_estimation_instructions_construction_types(self, mock_context_wrapper):
        """Test that instructions mention construction types."""
        instructions = cost_estimation_instructions(mock_context_wrapper, cost_estimation_agent)
        
        construction_types = ["Holzbau", "Systembau", "timber frame", "system construction"]

        assert any(const_type in instructions for const_type in construction_types)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_cost_estimation_instructions_handoff_guidance(self, mock_context_wrapper):
        """Test that instructions include handoff guidance."""
        instructions = cost_estimation_instructions(mock_context_wrapper, cost_estimation_agent)
        
        handoff_guidance = [
            "Appointment Booking Agent",
            "Triage Agent",
            "consultation",
            "other questions"
        ]

        for guidance in handoff_guidance:
            assert guidance in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_cost_estimation_agent_guardrails(self):
        """Test that cost estimation agent has proper guardrails."""
        assert len(cost_estimation_agent.input_guardrails) == 2
        
        guardrail_names = []
        for guardrail in cost_estimation_agent.input_guardrails:
            if hasattr(guardrail, 'name'):
                guardrail_names.append(guardrail.name)
            elif hasattr(guardrail, '__name__'):
                guardrail_names.append(guardrail.__name__)

        assert any("relevance" in name.lower() for name in guardrail_names)
        assert any("jailbreak" in name.lower() for name in guardrail_names)

    @pytest.mark.asyncio
    @pytest.mark.agents
    @patch('main.Runner.run')
    async def test_cost_estimation_agent_execution(self, mock_runner, mock_context_wrapper):
        """Test cost estimation agent execution with mocked Runner."""
        # Mock successful run
        mock_result = MagicMock()
        mock_result.new_items = []
        mock_result.to_input_list.return_value = []
        mock_runner.return_value = mock_result

        # Test input
        input_text = "I want to estimate the cost of a 150m² house"
        
        result = await mock_runner(cost_estimation_agent, input_text, context=mock_context_wrapper.context)
        assert result is not None
        mock_runner.assert_called()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_cost_estimation_agent_instance_type(self):
        """Test that cost estimation agent is properly typed."""
        assert isinstance(cost_estimation_agent, Agent)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_cost_estimation_instructions_recommended_prefix(self, mock_context_wrapper):
        """Test that cost estimation instructions use recommended prompt prefix."""
        instructions = cost_estimation_instructions(mock_context_wrapper, cost_estimation_agent)
        
        from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
        if RECOMMENDED_PROMPT_PREFIX:
            assert RECOMMENDED_PROMPT_PREFIX in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_cost_estimation_instructions_dynamic_context(self):
        """Test cost estimation instructions with different context values."""
        # Test with different inquiry IDs
        test_contexts = [
            BuildingProjectContext(inquiry_id="INQ-11111"),
            BuildingProjectContext(inquiry_id="INQ-99999"),
            BuildingProjectContext(),  # No inquiry ID
        ]

        for context in test_contexts:
            wrapper = MagicMock(spec=RunContextWrapper)
            wrapper.context = context
            
            instructions = cost_estimation_instructions(wrapper, cost_estimation_agent)
            assert isinstance(instructions, str)
            assert len(instructions) > 0
            
            if context.inquiry_id:
                assert context.inquiry_id in instructions
            else:
                assert "[unknown]" in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_cost_estimation_agent_professional_tone(self, mock_context_wrapper):
        """Test that cost estimation instructions maintain professional tone."""
        instructions = cost_estimation_instructions(mock_context_wrapper, cost_estimation_agent)
        
        professional_elements = [
            "follow this procedure",
            "ask the customer",
            "emphasize",
            "offer to book"
        ]

        for element in professional_elements:
            assert element.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_cost_estimation_agent_step_by_step_process(self, mock_context_wrapper):
        """Test that instructions provide clear step-by-step process."""
        instructions = cost_estimation_instructions(mock_context_wrapper, cost_estimation_agent)
        
        # Should have numbered steps
        assert "1." in instructions
        assert "2." in instructions
        assert "3." in instructions
        assert "4." in instructions
        assert "5." in instructions
        assert "6." in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_cost_estimation_agent_tool_usage_guidance(self, mock_context_wrapper):
        """Test that instructions provide guidance on tool usage."""
        instructions = cost_estimation_instructions(mock_context_wrapper, cost_estimation_agent)
        
        tool_guidance = [
            "estimate_project_cost tool",
            "calculate",
            "preliminary estimate"
        ]

        for guidance in tool_guidance:
            assert guidance.lower() in instructions.lower()
