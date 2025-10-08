"""Preflight check for ERNI Gruppe Building Agents production deployment."""

import os
import sys
from typing import Iterable

REQUIRED_VARS: dict[str, str] = {
    "OPENAI_API_KEY": "OpenAI API key is required.",
    "OPENAI_VECTOR_STORE_ID": "Vector Store ID is required for FAQ agent.",
    "SECRET_KEY": "SECRET_KEY must be set to a strong random value.",
    "JWT_SECRET_KEY": "JWT_SECRET_KEY must be set (and should differ from SECRET_KEY).",
    "DB_PASSWORD": "Database password must be provided.",
    "REDIS_PASSWORD": "Redis password must be provided.",
    "ALLOWED_HOSTS": "ALLOWED_HOSTS must be configured for production.",
    "CORS_ORIGINS": "CORS_ORIGINS must list allowed origins.",
    "PUBLIC_HOSTNAME": "PUBLIC_HOSTNAME is required for frontend and reverse proxy.",
}

FORBIDDEN_VALUES = {"changeme", "please-change", "your_password_here", "your-secret-key-here", "your_postgres_password_here", "your_redis_password_here"}


def check_required() -> list[str]:
    issues: list[str] = []
    for var, message in REQUIRED_VARS.items():
        value = os.getenv(var)
        if not value:
            issues.append(f"[{var}] {message}")
        elif value.lower() in FORBIDDEN_VALUES:
            issues.append(f"[{var}] value '{value}' is a known insecure placeholder.")
    return issues


def check_lengths() -> list[str]:
    issues: list[str] = []
    for var in ("SECRET_KEY", "JWT_SECRET_KEY"):
        value = os.getenv(var, "")
        if value and len(value) < 32:
            issues.append(f"[{var}] length {len(value)} < 32 characters.")
    return issues


def check_difference() -> list[str]:
    issues: list[str] = []
    secret = os.getenv("SECRET_KEY")
    jwt_secret = os.getenv("JWT_SECRET_KEY")
    if secret and jwt_secret and secret == jwt_secret:
        issues.append("SECRET_KEY and JWT_SECRET_KEY must differ for defense in depth.")
    return issues


def fail(messages: Iterable[str]) -> None:
    print("❌ Preflight check failed:\n")
    for msg in messages:
        print(f"  • {msg}")
    sys.exit(1)


def main() -> None:
    problems = []
    problems.extend(check_required())
    problems.extend(check_lengths())
    problems.extend(check_difference())

    if problems:
        fail(problems)

    print("✅ Preflight check passed. All critical environment variables look good.")


if __name__ == "__main__":
    main()
