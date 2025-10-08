"""
Unit tests for PII output guardrail.

Tests the PII detection guardrail configuration and integration.
"""

import pytest
from agents import OutputGuardrail

from main import (
    pii_guardrail,
    triage_agent,
    project_information_agent,
    cost_estimation_agent,
    project_status_agent,
    appointment_booking_agent,
    faq_agent,
)


class TestPIIGuardrail:
    """Test suite for PII output guardrail configuration."""

    @pytest.mark.unit
    @pytest.mark.guardrails
    def test_pii_guardrail_is_output_guardrail(self):
        """Test that pii_guardrail is an OutputGuardrail instance."""
        assert isinstance(pii_guardrail, OutputGuardrail)

    @pytest.mark.unit
    @pytest.mark.guardrails
    def test_pii_guardrail_has_name(self):
        """Test that PII guardrail has a name."""
        assert hasattr(pii_guardrail, "name")
        assert pii_guardrail.name == "PII Guardrail"

    @pytest.mark.unit
    @pytest.mark.guardrails
    def test_all_agents_have_pii_guardrail(self):
        """Test that all agents have PII output guardrail configured."""
        agents = [
            triage_agent,
            project_information_agent,
            cost_estimation_agent,
            project_status_agent,
            appointment_booking_agent,
            faq_agent,
        ]

        for agent in agents:
            assert hasattr(agent, "output_guardrails"), f"{agent.name} missing output_guardrails"
            assert len(agent.output_guardrails) > 0, f"{agent.name} has no output guardrails"

            # Check that PII guardrail is in the list
            guardrail_names = [
                getattr(g, "name", str(g)) for g in agent.output_guardrails
            ]
            assert "PII Guardrail" in guardrail_names, (
                f"{agent.name} missing PII Guardrail. "
                f"Has: {guardrail_names}"
            )

    @pytest.mark.unit
    @pytest.mark.guardrails
    def test_pii_guardrail_configuration(self):
        """Test PII guardrail configuration details."""
        # Verify it's an output guardrail (not input)
        assert isinstance(pii_guardrail, OutputGuardrail)

        # Verify it has a guardrail function
        assert hasattr(pii_guardrail, "guardrail_function")
        assert callable(pii_guardrail.guardrail_function)

    @pytest.mark.unit
    @pytest.mark.guardrails
    def test_pii_guardrail_consistency_across_agents(self):
        """Test that all agents use the same PII guardrail instance."""
        agents = [
            triage_agent,
            project_information_agent,
            cost_estimation_agent,
            project_status_agent,
            appointment_booking_agent,
            faq_agent,
        ]

        # Get PII guardrail from first agent
        first_pii_guardrail = None
        for g in agents[0].output_guardrails:
            if getattr(g, "name", "") == "PII Guardrail":
                first_pii_guardrail = g
                break

        assert first_pii_guardrail is not None

        # Verify all other agents use the same instance
        for agent in agents[1:]:
            agent_pii_guardrail = None
            for g in agent.output_guardrails:
                if getattr(g, "name", "") == "PII Guardrail":
                    agent_pii_guardrail = g
                    break

            assert agent_pii_guardrail is not None
            assert agent_pii_guardrail is first_pii_guardrail, (
                f"{agent.name} uses different PII guardrail instance"
            )

