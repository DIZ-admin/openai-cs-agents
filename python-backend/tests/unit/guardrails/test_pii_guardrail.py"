"""
Unit tests for PII output guardrail.

Tests the PII detection guardrail that prevents exposure of sensitive
personally identifiable information in agent responses.
"""

import pytest
from agents import Agent, RunContextWrapper

from main import pii_guardrail, BuildingProjectContext


class TestPIIGuardrail:
    """Test suite for PII output guardrail."""

    @pytest.mark.asyncio
    @pytest.mark.guardrails
    async def test_pii_guardrail_safe_response(self):
        """Test that safe responses pass the PII guardrail."""
        # Create mock context
        context = RunContextWrapper(context=BuildingProjectContext())
        
        # Create mock agent
        agent = Agent(name="Test Agent", instructions="Test")
        
        # Safe response with only company information
        safe_output = (
            "ERNI Gruppe is located at Guggibadstrasse 8, 6288 Schongau. "
            "You can reach us at 041 570 70 70 or info@erni-gruppe.ch."
        )
        
        # Run guardrail
        result = await pii_guardrail(context, agent, safe_output)
        
        # Should pass (tripwire not triggered)
        assert result.tripwire_triggered is False
        assert result.output_info.contains_pii is False

    @pytest.mark.asyncio
    @pytest.mark.guardrails
    async def test_pii_guardrail_detects_email(self):
        """Test that personal email addresses are detected."""
        context = RunContextWrapper(context=BuildingProjectContext())
        agent = Agent(name="Test Agent", instructions="Test")
        
        # Response with personal email
        unsafe_output = (
            "Your consultation is confirmed. "
            "We'll send details to john.smith@gmail.com."
        )
        
        result = await pii_guardrail(context, agent, unsafe_output)
        
        # Should fail (tripwire triggered)
        assert result.tripwire_triggered is True
        assert result.output_info.contains_pii is True

    @pytest.mark.asyncio
    @pytest.mark.guardrails
    async def test_pii_guardrail_detects_phone(self):
        """Test that personal phone numbers are detected."""
        context = RunContextWrapper(context=BuildingProjectContext())
        agent = Agent(name="Test Agent", instructions="Test")
        
        # Response with personal phone number
        unsafe_output = (
            "Your project manager will call you at +41 79 123 4567."
        )
        
        result = await pii_guardrail(context, agent, unsafe_output)
        
        # Should fail (tripwire triggered)
        assert result.tripwire_triggered is True
        assert result.output_info.contains_pii is True

    @pytest.mark.asyncio
    @pytest.mark.guardrails
    async def test_pii_guardrail_allows_company_contact(self):
        """Test that company contact information is allowed."""
        context = RunContextWrapper(context=BuildingProjectContext())
        agent = Agent(name="Test Agent", instructions="Test")
        
        # Response with only company contact info
        safe_output = (
            "Contact ERNI Gruppe:\n"
            "Phone: 041 570 70 70\n"
            "Email: info@erni-gruppe.ch\n"
            "Address: Guggibadstrasse 8, 6288 Schongau"
        )
        
        result = await pii_guardrail(context, agent, safe_output)
        
        # Should pass
        assert result.tripwire_triggered is False
        assert result.output_info.contains_pii is False

    @pytest.mark.asyncio
    @pytest.mark.guardrails
    async def test_pii_guardrail_detects_credit_card(self):
        """Test that credit card numbers are detected."""
        context = RunContextWrapper(context=BuildingProjectContext())
        agent = Agent(name="Test Agent", instructions="Test")
        
        # Response with credit card number
        unsafe_output = (
            "Please use card 4532-1234-5678-9010 for payment."
        )
        
        result = await pii_guardrail(context, agent, unsafe_output)
        
        # Should fail
        assert result.tripwire_triggered is True
        assert result.output_info.contains_pii is True

