#!/bin/bash

# Concert AI Agent - Production Startup Script

echo "========================================================================"
echo "🤖 CONCERT AI AGENT - Production System v3.0"
echo "========================================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import yaml" 2>/dev/null; then
    echo ""
    echo "📦 Installing dependencies..."
    pip install -q -r requirements.txt
    echo "✓ Dependencies installed"
fi

# Check Ollama
echo ""
echo "Checking Ollama..."
if command -v ollama &> /dev/null; then
    if ollama list | grep -q "codellama"; then
        echo "✓ Ollama detected with codellama model"
    else
        echo "⚠️  Ollama found but codellama model not installed"
        echo "Run: ollama pull codellama:7b"
    fi
else
    echo "⚠️  Ollama not found (optional for LLM features)"
fi

# Check Git
echo ""
echo "Checking Git..."
if command -v git &> /dev/null; then
    echo "✓ Git detected"
else
    echo "⚠️  Git not found (required for version control)"
fi

# Check Ansible
echo ""
echo "Checking Ansible..."
if command -v ansible-playbook &> /dev/null; then
    echo "✓ Ansible detected"
else
    echo "⚠️  Ansible not found (required for playbook execution)"
    echo "Install: pip install ansible"
fi

echo ""
echo "========================================================================"
echo "🚀 Starting Concert AI Agent..."
echo "========================================================================"
echo ""

# Run the application
if [ $# -eq 0 ]; then
    # Interactive mode
    python3 src/main.py
else
    # Command line mode
    python3 src/main.py "$@"
fi

# Made with Bob
