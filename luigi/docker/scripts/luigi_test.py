"""
All luigi event types:
DEPENDENCY_DISCOVERED= 'event.core.dependency.discovered'
DEPENDENCY_MISSING= 'event.core.dependency.missing'
DEPENDENCY_PRESENT= 'event.core.dependency.present'
BROKEN_TASK= 'event.core.task.broken'
START= 'event.core.start'
PROGRESS= 'event.core.progress'
This event can be fired by the task itself while running. The purpose is for the task to report progress,
metadata or any generic info so that event handler listening for this can keep track of the progress of running task.

FAILURE= 'event.core.failure'
SUCCESS= 'event.core.success'
PROCESSING_TIME= 'event.core.processing_time'
TIMEOUT= 'event.core.timeout'
PROCESS_FAILURE= 'event.core.process_failure'
"""


import luigi
import logging
from kafka import KafkaProducer
import json
import traceback
import sys
import socket
import subprocess
import datetime


logger = logging.getLogger('luigi')
KAFKA_VERSION = (2, 4)
producer = KafkaProducer(bootstrap_servers=['kafka:9092'],  api_version=KAFKA_VERSION)
KAFKA_TOPIC = "test"


def get_ts_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def message_kafka(type_str, task, msg, extra_fields={}):
    dict_to_send = {}
    dict_to_send["ts"] = get_ts_now()
    dict_to_send["type"] = type_str
    dict_to_send["message"] = msg
    dict_to_send["task"] = str(task)
    dict_to_send.update(extra_fields)
    send_msg_to_kafk(json.dumps(dict_to_send))


def send_msg_to_kafk(msg):
    try:
        logger.warning("sending {}".format(msg))
        producer.send(KAFKA_TOPIC, value=msg)
    except Exception:
        logger.wanring("failed to send to kafka")


def format_traceback():
    formatted_traceback = traceback.format_exc()
    return formatted_traceback


def format_error(task, subject, headline, formatted_traceback):
    host = socket.gethostname()
    formatted_subject = subject.format(task=task, host=host)
    formatted_headline = headline.format(task=task)
    command = subprocess.list2cmdline(sys.argv)
    message = luigi.notifications.format_task_error(formatted_headline, task, command, formatted_traceback)
    return ''.join([formatted_subject, message]).strip('\n')


def format_time(time_spent):
    """
    time_spent: float
    """
    mon, sec = divmod(time_spent, 60)
    hr, mon = divmod(mon, 60)
    return "%d:%02d:%02d" % (hr, mon, sec)


"""
Luigi: DummyNeverFinish() failed scheduling.
Host: luigi_hostWill not run DummyNeverFinish() or any dependencies due to error in deps()
method Name: DummyNeverFinish Parameters:
    Command line: /usr/local/bin/luigi --local-scheduler --module luigi_test DummyNeverFinish Traceback (most recent call last):
    File "/usr/local/lib/python2.7/dist-packages/luigi/worker.py", line 184, in run raise RuntimeError('Unfulfilled %s at run time: %s' % (deps, ', '.join(missing)))
RuntimeError: Unfulfilled dependency at run time: DummyRunsForever__99914b932b
"""


def extract_dependency_classes(err_message):
    depended_on_class = "CannotParseDependency"
    try:
        res = err_message.split("Unfulfilled dependency at run time:")
        depended_on_class = '_'.join(res[-1].split('_')[:-1]).strip('_')
    except Exception:
        pass
    return depended_on_class


@luigi.Task.event_handler(luigi.Event.FAILURE)
def alert_failed_task(task, err):
    """
    alerts when task failed
    """

    extra_json_fields = {}
    # host = socket.gethostname()
    formatted_traceback = format_traceback()
    subject = "Luigi: {task} failed scheduling. Host: {host}"
    headline = "Will not run {task} or any dependencies due to error in deps() method"
    msg = format_error(task, subject, headline, formatted_traceback)

    type_str = "Failed"
    if "Unfulfilled dependency at run time:" in msg:
        type_str = "Unfulfilled Dependencies"
        depended_on_class = extract_dependency_classes(msg)
        extra_json_fields["dependency_missing"] = depended_on_class
    message_kafka(type_str, task, msg, extra_fields=extra_json_fields)


@luigi.Task.event_handler(luigi.Event.PROCESSING_TIME)
def task_time_handler(task, time_spent):
    """
    keeps track of how long a task took
    task, class, class of the task
    time_spent, float, time spent for task
    """
    tm = format_time(time_spent)
    msg = "{task} finished; time took: {time}".format(task=task, time=tm)
    message_kafka("Task Finished", task, msg)

# ==========================END OF WHAT WORKS==============================


# cannot recreate this
@luigi.Task.event_handler(luigi.Event.PROCESS_FAILURE)
def process_failure(task, err):
    """
    alerts when a process failed
    """
    msg = "{} process failure {}".format(task, err)
    message_kafka("Process Failed", task, msg)


# def format_unfulfilled_dependencies_message(task, subject, headline, formatted_traceback):
#     subject="Luigi: {task} FAILED. Host: {host}",
#     headline="A task failed when running. Most likely run() raised an exception.",
#     msg = format_error(task, subject, headline, formatted_traceback)
#     return msg


