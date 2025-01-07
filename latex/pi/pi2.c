// {gcc,clang} -O2 -Wall -o pi2 pi2.c -lmpfi -lmpfr -lm

// Ez a megoldas belulrol es kivulrol is kozelit sokszogekkel, igy
// amikor mar nem no a pontossag, akkor egyszeruen kitudja irni a
// valahany elso kozos szamjegyet es kesz.


#include <stdio.h>
#include <stdlib.h>
#include <mpfi.h>
#include <mpfi_io.h>
#include <mpfr.h>
#include <math.h>

// meaning of bc2 is bc^2, and bc24 is bc^2/4
mpfi_t bc24;
void felezo_belul(mpfi_t *bc2) {
  mpfi_div_2ui(bc24, *bc2, 2);
  mpfi_ui_sub(*bc2, 1, bc24);
  mpfi_sqrt(*bc2, *bc2);
  mpfi_ui_sub(*bc2, 1, *bc2);
  mpfi_sqr(*bc2, *bc2);
  mpfi_add(*bc2, *bc2, bc24);
}

// kbc' = kbc / (sqrt(1 + kbc * kbc / 4) + 1), ahol az oldalhossz a h, kezdetben haromszog eseten 2sqrt(3)
// es igy a hatszognel: 2sqrt(3)/3
// kbc24 meaning is kbc^2/4
mpfi_t kbc24;
void felezo_kivul(mpfi_t *kbc) {
  mpfi_div_2ui(kbc24, *kbc, 1);
  mpfi_sqr(kbc24, kbc24);
  mpfi_add_ui(kbc24, kbc24, 1);
  mpfi_sqrt(kbc24, kbc24);
  mpfi_add_ui(kbc24, kbc24, 1);
  mpfi_div(*kbc, *kbc, kbc24);
}

mpfi_t becsbelul, becskivul, merged;
mpfr_t bbl, bkr, becsdiff;
double becsul(mpfi_t *bc2, mpfi_t *kbc, int i) {
  mpfi_sqrt(becsbelul, *bc2);
  mpfi_mul_ui(becsbelul, becsbelul, 6);
  mpfi_div_2si(becsbelul, becsbelul, -i);

  mpfi_mul_ui(becskivul, *kbc, 6);
  mpfi_div_2si(becskivul, becskivul, -i);

  mpfi_get_left(bbl, becsbelul);
  mpfi_get_right(bkr, becskivul);
  mpfi_interv_fr(merged, bbl, bkr);

  mpfi_diam_abs(becsdiff, merged);
  mpfr_log10(becsdiff, becsdiff, MPFR_RNDD);

  return -mpfr_get_d(becsdiff, MPFR_RNDD);
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
  mpfr_set_default_prec(dps(d));
  mpfi_inits(becsbelul, becskivul, merged, bc24, kbc24, NULL);
  mpfr_inits(bbl, bkr, becsdiff, NULL);

  mpfi_t bc2;
  mpfi_init_set_ui(bc2, 1);

  mpfi_t kbc;
  mpfi_init_set_ui(kbc, 3);
  mpfi_sqrt(kbc, kbc);
  mpfi_mul_ui(kbc, kbc, 2);
  mpfi_div_ui(kbc, kbc, 3);

  int i = 0;
  double prev = 0, cur;
  for (;;i++) {
    felezo_belul(&bc2);
    felezo_kivul(&kbc);
    if ((d - prev > 1000 && 0 == i % 1000) ||
        (d - prev <= 1000 && 0 == i % 100) ||
        (d - prev <= 100)) {
      cur = becsul(&bc2, &kbc, i);
      printf("%10.2f / %10d   (%4.2f%%)\r", cur, d, cur * 100 / (double) d );
      fflush(stdout);
      if (prev >= cur) {
        break;
      }
      prev = cur;
    }
  }
  printf("\n\n\n");

  char sleft[d+10], sright[d+10];
  mpfr_exp_t eleft, eright;

  mpfr_get_str(sleft, &eleft, 10, d, bbl, MPFR_RNDD);
  mpfr_get_str(sright, &eright, 10, d, bkr, MPFR_RNDU);

  printf("         3.\n");
  int cont = 1;
  for (int i = 0 ; i < d && cont; i+=100) {
    char savel = sleft[i+101];
    char saver = sright[i+101];
    sleft [i+101] = 0;
    sright[i+101] = 0;
    for (int j = 0; j < 100 && cont; j++) {
      if (sleft[i+j+1] == sright[i+j+1]) {
        if (j == 0) printf("%7d: ", i+1);
        putc(sleft[i+j+1], stdout);
      } else {
        cont = 0;
      }
    }
    printf("\n");
    sleft [i+101] = savel;
    sright[i+101] = saver;
  }

  printf("\nIterations used: %d\n", i);

  mpfi_clears(becsbelul, becskivul, merged, bc24, kbc24, NULL);
  mpfr_clears(bbl, bkr, becsdiff, NULL);

  return 0;
}
