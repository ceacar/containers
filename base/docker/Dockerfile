FROM ubuntu

# declare of env variable from docker build command
ARG docker_build_path=local

# disable interactive mode since cassandra will promp for timezone information
ENV DEBIAN_FRONTEND noninteractive

ENV DOCKER_BUILD_PATH=${docker_build_path}

# install dependencies for curl cmd and curl cmd itself
RUN apt-get update && apt-get install -y python3 python-pip python3-pip

# add tools for common troubleshoot
RUN apt-get install -y vim less htop tmux screen curl iputils-ping iproute2 dnsutils git netcat maven
RUN pip install --upgrade pip
RUN pip3 install git+https://github.com/ceacar/excalibur
RUN apt-get clean && apt-get update && apt-get install -y default-jdk
