#include "checker.h"

#define N  4

// A structure to represent a queue
typedef struct Queue {
    int front, rear, size;
    unsigned capacity;
    u_int8_t* array;
} Queue;
 
// function to create a queue
// of given capacity.
// It initializes size of queue as 0
void initQueue(Queue* queue, unsigned capacity, u_int8_t * x)
{
    queue->capacity = capacity;
    queue->front = queue->size = 0;
 
    // This is important, see the enqueue
    queue->rear = capacity - 1;
    queue->array = x;
}
 
Queue* createQueue(unsigned capacity)
{	
	Queue* queue = malloc(sizeof(Queue));
    queue->capacity = capacity;
    queue->front = queue->size = 0;
 
    // This is important, see the enqueue
    queue->rear = capacity - 1;
    queue->array = malloc(2*capacity*sizeof(u_int8_t));

	return queue;
}
 
 
// Queue is empty when size is 0
int oqueue_empty(struct Queue* queue)
{
    return (queue->size == 0);
}
 
// Function to add an item to the queue.
// It changes rear and size
void oqueue_push(struct Queue* queue, u_int8_t *item)
{
    queue->rear = (queue->rear + 1)
                  % queue->capacity;
    queue->array[queue->rear*2] = item[0];
    queue->array[queue->rear*2+1] = item[1];
    queue->size = queue->size + 1;
    //printf("%d enqueued to queue\n", item);
}
 
// Function to remove an item from queue.
// It changes front and size
void oqueue_pop(u_int8_t * item, struct Queue* queue)
{
    item[0] = queue->array[queue->front*2];
	item[1] = queue->array[queue->front*2+1];
    queue->front = (queue->front + 1)
                   % queue->capacity;
    queue->size = queue->size - 1;
}
 

void oram_read(u_int8_t * output, u_int8_t * o, int index, int len) {
	for (int i = 0; i < len; i++) {
		output[i] = o[index*len + i];
	}
	//ocCopy(o->cpy, output, element(o->cpy, o->data, index));
}
void oram_write(u_int8_t * o, u_int8_t * input, int index, int len) {
  for (int i = 0; i < len; i++) {
		o[index*len + i] = input[i] ;
	}
  //ocCopy(o->cpy, element(o->cpy, o->data, ii), input);
}
static void wStatusFunction(void * oramBlock, void * extBlock){
	if (((u_int8_t *) extBlock)[1] < ((u_int8_t *) oramBlock)[1] | ((u_int8_t *) oramBlock)[1] == 0xff) {
		u_int8_t temp = ((u_int8_t *) extBlock)[0];
		((u_int8_t *) extBlock)[0] = ((u_int8_t *) oramBlock)[0];
		((u_int8_t *) oramBlock)[0] = temp;

		temp = ((u_int8_t *) extBlock)[1];
		((u_int8_t *) extBlock)[1] = ((u_int8_t *) oramBlock)[1];
		((u_int8_t *) oramBlock)[1] = temp;

		temp = ((u_int8_t *) extBlock)[2];
		((u_int8_t *) extBlock)[2] = ((u_int8_t *) oramBlock)[2];
		((u_int8_t *) oramBlock)[2] = temp;
	} else {
		((u_int8_t *) extBlock)[1] = ((u_int8_t *) oramBlock)[1];
	}
}

void oram_apply(u_int8_t  * o, u_int8_t * input, int index) {
	wStatusFunction(o+index*3, input);
	//fn(o->cpy, element(o->cpy, o->data, index), input);
}
void oqueue_free(Queue* q) {
	free(q->array);
	q->array = NULL;
	free(q);
}

void oram_free(void *v){
	free(v);
}

