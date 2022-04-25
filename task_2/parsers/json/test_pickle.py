import unittest
from pickle import Pickle
from test_functions import *


class TestPickle(unittest.TestCase):
    def setUp(self):
        self.pickle = Pickle()

    def testSerialize(self):
        test_obj = {"a": 1, "b": {"c": 3}}

        self.assertEqual(self.pickle.serialize(test_obj), b'\x80\x04\x95\x18\x00\x00\x00\x00\x00\
        x00\x00}\x94(\x8c\x01a\x94K\x01\x8c\x01b\x94}\x94\x8c\x01c\x94K\x03su.')

    def testParse(self):
        test_string = b'\x80\x04\x95\x18\x00\x00\x00\x00\x00\x00\x00}\x94' \
                     b'(\x8c\x01a\x94K\x01\x8c\x01b\x94}\x94\x8c\x01c\x94K\x03su.'
        self.assertEqual(self.pickle.parse(test_string), {"a": 1, "b": {"c": 3}})

    def testBackAndForth(self):
        test_obj = {"func": test_func, "testClass": A}
        pickled = self.pickle.dumps(test_obj)
        pickled_pickled = self.pickle.loads(pickled)
        self.assertEqual(pickled_pickled, test_obj)


if __name__ == "__main__":
    unittest.main()
