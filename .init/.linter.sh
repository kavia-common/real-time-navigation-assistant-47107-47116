#!/bin/bash
cd /home/kavia/workspace/code-generation/real-time-navigation-assistant-47107-47116/navigation_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

