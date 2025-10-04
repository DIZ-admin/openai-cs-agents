"""
Unit tests for cost estimation tool functionality.

Tests the REAL estimate_project_cost_impl function from main.py.
"""

import pytest
from unittest.mock import MagicMock
from agents import RunContextWrapper

from main import estimate_project_cost_impl, BuildingProjectContext


class TestEstimateProjectCost:
    """Test cases for the cost estimation tool."""

    @pytest.fixture
    def mock_context_wrapper(self):
        """Create a mock context wrapper for testing."""
        context = BuildingProjectContext()
        wrapper = MagicMock(spec=RunContextWrapper)
        wrapper.context = context
        return wrapper

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_estimate_einfamilienhaus_holzbau(self, mock_context_wrapper):
        """Test cost estimation for single-family house with timber construction using REAL function."""
        result = await estimate_project_cost_impl(
            context=mock_context_wrapper,
            project_type="Einfamilienhaus",
            area_sqm=150.0,
            construction_type="Holzbau"
        )

        # Check result format (REAL function output)
        assert isinstance(result, str)
        assert "📊 Preliminary Cost Estimate for Einfamilienhaus (150.0 m²):" in result
        assert "Construction type: Holzbau" in result
        assert "Price per m²: CHF 3000" in result  # No comma in real function
        assert "CHF 450,000 - 562,500" in result
        assert "preliminary estimate" in result
        assert "consultation with our architect" in result  # Real function says "architect" not "specialists"

        # Check context updates
        assert mock_context_wrapper.context.project_type == "Einfamilienhaus"
        assert mock_context_wrapper.context.construction_type == "Holzbau"
        assert mock_context_wrapper.context.area_sqm == 150.0
        assert mock_context_wrapper.context.budget_chf == 450000.0

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_estimate_einfamilienhaus_systembau(self, mock_context_wrapper):
        """Test cost estimation for single-family house with system construction using REAL function."""
        result = await estimate_project_cost_impl(
            context=mock_context_wrapper,
            project_type="Einfamilienhaus",
            area_sqm=200.0,
            construction_type="Systembau"
        )

        assert "Construction type: Systembau" in result
        assert "Price per m²: CHF 2500" in result  # No comma
        assert "CHF 500,000 - 625,000" in result

        # Check context updates
        assert mock_context_wrapper.context.project_type == "Einfamilienhaus"
        assert mock_context_wrapper.context.construction_type == "Systembau"
        assert mock_context_wrapper.context.area_sqm == 200.0
        assert mock_context_wrapper.context.budget_chf == 500000.0

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_estimate_mehrfamilienhaus_holzbau(self, mock_context_wrapper):
        """Test cost estimation for multi-family house with timber construction using REAL function."""
        result = await estimate_project_cost_impl(
            context=mock_context_wrapper,
            project_type="Mehrfamilienhaus",
            area_sqm=300.0,
            construction_type="Holzbau"
        )

        assert "Mehrfamilienhaus (300.0 m²)" in result
        assert "Construction type: Holzbau" in result
        assert "Price per m²: CHF 2800" in result  # No comma
        assert "CHF 840,000 - 1,050,000" in result

        # Check context updates
        assert mock_context_wrapper.context.project_type == "Mehrfamilienhaus"
        assert mock_context_wrapper.context.construction_type == "Holzbau"
        assert mock_context_wrapper.context.area_sqm == 300.0
        assert mock_context_wrapper.context.budget_chf == 840000.0

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_estimate_agrar_building(self, mock_context_wrapper):
        """Test cost estimation for agricultural building using REAL function."""
        result = await estimate_project_cost_impl(
            context=mock_context_wrapper,
            project_type="Agrar",
            area_sqm=500.0,
            construction_type="Holzbau"
        )

        assert "Agrar (500.0 m²)" in result
        assert "Construction type: Holzbau" in result
        assert "Price per m²: CHF 2000" in result  # No comma
        assert "CHF 1,000,000 - 1,250,000" in result

        # Check context updates
        assert mock_context_wrapper.context.project_type == "Agrar"
        assert mock_context_wrapper.context.construction_type == "Holzbau"
        assert mock_context_wrapper.context.area_sqm == 500.0
        assert mock_context_wrapper.context.budget_chf == 1000000.0

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_estimate_renovation_project(self, mock_context_wrapper):
        """Test cost estimation for renovation project using REAL function."""
        result = await estimate_project_cost_impl(
            context=mock_context_wrapper,
            project_type="Renovation",
            area_sqm=100.0,
            construction_type="Systembau"
        )

        assert "Renovation (100.0 m²)" in result
        assert "Construction type: Systembau" in result
        assert "Price per m²: CHF 1200" in result  # No comma
        assert "CHF 120,000 - 150,000" in result

        # Check context updates
        assert mock_context_wrapper.context.project_type == "Renovation"
        assert mock_context_wrapper.context.construction_type == "Systembau"
        assert mock_context_wrapper.context.area_sqm == 100.0
        assert mock_context_wrapper.context.budget_chf == 120000.0

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_estimate_unknown_project_type(self, mock_context_wrapper):
        """Test cost estimation with unknown project type using REAL function."""
        result = await estimate_project_cost_impl(
            context=mock_context_wrapper,
            project_type="UnknownType",
            area_sqm=150.0,
            construction_type="Holzbau"
        )

        # Should return error message (REAL function format)
        assert "❌ Unknown project type: 'UnknownType'" in result
        assert "Valid project types are:" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_estimate_unknown_construction_type(self, mock_context_wrapper):
        """Test cost estimation with unknown construction type using REAL function."""
        result = await estimate_project_cost_impl(
            context=mock_context_wrapper,
            project_type="Einfamilienhaus",
            area_sqm=150.0,
            construction_type="UnknownType"
        )

        # Should return error message (REAL function format)
        assert "❌ Unknown construction type: 'UnknownType'" in result
        assert "Valid construction types for Einfamilienhaus are:" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_estimate_small_area(self, mock_context_wrapper):
        """Test cost estimation with small area."""
        result = await estimate_project_cost_impl(
            context=mock_context_wrapper,
            project_type="Einfamilienhaus",
            area_sqm=50.0,
            construction_type="Holzbau"
        )

        assert "Einfamilienhaus (50.0 m²)" in result
        assert "CHF 150,000 - 187,500" in result

        # Check context updates
        assert mock_context_wrapper.context.area_sqm == 50.0
        assert mock_context_wrapper.context.budget_chf == 150000.0

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_estimate_large_area(self, mock_context_wrapper):
        """Test cost estimation with large area."""
        result = await estimate_project_cost_impl(
            context=mock_context_wrapper,
            project_type="Mehrfamilienhaus",
            area_sqm=1000.0,
            construction_type="Systembau"
        )

        assert "Mehrfamilienhaus (1000.0 m²)" in result
        assert "CHF 2,300,000 - 2,875,000" in result

        # Check context updates
        assert mock_context_wrapper.context.area_sqm == 1000.0
        assert mock_context_wrapper.context.budget_chf == 2300000.0

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_estimate_decimal_area(self, mock_context_wrapper):
        """Test cost estimation with decimal area."""
        result = await estimate_project_cost_impl(
            context=mock_context_wrapper,
            project_type="Einfamilienhaus",
            area_sqm=175.5,
            construction_type="Holzbau"
        )

        assert "Einfamilienhaus (175.5 m²)" in result
        # 175.5 * 3000 = 526,500
        assert "CHF 526,500 - 658,125" in result

        # Check context updates
        assert mock_context_wrapper.context.area_sqm == 175.5
        assert mock_context_wrapper.context.budget_chf == 526500.0

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_estimate_price_calculation_accuracy(self, mock_context_wrapper):
        """Test accuracy of price calculations."""
        test_cases = [
            # (project_type, construction_type, area, expected_base_price, expected_min, expected_max)
            ("Einfamilienhaus", "Holzbau", 100.0, 3000, 300000, 375000),
            ("Einfamilienhaus", "Systembau", 100.0, 2500, 250000, 312500),
            ("Mehrfamilienhaus", "Holzbau", 100.0, 2800, 280000, 350000),
            ("Mehrfamilienhaus", "Systembau", 100.0, 2300, 230000, 287500),
            ("Agrar", "Holzbau", 100.0, 2000, 200000, 250000),
            ("Agrar", "Systembau", 100.0, 1800, 180000, 225000),
            ("Renovation", "Holzbau", 100.0, 1500, 150000, 187500),
            ("Renovation", "Systembau", 100.0, 1200, 120000, 150000),
        ]

        for project_type, construction_type, area, expected_price, expected_min, expected_max in test_cases:
            result = await estimate_project_cost_impl(
                context=mock_context_wrapper,
                project_type=project_type,
                area_sqm=area,
                construction_type=construction_type
            )

            # REAL function doesn't use comma in price_per_sqm
            assert f"Price per m²: CHF {expected_price}" in result
            assert f"CHF {expected_min:,.0f} - {expected_max:,.0f}" in result
            assert mock_context_wrapper.context.budget_chf == expected_min

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_estimate_context_preservation(self, mock_context_wrapper):
        """Test that existing context is preserved and only relevant fields are updated."""
        # Set some initial context
        mock_context_wrapper.context.customer_name = "Hans Müller"
        mock_context_wrapper.context.customer_email = "hans@example.com"
        mock_context_wrapper.context.inquiry_id = "INQ-12345"

        await estimate_project_cost_impl(
            context=mock_context_wrapper,
            project_type="Einfamilienhaus",
            area_sqm=150.0,
            construction_type="Holzbau"
        )

        # Check that existing context is preserved
        assert mock_context_wrapper.context.customer_name == "Hans Müller"
        assert mock_context_wrapper.context.customer_email == "hans@example.com"
        assert mock_context_wrapper.context.inquiry_id == "INQ-12345"

        # Check that new context is added
        assert mock_context_wrapper.context.project_type == "Einfamilienhaus"
        assert mock_context_wrapper.context.construction_type == "Holzbau"
        assert mock_context_wrapper.context.area_sqm == 150.0
        assert mock_context_wrapper.context.budget_chf == 450000.0

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_estimate_zero_area(self, mock_context_wrapper):
        """Test cost estimation with zero area using REAL function."""
        result = await estimate_project_cost_impl(
            context=mock_context_wrapper,
            project_type="Einfamilienhaus",
            area_sqm=0.0,
            construction_type="Holzbau"
        )

        # Should return error message for zero area (REAL function format)
        assert "❌ Invalid area: Area must be greater than 0 m²" in result
        assert "Please provide a valid project area" in result
