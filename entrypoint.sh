#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

if [ "$1" = "uvicorn" ]; then
    echo "=== Running startup setup tasks ==="
    echo "Building/updating the FAISS index..."
    python index/build_index.py
    echo "=== Startup setup tasks complete ==="
else
    echo "=== Skipping index build for non-server container ==="
fi

echo "Starting command: $@"
exec "$@"
