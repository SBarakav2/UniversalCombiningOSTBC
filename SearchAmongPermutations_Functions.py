import itertools
from itertools import permutations
import numpy as np
from sympy import *
from scipy.special import comb
import math


def calc_number_of_iters(n_t, n_r):
    """Calculates mathematically the number of iterations of the generator 'generate_all_matrix_options"""
    calc_result = 1;
    for row_ind in range(n_r - 1):
        calc_result = calc_result * comb(n_t * (n_r - row_ind), n_t, exact=True) * math.factorial(n_t) * (2 ** (n_t-1))
    return calc_result


def generate_block_matrix(mat_set, n_t, n_r):
    for mat_ind, sign_mat in generate_all_matrix_options(n_t, n_r):
        big_mat = Matrix([[mat_set[ind] * (sign_mat[row][col] * 2 - 1) for col, ind in enumerate(indices)]
                          for row, indices in enumerate(mat_ind)])
        yield big_mat


def generate_all_matrix_options(n_t, n_r):
    """ generates all possible matrices out of the subset with one exception:
    the 'last_row' row contains the only option for values without checking their permutations.
    For each such matrix it also generates all possible sign patterns ('0' or '1') whereas the first column
    and the last row are fixed to '0'."""
    # run over options from first row to last
    for x, y in generate_from_row(0, list(range(n_t * n_r)), n_t, n_r - 1):
        yield x, y


def generate_from_row(row_num, subset, n_t, last_row):
    """ generates all possible matrices out of the subset, i.e. going through all over possible
    options for row number 'row_num' and all possible options for the rows below with one exception:
    the 'last_row' row contains the only option for values without checking their permutations.
    For each such matrix it also generates all possible sign patterns ('0' or '1') whereas the first column
    and the last row are fixed to '0'."""
    if row_num == last_row:
        yield [subset], [[0]*n_t]
    for in_, out_ in comb_and_comp(subset, n_t):
        # run over all possible permutations
        for permut in itertools.permutations(in_, n_t):
            for sign_pattern in generate_sign_pattern(n_t):
                g = generate_from_row(row_num + 1, out_, n_t, last_row)
                for sub_result, sub_pattern in g:
                    sub_result.insert(0, list(permut))
                    sub_pattern.insert(0, list(sign_pattern))
                    yield sub_result, sub_pattern


def generate_sign_pattern(size):
    """The functions gives a generator to pattern. The pattern is a list  of size
    'size' with '0' or '1's which means to do/not a certain operation (for example minus).
    The generator won't yield two identical patterns up to 'not'
    for example: 000111 and 111000 are identical up to 'not'."""
    for counter in range(2 ** (size - 1)):
        yield [int(x) for x in '{:0{}b}'.format(counter, size)]


def comb_and_comp(lst, n):
    """ This code was taken from 'Stack Overflow'
    The generator returns all possible sub-list of size 'n' and their complements as  a tuple of lists.
    i.e returns: (sub_list, complement)"""
    # no combinations
    if len(lst) < n:
        return
    # trivial 'empty' combination
    if n == 0 or lst == []:
        yield [], lst
    else:
        first, rest = lst[0], lst[1:]
        # combinations that contain the first element
        for in_, out in comb_and_comp(rest, n - 1):
            yield [first] + in_, out
        # combinations that do not contain the first element
        for in_, out in comb_and_comp(rest, n):
            yield in_, [first] + out
