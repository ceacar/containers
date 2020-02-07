import luigi
import logging
from kafka import KafkaProducer
import json
import traceback
import sys
import socket
import subprocess


"""
All luigi event types:

DEPENDENCY_DISCOVERED= 'event.core.dependency.discovered'
DEPENDENCY_MISSING= 'event.core.dependency.missing'
DEPENDENCY_PRESENT= 'event.core.dependency.present'
BROKEN_TASK= 'event.core.task.broken'
START= 'event.core.start'
PROGRESS= 'event.core.progress'
This event can be fired by the task itself while running. The purpose is for the task to report progress, metadata or any generic info so that event handler listening for this can keep track of the progress of running task.

FAILURE= 'event.core.failure'
SUCCESS= 'event.core.success'
PROCESSING_TIME= 'event.core.processing_time'
TIMEOUT= 'event.core.timeout'
PROCESS_FAILURE= 'event.core.process_failure'
"""


logger = logging.getLogger('luigi')
KAFKA_VERSION = (2, 4)
# producer = KafkaProducer(bootstrap_servers=['localhost:38887'], value_serializer=lambda x: json.dumps(x).encode('utf-8'), api_version=KAFKA_VERSION)
producer = KafkaProducer(bootstrap_servers=['kafka:9092'],  api_version=KAFKA_VERSION)


def format_traceback():
    formatted_traceback = traceback.format_exc()
    return formatted_traceback


def format_error(task, subject, headline, formatted_traceback):
    subject="Luigi: {task} failed scheduling. Host: {host}"
    headline="Will not run {task} or any dependencies due to error in deps() method"
    formatted_subject = subject.format(task=task, host=host)
    formatted_headline = headline.format(task=task, host=host)
    command = subprocess.list2cmdline(sys.argv)
    message = luigi.notifications.format_task_error(formatted_headline, task, command, formatted_traceback)
    return subject + message


@luigi.Task.event_handler(luigi.Event.SUCCESS)
def celebrate_sucess(task):
    print("{} finished".format(task))


@luigi.Task.event_handler(luigi.Event.DEPENDENCY_MISSING)
def alert_err(task):
    # task, formatted_traceback,
    # subject="Luigi: {task} failed scheduling. Host: {host}",
    # headline="Will not run {task} or any dependencies due to error in deps() method",
    # formatted_subject = subject.format(task=task, host=self.host)
    # formatted_headline = headline.format(task=task, host=self.host)
    # command = subprocess.list2cmdline(sys.argv)
    # message = luigi.notifications.format_task_error(formatted_headline, task, command, formatted_traceback)

    producer.send('test', value="Unfulfilled dependencies {}".format(task))
    # producer.send('test', value=subject + message)


@luigi.Task.event_handler(luigi.Event.FAILURE)
def alert_failed_task(task, err):
    # luigi.notifications.generate_email
    import ipdb
    ipdb.set_trace()
    host = socket.gethostname()

    formatted_traceback = format_traceback()
    subject="Luigi: {task} failed scheduling. Host: {host}"
    headline="Will not run {task} or any dependencies due to error in deps() method"

    msg = format_error(task, subject, headline, formatted_traceback)


    producer.send('test', value=msg)

    # msg = "{} failed, err:{}".format(task, str(err))
    # producer.send('test', value=msg)

@luigi.Task.event_handler(luigi.Event.PROCESSING_TIME)
def long_running(task, err):
    producer.send('test', value="{} is running long, {}".format(task, err))

@luigi.Task.event_handler(luigi.Event.TIMEOUT)
def alert_timeout(task):
    producer.send('test', value="timeout " + str(task))

@luigi.Task.event_handler(luigi.Event.PROCESS_FAILURE)
def process_failure(task,err):
    producer.send('test', value="process_failure {} {}".format(task,err))




class Dummy1(luigi.Task):
    has_been_run = False

    def run(self):
        self.has_been_run = True

    def complete(self):
        if self.has_been_run:
            return True
        return False

class Dummy2(Dummy1):
    has_been_run = False
    def requires(self):
        yield Dummy1()


class DummyNeverFinish(Dummy1):
    def run(self):
        import time
        time.sleep(3600)


class Dummy3(Dummy1):
    has_been_run = False
    def requires(self):
        yield Dummy1()
        yield luigi.task.externalize(DummyNeverFinish())

    def run(self):
        super(Dummy3, self).run()
        raise Exception('oof')


class Dummy4(Dummy1):
    has_been_run = False
    def requires(self):
        return []

    def run(self):
        super(Dummy4, self).run()
        raise Exception('oof')
