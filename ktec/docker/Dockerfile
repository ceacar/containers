from ceacar/exp:simple_base

RUN useradd -ms /bin/bash ktec
RUN mkdir -p /plugin/ktec
RUN chmod 777 -R /plugin
USER ktec

# installs kafka for a script in kafka's bin dir
RUN mkdir -p /home/ktec/kafka/configs
WORKDIR /home/ktec/kafka
RUN curl -O http://apache-mirror.8birdsvideo.com/kafka/2.4.0/kafka_2.12-2.4.0.tgz
RUN tar -xzf kafka_2.12-2.4.0.tgz
RUN cd kafka_2.12-2.4.0

# install kafka to elasticsearch connector from git source
WORKDIR /home/ktec
RUN git clone -b 0.10.0.0 https://github.com/confluentinc/kafka-connect-elasticsearch.git
WORKDIR /home/ktec/kafka-connect-elasticsearch

# build with all dependencies, if not, it will error out
COPY ./configs/pom.xml /home/ktec/kafka-connect-elasticsearch/pom.xml
RUN chmod 755 /home/ktec/kafka-connect-elasticsearch/pom.xml
RUN mvn clean package

RUN cp /home/ktec/kafka-connect-elasticsearch/target/kafka-connect-elasticsearch-3.2.0-SNAPSHOT-jar-with-dependencies.jar /plugin/ktec/


# copy connector configs
RUN mkdir -p /home/ktec/ktec_configs
COPY ./configs/connect-standalone.properties /home/ktec/ktec_configs/connect-standalone.properties
COPY ./configs/elasticsearch-connect.properties /home/ktec/ktec_configs/elasticsearch-connect.properties
RUN chmod 755 /home/ktec/ktec_configs/connect-standalone.properties
RUN chmod 755 /home/ktec/ktec_configs/elasticsearch-connect.properties
# remove this jar without dependeices, it will confuse java
RUN rm ./target/kafka-connect-elasticsearch-3.2.0-SNAPSHOT.jar
# ENV CLASSPATH /home/ktec/kafka-connect-elasticsearch/target/kafka-connect-elasticsearch-3.2.0-SNAPSHOT.jar
ENV CLASSPATH /home/ktec/kafka-connect-elasticsearch/target

# CMD ["/home/ktec/kafka/kafka_2.12-2.4.0/bin/connect-standalone.sh /home/ktec/ktec_configs/connect-standalone.properties /home/ktec/ktec_configs/elasticsearch-connect.properties"]
CMD ["/bin/bash -c 'sleep 9999999999'"]
