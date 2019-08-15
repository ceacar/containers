FROM ubuntu

# disable interactive mode since cassandra will promp for timezone information
ENV DEBIAN_FRONTEND noninteractive

# install dependencies for curl cmd and curl cmd itself
RUN apt-get update && apt-get install -y curl gnupg2
RUN echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | tee -a /etc/apt/sources.list.d/cassandra.sources.list
RUN curl https://www.apache.org/dist/cassandra/KEYS | apt-key add -

# install cassandra
# TODO: cassandra wants to setup demographic for its timezone, what to solve this issue
RUN apt-get update && apt-get install -y cassandra

# add tools for common troubleshoot
RUN apt-get install -y vim less htop

# you may see /etc/init.d/cassandra: 72: ulimit: error setting limit (Operation not permitted), it is script try to set ulimit
# docker doesn't allow this operation
# ENTRYPOINT ["service", "cassandra", "start"]
