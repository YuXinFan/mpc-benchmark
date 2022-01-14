#include "stdbool.h"
#include "stdint.h"
#include "stddef.h"
#include "../src/checker.h"
#define N 20
#define Log2N 3

int binary_almost_search(int *haystack, int* needle, int size){
    int upper_bound = Log2N + 1;

	int index = -1;
	int iimin = 0;
	int iimax = size - 1;
	int iimid;

	int aa;
	int bb = *needle;
	
    bool oeq;

	int * temp_element = calloc(1, sizeof(int));
	int * temp_left = calloc(1, sizeof(int));
	int * temp_right = calloc(1, sizeof(int));


	for (int ii = 0; ii < upper_bound; ii++) {
		iimid = (iimin + iimax) / 2;
        *temp_element = haystack[iimid];
		aa = *temp_element;
		oeq = aa == bb;
		if (oeq) {
			index = iimid;
		}
        bool ogtt = iimid > iimin;
        if ( revealOblivBool(ogtt, 0)) {
            *temp_left = haystack[iimid-1];
            int tleft = *temp_left;
            if ( tleft == bb ){
                index = (iimid-1);
            }
        }
        bool olt = iimid < iimax;
        if (revealOblivBool(olt, 1)) {
            *temp_right = haystack[iimid+1];
            int tright = *temp_right;
            if ( tright == bb ){
                index = (iimid + 1);
            }
        }
        bool ogt = aa > bb;
        if (ogt) {
            iimax = iimid-2;
        }else {
            iimin = iimid+2;
        }
		
	}
    free(temp_right);
    free(temp_left);
	free(temp_element);
	return index;
}

void binary_almost_search_main(int *idx, int *needle, int* arr, int n){
    *idx = binary_almost_search(arr, needle, n);
}

int main(){
    int arr_size = 10;
    int arr[arr_size];
    int val;
    int idx = -1;
    checker_init(2);
    checker_make_symbolic(&arr, sizeof(arr), "arr");
    checker_make_symbolic(&val, sizeof(val), "val");

    for(int i = 0; i < arr_size; i++){
        bool c1 = true;
        for(int j = 0; j < arr_size; j++){
            if (j < i-1){
                c1 = c1 & (arr[j]<arr[i]);
            }else if ( j > i + 1){
                c1 = c1 & (arr[j]>arr[i]);
            }
        }
        checker_assume(c1);
    }

    binary_almost_search_main(&idx, &val, arr, arr_size);
    checker_check_int(idx);
}