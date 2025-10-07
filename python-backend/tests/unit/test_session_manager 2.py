"""
Unit tests for AgentSessionManager.

Tests session creation, retrieval, caching, and lifecycle management.
"""

import pytest
import tempfile
from pathlib import Path

from session_manager import (
    AgentSessionManager,
    get_session_manager,
    reset_session_manager,
)
from agents import SQLiteSession


class TestAgentSessionManager:
    """Test AgentSessionManager class."""

    def test_initialization_default_path(self):
        """Test manager initialization with default database path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            manager = AgentSessionManager(db_path=str(db_path))

            assert manager.db_path == db_path
            assert manager.get_active_session_count() == 0

    def test_initialization_creates_directory(self):
        """Test that manager creates database directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "subdir" / "test.db"
            manager = AgentSessionManager(db_path=str(db_path), auto_create_db=True)

            assert db_path.parent.exists()
            assert manager.db_path == db_path

    def test_get_session_creates_new_session(self):
        """Test getting a new session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            manager = AgentSessionManager(db_path=str(db_path))

            session = manager.get_session("conv-123")

            assert isinstance(session, SQLiteSession)
            assert manager.get_active_session_count() == 1
            assert manager.has_session("conv-123")

    def test_get_session_returns_cached_session(self):
        """Test that getting same session returns cached instance."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            manager = AgentSessionManager(db_path=str(db_path))

            session1 = manager.get_session("conv-123")
            session2 = manager.get_session("conv-123")

            assert session1 is session2
            assert manager.get_active_session_count() == 1

    def test_get_session_empty_id_raises_error(self):
        """Test that empty conversation_id raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            manager = AgentSessionManager(db_path=str(db_path))

            with pytest.raises(ValueError, match="conversation_id cannot be empty"):
                manager.get_session("")

    def test_create_session_alias(self):
        """Test that create_session is an alias for get_session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            manager = AgentSessionManager(db_path=str(db_path))

            session = manager.create_session("conv-123")

            assert isinstance(session, SQLiteSession)
            assert manager.has_session("conv-123")

    def test_has_session(self):
        """Test checking if session exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            manager = AgentSessionManager(db_path=str(db_path))

            assert not manager.has_session("conv-123")

            manager.get_session("conv-123")

            assert manager.has_session("conv-123")
            assert not manager.has_session("conv-456")

    def test_close_session(self):
        """Test closing a session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            manager = AgentSessionManager(db_path=str(db_path))

            manager.get_session("conv-123")
            assert manager.has_session("conv-123")

            manager.close_session("conv-123")

            assert not manager.has_session("conv-123")
            assert manager.get_active_session_count() == 0

    def test_close_session_nonexistent(self):
        """Test closing a session that doesn't exist (should not raise error)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            manager = AgentSessionManager(db_path=str(db_path))

            # Should not raise error
            manager.close_session("nonexistent")

    def test_close_all_sessions(self):
        """Test closing all sessions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            manager = AgentSessionManager(db_path=str(db_path))

            manager.get_session("conv-1")
            manager.get_session("conv-2")
            manager.get_session("conv-3")

            assert manager.get_active_session_count() == 3

            manager.close_all_sessions()

            assert manager.get_active_session_count() == 0
            assert not manager.has_session("conv-1")
            assert not manager.has_session("conv-2")
            assert not manager.has_session("conv-3")

    def test_get_active_session_count(self):
        """Test getting active session count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            manager = AgentSessionManager(db_path=str(db_path))

            assert manager.get_active_session_count() == 0

            manager.get_session("conv-1")
            assert manager.get_active_session_count() == 1

            manager.get_session("conv-2")
            assert manager.get_active_session_count() == 2

            manager.close_session("conv-1")
            assert manager.get_active_session_count() == 1

    def test_get_active_conversation_ids(self):
        """Test getting list of active conversation IDs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            manager = AgentSessionManager(db_path=str(db_path))

            manager.get_session("conv-1")
            manager.get_session("conv-2")
            manager.get_session("conv-3")

            ids = manager.get_active_conversation_ids()

            assert len(ids) == 3
            assert "conv-1" in ids
            assert "conv-2" in ids
            assert "conv-3" in ids

    def test_clear_cache(self):
        """Test clearing the session cache."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            manager = AgentSessionManager(db_path=str(db_path))

            manager.get_session("conv-1")
            manager.get_session("conv-2")

            assert manager.get_active_session_count() == 2

            manager.clear_cache()

            assert manager.get_active_session_count() == 0

    def test_repr(self):
        """Test string representation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            manager = AgentSessionManager(db_path=str(db_path))

            manager.get_session("conv-1")

            repr_str = repr(manager)

            assert "AgentSessionManager" in repr_str
            assert str(db_path) in repr_str
            assert "active_sessions=1" in repr_str


class TestGlobalSessionManager:
    """Test global session manager functions."""

    def teardown_method(self):
        """Reset global session manager after each test."""
        reset_session_manager()

    def test_get_session_manager_singleton(self):
        """Test that get_session_manager returns singleton instance."""
        manager1 = get_session_manager()
        manager2 = get_session_manager()

        assert manager1 is manager2

    def test_reset_session_manager(self):
        """Test resetting the global session manager."""
        manager1 = get_session_manager()
        manager1.get_session("conv-123")

        assert manager1.get_active_session_count() == 1

        reset_session_manager()

        manager2 = get_session_manager()

        assert manager2 is not manager1
        assert manager2.get_active_session_count() == 0

    def test_get_session_manager_with_custom_path(self):
        """Test getting session manager with custom database path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "custom.db"

            manager = get_session_manager(db_path=str(db_path))

            assert manager.db_path == db_path


class TestSessionManagerIntegration:
    """Integration tests for session manager."""

    def test_multiple_sessions_different_conversations(self):
        """Test managing multiple sessions for different conversations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            manager = AgentSessionManager(db_path=str(db_path))

            session1 = manager.get_session("conv-1")
            session2 = manager.get_session("conv-2")
            session3 = manager.get_session("conv-3")

            assert session1 is not session2
            assert session2 is not session3
            assert manager.get_active_session_count() == 3

    def test_session_persistence_after_close(self):
        """Test that closing session doesn't delete database data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            manager = AgentSessionManager(db_path=str(db_path))

            # Create session and close it
            session1 = manager.get_session("conv-123")
            manager.close_session("conv-123")

            # Get session again - should create new instance but same conversation
            session2 = manager.get_session("conv-123")

            assert session1 is not session2
            # Both sessions should have same session_id
            assert session1.session_id == session2.session_id

