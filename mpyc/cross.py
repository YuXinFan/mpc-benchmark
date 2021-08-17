import random 
from mpyc.runtime import mpc    # load MPyC
secflt = mpc.SecFlt()
mpc.run(mpc.start())  

def cross_raw(a,b,c,d):
    
    p = []
    area_abc = (a[0] - c[0]) * (b[1] - c[1]) - (a[1] - c[1]) * (b[0] - c[0])
    area_abd = (a[0] - d[0]) * (b[1] - d[1]) - (a[1] - d[1]) * (b[0] - d[0])
    

    area_cda = (c[0] - a[0]) * (d[1] - a[1]) - (c[1] - a[1]) * (d[0] - a[0])
    area_cdb = area_cda + area_abc - area_abd 

    t = area_cda / ( area_abd - area_abc )
    dx= t * (b[0] - a[0])
    dy= t * (b[1] - a[1])
    p = [a[0] + dx, a[1] + dy]
    false1 = (area_cda * area_cdb) >= 0.0
    false2 = (area_abc * area_abd) >= 0.0
    is_cross = 1-(false1 | false2)
    #p = p*false 
    return (is_cross, p)

@mpc.coroutine  
async def cross_opt(a,b,c,d):
    
    p = []
    area_abc = (a[0] - c[0]) * (b[1] - c[1]) - (a[1] - c[1]) * (b[0] - c[0])
    area_abd = (a[0] - d[0]) * (b[1] - d[1]) - (a[1] - d[1]) * (b[0] - d[0])
    false = (area_abc * area_abd) >= 0.0
    no_cross = await mpc.eq_public(false, 1)
    if ( no_cross ):
        return p

    area_cda = (c[0] - a[0]) * (d[1] - a[1]) - (c[1] - a[1]) * (d[0] - a[0])
    area_cdb = area_cda + area_abc - area_abd 
    false = (area_cda * area_cdb) >= 0.0
    no_cross = await mpc.eq_public(false, 1)
    if ( no_cross ):
        return p
    
    t = area_cda / ( area_abd - area_abc )
    dx= t * (b[0] - a[0])
    dy= t * (b[1] - a[1])
    p = [a[0] + dx, a[1] + dy]
    return p

def main():
    samples = 100
    import time 
    totalTime=0
    print("start benchmark Batcher Sort, %d times repeat:" % samples)

    for i in range(samples):
        clear_a = [random.uniform(0, 1000), random.uniform(0, 1000)]
        clear_b = [random.uniform(0, 1000), random.uniform(0, 1000)]
        clear_c = [random.uniform(0, 1000), random.uniform(0, 1000)]
        clear_d = [random.uniform(0, 1000), random.uniform(0, 1000)]
        sec_a = list(map(secflt, clear_a))
        sec_b = list(map(secflt, clear_b))
        sec_c = list(map(secflt, clear_c))
        sec_d = list(map(secflt, clear_d))

        timeS = time.perf_counter()
        p = cross_opt(sec_a,sec_b,sec_c,sec_d)
        #mpc.run(mpc.output(p))
        timeE = time.perf_counter()
        timeDiff = timeE-timeS 
        # print("%.3f, " % timeDiff, end="")
        totalTime += timeDiff
        print(p)
        # if mpc.output(p[0]):
        #     print("cross: ", p)
        #     pass
        # else:
        #     print("not cross: ", p)
        #     pass
    print()
    print("Total repeat %d times. Total execution time is %.3fs." % (samples, totalTime))
main()
mpc.run(mpc.shutdown())