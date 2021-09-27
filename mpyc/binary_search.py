from mpyc.runtime import mpc    # load MPyC
from mpyc.seclists import seclist, secindex
secint = mpc.SecInt()           # 32-bit secure MPyC integers
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
async def obinary_search(haystack, haystack_length, needle):
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

def bench(isopt = False, arraySize=10, searchSize = 1, samples=1):
    import random
    import time
    MIN = 0
    repeat = samples
    MAX = 2*arraySize

    func = None 
    if isopt :
        func = obinary_search_opt
    else:
        func = obinary_search

    mpc.run(mpc.start())            # required only when run with multiple parties

    totalTime = 0
    print("start benchmark binary search %s, %d times repeat:" % ("opt" if isopt else "", samples))
    for kk in range(samples):
        cleartext = gen_sorted_array(arraySize)
        eles = [cleartext[random.randint(0,arraySize-1)] for _ in range(searchSize)]
        x = list(map(secint, cleartext))
        x = seclist(x)
        for jj in range(searchSize):
            e = secint(eles[jj])
            # print(x)
            timeS = time.perf_counter()
            oy = func(x, arraySize, e)
            #y=mpc.run(mpc.output(oy))
            timeE = time.perf_counter()

            timeDiff = timeE-timeS 
            #print("%.3f, " % timeDiff, end="")
            totalTime += timeDiff
        print("Sample %d cost %.3f" % (kk, timeDiff))
    print("Total repeat %d times. Average execution time is %.3fs." % (samples, totalTime/samples))

    mpc.run(mpc.shutdown())
    f = open("Party.csv", "a+")
    f.write("%s, %d, Time/s, %.3f,%d\n" 
    % ("binary_search_opt" if isopt else "binary_search", arraySize,totalTime/samples, samples))
    f.close()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--opt', action='store_true')
    parser.add_argument('-e', type=int)
    parser.add_argument('-s', type=int)
    parser.add_argument('-i', type=int)


    args = parser.parse_args()

    bench(args.opt, args.e, args.s, args.i)
main()
