#include <math.h>

int triangle(int i) {
  /*
   * Compute the triangle of an integer.
   *
   * :arg i: the integer
   * :return: the corresponding triangular number
   */
  int j, t = 0;

  for (j = 1; j < i+1; j++) t += j;
  return t;
}

int factorial(int i) {
  /*
   * Compute the factorial of an integer.
   *
   * :arg i: the integer
   * :return: the corresponding factorial
   */
   int j, f = 1;

   for (j = 1; j < i+1; j++) f *= j;
   return f;
}

long factorial8(int i) {
  /*
   * Compute the factorial of an integer as an 8-byte integer.
   *
   * :arg i: the integer
   * :return: the corresponding factorial
   */
   int j;
   long f = 1;

   for (j = 1; j < i+1; j++) f *= j;
   return f;
}

void bubble_sort(int *array, int l) {
  /*
   * Apply the bubble sort algorithm to an array of integers.
   *
   * :arg array: the array of integers, which gets modified in-place
   * :arg l: the length of the array
   */
  int i, j, tmp;

  for (i = l-2; i >= 0; i--) {
    for (j = 0; j < i; j++) {
      if (array[j+1] < array[j]) {
        tmp = array[j+1];
        array[j+1] = array[j];
        array[j] = tmp;
      }
    }
  }
}

void bubble_sort8(long *array, int l) {
  /*
   * Apply the bubble sort algorithm to an array of 8-byte integers.
   *
   * :arg array: the array of 8-byte integers, which gets modified in-place
   * :arg l: the length of the array
   */
  int i, j;
  long tmp;

  for (i = l-2; i >= 0; i--) {
    for (j = 0; j < i; j++) {
      if (array[j+1] < array[j]) {
        tmp = array[j+1];
        array[j+1] = array[j];
        array[j] = tmp;
      }
    }
  }
}
