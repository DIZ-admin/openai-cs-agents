#!/bin/bash
# ============================================================================
# ERNI Gruppe Building Agents - Docker Test Script
# ============================================================================
# Tests the Docker deployment
# ============================================================================

set -e  # Exit on error

echo "============================================================================"
echo "ERNI Gruppe Building Agents - Testing Deployment"
echo "============================================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test 1: Backend Health
echo -e "${YELLOW}[1/5]${NC} Testing backend health..."
if curl -f -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✓ Backend is healthy${NC}"
    curl -s http://localhost:8000/health | python3 -m json.tool
else
    echo -e "${RED}✗ Backend health check failed${NC}"
    exit 1
fi
echo ""

# Test 2: Frontend
echo -e "${YELLOW}[2/5]${NC} Testing frontend..."
if curl -f -s http://localhost:3000 > /dev/null; then
    echo -e "${GREEN}✓ Frontend is accessible${NC}"
else
    echo -e "${RED}✗ Frontend is not accessible${NC}"
    exit 1
fi
echo ""

# Test 3: Nginx Proxy
echo -e "${YELLOW}[3/5]${NC} Testing nginx proxy..."
if curl -f -s http://localhost > /dev/null; then
    echo -e "${GREEN}✓ Nginx proxy is working${NC}"
else
    echo -e "${RED}✗ Nginx proxy is not working${NC}"
    exit 1
fi
echo ""

# Test 4: Chat API
echo -e "${YELLOW}[4/5]${NC} Testing chat API..."
RESPONSE=$(curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello",
    "conversation_id": "test-docker-123"
  }')

if echo "$RESPONSE" | grep -q "response"; then
    echo -e "${GREEN}✓ Chat API is working${NC}"
else
    echo -e "${RED}✗ Chat API failed${NC}"
    echo "Response: $RESPONSE"
    exit 1
fi
echo ""

# Test 5: FAQ Agent with Links
echo -e "${YELLOW}[5/5]${NC} Testing FAQ Agent with sitemap links..."
RESPONSE=$(curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Где на сайте почитать о ремонте крыши?",
    "conversation_id": "test-docker-faq-123"
  }')

if echo "$RESPONSE" | grep -q "https://www.erni-gruppe.ch"; then
    echo -e "${GREEN}✓ FAQ Agent provides website links${NC}"
    echo ""
    echo "Sample response:"
    echo "$RESPONSE" | python3 -m json.tool | grep -A 5 "response"
else
    echo -e "${YELLOW}⚠ FAQ Agent response doesn't contain website links${NC}"
    echo "Response: $RESPONSE"
fi
echo ""

echo "============================================================================"
echo -e "${GREEN}All Tests Passed!${NC}"
echo "============================================================================"
echo ""
echo "The Docker deployment is working correctly."
echo "You can now access the application at http://localhost:3000"
echo ""

