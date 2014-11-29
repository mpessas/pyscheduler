import sys
import selectors

from .tcpserver import init_socket, read


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    sock = init_socket('127.0.0.1', 8000)
    selector = selectors.DefaultSelector()
    selector.register(sock, selectors.EVENT_READ)

    while True:
        events = selector.select()
        for key, mask in events:
            print(read(key.fileobj))


if __name__ == '__main__':
    sys.exit(main())
