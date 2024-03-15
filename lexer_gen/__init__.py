'''

'''
from lexer_gen import *
from lexer_gen.utils import *
from typing import Any, Dict, Iterable, List, Set, Tuple, Union
from lexer_gen.ast import UnionNode, ConcatNode, ClosureNode, SymbolNode, EpsilonNode
from tools.pycompiler import Grammar
import pydot
import math


G = Grammar()

E = G.NonTerminal('E', True)
T, F, A, X, Y, Z = G.NonTerminals('T F A X Y Z')
pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')

############################ BEGIN PRODUCTIONS ############################
# ======================================================================= #
#                                                                         #
# ========================== { E --> T X } ============================== #
#                                                                         #
E %= T + X, lambda h,s: s[2], None, lambda h,s: s[1]
#                                                                         #
# =================== { X --> '|' T X | epsilon } ======================= #
#                                                                         #
X %= pipe + T + X, lambda h,s: s[3], None, None, lambda h,s: UnionNode(h[0], s[2]) #FIXME: arregla el or ese bro
X %= G.Epsilon, lambda h,s: h[0]
#                                                                         #
# ============================ { T --> F Y } ============================ #
#                                                                         #
T %= F + Y, lambda h,s: s[2], None, lambda h,s: s[1]
#                                                                         #
# ==================== { Y --> F Y | epsilon } ========================== #
#                                                                         #
Y %=  F + Y, lambda h,s: s[2], None, lambda h,s: ConcatNode(h[0], s[1]) #FIXME: arregla el concat ese manin
Y %= G.Epsilon, lambda h,s: h[0]
#                                                                         #
# ======================= { F --> A Z } ================================= #
#                                                                         #
F %= A + Z, lambda h,s: s[2], None, lambda h,s: s[1]
#                                                                         #
# ==================== { Z --> * Z | epsilon } ========================== #
#                                                                         #
Z %= star + Z, lambda h,s: s[2], None, lambda h,s: ClosureNode(h[0]) #FIXME: arregla el closure ese maquina 
Z %= G.Epsilon, lambda h,s: h[0]
#                                                                         #
# ==================== { A --> symbol | 'Epsilon' | ( E ) } ============= #
#                                                                         #
A %= symbol, lambda h,s: SymbolNode(s[1]), symbol
A %= epsilon, lambda h,s: EpsilonNode(s[1]), epsilon
A %= opar + E + cpar, lambda h,s: s[2], None, None, None
#                                                                         #
# ======================================================================= #
############################# END PRODUCTIONS #############################