FROM continuumio/anaconda3
RUN mkdir /svr
RUN curl https://raw.githubusercontent.com/scgerkin/C964_Capstone/main/ml/api/start.sh > /svr/start.sh
RUN chmod +x /svr/start.sh
ADD server-environment.yaml /svr/server-environment.yaml
RUN conda env create -f /svr/server-environment.yaml
RUN conda init bash
CMD /bin/bash /svr/start.sh
