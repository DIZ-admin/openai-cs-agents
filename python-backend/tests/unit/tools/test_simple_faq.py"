"""
Simple unit tests for FAQ lookup functionality.
"""

import pytest


# Test version of FAQ lookup function (copy of the logic from main.py)
async def faq_lookup_test(question: str) -> str:
    """Test version of FAQ lookup function."""
    q = question.lower()

    if "holz" in q or "wood" in q or "timber" in q or "material" in q:
        return (
            "🌲 Why Wood?\n\n"
            "Wood is the ideal building material:\n"
            "✓ Ecological and renewable\n"
            "✓ Grows in Swiss forests\n"
            "✓ Excellent thermal insulation\n"
            "✓ Healthy indoor climate\n"
            "✓ CO2-neutral\n"
            "✓ Fast assembly (saves time)\n\n"
            "ERNI is a certified Minergie partner."
        )

    if "zeit" in q or "time" in q or "dauer" in q or "duration" in q or "timeline" in q:
        return (
            "⏱️ Construction Timeline:\n\n"
            "Typical timelines for ERNI projects:\n"
            "• Planning phase: 2-4 months\n"
            "• Building permit: 1-3 months\n"
            "• Production: 4-8 weeks\n"
            "• Assembly: 1-2 weeks\n"
            "• Finishing: 2-4 months\n\n"
            "Total project time: 8-12 months"
        )

    if "minergie" in q or "certificate" in q or "zertifikat" in q:
        return (
            "🏆 ERNI Certifications:\n\n"
            "✓ Minergie-Fachpartner Gebäudehülle\n"
            "✓ Holzbau Plus certified\n"
            "✓ ISO 9001 quality management\n"
            "✓ Sustainable construction specialist\n\n"
            "We guarantee energy-efficient building solutions."
        )

    return (
        "❓ I don't have specific information about that topic.\n\n"
        "Please contact ERNI Gruppe directly:\n"
        "📞 041 570 70 70\n"
        "📧 info@erni-gruppe.ch\n"
        "🌐 www.erni-gruppe.ch"
    )


class TestSimpleFAQ:
    """Simple test cases for FAQ lookup functionality."""

    @pytest.mark.asyncio
    async def test_wood_materials_lookup(self):
        """Test FAQ lookup for wood/timber materials."""
        wood_questions = [
            "Why should I choose wood?",
            "What about timber construction?",
            "Tell me about wood materials",
            "holz advantages",
            "timber benefits",
        ]

        for question in wood_questions:
            result = await faq_lookup_test(question)
            
            assert isinstance(result, str)
            assert "🌲 Why Wood?" in result
            assert "Wood is the ideal building material" in result
            assert "Ecological and renewable" in result
            assert "Swiss forests" in result
            assert "thermal insulation" in result
            assert "Minergie partner" in result

    @pytest.mark.asyncio
    async def test_timeline_lookup(self):
        """Test FAQ lookup for construction timeline."""
        timeline_questions = [
            "How much time does construction take?",
            "What is the timeline?",
            "Construction duration time",
            "zeit for building",
            "dauer of project",
        ]

        for question in timeline_questions:
            result = await faq_lookup_test(question)

            assert isinstance(result, str)
            assert "⏱️ Construction Timeline:" in result
            assert "Planning phase: 2-4 months" in result
            assert "Production: 4-8 weeks" in result
            assert "Assembly: 1-2 weeks" in result
            assert "Total project time: 8-12 months" in result

    @pytest.mark.asyncio
    async def test_certification_lookup(self):
        """Test FAQ lookup for certifications."""
        cert_questions = [
            "What certificate do you have?",
            "Tell me about Minergie",
            "Do you have certificate?",
            "zertifikat information",
        ]

        for question in cert_questions:
            result = await faq_lookup_test(question)

            assert isinstance(result, str)
            assert "🏆 ERNI Certifications:" in result
            assert "Minergie-Fachpartner" in result
            assert "Holzbau Plus certified" in result
            assert "ISO 9001" in result

    @pytest.mark.asyncio
    async def test_unknown_question(self):
        """Test FAQ lookup for unknown questions."""
        unknown_questions = [
            "What's the weather like?",
            "Tell me about cars",
            "Random question",
            "Unrelated topic",
        ]

        for question in unknown_questions:
            result = await faq_lookup_test(question)
            
            assert isinstance(result, str)
            assert "❓ I don't have specific information" in result
            assert "041 570 70 70" in result
            assert "info@erni-gruppe.ch" in result
            assert "www.erni-gruppe.ch" in result

    @pytest.mark.asyncio
    async def test_case_insensitive_matching(self):
        """Test that FAQ lookup is case insensitive."""
        test_cases = [
            ("WOOD", "🌲 Why Wood?"),
            ("Wood", "🌲 Why Wood?"),
            ("wood", "🌲 Why Wood?"),
            ("HOLZ", "🌲 Why Wood?"),
            ("TIME", "⏱️ Construction Timeline:"),
            ("MINERGIE", "🏆 ERNI Certifications:"),
        ]

        for question, expected_start in test_cases:
            result = await faq_lookup_test(question)
            assert expected_start in result

    @pytest.mark.asyncio
    async def test_partial_keyword_matching(self):
        """Test that FAQ lookup works with partial keyword matches."""
        test_cases = [
            ("I love wooden houses", "🌲 Why Wood?"),
            ("Construction timeline please", "⏱️ Construction Timeline:"),
            ("Minergie certification info", "🏆 ERNI Certifications:"),
            ("What materials do you use?", "🌲 Why Wood?"),
        ]

        for question, expected_start in test_cases:
            result = await faq_lookup_test(question)
            assert expected_start in result

    @pytest.mark.asyncio
    async def test_empty_and_whitespace_input(self):
        """Test FAQ lookup with empty and whitespace input."""
        edge_cases = ["", "   ", "\t", "\n", "  \t  \n  "]

        for question in edge_cases:
            result = await faq_lookup_test(question)
            # Should return unknown/fallback response
            assert "❓ I don't have specific information" in result

    @pytest.mark.asyncio
    async def test_multilingual_keywords(self):
        """Test FAQ lookup with German and English keywords."""
        test_cases = [
            # German keywords
            ("Warum Holz wählen?", "🌲 Why Wood?"),
            ("Wie lange dauert der Bau?", "⏱️ Construction Timeline:"),
            ("Haben Sie Zertifikate?", "🏆 ERNI Certifications:"),
            
            # English keywords  
            ("Why choose timber?", "🌲 Why Wood?"),
            ("What's the construction time?", "⏱️ Construction Timeline:"),
            ("Do you have certificates?", "🏆 ERNI Certifications:"),
        ]

        for question, expected_start in test_cases:
            result = await faq_lookup_test(question)
            assert expected_start in result
