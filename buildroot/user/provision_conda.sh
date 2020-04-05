#!/usr/bin/env bash

#
# generate project environment
#

set -e

eval "$(conda shell.bash hook)"

# project enviro
conda env remove -y -n builder-marlin
conda create     -y -n builder-marlin python=3.8

conda activate         builder-marlin

# project deps
conda install -y \
    -c conda-forge \
    pip \

pip install --upgrade platformio
