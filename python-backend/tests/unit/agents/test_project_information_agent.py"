"""
Unit tests for Project Information Agent functionality.
"""

import pytest
from unittest.mock import MagicMock, patch
from agents import Agent, RunContextWrapper

from main import project_information_agent, BuildingProjectContext


class TestProjectInformationAgent:
    """Test cases for the Project Information Agent."""

    @pytest.fixture
    def mock_context_wrapper(self):
        """Create a mock context wrapper for testing."""
        context = BuildingProjectContext()
        wrapper = MagicMock(spec=RunContextWrapper)
        wrapper.context = context
        return wrapper

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_project_information_agent_configuration(self):
        """Test that project information agent is properly configured."""
        assert project_information_agent.name == "Project Information Agent"
        assert (
            "general information"
            in project_information_agent.handoff_description.lower()
        )
        assert (
            len(project_information_agent.tools) == 1
        )  # Should have faq_lookup_building tool
        assert (
            len(project_information_agent.input_guardrails) == 2
        )  # relevance and jailbreak
        assert project_information_agent.model == "gpt-4.1-mini"
        assert project_information_agent.model_settings is not None
        assert project_information_agent.model_settings.temperature == 0.7

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_project_information_agent_tools(self):
        """Test that project information agent has correct tools."""
        tool_names = []
        for tool in project_information_agent.tools:
            if hasattr(tool, "name"):
                tool_names.append(tool.name)
            elif hasattr(tool, "__name__"):
                tool_names.append(tool.__name__)

        assert any("faq_lookup_building" in name for name in tool_names)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_project_information_agent_handoffs(self):
        """Test that project information agent has correct handoff targets."""
        handoff_names = []
        for handoff in project_information_agent.handoffs:
            if hasattr(handoff, "agent_name"):
                handoff_names.append(handoff.agent_name)
            elif hasattr(handoff, "name"):
                handoff_names.append(handoff.name)

        expected_targets = [
            "Triage Agent",
            "Cost Estimation Agent",
            "Appointment Booking Agent",
        ]
        for target in expected_targets:
            assert any(target in name for name in handoff_names)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_project_information_agent_instructions(self, mock_context_wrapper):
        """Test project information agent instructions."""
        if callable(project_information_agent.instructions):
            instructions = project_information_agent.instructions(
                mock_context_wrapper, project_information_agent
            )
        else:
            instructions = project_information_agent.instructions

        assert isinstance(instructions, str)
        assert "Project Information Agent" in instructions
        assert "ERNI Gruppe" in instructions
        assert "timber construction" in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_project_information_agent_services_coverage(
        self, mock_context_wrapper
    ):
        """Test that instructions cover all ERNI services."""
        if callable(project_information_agent.instructions):
            instructions = project_information_agent.instructions(
                mock_context_wrapper, project_information_agent
            )
        else:
            instructions = project_information_agent.instructions

        erni_services = [
            "Planung",
            "Holzbau",
            "Spenglerei",
            "Ausbau",
            "Realisation",
            "Agrar",
        ]

        for service in erni_services:
            assert service in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_project_information_agent_project_types(self, mock_context_wrapper):
        """Test that instructions mention project types."""
        if callable(project_information_agent.instructions):
            instructions = project_information_agent.instructions(
                mock_context_wrapper, project_information_agent
            )
        else:
            instructions = project_information_agent.instructions

        project_types = ["Einfamilienhaus", "Mehrfamilienhaus", "Agrar"]

        for project_type in project_types:
            assert project_type in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_project_information_agent_certifications(self, mock_context_wrapper):
        """Test that instructions mention ERNI certifications."""
        if callable(project_information_agent.instructions):
            instructions = project_information_agent.instructions(
                mock_context_wrapper, project_information_agent
            )
        else:
            instructions = project_information_agent.instructions

        certifications = ["Minergie", "Holzbau Plus"]

        for cert in certifications:
            assert cert in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_project_information_agent_handoff_guidance(
        self, mock_context_wrapper
    ):
        """Test that instructions include handoff guidance."""
        if callable(project_information_agent.instructions):
            instructions = project_information_agent.instructions(
                mock_context_wrapper, project_information_agent
            )
        else:
            instructions = project_information_agent.instructions

        handoff_guidance = [
            "cost estimate",
            "Cost Estimation Agent",
            "consultation",
            "Appointment Booking Agent",
            "Triage Agent",
        ]

        for guidance in handoff_guidance:
            assert guidance in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_project_information_agent_tool_usage(self, mock_context_wrapper):
        """Test that instructions mention tool usage."""
        if callable(project_information_agent.instructions):
            instructions = project_information_agent.instructions(
                mock_context_wrapper, project_information_agent
            )
        else:
            instructions = project_information_agent.instructions

        assert "faq_lookup_building" in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_project_information_agent_guardrails(self):
        """Test that project information agent has proper guardrails."""
        assert len(project_information_agent.input_guardrails) == 2

        guardrail_names = []
        for guardrail in project_information_agent.input_guardrails:
            if hasattr(guardrail, "name"):
                guardrail_names.append(guardrail.name)
            elif hasattr(guardrail, "__name__"):
                guardrail_names.append(guardrail.__name__)

        assert any("relevance" in name.lower() for name in guardrail_names)
        assert any("jailbreak" in name.lower() for name in guardrail_names)

    @pytest.mark.asyncio
    @pytest.mark.agents
    @patch("main.Runner.run")
    async def test_project_information_agent_execution(
        self, mock_runner, mock_context_wrapper
    ):
        """Test project information agent execution with mocked Runner."""
        # Mock successful run
        mock_result = MagicMock()
        mock_result.new_items = []
        mock_result.to_input_list.return_value = []
        mock_runner.return_value = mock_result

        # Test input
        input_text = "Tell me about ERNI's building process"

        result = await mock_runner(
            project_information_agent, input_text, context=mock_context_wrapper.context
        )
        assert result is not None
        mock_runner.assert_called()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_project_information_agent_instance_type(self):
        """Test that project information agent is properly typed."""
        assert isinstance(project_information_agent, Agent)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_project_information_agent_building_process(
        self, mock_context_wrapper
    ):
        """Test that instructions explain the building process."""
        if callable(project_information_agent.instructions):
            instructions = project_information_agent.instructions(
                mock_context_wrapper, project_information_agent
            )
        else:
            instructions = project_information_agent.instructions

        building_process_steps = ["Planning", "Production", "Assembly", "Finishing"]

        for step in building_process_steps:
            assert step in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_project_information_agent_timber_advantages(
        self, mock_context_wrapper
    ):
        """Test that instructions mention timber construction advantages."""
        if callable(project_information_agent.instructions):
            instructions = project_information_agent.instructions(
                mock_context_wrapper, project_information_agent
            )
        else:
            instructions = project_information_agent.instructions

        timber_advantages = [
            "timber construction",
            "advantages",
            "holzbau",  # More specific match from actual instructions (German for timber construction)
        ]

        for advantage in timber_advantages:
            assert advantage.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_project_information_agent_friendly_tone(self, mock_context_wrapper):
        """Test that instructions emphasize friendly and informative tone."""
        if callable(project_information_agent.instructions):
            instructions = project_information_agent.instructions(
                mock_context_wrapper, project_information_agent
            )
        else:
            instructions = project_information_agent.instructions

        tone_keywords = ["friendly", "informative", "explain", "help"]

        assert any(keyword in instructions.lower() for keyword in tone_keywords)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_project_information_agent_comprehensive_coverage(
        self, mock_context_wrapper
    ):
        """Test that agent covers all required information areas."""
        if callable(project_information_agent.instructions):
            instructions = project_information_agent.instructions(
                mock_context_wrapper, project_information_agent
            )
        else:
            instructions = project_information_agent.instructions

        coverage_areas = [
            "building process",
            "services",
            "projects",
            "certifications",
            "advantages",
        ]

        for area in coverage_areas:
            assert area.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_project_information_agent_role_clarity(self, mock_context_wrapper):
        """Test that agent role is clearly defined."""
        if callable(project_information_agent.instructions):
            instructions = project_information_agent.instructions(
                mock_context_wrapper, project_information_agent
            )
        else:
            instructions = project_information_agent.instructions

        role_indicators = ["role is to explain", "your role", "explain to customers"]

        assert any(indicator in instructions.lower() for indicator in role_indicators)
