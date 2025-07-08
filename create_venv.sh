#!/bin/bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "not found requirements.txt, dependencies not installed."
fi