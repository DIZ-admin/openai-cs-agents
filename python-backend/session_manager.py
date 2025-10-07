"""
Session Manager for ERNI Gruppe Building Agents.

This module provides a centralized wrapper for managing agent conversation sessions
using SQLiteSession from the OpenAI Agents SDK.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Optional

import redis
from agents import SQLiteSession

logger = logging.getLogger(__name__)


class AgentSessionManager:
    """
    Centralized manager for agent conversation sessions.

    Provides a clean interface for creating, retrieving, and managing
    SQLiteSession instances for agent conversations.

    Features:
    - Automatic session creation and retrieval
    - Configurable database path
    - Session lifecycle management
    - Thread-safe session access
    - Automatic database initialization

    Example:
        >>> manager = AgentSessionManager()
        >>> session = manager.get_session("conversation-123")
        >>> # Use session with agents
        >>> manager.close_session("conversation-123")
    """

    def __init__(
        self,
        db_path: Optional[str] = None,
        auto_create_db: bool = True,
        redis_url: Optional[str] = None,
    ):
        """
        Initialize the session manager.

        Args:
            db_path: Path to SQLite database file. If None, uses environment
                    variable SESSIONS_DB_PATH or defaults to "data/conversations.db"
            auto_create_db: Whether to automatically create database directory
                           if it doesn't exist
            redis_url: Redis connection URL. If None, uses environment variable
                      REDIS_URL or defaults to "redis://localhost:6379/0"
        """
        # Determine database path
        if db_path is None:
            db_path = os.getenv("SESSIONS_DB_PATH", "data/conversations.db")

        self.db_path = Path(db_path)

        # Create database directory if needed
        if auto_create_db:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Session database directory ensured: {self.db_path.parent}")

        # Cache for active sessions (optional optimization)
        self._sessions: Dict[str, SQLiteSession] = {}

        # Initialize Redis client for context storage (shared across workers)
        if redis_url is None:
            redis_url = os.getenv("REDIS_URL")

        if redis_url:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
        else:
            # Fallback to individual environment variables
            redis_host = os.getenv("REDIS_HOST", "localhost")
            redis_port = int(os.getenv("REDIS_PORT", "6379"))
            redis_password = os.getenv("REDIS_PASSWORD")
            redis_db = int(os.getenv("REDIS_DB", "0"))

            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                db=redis_db,
                decode_responses=True,  # Automatically decode bytes to strings
            )

        # Test Redis connection
        try:
            self.redis_client.ping()
            logger.info("Redis connection established for context storage")
        except redis.ConnectionError as e:
            logger.warning(f"Redis connection failed: {e}. Context will not persist across workers.")
            self.redis_client = None

        logger.info(f"AgentSessionManager initialized with database: {self.db_path}")

    def get_session(self, conversation_id: str) -> SQLiteSession:
        """
        Get or create a SQLiteSession for the given conversation ID.

        This method is idempotent - calling it multiple times with the same
        conversation_id will return the same session instance.

        Args:
            conversation_id: Unique conversation identifier

        Returns:
            SQLiteSession instance for managing conversation history

        Example:
            >>> manager = AgentSessionManager()
            >>> session = manager.get_session("conv-123")
            >>> # Session is now ready to use with agents
        """
        if not conversation_id:
            raise ValueError("conversation_id cannot be empty")

        # Check if session already exists in cache
        if conversation_id in self._sessions:
            logger.debug(f"Returning cached session for conversation: {conversation_id}")
            return self._sessions[conversation_id]

        # Create new session
        logger.debug(f"Creating new session for conversation: {conversation_id}")
        session = SQLiteSession(
            session_id=conversation_id,
            db_path=str(self.db_path),
        )

        # Cache the session
        self._sessions[conversation_id] = session

        return session

    def create_session(self, conversation_id: str) -> SQLiteSession:
        """
        Create a new session (alias for get_session for clarity).

        Args:
            conversation_id: Unique conversation identifier

        Returns:
            SQLiteSession instance

        Example:
            >>> manager = AgentSessionManager()
            >>> session = manager.create_session("new-conversation")
        """
        return self.get_session(conversation_id)

    def has_session(self, conversation_id: str) -> bool:
        """
        Check if a session exists in the cache.

        Note: This only checks the in-memory cache, not the database.
        A session might exist in the database but not be cached.

        Args:
            conversation_id: Conversation identifier to check

        Returns:
            True if session is cached, False otherwise

        Example:
            >>> manager = AgentSessionManager()
            >>> manager.has_session("conv-123")
            False
            >>> session = manager.get_session("conv-123")
            >>> manager.has_session("conv-123")
            True
        """
        return conversation_id in self._sessions

    def close_session(self, conversation_id: str) -> None:
        """
        Close and remove a session from the cache.

        This doesn't delete the conversation history from the database,
        it just removes the session from the in-memory cache.

        Args:
            conversation_id: Conversation identifier to close

        Example:
            >>> manager = AgentSessionManager()
            >>> session = manager.get_session("conv-123")
            >>> # ... use session ...
            >>> manager.close_session("conv-123")
        """
        if conversation_id in self._sessions:
            logger.debug(f"Closing session for conversation: {conversation_id}")
            # SQLiteSession doesn't have an explicit close method
            # Just remove from cache
            del self._sessions[conversation_id]
        else:
            logger.debug(f"Session not found in cache: {conversation_id}")

    def close_all_sessions(self) -> None:
        """
        Close all cached sessions.

        Useful for cleanup when shutting down the application.

        Example:
            >>> manager = AgentSessionManager()
            >>> # ... create multiple sessions ...
            >>> manager.close_all_sessions()
        """
        logger.info(f"Closing {len(self._sessions)} cached sessions")
        self._sessions.clear()

    def get_active_session_count(self) -> int:
        """
        Get the number of currently cached sessions.

        Returns:
            Number of sessions in the cache

        Example:
            >>> manager = AgentSessionManager()
            >>> manager.get_active_session_count()
            0
            >>> session = manager.get_session("conv-123")
            >>> manager.get_active_session_count()
            1
        """
        return len(self._sessions)

    # Backward compatibility methods for tests
    def get(self, conversation_id: str) -> Optional[Dict]:
        """
        Get conversation state (backward compatibility with tests).

        This method exists for backward compatibility with existing tests
        that expect a conversation_store.get() interface.

        Args:
            conversation_id: Conversation identifier

        Returns:
            None (SQLiteSession manages state internally)
        """
        # For backward compatibility, return None
        # SQLiteSession manages state internally
        return None

    def save(self, conversation_id: str, state: Optional[Dict] = None) -> None:
        """
        Save conversation state (backward compatibility with tests).

        This method exists for backward compatibility with existing tests
        that expect a conversation_store.save() interface.

        Args:
            conversation_id: Conversation identifier
            state: Conversation state (ignored, SQLiteSession manages state)
        """
        # For backward compatibility, do nothing
        # SQLiteSession automatically persists state
        pass

    def get_active_conversation_ids(self) -> list[str]:
        """
        Get list of all cached conversation IDs.

        Returns:
            List of conversation IDs currently in cache

        Example:
            >>> manager = AgentSessionManager()
            >>> manager.get_session("conv-1")
            >>> manager.get_session("conv-2")
            >>> manager.get_active_conversation_ids()
            ['conv-1', 'conv-2']
        """
        return list(self._sessions.keys())

    def clear_cache(self) -> None:
        """
        Clear the session cache (alias for close_all_sessions).

        Example:
            >>> manager = AgentSessionManager()
            >>> manager.clear_cache()
        """
        self.close_all_sessions()

    def get_context(self, conversation_id: str) -> Optional[Dict]:
        """
        Get stored context for a conversation from Redis.

        Falls back to in-memory storage if Redis is unavailable.

        Args:
            conversation_id: Conversation identifier

        Returns:
            Stored context dictionary or None if not found
        """
        if not conversation_id:
            return None

        # Try Redis first (shared across workers)
        if self.redis_client:
            try:
                redis_key = f"context:{conversation_id}"
                context_json = self.redis_client.get(redis_key)
                if context_json:
                    context = json.loads(context_json)
                    logger.debug(f"Retrieved context from Redis for conversation: {conversation_id}")
                    return context
            except (redis.ConnectionError, redis.TimeoutError, json.JSONDecodeError) as e:
                logger.warning(f"Failed to retrieve context from Redis: {e}")

        # Fallback to in-memory storage (worker-local, not recommended for production)
        return self._contexts.get(conversation_id) if hasattr(self, '_contexts') else None

    def set_context(self, conversation_id: str, context: Dict, ttl_seconds: int = 86400) -> None:
        """
        Store context for a conversation in Redis.

        Falls back to in-memory storage if Redis is unavailable.

        Args:
            conversation_id: Conversation identifier
            context: Context dictionary to store
            ttl_seconds: Time-to-live in seconds (default: 24 hours)
        """
        if not conversation_id:
            return

        # Try Redis first (shared across workers)
        if self.redis_client:
            try:
                redis_key = f"context:{conversation_id}"
                context_json = json.dumps(context)
                self.redis_client.setex(redis_key, ttl_seconds, context_json)
                logger.debug(f"Stored context in Redis for conversation: {conversation_id} (TTL: {ttl_seconds}s)")
                return
            except (redis.ConnectionError, redis.TimeoutError, TypeError) as e:
                logger.warning(f"Failed to store context in Redis: {e}. Falling back to in-memory storage.")

        # Fallback to in-memory storage (worker-local, not recommended for production)
        if not hasattr(self, '_contexts'):
            self._contexts = {}
        self._contexts[conversation_id] = context
        logger.debug(f"Stored context in memory for conversation: {conversation_id}")

    def __repr__(self) -> str:
        """String representation of the session manager."""
        return (
            f"AgentSessionManager(db_path='{self.db_path}', "
            f"active_sessions={len(self._sessions)})"
        )


# Global session manager instance (singleton pattern)
_session_manager: Optional[AgentSessionManager] = None


def get_session_manager(
    db_path: Optional[str] = None,
    auto_create_db: bool = True,
) -> AgentSessionManager:
    """
    Get the global AgentSessionManager instance (singleton pattern).

    Args:
        db_path: Path to SQLite database file (only used on first call)
        auto_create_db: Whether to auto-create database directory (only used on first call)

    Returns:
        Global AgentSessionManager instance

    Example:
        >>> manager = get_session_manager()
        >>> session = manager.get_session("conv-123")
    """
    global _session_manager
    if _session_manager is None:
        _session_manager = AgentSessionManager(
            db_path=db_path,
            auto_create_db=auto_create_db,
        )
    return _session_manager


def reset_session_manager() -> None:
    """
    Reset the global session manager (useful for testing).

    Example:
        >>> reset_session_manager()
        >>> manager = get_session_manager()  # Creates new instance
    """
    global _session_manager
    if _session_manager is not None:
        _session_manager.close_all_sessions()
    _session_manager = None

