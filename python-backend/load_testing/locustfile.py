"""
Locust Load Testing Configuration for ERNI Gruppe Building Agents API.

This file defines load testing scenarios using Locust framework.

Installation:
    pip install locust

Usage:
    # Start Locust web UI
    locust -f load_testing/locustfile.py --host=http://localhost:8000
    
    # Run headless with specific parameters
    locust -f load_testing/locustfile.py --host=http://localhost:8000 \
           --users 50 --spawn-rate 5 --run-time 15m --headless

Test Scenarios:
    - Baseline: 10 users, 5 minutes
    - Normal Load: 50 users, 15 minutes
    - Peak Load: 100 users, 10 minutes
    - Stress Test: 200+ users until failure
    - Endurance: 50 users, 2 hours
"""

import json
import random
import time
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner

# ============================================================================
# Test Data
# ============================================================================

# Sample conversation messages
SAMPLE_MESSAGES = [
    "Hello, I want to build a wooden house",
    "How much would a 150m² house cost?",
    "What's the status of project 2024-156?",
    "I'd like to book a consultation with an architect",
    "Why should I choose timber construction?",
    "What certifications does ERNI have?",
    "Tell me about your services",
    "What are the advantages of wood?",
    "I need information about building permits",
    "How long does a typical project take?",
]

# Project types for cost estimation
PROJECT_TYPES = ["Einfamilienhaus", "Mehrfamilienhaus", "Agrar", "Renovation"]
CONSTRUCTION_TYPES = ["Holzbau", "Systembau"]

# ============================================================================
# Custom Metrics
# ============================================================================

# Track custom metrics
response_times = []
error_count = 0
success_count = 0


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """Track request metrics."""
    global response_times, error_count, success_count
    
    response_times.append(response_time)
    
    if exception:
        error_count += 1
    else:
        success_count += 1


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Print summary statistics when test stops."""
    if response_times:
        sorted_times = sorted(response_times)
        count = len(sorted_times)
        
        p50 = sorted_times[int(count * 0.50)]
        p95 = sorted_times[int(count * 0.95)]
        p99 = sorted_times[int(count * 0.99)]
        
        print("\n" + "="*80)
        print("LOAD TEST SUMMARY")
        print("="*80)
        print(f"Total Requests: {count}")
        print(f"Successful: {success_count} ({success_count/count*100:.2f}%)")
        print(f"Failed: {error_count} ({error_count/count*100:.2f}%)")
        print(f"\nResponse Times:")
        print(f"  P50 (median): {p50:.0f}ms")
        print(f"  P95: {p95:.0f}ms")
        print(f"  P99: {p99:.0f}ms")
        print(f"  Min: {min(sorted_times):.0f}ms")
        print(f"  Max: {max(sorted_times):.0f}ms")
        print(f"  Average: {sum(sorted_times)/count:.0f}ms")
        print("="*80 + "\n")


# ============================================================================
# User Behavior Classes
# ============================================================================

class ERNIBuildingAgentsUser(HttpUser):
    """
    Base user class for ERNI Building Agents load testing.
    
    Simulates realistic user behavior with think time between requests.
    """
    
    # Wait 1-3 seconds between tasks (realistic user behavior)
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a user starts. Initialize conversation."""
        self.conversation_id = None
        self.auth_token = None
        
        # Optional: Authenticate user
        # Uncomment if authentication is required
        # self.authenticate()
    
    def authenticate(self):
        """Authenticate and get JWT token."""
        response = self.client.post(
            "/auth/token",
            params={"username": "testuser", "password": "testpass"},
            name="/auth/token"
        )
        
        if response.status_code == 200:
            data = response.json()
            self.auth_token = data.get("access_token")
    
    def get_headers(self):
        """Get request headers with optional authentication."""
        headers = {"Content-Type": "application/json"}
        
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        return headers
    
    @task(10)
    def health_check(self):
        """
        Health check endpoint (10% of requests).
        
        This is a lightweight endpoint that should always be fast.
        """
        self.client.get("/health", name="/health")
    
    @task(5)
    def readiness_check(self):
        """
        Readiness check endpoint (5% of requests).
        
        Checks if the service is ready to handle requests.
        """
        self.client.get("/readiness", name="/readiness")
    
    @task(5)
    def get_agents_list(self):
        """
        Get list of available agents (5% of requests).
        """
        self.client.get("/agents", name="/agents")
    
    @task(50)
    def chat_conversation(self):
        """
        Main chat endpoint (50% of requests).
        
        Simulates a realistic conversation with the agents.
        """
        # Generate or reuse conversation ID
        if not self.conversation_id:
            import uuid
            self.conversation_id = str(uuid.uuid4())
        
        # Select random message
        message = random.choice(SAMPLE_MESSAGES)
        
        # Send chat request
        payload = {
            "message": message,
            "conversation_id": self.conversation_id
        }
        
        response = self.client.post(
            "/chat",
            json=payload,
            headers=self.get_headers(),
            name="/chat"
        )
        
        # Validate response
        if response.status_code == 200:
            try:
                data = response.json()
                # Check for expected fields
                if "response" not in data:
                    response.failure("Missing 'response' field in chat response")
            except json.JSONDecodeError:
                response.failure("Invalid JSON response")
    
    @task(20)
    def cost_estimation_flow(self):
        """
        Cost estimation conversation flow (20% of requests).
        
        Simulates a user asking for cost estimation.
        """
        import uuid
        conv_id = str(uuid.uuid4())
        
        # Step 1: Initial inquiry
        self.client.post(
            "/chat",
            json={
                "message": "How much would it cost to build a house?",
                "conversation_id": conv_id
            },
            headers=self.get_headers(),
            name="/chat (cost estimation)"
        )
        
        # Think time
        time.sleep(random.uniform(0.5, 1.5))
        
        # Step 2: Provide details
        project_type = random.choice(PROJECT_TYPES)
        construction_type = random.choice(CONSTRUCTION_TYPES)
        area = random.randint(100, 300)
        
        self.client.post(
            "/chat",
            json={
                "message": f"{project_type}, {area} m², {construction_type}",
                "conversation_id": conv_id
            },
            headers=self.get_headers(),
            name="/chat (cost details)"
        )
    
    @task(10)
    def project_status_check(self):
        """
        Project status check (10% of requests).
        """
        import uuid
        conv_id = str(uuid.uuid4())
        
        # Random project number
        project_number = f"2024-{random.randint(100, 200)}"
        
        self.client.post(
            "/chat",
            json={
                "message": f"What's the status of project {project_number}?",
                "conversation_id": conv_id
            },
            headers=self.get_headers(),
            name="/chat (project status)"
        )


