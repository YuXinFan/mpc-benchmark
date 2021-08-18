bench_quick_sort "-n 1000 -i 10" # sort 1000 elements, repeat 10 times
bench_batcher_sort "-n 1000 -i 10" # sort 1000 elements, repeat 10 times
bench_binary_search "-e 1000 -s 20 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times
bench_binary_search_opt "-e 1000 -s 20 -i 10"  # on 1000 elements, search 20 elements, repeat 10 times

