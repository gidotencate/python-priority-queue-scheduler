import time
import sys
from priority_queue_with_bubble import PriorityQueue as DefaultPriorityQueue

class Scheduler:
    def __init__(self, pq= None) -> None:
        self.pq = pq if pq is not None else DefaultPriorityQueue()

    def schedule(self, priority, run_at, task_name):
        self.pq.insert((run_at, priority), {"run_at": run_at, "task": task_name})

    def run_pending(self):
        now = time.time()
        while not self.pq.is_empty():
            top = self.pq.peek()
            if top["description"]["run_at"] > now:
                break
            due_task = self.pq.delete()
            print(f"Running: {due_task["description"]["task"]}")

def main():
    sched = Scheduler()
    now = time.time()

    sched.schedule(priority=5, run_at=now, task_name="Powerpoint")
    sched.schedule(priority=9, run_at=now + 7, task_name="Excel")
    sched.schedule(priority=3, run_at=now -2, task_name="Word")
    sched.schedule(priority=40, run_at=now + 10, task_name="Powershell")
    sched.schedule(priority=1, run_at=now - 5, task_name="Windows Store")
    sched.schedule(priority=12, run_at=now, task_name="Outlook")

    while True:
        if not sched.pq.is_empty():
            sched.run_pending()
            time.sleep(1)
        else:
            break

    print("Finished all tasks!")
    return 0


if __name__ == "__main__":
    sys.exit(main())