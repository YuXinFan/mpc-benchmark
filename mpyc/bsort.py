from random import randrange
from mpyc.runtime import mpc    # load MPyC
secint = mpc.SecInt()           # 32-bit secure MPyC integers
mpc.run(mpc.start())            # required only when run with multiple parties
import traceback                # to show some suppressed error messages

def oddeven_merge(lo, hi, r):
    step = r * 2
    if step < hi - lo:
        yield from oddeven_merge(lo, hi, step)
        yield from oddeven_merge(lo + r, hi, step)
        yield from [(i, i + r) for i in range(lo + r, hi - r, step)]
    else:
        yield (lo, lo + r)

def oddeven_merge_sort_range(lo, hi):
    """ sort the part of x with indices between lo and hi.

    Note: endpoints (lo and hi) are included.
    """
    if (hi - lo) >= 1:
        # if there is more than one element, split the input
        # down the middle and first sort the first and second
        # half, followed by merging them.
        mid = lo + ((hi - lo) // 2)
        yield from oddeven_merge_sort_range(lo, mid)
        yield from oddeven_merge_sort_range(mid + 1, hi)
        yield from oddeven_merge(lo, hi, 1)

def oddeven_merge_sort(length):
    """ "length" is the length of the list to be sorted.
    Returns a list of pairs of indices starting with 0 """
    yield from oddeven_merge_sort_range(0, length - 1)


def compare_and_swap(x, a, b):
    c = x[a] > x[b]                  # secure comparison, secint c represents a secret-shared bit
    d = c * (x[b] - x[a])            # secure subtraction
    x[a], x[b] = x[a] + d, x[b] - d  # secure swap: x[a], x[b] swapped if only if c=1

# @mpc.coroutine
# async def compare_and_swap(x, a, b):
#     ogt = x[a] > x[b]
#     gt = await mpc.eq_public(ogt, 1)
#     if (gt) :
#         x[a], x[b] = x[b], x[a]

def main(samples=1):
    import random
    import time
    MIN = 0
    MAX = 1000000
    n = 65536

    totalTime = 0
    print("start benchmark Batcher Sort, %d times repeat:" % samples)
    for kk in range(samples):
        cleartext = random.sample(range(MIN, MAX), n)
        x = list(map(secint, cleartext))
        # print(x)
        timeS = time.perf_counter()
        for i in oddeven_merge_sort(len(x)): compare_and_swap(x, *i)
        mpc.run(mpc.output(x))
        timeE = time.perf_counter()

        timeDiff = timeE-timeS 
        print("%.3f, " % timeDiff, end="")
        totalTime += timeDiff
    print()
    print("Total repeat %d times. Average execution time is %.3fs." % (samples, totalTime/samples))

if __name__ == '__main__':
    # import timeit
    # iters = 1
    # time = timeit.timeit("main()", setup="from __main__ import main", number = iters) 
    # print("Total repeat %d times. Average execution time is %.3f." % (iters, time/iters))
    main(1)
