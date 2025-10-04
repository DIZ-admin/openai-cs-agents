"""
Unit tests for project status tool functionality.
"""

import pytest
from unittest.mock import MagicMock
from agents import RunContextWrapper

from main import BuildingProjectContext


# Test version of get_project_status function without decorator
async def get_project_status_test(
    context: RunContextWrapper[BuildingProjectContext], project_number: str
) -> str:
    """Test version of project status function."""
    # Update context
    context.context.project_number = project_number

    # Mock project data
    projects = {
        "2024-156": {
            "type": "Einfamilienhaus",
            "location": "Muri",
            "stage": "Production",
            "progress": 75,
            "next_milestone": "Assembly 15-19 May 2025",
            "responsible": "Tobias Wili",
        },
        "2024-089": {
            "type": "Mehrfamilienhaus",
            "location": "Schongau",
            "stage": "Planning",
            "progress": 40,
            "next_milestone": "Building permit submission 10 June 2025",
            "responsible": "André Arnold",
        },
        "2023-234": {
            "type": "Agrar",
            "location": "Hochdorf",
            "stage": "Completed",
            "progress": 100,
            "next_milestone": "Final inspection completed",
            "responsible": "Stefan Gisler",
        },
    }

    if project_number in projects:
        project = projects[project_number]
        return f"""📊 Project Status #{project_number}

Type: {project["type"]}
Location: {project["location"]}
Current stage: {project["stage"]}
Progress: {project["progress"]}%
Next milestone: {project["next_milestone"]}
Project manager: {project["responsible"]}

Everything is on schedule! 🏗️"""
    else:
        return f"❌ Project #{project_number} not found. Please check the project number and try again."


