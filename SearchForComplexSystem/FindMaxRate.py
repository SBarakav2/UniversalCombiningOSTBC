from Tools import *
import math
import itertools
from sympy.utilities.iterables import multiset_permutations
import numpy as np
from helper_functions import *


def generate_pattern(size):
    """The functions gives a generator to pattern. The pattern is a list  of size
    'size' with '0' or '1's which means to do/not a certain operation (for example conjugate).
    The generator won't yield two identical patterns up to 'not'
    for example: 000111 and 111000 are identical up to 'not'."""
    for counter in range(2 ** (size - 1)):
        yield [int(x) for x in '{:0{}b}'.format(counter, size)]


def generate_channel_vec(rec_num, trans_num, reals_only=False):
    # generate basic list of vectors for each receiver
    basic_list = []
    for rec_ind in range(rec_num):
        block_string = ''
        for trans_ind in range(trans_num):
            block_string += f'h_{{%d-%d}}' % (trans_ind, rec_ind)
            if trans_ind < trans_num - 1:
                block_string += "  &  "
        basic_list.append(Block(block_string))

    g_conj = generate_pattern(rec_num)
    if reals_only:  # if only reals, conjugates won't be checked
        g_conj = ([0] * rec_num for _ in range(1))
    for conj_pattern in g_conj:
        # for each conjugate pattern generate the basic_conj_list
        basic_conj_list = deepcopy(basic_list)
        # go over all receiver and do conjugate accordingly
        for rec_ind in range(rec_num):
            if conj_pattern[rec_ind] == 1:
                for trans_ind in range(trans_num):
                    basic_conj_list[rec_ind][0][trans_ind].conjugate = '*'
        # for each receiver generate all possibilities for minuses among each transmitter
        minus_generator = generate_pattern(trans_num)
        for item in itertools.combinations_with_replacement(minus_generator, rec_num):
            # create a basic_minus_list
            basic_minus_list = deepcopy(basic_conj_list)
            # operate the minus operation
            for rec_ind in range(rec_num):
                for trans_ind in range(trans_num):
                    if item[rec_ind][trans_ind] == 1:
                        basic_minus_list[rec_ind][0][trans_ind].sign = '-'
            # concatenate to long channel coefficients vector
            basic_h = np.concatenate(basic_minus_list, axis=1)
            for h in multiset_permutations(basic_h[0]):
                yield np.vstack((h, )).view(Block)


def find_max_rate(stbc, trans_num, rec_num, reals_only=False, jump_iters=1):
    """ Finds the vector of channel coefficients that is quivalent to a MIMO system with the 'stbc'
    transmission and of size 'trans_num' x 'rec_num' which is equivalent to a combining system with minimum
    channel uses.
    'real_only' parameter allows to iterate over real channel coefficients (i,e '-' or '+')
    'jump_iters' allows to jump over iters in order to reduce search time on expanse of probably missing options"""
    if stbc.shape[1] != trans_num * rec_num:
        raise ValueError('Shape of stbc is not compatible with tottal number of channel coefficients')
    g_ch_vec = generate_channel_vec(rec_num, trans_num, reals_only)
    total_iterations = (2 ** (rec_num-1)) * ((2 ** (trans_num-1)) ** rec_num ) * math.factorial(rec_num*trans_num)
    if reals_only:
        total_iterations = ((2 ** (trans_num - 1)) ** rec_num) * math.factorial(rec_num * trans_num)
    print('Total iterations: ' + str(total_iterations))
    max_vec = []
    min_times = stbc.shape[1] * stbc.shape[0]
    for vec_ind, channel_coeff in enumerate(g_ch_vec):
        if vec_ind % jump_iters == 0:  # don't check every iter, but only 'jump_iters' multiples
            transmission_matrix, x = find_combining_system(stbc, channel_coeff)
            times_needed = transmission_matrix.shape[0]
            # update optimum
            if times_needed < min_times:
                min_times = times_needed
                max_vec = channel_coeff
            # print iteration
            if vec_ind % 1 == 0:
                print('iter:' + str(vec_ind) + ',current times:' + str(times_needed) + ', min times: ' + str(min_times))
    return max_vec, min_times
