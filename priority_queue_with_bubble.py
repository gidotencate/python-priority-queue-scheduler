class PriorityQueue:
    def __init__(self) -> None:
        self.pqueue = []
        self.next_id = 0

    def insert(self, priority, item) -> None:
        self.pqueue.append({
            "priority": priority,
            "id": self.next_id,
            "description": item,
        })

        self.next_id += 1
        self._bubble_up(len(self.pqueue) -1)

    def peek(self):
        if not self.pqueue:
            raise IndexError("Queue empty.")
        return self.pqueue[0]
    

    def delete(self):
        if not self.pqueue:
            raise IndexError("Queue empty.")
        top = self.pqueue[0]
        last = self.pqueue.pop()
        if self.pqueue:
            self.pqueue[0] = last
            self._bubble_down(0)
        return top

    def is_empty(self) -> bool:
        return len(self.pqueue) == 0

    def _bubble_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.pqueue[i]["priority"] < self.pqueue[parent]["priority"]:
                self.pqueue[i], self.pqueue[parent] = self.pqueue[parent], self.pqueue[i]
                i = parent
            else:
                break

    def _bubble_down(self, i):
        n = len(self.pqueue)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            smallest = i
            if left < n and self.pqueue[left]["priority"] < self.pqueue[smallest]["priority"]:
                smallest = left
            if right < n and self.pqueue[right]["priority"] < self.pqueue[smallest]["priority"]:
                smallest = right
            if smallest == i:
                break
            self.pqueue[i], self.pqueue[smallest] = self.pqueue[smallest], self.pqueue[i]
            i = smallest