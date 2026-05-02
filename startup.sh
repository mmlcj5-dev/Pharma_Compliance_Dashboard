#!/bin/bash
set -e

# Locate the virtual environment created by Oryx
VENV_DIR=$(find /tmp -maxdepth 2 -type d -name antenv | head -n 1)

# Safety check
if [ -z "$VENV_DIR" ]; then
  echo "ERROR: Could not find antenv virtual environment under /tmp"
  exit 1
fi

# Launch Streamlit using the venv's Python
exec "$VENV_DIR/bin/python" -m streamlit run pharma_dashboard/app.py --server.port=8000 --server.address=0.0.0.0