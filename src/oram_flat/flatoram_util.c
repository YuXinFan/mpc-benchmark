#include "flatoram_util.h"

#include <omp.h>

#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>

#include <wmmintrin.h>
#include <tmmintrin.h>


// gcc -c -O3 -maes -I/usr/include -I . -I ../../src/ -std=c99 -fopenmp flatoram_util.c -o flatoram_util.o -I ../ext/oblivc

static int sslinits = 0;
static void* sslzero;
static omp_lock_t * ssllocks;

void get_random_bytes(void *buf, size_t bytes) {
	//only supported on recend linuxes, unfortunately.
	//getrandom(buf, bytes, 0);

	FILE *fp;
	fp = fopen("/dev/urandom", "r");
	fread(buf, 1, bytes, fp);
	fclose(fp);
}


// Locking callback
void openmp_locking_callback(int mode, int type, char *file, int line) {
	if (mode & CRYPTO_LOCK) {
		omp_set_lock(&ssllocks[type]);
	} else {
		omp_unset_lock(&ssllocks[type]);
	}
}

// Thread ID callback
unsigned long openmp_thread_id(void) {
	return (unsigned long)omp_get_thread_num();
}

void openmp_thread_setup(void) {
	ssllocks = OPENSSL_malloc(CRYPTO_num_locks() * sizeof(omp_lock_t));
	for (int ii=0; ii<CRYPTO_num_locks(); ii++) omp_init_lock(&ssllocks[ii]);
	CRYPTO_set_id_callback((unsigned long (*)())openmp_thread_id);
	CRYPTO_set_locking_callback((void (*)())openmp_locking_callback);
}

void openmp_thread_cleanup(void) {
	CRYPTO_set_id_callback(NULL);
	CRYPTO_set_locking_callback(NULL);
	for (int ii=0; ii<CRYPTO_num_locks(); ii++) omp_destroy_lock(&ssllocks[ii]);
	OPENSSL_free(ssllocks);
}



void offline_expand_init() {
	if (sslinits == 0) {
		openmp_thread_setup();
		ERR_load_crypto_strings();
		OpenSSL_add_all_algorithms();
		OPENSSL_config(NULL);
		sslzero = calloc(1, 16);
	}
	sslinits++;
}

void offline_expand_deinit() {
	if (sslinits == 1) {
		ENGINE_cleanup(); 
		CONF_modules_unload(1);
		EVP_cleanup();
		CRYPTO_cleanup_all_ex_data();
		ERR_remove_state(0);
		ERR_free_strings();
		free(sslzero);
		sslzero = NULL;
		openmp_thread_cleanup();
	}
	sslinits--;
}

#define KE(NK,OK,RND) NK = OK;	\
    NK = _mm_xor_si128(NK, _mm_slli_si128(NK, 4));	\
    NK = _mm_xor_si128(NK, _mm_slli_si128(NK, 4));	\
    NK = _mm_xor_si128(NK, _mm_slli_si128(NK, 4));	\
	OK = _mm_xor_si128(NK, _mm_shuffle_epi32(_mm_aeskeygenassist_si128(OK, RND), 0xff)); \


void offline_expand_2(uint8_t * dest, uint8_t * src) {
	// EVP_CIPHER_CTX *ctx;
	// ctx = EVP_CIPHER_CTX_new();
	// EVP_EncryptInit_ex(ctx, EVP_aes_128_ctr(), NULL, src, sslzero);
	// EVP_CIPHER_CTX_set_padding(ctx, 0);
	// int len;
	// for (size_t ii = 0; ii < n; ii++) {
	// 	EVP_EncryptUpdate(ctx, &dest[BLOCKSIZE*ii], &len, sslzero, BLOCKSIZE);
	// }
	// EVP_CIPHER_CTX_free(ctx);
	EVP_CIPHER_CTX *ctx;
	ctx = EVP_CIPHER_CTX_new();
	EVP_EncryptInit_ex(ctx, EVP_aes_128_ctr(), NULL, src, sslzero);
	EVP_CIPHER_CTX_set_padding(ctx, 0);
	int len;
	for (size_t ii = 0; ii < n; ii++) {
		EVP_EncryptUpdate(ctx, &dest[BLOCKSIZE*ii], &len, sslzero, BLOCKSIZE);
	}
	EVP_CIPHER_CTX_free(ctx);	
}

