#!/bin/bash

set -xeuo pipefail

. .venv/bin/activate
rm -rf .jupyterlite.doit.db _output contents-ipynb
mkdir -p contents-ipynb
for f in contents/*.py; do
    jupytext --to ipynb -o contents-ipynb/$(basename $f .py).ipynb $f
done
jupyter lite build --no-sourcemaps --contents contents-ipynb
