import subprocess
import re
import os
import argparse
import pandas as pd 
import time
log = ""

def clean_csv():
    p0 = "Party.csv"
    if os.path.exists(p0):
        os.remove(p0)

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
    for i in range(int(len(l0)/3/2)):
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
    df = pd.DataFrame(pp)
    df.to_csv("./Party.csv", index=False)
    print(df)

def bench_single(bname, params, opt):
    cmd = "python %s.py  %s %s" % (bname, params,opt)
    exit_code = subprocess.call(cmd, shell=True)
    if (exit_code != 0):
        os.error("Failed:" + cmd + "\n")
    time.sleep(1)

def bench_test():
    cases = [("batcher_sort", "quick_sort"),
            ("linear_search", "linear_search_opt"),
            ("binary_search", "binary_search_opt"),
            ("almost_search", "almost_search_opt"),
            ("naive_psi", "naive_psi_opt")]
    params = ["-n 100 -i 2", 
        "-e 100 -s 30 -i 2", 
        "-e 100 -s 30 -i 2", 
        "-e 100 -s 30 -i 2",
        "-n 100 -i 2"]
    for i in range(len(cases)):
        cmd = "./build/tests/bench_%s  %s & ./build/tests/bench_%s  %s -c localhost" % (cases[i][0], params[i], cases[i][0], params[i])
        exit_code = subprocess.call(cmd, shell=True)
        if (exit_code != 0):
            os.error("Failed:" + cmd + "\n")

        cmd = "./build/tests/bench_%s  %s & ./build/tests/bench_%s  %s -c localhost" % (cases[i][1], params[i], cases[i][1], params[i])
        exit_code = subprocess.call(cmd, shell=True)
        if (exit_code != 0):
            os.error("Failed:" + cmd + "\n")


def bench_one(btype, bname):
    tdic = {}
    tdic["sort"] = ["-n 10 -i 2",
            "-n 100 -i 2",
            "-n 1000 -i 2",
            "-n 10000 -i 2"]
    tdic["search"] = ["-e 10 -s 5 -i 2",
            "-e 100 -s 50 -i 2",
            "-e 1000 -s 500 -i 2",
            "-e 10000 -s 5000 -i 2"]
    tdic["psi"] = ["-n 10 -i 2",
            "-n 100 -i 2",
            "-n 1000 -i 2",
            "-n 10000 -i 2"]
    for i in tdic[btype]:        
        cmd = "./build/tests/bench_%s  %s & ./build/tests/bench_%s  %s -c localhost" % (bname, i, bname, i)
        exit_code = subprocess.call(cmd, shell=True)
        if (exit_code != 0):
            os.error("Failed:" + cmd + "\n")

def bench_pair(btype, bname):
    tdic = {}
    tdic["sort"] = ["-n 10 -i 10",
            "-n 100 -i 10",
            "-n 1000 -i 10",
            "-n 10000 -i 10"]
    tdic["search"] = ["-e 10 -s 1 -i 10",
            "-e 100 -s 1 -i 10",
            "-e 1000 -s 1 -i 10",
            "-e 10000 -s 1 -i 10",
            "-e 100000 -s 1 -i 10"]
    tdic["psi"] = ["-n 10 -i 10",
            "-n 100 -i 10",
            "-n 1000 -i 10",
            "-n 10000 -i 10"]
    tdic["line_insect"] = ["-n 10 -i 10",
            "-n 100 -i 10",
            "-n 1000 -i 10"]
    for i in tdic[btype]:        
        cmd = "python %s.py  %s " % (bname, i)
        exit_code = subprocess.call(cmd, shell=True)
        if (exit_code != 0):
            os.error("Failed:" + cmd + "\n")
        time.sleep(1)
        cmd = "python %s.py  %s --opt" % (bname, i)
        exit_code = subprocess.call(cmd, shell=True)
        if (exit_code != 0):
            os.error("Failed:" + cmd + "\n")
        time.sleep(1)
        
        
def bench_all():
    cases = [("batcher_sort", "quick_sort"),
            ("linear_search", "linear_search_opt"),
            ("binary_search", "binary_search_opt"),
            ("almost_search", "almost_search_opt"),
            ("naive_psi", "naive_psi_opt")]
    params = ["-n 100 -i 2", 
        "-e 100 -s 30 -i 2", 
        "-e 100 -s 30 -i 2", 
        "-e 100 -s 30 -i 2",
        "-n 100 -i 2"]
    for i in range(len(cases)):
        cmd = "./build/tests/bench_%s  %s & ./build/tests/bench_%s  %s -c localhost" % (cases[i][0], params[i], cases[i][0], params[i])
        exit_code = subprocess.call(cmd, shell=True)
        if (exit_code != 0):
            log = log + "Failed:" + cmd + "\n"

        cmd = "./build/tests/bench_%s  %s & ./build/tests/bench_%s  %s -c localhost" % (cases[i][1], params[i], cases[i][1], params[i])
        exit_code = subprocess.call(cmd, shell=True)
        if (exit_code != 0):
            log = log + "Failed:" + cmd + "\n"

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str)
    parser.add_argument('--name', type=str)

    parser.add_argument('--all', action='store_true')
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--one', action='store_true')
    parser.add_argument('--single', action='store_true')
    parser.add_argument('--params', type=str)


    parser.add_argument('--pair', action='store_true')
    parser.add_argument('--csv', action="store_true")
    parser.add_argument("--man", action="store_true")

    args = parser.parse_args()

    if args.man:
        clean_csv()
        bench_pair("search", "linear_search")
        #bench_pair("search", "binary_search")
        #bench_pair("search", "almost_search")
        #bench_pair("psi", "naive_psi")
        #bench_single("sort", "-n 100000 -i 10", "--opt")
        #bench_single("linear_search", "-e 100000 -s 100 -i 10", "--opt")
        #bench_single("binary_search", "-e 100000 -s 100 -i 2", "--opt")
        #bench_single("binary_search", "-e 100000 -s 100 -i 2", "")
        #bench_single("almost_search", "-e 100000 -s 100 -i 1", "--opt")
        #bench_single("almost_search", "-e 100000 -s 100 -i 1", "")
        #bench_single("naive_psi", "-n 10000 -i 2", "--opt")

        #bench_pair("sort", "sort")
        #bench_pair("line_insect", "line_intersect")

        return 

    if (args.csv):
        make_csv()
    else:
        clean_csv()
        if (args.test):
            bench_test()
        elif (args.all):
            bench_all()
        elif args.single:
            bench_single(args.raw, args.opt, args.params)
        elif (args.one):
            bench_one(args.type, args.name)
        elif (args.pair):
            bench_pair(args.type, args.name)
        #make_csv()
        print(log)

main()