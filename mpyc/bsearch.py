from mpyc.runtime import mpc    # load MPyC
secint = mpc.SecInt()           # 32-bit secure MPyC integers
mpc.run(mpc.start())            # required only when run with multiple parties
import traceback     
import math  

@mpc.coroutine
async def obinary_search_revealed(result, haystack, haystack_length, needle):
    upper_bound = int(math.log2(haystack_length)) + 1
    index = secint(-1)
    iimin = secint(0)
    iimax = secint(haystack_length - 1)
    bb = needle
    for ii in range(upper_bound):
        iimid = (iimin + iimax) / 2
        temp_element = haystack[iimid]
        oeq = temp_element == bb
        eq = mpc.eq_public(oeq, 1)
        if await (eq) :
            result = temp_element
            index = iimid
            break
        else:
            olt = temp_element < bb
            iimin = iimin*(1-olt) + (iimid+1)*olt 
            iimax = iimax*(olt) + iimid*(1-olt)
    return index
	
def main(samples=1):
    import random
    import time
    MIN = 0
    MAX = 10000
    n = 512

    totalTime = 0
    print("start benchmark Batcher Sort, %d times repeat:" % samples)
    for kk in range(samples):
        cleartext = random.sample(range(MIN, MAX), n)
        x = list(map(secint, cleartext))
        ele = random.randrange(MIN,MAX)
        ele = secint(ele)
        # print(x)
        y = secint()
        timeS = time.perf_counter()
        obinary_search_revealed(y,x,n,ele)
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
    main(2)
