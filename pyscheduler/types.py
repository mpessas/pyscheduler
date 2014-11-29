"""Various types used in the library.

"""

import functools


@functools.total_ordering
class Payload:
    """Sample class for a Payload for the scheduler.

    Any subclass needs to implement the ``from_payload`` method as
    constructor, ``_timestamp`` and ``execute``.

    """

    @classmethod
    def from_payload(cls, payload):
        """Payload is the raw bytes message read from the socket."""
        return cls(float(payload))

    def __init__(self, data):
        self.data = data

    def __lt__(self, other):
        return self._timestamp() < other._timestamp()

    def __eq__(self, other):
        return self._timestamp() == other._timestamp()

    def __str__(self):
        return str(self.data)

    def _timestamp(self):
        return float(self.data)

    @property
    def timestamp(self):
        return self._timestamp()

    def execute(self):
        print("Hi from {0}".format(self))
