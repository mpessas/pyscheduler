import logging
import sys
from .log import logger
from .run import run
from .types import Payload


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    logger.setLevel(logging.DEBUG)
    log_handler = logging.StreamHandler()
    logger.addHandler(log_handler)
    try:
        logger.info('Started listening for requests.')
        run('127.0.0.1', 8000, Payload)
    except Exception as e:
        logger.exception("An error occurred: %s", e)
        return -1


sys.exit(main())
