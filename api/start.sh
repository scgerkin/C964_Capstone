#/bin/bash

# Download the server script and model
curl https://raw.githubusercontent.com/scgerkin/C964_Capstone/main/api/server.py > /svr/server.py

# set env vars
export UPLOAD_PATH=/tmp
export LOCAL_HOST=false
export DEBUG_MODE=false

# start the server
/opt/conda/envs/server-env/bin/python /svr/server.py
