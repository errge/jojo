#!/bin/bash

set -xeuo pipefail

. .venv/bin/activate
rm -rf .jupyterlite.doit.db _output
jupyter lite build --no-sourcemaps
