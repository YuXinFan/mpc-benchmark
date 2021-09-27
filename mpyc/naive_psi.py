from mpyc.runtime import mpc    # load MPyC
secint = mpc.SecInt()           # 32-bit secure MPyC integers
mpc.run(mpc.start())            # required only when run with multiple parties
import traceback     

@mpc.coroutine
async def naive_psi(aarr, barr, size):
    intersect = [secint(-1)]*size
    for i in range(size):
        for j in range(size):
            intersect[i] = mpc.if_else(aarr[i]==barr[j], barr[j], intersect[i])
    return intersect

@mpc.coroutine
async def naive_psi_opt(aarr, barr, size):
    intersect = [secint(-1)]*size
    for i in range(size):
        for j in range(size):
            match = mpc.eq_public(aarr[i],barr[j])
            if await(match):
                intersect[i] = barr[j]
                break

    return intersect

def bench(isopt = False, arraySize=10, samples=1):
    import random
    import time
    MIN = 0
    MAX = 2*arraySize

    func = None 
    if isopt :
        func = naive_psi_opt
    else:
        func = naive_psi

    mpc.run(mpc.start())            # required only when run with multiple parties

    totalTime = 0
    print("start benchmark naive_psi %s, %d times repeat:" % ("opt" if isopt else "", samples))
    for kk in range(samples):
        caarr = random.sample(range(MIN, MAX), arraySize)
        cbarr = random.sample(range(MIN, MAX), arraySize)

        saarr = list(map(secint, caarr))
        sbarr = list(map(secint, cbarr))

        timeS = time.perf_counter()
        idx = func(saarr, sbarr, arraySize)
        mpc.run(mpc.output(idx))
        timeE = time.perf_counter()
        timeDiff = timeE-timeS 
        totalTime += timeDiff
        print("Sample %d cost %.3f" % (kk, timeDiff))
    print("Total repeat %d times. Average execution time is %.3fs." % (samples, totalTime/samples))

    mpc.run(mpc.shutdown())
    f = open("Party.csv", "a+")
    f.write("%s, %d, Time/s, %.3f,%d\n" 
    % ("naive_psi_opt" if isopt else "naive_psi", arraySize, totalTime/samples, samples))
    f.close()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--opt', action='store_true')
    parser.add_argument('-n', type=int)
    parser.add_argument('-r', type=int)

    args = parser.parse_args()

    bench(args.opt, args.n, args.r)
main()