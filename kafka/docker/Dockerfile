from ceacar/exp:simple_base

RUN mkdir -p /root/kafka/configs
WORKDIR /root/kafka
RUN curl -O http://apache-mirror.8birdsvideo.com/kafka/2.4.0/kafka_2.12-2.4.0.tgz
RUN tar -xzf kafka_2.12-2.4.0.tgz
RUN cd kafka_2.12-2.4.0
WORKDIR /root/kafka/kafka_2.12-2.4.0
COPY ./scripts/start_kafka_instance /root/kafka/kafka_2.12-2.4.0/start_kafka_instance
COPY ./configs/server.properties /root/kafka/configs/server.properties
RUN apt-get -y install kafkacat
CMD ["./start_kafka_instance"]
