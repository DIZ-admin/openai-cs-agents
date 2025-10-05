#!/bin/bash

#
# Comprehensive Security Audit Script for ERNI Gruppe Building Agents
#
# This script runs a complete security audit including:
# - Dependency vulnerability scanning
# - API security testing
# - Code security review
# - Infrastructure security checks
#
# Usage:
#   ./security_audit/run_security_audit.sh
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_ROOT"
FRONTEND_DIR="$(dirname "$PROJECT_ROOT")/ui"

# Output directory
OUTPUT_DIR="$SCRIPT_DIR/reports"
mkdir -p "$OUTPUT_DIR"

# Timestamp for report
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="$OUTPUT_DIR/security_audit_report_$TIMESTAMP.md"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                    ║${NC}"
echo -e "${BLUE}║        ERNI Gruppe Building Agents - Security Audit Suite         ║${NC}"
echo -e "${BLUE}║                                                                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📅 Date:${NC} $(date)"
echo -e "${BLUE}📁 Project:${NC} $PROJECT_ROOT"
echo -e "${BLUE}📄 Report:${NC} $REPORT_FILE"
echo ""

# Initialize report
cat > "$REPORT_FILE" << EOF
# Security Audit Report - ERNI Gruppe Building Agents

**Date:** $(date)  
**Auditor:** Automated Security Audit Suite  
**Project:** ERNI Gruppe Building Agents  

---

## Executive Summary

This report contains the results of a comprehensive security audit conducted on the ERNI Gruppe Building Agents project.

---

EOF

# ============================================================================
# 1. Dependency Vulnerability Scanning
# ============================================================================

echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}1. DEPENDENCY VULNERABILITY SCANNING${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════${NC}"
echo ""

echo "## 1. Dependency Vulnerability Scanning" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Check if pip-audit is installed
if ! command -v pip-audit &> /dev/null; then
    echo -e "${YELLOW}⚠️  pip-audit not found. Installing...${NC}"
    pip install pip-audit
fi

# Scan Python dependencies
echo -e "${BLUE}📦 Scanning Python dependencies...${NC}"
cd "$BACKEND_DIR"

if pip-audit -r requirements.txt --format=json > "$OUTPUT_DIR/python_vulnerabilities_$TIMESTAMP.json" 2>&1; then
    echo -e "${GREEN}✅ No vulnerabilities found in Python dependencies${NC}"
    echo "### Python Dependencies: ✅ PASS" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "No vulnerabilities found in Python dependencies." >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
else
    VULN_COUNT=$(cat "$OUTPUT_DIR/python_vulnerabilities_$TIMESTAMP.json" | grep -o '"name"' | wc -l)
    echo -e "${RED}❌ Found $VULN_COUNT vulnerable Python packages${NC}"
    echo "### Python Dependencies: ❌ FAIL" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "Found $VULN_COUNT vulnerable Python packages. See \`python_vulnerabilities_$TIMESTAMP.json\` for details." >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
fi

# Scan npm dependencies (if frontend exists)
if [ -d "$FRONTEND_DIR" ]; then
    echo -e "${BLUE}📦 Scanning npm dependencies...${NC}"
    cd "$FRONTEND_DIR"
    
    if npm audit --json > "$OUTPUT_DIR/npm_vulnerabilities_$TIMESTAMP.json" 2>&1; then
        echo -e "${GREEN}✅ No vulnerabilities found in npm dependencies${NC}"
        echo "### npm Dependencies: ✅ PASS" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
    else
        VULN_COUNT=$(cat "$OUTPUT_DIR/npm_vulnerabilities_$TIMESTAMP.json" | grep -o '"severity"' | wc -l)
        echo -e "${RED}❌ Found vulnerabilities in npm dependencies${NC}"
        echo "### npm Dependencies: ❌ FAIL" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
        echo "Found vulnerabilities in npm dependencies. See \`npm_vulnerabilities_$TIMESTAMP.json\` for details." >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
    fi
fi

echo ""

# ============================================================================
# 2. Code Security Review
# ============================================================================

echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}2. CODE SECURITY REVIEW${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════${NC}"
echo ""

echo "## 2. Code Security Review" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

cd "$BACKEND_DIR"

# Check for hardcoded secrets
echo -e "${BLUE}🔍 Checking for hardcoded secrets...${NC}"
if grep -r -i "password\s*=\s*['\"]" --include="*.py" . | grep -v "test" | grep -v ".pyc" > /dev/null; then
    echo -e "${RED}❌ Found potential hardcoded passwords${NC}"
    echo "### Hardcoded Secrets: ❌ FAIL" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "Found potential hardcoded passwords in code." >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
else
    echo -e "${GREEN}✅ No hardcoded passwords found${NC}"
    echo "### Hardcoded Secrets: ✅ PASS" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
fi

# Check for SQL injection vulnerabilities
echo -e "${BLUE}🔍 Checking for SQL injection vulnerabilities...${NC}"
if grep -r "execute.*%\|execute.*format\|execute.*+" --include="*.py" . | grep -v "test" | grep -v ".pyc" > /dev/null; then
    echo -e "${YELLOW}⚠️  Found potential SQL injection vulnerabilities${NC}"
    echo "### SQL Injection: ⚠️  WARNING" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "Found potential SQL injection vulnerabilities. Manual review required." >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
else
    echo -e "${GREEN}✅ No obvious SQL injection vulnerabilities${NC}"
    echo "### SQL Injection: ✅ PASS" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
fi

# Check .env is in .gitignore
echo -e "${BLUE}🔍 Checking .gitignore configuration...${NC}"
if grep -q "\.env" "$PROJECT_ROOT/.gitignore" 2>/dev/null; then
    echo -e "${GREEN}✅ .env is in .gitignore${NC}"
    echo "### .gitignore Configuration: ✅ PASS" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
else
    echo -e "${RED}❌ .env is NOT in .gitignore${NC}"
    echo "### .gitignore Configuration: ❌ FAIL" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo ".env file is not in .gitignore - risk of committing secrets!" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
fi

echo ""

# ============================================================================
# 3. API Security Testing
# ============================================================================

echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}3. API SECURITY TESTING${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════${NC}"
echo ""

echo "## 3. API Security Testing" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is running${NC}"
    
    # Run API security tests
    echo -e "${BLUE}🔒 Running API security tests...${NC}"
    cd "$SCRIPT_DIR"
    
    if python api_security_tests.py http://localhost:8000; then
        echo -e "${GREEN}✅ All API security tests passed${NC}"
        echo "### API Security Tests: ✅ PASS" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
        echo "All API security tests passed. See detailed results in \`api_security_test_*.json\`." >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
    else
        echo -e "${RED}❌ Some API security tests failed${NC}"
        echo "### API Security Tests: ❌ FAIL" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
        echo "Some API security tests failed. See detailed results in \`api_security_test_*.json\`." >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
    fi
else
    echo -e "${YELLOW}⚠️  Backend is not running. Skipping API tests.${NC}"
    echo "### API Security Tests: ⚠️  SKIPPED" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "Backend is not running. Start the backend and re-run the audit." >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
fi

echo ""

# ============================================================================
# 4. Infrastructure Security
# ============================================================================

echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}4. INFRASTRUCTURE SECURITY${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════${NC}"
echo ""

echo "## 4. Infrastructure Security" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Check Docker security
echo -e "${BLUE}🐳 Checking Docker configuration...${NC}"

if [ -f "$PROJECT_ROOT/docker-compose.yml" ]; then
    # Check for exposed ports
    if grep -q "ports:" "$PROJECT_ROOT/docker-compose.yml"; then
        echo -e "${GREEN}✅ Docker Compose file found${NC}"
        echo "### Docker Configuration: ✅ PASS" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
    fi
    
    # Check for secrets in docker-compose
    if grep -i "password\|secret\|key" "$PROJECT_ROOT/docker-compose.yml" | grep -v "POSTGRES_PASSWORD_FILE" | grep -v "environment:" > /dev/null; then
        echo -e "${YELLOW}⚠️  Found potential secrets in docker-compose.yml${NC}"
        echo "**Warning:** Potential secrets found in docker-compose.yml. Use environment variables instead." >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
    fi
fi

echo ""

# ============================================================================
# Final Summary
# ============================================================================

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                    ║${NC}"
echo -e "${BLUE}║                      AUDIT COMPLETE                                ║${NC}"
echo -e "${BLUE}║                                                                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✅ Security audit complete!${NC}"
echo -e "${BLUE}📄 Full report saved to:${NC} $REPORT_FILE"
echo ""

# Add final summary to report
cat >> "$REPORT_FILE" << EOF

---

## Recommendations

1. **Dependency Management:**
   - Regularly update dependencies to patch known vulnerabilities
   - Use \`pip-audit\` and \`npm audit\` in CI/CD pipeline
   - Consider using Dependabot for automated dependency updates

2. **Code Security:**
   - Conduct regular code reviews with security focus
   - Use static analysis tools (e.g., Bandit for Python)
   - Implement security linting in pre-commit hooks

3. **API Security:**
   - Ensure rate limiting is properly configured
   - Implement comprehensive input validation
   - Use HTTPS in production
   - Regularly test guardrails for bypass attempts

4. **Infrastructure:**
   - Use secrets management (e.g., AWS Secrets Manager, HashiCorp Vault)
   - Implement network segmentation
   - Enable audit logging
   - Regular security updates for base images

5. **Monitoring:**
   - Set up security monitoring and alerting
   - Implement intrusion detection
   - Regular security audits (quarterly recommended)

---

**Report Generated:** $(date)  
**Next Audit Recommended:** $(date -d "+3 months" 2>/dev/null || date -v +3m 2>/dev/null || echo "In 3 months")

EOF

echo -e "${BLUE}📊 Next steps:${NC}"
echo "  1. Review the full report: $REPORT_FILE"
echo "  2. Address any critical or high-severity findings"
echo "  3. Update dependencies with known vulnerabilities"
echo "  4. Schedule next security audit in 3 months"
echo ""

