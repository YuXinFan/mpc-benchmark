import subprocess
import re
import os
import argparse
import gen_query
import time 
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str)
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--clang', action='store_true')
    parser.add_argument('--sym', action='store_true')
    parser.add_argument('--gen', action='store_true')
    parser.add_argument('--solve', action='store_true')
    parser.add_argument('--pos', type=int)
    parser.add_argument('--postfix', type=int)



    args = parser.parse_args()

    #compiler
    cfile = args.input
    bcfile = cfile.replace(".c", ".bc")
    qfile = (cfile.split("/")[-1]).replace(".c", ".kquery")
    ofile = (cfile.split("/")[-1]).replace(".c", ".out")

    if (args.all or args.clang):

        exit_code = subprocess.call("clang-9 -I ~/mine/klee/include -emit-llvm -c -g -O0 -Xclang -disable-O0-optnone  -o ../build/" + bcfile + " ../example/" + cfile, shell=True)
        if exit_code != 0:
            print("[Checker] Compiler %s failed, exit code %d." % (cfile, exit_code))
            exit(exit_code)
        else:
            print("[Checker] Compiler %s done." % cfile)
        # check compiler states
    print(args.postfix)
    if (args.all or args.sym):
        #klee 
        folder = "../log"
        if not os.path.isdir(folder):
            os.mkdir(folder)
        outfile = open("../log/"+ofile + "" if args.postfix == None else str(args.postfix), "w+")
        # exit_code = subprocess.call("klee --disable-verify \
        #     --use-query-log=solver:kquery \
        #     --external-calls=all \
        #     --posix-runtime \
        #     --optimize-array=all \
        #     --write-kqueries \
        #     --write-no-tests \
        #     " + bcfile , shell=True, stderr=outfile)
        exit_code = subprocess.call("klee --disable-verify \
            --use-query-log=solver:kquery \
            --external-calls=all \
            --posix-runtime \
            --write-kqueries \
            --write-no-tests \
            ../build/" + bcfile , shell=True, stderr=outfile)
        outfile.close()
        # check klee states
        if exit_code != 0:
            print("[Checker] Symbolic execute %s failed, exit code %d." % (bcfile, exit_code))
            exit(exit_code)
        else:
            print("[Checker] Symbolic %s done." % bcfile)
    num_declassified = 0
    if (args.all or args.gen):
        #construct query
        num_declassified=gen_query.main("../log/"+ofile,qfile)
        print("[Checker] Generate solver query done.")
        if (num_declassified == 0):
            print("[Checker] Filter all constraints. Solver Done")
        # check query states
    num_declassified = args.pos if num_declassified == 0 else num_declassified
    if (args.all or args.solve):
    # run kleaver 
        for i in range(num_declassified):
            exit_code = subprocess.call("kleaver ../log/%s%d" % (qfile, i), shell=True)
            # checker kleaver states
            if exit_code != 0:
                print("[Checker] Solver failed to solve, exit code %d." % exit_code)
                exit(exit_code)
            else:
                print("[Checker] Solver %d-th declassified variable done." % (i+1))


main()