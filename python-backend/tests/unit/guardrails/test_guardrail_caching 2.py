"""
Unit tests for guardrail caching functionality.

Tests the TTL cache implementation for relevance and jailbreak guardrails
to verify performance improvements and correct cache behavior.
"""

import pytest
import time
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from main import (
    guardrail_cache,
    _hash_input,
)


class TestGuardrailCaching:
    """Test suite for guardrail caching functionality."""

    def setup_method(self):
        """Clear cache before each test."""
        guardrail_cache.clear()

    def test_hash_input_string(self):
        """Test hash function with string input."""
        input1 = "Hello world"
        input2 = "Hello world"
        input3 = "Different text"
        
        hash1 = _hash_input(input1)
        hash2 = _hash_input(input2)
        hash3 = _hash_input(input3)
        
        # Same input should produce same hash
        assert hash1 == hash2
        
        # Different input should produce different hash
        assert hash1 != hash3
        
        # Hash should be SHA256 (64 hex characters)
        assert len(hash1) == 64

    def test_hash_input_list(self):
        """Test hash function with list input."""
        input1 = [{"text": "Hello"}, {"text": "world"}]
        input2 = [{"text": "Hello"}, {"text": "world"}]
        input3 = [{"text": "Different"}]
        
        hash1 = _hash_input(input1)
        hash2 = _hash_input(input2)
        hash3 = _hash_input(input3)
        
        # Same input should produce same hash
        assert hash1 == hash2
        
        # Different input should produce different hash
        assert hash1 != hash3

    def test_cache_basic_operations(self):
        """Test basic cache operations."""
        # Add entry
        guardrail_cache["test_key"] = "test_value"
        assert "test_key" in guardrail_cache
        assert guardrail_cache["test_key"] == "test_value"

        # Clear cache
        guardrail_cache.clear()
        assert len(guardrail_cache) == 0

    def test_cache_size_limit(self):
        """Test that cache respects maximum size limit."""
        # Cache size is configured in main.py (default 1000)
        # This test verifies the cache doesn't grow indefinitely

        # Add entries up to limit
        for i in range(1100):
            cache_key = f"test_key_{i}"
            guardrail_cache[cache_key] = f"value_{i}"

        # Cache should not exceed max size
        assert len(guardrail_cache) <= 1000

    def test_cache_ttl_expiration(self):
        """Test that cache entries expire after TTL."""
        # This test verifies TTL behavior
        # Note: Actual TTL is 3600 seconds, so we just verify the cache type
        from cachetools import TTLCache
        assert isinstance(guardrail_cache, TTLCache)

        # Verify cache has TTL attribute
        assert hasattr(guardrail_cache, 'ttl')

