import subprocess
import re
import os
import argparse
import gen_query
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str)
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--clang', action='store_true')
    parser.add_argument('--sym', action='store_true')
    parser.add_argument('--gen', action='store_true')
    parser.add_argument('--solve', action='store_true')

    args = parser.parse_args()

    #compiler
    cfile = args.input
    bcfile = cfile.replace(".c", ".bc")
    qfile = (cfile.split("/")[-1]).replace(".c", ".kquery")
    ofile = (cfile.split("/")[-1]).replace(".c", ".out")

    if (args.all or args.sym or args.clang):

        exit_code = subprocess.call("clang-9 -I ~/mine/klee/include -emit-llvm -c -g -O0 -Xclang -disable-O0-optnone " + cfile, shell=True)
        if exit_code != 0:
            print("[Checker] Compiler %s failed, exit code %d." % (cfile, exit_code))
            exit(exit_code)
        else:
            print("[Checker] Compiler %s done." % cfile)
        # check compiler states

    if (args.all or args.sym):
        #klee 
        folder = "./log"
        if not os.path.isdir(folder):
            os.mkdir(folder)
        outfile = open("./log/"+ofile, "w+")
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
            " + bcfile , shell=True, stderr=outfile)
        outfile.close()
        # check klee states
        if exit_code != 0:
            print("[Checker] Symbolic execute %s failed, exit code %d." % (bcfile, exit_code))
            exit(exit_code)
        else:
            print("[Checker] Symbolic %s done." % bcfile)

    if (args.all or args.gen):
        #construct query
        gen_query.main("./log/"+ofile,qfile)
        print("[Checker] Generate solver query done.")
        # check query states

    if (args.all or args.solve):
    # run kleaver 
        exit_code = subprocess.call("kleaver ./log/%s" % qfile, shell=True)
        # checker kleaver states
        if exit_code != 0:
            print("[Checker] Solver failed to solve, exit code %d." % exit_code)
            exit(exit_code)
        else:
            print("[Checker] Solver done.")

        #analyze solver result
        kquery = ""
        re.findall(r"# query (\d+), ret expr (\[?[\(0-9a-zA-Z\_\ \)]*\]?)", kquery)
        #kret = re.findall(r"")

main()