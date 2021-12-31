#include "../src/checker.h"


void binary_almost_search_opt_main(int *idx, int needle, int* arr, int l, int r) {
    if (r >= l)
    {
        int mid = l + (r - l) / 2;
        // If the element is present at
        // one of the middle 3 positions
        bool left = mid > l;
        if ( left ){
            left = arr[mid-1] == needle;
        } 
        bool right = mid < r;
        if (right) {
            right =  arr[mid+1] == needle;
        }
        bool oeq = arr[mid] == needle;
        bool eq;
        revealOblivBool(&eq, oeq, 0);
        if (eq){
            *idx = mid;
            return ;
        }else if (left){
                *idx = (mid-1);
        }else if (right) {
                *idx = (mid + 1);
        }else {
            if (arr[mid] > needle){
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
    for(int i = 0; i < arr_size; i++){
        bool c1 = true;bool c2=true;bool c3=true;
        for(int j = 0; j < arr_size; j++){
            if (j < i-1){
                c1 = c1 & arr[j]<arr[i];
                c2 = c2 & arr[j]<arr[i];
                c3 = c3 & arr[j]<arr[i];
            }else if ( j == i -1){
                c1 = c1 & arr[j]<arr[i];
                c2 = c2 & arr[j]>arr[i];
                c3 = c3 & arr[j]<arr[j];
            }else if (j == i + 1){
                c1 = c1 & arr[j]>arr[i];
                if ( i > 0 ){
                    c2 = c2 & arr[j]>arr[i-1];
                }
                c3 = c3 & arr[j]<arr[i];
            }else if ( j > i + 1){
                c1 = c1 & arr[j]>arr[i];
                if ( i > 0 ){
                    c2 = c2 & arr[j]>arr[i-1];
                }
                if ( i < arr_size-1){
                    c3 = c3 & arr[j]>arr[i+1];
                }
            }
        }
        checker_assume(c1|c2|c3);
    }

    checker_make_symbolic(&val, sizeof(val), "val");

    binary_almost_search_opt(&idx, val, arr, arr_size);
    checker_check_int(idx);
}