u_int8_t* ogale_shapley_textbook_revealed(u_int8_t * output,  u_int8_t * mPrefsRaw, u_int8_t * wPrefsRaw, int n) {

	//u_int8_t *mPrefs = calloc(n*n, sizeof(u_int8_t));
	u_int8_t mPrefs[N*N];
	for (int i = 0; i < n*n; i++) {
		mPrefs[i] = mPrefsRaw[i];
	}
	//u_int8_t *wPrefs = malloc(n*n*sizeof(u_int8_t));
	u_int8_t wPrefs[N * N];

	//u_int8_t *mStatus = malloc(2*n*sizeof(u_int8_t));
	u_int8_t mStatus[2*N];
	//u_int8_t *wStatus = malloc(3*n*sizeof(u_int8_t));
	u_int8_t wStatus[3*N];


	//insert wprefs into oram
	for (int ii = 0; ii < n; ii++) {
		for (u_int8_t jj = 0; jj < n; jj++) {
			oram_write(wPrefs, &jj, ii*n + wPrefsRaw[ii * n + jj], 1); 
		}
	}

	Queue mQueue;
	u_int8_t queueArray[2*N];
	initQueue(&mQueue, n, queueArray);
	u_int8_t thisMQueue[2]; // [index, pref list pos]
	u_int8_t nextMQueue[2]; // [index, pref list pos]
	u_int8_t thisMStatus[2]; // [parter index, partner rating] 
	u_int8_t thisWStatus[3]; // [parter index, partner rating, partner's rating of self] 
	u_int8_t proposedW, thisWPrefs;
	
	// initialize mQueue and wStatus
	thisMQueue[1] = 0;
	thisWStatus[0] = 0xff;
	thisWStatus[1] = 0xff;
	thisWStatus[2] = 0;
	for (size_t ii = 0; ii < n; ii++) {
		thisMQueue[0] = ii;
		oqueue_push(&mQueue, thisMQueue);
		oram_write(wStatus, thisWStatus, ii, 3);
	}

    bool cond = false;
	for (size_t ii = 0; ii < n * n; ii++) {
		bool queue_empty = oqueue_empty(&mQueue);
		if (queue_empty == 0) {
			oqueue_pop(thisMQueue, &mQueue); // pop cuo wu
			oram_read(&proposedW, mPrefs, thisMQueue[0] * n + thisMQueue[1], 1);
			oram_read(&thisWPrefs, wPrefs, proposedW * n + thisMQueue[0], 1);

			// write new status for this w
			thisWStatus[0] = thisMQueue[0];
			thisWStatus[1] = thisWPrefs;
			thisWStatus[2] = thisMQueue[1];
			oram_apply(wStatus, thisWStatus, proposedW);
        }
        // thisW 当前的 matching 的rank 小于 
		cond = (thisWPrefs < thisWStatus[1]) | (thisWStatus[1] == 0xff);
        //revealOblivBool(&cond, ocond,0);
		bool condd;
		revealOblivBool(&condd, cond, 0);
		if (condd) {
            if (queue_empty==0) {
				// write new status for this m
				thisMStatus[0] = proposedW;
				thisMStatus[1] = thisMQueue[1];
				oram_write(mStatus, thisMStatus, thisMQueue[0], 2);

				// the old m is now sad and alone
				// fix bug
				if (thisWStatus[0] != 0xff) {
					nextMQueue[0] = thisWStatus[0];
					nextMQueue[1] = thisWStatus[2] + 1;
					oqueue_push(&mQueue, nextMQueue);
				}

			} 
		}else {
			if (queue_empty==0) {
				thisMQueue[1] += 1;
				oqueue_push(&mQueue, thisMQueue);
			}
		}
	}

	for (int ii = 0; ii < n; ii++) {
		oram_read(thisMStatus, mStatus, ii, 2);
		output[ii] = thisMStatus[0];
	}
	return output;
}

char **gen_labels(const char *prefix, int nums, int nums2){
    char **ptr = (char **)malloc(sizeof(char *)*nums*nums2);
    #pragma clang loop unroll(full)
    for (int i = 0; i < nums; i++){
	    for (int j = 0; j < nums2; j++){
			ptr[i*nums + j] = (char *)malloc(sizeof(char)*64);
			snprintf(ptr[i*nums+j], 36, "%s_%d_%d", prefix, i, j);
		}
    }
    return ptr;
}

