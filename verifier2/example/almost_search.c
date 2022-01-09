#include "../src/checker.h"
#include "math.h"
#define N 20
#define LOG2N 4
   
   
void binary_almost_search_opt(int *idx, int needle, int* arr, int n){
    int upper_bound = LOG2N + 1;

    *idx = -1;
	int iimin = 0;
	int iimax = N - 1;
	int iimid;

	int aa;
	int bb = needle;
	bool oeq;
    bool eq;
    for (int ii = 0; ii < upper_bound; ii++) {
		iimid = (iimin + iimax) / 2;
		oeq = bb == arr[iimid];
        revealOblivBool(&eq, oeq, 0);
		if (eq) {
			*idx = iimid;
            break;
		}else{
            if ( iimid > iimin) {
                if ( bb == arr[iimid-1] ){
                    *idx = (iimid-1);
                }
            }
            if (iimid < iimax) {
                if ( bb == arr[iimid+1] ){
                    *idx = (iimid + 1);
                }
            }
            bool ogt = arr[iimid] > bb;
            if (ogt) {
                iimax = iimid-2;
            }else {
                iimin = iimid+2;
            }
		}
	}
}

int main(){
    int arr_size = N;
    int arr[arr_size];
    int val;
    int idx = -1;
    checker_init(1);
    checker_make_symbolic(&arr, sizeof(arr), "arr");
    for (int i = 1; i < arr_size; i++) {
        checker_assume(arr[i-1] < arr[i]);
    }
    checker_make_symbolic(&val, sizeof(val), "val");

    binary_almost_search_opt(&idx, val, arr, arr_size);
    checker_check_int(idx);
}