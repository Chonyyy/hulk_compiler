import unittest
from lexer_gen.rgx_engine import *
from lexer_gen.ast import *
from lexer_gen.automatons import nfa_to_dfa, automaton_minimization
from cmp.tools.parsing import metodo_predictivo_no_recursivo #FIXME: Change for actual parser later
from cmp.tools.evaluation import evaluate_parse

class TestRgxEngine(unittest.TestCase):
    def setUp(self):
        self.G = Grammar()

        self.E = self.G.NonTerminal('E', True)
        self.T, self.F, self.A, self.X, self.Y, self.Z = self.G.NonTerminals('T F A X Y Z')
        self.pipe, self.star, self.opar, self.cpar, self.symbol, self.epsilon = self.G.Terminals('| * ( ) symbol ε')
        
        self.tokens = regex_tokenizer('a*(a|b)*cd | ε', self.G)

        ############################ BEGIN PRODUCTIONS ############################
        # ======================================================================= #
        #                                                                         #
        # ========================== { E --> T X } ============================== #
        #                                                                         #
        self.E %= self.T + self.X, lambda h,s: s[2], None, lambda h,s: s[1]
        #                                                                         #
        # =================== { X --> '|' T X | epsilon } ======================= #
        #                                                                         #
        self.X %= self.pipe + self.T + self.X, lambda h,s: s[3], None, None, lambda h,s: UnionNode(h[0], s[2]) #FIXME: arregla el or ese bro
        self.X %= self.G.Epsilon, lambda h,s: h[0]
        #                                                                         #
        # ============================ { T --> F Y } ============================ #
        #                                                                         #
        self.T %= self.F + self.Y, lambda h,s: s[2], None, lambda h,s: s[1]
        #                                                                         #
        # ==================== { Y --> F Y | epsilon } ========================== #
        #                                                                         #
        self.Y %=  self.F + self.Y, lambda h,s: s[2], None, lambda h,s: ConcatNode(h[0], s[1]) #FIXME: arregla el concat ese manin
        self.Y %= self.G.Epsilon, lambda h,s: h[0]
        #                                                                         #
        # ======================= { F --> A Z } ================================= #
        #                                                                         #
        self.F %= self.A + self.Z, lambda h,s: s[2], None, lambda h,s: s[1]
        #                                                                         #
        # ==================== { Z --> * Z | epsilon } ========================== #
        #                                                                         #
        self.Z %= self.star + self.Z, lambda h,s: s[2], None, lambda h,s: ClosureNode(h[0]) #FIXME: arregla el closure ese maquina 
        self.Z %= self.G.Epsilon, lambda h,s: h[0]
        #                                                                         #
        # ==================== { A --> symbol | 'Epsilon' | ( E ) } ============= #
        #                                                                         #
        self.A %= self.symbol, lambda h,s: SymbolNode(s[1]), self.symbol
        self.A %= self.epsilon, lambda h,s: EpsilonNode(s[1]), self.epsilon
        self.A %= self.opar + self.E + self.cpar, lambda h,s: s[2], None, None, None
        #                                                                         #
        # ======================================================================= #
        ############################# END PRODUCTIONS #############################

    def test_rgx_parser(self):
        #Usage Example
        parser = metodo_predictivo_no_recursivo(self.G)
        left_parse = parser(self.tokens)
        ast = evaluate_parse(left_parse, self.tokens)
        nfa = ast.evaluate()
        dfa = nfa_to_dfa(nfa)

        assert dfa.recognize('')
        assert dfa.recognize('cd')
        assert dfa.recognize('aaaaacd')
        assert dfa.recognize('bbbbbcd')
        assert dfa.recognize('bbabababcd')
        assert dfa.recognize('aaabbabababcd')

        assert not dfa.recognize('cda')
        assert not dfa.recognize('aaaaa')
        assert not dfa.recognize('bbbbb')
        assert not dfa.recognize('ababba')
        assert not dfa.recognize('cdbaba')
        assert not dfa.recognize('cababad')
        assert not dfa.recognize('bababacc')

        mini = automaton_minimization(dfa)