#!/bin/bash

# Exit on error
set -e

# Clean previous builds
rm -rf dist/
rm -rf build/
rm -rf *.egg-info

# Install poetry-dynamic-versioning if not already installed
poetry self add poetry-dynamic-versioning

# Build with dynamic versioning
poetry build

# Publish to PyPI
poetry publish --username antonkulaga --build

echo "Package published successfully!"
