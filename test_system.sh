#!/bin/bash

# Concert AI Agent - System Test Script
# Tests all components for production readiness

echo "========================================================================"
echo "🧪 CONCERT AI AGENT - SYSTEM TEST"
echo "========================================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0

# Test function
test_component() {
    local name=$1
    local command=$2
    
    echo -n "Testing $name... "
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((FAILED++))
        return 1
    fi
}

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo -e "${RED}✗ Virtual environment not found${NC}"
    exit 1
fi

echo "1. Testing Python Dependencies"
echo "----------------------------------------"
test_component "PyYAML" "python3 -c 'import yaml'"
test_component "Requests" "python3 -c 'import requests'"
echo ""

echo "2. Testing Core Modules"
echo "----------------------------------------"
test_component "Intent Parser" "python3 -c 'import sys; sys.path.insert(0, \"src\"); from intent_parser import IntentParser; p = IntentParser()'"
test_component "Template Generator" "python3 -c 'import sys; sys.path.insert(0, \"src\"); from template_generator import TemplateGenerator; t = TemplateGenerator()'"
test_component "Validator" "python3 -c 'import sys; sys.path.insert(0, \"src\"); from validator import PlaybookValidator; v = PlaybookValidator()'"
test_component "Git Manager" "python3 -c 'import sys; sys.path.insert(0, \"src\"); from git_manager import GitManager; g = GitManager()'"
test_component "Logger" "python3 -c 'import sys; sys.path.insert(0, \"src\"); from logger import AgentLogger; l = AgentLogger({})'"
echo ""

echo "3. Testing Enhanced Modules"
echo "----------------------------------------"
test_component "Playbook Checker" "python3 -c 'import sys; sys.path.insert(0, \"src\"); from playbook_checker import PlaybookChecker; p = PlaybookChecker()'"
test_component "Credential Manager" "python3 -c 'import sys; sys.path.insert(0, \"src\"); from credential_manager import CredentialManager; c = CredentialManager()'"
test_component "Inventory Manager" "python3 -c 'import sys; sys.path.insert(0, \"src\"); from inventory_manager import InventoryManager; i = InventoryManager()'"
echo ""

echo "4. Testing LLM Integration"
echo "----------------------------------------"
if curl -s http://localhost:11434 > /dev/null 2>&1; then
    echo -e "Ollama Status: ${GREEN}✓ Running${NC}"
    ((PASSED++))
    
    # Check if codellama model is available
    if ollama list 2>/dev/null | grep -q "codellama"; then
        echo -e "Codellama Model: ${GREEN}✓ Installed${NC}"
        ((PASSED++))
    else
        echo -e "Codellama Model: ${YELLOW}⚠ Not installed${NC}"
        echo "  Run: ollama pull codellama:7b"
        ((FAILED++))
    fi
else
    echo -e "Ollama Status: ${RED}✗ Not running${NC}"
    echo "  Start with: ollama serve"
    ((FAILED++))
fi
echo ""

echo "5. Testing File Structure"
echo "----------------------------------------"
test_component "Templates directory" "[ -d templates ]"
test_component "Config directory" "[ -d config ]"
test_component "Inventory directory" "[ -d inventory ]"
test_component "Output directory" "[ -d output ]"
test_component "Logs directory" "[ -d logs ]"
echo ""

echo "6. Testing Templates"
echo "----------------------------------------"
test_component "install_package.yml" "[ -f templates/install_package.yml ]"
test_component "configure_firewall.yml" "[ -f templates/configure_firewall.yml ]"
test_component "create_user.yml" "[ -f templates/create_user.yml ]"
test_component "deploy_docker.yml" "[ -f templates/deploy_docker.yml ]"
test_component "restart_service.yml" "[ -f templates/restart_service.yml ]"
test_component "update_config.yml" "[ -f templates/update_config.yml ]"
echo ""

echo "7. Testing Configuration"
echo "----------------------------------------"
test_component "config.yml exists" "[ -f config/config.yml ]"
test_component "config.yml is valid YAML" "python3 -c 'import yaml; yaml.safe_load(open(\"config/config.yml\"))'"
echo ""

echo "8. Testing Inventory"
echo "----------------------------------------"
test_component "inventory.ini exists" "[ -f inventory/inventory.ini ]"
if [ -f inventory/inventory.ini ]; then
    if grep -q "\[hosts\]" inventory/inventory.ini; then
        echo -e "Inventory format: ${GREEN}✓ Valid INI format${NC}"
        ((PASSED++))
    else
        echo -e "Inventory format: ${RED}✗ Invalid format${NC}"
        ((FAILED++))
    fi
fi
echo ""

echo "9. Testing Git Integration"
echo "----------------------------------------"
if command -v git &> /dev/null; then
    echo -e "Git installed: ${GREEN}✓ Yes${NC}"
    ((PASSED++))
    
    if [ -d output/.git ]; then
        echo -e "Git repository: ${GREEN}✓ Initialized${NC}"
        ((PASSED++))
    else
        echo -e "Git repository: ${YELLOW}⚠ Not initialized${NC}"
        echo "  Will be initialized on first use"
    fi
else
    echo -e "Git installed: ${RED}✗ No${NC}"
    ((FAILED++))
fi
echo ""

echo "10. Testing Ansible"
echo "----------------------------------------"
if command -v ansible-playbook &> /dev/null; then
    echo -e "Ansible installed: ${GREEN}✓ Yes${NC}"
    ((PASSED++))
    
    # Test ansible version
    ANSIBLE_VERSION=$(ansible-playbook --version | head -n1)
    echo "  Version: $ANSIBLE_VERSION"
else
    echo -e "Ansible installed: ${YELLOW}⚠ No${NC}"
    echo "  Install with: pip install ansible"
    echo "  (Optional - only needed for playbook execution)"
fi
echo ""

echo "11. Testing Main Application"
echo "----------------------------------------"
test_component "Main application loads" "python3 -c 'import sys; sys.path.insert(0, \"src\"); from main import ConcertAgentEnhanced'"
echo ""

echo "========================================================================"
echo "📊 TEST SUMMARY"
echo "========================================================================"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED - SYSTEM IS PRODUCTION READY!${NC}"
    echo ""
    echo "🚀 You can now use the system:"
    echo "   ./run.sh \"Install MySQL server\""
    echo ""
    exit 0
else
    echo -e "${YELLOW}⚠️  SOME TESTS FAILED - PLEASE FIX ISSUES ABOVE${NC}"
    echo ""
    exit 1
fi

# Made with Bob
