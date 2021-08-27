#include "checker.h"
#include "limits.h"
#include "float.h"

#define a0 A->S.x
#define a1 A->S.y
#define b0 A->E.x
#define b1 A->E.y
#define c0 B->S.x
#define c1 B->S.y
#define d0 B->E.x
#define d1 B->E.y

typedef struct Point{
    float x;
    float y;
} Point;

typedef struct OblivPoint{
    float x;
    float y;
} OPoint;

typedef struct OblivLine{
    OPoint S;
    OPoint E;
}OLine;

void line_insect_opt(OPoint *p, OLine *A, OLine *B){
    float area_abc = (a0 - c0) * (b1 - c1) - (a1 - c1) * (b0 - c0);
    float area_abd = (a0 - d0) * (b1 - d1) - (a1 - d1) * (b0 - d0);
    bool is_cd_same_side_of_ab = (area_abc * area_abd) >= 0;

    float area_cda = (c0 - a0) * (d1 - a1) - (c1 - a1) * (d0 - a0);
    float area_cdb = area_cda + area_abc - area_abd; 
    bool is_ab_same_side_of_cd = (area_cda * area_cdb) >= 0;
    
    bool ois_not_insect = is_ab_same_side_of_cd  | is_cd_same_side_of_ab;
    bool is_not_insect;
    revealOblivBool(&is_not_insect, ois_not_insect, 0);
    if (is_not_insect){
        p->x = FLT_MIN;
        p->y = FLT_MIN;
    }else{
        float t = area_cda / ( area_abd - area_abc );
        float dx= t * (b0 - a0);
        float dy= t * (b1 - a1);
        p->x = a0 + dx;
        p->y = a1 + dy;
    }
}

int main(){
    float l1ex;
    float l1ey;
    float l2ex;
    float l2ey;
    float l1sx;
    float l1sy;
    float l2sx;
    float l2sy;
    
    checker_make_symbolic(&(l1ex), sizeof(l1ex), "l1ex");
    checker_make_symbolic(&(l1ey), sizeof(l1ey), "l1ey");
    checker_make_symbolic(&(l1sx), sizeof(l1sx), "l1sx");
    checker_make_symbolic(&(l1sy), sizeof(l1sy), "l1sy");

    checker_make_symbolic(&(l2ex), sizeof(l2ex), "l2ex");
    checker_make_symbolic(&(l2ey), sizeof(l2ey), "l2ey");
    checker_make_symbolic(&(l2sx), sizeof(l2sx), "l2sx");
    checker_make_symbolic(&(l2sy), sizeof(l2sy), "l2sy");
    OLine l2;
    OLine l1; 
    l1.E.x = l1ex;
    l1.E.y = l1ey;
    l1.S.x = l1sx;
    l1.S.y = l1sy;

    l2.E.x = l2ex;
    l2.E.y = l2ey;
    l2.S.x = l2sx;
    l2.S.y = l2sy;
  
    OPoint p;
    line_insect_opt(&p, &l1, &l2);
    checker_check_float(p.x);

    return 0;
}