// {gcc,clang} -O2 -Wall -o pi pi.c -lmpfi -lmfr -lm

// todo (kivulrol): h / (sqrt(1 + h * h / 4) + 1), ahol az oldalhossz a h, kezdetben haromszog eseten 2sqrt(3)

#include <stdio.h>
#include <stdlib.h>
#include <mpfi.h>
#include <mpfi_io.h>
#include <mpfr.h>
#include <math.h>

mpfi_t bx2;
mpfi_t ax;
mpfi_t xy2;

void felezo(mpfi_t *bc) {
  mpfi_div_ui(*bc, *bc, 2);
  mpfi_sqr(bx2, *bc);
  mpfi_si_sub(ax, 1, bx2); mpfi_sqrt(ax, ax);
  mpfi_si_sub(xy2, 1, ax); mpfi_sqr(xy2, xy2);
  mpfi_add(*bc, bx2, xy2);
  mpfi_sqrt(*bc, *bc);
}

mpfi_t becsprime, becscur;
mpfr_t becsdiff;
int remain = 100;
double accuracy;
int becsul(mpfi_t *bc, int i, int d) {
  mpfi_mul_ui(becscur, *bc, 6);
  mpfi_div_2si(becscur, becscur, -i);
  mpfi_diam_abs(becsdiff, becscur);
  mpfr_log10(becsdiff, becsdiff, MPFR_RNDD);

  mpfi_sub(becsprime, becscur, becsprime);
  mpfi_log10(becsprime, becsprime);
  remain = d + mpfi_get_d(becsprime);
  accuracy = -mpfr_get_d(becsdiff, MPFR_RNDD);
  if (accuracy < d + 1) {
    fprintf(stderr, "Early exit, because accuracy is already too low\n");
    exit(1);
  }

  printf("Iteration: %7d, remaining digits: %7d, current accuracy: %10.2f\n", i, remain, accuracy);
  fflush(stdout);

  mpfi_swap(becscur, becsprime);
  return mpfi_cmp_si(becscur, -d);
}

int dps(int d) {
  // stolen from mpmath, but fixed the ln(10)/ln(2) value
  return (int) round((d + 1) * 3.32192809488736234787);
}

int main(int argc, char **argv) {
  if (argc != 2) {
    fprintf(stderr, "Usage: %s <digits>\n", argv[0]);
    exit(1);
  }

  unsigned int d = atoi(argv[1]);
  mpfr_set_default_prec(dps(d+10));
  mpfi_inits(bx2, ax, xy2, becscur, becsprime, NULL);
  mpfr_init(becsdiff);
  mpfi_set_ui(becsprime, 0);

  mpfi_t bc;
  mpfi_init_set_ui(bc, 1);

  int i = 0;
  for (;;i++) {
    felezo(&bc);
    if ((remain > 1000 && (0 == i % 1000)) ||
        (remain <= 1000 && (0 == i % 100)) ||
         remain <= 100) {
      if (becsul(&bc, i, d) < 0) break;
    }
  }
  printf("\n\n\n");

  mpfi_t result;
  mpfi_init(result);
  mpfi_mul_ui(result, bc, 6);
  mpfi_div_2si(result, result, -i);

  mpfr_t left, right;
  char sleft[d+10], sright[d+10];
  mpfr_exp_t eleft, eright;

  mpfr_inits(left, right, NULL);
  mpfi_get_left(left, result);
  mpfi_get_right(right, result);
  mpfr_get_str(sleft, &eleft, 10, d+10, left, MPFR_RNDD);
  mpfr_get_str(sright, &eright, 10, d+10, right, MPFR_RNDU);

  sleft[d+1] = 0;
  sright[d+1] = 0;

  if (0 != strcmp(sleft, sright)) {
    fprintf(stderr, "Interval computation didn't result in precise output, not enough safety?\n");
    exit(1);
  }

  printf("         3.\n");
  for (int i = 0 ; i < d; i+=100) {
    char save = sleft[i+101];
    sleft[i+101] = 0;
    printf("%7d: %s\n", i+1, sleft+i+1);
    sleft[i+101] = save;
  }
  printf("\nIterations used: %d, safety margin left: %10.2f\n", i, accuracy - d);

  mpfr_clears(left, right, becsdiff, NULL);
  mpfi_clears(result, bc, bx2, ax, xy2, becscur, becsprime, NULL);

  return 0;
}
