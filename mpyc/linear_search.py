from mpyc.runtime import mpc    # load MPyC
secint = mpc.SecInt()           # 32-bit secure MPyC integers
mpc.run(mpc.start())            # required only when run with multiple parties
import traceback                # to show some suppressed error messages


@mpc.coroutine  
async def linear_search_opt(val, arr, size):
    idx = -1
    for i in range(size): 
        find = mpc.eq_public(val, arr[i])
        if await(find):
            idx = i 
            break 
    return idx 



def main(samples=1):
    import random
    import time
    MIN = 0
    MAX = 1000
    n = 1000

    totalTime = 0
    print("start benchmark Batcher Sort, %d times repeat:" % samples)
    for kk in range(samples):
        cleartext = random.sample(range(MIN, MAX), n)
        ele = random.randrange(MIN,MAX)

        # print(cleartext)
        # print(ele)

        x = list(map(secint, cleartext))
        e = secint(ele)

        timeS = time.perf_counter()
        idx = linear_search_opt(e,x,n)
        #mpc.run(mpc.output(idx))
        timeE = time.perf_counter()

        if (idx != -1):
            print(cleartext[idx] == ele)
        print("idx:",idx)
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