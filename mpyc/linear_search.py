from mpyc.runtime import mpc    # load MPyC
secint = mpc.SecInt()           # 32-bit secure MPyC integers
mpc.run(mpc.start())            # required only when run with multiple parties
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
    idx = -1
    for i in range(size): 
        find = mpc.eq_public(val, arr[i])
        if await(find):
            idx = i 
            break 
    return idx 


def testOpt(samples=1, n=10):
    import random
    import time
    MIN = 0
    repeat = n
    MAX = 2*n 

    mpc.run(mpc.start())            # required only when run with multiple parties

    totalTime = 0
    print("start benchmark binary search opt, %d times repeat:" % samples)
    for kk in range(samples):
        cleartext = random.sample(range(MIN, MAX), n)
        x = list(map(secint, cleartext))
        for jj in range(repeat):
            ele = random.randrange(MIN,MAX)
            e = secint(ele)
            # print(x)
            timeS = time.perf_counter()
            oy = linear_search_opt(e, x, n)
            #y=mpc.run(mpc.output(oy))
            timeE = time.perf_counter()

            # if (y != -1):
            #     print("In:",cleartext[y]==ele)
            # else:
            #     print("Not-in:", cleartext.count(ele)==0)

            timeDiff = timeE-timeS 
            #print("%.3f, " % timeDiff, end="")
            totalTime += timeDiff
    print("Total repeat %d times. Average execution time is %.3fs." % (samples, totalTime/samples/repeat))

    mpc.run(mpc.shutdown())

def testRaw(samples=1, n=10):
    import random
    import time
    
    MIN = 0
    repeat = n
    MAX = 2*n 

    mpc.run(mpc.start())            # required only when run with multiple parties

    totalTime = 0
    print("start benchmark binary search raw, %d times repeat:" % samples)
    for kk in range(samples):
        cleartext = random.sample(range(MIN, MAX), n)
        x = list(map(secint, cleartext))
        for jj in range(repeat):
            ele = random.randrange(MIN,MAX)
            e = secint(ele)
            # print(x)
            timeS = time.perf_counter()
            oy = linear_search(e, x, n)
            #y=mpc.run(mpc.output(oy))
            timeE = time.perf_counter()

            # if (y != -1):
            #     print("In:",cleartext[y]==ele)
            # else:
            #     print("Not-in:", cleartext.count(ele)==0)

            timeDiff = timeE-timeS 
            #print("%.3f, " % timeDiff, end="")
            totalTime += timeDiff
    print("Total repeat %d times. Average execution time is %.3fs." % (samples, totalTime/samples/repeat))
    mpc.run(mpc.shutdown())

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--opt', action='store_true')
    parser.add_argument('-n', type=int)
    parser.add_argument('-r', type=int)

    args = parser.parse_args()

    if args.opt == True:
        testOpt(args.r, args.n)
    else:
        testRaw(args.r, args.n)
main()
