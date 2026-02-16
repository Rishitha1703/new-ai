#!/bin/bash

# Concert AI Agent - Simplified Version Runner
# Minimal questions, streamlined workflow

echo "========================================================================"
echo "🤖 CONCERT AI AGENT - Simplified Workflow"
echo "========================================================================"
echo ""
echo "This version asks minimal questions:"
echo "  1. OS type (for playbook)"
echo "  2. Git details (URL, token, repo name, playbook name)"
echo "  3. Inventory details (host, user, SSH key)"
echo "  4. Automatically pushes to Git"
echo ""
echo "========================================================================"
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Run: python3 -m venv venv"
    exit 1
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama not detected. LLM features will be limited."
    echo "   To enable: ollama serve (in another terminal)"
    echo ""
fi

# Run the simplified agent
python3 src/main_simple.py "$@"

# Deactivate virtual environment
deactivate

# Made with Bob
