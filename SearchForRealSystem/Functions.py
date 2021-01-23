from sympy import *
from sympy.physics.quantum import TensorProduct


def check_orthonormal(m):
    col_num = m.shape[1]
    prod = transpose(m) * m
    return prod == eye(col_num)


def check_hurwitz_radon(mat_set):
    """The function gets a set of matrices and checks whether it meets the Hurwitz-Radon constraint"""
    for i, m in enumerate(mat_set):
        # check orthonormality
        if check_orthonormal(m) is False:
            return False
        # check anti-symmetry
        if transpose(m) != -m:
            return False
        # check connections
        for j in range(i+1, len(mat_set)):
            n = mat_set[j]
            if n*m != -m*n:
                return False
    return True


def find_hurwitz_radon_parameters(n):
    """ The functions gets as input a number 'n', and returns the parameters (a,b,c,d) that associated
    with the number. Those numbers are needed for Hurwitz-radon number computation."""
    for a in range(n):
        if n % (2 ** a) != 0:
            continue
        else:
            if (n // (2 ** a)) % 2 == 1:  # is odd
                b = n // (2 ** a)
                break
    c, d = a // 4, a % 4
    return a, b, c, d


def hurwitz_radon_number(n):
    """ The functions gets as input a number 'n' and returns its Hurwitz-Radon Number raw(n)"""
    a, b, c, d = find_hurwitz_radon_parameters(n)
    return 8 * c + 2 ** d


def build_hurwitz_radon_general(n):
    """ The function gets as input a number 'n' and returns a set of matrices of size n x n
    that meets the Hurwitz-Radon constraints. Here no assumption is made on 'b', where b is a Hurwitz-Radon parameter"""
    a, b, c, d = find_hurwitz_radon_parameters(n)
    mat_set = build_hurwitz_radon(n)
    if not mat_set:  #  if the list is empty
        return mat_set
    if b > 1:
        for ind, mat in enumerate(mat_set):
            mat_set[ind] = TensorProduct(mat, eye(b))
    return mat_set



def build_hurwitz_radon(n):
    """ The function gets as input a number 'n' and returns a set of matrices of size n x n
    that meets the Hurwitz-Radon constraints. The functions assumes that 'b=1', where b is a Hurwitz-Radon parameter."""
    if n == 0:
        return []
    a, b, c, d = find_hurwitz_radon_parameters(n)
    s = c - 1
    R = Matrix([[0, 1], [-1, 0]])
    P = Matrix([[0, 1], [1, 0]])
    Q = Matrix([[1, 0], [0, -1]])
    I = eye(2)
    mat_set = list()
    if a == 0:
        return mat_set
    if a == 1:
        mat_set.append(R)
        return mat_set
    if a == 2:
        mat_set = [TensorProduct(R, I), TensorProduct(P, R), TensorProduct(Q, R)]
        return mat_set
    if a == 3:
        mat_set = [TensorProduct(I, TensorProduct(R, I)),
                   TensorProduct(I, TensorProduct(P, R)),
                   TensorProduct(Q, TensorProduct(Q, R)),
                   TensorProduct(P, TensorProduct(Q, R)),
                   TensorProduct(R, TensorProduct(P, Q)),
                   TensorProduct(R, TensorProduct(P, P)),
                   TensorProduct(R, TensorProduct(Q, I))]
        return mat_set
    elif d == 0:
        mat_set.append(TensorProduct(R, eye(2 ** (4*s + 3))))
        set_A = build_hurwitz_radon(2 ** (4*s + 3))
        for A in set_A:
            mat_set.append(TensorProduct(Q, A))
        return mat_set
    else:  # if 1<= d < 4
        set_L = build_hurwitz_radon(2 ** (4*s + 3))
        set_A = build_hurwitz_radon(2 ** d)
        for A in set_A:
            mat_set.append(TensorProduct(P, TensorProduct(eye(2 ** (4*s + 3)), A)))
        for L in set_L:
            mat_set.append(TensorProduct(Q, TensorProduct(L, eye(2 ** d))))
        mat_set.append(TensorProduct(R, eye(2 ** (4*s+3) * 2 **d)))
        return mat_set


def find_minimum_p(n):
    """The function find for 'n' number of transmit antennas the minimum delay 'p'"""
    p = 1
    while True:
        if hurwitz_radon_number(p) >= n:
            return p
        p += 1


def build_ostbc(n):
    """The function builds a real OSTBC with minimum delay (Specific construction of Jafarkhani)"""
    p = find_minimum_p(n)
    mat_set = build_hurwitz_radon(p)
    mat_set.insert(0, eye(p))
    # Construct variables vector
    var_vector = zeros(p, 1)
    basic_sym_string = 'x_'
    result_matrix = zeros(p, n)
    for i in range(p):
        sym = Symbol(basic_sym_string + str(i + 1))
        var_vector[i, 0] = sym
    # Construct OSTBC
    for i in range(n):
        result_matrix[:, i] = mat_set[i] * var_vector
    return result_matrix
