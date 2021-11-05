import logging


def get_logger(filename):
    logger = logging.getLogger(filename)
    logger.basicConfig(format="%(process)d %(levelname)s %(message)s")
    logger.setLevel(logging.INFO)

    return logger
