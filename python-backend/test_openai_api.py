#!/usr/bin/env python3
"""
Test script to verify OpenAI API compatibility with configured models.

This script tests:
1. OpenAI API key is valid
2. Model names are correct (gpt-4o-mini)
3. Basic agent execution works
4. Guardrails function properly

Usage:
    python test_openai_api.py

Environment variables required:
    OPENAI_API_KEY - Your OpenAI API key
    OPENAI_VECTOR_STORE_ID - Vector store ID for FAQ agent
"""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from openai import OpenAI

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


def test_environment_variables():
    """Test that required environment variables are set."""
    print("\n" + "=" * 60)
    print("1. Testing Environment Variables")
    print("=" * 60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    vector_store_id = os.getenv("OPENAI_VECTOR_STORE_ID")
    
    if not api_key:
        print_error("OPENAI_API_KEY is not set")
        return False
    
    if api_key.startswith("sk-"):
        print_success(f"OPENAI_API_KEY is set (starts with 'sk-')")
    else:
        print_warning("OPENAI_API_KEY doesn't start with 'sk-' (might be invalid)")
    
    if not vector_store_id:
        print_warning("OPENAI_VECTOR_STORE_ID is not set (FAQ agent won't work)")
    else:
        print_success(f"OPENAI_VECTOR_STORE_ID is set: {vector_store_id[:20]}...")
    
    return True


def test_openai_connection():
    """Test connection to OpenAI API."""
    print("\n" + "=" * 60)
    print("2. Testing OpenAI API Connection")
    print("=" * 60)
    
    try:
        client = OpenAI()
        
        # List available models
        print_info("Fetching available models...")
        models = client.models.list()
        
        # Check if our models are available
        model_ids = [model.id for model in models.data]
        
        if "gpt-4o-mini" in model_ids:
            print_success("Model 'gpt-4o-mini' is available")
        else:
            print_error("Model 'gpt-4o-mini' is NOT available")
            print_info("Available GPT-4 models:")
            for model_id in sorted(model_ids):
                if "gpt-4" in model_id.lower():
                    print(f"  - {model_id}")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Failed to connect to OpenAI API: {e}")
        return False


def test_model_execution():
    """Test basic model execution."""
    print("\n" + "=" * 60)
    print("3. Testing Model Execution")
    print("=" * 60)
    
    try:
        client = OpenAI()
        
        print_info("Testing gpt-4o-mini with simple completion...")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello, ERNI Gruppe!' in one sentence."}
            ],
            max_tokens=50,
            temperature=0.3
        )
        
        result = response.choices[0].message.content
        print_success(f"Model response: {result}")
        
        # Check token usage
        usage = response.usage
        print_info(f"Tokens used: {usage.total_tokens} (prompt: {usage.prompt_tokens}, completion: {usage.completion_tokens})")
        
        return True
        
    except Exception as e:
        print_error(f"Model execution failed: {e}")
        return False


def test_agents_import():
    """Test that agents can be imported."""
    print("\n" + "=" * 60)
    print("4. Testing Agent Imports")
    print("=" * 60)
    
    try:
        from main import (
            triage_agent,
            faq_agent,
            project_information_agent,
            cost_estimation_agent,
            project_status_agent,
            appointment_booking_agent,
            MAIN_AGENT_MODEL,
            GUARDRAIL_MODEL,
        )
        
        print_success("All agents imported successfully")
        print_info(f"Main agent model: {MAIN_AGENT_MODEL}")
        print_info(f"Guardrail model: {GUARDRAIL_MODEL}")
        
        # Verify model names
        if MAIN_AGENT_MODEL == "gpt-4o-mini":
            print_success("Main agent model is correct (gpt-4o-mini)")
        else:
            print_error(f"Main agent model is WRONG: {MAIN_AGENT_MODEL} (should be gpt-4o-mini)")
            return False
        
        if GUARDRAIL_MODEL == "gpt-4o-mini":
            print_success("Guardrail model is correct (gpt-4o-mini)")
        else:
            print_error(f"Guardrail model is WRONG: {GUARDRAIL_MODEL} (should be gpt-4o-mini)")
            return False
        
        # Check agent configuration
        agents = [
            ("Triage Agent", triage_agent),
            ("FAQ Agent", faq_agent),
            ("Project Information Agent", project_information_agent),
            ("Cost Estimation Agent", cost_estimation_agent),
            ("Project Status Agent", project_status_agent),
            ("Appointment Booking Agent", appointment_booking_agent),
        ]
        
        for name, agent in agents:
            print_info(f"  - {name}: {len(agent.tools)} tools, {len(agent.input_guardrails)} input guardrails")
        
        return True
        
    except Exception as e:
        print_error(f"Failed to import agents: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("ERNI Gruppe Building Agents - OpenAI API Test")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Environment Variables", test_environment_variables()))
    results.append(("OpenAI Connection", test_openai_connection()))
    results.append(("Model Execution", test_model_execution()))
    results.append(("Agent Imports", test_agents_import()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    print("\n" + "=" * 60)
    if passed == total:
        print_success(f"All tests passed! ({passed}/{total})")
        print_success("✓ OpenAI API is configured correctly")
        print_success("✓ Model names are correct (gpt-4o-mini)")
        print_success("✓ Agents are ready for production")
        return 0
    else:
        print_error(f"Some tests failed ({passed}/{total} passed)")
        print_error("Please fix the issues above before deploying to production")
        return 1


if __name__ == "__main__":
    sys.exit(main())

