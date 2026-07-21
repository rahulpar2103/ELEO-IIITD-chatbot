#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

case "$1" in
    *uvicorn*)
        echo "=== Running startup setup tasks ==="
        echo "Building/updating the FAISS index..."
        python index/build_index.py
        echo "=== Startup setup tasks complete ==="
        ;;
    *)
        echo "=== Skipping index build for non-server container ==="
        ;;
esac

echo "Starting command: $@"
exec "$@"
