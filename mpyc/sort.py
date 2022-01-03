from random import randrange
from mpyc.runtime import mpc    # load MPyC
secint = mpc.SecInt()           # 32-bit secure MPyC integers
import traceback                # to show some suppressed error messages
import math 

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

def batcher_sort(arr1, arr2):
    mpc.run(mpc.start())
    shared_arr1 = mpc.input(arr1, senders=[0])[0]
    shared_arr2 = mpc.input(arr2, senders=[1])[0]
    shared_arr = shared_arr1 + shared_arr2
    n = len(shared_arr)
    extend = 2 ** math.ceil(math.log2(n))
    extend = extend - n 
    for i in range(extend):
        shared_arr.append(secint(0))
    for i in oddeven_merge_sort(len(shared_arr)):
        compare_and_swap(shared_arr, *i)
    x = shared_arr[extend:]
    mpc.run(mpc.shutdown())
# @mpc.coroutine
# async def compare_and_swap(x, a, b):
#     ogt = x[a] > x[b]
#     gt = await mpc.eq_public(ogt, 1)
#     if (gt) :
#         x[a], x[b] = x[b], x[a]
def partition(arr, low, high):
    i = (low-1)         # index of smaller element
    pivot = arr[high]     # pivot
  
    for j in range(low, high):
  
        # If current element is smaller than or
        # equal to pivot
        oleq = arr[j] <= pivot
        leq = mpc.run(mpc.eq_public(oleq, 1))
        if leq:
  
            # increment index of smaller element
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]
  
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)
  
# The main function that implements QuickSort
# arr[] --> Array to be sorted,
# low  --> Starting index,
# high  --> Ending index
  
# Function to do Quick sort
def quickSort(arr, low, high):
    if len(arr) == 1:
        return arr
    if low < high:
  
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, low, high)
        # print(pi)
  
        # Separately sort elements before
        # partition and after partition
        quickSort(arr, low, pi-1)
        quickSort(arr, pi+1, high)

def quick_sort(arr1, arr2):
    mpc.run(mpc.start())
    shared_arr1 = mpc.input(arr1, senders=[0])[0]
    shared_arr2 = mpc.input(arr2, senders=[1])[0]
    shared_arr = shared_arr1 + shared_arr2
    quickSort(shared_arr, 0, len(shared_arr)-1)
    mpc.run(mpc.shutdown())


def bench(isopt = False, arraySize=10,  samples=1):
    import random
    import time
    MIN = 0
    MAX = 2*arraySize

    totalTime = 0
    print("start benchmark %s, %d times repeat:" % ("quick_sort" if isopt else "batcher_sort", samples))
    for kk in range(samples):
        cleartext1 = random.sample(range(MIN, MAX), int(arraySize/2))
        cleartext2 = random.sample(range(MIN, MAX), arraySize - int(arraySize/2))
        x1 = list(map(secint, cleartext1))
        x2 = list(map(secint, cleartext2))

        # print(x)
        if isopt:
            timeS = time.perf_counter()
            quick_sort(x1, x2)
            timeE = time.perf_counter()
        else:
            timeS = time.perf_counter()
            batcher_sort(x1, x2)
            timeE = time.perf_counter()
        timeDiff = timeE-timeS 
            #print("%.3f, " % timeDiff, end="")
        totalTime += timeDiff
        print("Sample %d cost %.3f" % (kk, timeDiff))
    print("Total repeat %d times. Average execution time is %.3fs." % (samples, totalTime/samples))

    f = open("Party.csv", "a+")
    f.write("%s, %d, Time/s, %.3f,%d\n" 
    % ("quick_sort" if isopt else "batcher_sort", arraySize, totalTime/samples, samples))
    f.close()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--opt', action='store_true')
    parser.add_argument('-n', type=int)
    parser.add_argument('-i', type=int)


    args = parser.parse_args()

    bench(args.opt, args.n, args.i)
main()
