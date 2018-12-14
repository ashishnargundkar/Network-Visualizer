#!/bin/bash

cd $VIS_DIR
pip3 install --user virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r Requirements.txt
deactivate
