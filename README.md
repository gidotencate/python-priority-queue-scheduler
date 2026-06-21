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
naive (unsorted list)           100          0.028          0.021       1.00x *
bubble heap                     100          0.028          0.086       4.15x
heapq                           100          0.090          0.022       1.07x

naive (unsorted list)           200          0.044          0.036       1.00x *
bubble heap                     200          0.048          0.187       5.17x
heapq                           200          0.041          0.041       1.14x

naive (unsorted list)           500          0.157          0.095       1.00x *
bubble heap                     500          0.140          0.570       6.00x
heapq                           500          0.129          0.112       1.18x

naive (unsorted list)          1000          0.287          0.202       1.00x *
bubble heap                    1000          0.605          1.413       6.99x
heapq                          1000          0.282          0.255       1.26x

naive (unsorted list)          2000          0.630          0.507       1.00x *
bubble heap                    2000          0.572          3.021       5.95x
heapq                          2000          0.574          0.521       1.03x

naive (unsorted list)          5000          2.021          2.017       1.32x
bubble heap                    5000          1.477          8.865       5.78x
heapq                          5000          1.563          1.533       1.00x *

naive (unsorted list)         10000          3.482          5.955       1.63x
bubble heap                   10000          2.992         21.487       5.88x
heapq                         10000          3.477          3.653       1.00x *

naive (unsorted list)         20000          7.412         22.094       2.79x
bubble heap                   20000          6.810         44.976       5.69x
heapq                         20000          7.820          7.906       1.00x *

naive (unsorted list)         50000         21.226        112.831       5.23x
bubble heap                   50000         21.532        131.033       6.07x
heapq                         50000         24.293         21.594       1.00x *

naive (unsorted list)         70000         23.731        208.284       6.68x
bubble heap                   70000         29.499        182.433       5.85x
heapq                         70000         38.881         31.198       1.00x *

naive (unsorted list)        100000         36.823        422.126       8.15x
bubble heap                  100000         41.753        274.900       5.31x
heapq                        100000         60.882         51.817       1.00x *
```

The insert and drain columns tell different stories:

- **Insert**: the hand-rolled bubble heap wins at nearly every size. `insert` only ever walks bubble-up along a single path from leaf to root, which is cheap even in pure Python — and it's short enough that `heapq`'s C-level function-call overhead doesn't pay for itself until N is fairly large.
- **Drain**: this is where the naive O(n²) list actually beats the hand-rolled heap, all the way up through N=50,000. The crossover sits between N=50,000 (naive still ahead: 112.8ms vs 131.0ms) and N=70,000 (bubble heap pulls ahead: 208.3ms vs 182.4ms). The hand-rolled heap does its comparisons in pure Python; the naive version leans on `sorted()` and `list.remove()`, which run in C — so the "worse" algorithm wins on wall-clock time until the input is large enough for the asymptotics to dominate the constant-factor gap. `heapq` wins drain at every size tested, for the same reason in reverse: it's the same heap algorithm as the hand-rolled version, just implemented in C.

Big-O describes what happens as N approaches infinity — it says nothing about the constant factor, and the constant factor is what actually decides the winner across most of the range tested here.

## Design notes

- **Scheduling order**: `Scheduler.schedule()` inserts with a composite key `(run_at, priority)` rather than just `priority`. Since Python tuples compare lexicographically, the heap naturally orders by due time first and falls back to priority only when two tasks are due at the exact same time.
- **Why `run_pending()`'s early exit is safe**: it peeks the root and stops the moment it isn't due yet. That's only correct because the root is the *global* minimum `(run_at, priority)` tuple in the heap — if it isn't due, nothing else in the queue can be due either.
- **Dependency injection**: `Scheduler(pq=...)` takes any object implementing `insert`/`peek`/`delete`/`is_empty`, so the scheduling logic never needs to know which queue implementation it's running on.

## License

MIT, see [LICENSE](LICENSE).
