"""
Unit tests for FAQ lookup tool functionality.

Tests the REAL faq_lookup_building_impl function from main.py.
"""

import pytest

from main import faq_lookup_building_impl


class TestFAQLookupBuilding:
    """Test cases for the FAQ lookup building tool."""

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_faq_lookup_wood_materials(self):
        """Test FAQ lookup for wood/timber materials."""
        wood_questions = [
            "Why should I choose wood?",
            "What about timber construction?",
            "Tell me about wood materials",
            "holz advantages",
            "timber benefits",
        ]

        for question in wood_questions:
            # Call the test function
            result = await faq_lookup_building_impl(question)

            assert isinstance(result, str)
            assert "🌲 Why Wood?" in result
            assert "Ecological and renewable" in result
            assert "Swiss forests" in result
            assert "thermal insulation" in result
            assert "Minergie partner" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_faq_lookup_construction_timeline(self):
        """Test FAQ lookup for construction timeline questions using REAL function."""
        # REAL function checks for: "zeit", "time", "dauer", "duration", "срок"
        timeline_questions = [
            "How much time does construction take?",
            "What is the construction time?",
            "zeit for building",
            "construction duration",
            "how long time needed",
        ]

        for question in timeline_questions:
            result = await faq_lookup_building_impl(question)

            assert isinstance(result, str)
            assert "⏱️ Construction Timeline:" in result
            # REAL function format
            assert "Planning: 2-3 months" in result
            assert "Production: 4-6 weeks" in result
            assert "Assembly: 2-4 weeks" in result
            assert "6-9 months" in result
            assert "single-family house" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_faq_lookup_minergie_certification(self):
        """Test FAQ lookup for Minergie certification questions using REAL function."""
        # REAL function checks for: "minergie", "certificate", "zertifikat"
        certification_questions = [
            "What is Minergie?",
            "Tell me about certificate",
            "ERNI certificates",
            "zertifikat information",
        ]

        for question in certification_questions:
            result = await faq_lookup_building_impl(question)

            assert isinstance(result, str)
            assert "🏆 ERNI Certifications:" in result
            assert "Minergie-Fachpartner" in result
            assert "Holzbau Plus" in result
            # REAL function format
            assert "energy efficiency" in result
            assert "80% less energy" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_faq_lookup_warranty_information(self):
        """Test FAQ lookup for warranty questions using REAL function."""
        warranty_questions = [
            "What warranty do you offer?",
            "garantie information",
            "warranty terms",
        ]

        for question in warranty_questions:
            result = await faq_lookup_building_impl(question)

            assert isinstance(result, str)
            assert "🛡️ ERNI Warranties:" in result
            # REAL function format
            assert "Construction warranty: 5 years" in result
            assert "Roof warranty: 5 years" in result
            assert "Windows/doors warranty: 2 years" in result
            assert "Dachservice" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_faq_lookup_pricing_information(self):
        """Test FAQ lookup for pricing questions using REAL function."""
        # REAL function checks for: "preis", "cost", "price", "kosten"
        pricing_questions = [
            "How much does it cost?",
            "What is the price?",
            "kosten estimation",
            "preis per square meter",
        ]

        for question in pricing_questions:
            result = await faq_lookup_building_impl(question)

            assert isinstance(result, str)
            # REAL function format
            assert "💰 Pricing:" in result
            assert "detailed cost estimate" in result
            assert "Project type" in result
            assert "Area in m²" in result
            assert "Construction type" in result
            assert "preliminary estimate" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_faq_lookup_services_information(self):
        """Test FAQ lookup for services questions using REAL function."""
        services_questions = [
            "What services do you offer?",
            "ERNI services",
            "wartung and maintenance",
        ]

        for question in services_questions:
            result = await faq_lookup_building_impl(question)

            assert isinstance(result, str)
            # REAL function uses 🔧 not 🏗️
            assert "🔧 ERNI Services:" in result
            assert "Planning & Architecture" in result
            assert "Timber Construction (Holzbau)" in result
            assert "Roofing & Sheet Metal Work (Spenglerei)" in result
            assert "Interior Finishing (Ausbau)" in result
            assert "General/Total Contracting (Realisation)" in result
            assert "Agricultural Buildings (Agrar)" in result
            assert "Everything under one roof!" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_faq_lookup_unknown_question(self):
        """Test FAQ lookup for unknown/unmatched questions using REAL function."""
        unknown_questions = [
            "What is the meaning of life?",
            "How to cook pasta?",
            "Weather forecast",
            "Random question",
            "Unrelated topic",
        ]

        for question in unknown_questions:
            result = await faq_lookup_building_impl(question)

            assert isinstance(result, str)
            # REAL function format
            assert (
                "I'm sorry, I don't have an answer to that specific question" in result
            )
            assert "speak with one of our consultants" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_faq_lookup_case_insensitive(self):
        """Test that FAQ lookup is case insensitive using REAL function."""
        test_cases = [
            ("WOOD", "🌲 Why Wood?"),
            ("Wood", "🌲 Why Wood?"),
            ("wood", "🌲 Why Wood?"),
            ("HOLZ", "🌲 Why Wood?"),
            ("Holz", "🌲 Why Wood?"),
            ("MINERGIE", "🏆 ERNI Certifications:"),
            ("Minergie", "🏆 ERNI Certifications:"),
            ("TIME", "⏱️ Construction Timeline:"),
            ("Zeit", "⏱️ Construction Timeline:"),
        ]

        for question, expected_start in test_cases:
            result = await faq_lookup_building_impl(question)
            assert expected_start in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_faq_lookup_empty_input(self):
        """Test FAQ lookup with empty input using REAL function."""
        result = await faq_lookup_building_impl("")

        assert isinstance(result, str)
        # REAL function format
        assert "I'm sorry, I don't have an answer to that specific question" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_faq_lookup_whitespace_input(self):
        """Test FAQ lookup with whitespace-only input using REAL function."""
        result = await faq_lookup_building_impl("   ")

        assert isinstance(result, str)
        # REAL function format
        assert "I'm sorry, I don't have an answer to that specific question" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_faq_lookup_partial_matches(self):
        """Test FAQ lookup with partial keyword matches using REAL function."""
        # REAL function checks specific keywords, not general terms
        partial_matches = [
            ("wood construction benefits", "🌲 Why Wood?"),
            ("construction time estimate", "⏱️ Construction Timeline:"),
            ("warranty and guarantee info", "🛡️ ERNI Warranties:"),
            ("service offerings", "🔧 ERNI Services:"),  # REAL function uses 🔧
            (
                "certificate standards",
                "🏆 ERNI Certifications:",
            ),  # Must contain "certificate"
            (
                "cost and pricing",
                "💰 Pricing:",
            ),  # REAL function uses "Pricing:" not "Pricing Information:"
        ]

        for question, expected_start in partial_matches:
            result = await faq_lookup_building_impl(question)
            assert expected_start in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_faq_lookup_multilingual_keywords(self):
        """Test FAQ lookup with German and English keywords using REAL function."""
        multilingual_tests = [
            ("holz material", "🌲 Why Wood?"),
            ("wood material", "🌲 Why Wood?"),
            ("zeit duration", "⏱️ Construction Timeline:"),
            ("time duration", "⏱️ Construction Timeline:"),
            ("garantie warranty", "🛡️ ERNI Warranties:"),
            ("preis cost", "💰 Pricing:"),  # REAL function uses "Pricing:"
            ("kosten price", "💰 Pricing:"),  # REAL function uses "Pricing:"
        ]

        for question, expected_start in multilingual_tests:
            result = await faq_lookup_building_impl(question)
            assert expected_start in result
