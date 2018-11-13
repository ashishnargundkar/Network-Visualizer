#!/bin/bash
sudo apt-get install curl
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install -y mongodb

pip3 install --user virtualenv
python3 -m virtualenv $VIS_DIR/venv
source $VIS_DIR/venv/bin/activate
pip3 install -r Requirements.txt
deactivate

source $VIS_DIR/npm_setup.sh
ln -s `pwd`/visualizer.sh $VIS_DIR/visualizer
chmod +x $VIS_DIR/visualizer
