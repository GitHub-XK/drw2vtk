#!/bin/bash

pip uninstall drw2vtk
python setup.py clean
rm dist/*
python setup.py sdist
pip install -e .
