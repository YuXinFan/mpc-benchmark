#include "checker.h"
#define N 16

void oram_read(void *t, void* s, int idx) {
    *(int *)t = ((int *)s)[idx];
}

void ocCopy(void* r, void* t) {
    *(int *)r = *(int *)t;
}

int obinary_search_oram(void* result, int *haystack, void* needle) {

	// upper bound = logN + 1;
	int upper_bound = 4 + 1;

	int index = -1;
	int iimin = 0;
	int iimax = N - 1;
	int iimid;

	int *aa;
	int *bb = ((int *)needle);
	bool olt;
	bool oeq;
	void * temp_element = calloc(1, sizeof(int));

	bool eq;
	for (int ii = 0; ii < upper_bound; ii++) {
		iimid = (iimin + iimax) / 2;
		oram_read(temp_element, haystack, iimid);
		aa = (int *)temp_element;
		oeq = *aa == *bb;
        bool eq;
        revealOblivBool(&eq, oeq, 0);
		if (eq) {
			ocCopy(result, temp_element);
			index = iimid;
            break;
		}else{
			olt = *aa < *bb;
			if (olt) {
				iimin = iimid + 1;
			}else {
				iimax = iimid;
			}
		}
		
	}
	free(temp_element);
	return index;
}

int main(){
    int arr_size = 16;
    int arr[arr_size];
    int val;
    int result;
    checker_make_symbolic(&arr, sizeof(arr), "arr");
    for (int i = 1; i < arr_size; i++) {
        checker_assume(arr[i-1] < arr[i]);
    }
    checker_make_symbolic(&val, sizeof(val), "val");
    int idx = obinary_search_oram(&result, arr, &val);
    checker_check_int(idx);
    return 0;
}