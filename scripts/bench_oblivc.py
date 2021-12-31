import subprocess
import re
import os
import argparse
import pandas as pd 
import time

cases = [("batcher_sort", "quick_sort"),
            ("linear_search", "linear_search_opt"),
            ("binary_search", "binary_search_opt"),
            ("almost_search", "almost_search_opt"),
            ("naive_psi", "naive_psi_opt")]

log = "LOG:\n"

def clean_csv():
    p0 = "Party-0.csv"
    p1 = "Party-1.csv"
    if os.path.exists(p0):
        os.remove(p0)
    if os.path.exists(p1):
        os.remove(p1)

def make_csv():
    p0=pd.read_csv("Party-0.csv", names=['Name', 'InSize', 'Type', 'Val', "Repeat"])
    p1=pd.read_csv("Party-1.csv", names=['Name', 'InSize', 'Type', 'Val', "Repeat"])
    pp ={"Name": p0["Name"], "InSize": p0["InSize"],"Type": p0["Type"]}
    val = []
    l0 = p0["Val"].to_list()
    l1 = p1["Val"].to_list()
    assert(len(l0)==len(l1))
    for i in range(len(l0)):
        v1 = l0[i]
        v2 = l1[i]
        val.append(max(v1,v2))
    pp["Val"] = val 
    pp["Repeat"] = p0["Repeat"]
    ## compute performace improve 
    im = []
    for i in range(int(len(val)/3/2)):
        im.append(0)
        im.append(0)
        im.append(0)
        if (pp["Val"][i*6] == 0.0):
            im.append(0)
        else:
            im.append((pp["Val"][i*6]-pp["Val"][i*6+3])/pp["Val"][i*6])
        if (pp["Val"][i*6+1] == 0.0):
            im.append(0)
        else:
            im.append((pp["Val"][i*6+1]-pp["Val"][i*6+1+3])/pp["Val"][i*6+1])
        if (pp["Val"][i*6+2] == 0.0):
            im.append(0)
        else:
            im.append((pp["Val"][i*6+2]-pp["Val"][i*6+2+3])/pp["Val"][i*6+2])

    pp["Reduce"] = im
    print(pp)
    df = pd.DataFrame(pp)
    df.to_csv("./Party.csv", index=False)
    print(df)

def gen_param(bname, scale, repeat):
    if bname == cases[0][0] or bname == cases[0][1] \
        or bname == cases[4][0] or bname == cases[4][1]:
        return "-n %s -i %s" % (scale, repeat)
    elif bname == cases[1][0] or bname == cases[1][1] \
        or bname == cases[2][0] or bname == cases[2][1] \
        or bname == cases[3][0] or bname == cases[3][1]:
        return "-e %s -s 1 -i %s" % (scale, repeat)
    else:
        os.error("gen_param failed: (%s, %s, %s)" % (bname,scale,repeat))

def bench_target(bname, scale_range, repeat):
    if type(scale_range)==int:
        scale_range = [scale_range]
    for j in scale_range:
        params = gen_param(bname, j, repeat)
        global log 
        log += " %s " % params
        bench_single(bname, params)

def bench_single(bname, bparams):
    cmd = "../oblivc/build/tests/bench_%s  %s & ../oblivc/build/tests/bench_%s  %s -c localhost" % (bname, bparams, bname, bparams)
    exit_code = subprocess.call(cmd, shell=True)
    if (exit_code != 0):
        os.error("Failed:" + cmd + "\n")
    time.sleep(1)

def bench_all(scale_range, repeat):
    
    if type(scale_range)==int:
        scale_range = [scale_range]
    for i in range(len(cases)):
        for j in scale_range:
            params = gen_param(cases[i][0], j, repeat)
            bench_single(cases[i][0], params)
            bench_single(cases[i][1], params)

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--all', action='store_true')

    parser.add_argument('--single', action='store_true')
    parser.add_argument('--name', type=str)
    parser.add_argument('--params', type=str)
    parser.add_argument('--range', nargs='+', help='<Required> Set flag', required=True)
    parser.add_argument('--target', action='store_true')
    parser.add_argument('--repeat', type=int)

    parser.add_argument('--csv', action="store_true")

    parser.add_argument("--man", action="store_true")

    args = parser.parse_args()

    if args.man:
        clean_csv()
        bench_single("binary_search","-e 100000 -s 100 -i 10")
        bench_single("binary_search_opt","-e 100000 -s 100 -i 10")
        
        bench_single("naive_psi","-n 10000 -i 10")
        bench_single("naive_psi_opt","-n 10000 -i 10")
        
        bench_single("line_insect","-n 10000  -i 10")
        bench_single("line_insect_opt","-n 10000 -i 10")

        bench_single("almost_search","-e 100000 -s 100 -i 1")
        bench_single("almost_search_opt","-e 100000 -s 100 -i 1")
        
        bench_single("linear_search","-e 100000 -s 100 -i 10")
        bench_single("linear_search_opt","-e 100000 -s 100 -i 10")

        make_csv()
        return 

    if (args.csv):
        make_csv()
    else:
        clean_csv()
        if (args.all):
            bench_all(args.range, args.repeat)
            make_csv()
        elif args.single:
            bench_single(args.name, args.params)
        elif (args.target):
            bench_target(args.name, args.range, args.repeat)
    print(log)

main()
