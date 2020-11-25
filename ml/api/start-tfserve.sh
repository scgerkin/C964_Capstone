#!/bin/bash

# Will need to copy `./ml/models/save/dx-classifier` to ~/ml on
#    server, and allow ingress on 8500 for gRPC and 8501 for REST.

export ML_PATH=$HOME/ml
docker run -it --rm \
 -p 8500:8500 \
 -p 8501:8501 \
 -v "$ML_PATH/dx-classifier:/models/dx-classifier" \
 -e MODEL_NAME=dx-classifier \
 tensorflow/serving