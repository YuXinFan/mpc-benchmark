from mpyc.runtime import mpc    # load MPyC
secint = mpc.SecInt()           # 32-bit secure MPyC integers
mpc.run(mpc.start())            # required only when run with multiple parties
import traceback     
import math  

@mpc.coroutine
async def binary_almost_search_main(needle, arr, l, r):
    if (r >= l):
        mid = l + int((r-l)/2)
        left = mid > l
        if left :
            left = arr[mid-1] == needle
        right = mid < r 
        if right:
            right = arr[mid+1] == needle 

        oeq = arr[mid] == needle 

        idx = mpc.if_else(oeq, mid, -1)
        idx = mpc.if_else(left, (mid-1), mpc.if_else(right, mid+1, idx))
        
        gt = arr[mid] > needle 
        lt = arr[mid] < needle 
        if mid-2 >= l :
            ll = binary_almost_search_opt_main(needle, arr, l, mid - 2)
            idx = mpc.if_else(gt, ll, idx)
        if r >= mid+2:
            rr = binary_almost_search_opt_main(needle, arr, mid + 2, r)
            idx = mpc.if_else(lt, rr, idx)
        return idx 

def binary_almost_search(needle, arr, n):
    return binary_almost_search_opt_main(needle, arr, 0, n-1)

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
                idx = mpc.if_else(gt, ll, idx)
            if r >= mid+2:
                rr = binary_almost_search_opt_main(needle, arr, mid + 2, r)
                idx = mpc.if_else(lt, rr, idx)
            return idx 

def binary_almost_search_opt(needle, arr, n):
    return binary_almost_search_opt_main(needle, arr, 0, n-1)



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
        cleartext = sorted(cleartext)
        x = list(map(secint, cleartext))
        for jj in range(repeat):
            ele = random.randrange(MIN,MAX)
            e = secint(ele)
            # print(x)
            timeS = time.perf_counter()
            oy = binary_almost_search_opt(e, x, n)
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
        cleartext = sorted(cleartext)
        x = list(map(secint, cleartext))
        for jj in range(repeat):
            ele = random.randrange(MIN,MAX)
            e = secint(ele)
            # print(x)
            timeS = time.perf_counter()
            oy = binary_almost_search(e, x, n)
            #y=mpc.run(mpc.output(oy))
            timeE = time.perf_counter()

            # if (y != -1):
            #     print("In:",cleartext[y]==ele)
            # else:
            #     print("Not-in:", cleartext.count(ele)==0)

            timeDiff = timeE-timeS 
            #print("%.3f, " % timeDiff, end="")
            totalTime += timeDiff
    print()
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


        
