function bench_one () {
    echo "------   $2   ------   $1   ------      "
    o1=`./build/tests/$1  $2 & ./build/tests/$1  $2 -c localhost`
}

bench_one bench_quick_sort "-n 100 -i 5" # sort 1000 elements, repeat 10 times
bench_one bench_batcher_sort "-n 100 -i 5" # sort 1000 elements, repeat 10 times

bench_one bench_binary_search "-e 100 -s 30 -i 5"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_binary_search_opt "-e 100 -s 30 -i 5"  # on 1000 elements, search 20 elements, repeat 10 times

bench_one bench_linear_search "-e 100 -s 30 -i 5"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_linear_search_opt "-e 100 -s 30 -i 5"  # on 1000 elements, search 20 elements, repeat 10 times

bench_one bench_almost_search "-e 100 -s 30 -i 5"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_almost_search_opt "-e 100 -s 30 -i 5"  # on 1000 elements, search 20 elements, repeat 10 times

bench_one bench_naive_psi "-n 100 -i 5"
bench_one bench_naive_psi_opt "-n 100 -i 5"
