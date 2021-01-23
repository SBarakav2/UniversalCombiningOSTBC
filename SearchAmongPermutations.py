from SearchAmongPermutations_Functions import *
from Functions import *
from fractions import Fraction


def execute_search_among_permutations(n_t, n_r):
    print(" ===================================================================== ")
    n = n_t * n_r
    print("Run for Nt = " + str(n_t) + ", Nr = " + str(n_r))
    total_number_of_iterations = calc_number_of_iters(n_t, n_r)
    print("Number of Iterations: " + str(total_number_of_iterations))
    min_p = find_minimum_p(n)
    hr_set = build_hurwitz_radon(min_p)
    mat_set = hr_set[0:n-1]
    mat_set.append(eye(min_p))
    # Start Searching
    iter = 0
    min_rank = n * min_p
    g = generate_block_matrix(mat_set, n_t, n_r)
    for x in g:
        rank = x.rank()
        min_rank = min(min_rank, rank)
        # prints
        iter = iter + 1
        if iter % 1 == 0 or rank != min_rank:
            print(str(iter) + " / " + str(total_number_of_iterations) + " : " + str(rank) +
                  ",  minimum is: " + str(min_rank))
    print("Minimum rank is: " + str(min_rank))
    print("Hence minimum rate is: " + str(Fraction(min_p, min_rank)))
    return min_rank, min_p
