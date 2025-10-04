# Coverage Improvement Plan - Week 4, Task 4.1

**Date:** 2025-10-05  
**Current Coverage:** 23%  
**Target Coverage:** 90%  
**Status:** 17 failing tests, 270 passing tests

---

## Executive Summary

### Current State Analysis

**Coverage by Module:**
- ✅ **Excellent Coverage (>80%):**
  - `metrics.py`: 95% (56/59 statements)
  - `prompt_loader.py`: 84% (54/64 statements)
  - `__init__.py`: 100% (1/1 statements)

- ⚠️ **Good Coverage (50-80%):**
  - `logging_config.py`: 67% (46/69 statements)
  - `session_manager.py`: 56% (31/55 statements)
  - `tests/conftest.py`: 51% (38/75 statements)

- ❌ **Poor Coverage (<50%):**
  - `main.py`: 48% (127/266 statements) - **139 missing**
  - `auth.py`: 45% (39/86 statements) - **47 missing**
  - `api.py`: 35% (96/274 statements) - **178 missing**
  - `production_config.py`: 0% (0/121 statements) - **121 missing**

- 🚫 **No Coverage (0%):**
  - `tests/e2e/test_e2e_full_stack.py`: 0% (0/278 statements)
  - `tests/integration/test_agents_sdk.py`: 0% (0/104 statements)
  - `tests/integration/test_api_endpoints.py`: 0% (0/206 statements)
  - `tests/integration/test_main_integration.py`: 0% (0/142 statements)

---

## Phase 1: Fix Failing Tests (Priority: CRITICAL)

### 1.1 Model Configuration Failures (5 tests)

**Issue:** Tests expect `gpt-4o-mini` but code uses `gpt-4.1-mini`

**Affected Tests:**
- `test_appointment_booking_agent_configuration`
- `test_cost_estimation_agent_configuration`
- `test_project_information_agent_configuration`
- `test_project_status_agent_configuration`
- `test_triage_agent_model_configuration`

**Fix:** Update test assertions to expect `gpt-4.1-mini`

**Files to Update:**
- `tests/unit/agents/test_appointment_booking_agent.py`
- `tests/unit/agents/test_cost_estimation_agent.py`
- `tests/unit/agents/test_project_information_agent.py`
- `tests/unit/agents/test_project_status_agent.py`
- `tests/unit/agents/test_triage_agent.py`

**Estimated Time:** 15 minutes

---

### 1.2 FAQ Agent Instruction Failures (4 tests)

**Issue:** Test assertions use outdated text patterns that don't match current instructions

**Affected Tests:**
- `test_faq_agent_knowledge_base_access` - Looking for "knowledge base"
- `test_faq_agent_website_links` - Looking for "website links"
- `test_faq_agent_answer_quality_guidance` - Looking for "answer questions"
- `test_faq_agent_error_handling` - Looking for "cannot answer"

**Fix:** Update test assertions to match actual instruction wording:
- "knowledge base" → "comprehensive knowledge base"
- "website links" → "relevant website links"
- "answer questions" → "answer frequently asked questions"
- "cannot answer" → "cannot find the answer"

**Files to Update:**
- `tests/unit/agents/test_faq_agent.py`

**Estimated Time:** 10 minutes

---

### 1.3 FAQ Agent Tool Count Failure (1 test)

**Issue:** Test expects 1 tool but FAQ agent now has 2 tools (FileSearchTool + faq_lookup_building)

**Affected Test:**
- `test_faq_agent_single_tool_focus`

**Fix:** Update assertion to expect 2 tools or rename test to reflect dual-tool approach

**Files to Update:**
- `tests/unit/agents/test_faq_agent.py`

**Estimated Time:** 5 minutes

---

### 1.4 Project Status Agent Instruction Failure (1 test)

**Issue:** Test looks for "milestones" (plural) but instruction says "milestone" (singular)

**Affected Test:**
- `test_project_status_instructions_procedure`

**Fix:** Update test to search for "milestone" instead of "milestones"

**Files to Update:**
- `tests/unit/agents/test_project_status_agent.py`

**Estimated Time:** 5 minutes

---

## Phase 2: Coverage Gap Analysis

### 2.1 Critical Business Logic Gaps

**Priority 1: API Endpoints (`api.py` - 35% coverage, 178 missing)**

**Missing Coverage Areas:**
1. Error handling in API endpoints
2. Request validation logic
3. Response formatting
4. Edge cases in conversation management
5. Agent routing logic
6. Session management integration
7. Authentication middleware integration

**Impact:** HIGH - API is the main entry point for all requests

---

**Priority 2: Core Agent Logic (`main.py` - 48% coverage, 139 missing)**

