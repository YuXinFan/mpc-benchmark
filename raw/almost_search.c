#include "checker.h"
void binary_almost_search_opt_main(int *idx, int needle, int* arr, int l, int r) {
    if (r >= l)
    {
        int mid = l + (r - l) / 2;
        // If the element is present at
        // one of the middle 3 positions
        bool left = mid > l;
        if ( left ){
            left = arr[mid+1] == needle;
        } 
        bool right = mid < r;
        if (right) {
            right =  arr[mid+1] == needle;
        }
        if (arr[mid] == needle){
            *idx = mid;
        }else if (left){
                *idx = (mid-1);
        }else if (right) {
                *idx = (mid + 1);
        }else {
            bool ogt = arr[mid] > needle;
            bool gt;
            revealOblivBool(&gt, ogt, 0);
            if (gt){
                binary_almost_search_opt_main(idx, needle, arr, l, mid - 2);
            } else {
                binary_almost_search_opt_main(idx, needle, arr, mid + 2, r);
            }
        }
    }
}
void binary_almost_search_opt(int *idx, int needle, int* arr, int n){
    binary_almost_search_opt_main(idx, needle, arr, 0, n-1);
}

int main(){
    int arr_size = 16;
    int arr[arr_size];
    int val;
    int idx = -1;
    checker_make_symbolic(&arr, sizeof(arr), "arr");
    for (int i = 1; i < arr_size; i++) {
        checker_assume(arr[i-1] < arr[i]);
    }
    // for(int i = 2; i < arr_size-2; i++){
    //     checker_assume( ((arr[i-1]<arr[i]) & (arr[i] < arr[i+1])) |
    //         ( (((arr[i] < arr[i-1]) & (arr[i-2] < arr[i])) & (arr[i-1]>arr[i+1]))) |
    //         ( (((arr[i-1] < arr[i+1]) & (arr[i+1]<arr[i])) & (arr[i] < arr[i+2]))));
    // }
    // checker_assume( (arr[0] < arr[1]) | ((arr[1] < arr[0]) & (arr[0] < arr[2])));
    // checker_assume( (arr[arr_size-2] < arr[arr_size-1]) | ((arr[arr_size-3] < arr[arr_size-1]) & (arr[arr_size-1] < arr[arr_size-2])));

    checker_make_symbolic(&val, sizeof(val), "val");

    binary_almost_search_opt(&idx, val, arr, arr_size);
    checker_check_int(idx);
}