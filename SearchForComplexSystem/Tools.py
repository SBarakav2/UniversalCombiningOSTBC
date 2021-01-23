from copy import copy, deepcopy
import numpy as np
import re
import pandas

BULLET = 0x2022
SUPERSCRIPT_STAR = 0x20F0
SUBSCRIPT_0 = 0x2080
SUBSCRIPT_MINUS = 0x208B


class Symbol:
    """ Symbol string format is: "<letter>_{<first index>(-<second index>)}"
    where the <letter> is actually any string without restrictions,
    <first index> and <second index> are numbers only, while <second index> is optional
    Another value the symbol string can get is '0' which represents the zero symbol."""
    def __init__(self, sym_string="h_{1-1}"):
        # handle zero case
        if sym_string == '0':
            self.letter, self.indices_list = '0', []
            return
        # handle other cases
        elif re.match(r"^.+_\{.+\}$", sym_string):  # for example "h_{1}" or "hl_{12}" but not "_{1}"
            split_string = sym_string.split('_')
            self.letter = split_string[0]
            index = split_string[1][1:-1]
        # incorrect format
        else:
            raise ValueError('Incorrect symbol format')
        if re.match(r"^[0-9]+(-[0-9]*)?$", index):  # for example "9" or "9-10", allows at most 2 indices
            self.indices_list = index.split('-')
        else:
            raise ValueError('Incorrect index format')

    def __repr__(self):
        # handle zero case
        if self.letter == '0':
            return '0 '
        # other cases
        print_string = self.letter
        for char in self.indices_list[0]:  # first index
            print_string += chr(SUBSCRIPT_0 + int(char))
        if len(self.indices_list) == 2:
            print_string += chr(SUBSCRIPT_MINUS)
            for char in self.indices_list[1]:  # second index
                print_string += chr(SUBSCRIPT_0 + int(char))
        return print_string

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def change_letter(self, new_letter):
        self.letter = new_letter


class Element:
    """ Element string format is: "(<sign>)<sym_string>(<conjugate>)"
    where <sign> is optional and may include '+' or '-' while if does not appear it means '+'
    <sym_string> is the string depicts the Symbols
    <conjugate> is optional and may be '*' only, if does not appear it means that there is no conjugate sign"""
    def __init__(self, elem_string="-h_{1-1}*"):
        m = re.match(r"^(?P<sign>[-+]?)(?P<sym_string>.*?)(?P<conjugate>\*?)$", elem_string)
        if not m:
            raise ValueError('incorrect element string format')
        self.sign = '+' if m.groupdict()['sign'] == '' else m.groupdict()['sign']
        self.symbol = Symbol(m.groupdict()['sym_string'])
        self.conjugate = m.groupdict()['conjugate']
        # handle zero
        if self.symbol.letter == '0':
            self.sign, self.conjugate = '+', ''

    def __repr__(self):
        sign_str = '-' if self.sign == '-' else ' '
        conj_str = chr(SUPERSCRIPT_STAR) if self.conjugate == '*' else ' '
        return sign_str + str(self.symbol) + conj_str

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __mul__(self, other):
        phrase1 = Phrase(deepcopy(self), deepcopy(other))
        return phrase1

    def negate(self):
        res = deepcopy(self)
        # handle zero
        if res.symbol.letter == '0':
            return res
        # other cases
        else:
            res.sign = '-' if self.sign == '+' else '+'
            return res

    def compare_without_sign(self, other):
        return self.conjugate == other.conjugate and self.symbol == other.symbol