void offline_expand(uint8_t * dest, uint8_t * src, size_t n) {

    __m128i seed;
    seed = _mm_load_si128((__m128i *) src);

	__m128i nk; // next key
	__m128i ml,mr, ok;
	ok = seed;

    ml = _mm_xor_si128(ml, ml); 				// msg = 0
    mr = _mm_set_epi64((__m64)0l,(__m64)1l);	// msg = 1

    // round 0
    ml = _mm_xor_si128(ml, ok);
    mr = _mm_xor_si128(mr, ok);

	// key expand 1 KEYEXP128(rk[0], 0x01);
	KE(nk, ok, 0x01)
    ml = _mm_aesenc_si128(ml, ok);
    mr = _mm_aesenc_si128(mr, ok);

	KE(nk, ok, 0x02)
    ml = _mm_aesenc_si128(ml, ok);
    mr = _mm_aesenc_si128(mr, ok);

	KE(nk, ok, 0x04)
    ml = _mm_aesenc_si128(ml, ok);
    mr = _mm_aesenc_si128(mr, ok);

	KE(nk, ok, 0x08)
    ml = _mm_aesenc_si128(ml, ok);
    mr = _mm_aesenc_si128(mr, ok);

	KE(nk, ok, 0x10)
    ml = _mm_aesenc_si128(ml, ok);
    mr = _mm_aesenc_si128(mr, ok);

	KE(nk, ok, 0x20)
    ml = _mm_aesenc_si128(ml, ok);
    mr = _mm_aesenc_si128(mr, ok);

	KE(nk, ok, 0x40)
    ml = _mm_aesenc_si128(ml, ok);
    mr = _mm_aesenc_si128(mr, ok);

	KE(nk, ok, 0x80)
    ml = _mm_aesenc_si128(ml, ok);
    mr = _mm_aesenc_si128(mr, ok);

	KE(nk, ok, 0x1b)
    ml = _mm_aesenc_si128(ml, ok);
    mr = _mm_aesenc_si128(mr, ok);

	KE(nk, ok, 0x36)
    ml = _mm_aesenclast_si128(ml, ok);
    mr = _mm_aesenclast_si128(mr, ok);

    _mm_storeu_si128((__m128i*) dest, ml);
    uint8_t* pp = (dest+16);
    _mm_storeu_si128((__m128i*) pp, mr);

}


void offline_expand(uint8_t * dest, uint8_t * src, size_t n) {
#define KE2(NK,OK,RND) NK = OK;	\
    NK = _mm_xor_si128(NK, _mm_slli_si128(NK, 4));	\
    NK = _mm_xor_si128(NK, _mm_slli_si128(NK, 4));	\
    NK = _mm_xor_si128(NK, _mm_slli_si128(NK, 4));	\
	NK = _mm_xor_si128(NK, _mm_shuffle_epi32(_mm_aeskeygenassist_si128(OK, RND), 0xff)); \


    // this version handles the case when n!=2 using a loop

    __m128i seed;
    seed = _mm_load_si128((__m128i *) src);

	__m128i r1,r2,r3,r4,r5,r6,r7,r8,r9,r10; // next key
	__m128i mr, ok;
	ok = seed;

	KE2(r1, ok, 0x01)
	KE2(r2, r1, 0x02)
	KE2(r3, r2, 0x04)
	KE2(r4, r3, 0x08)
	KE2(r5, r4, 0x10)
	KE2(r6, r5, 0x20)
	KE2(r7, r6, 0x40)
	KE2(r8, r7, 0x80)
	KE2(r9, r8, 0x1b)
	KE2(r10, r9, 0x36)

	__m128i mask = _mm_set_epi64((__m64)0x08090a0b0c0d0e0fULL, (__m64)0x0001020304050607ULL );

	for(size_t li=0; li<n; li++) {
	    mr = _mm_set_epi64((__m64)li,(__m64)0l);	// msg = li
		mr = _mm_shuffle_epi8 (mr, mask);

	    mr = _mm_xor_si128(mr, ok);					// round 0

	    mr = _mm_aesenc_si128(mr, r1);
	    mr = _mm_aesenc_si128(mr, r2);
	    mr = _mm_aesenc_si128(mr, r3);
	    mr = _mm_aesenc_si128(mr, r4);
	    mr = _mm_aesenc_si128(mr, r5);
	    mr = _mm_aesenc_si128(mr, r6);
	    mr = _mm_aesenc_si128(mr, r7);
	    mr = _mm_aesenc_si128(mr, r8);
	    mr = _mm_aesenc_si128(mr, r9);
	    mr = _mm_aesenclast_si128(mr, r10);
	    uint8_t* pp = dest+(li*16);
	    _mm_storeu_si128((__m128i*) pp, mr);

	}



}

