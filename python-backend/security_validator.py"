"""
Security Validator for Production Environment
Ensures all required secrets are properly configured before startup.
"""

import os
import sys
from typing import List, Tuple


class ProductionSecurityValidator:
    """Validates security configuration for production environment."""
    
    # Weak/default values that should never be used in production
    FORBIDDEN_VALUES = [
        "changeme",
        "dev-secret-key-change-in-production",
        "please-change-this-secret-key-in-production",
        "test-api-key",
        "secret",
        "password",
        "admin",
    ]
    
    @classmethod
    def validate_all(cls) -> None:
        """
        Validate all production secrets.
        
        Raises:
            SystemExit: If any validation fails in production environment
        """
        environment = os.getenv("ENVIRONMENT", "development")
        
        if environment != "production":
            print(f"ℹ️  Environment: {environment} - Skipping production security validation")
            return
        
        print("🔒 Validating production security configuration...")
        
        errors: List[str] = []
        
        # Validate required secrets
        errors.extend(cls._validate_required_secrets())
        
        # Validate secret strength
        errors.extend(cls._validate_secret_strength())
        
        # Validate database configuration
        errors.extend(cls._validate_database_config())
        
        if errors:
            print("\n❌ PRODUCTION SECURITY VALIDATION FAILED:\n")
            for error in errors:
                print(f"  • {error}")
            print("\n🛑 Application startup aborted for security reasons.\n")
            sys.exit(1)
        
        print("✅ Production security validation passed\n")
    
    @classmethod
    def _validate_required_secrets(cls) -> List[str]:
        """Validate that all required secrets are set."""
        errors = []
        
        required_secrets = [
            ("OPENAI_API_KEY", "OpenAI API key"),
            ("SECRET_KEY", "JWT secret key"),
            ("DB_PASSWORD", "Database password"),
            ("REDIS_PASSWORD", "Redis password"),
        ]
        
        for env_var, description in required_secrets:
            value = os.getenv(env_var)
            
            if not value:
                errors.append(f"{description} ({env_var}) is not set")
            elif value.lower() in cls.FORBIDDEN_VALUES:
                errors.append(
                    f"{description} ({env_var}) uses forbidden default value: '{value}'"
                )
        
        return errors
    
    @classmethod
    def _validate_secret_strength(cls) -> List[str]:
        """Validate that secrets meet minimum strength requirements."""
        errors = []
        
        # Validate SECRET_KEY length
        secret_key = os.getenv("SECRET_KEY", "")
        if len(secret_key) < 32:
            errors.append(
                f"SECRET_KEY is too short ({len(secret_key)} chars). "
                f"Minimum 32 characters required for production."
            )
        
        # Validate DB_PASSWORD length
        db_password = os.getenv("DB_PASSWORD", "")
        if len(db_password) < 16:
            errors.append(
                f"DB_PASSWORD is too short ({len(db_password)} chars). "
                f"Minimum 16 characters required for production."
            )
        
        # Validate REDIS_PASSWORD length
        redis_password = os.getenv("REDIS_PASSWORD", "")
        if len(redis_password) < 16:
            errors.append(
                f"REDIS_PASSWORD is too short ({len(redis_password)} chars). "
                f"Minimum 16 characters required for production."
            )
        
        return errors
    
    @classmethod
    def _validate_database_config(cls) -> List[str]:
        """Validate database configuration."""
        errors = []
        
        database_url = os.getenv("DATABASE_URL", "")
        
        # Check if using default SQLite in production
        if "sqlite" in database_url.lower():
            errors.append(
                "SQLite database detected in production. "
                "Use PostgreSQL for production deployments."
            )
        
        # Check if password is in DATABASE_URL
        if database_url and "changeme" in database_url:
            errors.append(
                "DATABASE_URL contains default password 'changeme'. "
                "Please use a strong password."
            )
        
        return errors


# Auto-validate on import in production
if __name__ != "__main__":
    ProductionSecurityValidator.validate_all()

