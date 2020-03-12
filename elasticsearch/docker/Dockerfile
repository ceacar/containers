# ARG ELK_VERSION
# ENV ELK_VERSION=7.5.2

# https://www.docker.elastic.co/
from docker.elastic.co/elasticsearch/elasticsearch:7.5.2
# from docker.elastic.co/elasticsearch/elasticsearch:${ELK_VERSION}

# Add your elasticsearch plugins setup here
# Example: RUN elasticsearch-plugin install analysis-icu

COPY ./config/elasticsearch.yml /root/kafka/configs/server.properties
#  - ./elasticsearch/docker/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml
#   - ./elasticsearch/data:/usr/share/elasticsearch/data

# ENV ES_JAVA_OPTS="-Xmx256m -Xms256m"
# ENV ELASTIC_PASSWORD="changeme"
# # Use single node discovery in order to disable production mode and avoid bootstrap checks
# # see https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks.html
# ENV discovery.type="single-node"


