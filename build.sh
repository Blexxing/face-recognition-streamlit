#!/usr/bin/env bash

# Update OS and install compilers and cmake
apt-get update && apt-get install -y cmake build-essential

# Upgrade pip to latest version
pip install --upgrade pip

# Install prebuilt dlib wheel
pip install "dlib==20.0.0" --find-links https://github.com/ageitgey/dlib/releases/tag/v20.0.0

# Install other Python packages from requirements.txt (without dlib)
pip install -r requirements.txt
