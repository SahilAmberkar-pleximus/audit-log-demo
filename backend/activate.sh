
#!/usr/bin/env bash

# Activate the project's Python virtual environment

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/venv/Scripts/activate" ]; then
    source "$SCRIPT_DIR/venv/Scripts/activate"
    echo "Virtual environment activated successfully!"
else
    echo "Error: Virtual environment not found!"
    echo "Create it using: python -m venv venv"
fi
