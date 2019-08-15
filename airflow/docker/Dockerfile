FROM ubuntu

# declare of env variable from docker build command
ARG docker_build_path=local

# disable interactive mode since cassandra will promp for timezone information
ENV DEBIAN_FRONTEND noninteractive

ENV DOCKER_BUILD_PATH=${docker_build_path}

# install dependencies for curl cmd and curl cmd itself
RUN apt-get update && apt-get install -y python3 python-pip

# add tools for common troubleshoot
RUN apt-get install -y vim less htop tmux screen curl

# you may see /etc/init.d/cassandra: 72: ulimit: error setting limit (Operation not permitted), it is script try to set ulimit
RUN pip install --upgrade pip
RUN pip install apache-airflow
RUN airflow initdb
RUN mkdir -p /var/log/airflow
COPY scripts/start_airflow /usr/local/bin/

WORKDIR /root/airflow
RUN apt-get install -y dnsutils
# ENTRYPOINT ["./start_airflow"]
#ENTRYPOINT ["start_airflow"]
CMD ["start_airflow"]
