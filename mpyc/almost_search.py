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
        v = v + random.randrange(0,3)
        l.append(v)

    return l 

def binary_almost_search(haystack, haystack_length, needle):
    mpc.run(mpc.start())

    shared_haystack = seclist(mpc.input(haystack, senders=[0])[0])
    shared_needle = mpc.input(needle, senders=[1])[0]

    upper_bound = int(math.log2(haystack_length)) + 1
    index = secint(-1)
    iimin = secint(0)
    iimax = secint(haystack_length - 1)
    bb = shared_needle
    for _ in range(upper_bound):
        ii = iimin + iimax
        cc =  ii % 2
        iimid = mpc.if_else( cc, mpc.div(iimax+iimin-1, 2), mpc.div(iimax+iimin, 2) )
        aa = shared_haystack[iimid] # oram_read(haystack, haystack_length, iimid)
        oeq = aa == bb 
        index = mpc.if_else(oeq, iimid, index)
        left = shared_haystack[iimid-1]
        index = mpc.if_else(aa==left, iimid-1, index)

        right = shared_haystack[iimid+1]
        index = mpc.if_else(aa==right, iimid+1, index)

        ogt = aa > bb
        iimin = mpc.if_else(ogt, iimin, iimid+2)
        iimax = mpc.if_else(ogt, iimid-2, iimax)
    oindex = mpc.run(mpc.output(index))
    mpc.run(mpc.shutdown())
    return oindex

def binary_almost_search_opt(haystack, haystack_length, needle):
    mpc.run(mpc.start())
    shared_haystack = seclist(mpc.input(haystack, senders=[0])[0])
    shared_needle = mpc.input(needle, senders=[1])[0]
    
    upper_bound = int(math.log2(haystack_length)) + 1
    index = secint(-1)
    iimin = secint(0)
    iimax = secint(haystack_length - 1)
    bb = shared_needle
    for _ in range(upper_bound):
        ii = iimin + iimax
        cc =  ii % 2
        iimid = mpc.if_else( cc, mpc.div(iimax+iimin-1, 2), mpc.div(iimax+iimin, 2) )
        aa = shared_haystack[iimid] # oram_read(haystack, haystack_length, iimid)
        eq = mpc.run(mpc.eq_public(aa, bb))
        if eq:
            index = iimid 
            break  
        left = shared_haystack[iimid-1]
        index = mpc.if_else(aa==left, iimid-1, index)

        right = shared_haystack[iimid+1]
        index = mpc.if_else(aa==right, iimid+1, index)

        ogt = aa > bb
        iimin = mpc.if_else(ogt, iimin, iimid+2)
        iimax = mpc.if_else(ogt, iimid-2, iimax)
    oindex = mpc.run(mpc.output(index))
    mpc.run(mpc.shutdown())
    return oindex


def bench(isopt = False, arraySize=10, searchSize = 1, samples=1):
    import random
    import time
    MIN = 0
    repeat = samples
    MAX = 2*arraySize

    totalTime = 0
    print("start benchmark almost search %s, %d times repeat:" % ("opt" if isopt else "", samples))
    for kk in range(samples):
        cleartext = gen_sorted_array(arraySize)
        eles = [cleartext[random.randint(0,arraySize-1)] for _ in range(searchSize)]
        x = list(map(secint, cleartext))
        for jj in range(searchSize):
            e = secint(eles[jj])
            if isopt:
                timeS = time.perf_counter()
                oy = binary_almost_search_opt(x, arraySize, e)
                timeE = time.perf_counter()
            else:
                timeS = time.perf_counter()
                oy = binary_almost_search(x, arraySize, e)
                timeE = time.perf_counter()
            timeDiff = timeE-timeS 
            #print("%.3f, " % timeDiff, end="")
            totalTime += timeDiff
        print("Sample %d cost %.3f" % (kk, timeDiff))
    print("Total repeat %d times. Average execution time is %.3fs." % (samples, totalTime/samples))

    f = open("Party.csv", "a+")
    f.write("%s, %d, Time/s, %.3f,%d\n" 
    % ("almost_search_opt" if isopt else "almost_search", arraySize, totalTime/samples, samples))
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


        
