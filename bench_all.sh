
function bench_one () {
    echo "------   $2   ------   $1   ------      "
    o1=`./build/tests/$1  $2 & ./build/tests/$1  $2 -c localhost`
}

bench_one bench_quick_sort "-n 10 -i 10" # sort 1000 elements, repeat 10 times
bench_one bench_quick_sort "-n 100 -i 10" # sort 1000 elements, repeat 10 times
bench_one bench_quick_sort "-n 1000 -i 10" # sort 1000 elements, repeat 10 times
bench_one bench_quick_sort "-n 10000 -i 10" # sort 1000 elements, repeat 10 times
#bench_one bench_quick_sort "-n 100000 -i 10" # sort 1000 elements, repeat 10 times
#bench_one bench_quick_sort "-n 1000000 -i 10" # sort 1000 elements, repeat 10 times


bench_one bench_batcher_sort "-n 10 -i 10" # sort 1000 elements, repeat 10 times
bench_one bench_batcher_sort "-n 100 -i 10" # sort 1000 elements, repeat 10 times
bench_one bench_batcher_sort "-n 1000 -i 10" # sort 1000 elements, repeat 10 times
bench_one bench_batcher_sort "-n 10000 -i 10" # sort 1000 elements, repeat 10 times
#bench_one bench_batcher_sort "-n 100000 -i 10" # sort 1000 elements, repeat 10 times
#bench_one bench_batcher_sort "-n 1000000 -i 10" # sort 1000 elements, repeat 10 times


bench_one bench_binary_search "-e 10 -s 5 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_binary_search "-e 100 -s 50 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_binary_search "-e 1000 -s 500 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_binary_search "-e 10000 -s 5000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
#bench_one bench_binary_search "-e 100000 -s 50000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
#bench_one bench_binary_search "-e 1000000 -s 500000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times

bench_one bench_binary_search_opt "-e 10 -s 3 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_binary_search_opt "-e 100 -s 30 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_binary_search_opt "-e 1000 -s 300 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_binary_search_opt "-e 10000 -s 3000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
#bench_one bench_binary_search_opt "-e 100000 -s 30000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
#bench_one bench_binary_search_opt "-e 1000000 -s 300000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times

bench_one bench_linear_search "-e 10 -s 5 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_linear_search "-e 100 -s 50 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_linear_search "-e 1000 -s 500 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_linear_search "-e 10000 -s 5000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
#bench_one bench_linear_search "-e 100000 -s 50000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
#bench_one bench_linear_search "-e 1000000 -s 500000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times

bench_one bench_linear_search_opt "-e 10 -s 3 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_linear_search_opt "-e 100 -s 30 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_linear_search_opt "-e 1000 -s 300 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_linear_search_opt "-e 10000 -s 3000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
#bench_one bench_linear_search_opt "-e 100000 -s 30000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
#bench_one bench_linear_search_opt "-e 1000000 -s 300000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times

bench_one bench_almost_search "-e 10 -s 5 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_almost_search "-e 100 -s 50 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_almost_search "-e 1000 -s 500 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_almost_search "-e 10000 -s 5000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
#bench_one bench_almost_search "-e 100000 -s 50000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
#bench_one bench_almost_search "-e 1000000 -s 500000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times

bench_one bench_almost_search_opt "-e 10 -s 3 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_almost_search_opt "-e 100 -s 30 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_almost_search_opt "-e 1000 -s 300 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_one bench_almost_search_opt "-e 10000 -s 3000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
#bench_one bench_almost_search_opt "-e 100000 -s 30000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
#bench_one bench_almost_search_opt "-e 1000000 -s 300000 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times

bench_one bench_naive_psi "-n 10 -i 10"
bench_one bench_naive_psi "-n 100 -i 10"
bench_one bench_naive_psi "-n 1000 -i 10"
bench_one bench_naive_psi "-n 10000 -i 10"
#bench_one bench_naive_psi "-n 100000 -i 10"
#bench_one bench_naive_psi "-n 1000000 -i 10"

bench_one bench_naive_psi_opt "-n 10 -i 10"
bench_one bench_naive_psi_opt "-n 100 -i 10"
bench_one bench_naive_psi_opt "-n 1000 -i 10"
bench_one bench_naive_psi_opt "-n 10000 -i 10"
#bench_one bench_naive_psi_opt "-n 100000 -i 10"
#bench_one bench_naive_psi_opt "-n 1000000 -i 10"

#bench_one bench_line_insect "-n 10"

#bench_point_contain bench_point_contain_opt 

#bench_gs
#bench_gs_textbook



