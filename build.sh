#!/usr/bin/env bash

# Update OS and install compilers and cmake
apt-get update && apt-get install -y cmake build-essential

# Upgrade pip to latest version
pip install --upgrade pip

# Install Python packages from requirements.txt
pip install -r requirements.txt
