import subprocess
import re
import os
import argparse
import pandas as pd 

log = ""

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
    df = pd.DataFrame(pp)
    df.to_csv("./Party.csv", index=False)
    print(df)

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
            log = log + "Failed:" + cmd + "\n"

        cmd = "./build/tests/bench_%s  %s & ./build/tests/bench_%s  %s -c localhost" % (cases[i][1], params[i], cases[i][1], params[i])
        exit_code = subprocess.call(cmd, shell=True)
        if (exit_code != 0):
            log = log + "Failed:" + cmd + "\n"

def bench_one():
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
    # parser.add_argument('--input', type=str)
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--one', action='store_true')
    parser.add_argument('--pair', action='store_true')

    args = parser.parse_args()

    clean_csv()
    if (args.test):
        bench_test()
    elif (args.bench_all):
        bench_all()
    
    make_csv()
    print(log)
main()