int8_t checker_int8(const char *name){
	int8_t x;
	checker_make_symbolic(&x, sizeof(x), name);
	return x;
}

int main() {
	int pairs = N;
	u_int8_t mPrefs[pairs*pairs];
	char **mPrefs_l = gen_labels("mPrefs", pairs, pairs);
	u_int8_t wPrefs[pairs*pairs];
	char **wPrefs_l = gen_labels("wPrefs", pairs, pairs);
	u_int8_t output[pairs];
    #pragma clang loop unroll(full)
	for (int i = 0; i < pairs*pairs; i++) {
		mPrefs[i] = checker_int8(mPrefs_l[i]);
		checker_assume(mPrefs[i] >=0 && mPrefs[i] < pairs);
		wPrefs[i] = checker_int8(wPrefs_l[i]);
		checker_assume(wPrefs[i] >=0 && wPrefs[i] < pairs);
	}

    #pragma clang loop unroll(full)
	for (int ll = 0; ll < pairs; ll++) {
    	#pragma clang loop unroll(full)
		for (int kk = 0; kk < pairs; kk++) {
			#pragma clang loop unroll(full)
			for (int jj = kk+1; jj < pairs; jj++) {
				checker_assume( wPrefs[ll * pairs + kk] != wPrefs[ll * pairs + jj] );

				checker_assume( mPrefs[ll * pairs + kk] != mPrefs[ll * pairs + jj] );
			}
		}
	}
	printf("Assume Done.\n");
	ogale_shapley_textbook_revealed(output, mPrefs, wPrefs, pairs);
	checker_check_int8_array(output, pairs);
	return 0;
}
// int main() {
// 	int pairs = N;
// 	u_int8_t * perm = malloc(pairs * sizeof(u_int8_t));
// 	for (u_int8_t kk = 0; kk < pairs; kk++) {
// 		perm[kk] = kk;
// 	}
// 	u_int8_t * mPrefs = malloc(pairs * pairs * sizeof(u_int8_t));
// 	u_int8_t * wPrefs = malloc(pairs * pairs * sizeof(u_int8_t));
// 	u_int8_t * output = malloc(pairs * sizeof(u_int8_t));

// 	// int amPrefs[16] = {3, 1, 2, 0,
//     //     1, 0, 2, 3,
//     //     0, 1, 2, 3,
//     //     0, 1, 2, 3};
// 	// int awPrefs[16] = {0, 1, 2, 3,
//     //     0, 1, 2, 3,
//     //     0, 1, 2, 3,
//     //     0, 1, 2, 3};
// 	// for (int i = 0; i < 16; i++) {
// 	// 	mPrefs[i] = amPrefs[i];
// 	// 	wPrefs[i] = awPrefs[i];
// 	// }
// 	for ( int sample = 0; sample < 5 ; sample++) {
// 		for (int ll = 0; ll < pairs; ll++) {
// 			shuffle(perm, pairs);
// 			for (int jj = 0; jj < pairs; jj++) {
// 				mPrefs[ll * pairs + jj] = perm[jj];
// 			}
// 			for (int jj = 0; jj < pairs; jj++) {
// 				wPrefs[ll * pairs + jj] = perm[jj];
// 			}
// 		}
// 		print_array("mPrefs", mPrefs, pairs, pairs);
// 		print_array("wPrefs", wPrefs, pairs, pairs);

// 		ogale_shapley_textbook_revealed(output, mPrefs, wPrefs, pairs);
// 		for (int i = 0; i < pairs; i++) {
// 			printf("%d,", output[i]);
// 		}
// 		printf("\n");
// 	}
	
// 	free(perm);
// 	free(output);
// 	free(mPrefs);
// 	free(wPrefs);

// 	return 0;
// }