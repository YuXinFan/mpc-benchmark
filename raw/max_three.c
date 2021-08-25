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
typedef struct Value {
    Pair *expr;
} Value;

typedef struct Key {
    char *str;
} Key;

typedef struct Map {
    Key key;
    Value value;
} Map;


Map ms[10];
Pair A[10];
int i = 0;
static inline void revealOblivBool(bool *a, bool aa, int party){
    *a = aa;
    // get the expr as constraint = value
    //int v = klee_get_value_i32(aa);
    //klee_print_range("reveal", aa);
    A[i].expr = aa;
    //A[i].value = v;
    i++;

}

void max_three_opt(int *o, int *a, int *b, int *c){
    *o = 0;
    int max = *a;
    if (max < *b) {
        max = *b;
        *o = 1;
    }
    bool ol = max < *c;
    bool l;
    revealOblivBool(&l, ol,0);
    if (l) {
        max = *c;
        *o = 2;
    }
}

int main() {
    int a;
    int b;
    int c;
    int o;
    klee_make_symbolic(&a, sizeof(a), "secret_a");
    klee_make_symbolic(&b, sizeof(b), "secret_b");
    klee_make_symbolic(&c, sizeof(c), "secret_c");
    klee_make_symbolic(&o, sizeof(o), "o");

    max_three_opt(&o, &a, &b, &c);
    
    char *label = (char *)malloc(sizeof(char)*100);
    char output[10];
    sprintf(output,"%d",o);
    for (int j = 0; j < i; j++) {
        sprintf(label, "Output is %d, total %d, now %d-th", o, i, j+1);
        const char *const_res =  label;
        klee_print_range(const_res, A[j].expr);
    }

    return o;
}