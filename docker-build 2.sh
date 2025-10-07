#!/bin/bash
# ============================================================================
# ERNI Gruppe Building Agents - Docker Build Script
# ============================================================================
# Builds all Docker containers for the application
# ============================================================================

set -e  # Exit on error

echo "============================================================================"
echo "ERNI Gruppe Building Agents - Docker Build"
echo "============================================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is running
echo -e "${YELLOW}[1/5]${NC} Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running. Please start Docker Desktop.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker is running${NC}"
echo ""

# Check if .env file exists
echo -e "${YELLOW}[2/5]${NC} Checking environment configuration..."
if [ ! -f "python-backend/.env" ]; then
    echo -e "${RED}Error: python-backend/.env file not found${NC}"
    echo "Please create it from python-backend/.env.example"
    exit 1
fi

# Check if OPENAI_API_KEY is set
if ! grep -q "OPENAI_API_KEY=sk-" python-backend/.env; then
    echo -e "${RED}Error: OPENAI_API_KEY not set in python-backend/.env${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Environment configured${NC}"
echo ""

# Build backend
echo -e "${YELLOW}[3/5]${NC} Building backend container..."
docker build -t erni-backend:latest ./python-backend
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend built successfully${NC}"
else
    echo -e "${RED}✗ Backend build failed${NC}"
    exit 1
fi
echo ""

# Build frontend
echo -e "${YELLOW}[4/5]${NC} Building frontend container..."
docker build -t erni-frontend:latest ./ui
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Frontend built successfully${NC}"
else
    echo -e "${RED}✗ Frontend build failed${NC}"
    exit 1
fi
echo ""

# Pull nginx
echo -e "${YELLOW}[5/5]${NC} Pulling nginx image..."
docker pull nginx:alpine
echo -e "${GREEN}✓ Nginx image ready${NC}"
echo ""

echo "============================================================================"
echo -e "${GREEN}Build Complete!${NC}"
echo "============================================================================"
echo ""
echo "Next steps:"
echo "  1. Start services:    ./docker-start.sh"
echo "  2. View logs:         docker-compose -f docker-compose.simple.yml logs -f"
echo "  3. Stop services:     docker-compose -f docker-compose.simple.yml down"
echo ""

