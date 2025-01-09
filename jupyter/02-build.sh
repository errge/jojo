#!/bin/bash

set -xeuo pipefail

. .venv/bin/activate
rm -rf .jupyterlite.doit.db _output contents-ipynb
mkdir -p contents-ipynb
for f in contents/*.py; do
    jupytext --set-kernel python3 --execute --to ipynb -o contents-ipynb/$(basename $f .py).ipynb $f
    jupyter nbconvert --to webpdf contents-ipynb/$(basename $f .py).ipynb

    # Evaluated ipynbs can be very big, we already have the PDF, let's delete the evaluation
    rm contents-ipynb/$(basename $f .py).ipynb
    # Set kernel to xpython, so user doesn't have to select
    jupytext --update-metadata '{"kernelspec":{"name":"xpython"}}' --to ipynb -o contents-ipynb/$(basename $f .py).ipynb $f
done
jupyter lite build --no-sourcemaps --contents contents-ipynb
