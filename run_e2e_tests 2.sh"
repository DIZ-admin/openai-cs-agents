#!/bin/bash

# ============================================================================
# ERNI Gruppe Building Agents - E2E Test Runner
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_URL="http://127.0.0.1:8000"
FRONTEND_URL="http://localhost:3000"
REPORT_FILE="e2e_test_report.md"
LOG_FILE="e2e_test_log.txt"

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                  ERNI Gruppe Building Agents - E2E Tests                    ║${NC}"
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo ""

# ============================================================================
# Step 1: Verify Services
# ============================================================================

echo -e "${YELLOW}[1/4] Verifying Services...${NC}"
echo ""

# Check backend
echo -n "  Backend ($BACKEND_URL): "
if curl -s -f "$BACKEND_URL/health" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ RUNNING${NC}"
else
    echo -e "${RED}✗ NOT RUNNING${NC}"
    echo -e "${RED}ERROR: Backend is not running. Please start it first.${NC}"
    exit 1
fi

# Check frontend
echo -n "  Frontend ($FRONTEND_URL): "
if curl -s -f "$FRONTEND_URL" > /dev/null 2>&1 || curl -s "$FRONTEND_URL" 2>&1 | grep -q "200\|404"; then
    echo -e "${GREEN}✓ RUNNING${NC}"
else
    echo -e "${RED}✗ NOT RUNNING${NC}"
    echo -e "${RED}ERROR: Frontend is not running. Please start it first.${NC}"
    exit 1
fi

echo ""

# ============================================================================
# Step 2: Check Environment
# ============================================================================

echo -e "${YELLOW}[2/4] Checking Environment...${NC}"
echo ""

# Check Python virtual environment
if [ ! -d "python-backend/.venv" ]; then
    echo -e "${RED}ERROR: Virtual environment not found${NC}"
    exit 1
fi

# Check models configuration
echo -n "  OpenAI Models: "
MAIN_MODEL=$(grep "OPENAI_MAIN_AGENT_MODEL" python-backend/.env | cut -d'=' -f2)
GUARDRAIL_MODEL=$(grep "OPENAI_GUARDRAIL_MODEL" python-backend/.env | cut -d'=' -f2)
echo -e "${GREEN}$MAIN_MODEL / $GUARDRAIL_MODEL${NC}"

echo ""

# ============================================================================
# Step 3: Run E2E Tests
# ============================================================================

echo -e "${YELLOW}[3/4] Running E2E Tests...${NC}"
echo ""

cd python-backend

# Run pytest with detailed output
.venv/bin/pytest tests/e2e/test_e2e_full_stack.py \
    -v \
    --tb=short \
    --color=yes \
    --durations=10 \
    2>&1 | tee "../$LOG_FILE"

# Capture exit code
TEST_EXIT_CODE=${PIPESTATUS[0]}

cd ..

echo ""

# ============================================================================
# Step 4: Generate Report
# ============================================================================

echo -e "${YELLOW}[4/4] Generating Report...${NC}"
echo ""

# Create report
cat > "$REPORT_FILE" << 'EOF'
# ERNI Gruppe Building Agents - E2E Test Report

## Test Execution Summary

**Date:** $(date '+%Y-%m-%d %H:%M:%S')  
**Backend URL:** $BACKEND_URL  
**Frontend URL:** $FRONTEND_URL  
**OpenAI Model (Main):** $MAIN_MODEL  
**OpenAI Model (Guardrail):** $GUARDRAIL_MODEL  

---

## Test Results

EOF

# Parse test results from log
TOTAL_TESTS=$(grep -c "PASSED\|FAILED" "$LOG_FILE" || echo "0")
PASSED_TESTS=$(grep -c "PASSED" "$LOG_FILE" || echo "0")
FAILED_TESTS=$(grep -c "FAILED" "$LOG_FILE" || echo "0")

# Add results to report
cat >> "$REPORT_FILE" << EOF

### Summary Statistics

| Metric | Value |
|--------|-------|
| Total Tests | $TOTAL_TESTS |
| Passed | $PASSED_TESTS |
| Failed | $FAILED_TESTS |
| Success Rate | $(awk "BEGIN {printf \"%.1f%%\", ($PASSED_TESTS/$TOTAL_TESTS)*100}") |

---

## Test Details

EOF

# Extract test details from log
echo "### Individual Test Results" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

grep -E "TEST [0-9]|✅ TEST|✗ TEST|PASSED|FAILED" "$LOG_FILE" | while read line; do
    echo "- $line" >> "$REPORT_FILE"
done

# Add performance metrics
echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "## Performance Metrics" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

grep "Response time:" "$LOG_FILE" | while read line; do
    echo "- $line" >> "$REPORT_FILE"
done

# Add recommendations
cat >> "$REPORT_FILE" << 'EOF'

---

## Recommendations

EOF

if [ $FAILED_TESTS -eq 0 ]; then
    cat >> "$REPORT_FILE" << 'EOF'
✅ **All tests passed successfully!**

The application is functioning correctly across all tested scenarios:
- Agent routing and handoffs working properly
- Context preservation across conversations
- Guardrails protecting against invalid inputs
- Frontend-backend integration working seamlessly
- Performance within acceptable limits

**Next Steps:**
- Consider adding more edge case tests
- Monitor production performance metrics
- Set up continuous E2E testing in CI/CD pipeline

EOF
else
    cat >> "$REPORT_FILE" << 'EOF'
⚠️ **Some tests failed. Please review the failures above.**

**Action Items:**
1. Review failed test details in the log file
2. Check backend and frontend logs for errors
3. Verify OpenAI API connectivity
4. Ensure all services are properly configured
5. Re-run tests after fixes

EOF
fi

# Add full log reference
cat >> "$REPORT_FILE" << EOF

---

## Full Test Log

See \`$LOG_FILE\` for complete test output.

---

**Generated:** $(date '+%Y-%m-%d %H:%M:%S')
EOF

echo -e "${GREEN}✓ Report generated: $REPORT_FILE${NC}"
echo ""

# ============================================================================
# Final Summary
# ============================================================================

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                           E2E TEST SUMMARY                                   ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  Total Tests:   ${BLUE}$TOTAL_TESTS${NC}"
echo -e "  Passed:        ${GREEN}$PASSED_TESTS${NC}"
echo -e "  Failed:        ${RED}$FAILED_TESTS${NC}"
echo ""

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED!${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}❌ SOME TESTS FAILED${NC}"
    echo ""
    echo -e "Review the report: ${YELLOW}$REPORT_FILE${NC}"
    echo -e "Review the log: ${YELLOW}$LOG_FILE${NC}"
    echo ""
    exit 1
fi

