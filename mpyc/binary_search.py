from mpyc.runtime import mpc    # load MPyC
from mpyc.seclists import seclist, secindex
secint = mpc.SecInt()           # 32-bit secure MPyC integers
import traceback     
import math  

def oram_read(arr, size, idx):
    ret = secint(-1)
    for i in range(size):
        ret = mpc.if_else(i == idx, arr[i], ret)
    return ret 

@mpc.coroutine
async def obinary_search(haystack, haystack_length, needle):
    upper_bound = int(math.log2(haystack_length)) + 1
    index = secint(-1)
    iimin = secint(0)
    iimax = secint(haystack_length - 1)
    bb = needle
    haystack = seclist(haystack, secint)
    for _ in range(upper_bound):
        ii = iimin + iimax
        cc =  ii % 2
        iimid = mpc.if_else( cc, mpc.div(iimax+iimin-1, 2), mpc.div(iimax+iimin, 2) )
        aa = haystack[iimid] # oram_read(haystack, haystack_length, iimid)
        oeq = aa == bb 
        index = mpc.if_else(oeq, iimid, index)
        olt = aa < bb
        iimin = mpc.if_else(olt, iimid+1, iimin)
        iimax = mpc.if_else(olt, iimax, iimid)
    return index


@mpc.coroutine
async def obinary_search_opt(haystack, haystack_length, needle):
    upper_bound = int(math.log2(haystack_length)) + 1
    index = secint(-1)
    iimin = secint(0)
    iimax = secint(haystack_length - 1)
    bb = needle
    haystack = seclist(haystack, secint)
    for _ in range(upper_bound):
        ii = iimin + iimax
        cc =  ii % 2
        iimid = mpc.if_else( cc, mpc.div(iimax+iimin-1, 2), mpc.div(iimax+iimin, 2) )
        aa = haystack[iimid] # oram_read(haystack, haystack_length, iimid)
        eq = await mpc.eq_public(aa, bb)
        if eq :
            index = iimid
            break
        else:
            olt = aa < bb
            iimin = mpc.if_else(olt, iimid+1, iimin)
            iimax = mpc.if_else(olt, iimax, iimid)
    return index


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
            oy = obinary_search_opt(x, n, e)
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
            oy = obinary_search(x, n, e)
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
