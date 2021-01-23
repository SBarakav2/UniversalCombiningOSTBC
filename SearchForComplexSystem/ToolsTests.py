from Tools import *
# from Block import *
# from Element import *
# from Symbol import *
import unittest


class PhraseTest(unittest.TestCase):

    def test_check_str(self):
        block1 = Block(block_string="x_{1} & -x_{2} & x_{3}*")
        block2 = Block(block_string="h_{2}* & h_{3} & -h_{1}*")
        phrase1 = Phrase(block1, block2)
        expected_string = '+   x₁  •  h₂⃰   -   x₂  •  h₃    -   x₃⃰ •  h₁⃰   '
        self.assertEqual(str(phrase1), expected_string)

    def test_init_with_elements(self):
        elem1 = Element(elem_string="-x_{1}*")
        elem2 = Element(elem_string="x_{2}")
        phrase1 = Phrase(elem1, elem2)
        expected_string = '-   x₁⃰ •  x₂    '
        self.assertEqual(str(phrase1), expected_string)

    def test_add(self):
        block1 = Block(block_string="x_{1} & -x_{2} & x_{3}*")
        block2 = Block(block_string="h_{2}* & h_{3} & -h_{1}*")
        phrase1 = Phrase(block1, block2)

        block1 = Block(block_string="x_{2} & -x_{3} & x_{4}*")
        block2 = Block(block_string="h_{5}* & h_{6} & -h_{7}*")
        phrase2 = Phrase(block1, block2)

        expected_string = "+   x₁  •  h₂⃰   -   x₂  •  h₃    -   x₃⃰ •  h₁⃰   +"\
                          "   x₂  •  h₅⃰   -   x₃  •  h₆    -   x₄⃰ •  h₇⃰   "
        self.assertEqual(str(phrase1 + phrase2), expected_string)

    def test_eq(self):
        # equal phrases
        phrase1 = Phrase(Block("x_{3}* & -x_{1} & h_{4}"), Block("-h_{3}* & -h_{2}* & x_{4}"))
        phrase2 = Phrase(Block("h_{2}* & -x_{3}* & x_{4}"), Block("x_{1} & h_{3}* & h_{4}"))
        self.assertTrue(phrase1 == phrase2)
        # equal phrases with zeros
        phrase1 = Phrase(Block("x_{3}* & 0 & h_{4}"), Block("-h_{3}* & -h_{2}* & x_{4}"))
        phrase2 = Phrase(Block("h_{2}* & -0* & x_{4}"), Block("x_{1} & h_{3}* & h_{4}"))
        # not same size
        phrase1 = Phrase(Block("x_{3}* & -x_{1} & h_{4}"), Block("-h_{3}* & -h_{2}* & x_{4}"))
        phrase2 = Phrase(Block("h_{2}* & -x_{3}*"), Block("x_{1} & h_{3}*"))
        self.assertFalse(phrase1 == phrase2)
        # wrong sign
        phrase1 = Phrase(Block("-x_{3}* & -x_{1} & h_{4}"), Block("-h_{3}* & -h_{2}* & x_{4}"))
        phrase2 = Phrase(Block("h_{2}* & -x_{3}* & x_{4}"), Block("x_{1} & h_{3}* & h_{4}"))
        self.assertFalse(phrase1 == phrase2)

    def test_conjugate(self):
        phrase = Phrase(Element('-x_{3}'), Element('h_{2-1}*'))
        phrase_conj = Phrase(Element('-x_{3}*'), Element('h_{2-1}'))
        self.assertEqual(phrase.conjugate(), phrase_conj)

        phrase = Phrase(Element('-x_{3}*'), Element('h_{2-1}*'))
        phrase_conj = Phrase(Element('-x_{3}'), Element('h_{2-1}'))
        self.assertEqual(phrase.conjugate(), phrase_conj)
        # with zeros
        phrase = Phrase(Element('-x_{3}*'), Element('0'))
        phrase_conj = Phrase(Element('-x_{3}'), Element('0'))
        self.assertEqual(phrase.conjugate(), phrase_conj)


class BlockTest(unittest.TestCase):

    # HappyFlow
    def test_check_random_elements(self):
        block1 = Block(block_string="x_{1} & -x_{2} & x_{3}* // x_{2}* & x_{3} & -x_{1}*")
        self.assertEqual(block1[0, 0], Element("x_{1}"))

    def test_mul_blocks(self):
        block1 = Block(block_string="x_{1} & -x_{2} & x_{3}* // " + "x_{2}* & x_{3}* & -x_{1}")
        chan_coeff = Block("h_{1-1} // h_{1-2} // h_{1-3}")
        expected_string = "                                                           0\n"\
                          "0  +   x₁  •  h₁₋₁    -   x₂  •  h₁₋₂    +   x₃⃰ •  h₁₋₃    \n"\
                          "1  +   x₂⃰ •  h₁₋₁    +   x₃⃰ •  h₁₋₂    -   x₁  •  h₁₋₃    "
        self.assertEqual(str(np.matmul(block1, chan_coeff)), expected_string)


class ElementTest(unittest.TestCase):

    # HappyFlow
    def test_mul(self):
        elem1 = Element("-x_{2}*")
        elem2 = Element("-h_{1}")
        expected_string = '+   x₂⃰ •  h₁    '
        self.assertEqual(str(elem1 * elem2), expected_string)

    def test_plus_conj(self):
        string = str(Element('+h_{1-2}*'))
        self.assertEqual(string, ' h₁₋₂⃰')

    def test_minus_no_conj(self):
        string = str(Element('-h_{1-2}'))
        self.assertEqual(string, '-h₁₋₂ ')

    def test_compare_without_sign(self):
        elem1 = Element("-x_{2}*")
        elem2 = Element("x_{2}*")
        elem3 = Element("x_{2}")
        elem4 = Element("-h_{2}*")
        self.assertTrue(elem1.compare_without_sign(elem2))
        self.assertFalse(elem1.compare_without_sign(elem3))
        self.assertFalse(elem1.compare_without_sign(elem4))

    def test_zero_equality(self):
        elem1 = Element("-0*")
        elem2 = Element("0")
        self.assertTrue(elem1, elem2)
        self.assertTrue(elem1.negate(), elem2)

    # BadFlow
    def test_incorrect_sym_string(self):
        with self.assertRaises(ValueError):
            elem = Element('-h_{1}**')


class SymbolTest(unittest.TestCase):

    # Happy flows
    def test_one_index(self):
        string = str(Symbol('chan_{2}'))
        self.assertEqual(string, "chan₂")


    def test_double_index(self):
        string = str(Symbol('chan_{2-45}'))
        self.assertEqual(string, "chan₂₋₄₅")

    def test_zero_symbol(self):
        string = str(Symbol('0'))
        self.assertEqual(string, "0 ")

    # Bad flows
    def test_incorrect_letter(self):
        with self.assertRaises(ValueError):
            sym = Symbol('_{2-45}')

    def test_incorrect_index(self):
        with self.assertRaises(ValueError):
            sym = Symbol('h_{2-4-2}')