**Missing Coverage Areas:**
1. Agent instruction functions (dynamic context injection)
2. Tool implementations:
   - `estimate_project_cost` - edge cases
   - `get_project_status` - error handling
   - `check_specialist_availability` - date parsing
   - `book_consultation` - validation logic
3. Guardrail functions:
   - `relevance_guardrail` - boundary cases
   - `jailbreak_guardrail` - attack patterns
   - `pii_guardrail` - PII detection edge cases
4. Handoff callback functions
5. Context initialization logic

**Impact:** HIGH - Core business logic

---

**Priority 3: Authentication (`auth.py` - 45% coverage, 47 missing)**

**Missing Coverage Areas:**
1. Token validation edge cases
2. Error handling for invalid tokens
3. Token expiration logic
4. Rate limiting integration
5. Security header validation

**Impact:** MEDIUM-HIGH - Security-critical component

---

**Priority 4: Production Configuration (`production_config.py` - 0% coverage, 121 missing)**

**Missing Coverage Areas:**
1. Environment variable loading
2. Configuration validation
3. Default value handling
4. Error handling for missing configs

**Impact:** MEDIUM - Important for production deployment

---

### 2.2 Integration Test Gaps (0% coverage)

**Files with No Coverage:**
- `tests/integration/test_agents_sdk.py` (104 statements)
- `tests/integration/test_api_endpoints.py` (206 statements)
- `tests/integration/test_main_integration.py` (142 statements)
- `tests/e2e/test_e2e_full_stack.py` (278 statements)

**Issue:** Integration and E2E tests are not being executed during coverage runs

**Reason:** Coverage command only runs `tests/unit/` directory

**Fix:** Update coverage command to include integration tests

---

## Phase 3: Test Writing Strategy

### 3.1 API Endpoint Tests (`api.py`)

**Target Coverage:** 80%+ (from 35%)

**Test Files to Create/Enhance:**
- `tests/unit/test_api_error_handling.py` (NEW)
- `tests/unit/test_api_validation.py` (NEW)
- `tests/unit/test_api_conversation_management.py` (NEW)

**Test Scenarios:**
1. **Error Handling:**
   - Invalid conversation IDs
   - Missing required fields
   - Malformed JSON requests
   - Database connection errors
   - OpenAI API errors

2. **Request Validation:**
   - Empty messages
   - Oversized messages
   - Invalid agent names
   - Missing authentication headers

3. **Response Formatting:**
   - Successful responses
   - Error responses
   - Streaming responses
   - Partial responses

4. **Conversation Management:**
   - Creating new conversations
   - Retrieving conversation history
   - Deleting conversations
   - Listing conversations

**Estimated Lines:** ~400 lines (split into 2 files)

---

### 3.2 Core Agent Logic Tests (`main.py`)

**Target Coverage:** 85%+ (from 48%)

**Test Files to Create/Enhance:**
- `tests/unit/tools/test_cost_estimation_edge_cases.py` (NEW)
- `tests/unit/tools/test_project_status_error_handling.py` (NEW)
- `tests/unit/tools/test_consultation_booking_validation.py` (NEW)
- `tests/unit/guardrails/test_guardrail_edge_cases.py` (NEW)

**Test Scenarios:**
1. **Tool Edge Cases:**
   - `estimate_project_cost`:
     - Zero area
     - Negative area
     - Extremely large area
     - Invalid project types
     - Invalid construction types
   
   - `get_project_status`:
     - Non-existent project numbers
     - Invalid project number formats
     - Null/empty project numbers
   
   - `check_specialist_availability`:
     - Invalid date formats
     - Past dates
     - Far future dates
     - Invalid specialist types
   
   - `book_consultation`:
     - Invalid email formats
     - Invalid phone formats
     - Missing required fields
     - Duplicate bookings

2. **Guardrail Edge Cases:**
   - `relevance_guardrail`:
     - Borderline relevant questions
     - Mixed relevant/irrelevant content
     - Non-English input
   
   - `jailbreak_guardrail`:
     - Sophisticated prompt injection
     - Encoded attacks
     - Multi-step attacks
   
   - `pii_guardrail`:
     - Various PII formats
     - Partial PII
     - Obfuscated PII

3. **Agent Instructions:**
   - Dynamic context injection
   - Missing context fields
   - Null context values

**Estimated Lines:** ~600 lines (split into 4 files)

---

### 3.3 Authentication Tests (`auth.py`)

**Target Coverage:** 90%+ (from 45%)

**Test Files to Enhance:**
- `tests/unit/test_auth.py` (EXISTING - enhance)

**Test Scenarios:**
1. **Token Validation:**
   - Expired tokens
   - Malformed tokens
   - Missing tokens
   - Invalid signatures
   - Tampered tokens

