#!/bin/bash

cd $VIS_DIR/setup
pip3 install --user virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r Requirements.txt
deactivate

source npm_setup.sh
ln -s visualizer.sh $VIS_DIR/visualizer
chmod +x $VIS_DIR/visualizer
