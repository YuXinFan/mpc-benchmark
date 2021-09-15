from mpyc.runtime import mpc    # load MPyC
secint = mpc.SecInt()           # 32-bit secure MPyC integers
mpc.run(mpc.start())            # required only when run with multiple parties
import traceback                # to show some suppressed error messages


@mpc.coroutine  
async def partition(arr, low, high):
    i = (low-1)         # index of smaller element
    pivot = arr[high]     # pivot
  
    for j in range(low, high):
  
        # If current element is smaller than or
        # equal to pivot
        oleq = arr[j] <= pivot
        if await mpc.eq_public(oleq, 1):
  
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
  
@mpc.coroutine  
async def quickSort(arr, low, high):
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

def quickSortMain(arr, low, high):
    quickSort(arr, low, high)

def main(samples=1):
    import random
    import time
    MIN = 0
    MAX = 1000000
    n = 1000
    totalTime = 0
    print("start benchmark Batcher Sort, %d times repeat:" % samples)
    for kk in range(samples):
        cleartext = random.sample(range(MIN, MAX), n)
        x = list(map(secint, cleartext))
        # print(x)
        timeS = time.perf_counter()
        quickSortMain(x, 0, len(x)-1)
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