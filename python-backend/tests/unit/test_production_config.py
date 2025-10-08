"""
Unit tests for production configuration.

Tests configuration loading and validation.
"""

import os
import pytest
from unittest.mock import patch

from production_config import Config


class TestProductionConfig:
    """Test production configuration."""

    def test_config_default_values(self):
        """Test that Config loads default values."""
        # Test default values
        assert Config.ENVIRONMENT in ["development", "staging", "production", "test"]
        assert isinstance(Config.DEBUG, bool)
        assert Config.LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        assert isinstance(Config.APP_NAME, str)
        assert isinstance(Config.APP_VERSION, str)

    def test_config_server_defaults(self):
        """Test server configuration defaults."""
        assert Config.HOST == "0.0.0.0"
        assert isinstance(Config.PORT, int)
        assert Config.PORT > 0
        assert isinstance(Config.WORKERS, int)
        assert Config.WORKERS > 0
        assert isinstance(Config.TIMEOUT, int)
        assert Config.TIMEOUT > 0

    def test_config_openai_settings(self):
        """Test OpenAI configuration."""
        assert isinstance(Config.OPENAI_API_KEY, str)
        # OPENAI_ORG_ID can be None
        assert Config.OPENAI_ORG_ID is None or isinstance(Config.OPENAI_ORG_ID, str)

    def test_config_database_settings(self):
        """Test database configuration."""
        assert isinstance(Config.DATABASE_URL, str)
        assert isinstance(Config.DB_POOL_SIZE, int)
        assert Config.DB_POOL_SIZE > 0
        assert isinstance(Config.DB_MAX_OVERFLOW, int)
        assert Config.DB_MAX_OVERFLOW > 0
        assert isinstance(Config.DB_POOL_RECYCLE, int)
        assert Config.DB_POOL_RECYCLE > 0

    def test_config_redis_settings(self):
        """Test Redis configuration."""
        assert isinstance(Config.REDIS_URL, str)
        # REDIS_PASSWORD can be None
        assert Config.REDIS_PASSWORD is None or isinstance(Config.REDIS_PASSWORD, str)
        assert isinstance(Config.REDIS_MAX_CONNECTIONS, int)
        assert Config.REDIS_MAX_CONNECTIONS > 0

    def test_config_security_settings(self):
        """Test security configuration."""
        assert isinstance(Config.SECRET_KEY, str)
        assert len(Config.SECRET_KEY) > 0
        assert isinstance(Config.ALLOWED_HOSTS, list)
        assert len(Config.ALLOWED_HOSTS) > 0

    @patch.dict(os.environ, {"ENVIRONMENT": "production"})
    def test_config_with_production_env(self):
        """Test configuration with production environment."""
        # Reload the module to pick up new env vars
        import importlib
        import production_config
        importlib.reload(production_config)
        
        assert production_config.Config.ENVIRONMENT == "production"

    @patch.dict(os.environ, {"DEBUG": "true"})
    def test_config_with_debug_enabled(self):
        """Test configuration with debug enabled."""
        import importlib
        import production_config
        importlib.reload(production_config)
        
        assert production_config.Config.DEBUG is True

    @patch.dict(os.environ, {"PORT": "9000"})
    def test_config_with_custom_port(self):
        """Test configuration with custom port."""
        import importlib
        import production_config
        importlib.reload(production_config)
        
        assert production_config.Config.PORT == 9000

    @patch.dict(os.environ, {"LOG_LEVEL": "DEBUG"})
    def test_config_with_custom_log_level(self):
        """Test configuration with custom log level."""
        import importlib
        import production_config
        importlib.reload(production_config)
        
        assert production_config.Config.LOG_LEVEL == "DEBUG"

    def test_config_allowed_hosts_parsing(self):
        """Test that ALLOWED_HOSTS is parsed correctly."""
        assert isinstance(Config.ALLOWED_HOSTS, list)
        # Should contain at least localhost
        assert any("localhost" in host or "127.0.0.1" in host for host in Config.ALLOWED_HOSTS)

    def test_config_database_url_format(self):
        """Test database URL format."""
        assert Config.DATABASE_URL.startswith("sqlite://") or \
               Config.DATABASE_URL.startswith("postgresql://") or \
               Config.DATABASE_URL.startswith("mysql://")

    def test_config_redis_url_format(self):
        """Test Redis URL format."""
        assert Config.REDIS_URL.startswith("redis://")

    @patch.dict(os.environ, {"WORKERS": "8"})
    def test_config_with_custom_workers(self):
        """Test configuration with custom worker count."""
        import importlib
        import production_config
        importlib.reload(production_config)
        
        assert production_config.Config.WORKERS == 8

    @patch.dict(os.environ, {"TIMEOUT": "300"})
    def test_config_with_custom_timeout(self):
        """Test configuration with custom timeout."""
        import importlib
        import production_config
        importlib.reload(production_config)
        
        assert production_config.Config.TIMEOUT == 300

    @patch.dict(os.environ, {"DB_POOL_SIZE": "20"})
    def test_config_with_custom_db_pool_size(self):
        """Test configuration with custom database pool size."""
        import importlib
        import production_config
        importlib.reload(production_config)
        
        assert production_config.Config.DB_POOL_SIZE == 20

    @patch.dict(os.environ, {"REDIS_MAX_CONNECTIONS": "100"})
    def test_config_with_custom_redis_connections(self):
        """Test configuration with custom Redis max connections."""
        import importlib
        import production_config
        importlib.reload(production_config)
        
        assert production_config.Config.REDIS_MAX_CONNECTIONS == 100

    def test_config_types_are_correct(self):
        """Test that all config values have correct types."""
        assert isinstance(Config.ENVIRONMENT, str)
        assert isinstance(Config.DEBUG, bool)
        assert isinstance(Config.LOG_LEVEL, str)
        assert isinstance(Config.APP_NAME, str)
        assert isinstance(Config.APP_VERSION, str)
        assert isinstance(Config.HOST, str)
        assert isinstance(Config.PORT, int)
        assert isinstance(Config.WORKERS, int)
        assert isinstance(Config.TIMEOUT, int)
        assert isinstance(Config.OPENAI_API_KEY, str)
        assert isinstance(Config.DATABASE_URL, str)
        assert isinstance(Config.DB_POOL_SIZE, int)
        assert isinstance(Config.DB_MAX_OVERFLOW, int)
        assert isinstance(Config.DB_POOL_RECYCLE, int)
        assert isinstance(Config.REDIS_URL, str)
        assert isinstance(Config.REDIS_MAX_CONNECTIONS, int)
        assert isinstance(Config.SECRET_KEY, str)
        assert isinstance(Config.ALLOWED_HOSTS, list)

    @patch.dict(os.environ, {"ALLOWED_HOSTS": "example.com,api.example.com,*.example.com"})
    def test_config_multiple_allowed_hosts(self):
        """Test configuration with multiple allowed hosts."""
        import importlib
        import production_config
        importlib.reload(production_config)
        
        hosts = production_config.Config.ALLOWED_HOSTS
        assert len(hosts) == 3
        assert "example.com" in hosts
        assert "api.example.com" in hosts
        assert "*.example.com" in hosts

    def test_config_secret_key_not_empty(self):
        """Test that secret key is not empty."""
        assert Config.SECRET_KEY != ""
        assert len(Config.SECRET_KEY) >= 10  # Minimum reasonable length

    def test_config_port_in_valid_range(self):
        """Test that port is in valid range."""
        assert 1 <= Config.PORT <= 65535

    def test_config_workers_positive(self):
        """Test that workers count is positive."""
        assert Config.WORKERS > 0
        assert Config.WORKERS <= 32  # Reasonable upper limit

    def test_config_timeout_reasonable(self):
        """Test that timeout is reasonable."""
        assert Config.TIMEOUT > 0
        assert Config.TIMEOUT <= 3600  # Max 1 hour

    def test_config_db_pool_settings_reasonable(self):
        """Test that database pool settings are reasonable."""
        assert Config.DB_POOL_SIZE > 0
        assert Config.DB_POOL_SIZE <= 100
        assert Config.DB_MAX_OVERFLOW > 0
        assert Config.DB_MAX_OVERFLOW <= 200
        assert Config.DB_POOL_RECYCLE > 0
        assert Config.DB_POOL_RECYCLE <= 86400  # Max 24 hours

    def test_config_redis_connections_reasonable(self):
        """Test that Redis max connections is reasonable."""
        assert Config.REDIS_MAX_CONNECTIONS > 0
        assert Config.REDIS_MAX_CONNECTIONS <= 1000


