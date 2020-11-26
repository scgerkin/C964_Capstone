#/bin/bash

# Download the server script and model
curl https://raw.githubusercontent.com/scgerkin/C964_Capstone/main/ml/api/server.py > /svr/server.py
curl https://raw.githubusercontent.com/scgerkin/C964_Capstone/main/ml/api/finding_predictor.pkl > /svr/finding_predictor.pkl

# set env vars
export UPLOAD_PATH=/tmp
export MODEL_PATH=/svr/finding_predictor.pkl

# start the server
/opt/conda/envs/server-env/bin/python /svr/server.py
