FROM continuumio/anaconda3
ADD server.py /svr/server.py
ADD server-environment.yaml /svr/server-environment.yaml
ADD finding_predictor.pkl /svr/finding_predictor.pkl
ENV UPLOAD_PATH=/tmp
ENV MODEL_PATH=/svr/finding_predictor.pkl
ENV TF_SERVE_URL=http://localhost:8501/v1/models/dx-classifier:predict
RUN conda env create -f /svr/server-environment.yaml
RUN conda init bash
CMD /opt/conda/envs/server-env/bin/python /svr/server.py
