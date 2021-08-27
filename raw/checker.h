#include "stdbool.h"
#include "stdio.h"
#include "string.h"
#include "malloc.h"
#include "klee/klee.h"
// save each revealed constraints
// get output and add the constraint to it 
// backtrace and update saved constraints   or multi-thread with fork
typedef struct Pair {
    bool expr;
    bool value;
} Pair;

Pair A[100];
int i = 0;
void checker_make_symbolic(void *addr, size_t nbytes, const char *name){
    klee_make_symbolic(addr, nbytes, name);
}

void checker_assume(uintptr_t condition) {
    klee_assume(condition);
    klee_print_expr("Assume", condition);
}

void checker_check_int_array(int o){

} 
void checker_check_float_array(int o){
    
} 
void checker_check_int(int o){
    char *label = (char *)malloc(sizeof(char)*100);
    for (int j = 0; j < i; j++) {
        sprintf(label, "MARK:Output is %d, total %d, now %d-th", o, i, j+1);
        const char *const_res =  label;
        klee_print_range(const_res, A[j].expr);
    }
}
void checker_check_float(float o){
    char *label = (char *)malloc(sizeof(char)*100);
    for (int j = 0; j < i; j++) {
        sprintf(label, "MARK:Output is %3f, total %d, now %d-th", o, i, j+1);
        const char *const_res =  label;
        klee_print_range(const_res, A[j].expr);
    }
}


static inline void revealOblivBool(bool *a, bool aa, int party){
    *a = aa;
    A[i].expr = aa;
    i++;
}