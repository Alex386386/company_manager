#!/bin/sh

echo "Waiting for postgres..."
sleep 3
uvicorn auth_main:app --host 0.0.0.0 --port 8000