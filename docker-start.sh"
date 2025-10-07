#!/bin/bash
# ============================================================================
# ERNI Gruppe Building Agents - Docker Start Script
# ============================================================================
# Starts all Docker containers for the application
# ============================================================================

set -e  # Exit on error

echo "============================================================================"
echo "ERNI Gruppe Building Agents - Starting Services"
echo "============================================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is running
echo -e "${YELLOW}[1/3]${NC} Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running. Please start Docker Desktop.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker is running${NC}"
echo ""

# Check if images exist
echo -e "${YELLOW}[2/3]${NC} Checking Docker images..."
if ! docker images | grep -q "erni-backend"; then
    echo -e "${RED}Error: Backend image not found. Please run ./docker-build.sh first${NC}"
    exit 1
fi
if ! docker images | grep -q "erni-frontend"; then
    echo -e "${RED}Error: Frontend image not found. Please run ./docker-build.sh first${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker images ready${NC}"
echo ""

# Start services
echo -e "${YELLOW}[3/3]${NC} Starting services..."
docker-compose -f docker-compose.simple.yml up -d

echo ""
echo "============================================================================"
echo -e "${GREEN}Services Started!${NC}"
echo "============================================================================"
echo ""
echo "Access points:"
echo "  • Frontend:    http://localhost:3000"
echo "  • Backend API: http://localhost:8000"
echo "  • API Docs:    http://localhost:8000/docs"
echo "  • Nginx Proxy: http://localhost"
echo ""
echo "Useful commands:"
echo "  • View logs:        docker-compose -f docker-compose.simple.yml logs -f"
echo "  • Check status:     docker-compose -f docker-compose.simple.yml ps"
echo "  • Stop services:    docker-compose -f docker-compose.simple.yml down"
echo "  • Restart service:  docker-compose -f docker-compose.simple.yml restart <service>"
echo ""
echo "Waiting for services to be healthy..."
sleep 10

# Check health
echo ""
echo "Service status:"
docker-compose -f docker-compose.simple.yml ps
echo ""

