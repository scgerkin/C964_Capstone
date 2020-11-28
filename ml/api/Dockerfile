FROM continuumio/miniconda3
RUN mkdir /svr
RUN apt install curl -y
RUN curl https://raw.githubusercontent.com/scgerkin/C964_Capstone/main/ml/api/server.py > /svr/server.py
RUN curl https://raw.githubusercontent.com/scgerkin/C964_Capstone/main/ml/api/finding_predictor.pkl > /svr/finding_predictor.pkl
ENV UPLOAD_PATH=/tmp
ENV MODEL_PATH=/svr/finding_predictor.pkl
ENV LOCAL_HOST=false
ENV DEBUG_MODE=false
ADD server-environment.yaml /svr/server-environment.yaml
RUN conda env create -f /svr/server-environment.yaml
RUN conda init bash
CMD /opt/conda/envs/server-env/bin/python /svr/server.py
