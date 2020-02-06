from ceacar/exp:simple_base

RUN mkdir -p /root/luigi/log
WORKDIR /root/luigi
RUN pip install luigi
RUN pip install kafka-python
COPY ./scripts/start_luigi_scheduler /root/luigi/start_luigi_scheduler
COPY ./configs/luigi.cfg /root/luigi/luigi.cfg
COPY ./tests /root/tests
COPY ./scripts/luigi_test.py /root/tests/luigi_test.py
ENV PYTHONPATH "${PYTHONPATH}:/root/tests"
RUN apt-get -y install kafkacat
CMD ["./start_luigi_scheduler"]