class TestConfigValidation:
    """Test configuration validation methods."""

    @patch.dict(os.environ, {"OPENAI_API_KEY": ""})
    def test_validate_config_missing_api_key(self):
        """Test validation fails when OPENAI_API_KEY is missing."""
        import importlib
        import production_config
        importlib.reload(production_config)

        with pytest.raises(ValueError, match="OPENAI_API_KEY is required"):
            production_config.Config.validate()

    @patch.dict(os.environ, {
        "ENVIRONMENT": "production",
        "SECRET_KEY": "dev-secret-key-change-in-production",
        "OPENAI_API_KEY": "test-key"
    })
    def test_validate_config_production_with_dev_secret(self):
        """Test validation fails in production with dev secret key."""
        import importlib
        import production_config
        importlib.reload(production_config)

        with pytest.raises(ValueError, match="SECRET_KEY must be changed"):
            production_config.Config.validate()

    @patch.dict(os.environ, {
        "ENVIRONMENT": "production",
        "DEBUG": "true",
        "SECRET_KEY": "production-secret-key",
        "OPENAI_API_KEY": "test-key"
    })
    def test_validate_config_production_with_debug(self):
        """Test validation fails in production with DEBUG=true."""
        import importlib
        import production_config
        importlib.reload(production_config)

        with pytest.raises(ValueError, match="DEBUG must be false"):
            production_config.Config.validate()

    @patch.dict(os.environ, {
        "ENVIRONMENT": "development",
        "OPENAI_API_KEY": "test-key"
    })
    def test_validate_config_development_passes(self):
        """Test validation passes in development environment."""
        import importlib
        import production_config
        importlib.reload(production_config)

        # Should not raise
        result = production_config.Config.validate()
        assert result is True


