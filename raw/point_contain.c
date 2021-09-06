#include "checker.h"

typedef struct OblivPoint {
    int x;
    int y;
}OPoint;

typedef struct OblivVector {
    OPoint begin;
    OPoint end;
}OVector;

int direction(OPoint *p, OVector *v){
    int x1 = v->begin.x - p->x;
    int y1 = v->begin.y - p->y;
    int x2 = v->end.x - v->begin.x;
    int y2 = v->end.y - v->begin.y;
    int delta = x1 * y2 - x2 * y1;
    int res = (delta > 0) - (delta < 0);
    return res;
}

void point_contain_opt(int *out, OPoint *p, OVector *v, int size){
    *out = 1;
    int first_d = direction(p, &v[0]);
    for (int i = 1; i < size; i++) {
        int next_d = direction(p, &v[i]);
        bool at_edge = first_d == 0 | next_d == 0;
        bool findout;
        revealOblivBool(&findout, at_edge, 0);
        if (findout) {
            *out = 0;
            break;
        } else {
            bool diff_direct = first_d != next_d;
            revealOblivBool(&findout, diff_direct, 0);
            if (findout) {
                *out = -1;
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
	OPoint p;
    int tx;
    checker_make_symbolic(&tx, sizeof(tx), "tx");
	int ty;
    checker_make_symbolic(&ty, sizeof(ty), "ty");
    p.x = tx;
    p.y = ty;

    int size = 6;
    OVector v[size];
    char **vv = gen_labels("v", size);
    // assume a line has different start and end point
    for (int i = 0; i < size; i++) {
        char ** ll = gen_labels(vv[i], 4);
        v[i].begin.x = checker_int(ll[0]);
        v[i].begin.y = checker_int(ll[1]);
        v[i].end.x = checker_int(ll[2]);
        v[i].end.y = checker_int(ll[3]);
        checker_assume( (v[i].begin.x != v[i].end.x) | (v[i].begin.y != v[i].end.y));
    }
    // assume one line's end is one line's start | is a poly
    for (int i = 0; i < size; i++) {

    }

    // assume the poly is convex


	int out;
    point_contain_opt(&out, &p, v, size);
    checker_check_int(out);
    return 0;
}