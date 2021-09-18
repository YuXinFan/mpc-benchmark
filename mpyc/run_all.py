import subprocess

def main():

    # exit_code = subprocess.call("python almost_search.py --opt -n 10 -r 10", shell=True)
    # assert(exit_code == 0)
    # exit_code = subprocess.call("python almost_search.py --opt -n 100 -r 10", shell=True)
    # assert(exit_code == 0)

    # exit_code = subprocess.call("python almost_search.py  -n 10 -r 10", shell=True)
    # assert(exit_code == 0)
    # exit_code = subprocess.call("python almost_search.py  -n 100 -r 10", shell=True)
    # assert(exit_code == 0)

    # exit_code = subprocess.call("python binary_search.py --opt -n 10 -r 10", shell=True)
    # assert(exit_code == 0)
    # exit_code = subprocess.call("python binary_search.py --opt -n 100 -r 10", shell=True)
    # assert(exit_code == 0)

    # exit_code = subprocess.call("python binary_search.py  -n 10 -r 10", shell=True)
    # assert(exit_code == 0)
    # exit_code = subprocess.call("python binary_search.py  -n 100 -r 10", shell=True)
    # assert(exit_code == 0)

    # exit_code = subprocess.call("python linear_search.py --opt -n 10 -r 10", shell=True)
    # assert(exit_code == 0)
    # exit_code = subprocess.call("python linear_search.py --opt -n 100 -r 10", shell=True)
    # assert(exit_code == 0)

    # exit_code = subprocess.call("python linear_search.py  -n 10 -r 10", shell=True)
    # assert(exit_code == 0)
    # exit_code = subprocess.call("python linear_search.py  -n 100 -r 10", shell=True)
    # assert(exit_code == 0)

    exit_code = subprocess.call("python almost_search.py  -n 1000 -r 1", shell=True)
    assert(exit_code == 0)
    exit_code = subprocess.call("python almost_search.py --opt -n 1000 -r 1", shell=True)
    assert(exit_code == 0)

    exit_code = subprocess.call("python binary_search.py  -n 1000 -r 1", shell=True)
    assert(exit_code == 0)
    exit_code = subprocess.call("python binary_search.py  --opt -n 1000 -r 1", shell=True)
    assert(exit_code == 0)

    
    exit_code = subprocess.call("python linear_search.py  -n 1000 -r 1", shell=True)
    assert(exit_code == 0)
    exit_code = subprocess.call("python linear_search.py --opt -n 1000 -r 1", shell=True)
    assert(exit_code == 0)
main()


