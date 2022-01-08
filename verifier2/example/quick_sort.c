#include "../src/checker.h"

void swap(int8_t *a, int8_t *b){
  int8_t t = *a;
  *a = *b;
  *b = t;
}

int8_t partition(int8_t * data, int8_t * output, int8_t n){
  int8_t i = 0;
  int8_t *pi = data + n - 1;
  bool oleq = true;
  for (int8_t j = 0; j < n-1; j++){
    oleq = *(data+j) <= *pi;
    bool leq;
    revealOblivBool(&leq, oleq, 0);
    if (oleq) {
      bool oneq = i!=j;
      bool neq;
      revealOblivBool(&neq, oneq, 1);
      if ( neq ) {
        swap(data+i, data+j);
        swap(output+i, output+j);
      }
      i = i + 1;
    }
  }
  bool oneq = i != n-1;
  bool neq;
  revealOblivBool(&neq, oneq, 2);
  if ( neq ) {
    swap(data+i, pi);
    swap(output+i, output + n - 1);
  }

  return i;
}

void oqsort_main(int8_t * data, int8_t * output, int8_t len){
  if (1 < len) {
    // p is the index of pivot
    int8_t p = partition(data, output, len);
    //int8_t p = 1;
    // sort first p value
    oqsort_main(data, output, p);
    // sort last n-p-1 value
    oqsort_main(data+p+1, output+p+1, len-p-1);
  }
}

void oqsort(int8_t * data, size_t end){
  //fprint8_tf(stdout, "entry\n");
  int8_t * temp = malloc(end * sizeof(int8_t));
  for (int i = 0; i < end; i++){
    temp[i] = data[i];
    data[i] = i;
  }
  //fprint8_tf(stdout, "temp malloc\n");
  oqsort_main(temp, data, end);
  //fprint8_tf(stdout, "qsort main \n");

  free(temp);
}


int main(){
    int size = 6;
    int8_t arr[size];
    checker_init(3);
    checker_make_symbolic(arr, sizeof(arr), "arr");
    oqsort(arr, size);
    checker_check_int8_array(arr, size);
    return 0;
}