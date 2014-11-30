"""Main functions of library.

"""

from functools import partial
import selectors
import signal
import time

import linuxfd

from .log import logger
from .scheduler import Scheduler
from .tcpserver import init_socket, handle_request, close_socket


def run(host, port, Payload):
    """Select loop of scheduler.

    :param host: A string with the host to bind to.
    :param port: An integer with the port to bind to.
    :param Payload: A class that follows the interface of ``types.Payload``.

    """
    scheduler = Scheduler()

    sock = init_socket('127.0.0.1', 8000)
    selector = selectors.DefaultSelector()
    callback = partial(handle_request, klass=Payload)
    selector.register(sock, selectors.EVENT_READ, callback)

    sigint_fd = linuxfd.signalfd(
        signalset={signal.SIGINT, signal.SIGTERM}, nonBlocking=True
    )
    selector.register(sigint_fd, selectors.EVENT_READ, True)
    sighup_fd = linuxfd.signalfd(signalset={signal.SIGHUP}, nonBlocking=True)
    selector.register(sighup_fd, selectors.EVENT_READ, scheduler.report)
    signal.pthread_sigmask(
        signal.SIG_BLOCK, {signal.SIGINT, signal.SIGHUP, signal.SIGTERM}
    )

    timestamp = None
    should_exit = False
    while True:
        if should_exit:
            break
        if timestamp is None:
            timeout = timestamp
        else:
            timeout = timestamp - time.time()
            assert timeout >= 0
        logger.debug('Selecting on timeout {0}'.format(timeout))
        events = selector.select(timeout)
        if not events:
            item = scheduler.pop()
            item.execute()
            timestamp = getattr(scheduler.top(), 'timestamp', None)
        for key, mask in events:
            callback = key.data
            if not callable(callback):
                should_exit = True
            elif key.fileobj == sock:
                item = callback(key.fileobj)
                scheduler.push(item)
                timestamp = scheduler.top().timestamp
            else:
                key.fileobj.read()
                callback()
    close_socket(sock)
