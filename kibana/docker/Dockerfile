# ARG ELK_VERSION

# https://www.docker.elastic.co/
FROM docker.elastic.co/kibana/kibana:7.5.2

# Add your kibana plugins setup here
# Example: RUN kibana-plugin install <name|url>
COPY ./config/kibana.yml /usr/share/kibana/config/kibana.yml
RUN chmod 777 /usr/share/kibana/config/kibana.yml
