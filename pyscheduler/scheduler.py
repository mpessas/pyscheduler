"""Scheduler object.

Store data based on timestamps.

"""

import heapq
from .log import logger


class Scheduler:

    def __init__(self):
        self.tasks = []

    def push(self, item):
        heapq.heappush(self.tasks, item)

    def pop(self):
        return heapq.heappop(self.tasks)

    def top(self):
        return self.tasks[0] if self else None

    def report(self):
        """Print a report of current status of scheduler."""
        if self.top():
            logger.info('Next timestamp: %s', self.top().timestamp)
        else:
            logger.info('Nothing in the queue.')

    def __len__(self):
        return len(self.tasks)
