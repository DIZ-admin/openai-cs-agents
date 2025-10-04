"""
Production Configuration and Utilities for ERNI Gruppe Building Agents
"""

import logging
import os
from datetime import datetime
from typing import Optional

# ============================================================================
# Environment Configuration
# ============================================================================


class Config:
    """Application configuration from environment variables."""

    # Application
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    APP_NAME: str = os.getenv("APP_NAME", "ERNI Building Agents")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    WORKERS: int = int(os.getenv("WORKERS", "4"))
    TIMEOUT: int = int(os.getenv("TIMEOUT", "120"))

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_ORG_ID: Optional[str] = os.getenv("OPENAI_ORG_ID")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./erni_agents.db")
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "10"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))
    DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "3600"))

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD")
    REDIS_MAX_CONNECTIONS: int = int(os.getenv("REDIS_MAX_CONNECTIONS", "50"))

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALLOWED_HOSTS: list = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    CORS_ALLOW_CREDENTIALS: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    RATE_LIMIT_PER_HOUR: int = int(os.getenv("RATE_LIMIT_PER_HOUR", "1000"))
    RATE_LIMIT_PER_DAY: int = int(os.getenv("RATE_LIMIT_PER_DAY", "10000"))
    RATE_LIMIT_STORAGE: str = os.getenv("RATE_LIMIT_STORAGE", "memory")

    # Session
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))
    SESSION_COOKIE_NAME: str = os.getenv("SESSION_COOKIE_NAME", "erni_session")
    SESSION_COOKIE_SECURE: bool = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
    SESSION_COOKIE_HTTPONLY: bool = os.getenv("SESSION_COOKIE_HTTPONLY", "true").lower() == "true"
    SESSION_COOKIE_SAMESITE: str = os.getenv("SESSION_COOKIE_SAMESITE", "lax")

    # Performance
    ENABLE_COMPRESSION: bool = os.getenv("ENABLE_COMPRESSION", "true").lower() == "true"
    COMPRESSION_MIN_SIZE: int = int(os.getenv("COMPRESSION_MIN_SIZE", "1000"))
    ENABLE_CACHING: bool = os.getenv("ENABLE_CACHING", "true").lower() == "true"
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "300"))

    # Monitoring
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN")
    SENTRY_ENVIRONMENT: str = os.getenv("SENTRY_ENVIRONMENT", ENVIRONMENT)
    SENTRY_TRACES_SAMPLE_RATE: float = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1"))

    @classmethod
    def validate(cls):
        """Validate required configuration."""
        errors = []

        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required")

        if cls.ENVIRONMENT == "production":
            if cls.SECRET_KEY == "dev-secret-key-change-in-production":
                errors.append("SECRET_KEY must be changed in production")

            if cls.DEBUG:
                errors.append("DEBUG must be false in production")

            if "http://localhost" in cls.CORS_ORIGINS:
                errors.append("localhost should not be in CORS_ORIGINS in production")

        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")

        return True


# ============================================================================
# Logging Configuration
# ============================================================================


def setup_logging():
    """Configure application logging."""
    log_level = getattr(logging, Config.LOG_LEVEL.upper())

    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Set specific log levels for libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured: level={Config.LOG_LEVEL}, environment={Config.ENVIRONMENT}")

    return logger


# ============================================================================
# Security Headers
# ============================================================================

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
}

if Config.ENVIRONMENT == "production":
    SECURITY_HEADERS["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"


# ============================================================================
# Health Check Response
# ============================================================================


def get_health_status() -> dict:
    """Get application health status."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": Config.APP_VERSION,
        "environment": Config.ENVIRONMENT,
    }


# ============================================================================
# Input Validation
# ============================================================================

from typing import Optional

from pydantic import BaseModel, Field, validator


class CustomerContactValidation(BaseModel):
    """Validation model for customer contact information."""

    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    phone: str = Field(..., regex=r"^\+41\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}$")

    @validator("name")
    def validate_name(cls, v):
        """Validate and sanitize name."""
        v = v.strip()
        if not v.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters and spaces")
        return v

    @validator("phone")
    def validate_phone(cls, v):
        """Validate Swiss phone number format."""
        # Remove spaces for validation
        phone_clean = v.replace(" ", "")
        if not phone_clean.startswith("+41"):
            raise ValueError("Phone number must be a Swiss number (+41)")
        return v


class ProjectDataValidation(BaseModel):
    """Validation model for project data."""

    project_type: str = Field(..., regex=r"^(Einfamilienhaus|Mehrfamilienhaus|Agrar|Renovation)$")
    construction_type: str = Field(..., regex=r"^(Holzbau|Systembau)$")
    area_sqm: float = Field(..., gt=0, le=10000)
    location: Optional[str] = Field(None, max_length=200)

    @validator("area_sqm")
    def validate_area(cls, v):
        """Validate area is reasonable."""
        if v < 10:
            raise ValueError("Area must be at least 10 m²")
        if v > 10000:
            raise ValueError("Area cannot exceed 10,000 m²")
        return round(v, 2)


# ============================================================================
# Rate Limiting Utilities
# ============================================================================


class RateLimitExceeded(Exception):
    """Exception raised when rate limit is exceeded."""

    pass


def get_rate_limit_key(identifier: str, window: str) -> str:
    """Generate rate limit key."""
    return f"rate_limit:{identifier}:{window}"


# ============================================================================
# Error Responses
# ============================================================================

ERROR_RESPONSES = {
    400: {"description": "Bad Request", "content": {"application/json": {"example": {"detail": "Invalid input data"}}}},
    401: {
        "description": "Unauthorized",
        "content": {"application/json": {"example": {"detail": "Authentication required"}}},
    },
    403: {"description": "Forbidden", "content": {"application/json": {"example": {"detail": "Access denied"}}}},
    404: {"description": "Not Found", "content": {"application/json": {"example": {"detail": "Resource not found"}}}},
    429: {
        "description": "Too Many Requests",
        "content": {"application/json": {"example": {"detail": "Rate limit exceeded. Please try again later."}}},
    },
    500: {
        "description": "Internal Server Error",
        "content": {"application/json": {"example": {"detail": "An internal error occurred"}}},
    },
    503: {
        "description": "Service Unavailable",
        "content": {"application/json": {"example": {"detail": "Service temporarily unavailable"}}},
    },
}


# ============================================================================
# Initialization
# ============================================================================


def initialize_production_config():
    """Initialize production configuration."""
    # Validate configuration
    Config.validate()

    # Setup logging
    logger = setup_logging()
    logger.info(f"Starting {Config.APP_NAME} v{Config.APP_VERSION}")
    logger.info(f"Environment: {Config.ENVIRONMENT}")
    logger.info(f"Debug mode: {Config.DEBUG}")

    # Initialize Sentry if configured
    if Config.SENTRY_DSN:
        try:
            import sentry_sdk
            from sentry_sdk.integrations.fastapi import FastApiIntegration

            sentry_sdk.init(
                dsn=Config.SENTRY_DSN,
                environment=Config.SENTRY_ENVIRONMENT,
                traces_sample_rate=Config.SENTRY_TRACES_SAMPLE_RATE,
                integrations=[FastApiIntegration()],
            )
            logger.info("Sentry initialized")
        except ImportError:
            logger.warning("Sentry SDK not installed, error tracking disabled")

    return logger
