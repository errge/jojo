#!/bin/bash

set -xeuo pipefail
shopt -s nullglob

. .venv/bin/activate
rm -rf .jupyterlite.doit.db _output contents-ipynb
mkdir -p contents-ipynb
for f in contents/*.py; do
    # notebooks might open local data files, so let's run the executor inside the contents-data directory
    jupytext --set-kernel python3 --execute --run-path $PWD/contents-data --to ipynb -o contents-ipynb/$(basename $f .py).ipynb $f
    jupyter nbconvert --to webpdf contents-ipynb/$(basename $f .py).ipynb

    # Evaluated ipynbs can be very big, we already have the PDF, let's delete the evaluation
    rm contents-ipynb/$(basename $f .py).ipynb
    # Set kernel to xpython, so user doesn't have to select
    jupytext --update-metadata '{"kernelspec":{"name":"xpython"}}' --to ipynb -o contents-ipynb/$(basename $f .py).ipynb $f
done

cp -av contents-data/. contents-ipynb/.
jupyter lite build --no-sourcemaps --contents contents-ipynb
