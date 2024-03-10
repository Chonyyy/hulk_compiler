import unittest
from lexer.rgx_engine import *
from lexer.ast import *
from lexer.automatons import nfa_to_dfa, automaton_minimization
from cmp.tools.parsing import metodo_predictivo_no_recursivo #FIXME: Change for actual parser later
from cmp.tools.evaluation import evaluate_parse

class TestLexerGenerator(unittest.TestCase):
    def setUp(self):
        pass