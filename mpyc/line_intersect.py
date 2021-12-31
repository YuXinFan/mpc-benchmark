import random 
from mpyc.runtime import mpc    # load MPyC
secflt = mpc.SecFlt()

def line_intersect(a,b,c,d):
    mpc.run(mpc.start())
    shared_a = mpc.input(a, senders=[0])[0]
    shared_b = mpc.input(b, senders=[0])[0]
    shared_c = mpc.input(c, senders=[1])[0]
    shared_d = mpc.input(d, senders=[1])[0]

    p = []
    area_abc = (shared_a[0] - shared_c[0]) * (shared_b[1] - shared_c[1]) - (shared_a[1] - shared_c[1]) * (shared_b[0] - shared_c[0])
    area_abd = (shared_a[0] - shared_d[0]) * (shared_b[1] - shared_d[1]) - (shared_a[1] - shared_d[1]) * (shared_b[0] - shared_d[0])
    

    area_cda = (shared_c[0] - shared_a[0]) * (shared_d[1] - shared_a[1]) - (shared_c[1] - shared_a[1]) * (shared_d[0] - shared_a[0])
    area_cdb = area_cda + area_abc - area_abd 

    t = area_cda / ( area_abd - area_abc )
    dx= t * (shared_b[0] - shared_a[0])
    dy= t * (shared_b[1] - shared_a[1])
    p = [shared_a[0] + dx, shared_a[1] + dy]
    false1 = (area_cda * area_cdb) >= 0.0
    false2 = (area_abc * area_abd) >= 0.0
    is_cross = 1-(false1 | false2)
    #p = p*false 
    ois_cross = mpc.run(mpc.output(is_cross))
    op = mpc.run(mpc.output(p))

    return (ois_cross, op)

def line_intersect_opt(a,b,c,d):
    mpc.run(mpc.start())
    shared_a = mpc.input(a, senders=[0])[0]
    shared_b = mpc.input(b, senders=[0])[0]
    shared_c = mpc.input(c, senders=[1])[0]
    shared_d = mpc.input(d, senders=[1])[0]
    
    p = []
    area_abc = (shared_a[0] - shared_c[0]) * (shared_b[1] - shared_c[1]) - (shared_a[1] - shared_c[1]) * (shared_b[0] - shared_c[0])

    area_abd = (shared_a[0] - shared_d[0]) * (shared_b[1] - shared_d[1]) - (shared_a[1] - shared_d[1]) * (shared_b[0] - shared_d[0])
    is_cd_same_side_of_ab = (area_abc * area_abd) >= 0.0

    area_cda = (shared_c[0] - shared_a[0]) * (shared_d[1] - shared_a[1]) - (shared_c[1] - shared_a[1]) * (shared_d[0] - shared_a[0])
    area_cdb = area_cda + area_abc - area_abd
    is_ab_same_side_of_cd = (area_cda * area_cdb) >= 0.0
    onot_insect = is_ab_same_side_of_cd | is_cd_same_side_of_ab 
    not_insect = mpc.run(mpc.eq_public(onot_insect, 1))
    if ( not_insect ):
        return p
    
    t = area_cda / ( area_abd - area_abc )
    dx= t * (shared_b[0] - shared_a[0])
    dy= t * (shared_b[1] - shared_a[1])
    p = [shared_a[0] + dx, shared_a[1] + dy]
    return p

def bench(isopt = False, arraySize=10, samples=1):
    import random
    import time

    totalTime = 0
    print("start benchmark line_insect %s, %d times repeat:" % ("opt" if isopt else "", samples))
    for kk in range(samples):
        for jj in range(arraySize):
            clear_a = [random.uniform(0, 1000), random.uniform(0, 1000)]
            clear_b = [random.uniform(0, 1000), random.uniform(0, 1000)]
            clear_c = [random.uniform(0, 1000), random.uniform(0, 1000)]
            clear_d = [random.uniform(0, 1000), random.uniform(0, 1000)]
            sec_a = list(map(secflt, clear_a))
            sec_b = list(map(secflt, clear_b))
            sec_c = list(map(secflt, clear_c))
            sec_d = list(map(secflt, clear_d))

            if isopt:
                timeS = time.perf_counter()
                line_intersect_opt(sec_a,sec_b,sec_c,sec_d)
                #mpc.run(mpc.output(p))
                timeE = time.perf_counter()
            else:
                timeS = time.perf_counter()
                line_intersect(sec_a,sec_b,sec_c,sec_d)
                #mpc.run(mpc.output(p))
                timeE = time.perf_counter()
            timeDiff = timeE-timeS 
            # print("%.3f, " % timeDiff, end="")
            totalTime += timeDiff
        print("Sample %d cost %.3f" % (kk, timeDiff))
    print("Total repeat %d times. Average execution time is %.3fs." % (samples, totalTime/samples))

    f = open("Party.csv", "a+")
    f.write("%s, %d, Time/s, %.3f,%d\n" 
    % ("line_insect_opt" if isopt else "line_search", arraySize, totalTime/samples, samples))
    f.close()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--opt', action='store_true')
    parser.add_argument('-n', type=int)
    parser.add_argument('-i', type=int)

    args = parser.parse_args()

    bench(args.opt, args.n, args.i)
main()