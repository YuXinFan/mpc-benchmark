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

bool Checker[10][10000];
int CheckerIDX[10];
int NUM_Checker;

void checker_make_symbolic(void *addr, size_t nbytes, const char *name){
    klee_make_symbolic(addr, nbytes, name);
    char *ll = (char *)malloc(sizeof(char)*256);
    sprintf(ll, "[~Make Symbolic] %s", name);
    klee_print_expr(ll, (int *)addr);
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
    klee_print_expr("[~Assume]", condition);
}

void checker_check_int8_array(int8_t *o, int size){
   
    klee_print_expr("[Array] Size", size);
    klee_print_expr("[PathCond]", NULL);

    char *label = (char *)malloc(sizeof(char)*256);
    char *ll = (char *)malloc(sizeof(char)*256);

    #pragma clang loop unroll(full)
    for (int ii = 0; ii < size; ii++) {
        sprintf(ll, "[State ID] [Array IDX][%d] Expr=", ii);
        const char *const_res =  ll;
        klee_print_expr(const_res, o[ii]);
    }

    #pragma clang loop unroll(full)
    for (int ii = 0; ii < NUM_Checker; ii++){
        int num_loop = CheckerIDX[ii];
        for (int kk = 0; kk < num_loop; kk++){
            sprintf(label, "[State ID] [Declassified][%d] [%d/%d] %d==", ii, kk+1, num_loop, klee_get_value_i32(Checker[ii][kk]));
            const char *const_res =  label;
            klee_print_expr(const_res, Checker[ii][kk]);
        }
    }
} 
void checker_check_float_array(int o){
    
} 
void checker_check_int(int o){
    klee_print_expr("[Array] Size", 1);
    klee_print_expr("[PathCond]", NULL);

    char *label = (char *)malloc(sizeof(char)*256);
    char *ll = (char *)malloc(sizeof(char)*256);

    #pragma clang loop unroll(full)
    for (int ii = 0; ii < 1; ii++) {
        sprintf(ll, "[State ID] [Array IDX][%d] Expr=", ii);
        const char *const_res =  ll;
        klee_print_expr(const_res, o);
    }

    #pragma clang loop unroll(full)
    for (int ii = 0; ii < NUM_Checker; ii++){
        int num_loop = CheckerIDX[ii];
        for (int kk = 0; kk < num_loop; kk++){
            sprintf(label, "[State ID] [Declassified][%d] [%d/%d] %d==", ii, kk+1, num_loop, klee_get_value_i32(Checker[ii][kk]));
            const char *const_res =  label;
            klee_print_expr(const_res, Checker[ii][kk]);
        }
    }
}

void checker_init(int num){
    NUM_Checker = num;
}

// static inline void revealOblivBool(bool *a, bool aa, int idx){
//     *a = aa;
//     Checker[idx][CheckerIDX[idx]] = aa;
//     CheckerIDX[idx] += 1;
// }

static inline bool revealOblivBool(bool aa, int idx){
    Checker[idx][CheckerIDX[idx]] = aa;
    CheckerIDX[idx] += 1;
    return aa;
}