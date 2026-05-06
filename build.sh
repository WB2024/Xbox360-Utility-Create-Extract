#!/usr/bin/env bash
# Build script for 360 Utility Batch Create Extract (Linux)
# Requires: pip install pyinstaller

set -e

pyinstaller \
    --onefile \
    --add-data "x_tool:x_tool" \
    --add-data "images:images" \
    --add-data "x_ISO:x_ISO" \
    --name "360 Utility Batch Create Extract v1.2" \
    main.pyw

echo ""
echo "Build complete. Binary is in dist/"