class StressTestUser(ERNIBuildingAgentsUser):
    """
    Stress test user with more aggressive behavior.
    
    Used for stress testing to find breaking points.
    """
    
    # Shorter wait time for stress testing
    wait_time = between(0.1, 0.5)
    
    @task(80)
    def rapid_fire_chat(self):
        """Send rapid-fire chat requests."""
        import uuid
        
        for _ in range(5):  # Send 5 requests in quick succession
            self.client.post(
                "/chat",
                json={
                    "message": random.choice(SAMPLE_MESSAGES),
                    "conversation_id": str(uuid.uuid4())
                },
                headers=self.get_headers(),
                name="/chat (stress)"
            )
            time.sleep(0.1)  # Minimal delay


# ============================================================================
# Custom Load Shapes
# ============================================================================

from locust import LoadTestShape

class StepLoadShape(LoadTestShape):
    """
    Step load pattern: gradually increase load in steps.
    
    Useful for finding the breaking point of the system.
    """
    
    step_time = 60  # Each step lasts 60 seconds
    step_load = 10  # Increase by 10 users each step
    spawn_rate = 5  # Spawn 5 users per second
    time_limit = 600  # Total test duration: 10 minutes
    
    def tick(self):
        run_time = self.get_run_time()
        
        if run_time > self.time_limit:
            return None
        
        current_step = run_time // self.step_time
        return (current_step * self.step_load, self.spawn_rate)


class WaveLoadShape(LoadTestShape):
    """
    Wave load pattern: simulate traffic waves (peak hours).
    
    Useful for testing how the system handles varying load.
    """
    
    time_limit = 900  # 15 minutes
    min_users = 10
    max_users = 100
    
    def tick(self):
        run_time = self.get_run_time()
        
        if run_time > self.time_limit:
            return None
        
        # Sine wave pattern
        import math
        wave_position = (run_time / self.time_limit) * 2 * math.pi
        user_count = int(
            self.min_users + 
            (self.max_users - self.min_users) * (math.sin(wave_position) + 1) / 2
        )
        
        return (user_count, 10)


# ============================================================================
# Usage Examples
# ============================================================================

"""
BASELINE TEST (10 users, 5 minutes):
    locust -f locustfile.py --host=http://localhost:8000 \
           --users 10 --spawn-rate 2 --run-time 5m --headless

NORMAL LOAD (50 users, 15 minutes):
    locust -f locustfile.py --host=http://localhost:8000 \
           --users 50 --spawn-rate 5 --run-time 15m --headless

PEAK LOAD (100 users, 10 minutes):
    locust -f locustfile.py --host=http://localhost:8000 \
           --users 100 --spawn-rate 10 --run-time 10m --headless

STRESS TEST (Step load until failure):
    locust -f locustfile.py --host=http://localhost:8000 \
           --users 200 --spawn-rate 10 --run-time 10m --headless \
           --shape=StepLoadShape

ENDURANCE TEST (50 users, 2 hours):
    locust -f locustfile.py --host=http://localhost:8000 \
           --users 50 --spawn-rate 5 --run-time 2h --headless

WEB UI (interactive):
    locust -f locustfile.py --host=http://localhost:8000
    # Open http://localhost:8089 in browser
"""