class Phrase:
    """A Phrase can be initiated by 2 one dimensional Blocks or by 2 Elements.
    it represents a sum of products of several Elements,
    when initialized with Blocks, the sum is inner product of the two Blocks"""
    def __init__(self, block1, block2):
        if not (isinstance(block1, Block) and isinstance(block2, Block) or
                isinstance(block1, Element) and isinstance(block2, Element)):
            raise TypeError('block1 and block2 must be of type Block')
        if isinstance(block1, Element):  # build blocks out of single elements
            self.block1, self.block2 = Block("x_{1}"), Block("x_{2}")
            self.block1[0, 0], self.block2[0, 0] = block1, block2
        else:
            self.block1 = block1
            self.block2 = block2
        if len(self.block1[0]) != len(self.block2[0]) or len(self.block1) > 1 or len(self.block2) > 1:
            raise ValueError('block1 and block2 must be 1 dimensional vector with the same size')
        # fix sign
        for i in range(len(self.block1[0])):
            elem1, elem2 = self.block1[0, i], self.block2[0, i]
            elem1.sign = '+' if elem1.sign == elem2.sign else '-'
            elem2.sign = '+'

    def __repr__(self):
        result_str = ''
        for i in range(len(self.block1[0])):
            elem1, elem2 = self.block1[0, i], self.block2[0, i]
            result_str += elem1.sign  # otherwise the '+' won't be printed
            unsigned_elem1 = copy(elem1)
            unsigned_elem1.sign = '+'
            result_str += "  " + str(unsigned_elem1) + " " + chr(BULLET) + " " + str(elem2) + "   "
        return result_str

    def __add__(self, other):
        if not isinstance(other, Phrase):
            raise TypeError('other must be of type Phrase')
        block1 = np.concatenate((self.block1, other.block1), axis=1).view(Block)
        block2 = np.concatenate((self.block2, other.block2), axis=1).view(Block)
        return Phrase(block1, block2)

    def __len__(self):
        return len(self.block1[0])

    def __eq__(self, other):
        """ Equality occures when the two phrases represents the same mathematical phrase while allowing
        associativity"""
        if len(self.block1[0]) != len(other.block1[0]):
            return False
        # Check for single product
        if len(self.block1[0]) == 1:
            self_elem1, self_elem2 = self.block1[0, 0], self.block2[0, 0]
            other_elem1, other_elem2 = other.block1[0, 0], other.block2[0, 0]
            # if self is zero the other must be zero too
            if self_elem1.symbol.letter == '0' or self_elem2.symbol.letter == '0':
                if other_elem1.symbol.letter == '0' or other_elem2.symbol.letter =='0':
                    return True
                else:
                    return False
            if self_elem1.sign != other_elem1.sign:  # sign appears only in first element
                return False
            # check elements
            if self_elem1.compare_without_sign(other_elem1) and self_elem2.compare_without_sign(other_elem2):
                return True
            elif self_elem1.compare_without_sign(other_elem2) and self_elem2.compare_without_sign(other_elem1):
                return True
            else:
                return False
        # Check for multiple products
        else:
            found_list = [False] * len(self)
            for self_ind in range(len(self)):
                prod_self = Phrase(self.block1[0, self_ind], self.block2[0, self_ind])
                # find the element in 'other'
                elem_exists = False
                for other_ind in range(len(other)):
                    prod_other = Phrase(other.block1[0, other_ind], other.block2[0, other_ind])
                    if prod_self == prod_other:
                        found_list[other_ind], elem_exists = True, True
                        break
                if not elem_exists:
                    return False
            # Check the found_list
            return all(found_list)

    def conjugate(self):
        new_phrase = deepcopy(self)
        for x, y in zip(new_phrase.block1[0], new_phrase.block2[0]):
            x_conj, y_conj = x.conjugate, y.conjugate
            if x.symbol.letter != '0':
                x.conjugate = '*' if x_conj == '' else ''
            if y.symbol.letter != '0':
                y.conjugate = '*' if y_conj == '' else ''
        return new_phrase

    def minus(self):
        new_phrase = deepcopy(self)
        for x in new_phrase.block1[0]:
            if x.symbol.letter != '0':
                x_sign = x.sign
                x.sign = '+' if x_sign == '-' else '-'
        return new_phrase

    def is_only_zeros(self):
        for x, y in zip(self.block1[0], self.block2[0]):
            if x.symbol.letter != '0' and y.symbol.letter != '0':
                return False
        return True


class Block(np.ndarray):
    """ According to the block format, rows are separated by '//' and elements by '&'.
    """

    def __new__(cls, block_string="x_{1} & x_{2} // -x_{2}* & x_{1}*"):
        block_string = re.sub(r"[\n\t\s]*", "", block_string)
        rows = block_string.split('//')
        elem_strings = [row.split('&') for row in rows]
        if not all(len(i) == len(elem_strings[0]) for i in elem_strings):
            raise ValueError('Incorrect block string format: each row must be with the same size')
        rows_count, cols_count = len(rows), len(elem_strings[0])
        obj = super(Block, cls).__new__(cls, (rows_count, cols_count), Element)
        for rowInd in range(rows_count):
            for colInd in range(cols_count):
                obj[rowInd, colInd] = Element(elem_strings[rowInd][colInd])
        return obj

    def __str__(self):
        return pandas.DataFrame(self.view(np.ndarray)).to_string()
