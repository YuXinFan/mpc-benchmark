#include "../src/checker.h"

void max_three_opt(int *o, int *a, int *b, int *c){
    *o = 0;
    int max = *a;
    bool oll = max < *b;
    bool ll;
    revealOblivBool(&ll, oll,0);
    if (ll) {
        max = *b;
        *o = 1;
    }
    bool ol = max < *c;
    bool l;
    revealOblivBool(&l, ol,1);
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
    checker_init(2);
    checker_make_symbolic(&a, sizeof(a), "secret_a");
    checker_make_symbolic(&b, sizeof(b), "secret_b");
    checker_make_symbolic(&c, sizeof(c), "secret_c");
    checker_make_symbolic(&o, sizeof(o), "o");

    max_three_opt(&o, &a, &b, &c);
    
    checker_check_int(o);
    return o;
}