2. **Error Handling:**
   - Network errors
   - Invalid credentials
   - Rate limit exceeded
   - Server errors

3. **Security Headers:**
   - Missing headers
   - Invalid header formats
   - CORS validation

**Estimated Lines:** ~200 lines (additions to existing file)

---

### 3.4 Production Configuration Tests (`production_config.py`)

**Target Coverage:** 80%+ (from 0%)

**Test Files to Create:**
- `tests/unit/test_production_config.py` (NEW)

**Test Scenarios:**
1. **Environment Variable Loading:**
   - All variables present
   - Missing optional variables
   - Missing required variables
   - Invalid variable formats

2. **Configuration Validation:**
   - Valid configurations
   - Invalid port numbers
   - Invalid URLs
   - Invalid boolean values

3. **Default Values:**
   - Default value application
   - Override behavior

**Estimated Lines:** ~250 lines

---

## Phase 4: Implementation Plan

### Week 4 - Day 1-2: Fix Failing Tests
- [ ] Fix model configuration tests (5 tests)
- [ ] Fix FAQ agent instruction tests (4 tests)
- [ ] Fix FAQ agent tool count test (1 test)
- [ ] Fix project status instruction test (1 test)
- [ ] Verify all 287 tests pass
- [ ] Re-run coverage report

**Deliverable:** All tests passing, baseline coverage established

---

### Week 4 - Day 3-4: API Coverage
- [ ] Create `test_api_error_handling.py`
- [ ] Create `test_api_validation.py`
- [ ] Create `test_api_conversation_management.py`
- [ ] Run coverage: Target 80% for `api.py`

**Deliverable:** API coverage increased from 35% to 80%+

---

### Week 4 - Day 5-6: Core Agent Logic Coverage
- [ ] Create `test_cost_estimation_edge_cases.py`
- [ ] Create `test_project_status_error_handling.py`
- [ ] Create `test_consultation_booking_validation.py`
- [ ] Create `test_guardrail_edge_cases.py`
- [ ] Run coverage: Target 85% for `main.py`

**Deliverable:** Main.py coverage increased from 48% to 85%+

---

### Week 4 - Day 7: Authentication & Configuration Coverage
- [ ] Enhance `test_auth.py`
- [ ] Create `test_production_config.py`
- [ ] Run coverage: Target 90% for `auth.py`, 80% for `production_config.py`

**Deliverable:** Auth and config coverage at target levels

---

### Week 4 - Day 8: Integration Test Execution
- [ ] Update coverage command to include integration tests
- [ ] Fix any integration test failures
- [ ] Run full coverage report

**Deliverable:** Integration tests included in coverage metrics

---

### Week 4 - Day 9-10: Final Push & Documentation
- [ ] Identify remaining coverage gaps
- [ ] Write targeted tests for gaps
- [ ] Update test documentation
- [ ] Generate final coverage report
- [ ] Update `tasks.md`

**Deliverable:** 90%+ overall coverage achieved

---

## Success Metrics

### Coverage Targets by Module

| Module | Current | Target | Gap |
|--------|---------|--------|-----|
| `api.py` | 35% | 80% | +45% |
| `main.py` | 48% | 85% | +37% |
| `auth.py` | 45% | 90% | +45% |
| `production_config.py` | 0% | 80% | +80% |
| `logging_config.py` | 67% | 85% | +18% |
| `session_manager.py` | 56% | 85% | +29% |
| **Overall** | **23%** | **90%** | **+67%** |

### Test Count Targets

| Category | Current | Target | New Tests |
|----------|---------|--------|-----------|
| Unit Tests | 287 | ~350 | +63 |
| Integration Tests | 0 (not run) | 452 | Enable existing |
| E2E Tests | 0 (not run) | 278 | Enable existing |
| **Total** | **287** | **~1080** | **+793** |

---

## Risk Mitigation

### Risk 1: Time Constraints
**Mitigation:** Prioritize critical business logic (API, main.py) over configuration files

### Risk 2: Flaky Tests
**Mitigation:** Mock all external dependencies (OpenAI API, database)

### Risk 3: Coverage vs. Quality
**Mitigation:** Focus on meaningful test scenarios, not just line coverage

### Risk 4: Breaking Changes
**Mitigation:** Run full test suite after each batch of new tests

---

## Next Steps

1. **Immediate:** Fix 17 failing tests
2. **Day 1-2:** Achieve 100% test pass rate
3. **Day 3-4:** Increase API coverage to 80%
4. **Day 5-6:** Increase main.py coverage to 85%
5. **Day 7:** Complete auth and config coverage
6. **Day 8-10:** Final push to 90% overall coverage

---

**Last Updated:** 2025-10-05  
**Owner:** Development Team  
**Status:** In Progress - Phase 1

