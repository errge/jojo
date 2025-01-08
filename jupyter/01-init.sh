#!/bin/bash

set -xeuo pipefail

cd $(dirname $(readlink -f "$0"))

export UV_INSTALL_DIR=$PWD/.venv/uv
export UV_PYTHON_INSTALL_DIR=$PWD/.venv/python
export UV_PYTHON_PREFERENCE=only-managed
export UV_CACHE_DIR=$PWD/.venv-cache
export UV_NO_CONFIG=1
export UV_NO_ENV_FILE=1
export UV_TOOL_DIR=$PWD/.venv/tools

rm -rf .venv

# Install uv in a temporary directory for bootstrap
virtualenv .venv/bootstrap
.venv/bootstrap/bin/pip install uv
mv .venv/bootstrap/bin/uv .venv
rm -rf .venv/bootstrap

# Install our own python
.venv/uv python install -i .venv/python 3.13

# The venv that we will actually use
.venv/uv venv --allow-existing -n .venv
.venv/uv sync

# Needed for PDF generation
.venv/bin/playwright install chromium

# micromamba is needed for jupyter build
curl -sL -o .venv/bin/micromamba https://github.com/mamba-org/micromamba-releases/releases/download/2.0.5-0/micromamba-linux-64
chmod a+x .venv/bin/micromamba
