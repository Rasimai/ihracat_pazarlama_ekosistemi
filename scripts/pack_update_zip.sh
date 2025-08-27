#!/usr/bin/env bash
set -euo pipefail
mkdir -p dist
NAME=ipe
VER=${1:-v0.1.0}
ZIP="dist/${NAME}_${VER}.zip"
rm -f "$ZIP"
zip -r "$ZIP" \
  apps agents api core state \
  Dockerfile docker-compose.yml requirements.txt manifest.json README.md .env.example \
  -x "state/db.sqlite" -x "__pycache__/*" -x "*/__pycache__/*"
shasum -a 256 "$ZIP" > "dist/sha256.txt"
echo "Built $ZIP"
