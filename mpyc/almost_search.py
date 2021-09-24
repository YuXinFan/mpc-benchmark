from mpyc.runtime import mpc    # load MPyC
from mpyc.seclists import seclist, secindex
secint = mpc.SecInt()           # 32-bit secure MPyC integers
mpc.run(mpc.start())            # required only when run with multiple parties
import traceback     
import math  

def gen_sorted_array(n):
    import random 
    l = []
    v = 0
    for i in range(n):
        v = v + random.randrange(0,8)
        l.append(v)

    return l 

@mpc.coroutine
async def binary_almost_search_main(haystack, haystack_length, needle):
    upper_bound = int(math.log2(haystack_length)) + 1
    index = secint(-1)
    iimin = secint(0)
    iimax = secint(haystack_length - 1)
    bb = needle
    for _ in range(upper_bound):
        ii = iimin + iimax
        cc =  ii % 2
        iimid = mpc.if_else( cc, mpc.div(iimax+iimin-1, 2), mpc.div(iimax+iimin, 2) )
        aa = haystack[iimid] # oram_read(haystack, haystack_length, iimid)
        oeq = aa == bb 
        index = mpc.if_else(oeq, iimid, index)
        left = haystack[iimid-1]
        index = mpc.if_else(aa==left, iimid-1, index)

        right = haystack[iimid+1]
        index = mpc.if_else(aa==right, iimid+1, index)

        ogt = aa > bb
        iimin = mpc.if_else(ogt, iimin, iimid+2)
        iimax = mpc.if_else(ogt, iimid-2, iimax)
    return index


def binary_almost_search(arr, n, needle):
    return binary_almost_search_main(arr, n, needle)

@mpc.coroutine
async def binary_almost_search_opt_main(haystack, haystack_length, needle):
    upper_bound = int(math.log2(haystack_length)) + 1
    index = secint(-1)
    iimin = secint(0)
    iimax = secint(haystack_length - 1)
    bb = needle
    for _ in range(upper_bound):
        ii = iimin + iimax
        cc =  ii % 2
        iimid = mpc.if_else( cc, mpc.div(iimax+iimin-1, 2), mpc.div(iimax+iimin, 2) )
        aa = haystack[iimid] # oram_read(haystack, haystack_length, iimid)
        eq = await mpc.eq_public(aa, bb)
        if eq:
            index = iimid 
            break  
        left = haystack[iimid-1]
        index = mpc.if_else(aa==left, iimid-1, index)

        right = haystack[iimid+1]
        index = mpc.if_else(aa==right, iimid+1, index)

        ogt = aa > bb
        iimin = mpc.if_else(ogt, iimin, iimid+2)
        iimax = mpc.if_else(ogt, iimid-2, iimax)
    return index

def binary_almost_search_opt(arr, n, needle):
    return binary_almost_search_opt_main(arr, n, needle)



def testOpt(arraySize=10, searchSize = 1, samples=1):
    import random
    import time

    mpc.run(mpc.start())            # required only when run with multiple parties

    totalTime = 0
    print("start benchmark binary search opt, %d times repeat:" % samples)
    for kk in range(samples):
        cleartext = gen_sorted_array(arraySize)
        eles = [cleartext[random.randint(0,arraySize-1)] for _ in range(arraySize)]
        x = list(map(secint, cleartext))
        x = seclist(x)
        for jj in range(searchSize):
            e = secint(eles[jj])
            # print(x)
            timeS = time.perf_counter()
            oy = binary_almost_search_opt(x, arraySize, e)
            #y=mpc.run(mpc.output(oy))
            timeE = time.perf_counter()

            timeDiff = timeE-timeS 
            #print("%.3f, " % timeDiff, end="")
            totalTime += timeDiff
    print("Total repeat %d times. Average execution time is %.3fs." % (samples, totalTime/samples))
    mpc.run(mpc.shutdown())

def testRaw(arraySize=10, searchSize = 1, samples=1):
    import random
    import time

    mpc.run(mpc.start())            # required only when run with multiple parties

    totalTime = 0
    print("start benchmark binary search raw, %d times repeat:" % samples)
    for kk in range(samples):
        cleartext = gen_sorted_array(arraySize)
        eles = [cleartext[random.randint(0,arraySize-1)] for _ in range(arraySize)]
        x = list(map(secint, cleartext))
        x = seclist(x)
        for jj in range(searchSize):
            e = secint(eles[jj])
            # print(x)
            timeS = time.perf_counter()
            oy = binary_almost_search(x, arraySize, e)
            #y=mpc.run(mpc.output(oy))
            timeE = time.perf_counter()

            timeDiff = timeE-timeS 
            #print("%.3f, " % timeDiff, end="")
            totalTime += timeDiff
    print("Total repeat %d times. Average execution time is %.3fs." % (samples, totalTime/samples))
    mpc.run(mpc.shutdown())

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--opt', action='store_true')
    parser.add_argument('-e', type=int)
    parser.add_argument('-s', type=int)
    parser.add_argument('-i', type=int)


    args = parser.parse_args()

    if args.opt == True:
        testOpt(args.e, args.s, args.i)
    else:
        testRaw(args.e, args.s, args.i)
main()


        
