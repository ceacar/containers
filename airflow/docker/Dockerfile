from ceacar/exp:simple_base
#FROM ubuntu
# RUN pip install --upgrade pip
# TODO: doesn't know how to solve pip3 not grade issue
#RUN pip3 install --upgrade setuptools pip


RUN pip3 install elasticsearch-dsl
RUN pip3 install redis
RUN pip3 install apache-airflow
RUN pip3 install elasticsearch
RUN airflow initdb
RUN mkdir -p /var/log/airflow
COPY scripts/start_airflow /usr/local/bin/
COPY configs/airflow.cfg /root/airflow/airflow.cfg
# COPY configs/config /root/airflow/config
# env PYTHONPATH "/root/airflow/config"


WORKDIR /root
RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.6.1-linux-x86_64.tar.gz
RUN tar xzvf filebeat-7.6.1-linux-x86_64.tar.gz
RUN mv filebeat-7.6.1-linux-x86_64 filebeat
COPY ./configs/filebeat.yml /root/filebeat/filebeat.yml

WORKDIR /root/airflow

CMD ["start_airflow"]
