#!/usr/bin/env bash
# Build script for 360 Utility Batch Create Extract (Linux)
# Requires: pip install pyinstaller
#           cargo (Rust toolchain) for iso2god and god2iso
#           gcc, libcurl-dev, zlib1g-dev for abgx360

set -e

echo "==> Building iso2god (ISO to GOD converter)..."
cd x_tool/iso2god-rs
cargo build --release
cp target/release/iso2god ../iso2god
cd ../..

echo "==> Building god2iso (GOD to ISO converter)..."
cd x_tool/god2iso-rs
cargo build --release
cp target/release/god2iso ../god2iso
cd ../..

echo "==> Building abgx360 (ISO fix/verify tool)..."
cd x_tool/abgx360-src
./configure --prefix="$(pwd)/install"
make -j"$(nproc)"
cp src/abgx360 ../abgx360
cd ../..

echo "==> Bundling Python application with PyInstaller..."
pyinstaller \
    --onefile \
    --add-data "x_tool:x_tool" \
    --add-data "images:images" \
    --add-data "x_ISO:x_ISO" \
    --name "360 Utility Batch Create Extract v1.2" \
    main.pyw

echo ""
echo "Build complete. Binary is in dist/"
