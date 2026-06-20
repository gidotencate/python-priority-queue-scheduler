class PriorityQueue:
    pqueue = list()
    next_id = 0

    def insert(self, priority, item) -> None:
        self.pqueue.append({
            "priority": priority,
            "id": self.next_id,
            "description": item
        })

        self.next_id += 1
        

    def remove(self, item_id):
        for item in self.pqueue:
            if item['id'] == item_id:
                self.pqueue.remove(item)
                return item
        return None

    def remove_all_items(self):
        removed = []
        for item in sorted(self.pqueue, key=lambda item: item['priority']):
            removed.append(self.remove(item['id']))
        return removed

    def get_queue(self):
        return self.pqueue

    def is_empty(self) -> bool:
        if not self.pqueue:
            return True
        return False