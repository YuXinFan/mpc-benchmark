#include "staticutil.h"
void static_write_hard(int party, char *name, int arrSize, char *type, float val, int repeat){
   FILE *fptr;

   // use appropriate location if you are using MacOS or Linux
    if (party == 1) {
        fptr = fopen("./Party-1.csv","a");
    }else {
        fptr = fopen("./Party-0.csv", "a");
    }

   if(fptr == NULL)
   {
      printf("[static_write]:Open File Error!");   
      exit(1);             
   }
   fprintf(fptr,"%s,%d, %s, %.3f, %d\n",name, arrSize, type, val, repeat);

   fclose(fptr);
}

void static_write_simple(int party, char *name, int eleSize, int arrSize, char *type, float val, int repeat){
   FILE *fptr;

   // use appropriate location if you are using MacOS or Linux
    if (party == 1) {
        fptr = fopen("./Party-1.csv","a");
    }else {
        fptr = fopen("./Party-0.csv", "a");
    }

   if(fptr == NULL)
   {
      printf("[static_write]:Open File Error!");   
      exit(1);             
   }
   fprintf(fptr,"%s,%d/%d, %s, %.3f, %d\n",name, eleSize, arrSize, type, val, repeat);

   fclose(fptr);
}