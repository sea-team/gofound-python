#!/usr/bin/env bash
echo 'release gofound'
rm -rf dist/*
python3 setup.py sdist
twine upload dist/*
echo 'gofound upload success!'