class TestLoggingSetup:
    """Test logging configuration."""

    def test_setup_logging_creates_logger(self):
        """Test that setup_logging creates and configures logger."""
        from production_config import setup_logging

        logger = setup_logging()
        assert logger is not None
        assert logger.name == "production_config"

    @patch.dict(os.environ, {"LOG_LEVEL": "DEBUG"})
    def test_setup_logging_with_debug_level(self):
        """Test logging setup with DEBUG level."""
        import importlib
        import production_config
        importlib.reload(production_config)

        logger = production_config.setup_logging()
        assert logger is not None

    @patch.dict(os.environ, {"LOG_LEVEL": "ERROR"})
    def test_setup_logging_with_error_level(self):
        """Test logging setup with ERROR level."""
        import importlib
        import production_config
        importlib.reload(production_config)

        logger = production_config.setup_logging()
        assert logger is not None


class TestValidationModels:
    """Test Pydantic validation models."""

    def test_customer_contact_validation_valid(self):
        """Test CustomerContactValidation with valid data."""
        from production_config import CustomerContactValidation

        contact = CustomerContactValidation(
            name="John Doe",
            email="john.doe@example.com",
            phone="+41 79 123 45 67"
        )
        assert contact.name == "John Doe"
        assert contact.email == "john.doe@example.com"
        assert contact.phone == "+41 79 123 45 67"

    def test_customer_contact_validation_invalid_email(self):
        """Test CustomerContactValidation with invalid email."""
        from production_config import CustomerContactValidation

        with pytest.raises(Exception):  # Pydantic ValidationError
            CustomerContactValidation(
                name="John Doe",
                email="invalid-email",
                phone="+41 79 123 45 67"
            )

    def test_customer_contact_validation_invalid_phone(self):
        """Test CustomerContactValidation with invalid phone."""
        from production_config import CustomerContactValidation

        with pytest.raises(Exception):  # Pydantic ValidationError
            CustomerContactValidation(
                name="John Doe",
                email="john.doe@example.com",
                phone="123456789"
            )

    def test_customer_contact_validation_name_too_short(self):
        """Test CustomerContactValidation with name too short."""
        from production_config import CustomerContactValidation

        with pytest.raises(Exception):  # Pydantic ValidationError
            CustomerContactValidation(
                name="J",
                email="john.doe@example.com",
                phone="+41 79 123 45 67"
            )

    def test_customer_contact_validation_name_with_numbers(self):
        """Test CustomerContactValidation with numbers in name."""
        from production_config import CustomerContactValidation

        with pytest.raises(ValueError, match="Name must contain only letters"):
            CustomerContactValidation(
                name="John123",
                email="john.doe@example.com",
                phone="+41 79 123 45 67"
            )

    def test_customer_contact_validation_non_swiss_phone(self):
        """Test CustomerContactValidation with non-Swiss phone."""
        from production_config import CustomerContactValidation

        # Non-Swiss phone will fail regex pattern validation first
        with pytest.raises(Exception):  # Pydantic ValidationError
            CustomerContactValidation(
                name="John Doe",
                email="john.doe@example.com",
                phone="+1 555 123 4567"
            )

    def test_project_data_validation_valid(self):
        """Test ProjectDataValidation with valid data."""
        from production_config import ProjectDataValidation

        project = ProjectDataValidation(
            project_type="Einfamilienhaus",
            construction_type="Holzbau",
            area_sqm=150.0,
            location="Zurich"
        )
        assert project.project_type == "Einfamilienhaus"
        assert project.construction_type == "Holzbau"
        assert project.area_sqm == 150.0
        assert project.location == "Zurich"

    def test_project_data_validation_invalid_project_type(self):
        """Test ProjectDataValidation with invalid project type."""
        from production_config import ProjectDataValidation

        with pytest.raises(Exception):  # Pydantic ValidationError
            ProjectDataValidation(
                project_type="InvalidType",
                construction_type="Holzbau",
                area_sqm=150.0
            )

    def test_project_data_validation_invalid_construction_type(self):
        """Test ProjectDataValidation with invalid construction type."""
        from production_config import ProjectDataValidation

        with pytest.raises(Exception):  # Pydantic ValidationError
            ProjectDataValidation(
                project_type="Einfamilienhaus",
                construction_type="InvalidType",
                area_sqm=150.0
            )

    def test_project_data_validation_zero_area(self):
        """Test ProjectDataValidation with zero area."""
        from production_config import ProjectDataValidation

        with pytest.raises(Exception):  # Pydantic ValidationError
            ProjectDataValidation(
                project_type="Einfamilienhaus",
                construction_type="Holzbau",
                area_sqm=0.0
            )

    def test_project_data_validation_negative_area(self):
        """Test ProjectDataValidation with negative area."""
        from production_config import ProjectDataValidation

        with pytest.raises(Exception):  # Pydantic ValidationError
            ProjectDataValidation(
                project_type="Einfamilienhaus",
                construction_type="Holzbau",
                area_sqm=-100.0
            )

    def test_project_data_validation_area_too_large(self):
        """Test ProjectDataValidation with area exceeding limit."""
        from production_config import ProjectDataValidation

        with pytest.raises(Exception):  # Pydantic ValidationError
            ProjectDataValidation(
                project_type="Einfamilienhaus",
                construction_type="Holzbau",
                area_sqm=20000.0  # Exceeds 10000 limit
            )

