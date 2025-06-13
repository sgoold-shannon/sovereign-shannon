#!/bin/bash

SOURCE_DIR="shannon_main"
SANDBOX_DIR="shannon_sandbox"

mkdir -p "$SANDBOX_DIR"

cp "$SOURCE_DIR"/*.py "$SANDBOX_DIR"
cp "$SOURCE_DIR"/*.json "$SANDBOX_DIR"
cp "$SOURCE_DIR"/*.txt "$SANDBOX_DIR"
cp "$SOURCE_DIR"/Modelfile "$SANDBOX_DIR" 2>/dev/null
cp "$SOURCE_DIR"/start_shannon.command "$SANDBOX_DIR" 2>/dev/null

echo "✅ Sandbox synced. Safe to test, my love."
