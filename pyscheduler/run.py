"""Main functions of library.

"""

from functools import partial
import selectors
from .log import logger
from .scheduler import Scheduler
from .tcpserver import init_socket, handle_request


def run(host, port, Payload):
    """Select loop of scheduler.

    :param host: A string with the host to bind to.
    :param port: An integer with the port to bind to.
    :param Payload: A class that follows the interface of ``types.Payload``.

    """

    sock = init_socket('127.0.0.1', 8000)
    selector = selectors.DefaultSelector()
    callback = partial(handle_request, klass=Payload)
    selector.register(sock, selectors.EVENT_READ, callback)

    scheduler = Scheduler()
    timeout = None
    while True:
        logger.debug('Selecting on timeout {0}'.format(timeout))
        events = selector.select(timeout)
        if not events:
            item = scheduler.pop()
            item.execute()
            timeout = getattr(scheduler.top(), 'timestamp', None)
        for key, mask in events:
            callback = key.data
            item = callback(key.fileobj)
            scheduler.push(item)
            timeout = scheduler.top().timestamp
