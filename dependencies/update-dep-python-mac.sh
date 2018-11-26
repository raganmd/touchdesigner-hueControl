#!/bin/bash 

# fix up pip with python3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Update dependencies

# make sure pip is up to date
python3 -m pip install --upgrade pip

# change current direcotry to where the script is run from
pwd

# pull phue
python3 -m pip install --target="\python" phue
