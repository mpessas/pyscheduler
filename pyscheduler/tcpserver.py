"""TCP server.

Listen on TCP socket and act on messages.

"""

import socket
from .types import Payload
from .log import logger


def init_socket(host, port):
    """Initialize the socket."""
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(10)
    sock.setblocking(False)
    logger.debug('Socket initialized')
    return sock


def read(sock):
    """Read from the specified socket."""
    conn, addr = sock.accept()
    msg = b''
    while True:
        data = conn.recv(1024)
        if not data:
            break
        msg += data
    return msg


def close_socket(sock):
    sock.close()
    logger.debug('Socket closed')


def handle_request(fd, klass=Payload):
    return klass.from_payload(read(fd))
