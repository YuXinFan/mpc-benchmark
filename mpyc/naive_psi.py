from mpyc.runtime import mpc    # load MPyC
secint = mpc.SecInt()           # 32-bit secure MPyC integers
mpc.run(mpc.start())            # required only when run with multiple parties
import traceback     
import math  
# void naive_psi_opt(int8_t *int8_tersection, int8_t *aarr, int8_t *barr, int8_t size){
#     for (int8_t i = 0; i < size; i++) {
#         for (int8_t j = 0; j < size; j++) {
#             bool omatch = (aarr[i] == barr[j]);
#             bool match;
#             revealOblivBool(&match, omatch, 0);
#             if ( match ) {
#                 int8_tersection[i] = barr[j];
#                 break;
#             }
#         } 
#     }
# }
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

def main(samples=1):
    import random
    import time
    MIN = 0
    MAX = 100
    n = 100

    totalTime = 0
    print("start benchmark Batcher Sort, %d times repeat:" % samples)
    for kk in range(samples):
        caarr = random.sample(range(MIN, MAX), n)
        cbarr = random.sample(range(MIN, MAX), n)

        saarr = list(map(secint, caarr))
        sbarr = list(map(secint, cbarr))


        timeS = time.perf_counter()
        idx = naive_psi_opt(saarr, sbarr, n)
        mpc.run(mpc.output(idx))
        timeE = time.perf_counter()

        print("idx:",mpc.output(idx))
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

