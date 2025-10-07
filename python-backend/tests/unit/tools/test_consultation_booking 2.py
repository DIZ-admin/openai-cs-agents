"""
Unit tests for consultation booking tool functionality.

Tests the REAL book_consultation_impl function from main.py.
"""

import pytest
from unittest.mock import MagicMock
from agents import RunContextWrapper

from main import book_consultation_impl, BuildingProjectContext


class TestBookConsultation:
    """Test cases for the consultation booking tool."""

    @pytest.fixture
    def mock_context_wrapper(self):
        """Create a mock context wrapper for testing."""
        context = BuildingProjectContext()
        wrapper = MagicMock(spec=RunContextWrapper)
        wrapper.context = context
        return wrapper

    @pytest.fixture
    def context_with_customer_info(self):
        """Create a context with customer information."""
        context = BuildingProjectContext(
            customer_name="Hans Müller",
            customer_email="hans.mueller@example.com",
            customer_phone="+41 79 123 45 67",
        )
        wrapper = MagicMock(spec=RunContextWrapper)
        wrapper.context = context
        return wrapper

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_book_consultation_architekt(self, mock_context_wrapper):
        """Test booking consultation with Architekt using REAL function."""
        result = await book_consultation_impl(
            context=mock_context_wrapper,
            specialist_type="Architekt",
            date="Tuesday, May 15",
            time="14:00",
            customer_name="John Doe",
            customer_email="john.doe@example.com",
            customer_phone="+41 79 999 88 77",
        )

        assert isinstance(result, str)
        assert "✅ Consultation Booked!" in result
        assert "Customer: John Doe" in result
        assert "Specialist: Architekt" in result
        assert "Date: Tuesday, May 15" in result
        assert "Time: 14:00" in result
        assert "Location: ERNI Gruppe, Guggibadstrasse 8, 6288 Schongau" in result
        assert "Confirmation sent to john.doe@example.com" in result
        assert "Phone: +41 79 999 88 77" in result
        assert "contact you one day before" in result

        # Check context updates - REAL function saves contact data!
        assert mock_context_wrapper.context.consultation_booked is True
        assert mock_context_wrapper.context.specialist_assigned == "Architekt"
        assert mock_context_wrapper.context.customer_name == "John Doe"
        assert mock_context_wrapper.context.customer_email == "john.doe@example.com"
        assert mock_context_wrapper.context.customer_phone == "+41 79 999 88 77"

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_book_consultation_holzbau_ingenieur(self, mock_context_wrapper):
        """Test booking consultation with Holzbau-Ingenieur using REAL function."""
        result = await book_consultation_impl(
            context=mock_context_wrapper,
            specialist_type="Holzbau-Ingenieur",
            date="Wednesday, May 16",
            time="09:00",
            customer_name="Maria Schmidt",
            customer_email="maria.schmidt@example.com",
            customer_phone="+41 79 888 77 66",
        )

        assert "Specialist: Holzbau-Ingenieur" in result
        assert "Date: Wednesday, May 16" in result
        assert "Time: 09:00" in result
        assert "Customer: Maria Schmidt" in result

        # Check context updates
        assert mock_context_wrapper.context.consultation_booked is True
        assert mock_context_wrapper.context.specialist_assigned == "Holzbau-Ingenieur"
        assert mock_context_wrapper.context.customer_name == "Maria Schmidt"
        assert (
            mock_context_wrapper.context.customer_email == "maria.schmidt@example.com"
        )

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_book_consultation_bauleiter(self, mock_context_wrapper):
        """Test booking consultation with Bauleiter using REAL function."""
        result = await book_consultation_impl(
            context=mock_context_wrapper,
            specialist_type="Bauleiter",
            date="Friday, May 18",
            time="16:00",
            customer_name="Peter Weber",
            customer_email="peter.weber@example.com",
            customer_phone="+41 79 777 66 55",
        )

        assert "Specialist: Bauleiter" in result
        assert "Date: Friday, May 18" in result
        assert "Time: 16:00" in result
        assert "Customer: Peter Weber" in result

        # Check context updates
        assert mock_context_wrapper.context.consultation_booked is True
        assert mock_context_wrapper.context.specialist_assigned == "Bauleiter"
        assert mock_context_wrapper.context.customer_name == "Peter Weber"

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_book_consultation_with_customer_email(
        self, context_with_customer_info
    ):
        """Test booking consultation with customer info using REAL function."""
        result = await book_consultation_impl(
            context=context_with_customer_info,
            specialist_type="Architekt",
            date="Monday, May 14",
            time="10:00",
            customer_name="Hans Müller",
            customer_email="hans.mueller@example.com",
            customer_phone="+41 79 123 45 67",
        )

        assert "Confirmation sent to hans.mueller@example.com" in result
        assert "Customer: Hans Müller" in result

        # Check context updates
        assert context_with_customer_info.context.consultation_booked is True
        assert context_with_customer_info.context.specialist_assigned == "Architekt"
        assert (
            context_with_customer_info.context.customer_email
            == "hans.mueller@example.com"
        )

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_book_consultation_saves_all_contact_data(self, mock_context_wrapper):
        """Test that REAL function saves all contact data to context."""
        result = await book_consultation_impl(
            context=mock_context_wrapper,
            specialist_type="Architekt",
            date="Monday, May 14",
            time="10:00",
            customer_name="Test User",
            customer_email="test@example.com",
            customer_phone="+41 79 000 00 00",
        )

        # Verify all contact data is saved
        assert mock_context_wrapper.context.customer_name == "Test User"
        assert mock_context_wrapper.context.customer_email == "test@example.com"
        assert mock_context_wrapper.context.customer_phone == "+41 79 000 00 00"
        assert "Confirmation sent to test@example.com" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_book_consultation_different_times(self, mock_context_wrapper):
        """Test booking consultations at different times using REAL function."""
        time_slots = [
            "09:00",
            "10:00",
            "11:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00",
        ]

        for time_slot in time_slots:
            result = await book_consultation_impl(
                context=mock_context_wrapper,
                specialist_type="Architekt",
                date="Monday",
                time=time_slot,
                customer_name="Time Test",
                customer_email="time@example.com",
                customer_phone="+41 79 111 11 11",
            )

            assert f"Time: {time_slot}" in result
            assert mock_context_wrapper.context.consultation_booked is True

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_book_consultation_different_dates(self, mock_context_wrapper):
        """Test booking consultations on different dates using REAL function."""
        date_formats = [
            "Monday, May 14",
            "Tuesday",
            "15.05.2025",
            "May 15, 2025",
            "next Tuesday",
            "tomorrow",
        ]

        for date in date_formats:
            result = await book_consultation_impl(
                context=mock_context_wrapper,
                specialist_type="Architekt",
                date=date,
                time="14:00",
                customer_name="Date Test",
                customer_email="date@example.com",
                customer_phone="+41 79 222 22 22",
            )

            assert f"Date: {date}" in result
            assert mock_context_wrapper.context.consultation_booked is True

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_book_consultation_context_preservation(
        self, context_with_customer_info
    ):
        """Test that existing context is preserved during booking using REAL function."""
        # Set some additional context
        context_with_customer_info.context.project_type = "Einfamilienhaus"
        context_with_customer_info.context.area_sqm = 150.0
        context_with_customer_info.context.inquiry_id = "INQ-12345"

        await book_consultation_impl(
            context=context_with_customer_info,
            specialist_type="Architekt",
            date="Monday",
            time="14:00",
            customer_name="Hans Müller",
            customer_email="hans.mueller@example.com",
            customer_phone="+41 79 123 45 67",
        )

        # Check that existing context is preserved
        assert context_with_customer_info.context.customer_name == "Hans Müller"
        assert (
            context_with_customer_info.context.customer_email
            == "hans.mueller@example.com"
        )
        assert context_with_customer_info.context.project_type == "Einfamilienhaus"
        assert context_with_customer_info.context.area_sqm == 150.0
        assert context_with_customer_info.context.inquiry_id == "INQ-12345"

        # Check that booking context is added
        assert context_with_customer_info.context.consultation_booked is True
        assert context_with_customer_info.context.specialist_assigned == "Architekt"

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_book_consultation_multiple_bookings(self, mock_context_wrapper):
        """Test multiple consultation bookings (should overwrite previous) using REAL function."""
        # First booking
        await book_consultation_impl(
            context=mock_context_wrapper,
            specialist_type="Architekt",
            date="Monday",
            time="14:00",
            customer_name="First Customer",
            customer_email="first@example.com",
            customer_phone="+41 79 111 11 11",
        )

        assert mock_context_wrapper.context.consultation_booked is True
        assert mock_context_wrapper.context.specialist_assigned == "Architekt"
        assert mock_context_wrapper.context.customer_name == "First Customer"

        # Second booking (should overwrite contact data)
        await book_consultation_impl(
            context=mock_context_wrapper,
            specialist_type="Holzbau-Ingenieur",
            date="Tuesday",
            time="10:00",
            customer_name="Second Customer",
            customer_email="second@example.com",
            customer_phone="+41 79 222 22 22",
        )

        assert mock_context_wrapper.context.consultation_booked is True
        assert mock_context_wrapper.context.specialist_assigned == "Holzbau-Ingenieur"
        assert mock_context_wrapper.context.customer_name == "Second Customer"
        assert mock_context_wrapper.context.customer_email == "second@example.com"

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_book_consultation_empty_inputs(self, mock_context_wrapper):
        """Test booking consultation with empty inputs using REAL function."""
        result = await book_consultation_impl(
            context=mock_context_wrapper,
            specialist_type="",
            date="",
            time="",
            customer_name="",
            customer_email="",
            customer_phone="",
        )

        assert "✅ Consultation Booked!" in result
        assert "Specialist: " in result
        assert "Date: " in result
        assert "Time: " in result

        # Context should still be updated
        assert mock_context_wrapper.context.consultation_booked is True
        assert mock_context_wrapper.context.specialist_assigned == ""

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_book_consultation_special_characters(self, mock_context_wrapper):
        """Test booking consultation with special characters in inputs using REAL function."""
        result = await book_consultation_impl(
            context=mock_context_wrapper,
            specialist_type="Architekt & Planner",
            date="Montag, 15. Mai 2025",
            time="14:00 Uhr",
            customer_name="Müller & Söhne",
            customer_email="mueller@example.com",
            customer_phone="+41 79 333 33 33",
        )

        assert "Specialist: Architekt & Planner" in result
        assert "Date: Montag, 15. Mai 2025" in result
        assert "Time: 14:00 Uhr" in result
        assert "Customer: Müller & Söhne" in result

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_book_consultation_return_format(self, mock_context_wrapper):
        """Test the format of the booking confirmation using REAL function."""
        result = await book_consultation_impl(
            context=mock_context_wrapper,
            specialist_type="Architekt",
            date="Monday, May 14",
            time="14:00",
            customer_name="Format Test",
            customer_email="format@example.com",
            customer_phone="+41 79 444 44 44",
        )

        lines = result.split("\n")

        # Should have confirmation header
        assert any("✅ Consultation Booked!" in line for line in lines)

        # Should have details section
        assert any("Details:" in line for line in lines)

        # Should have all required fields (including new Customer field)
        assert any("Customer:" in line for line in lines)
        assert any("Specialist:" in line for line in lines)
        assert any("Date:" in line for line in lines)
        assert any("Time:" in line for line in lines)
        assert any("Location:" in line for line in lines)

        # Should have confirmation and follow-up info
        assert any("Confirmation sent" in line for line in lines)
        assert any("Phone:" in line for line in lines)
        assert any("contact you one day before" in line for line in lines)

    @pytest.mark.asyncio
    @pytest.mark.tools
    async def test_book_consultation_office_location_consistent(
        self, mock_context_wrapper
    ):
        """Test that office location is consistent across all bookings using REAL function."""
        specialist_types = ["Architekt", "Holzbau-Ingenieur", "Bauleiter"]
        expected_location = "ERNI Gruppe, Guggibadstrasse 8, 6288 Schongau"

        for specialist_type in specialist_types:
            result = await book_consultation_impl(
                context=mock_context_wrapper,
                specialist_type=specialist_type,
                date="Monday",
                time="14:00",
                customer_name="Location Test",
                customer_email="location@example.com",
                customer_phone="+41 79 555 55 55",
            )

            assert f"Location: {expected_location}" in result