# we don't really need this, since we are collecting job finish time as well
# @luigi.Task.event_handler(luigi.Event.SUCCESS)
# def celebrate_sucess(task):
#     current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%s")
#     print("{task} finished at {current_time}".format(task=task, current_time=current_time))


"""
kafka_test | DummyRunsForever() finished; time took: 1:00:00
kafka_test | Luigi: {task} failed scheduling. Host: {host}Will not run DummyNeverFinish() or any dependencies due to error in deps() method
kafka_test |
kafka_test | Name: DummyNeverFinish
kafka_test |
kafka_test | Parameters:
kafka_test |
kafka_test |
kafka_test | Command line:
kafka_test |   /usr/local/bin/luigi --local-scheduler --module luigi_test DummyNeverFinish
kafka_test |
kafka_test | Traceback (most recent call last):
kafka_test |   File "/usr/local/lib/python2.7/dist-packages/luigi/worker.py", line 185, in run
kafka_test |     raise RuntimeError('Unfulfilled %s at run time: %s' % (deps, ', '.join(missing)))
kafka_test | RuntimeError: Unfulfilled dependency at run time: DummyRunsForever__99914b932b
kafka_test |
kafka_test |
kafka_test | Luigi: {task} failed scheduling. Host: {host}Will not run DummyNeverFinish() or any dependencies due to error in deps() method
kafka_test |
kafka_test | Name: DummyNeverFinish
kafka_test |
kafka_test | Parameters:
kafka_test |
kafka_test |
kafka_test | Command line:
kafka_test |   /usr/local/bin/luigi --local-scheduler --module luigi_test DummyNeverFinish
kafka_test |
kafka_test | Traceback (most recent call last):
kafka_test |   File "/usr/local/lib/python2.7/dist-packages/luigi/worker.py", line 185, in run
kafka_test |     raise RuntimeError('Unfulfilled %s at run time: %s' % (deps, ', '.join(missing)))
kafka_test | RuntimeError: Unfulfilled dependency at run time: DummyRunsForever__99914b932b
"""


# @luigi.Task.event_handler(luigi.Event.DEPENDENCY_MISSING)
# def alert_unfulfilled_dependency(task):
#     # task, formatted_traceback,
#     # subject="Luigi: {task} failed scheduling. Host: {host}",
#     # headline="Will not run {task} or any dependencies due to error in deps() method",
#     # formatted_subject = subject.format(task=task, host=self.host)
#     # formatted_headline = headline.format(task=task, host=self.host)
#     # command = subprocess.list2cmdline(sys.argv)
#     # message = luigi.notifications.format_task_error(formatted_headline, task, command, formatted_traceback)
#
#     missing = [dep.task_id for dep in task.deps() if not dep.complete()]
#     deps = 'dependency' if len(missing) == 1 else 'dependencies'
#
#     host = socket.gethostname()
#     formatted_traceback = ""
#
#     # subject="Luigi: {task} FAILED. Host: {host}",
#     subject=">>>>>>>>>>>Luigi: {task} FAILED. Host: {host}"
#     headline="A task failed when running. Most likely run() raised an exception."
#
#     exception_traceback = None
#     try:
#         err_msg = 'Unfulfilled %s at run time: %s' % (deps, task)
#         raise RuntimeError(err_msg)
#     except Exception as e:
#         typ, val, trc =  sys.exc_info()
#         formatted_traceback = ''.join(traceback.format_exception(type, val, trc))
#
#     msg = format_error(task, subject, headline, formatted_traceback)
#     producer.send(KAFKA_TOPIC, value=msg)


# this doesn't work
# @luigi.Task.event_handler(luigi.Event.PROGRESS)
# def alert_progress(task):
#     # this seems never get called
#     msg = "task running"
#     print(">>>")
#     print(msg)
#     logger.warning(msg)


# never get a time out emails, so put this on hold
# @luigi.Task.event_handler(luigi.Event.TIMEOUT)
# def alert_timeout(task):
#     producer.send(KAFKA_TOPIC, value="timeout " + str(task))


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


class DummyRunsForever(Dummy1):
    def run(self):
        import time
        time.sleep(6)


class DummyNeverFinish(Dummy1):

    def run(self):
        print("running DummyNeverFinish")
        import time
        time.sleep(1)

    def complete(self):
        return False

    def requires(self):
        yield DummyRunsForever()


class Dummy3(Dummy1):
    has_been_run = False

    def requires(self):
        yield Dummy1()
        yield luigi.task.externalize(DummyNeverFinish())

    def run(self):
        print("running Dummp3")
        super(Dummy3, self).run()
        raise Exception('oof')


class DummyFailed(Dummy1):
    has_been_run = False

    def run(self):
        print("running Dummp3")
        super(DummyFailed, self).run()
        raise Exception('oof')


class Dummy4(Dummy1):
    has_been_run = False

    def requires(self):
        return []

    def run(self):
        super(Dummy4, self).run()
        raise Exception('oof')


class DummyProcessFailue(Dummy1):
    def run(self):
        import time
        time.sleep(9999999999999999)
