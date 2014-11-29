"""Scheduler object.

Store data based on timestamps.

"""

import heapq


class Scheduler:

    def __init__(self):
        self.tasks = []

    def push(self, item):
        heapq.heappush(self.tasks, item)

    def pop(self):
        return heapq.heappop(self.tasks)

    def top(self):
        return self.tasks[0] if self else None

    def __len__(self):
        return len(self.tasks)
