# ERNI Gruppe Building Agents - E2E Test Report

## Test Execution Summary

**Date:** $(date '+%Y-%m-%d %H:%M:%S')  
**Backend URL:** $BACKEND_URL  
**Frontend URL:** $FRONTEND_URL  
**OpenAI Model (Main):** $MAIN_MODEL  
**OpenAI Model (Guardrail):** $GUARDRAIL_MODEL  

---

## Test Results


### Summary Statistics

| Metric | Value |
|--------|-------|
| Total Tests | 10 |
| Passed | 8 |
| Failed | 2 |
| Success Rate | 80.0% |

---

## Test Details

### Individual Test Results

- tests/e2e/test_e2e_full_stack.py::TestTriageAgent::test_basic_greeting [32mPASSED[0m[32m [ 11%][0m
- tests/e2e/test_e2e_full_stack.py::TestCostEstimation::test_cost_estimation_flow [32mPASSED[0m[32m [ 22%][0m
- tests/e2e/test_e2e_full_stack.py::TestProjectStatus::test_project_status_flow [32mPASSED[0m[32m [ 33%][0m
- tests/e2e/test_e2e_full_stack.py::TestAppointmentBooking::test_appointment_booking_flow [32mPASSED[0m[32m [ 44%][0m
- tests/e2e/test_e2e_full_stack.py::TestGuardrails::test_relevance_guardrail [32mPASSED[0m[32m [ 55%][0m
- tests/e2e/test_e2e_full_stack.py::TestGuardrails::test_jailbreak_guardrail [32mPASSED[0m[32m [ 66%][0m
- tests/e2e/test_e2e_full_stack.py::TestFrontendIntegration::test_frontend_proxy [32mPASSED[0m[32m [ 77%][0m
- tests/e2e/test_e2e_full_stack.py::TestPerformance::test_response_time [32mPASSED[0m[32m [ 88%][0m
- tests/e2e/test_e2e_full_stack.py::TestMultiTurnConversation::test_context_preservation [31mFAILED[0m[31m [100%][0m/Users/kostas/Documents/Projects/openai-cs-agents-demo/python-backend/.venv/lib/python3.13/site-packages/pytest_cov/plugin.py:355: CovFailUnderWarning: Coverage failure: total of 35 is less than fail-under=80
- TEST 8: MULTI-TURN CONVERSATION
- [31mFAILED[0m tests/e2e/test_e2e_full_stack.py::[1mTestMultiTurnConversation::test_context_preservation[0m - requests.exceptions.HTTPError: 429 Client Error: Too Many Requests for url: http://127.0.0.1:8000/chat

---

## Performance Metrics


---

## Recommendations

⚠️ **Some tests failed. Please review the failures above.**

**Action Items:**
1. Review failed test details in the log file
2. Check backend and frontend logs for errors
3. Verify OpenAI API connectivity
4. Ensure all services are properly configured
5. Re-run tests after fixes


---

## Full Test Log

See `e2e_test_log.txt` for complete test output.

---

**Generated:** 2025-10-04 18:15:08
