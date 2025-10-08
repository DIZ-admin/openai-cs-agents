#!/usr/bin/env python3
"""
Production Preflight Check for ERNI Gruppe Building Agents

This script validates that all production requirements are met before deployment.

Usage:
    python preflight_check.py

Exit codes:
    0 - All checks passed
    1 - One or more checks failed
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_success(message: str):
    """Print success message in green."""
    print(f"{GREEN}✓ {message}{RESET}")


def print_error(message: str):
    """Print error message in red."""
    print(f"{RED}✗ {message}{RESET}")


def print_warning(message: str):
    """Print warning message in yellow."""
    print(f"{YELLOW}⚠ {message}{RESET}")


def print_info(message: str):
    """Print info message in blue."""
    print(f"{BLUE}ℹ {message}{RESET}")


def check_environment_variables():
    """Check that all required environment variables are set."""
    print("\n" + "=" * 60)
    print("1. Checking Environment Variables")
    print("=" * 60)
    
    required_vars = {
        "OPENAI_API_KEY": "OpenAI API key",
        "SECRET_KEY": "Secret key for session encryption",
        "JWT_SECRET_KEY": "JWT secret key",
    }
    
    optional_vars = {
        "OPENAI_VECTOR_STORE_ID": "Vector Store ID for FAQ agent",
        "DB_PASSWORD": "Database password",
        "REDIS_PASSWORD": "Redis password",
    }
    
    all_passed = True
    
    # Check required variables
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            print_error(f"{var} is not set ({description})")
            all_passed = False
        elif value in ["your-api-key-here", "your-secret-key-here", "dev-secret-key-change-in-production"]:
            print_error(f"{var} contains placeholder value")
            all_passed = False
        else:
            print_success(f"{var} is set")
    
    # Check optional variables
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if not value:
            print_warning(f"{var} is not set ({description}) - optional but recommended")
        elif "placeholder" in value.lower() or "your-" in value.lower():
            print_warning(f"{var} contains placeholder value")
        else:
            print_success(f"{var} is set")
    
    return all_passed


def check_security_settings():
    """Check security settings."""
    print("\n" + "=" * 60)
    print("2. Checking Security Settings")
    print("=" * 60)
    
    all_passed = True
    
    # Check ENVIRONMENT
    environment = os.getenv("ENVIRONMENT", "development")
    if environment == "production":
        print_success(f"ENVIRONMENT is set to production")
    else:
        print_warning(f"ENVIRONMENT is set to '{environment}' (should be 'production' for production deployment)")
    
    # Check DEBUG
    debug = os.getenv("DEBUG", "false").lower()
    if debug == "false":
        print_success("DEBUG is disabled")
    else:
        print_error("DEBUG is enabled (must be false in production)")
        all_passed = False
    
    # Check REQUIRE_AUTH
    require_auth = os.getenv("REQUIRE_AUTH", "false").lower()
    if require_auth == "true":
        print_success("REQUIRE_AUTH is enabled")
    else:
        print_warning("REQUIRE_AUTH is disabled (should be true in production)")
    
    # Check SECRET_KEY length
    secret_key = os.getenv("SECRET_KEY", "")
    if len(secret_key) >= 32:
        print_success(f"SECRET_KEY is strong ({len(secret_key)} characters)")
    else:
        print_error(f"SECRET_KEY is too short ({len(secret_key)} characters, minimum 32)")
        all_passed = False
    
    # Check JWT_SECRET_KEY length
    jwt_secret = os.getenv("JWT_SECRET_KEY", "")
    if len(jwt_secret) >= 32:
        print_success(f"JWT_SECRET_KEY is strong ({len(jwt_secret)} characters)")
    else:
        print_error(f"JWT_SECRET_KEY is too short ({len(jwt_secret)} characters, minimum 32)")
        all_passed = False
    
    # Check that SECRET_KEY and JWT_SECRET_KEY are different
    if secret_key and jwt_secret and secret_key != jwt_secret:
        print_success("SECRET_KEY and JWT_SECRET_KEY are different")
    else:
        print_error("SECRET_KEY and JWT_SECRET_KEY must be different")
        all_passed = False
    
    return all_passed


def check_openai_configuration():
    """Check OpenAI configuration."""
    print("\n" + "=" * 60)
    print("3. Checking OpenAI Configuration")
    print("=" * 60)
    
    all_passed = True
    
    # Check API key format
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key.startswith("sk-"):
        print_success("OPENAI_API_KEY has correct format")
    else:
        print_error("OPENAI_API_KEY does not start with 'sk-'")
        all_passed = False
    
    # Check Vector Store ID
    vector_store_id = os.getenv("OPENAI_VECTOR_STORE_ID", "")
    if vector_store_id and not "placeholder" in vector_store_id.lower():
        if vector_store_id.startswith("vs_"):
            print_success("OPENAI_VECTOR_STORE_ID has correct format")
        else:
            print_warning("OPENAI_VECTOR_STORE_ID does not start with 'vs_'")
    else:
        print_warning("OPENAI_VECTOR_STORE_ID is not configured (FAQ agent will not work)")
    
    return all_passed


def check_dependencies():
    """Check that all dependencies are installed."""
    print("\n" + "=" * 60)
    print("4. Checking Dependencies")
    print("=" * 60)
    
    all_passed = True
    
    required_packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("agents", "agents"),
        ("openai", "openai"),
        ("pydantic", "pydantic"),
        ("python-jose", "jose"),  # python-jose imports as 'jose'
        ("passlib", "passlib"),
        ("bcrypt", "bcrypt"),
    ]

    for display_name, import_name in required_packages:
        try:
            __import__(import_name)
            print_success(f"{display_name} is installed")
        except ImportError:
            print_error(f"{display_name} is not installed")
            all_passed = False
    
    return all_passed


def check_file_structure():
    """Check that required files and directories exist."""
    print("\n" + "=" * 60)
    print("5. Checking File Structure")
    print("=" * 60)
    
    all_passed = True
    
    required_files = [
        "api.py",
        "main.py",
        "auth.py",
        "production_config.py",
        "requirements.txt",
        ".env",
    ]
    
    required_dirs = [
        "prompts",
        "tests",
    ]
    
    for file in required_files:
        if Path(file).exists():
            print_success(f"{file} exists")
        else:
            print_error(f"{file} is missing")
            all_passed = False
    
    for dir in required_dirs:
        if Path(dir).exists():
            print_success(f"{dir}/ directory exists")
        else:
            print_error(f"{dir}/ directory is missing")
            all_passed = False
    
    # Check data directory (will be created if missing)
    data_dir = Path("data")
    if not data_dir.exists():
        print_info("data/ directory will be created on first run")
    else:
        print_success("data/ directory exists")
    
    return all_passed


def main():
    """Run all preflight checks."""
    print("\n" + "=" * 60)
    print("ERNI Gruppe Building Agents - Production Preflight Check")
    print("=" * 60)
    
    results = []
    
    # Run all checks
    results.append(("Environment Variables", check_environment_variables()))
    results.append(("Security Settings", check_security_settings()))
    results.append(("OpenAI Configuration", check_openai_configuration()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("File Structure", check_file_structure()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Preflight Check Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        if result:
            print_success(f"{check_name}: PASSED")
        else:
            print_error(f"{check_name}: FAILED")
    
    print("\n" + "=" * 60)
    if passed == total:
        print_success(f"All checks passed! ({passed}/{total})")
        print_success("✓ System is ready for production deployment")
        return 0
    else:
        print_error(f"Some checks failed ({passed}/{total} passed)")
        print_error("✗ Please fix the issues above before deploying to production")
        return 1


if __name__ == "__main__":
    sys.exit(main())

