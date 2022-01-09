#include "../src/checker.h"

void linear_search_opt(int *idx, int *val, int *arr, int arr_size){
    *idx = -1;
    bool ofind;
    bool find;
    for (int i = 0; i < arr_size; i++) {
        ofind = *val == arr[i];
        revealOblivBool(&find, ofind, 0);
        if (find){
            *idx = i;
            break;
        }
    }
}

int main(){
    int arr_size = 40;
    int arr[arr_size];
    int val;
    int idx;
    checker_init(1);
    checker_make_symbolic(&arr, sizeof(arr), "arr");
    checker_make_symbolic(&val, sizeof(val), "val");

    linear_search_opt(&idx, &val, arr, arr_size);
    checker_check_int(idx);
    return 0;
}