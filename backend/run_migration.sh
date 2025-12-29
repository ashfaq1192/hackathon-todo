#!/bin/bash
# Script to run database migrations on Railway
# This can be executed via Railway's web terminal or CLI

echo "Running priority enum case fix migration..."
python migrations/003_fix_priority_enum_case.py
