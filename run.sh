#!/bin/bash
echo "Starting tokenization service..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000