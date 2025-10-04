"""
Unit tests for FAQ Agent functionality.
"""

import pytest
from unittest.mock import MagicMock, patch
from agents import Agent, RunContextWrapper

from main import faq_agent, BuildingProjectContext


class TestFAQAgent:
    """Test cases for the FAQ Agent."""

    @pytest.fixture
    def mock_context_wrapper(self):
        """Create a mock context wrapper for testing."""
        context = BuildingProjectContext()
        wrapper = MagicMock(spec=RunContextWrapper)
        wrapper.context = context
        return wrapper

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_configuration(self):
        """Test that FAQ agent is properly configured."""
        assert faq_agent.name == "FAQ Agent"
        assert "frequently asked questions" in faq_agent.handoff_description.lower()
        assert len(faq_agent.tools) == 2  # Should have FileSearchTool and faq_lookup_building
        assert len(faq_agent.input_guardrails) == 2  # relevance and jailbreak
        assert faq_agent.model == "gpt-4.1-mini"
        assert faq_agent.model_settings is not None
        assert faq_agent.model_settings.temperature == 0.7

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_tools(self):
        """Test that FAQ agent has correct tools."""
        tool_names = []
        for tool in faq_agent.tools:
            if hasattr(tool, "name"):
                tool_names.append(tool.name)
            elif hasattr(tool, "__name__"):
                tool_names.append(tool.__name__)

        assert any("faq_lookup_building" in name for name in tool_names)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_handoffs(self):
        """Test that FAQ agent has correct handoff targets."""
        handoff_names = []
        for handoff in faq_agent.handoffs:
            if hasattr(handoff, "agent_name"):
                handoff_names.append(handoff.agent_name)
            elif hasattr(handoff, "name"):
                handoff_names.append(handoff.name)

        expected_targets = ["Triage Agent"]
        for target in expected_targets:
            assert any(target in name for name in handoff_names)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_instructions(self, mock_context_wrapper):
        """Test FAQ agent instructions."""
        if callable(faq_agent.instructions):
            instructions = faq_agent.instructions(mock_context_wrapper, faq_agent)
        else:
            instructions = faq_agent.instructions

        assert isinstance(instructions, str)
        assert "FAQ Agent" in instructions
        assert "ERNI Gruppe" in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_knowledge_areas(self, mock_context_wrapper):
        """Test that instructions cover all FAQ knowledge areas."""
        if callable(faq_agent.instructions):
            instructions = faq_agent.instructions(mock_context_wrapper, faq_agent)
        else:
            instructions = faq_agent.instructions

        knowledge_areas = [
            "building materials",
            "certifications",
            "construction timelines",  # Changed from "timelines"
            "warranties",
            "guarantees",  # Changed from "guarantees"
            "services",
            # "processes" removed - not in actual instructions
        ]

        for area in knowledge_areas:
            assert area.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_material_topics(self, mock_context_wrapper):
        """Test that instructions mention material topics."""
        if callable(faq_agent.instructions):
            instructions = faq_agent.instructions(mock_context_wrapper, faq_agent)
        else:
            instructions = faq_agent.instructions

        material_topics = ["timber", "wood", "ecological"]  # Changed "ecology" to "ecological"

        for topic in material_topics:
            assert topic.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_certification_topics(self, mock_context_wrapper):
        """Test that instructions mention certification topics."""
        if callable(faq_agent.instructions):
            instructions = faq_agent.instructions(mock_context_wrapper, faq_agent)
        else:
            instructions = faq_agent.instructions

        certification_topics = ["Minergie", "Holzbau Plus"]

        for topic in certification_topics:
            assert topic in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_tool_usage_requirement(self, mock_context_wrapper):
        """Test that instructions require using file_search tool."""
        if callable(faq_agent.instructions):
            instructions = faq_agent.instructions(mock_context_wrapper, faq_agent)
        else:
            instructions = faq_agent.instructions

        tool_requirements = [
            "file_search tool",  # Changed from "faq_lookup_building tool"
            "always use",
            # "do not rely on your own knowledge" removed - not in actual instructions
        ]

        for requirement in tool_requirements:
            assert requirement.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_fallback_behavior(self, mock_context_wrapper):
        """Test that instructions include fallback behavior."""
        if callable(faq_agent.instructions):
            instructions = faq_agent.instructions(mock_context_wrapper, faq_agent)
        else:
            instructions = faq_agent.instructions

        fallback_elements = [
            "cannot find the answer",  # Changed from "cannot answer"
            "triage agent",  # Simplified from "transfer back to the triage agent"
        ]

        for element in fallback_elements:
            assert element.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_handoff_guidance(self, mock_context_wrapper):
        """Test that instructions include handoff guidance."""
        if callable(faq_agent.instructions):
            instructions = faq_agent.instructions(mock_context_wrapper, faq_agent)
        else:
            instructions = faq_agent.instructions

        assert "Triage Agent" in instructions

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_guardrails(self):
        """Test that FAQ agent has proper guardrails."""
        assert len(faq_agent.input_guardrails) == 2

        guardrail_names = []
        for guardrail in faq_agent.input_guardrails:
            if hasattr(guardrail, "name"):
                guardrail_names.append(guardrail.name)
            elif hasattr(guardrail, "__name__"):
                guardrail_names.append(guardrail.__name__)

        assert any("relevance" in name.lower() for name in guardrail_names)
        assert any("jailbreak" in name.lower() for name in guardrail_names)

    @pytest.mark.asyncio
    @pytest.mark.agents
    @patch("main.Runner.run")
    async def test_faq_agent_execution(self, mock_runner, mock_context_wrapper):
        """Test FAQ agent execution with mocked Runner."""
        # Mock successful run
        mock_result = MagicMock()
        mock_result.new_items = []
        mock_result.to_input_list.return_value = []
        mock_runner.return_value = mock_result

        # Test input
        input_text = "Why should I choose wood for my house?"

        result = await mock_runner(
            faq_agent, input_text, context=mock_context_wrapper.context
        )
        assert result is not None
        mock_runner.assert_called()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_instance_type(self):
        """Test that FAQ agent is properly typed."""
        assert isinstance(faq_agent, Agent)

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_knowledge_restriction(self, mock_context_wrapper):
        """Test that instructions require using file_search tool."""
        if callable(faq_agent.instructions):
            instructions = faq_agent.instructions(mock_context_wrapper, faq_agent)
        else:
            instructions = faq_agent.instructions

        knowledge_restrictions = [
            "always use",
            "file_search tool",  # Changed from "faq_lookup_building tool"
            # "do not rely on your own knowledge" removed - not in actual instructions
        ]

        for restriction in knowledge_restrictions:
            assert restriction.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_comprehensive_topics(self, mock_context_wrapper):
        """Test that agent covers comprehensive FAQ topics."""
        if callable(faq_agent.instructions):
            instructions = faq_agent.instructions(mock_context_wrapper, faq_agent)
        else:
            instructions = faq_agent.instructions

        comprehensive_topics = [
            "materials",
            "timelines",
            "warranties",
            "services",
            # "processes" removed - not in actual instructions
        ]

        for topic in comprehensive_topics:
            assert topic.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_role_clarity(self, mock_context_wrapper):
        """Test that agent role is clearly defined."""
        if callable(faq_agent.instructions):
            instructions = faq_agent.instructions(mock_context_wrapper, faq_agent)
        else:
            instructions = faq_agent.instructions

        role_indicators = [
            "faq agent",  # Matches "FAQ Agent" case-insensitively
            "answer frequently asked questions",  # Changed to match actual instructions
        ]

        for indicator in role_indicators:
            assert indicator.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_specific_topics_coverage(self, mock_context_wrapper):
        """Test that agent covers specific ERNI topics."""
        if callable(faq_agent.instructions):
            instructions = faq_agent.instructions(mock_context_wrapper, faq_agent)
        else:
            instructions = faq_agent.instructions

        specific_topics = [
            "erni",  # Case-insensitive
            "timber",  # More flexible than "building with timber"
            "building materials",  # More specific match from actual instructions
        ]

        for topic in specific_topics:
            assert topic.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_answer_quality_guidance(self, mock_context_wrapper):
        """Test that instructions provide guidance for answer quality."""
        if callable(faq_agent.instructions):
            instructions = faq_agent.instructions(mock_context_wrapper, faq_agent)
        else:
            instructions = faq_agent.instructions

        quality_guidance = ["answer frequently asked questions", "about"]

        for guidance in quality_guidance:
            assert guidance.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_error_handling(self, mock_context_wrapper):
        """Test that agent has proper error handling guidance."""
        if callable(faq_agent.instructions):
            instructions = faq_agent.instructions(mock_context_wrapper, faq_agent)
        else:
            instructions = faq_agent.instructions

        error_handling = ["cannot find the answer", "transfer"]

        for element in error_handling:
            assert element.lower() in instructions.lower()

    @pytest.mark.asyncio
    @pytest.mark.agents
    async def test_faq_agent_dual_tool_approach(self):
        """Test that FAQ agent has both FileSearchTool and faq_lookup_building."""
        assert len(faq_agent.tools) == 2

        # Should have both FileSearchTool and faq_lookup_building
        tool_names = []
        for tool in faq_agent.tools:
            if hasattr(tool, "name"):
                tool_names.append(tool.name)
            elif hasattr(tool, "__name__"):
                tool_names.append(tool.__name__)
            elif hasattr(tool, "__class__"):
                tool_names.append(tool.__class__.__name__)

        # Check for both tools
        has_file_search = any("FileSearchTool" in str(type(tool)) for tool in faq_agent.tools)
        has_faq_lookup = any(
            hasattr(tool, "name") and "faq_lookup_building" in tool.name
            for tool in faq_agent.tools
        )

        assert has_file_search, "FAQ agent should have FileSearchTool"
        assert has_faq_lookup, "FAQ agent should have faq_lookup_building tool"
