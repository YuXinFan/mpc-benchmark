from mpyc.runtime import mpc    # load MPyC
secint = mpc.SecInt()           # 32-bit secure MPyC integers
mpc.run(mpc.start())            # required only when run with multiple parties
import traceback     
import math  

@mpc.coroutine
async def binary_almost_search_opt_main(needle, arr, l, r):
    if (r >= l):
        mid = l + int((r-l)/2)
        left = mid > l
        if left :
            left = arr[mid-1] == needle
        right = mid < r 
        if right:
            right = arr[mid+1] == needle 
        eq = mpc.eq_public(arr[mid], needle)

        if await (eq):
            return mid 
        else:
            idx = mpc.if_else(left, (mid-1), mpc.if_else(right, mid+1, -1))
            
            gt = arr[mid] > needle 
            lt = arr[mid] < needle 
            if mid-2 >= l :
                ll = binary_almost_search_opt_main(needle, arr, l, mid - 2)
                idx = mpc.if_else(idx == -1, ll, idx)
            if r >= mid+2:
                rr = binary_almost_search_opt_main(needle, arr, mid + 2, r)
                idx = mpc.if_else(idx == -1, rr, idx)
            return idx 

def binary_almost_search_opt(needle, arr, n):
    return binary_almost_search_opt_main(needle, arr, 0, n-1)


def main(samples=1):
    import random
    import time
    MIN = 0
    MAX = 1000
    n = 100

    totalTime = 0
    print("start benchmark Batcher Sort, %d times repeat:" % samples)
    for kk in range(samples):
        cleartext = random.sample(range(MIN, MAX), n)
        cleartext = sorted(cleartext)
        ele = random.randrange(MIN,MAX)

        # print(cleartext)
        # print(ele)

        x = list(map(secint, cleartext))
        ele = secint(ele)

        timeS = time.perf_counter()
        idx = binary_almost_search_opt(ele,x,n)
        mpc.run(mpc.output(idx))
        timeE = time.perf_counter()

        # print("idx:",mpc.output(idx))
        timeDiff = timeE-timeS 
        print("%.3f, " % timeDiff, end="\n")
        totalTime += timeDiff
    print()
    print("Total repeat %d times. Average execution time is %.3fs." % (samples, totalTime/samples))

if __name__ == '__main__':
    # import timeit
    # iters = 1
    # time = timeit.timeit("main()", setup="from __main__ import main", number = iters) 
    # print("Total repeat %d times. Average execution time is %.3f." % (iters, time/iters))
    main(10)

        
