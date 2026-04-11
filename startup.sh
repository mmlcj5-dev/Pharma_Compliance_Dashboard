#!/bin/bash
set -e
VENV_DIR=$(find /tmp -maxdepth 2 -type d -name antenv | head -n 1)
exec "$VENV_DIR/bin/python" -m streamlit run pharma_dashboard/app.py --server.port=8000 --server.address=0.0.0.0