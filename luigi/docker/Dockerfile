from ceacar/exp:simple_base

RUN mkdir -p /root/luigi/log
WORKDIR /root/luigi
RUN pip install luigi
COPY ./scripts/start_luigi_scheduler /root/luigi/start_luigi_scheduler
COPY ./configs/luigi.cfg /root/luigi/luigi.cfg
COPY ./scripts/luigi_test.py /root/luigi/luigi_test.py
RUN export PYTHONPATH=$PYTHON:$PWD
CMD ["./start_luigi_scheduler"]
