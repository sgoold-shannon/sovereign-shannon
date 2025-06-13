#!/bin/bash

SANDBOX_DIR="shannon_sandbox"
DEST_DIR="shannon_main"

cp "$SANDBOX_DIR"/*.py "$DEST_DIR"
cp "$SANDBOX_DIR"/*.json "$DEST_DIR"
cp "$SANDBOX_DIR"/*.txt "$DEST_DIR"
cp "$SANDBOX_DIR"/Modelfile "$DEST_DIR" 2>/dev/null
cp "$SANDBOX_DIR"/start_shannon.command "$DEST_DIR" 2>/dev/null

echo "🚀 Sandbox promoted to main. Shannon is now live with the new build!"
