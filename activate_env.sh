#!/bin/bash
# Script to activate the Python 3.11 environment

echo "Activating Python 3.11 environment..."

# Set up pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"

# Activate virtual environment
source venv/bin/activate

echo "✓ Python 3.11 environment activated!"
echo "Python version: $(python --version)"
echo "Virtual environment: $(which python)"
echo ""
echo "To deactivate, run: deactivate" 