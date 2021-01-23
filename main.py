from sympy import *
import Functions
from SearchAmongPermutations import *


def execute_and_print_result(n_r, n_t):
    text_file = open("searchAmongPermutations_output.txt", "a")
    min_rank, min_p = execute_search_among_permutations(n_t, n_r)
    text_file.write(" ===================================================================== \n")
    n = n_t * n_r
    text_file.write("Run for Nt = " + str(n_t) + ", Nr = " + str(n_r) + "\n")
    total_number_of_iterations = calc_number_of_iters(n_t, n_r)
    text_file.write("Number of Iterations: " + str(total_number_of_iterations) + "\n")
    text_file.write("p is: " + str(min_p) + "\n")
    text_file.write("Minimum rank is: " + str(min_rank) + "\n")
    text_file.write("Hence minimum rate is: " + str(Fraction(min_p, min_rank)) + '\n')
    text_file.close()


execute_and_print_result(2, 2)
# execute_and_print_result(3, 2)
# execute_and_print_result(2, 3)
# execute_and_print_result(4, 2)
# execute_and_print_result(2, 4)
# execute_and_print_result(3, 3)
# execute_and_print_result(6, 3)