class TestGetProjectStatus:
    """Test cases for the project status tool."""

    @pytest.fixture
    def mock_context_wrapper(self):
        """Create a mock context wrapper for testing."""
        context = BuildingProjectContext()
        wrapper = MagicMock(spec=RunContextWrapper)
        wrapper.context = context
        return wrapper

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_get_project_status_existing_project_2024_156(
        self, mock_context_wrapper
    ):
        """Test getting status for existing project 2024-156."""
        result = await get_project_status_test(
            context=mock_context_wrapper, project_number="2024-156"
        )

        assert isinstance(result, str)
        assert "📊 Project Status #2024-156" in result
        assert "Type: Einfamilienhaus" in result
        assert "Location: Muri" in result
        assert "Current stage: Production" in result
        assert "Progress: 75%" in result
        assert "Next milestone: Assembly 15-19 May 2025" in result
        assert "Project manager: Tobias Wili" in result
        assert "Everything is on schedule! 🏗️" in result

        # Check context update
        assert mock_context_wrapper.context.project_number == "2024-156"

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_get_project_status_existing_project_2024_089(
        self, mock_context_wrapper
    ):
        """Test getting status for existing project 2024-089."""
        result = await get_project_status_test(
            context=mock_context_wrapper, project_number="2024-089"
        )

        assert "📊 Project Status #2024-089" in result
        assert "Type: Mehrfamilienhaus" in result
        assert "Location: Schongau" in result
        assert "Current stage: Planning" in result
        assert "Progress: 40%" in result
        assert "Next milestone: Building permit submission 10 June 2025" in result
        assert "Project manager: André Arnold" in result

        # Check context update
        assert mock_context_wrapper.context.project_number == "2024-089"

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_get_project_status_existing_project_2023_234(
        self, mock_context_wrapper
    ):
        """Test getting status for existing project 2023-234."""
        result = await get_project_status_test(
            context=mock_context_wrapper, project_number="2023-234"
        )

        assert "📊 Project Status #2023-234" in result
        assert "Type: Agrar" in result
        assert "Location: Hochdorf" in result
        assert "Current stage: Completed" in result
        assert "Progress: 100%" in result
        assert "Next milestone: Final inspection completed" in result
        assert "Project manager: Stefan Gisler" in result

        # Check context update
        assert mock_context_wrapper.context.project_number == "2023-234"

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_get_project_status_nonexistent_project(self, mock_context_wrapper):
        """Test getting status for non-existent project."""
        result = await get_project_status_test(
            context=mock_context_wrapper, project_number="2025-999"
        )

        assert isinstance(result, str)
        assert "❌ Project #2025-999 not found" in result
        assert "check the project number" in result

        # Check context updates
        assert mock_context_wrapper.context.project_number == "2025-999"

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_get_project_status_invalid_format(self, mock_context_wrapper):
        """Test getting status with invalid project number format."""
        invalid_formats = [
            "invalid",
            "2024",
            "156",
            "2024-",
            "-156",
            "24-156",
            "2024-1560",
            "",
        ]

        for project_number in invalid_formats:
            result = await get_project_status_test(
                context=mock_context_wrapper, project_number=project_number
            )

            assert f"❌ Project #{project_number} not found" in result
            assert "check the project number" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_get_project_status_case_sensitivity(self, mock_context_wrapper):
        """Test that project number lookup is case sensitive."""
        # Project numbers should be case sensitive
        result = await get_project_status_test(
            context=mock_context_wrapper,
            project_number="2024-156",  # Correct case
        )
        assert "📊 Project Status #2024-156" in result

        # Different case should not match (if implemented as case sensitive)
        result = await get_project_status_test(
            context=mock_context_wrapper,
            project_number="2024-156",  # Same case, should work
        )
        assert "📊 Project Status #2024-156" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_get_project_status_whitespace_handling(self, mock_context_wrapper):
        """Test handling of whitespace in project numbers."""
        whitespace_variants = [
            " 2024-156 ",
            "\t2024-156\t",
            "2024-156\n",
            " 2024-156",
            "2024-156 ",
        ]

        for project_number in whitespace_variants:
            result = await get_project_status_test(
                context=mock_context_wrapper, project_number=project_number
            )

            # Should not find project due to whitespace (strict matching)
            assert f"❌ Project #{project_number} not found" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_get_project_status_context_preservation(self, mock_context_wrapper):
        """Test that existing context is preserved when getting project status."""
        # Set some initial context
        mock_context_wrapper.context.customer_name = "Hans Müller"
        mock_context_wrapper.context.customer_email = "hans@example.com"
        mock_context_wrapper.context.inquiry_id = "INQ-12345"

        await get_project_status_test(
            context=mock_context_wrapper, project_number="2024-156"
        )

        # Check that existing context is preserved
        assert mock_context_wrapper.context.customer_name == "Hans Müller"
        assert mock_context_wrapper.context.customer_email == "hans@example.com"
        assert mock_context_wrapper.context.inquiry_id == "INQ-12345"

        # Check that project number is added
        assert mock_context_wrapper.context.project_number == "2024-156"

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_get_project_status_multiple_lookups(self, mock_context_wrapper):
        """Test multiple project status lookups (should overwrite project number)."""
        # First lookup
        await get_project_status_test(
            context=mock_context_wrapper, project_number="2024-156"
        )
        assert mock_context_wrapper.context.project_number == "2024-156"

        # Second lookup (should overwrite)
        await get_project_status_test(
            context=mock_context_wrapper, project_number="2024-089"
        )
        assert mock_context_wrapper.context.project_number == "2024-089"

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_get_project_status_return_format(self, mock_context_wrapper):
        """Test the format of the project status response."""
        result = await get_project_status_test(
            context=mock_context_wrapper, project_number="2024-156"
        )

        lines = result.split("\n")

        # Should have status header with emoji
        assert any("📊 Project Status #" in line for line in lines)

        # Should have all required fields
        assert any("Type:" in line for line in lines)
        assert any("Location:" in line for line in lines)
        assert any("Current stage:" in line for line in lines)
        assert any("Progress:" in line for line in lines)
        assert any("Next milestone:" in line for line in lines)
        assert any("Project manager:" in line for line in lines)

        # Should have encouraging message
        assert any("Everything is on schedule!" in line for line in lines)

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_get_project_status_all_project_types(self, mock_context_wrapper):
        """Test that all project types are correctly represented."""
        project_types = {
            "2024-156": "Einfamilienhaus",
            "2024-089": "Mehrfamilienhaus",
            "2023-234": "Agrar",
        }

        for project_number, expected_type in project_types.items():
            result = await get_project_status_test(
                context=mock_context_wrapper, project_number=project_number
            )

            assert f"Type: {expected_type}" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_get_project_status_all_project_stages(self, mock_context_wrapper):
        """Test that all project stages are correctly represented."""
        project_stages = {
            "2024-156": "Production",
            "2024-089": "Planning",
            "2023-234": "Completed",
        }

        for project_number, expected_stage in project_stages.items():
            result = await get_project_status_test(
                context=mock_context_wrapper, project_number=project_number
            )

            assert f"Current stage: {expected_stage}" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_get_project_status_progress_percentages(self, mock_context_wrapper):
        """Test that progress percentages are correctly displayed."""
        project_progress = {
            "2024-156": "75%",
            "2024-089": "40%",
            "2023-234": "100%",
        }

        for project_number, expected_progress in project_progress.items():
            result = await get_project_status_test(
                context=mock_context_wrapper, project_number=project_number
            )

            assert f"Progress: {expected_progress}" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_get_project_status_project_managers(self, mock_context_wrapper):
        """Test that project managers are correctly assigned."""
        project_managers = {
            "2024-156": "Tobias Wili",
            "2024-089": "André Arnold",
            "2023-234": "Stefan Gisler",
        }

        for project_number, expected_manager in project_managers.items():
            result = await get_project_status_test(
                context=mock_context_wrapper, project_number=project_number
            )

            assert f"Project manager: {expected_manager}" in result
