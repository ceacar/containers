from ceacar/exp:simple_base
#FROM ubuntu
# RUN pip install --upgrade pip
# TODO: doesn't know how to solve pip3 not grade issue
#RUN pip3 install --upgrade setuptools pip
RUN pip3 install apache-airflow
RUN airflow initdb
RUN mkdir -p /var/log/airflow
COPY scripts/start_airflow /usr/local/bin/

WORKDIR /root/airflow
RUN apt-get install -y dnsutils
# ENTRYPOINT ["./start_airflow"]
#ENTRYPOINT ["start_airflow"]
CMD ["start_airflow"]
