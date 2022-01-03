import subprocess
import re
import os
import argparse
import pandas as pd 
import time

cases = ["sort.py", 
        "linear_search.py",
        "binary_search.py",
        "almost_search.py",
        "naive_psi.py"]

log = "LOG:\n"

def gen_param(bname, scale, repeat):
    if bname == cases[0]  \
        or bname == cases[4]:
        return "-n %s -i %s" % (scale, repeat)
    elif bname == cases[1]\
        or bname == cases[2]\
        or bname == cases[3]:
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
    cmd = "python ../mpyc/%s %s -M 2" % (bname, bparams)
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

    # parser = argparse.ArgumentParser()

    # parser.add_argument('--all', action='store_true')

    # parser.add_argument('--single', action='store_true')
    # parser.add_argument('--name', type=str)
    # parser.add_argument('--params', type=str)
    # parser.add_argument('--range', nargs='+', help='<Required> Set flag', required=True)
    # parser.add_argument('--target', action='store_true')
    # parser.add_argument('--repeat', type=int)

    # parser.add_argument('--csv', action="store_true")

    # parser.add_argument("--man", action="store_true")

    # args = parser.parse_args()
    for bname in [cases[1]]:
        for i in range(10, 101, 10):
            param = gen_param(bname, i, 10)
            bench_single(bname, param)
            bench_single(bname, param + " --opt ")

main()
