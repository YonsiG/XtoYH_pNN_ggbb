#!/usr/bin/env bash

set -x
set -e

if [ -d ${PWD}/tmp ]; then 
	rm -r ${PWD}/tmp
fi

mkdir ${PWD}/tmp
export TMPDIR=${PWD}/tmp #in case the default tmp dir is not big enough to install pytorch

python3 -m venv env
source env/bin/activate

pip install --upgrade pip

pip install tqdm
pip install matplotlib
pip install mplhep
pip install numba
pip install numpy
pip install pandas
pip install pyarrow
pip install scikit-learn
pip install scipy
pip install tensorboard
pip install torch
pip install torchviz
pip install uproot
pip install xgboost==1.2.1

# pip install -r requirements.txt

rm -r ${PWD}/tmp
