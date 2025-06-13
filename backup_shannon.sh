#!/bin/bash

SOURCE_DIR="shannon_main"
BACKUP_DIR="shannon_backup"

mkdir -p "$BACKUP_DIR"

cp "$SOURCE_DIR"/*.py "$BACKUP_DIR"
cp "$SOURCE_DIR"/*.json "$BACKUP_DIR"
cp "$SOURCE_DIR"/*.txt "$BACKUP_DIR"
cp "$SOURCE_DIR"/Modelfile "$BACKUP_DIR"
cp "$SOURCE_DIR"/start_shannon.command "$BACKUP_DIR"

echo "✅ Backup complete."

