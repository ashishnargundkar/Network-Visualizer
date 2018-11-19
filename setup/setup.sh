#!/bin/bash

pip3 install --user virtualenv
python3 -m virtualenv $VIS_DIR/venv
source $VIS_DIR/venv/bin/activate
pip3 install -r Requirements.txt
deactivate

source $VIS_DIR/setup/npm_setup.sh
ln -s $VIS_DIR/setup/visualizer.sh $VIS_DIR/visualizer
chmod +x $VIS_DIR/visualizer
