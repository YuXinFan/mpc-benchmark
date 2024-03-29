#include "stdbool.h"
#include "stdio.h"
#include "string.h"
#include "malloc.h"
#include "time.h"
#include "stdlib.h"
#include "klee/klee.h"

// save each revealed constraints
// get output and add the constraint to it 
// backtrace and update saved constraints   or multi-thread with fork
typedef struct Pair {
    bool expr;
    bool value;
} Pair;

Pair A[10000];
int ChecherIDX = 0;
void checker_make_symbolic(void *addr, size_t nbytes, const char *name){
    klee_make_symbolic(addr, nbytes, name);
    printf("[Checker] Make symbolic %s\n", name);
}

int8_t checker_int8(const char *name){
	int8_t x;
	checker_make_symbolic(&x, sizeof(x), name);
	return x;
}

int checker_int(const char *name){
	int x;
	checker_make_symbolic(&x, sizeof(x), name);
	return x;
}

void checker_assume(uintptr_t condition) {
    klee_assume(condition);
    klee_print_expr("[Part-A] Assume", condition);
}

void checker_check_int8_array(int8_t *o, int size, bool range ){
   
    srand(time(0));
    int l = rand();
    srand(ChecherIDX);
    l = l + rand();
    srand(time(0));
    l = l + rand();
    srand(ChecherIDX);
    l = l + rand();
    srand(time(0));
    l = l + rand();
    srand(ChecherIDX);
    l = l + rand();
    srand(time(0));
    l = l + rand();
    srand(ChecherIDX);
    l = l + rand();
    klee_print_expr("[Array] Size", size);
    char *label = (char *)malloc(sizeof(char)*256);
    char *ll = (char *)malloc(sizeof(char)*65);

    #pragma clang loop unroll(full)
    for (int ii = 0; ii < size; ii++) {
        snprintf(ll, 64, "[Part-B] id %d, array idx %d", l, ii);
        if (range) {
            klee_print_range(ll, o[ii]);
        }else{
            klee_print_expr(ll, o[ii]);
        }
    }

    klee_print_expr("[CheckerIdx] ", ChecherIDX);
    #pragma clang loop unroll(full)
    for (int j = 0; j < ChecherIDX; j++) {
        sprintf(label, "[Part-C] id %d, total %d, now %d-th", l, ChecherIDX, j+1);
        const char *const_res =  label;
        klee_print_range(const_res, A[j].expr);
    }
} 
void checker_check_float_array(int o){
    
} 
void checker_check_int(int o){
    char *label = (char *)malloc(sizeof(char)*256);
    #pragma clang loop unroll(full)
    for (int j = 0; j < ChecherIDX; j++) {
        sprintf(label, "[Part-C] id %d, total %d, now %d-th", o, ChecherIDX, j+1);
        const char *const_res =  label;
        klee_print_range(const_res, A[j].expr);
    }
}

static inline void revealOblivBool(bool *a, bool aa, int party){
    *a = aa;
    A[ChecherIDX].expr = aa;
    ChecherIDX++;
}