#!/bin/bash

set -xeuo pipefail

. .venv/bin/activate
cd _output
python -m http.server
