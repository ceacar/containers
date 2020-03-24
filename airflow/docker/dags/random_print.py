import datetime
import logging
import excalibur




def print_time():
    logging.info('\n>>>'+str(datetime.datetime.now()))

@excalibur.debug
def task1():
    logging.info("||||||||||||||||task1|||||||||||||||")

def task0():
    logging.info("||||||||||||||||task0|||||||||||||||")

def taska():
    logging.info("||||||||||||||||taska|||||||||||||||")
def taskb():
    logging.info("||||||||||||||||taskb|||||||||||||||")
def taskc():
    logging.info("||||||||||||||||taskc|||||||||||||||")
def taskd():
    logging.info("||||||||||||||||taskd|||||||||||||||")
def taske():
    logging.info("||||||||||||||||taske|||||||||||||||")
