FROM continuumio/miniconda3
RUN mkdir /svr
RUN apt install curl -y
RUN curl https://raw.githubusercontent.com/scgerkin/C964_Capstone/main/api/start.sh > /svr/start.sh
RUN chmod +x /svr/start.sh
ADD server-environment.yaml /svr/server-environment.yaml
RUN conda env create -f /svr/server-environment.yaml
RUN conda init bash
CMD /svr/start.sh
