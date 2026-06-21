import time
from naive_priority_queue import PriorityQueue as NaivePriorityQueue
from priority_queue_with_bubble import PriorityQueue as BubblePriorityQueue
from priority_queue_heapq import PriorityQueue as HeapqPriorityQueue
from scheduler import Scheduler

IMPLEMENTATIONS = {
    "naive (unsorted list)": NaivePriorityQueue,
    "bubble heap": BubblePriorityQueue,
    "heapq": HeapqPriorityQueue,
}

def time_insert_and_drain(pq_class, n):
    pq = pq_class()

    start = time.perf_counter()
    for i in range(n):
        pq.insert(priority= i, item=f"task-{i}")
    insert_time = time.perf_counter() - start

    start = time.perf_counter()
    if hasattr(pq, "delete"):
        while not pq.is_empty():
            pq.delete()
    else:
        pq.remove_all_items()
    drain_time = time.perf_counter() - start

    return insert_time, drain_time


COMPLEXITY = {
    "naive (unsorted list)": "O(n^2) drain (sort + linear-scan remove per item)",
    "bubble heap": "O(n log n) drain, pure-Python sift",
    "heapq": "O(n log n) drain, C-optimized sift",
}


def benchmark_queues():
    print("=== Priority Queue Benchmark (insert N items, then drain all) ===")
    for name, complexity in COMPLEXITY.items():
        print(f"  {name}: {complexity}")
    print()
    print(f"{'Implementation':<25}{'N':>10}{'Insert (ms)':>15}{'Drain (ms)':>15}{'vs fastest':>14}")
    print("-" * 79)

    for n in (100, 200, 500, 1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 70_000, 100_000):
        results = {name: time_insert_and_drain(pq_class, n) for name, pq_class in IMPLEMENTATIONS.items()}
        fastest_drain = min(drain_time for _, drain_time in results.values())
        for name, (insert_time, drain_time) in results.items():
            marker = " *" if drain_time == fastest_drain else ""
            ratio = f"{drain_time / fastest_drain:.2f}x"
            print(f"{name:<25}{n:>10}{insert_time * 1000:>15.3f}{drain_time * 1000:>15.3f}{ratio:>12}{marker}")
        print()
    print("* fastest drain time for that N")


def benchmark_scheduler():
    print("=== Scheduler Demo (same Scheduler, different injected queue) ===")
    now = time.time()
    for name, pq_class in (("bubble heap", BubblePriorityQueue), ("heapq", HeapqPriorityQueue)):
        sched = Scheduler(pq=pq_class())
        sched.schedule(priority=5, run_at=now, task_name="Powerpoint")
        sched.schedule(priority=9, run_at=now + 7, task_name="Excel")
        sched.schedule(priority=3, run_at=now - 2, task_name="Word")
        print(f"\n--- {name} ---")
        sched.run_pending()


if __name__ == "__main__":
    benchmark_queues()
    benchmark_scheduler()