# python-priority-queue-scheduler

Three priority queue implementations — naive list, hand-rolled binary heap, and `heapq` — powering the same task scheduler via dependency injection, benchmarked head-to-head.

## Why this exists

A scheduler is a priority queue: every "what runs next" decision is just "pop the highest-priority item." This repo rebuilds that idea from scratch in three layers of increasing sophistication, wires all three into the same `Scheduler`, and benchmarks them to see how Big-O theory holds up against real wall-clock performance.

## What's in here

| File | What it is |
|---|---|
| [`naive_priority_queue.py`](naive_priority_queue.py) | An unsorted list. `insert` is O(1); removing the highest-priority item means sorting the whole list, O(n log n) per call. |
| [`priority_queue_with_bubble.py`](priority_queue_with_bubble.py) | A hand-rolled binary min-heap, with `_bubble_up`/`_bubble_down` written from scratch. O(log n) insert/delete. |
| [`priority_queue_heapq.py`](priority_queue_heapq.py) | The same min-heap algorithm, backed by Python's built-in [`heapq`](https://docs.python.org/3/library/heapq.html) (C-implemented). |
| [`scheduler.py`](scheduler.py) | A `Scheduler` that runs tasks at their scheduled time, ordered by priority among tasks that are due. Takes any of the above queues via constructor injection. |
| [`benchmark.py`](benchmark.py) | Times insert/drain across all three queue implementations at increasing N, and runs the same `Scheduler` against each. |

## Usage

```bash
# Run the scheduler demo (polls every second until all tasks have executed)
python3 scheduler.py

# Run the benchmark across all three implementations
python3 benchmark.py
```

Swap the queue backend by injecting a different instance:

```python
from scheduler import Scheduler
from priority_queue_heapq import PriorityQueue as HeapqPriorityQueue

sched = Scheduler(pq=HeapqPriorityQueue())
```

## Interface

`naive_priority_queue.py` predates the other two and has a different shape — it isn't a drop-in replacement for `Scheduler`. The two heap-based implementations share an identical interface, which is what makes the dependency injection above possible:

| Method | naive | bubble heap | heapq |
|---|---|---|---|
| `insert(priority, item)` | ✓ | ✓ | ✓ |
| `peek()` | — | ✓ | ✓ |
| `delete()` | — | ✓ | ✓ |
| `remove(item_id)` | ✓ | — | — |
| `remove_all_items()` | ✓ | — | — |
| `get_queue()` | ✓ | — | — |
| `is_empty()` | ✓ | ✓ | ✓ |

## Benchmark results

Insert N items, then drain the queue, timed with `time.perf_counter()`:

```
Implementation                    N    Insert (ms)     Drain (ms)    vs fastest
-------------------------------------------------------------------------------
naive (unsorted list)           100          0.042          0.022       1.00x *
bubble heap                     100          0.028          0.081       3.73x
heapq                           100          0.089          0.022       1.00x

naive (unsorted list)          1000          0.374          0.201       1.00x *
bubble heap                    1000          0.274          1.306       6.48x
heapq                          1000          0.593          0.241       1.20x

naive (unsorted list)         10000          4.217          7.634       2.30x
bubble heap                   10000          2.800         19.540       5.90x
heapq                         10000          2.978          3.314       1.00x *

naive (unsorted list)         50000         22.630        111.740       5.24x
bubble heap                   50000         21.521        120.494       5.65x
heapq                         50000         25.696         21.315       1.00x *

naive (unsorted list)        100000         41.053        419.931       9.30x
bubble heap                  100000         40.575        271.068       6.00x
heapq                        100000         55.822         45.173       1.00x *
```

**The naive O(n²) list is actually faster than the hand-rolled heap until somewhere around N=50,000.** Big-O describes what happens as N approaches infinity — it says nothing about the constant factor. The hand-rolled heap does its comparisons in pure Python; the naive version leans on `sorted()` and `list.remove()`, which run in C. The "worse" algorithm wins on wall-clock time until the input is large enough for the asymptotics to actually dominate. `heapq` wins at every scale tested, for the same reason in reverse — it's the same algorithm as the hand-rolled heap, just implemented in C.

## Design notes

- **Scheduling order**: `Scheduler.schedule()` inserts with a composite key `(run_at, priority)` rather than just `priority`. Since Python tuples compare lexicographically, the heap naturally orders by due time first and falls back to priority only when two tasks are due at the exact same time.
- **Why `run_pending()`'s early exit is safe**: it peeks the root and stops the moment it isn't due yet. That's only correct because the root is the *global* minimum `(run_at, priority)` tuple in the heap — if it isn't due, nothing else in the queue can be due either.
- **Dependency injection**: `Scheduler(pq=...)` takes any object implementing `insert`/`peek`/`delete`/`is_empty`, so the scheduling logic never needs to know which queue implementation it's running on.

## License

MIT, see [LICENSE](LICENSE).
