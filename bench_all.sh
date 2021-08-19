bench_quick_sort "-n 1000 -i 10" # sort 1000 elements, repeat 10 times
bench_batcher_sort "-n 1000 -i 10" # sort 1000 elements, repeat 10 times
bench_binary_search "-e 1000 -s 20 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_binary_search_opt "-e 1000 -s 20 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times

bench_linear_search "-e 1000 -s 20 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_linear_search_opt "-e 1000 -s 20 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times

bench_almost_search "-e 1000 -s 20 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_almost_search_opt "-e 1000 -s 20 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times

bench_naive_psi "-n 1000 -i 1" # on two 1000 elements array, repeat 1 times
bench_naive_psi_opt "-n 1000 -i 1"




