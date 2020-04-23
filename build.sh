#!/bin/bash

# del cache files
find ankipo -name "__pycache__" -print0 | xargs -0 -r -I{} rm -r {}
# remove old package
rm ankipo.ankiaddon || true
# create zip
cd ankipo && zip -r ../ankipo.ankiaddon *
