import heapq
import itertools


class PriorityQueue:
    def __init__(self) -> None:
        self.heap = []
        self.next_id = 0
        self._counter = itertools.count()

    def insert(self, priority, item) -> None:
        entry = (priority, next(self._counter), {
            "priority": priority,
            "id": self.next_id,
            "description": item,
        })
        heapq.heappush(self.heap, entry)
        self.next_id += 1

    def peek(self):
        if not self.heap:
            raise IndexError("Queue empty.")
        return self.heap[0][2]

    def delete(self):
        if not self.heap:
            raise IndexError("Queue empty.")
        return heapq.heappop(self.heap)[2]

    def is_empty(self) -> bool:
        return len(self.heap) == 0
