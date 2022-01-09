#include "../src/checker.h"

void naive_psi_opt(int8_t *int8_tersection, int8_t *aarr, int8_t *barr, int8_t size){
    for (int8_t i = 0; i < size; i++) {
        for (int8_t j = 0; j < size; j++) {
            bool omatch = (aarr[i] == barr[j]);
            bool match;
            revealOblivBool(&match, omatch, 0);
            if ( match ) {
                int8_tersection[i] = j;
                break;
            }
        } 
    }
}

char **gen_labels(const char *prefix, int nums){
    char **ptr = (char **)malloc(sizeof(char *)*nums);
    #pragma clang loop unroll(full)
    for (int i = 0; i < nums; i++){
			ptr[i] = (char *)malloc(sizeof(char)*64);
			snprintf(ptr[i], 36, "%s_%d", prefix, i);
    }
    return ptr;
}

int main(){
    int8_t size = 10;
    int8_t aarr[size];
    int8_t barr[size];
    //char **la = gen_labels("aarr", size);
    //char **lb = gen_labels("barr", size);
    checker_make_symbolic(&aarr, sizeof(aarr), "aarr");
    checker_make_symbolic(&barr, sizeof(barr), "barr");

    //#pragma clang loop unroll(full)
	//for (int i = 0; i < size; i++) {
	//	aarr[i] = checker_int8(la[i]);
    //    barr[i] = checker_int8(lb[i]);
	//}

    #pragma clang loop unroll(full)
	for (int ll = 0; ll < size; ll++) {
    	#pragma clang loop unroll(full)
		for (int kk = ll+1; kk < size; kk++) {
            checker_assume(aarr[ll] != aarr[kk]);
            checker_assume(barr[ll] != barr[kk]);
		}
	}
    int8_t intersection[size];
    for (int i = 0; i < size; i++){
        intersection[i] = -1;
    }
    checker_init(1);
    naive_psi_opt(intersection, aarr, barr, size);
    checker_check_int8_array(intersection, size);
    return 0;
}