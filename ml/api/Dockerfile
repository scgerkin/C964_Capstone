FROM continuumio/anaconda3
# TODO: Download server/model from S3 or github so that the image doesn't need to be rebuilt everytime a change is made
ADD server.py /svr/server.py
ADD server-environment.yaml /svr/server-environment.yaml
ADD finding_predictor.pkl /svr/finding_predictor.pkl
ENV UPLOAD_PATH=/tmp
ENV MODEL_PATH=/svr/finding_predictor.pkl
RUN conda env create -f /svr/server-environment.yaml
RUN conda init bash
CMD /opt/conda/envs/server-env/bin/python /svr/server.py
