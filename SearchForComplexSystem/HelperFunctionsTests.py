from helper_functions import *
import unittest


class SplitByReceiversTest(unittest.TestCase):

    def test_split_by_receivers(self):
        h = Block("-h_{1-1} // h_{2-1}* // h_{2-3}* // h_{1-2} // -h_{1-3} // h_{2-2}*")
        d = split_by_receivers(h)
        self.assertEqual(d, {'1': [0, 1], '2': [3, 5], '3': [4, 2]})

    def test_get_conjugates_by_rec(self):
        h = Block("-h_{1-1} // h_{2-1}* // h_{2-3}* // h_{1-2} // -h_{1-3} // h_{2-2}*")
        d = split_by_receivers(h)
        with self.assertRaises(ValueError):
            get_conjugate_by_receiver(h, d)

        h = Block("-h_{1-1}* // h_{2-1}* // h_{2-3} // h_{1-2}* // -h_{1-3} // h_{2-2}*")
        d = split_by_receivers(h)
        self.assertEqual(get_conjugate_by_receiver(h, d), {'1': '*', '2': '*', '3': ''})
