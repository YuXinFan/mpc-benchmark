from random import sample
from mpyc.runtime import mpc    # load MPyC
secint = mpc.SecInt()           # 32-bit secure MPyC integers
import traceback                # to show some suppressed error messages

@mpc.coroutine  
async def linear_search(val, arr, size):
    idx = -1
    for i in range(size):
        find = val == arr[i]
        idx = mpc.if_else(find, i, idx)
    return idx 

@mpc.coroutine  
async def linear_search_opt(val, arr, size):
    await mpc.returnType(int)
    idx = -1
    for i in range(size): 
        if await mpc.eq_public(val, arr[i]):
            idx = i 
            break 
    return 

def bench(isopt = False, arraySize=10, searchSize = 1, samples=1):
    import random
    import time
    MIN = 0
    MAX = 2*arraySize

    func = None 
    if isopt :
        func = linear_search_opt 
    else:
        func = linear_search

    mpc.run(mpc.start())            # required only when run with multiple parties

    totalTime = 0
    print("start benchmark binary search %s, %d times repeat:" % ("opt" if isopt else "", samples))
    for kk in range(samples):
        cleartext = random.sample(range(MIN, MAX), arraySize)
        eles = [cleartext[random.randint(0,arraySize-1)] for _ in range(searchSize)]
        x = list(map(secint, cleartext))
        timeSample = 0
        for jj in range(searchSize):
            e = secint(eles[jj])
            # print(x)
            timeS = time.perf_counter()
            oy = mpc.run(mpc.output(func(e, x, arraySize)))
            timeE = time.perf_counter()
            timeDiff = timeE-timeS 
            timeSample += timeDiff
            #print("%.3f, " % timeDiff, end="")
            totalTime += timeDiff
        print("Sample %d cost %.3f" % (kk, timeSample))
    print("Total repeat %d times. Average execution time is %.3fs." % (samples, totalTime/samples))

    mpc.run(mpc.shutdown())
    f = open("Party.csv", "a+")
    f.write("%s, %d, Time/s, %.3f,%d\n" % ("linear_search_opt" if isopt else "linear_search", arraySize,totalTime/samples, samples))
    f.close()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--opt', action='store_true')
    parser.add_argument('-e', type=int)
    parser.add_argument('-s', type=int)
    parser.add_argument('-i', type=int)

    args = parser.parse_args()

    bench(args.opt, args.e, args.s, args.i )
main()
