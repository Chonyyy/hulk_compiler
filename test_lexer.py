'''
for guidance:
assertEqual
assertNotEqual
assertTrue
assertFalse
assertIs
assertIsNot
assertIsNone
assertIsNotNone
assertIn
assertNotIn
assertIsInstance
assertNotIsInstance
'''

import unittest
from lexer.automatons import *

class TestAutomata(unittest.TestCase):
    def setUp(self):
        pass

    def test_nfa_construction(self):
        nfa = NFA(states=3, finals=[2], transitions={
            (0, 'a'): [0],
            (0, 'b'): [0, 1],
            (1, 'a'): [2]
        })
        test_case = {0: {'a': [0], 'b': [0, 1]}, 1: {'a': [2]}, 2: {}}
        self.assertEqual(nfa.transitions, test_case, "NFA construction failed")
    
    def test_dfa_construction(self):
        dfa = DFA(states=3, finals=[2], transitions={
            (0, 'a'): 0,
            (0, 'b'): 1,
            (1, 'a'): 2,
            (1, 'b'): 1,
            (2, 'a'): 0,
            (2, 'b'): 1,
        })
        test_case = {0: {'a': [0], 'b': [1]}, 1: {'a': [2], 'b': [1]}, 2: {'a': [0], 'b': [1]}}
        self.assertEqual(dfa.transitions, test_case, "DFA construction failed")

if __name__ == '__main__':
    unittest.main()