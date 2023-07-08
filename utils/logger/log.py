# Import modules
import logging
import os
import sys


# Create a custom logger
def createLogger(logName, logDir, logFileName):

    # create log dir path if doesn't exist
    try:
        os.makedirs(logDir, exist_ok=True)
    except Exception as e:
        sys.exit(e)

    # create formatter and add it to the handlers
    file_formatter = logging.Formatter('[%(asctime)s] | %(levelname)s | %(message)s | ' +
                                       '(%(filename)s:%(lineno)s)', datefmt='%Y-%m-%d %I:%M:%S %p')

    stream_formatter = logging.Formatter('%(message)s')

    # create file handler which logs even debug messages
    file_handler = logging.FileHandler(
        os.path.join(logDir, logFileName), mode='w+')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    # create console handler with a higher log level
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(stream_formatter)

    # set logger name
    logger = logging.getLogger(logName)
    logger.setLevel(logging.DEBUG)

    # add the handlers to the logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger

# Close the logger and close the file handlers


def closeLogger(logger):
    handlers = logger.handlers[:]
    for handler in handlers:
        logger.removeHandler(handler)
        handler.close()
