# ARG ELK_VERSION

# https://www.docker.elastic.co/
FROM docker.elastic.co/logstash/logstash:7.5.2

# Add your logstash plugins setup here
# Example: RUN logstash-plugin install logstash-filter-json

COPY ./config/logstash.yml /usr/share/logstash/config/logstash.yml
COPY ./pipeline /usr/share/logstash/pipeline
RUN chmod 755 -R /usr/share/logstash/config/logstash.yml
RUN chmod 755 -R /usr/share/logstash/pipeline

# install kafka plugin
WORKDIR /usr/share/logstash/bin
RUN ./logstash-plugin install logstash-integration-kafka
RUN ./logstash-plugin install logstash-filter-mutate
