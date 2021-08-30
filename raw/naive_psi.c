#include "checker.h"
#define SYMINT8(x,s) int8_t x; \
    checker_make_symbolic(&x, sizeof(x),s); \
    checker_assume(x>0); 

#define ASSUME(x) checker_assume(x);

void naive_psi_opt(int8_t *int8_tersection, int8_t *aarr, int8_t *barr, int8_t size){
    for (int8_t i = 0; i < size; i++) {
        for (int8_t j = 0; j < size; j++) {
            bool omatch = (aarr[i] == barr[j]);
            bool match;
            revealOblivBool(&match, omatch, 0);
            if ( match ) {
                int8_tersection[i] = barr[j];
                break;
            }
        } 
    }
}

int main(){
    int8_t size = 4;
    SYMINT8(a0, "a0") 
    SYMINT8(a1, "a1") 
    SYMINT8(a2, "a2") 
    SYMINT8(a3, "a3") 

    ASSUME(a0 != a1);
    ASSUME(a0 != a2);
    ASSUME(a0 != a3);
    ASSUME(a1 != a2);
    ASSUME(a1 != a3);
    ASSUME(a2 != a3);

    SYMINT8(b0, "b0") 
    SYMINT8(b1, "b1") 
    SYMINT8(b2, "b2") 
    SYMINT8(b3, "b3")

    ASSUME(b0 != b1);
    ASSUME(b0 != b2);
    ASSUME(b0 != b3);
    ASSUME(b1 != b2);
    ASSUME(b1 != b3);
    ASSUME(b2 != b3);
    int8_t aarr[size];
    aarr[0] = a0;
    aarr[1] = a1;
    aarr[2] = a2;
    aarr[3] = a3;
    int8_t barr[size];
    barr[0] = b0;
    barr[1] = b1;
    barr[2] = b2;
    barr[3] = b3;
    int8_t intersection[size];
    intersection[0]=-1;
    intersection[1]=-1;
    intersection[2]=-1;
    intersection[3]=-1;

    naive_psi_opt(intersection, aarr, barr, size);
    checker_check_int8_array(intersection, size);
    return 0;
}