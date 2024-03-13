
from lexer_gen import *
from lexer_gen.utils import *
from typing import Any, Dict, Iterable, List, Set, Tuple, Union
from lexer_gen.ast import UnionNode, ConcatNode, ClosureNode, SymbolNode, EpsilonNode
from cmp.pycompiler import Grammar
import pydot
import math


G = Grammar()

E = G.NonTerminal('E', True)
program,expression = G.NonTerminals('program expression ')
pipe, star, opar, cpar, symbol, epsilon, cpar, equal, plus, minus, asterisk, slash, backslash, circumflex, at, obracket, cbracket, obrace, cbrace, percent, dot, comma, and_token, or_token, not_token, colon, implication, potencial, destructive_assignment, comp_eq, comp_neq, comp_gt, comp_lt, comp_gte, comp_lte, double_at, print_token, sqrt, sin, cos, exp, log, rand, range_token, pi, e, function_token, let, in_token, if_token, else_token, true, false, elif_token, while_token, for_token, type_token, self_token, new, inherits, number, object_token, string, boolean, is_token, as_token, protocol, extends, iterable, range = G.Terminals('comment_line SEMICOLON OPAR CPAR EQUAL PLUS MINUS ASTERISK SLASH BACKSLASH CIRCUMFLEX AT OBRACKET CBRACKET OBRACE CBRACE PERCENT DOT COMMA AND OR NOT COLON IMPLICATION POTENCIAL DESTRUCTIVE_ASSIGNMENT COMP_EQ COMP_NEQ COMP_GT COMP_LT COMP_GTE COMP_LTE DOUBLE_AT PRINT SQRT SIN COS EXP LOG RAND RANGE PI E FUNCTION LET IN IF ELSE TRUE FALSE ELIF WHILE FOR TYPE SELF NEW INHERITS NUMBER OBJECT STRING BOOLEAN IS AS PROTOCOL EXTENDS ITERABLE RANGE string id num ws')


('', f'//({letters}|{uppercase_letters}|0|{nonzero_digits}|\t| |\\\\")*(\n)*'),#TODO: Add more symbols to this; Why // not final state ?; Fix how ne_line orks 
    ('', ';'),
    ('', '\('),
    ('CPAR', '\)'),
    ('EQUAL', '='),
    ('PLUS', '+'),
    ('MINUS', '-'),
    ('ASTERISK', '\*'),
    ('SLASH', '/'),
    ('BACKSLASH', '\\\\'),
    ('CIRCUMFLEX', '^'),
    # ('DITTO', '"'),
    ('AT', '@'),
    ('OBRACKET', '{'),
    ('CBRACKET', '}'),
    ('OBRACE', '['),
    ('CBRACE', ']'),
    ('PERCENT', '%'),
    ('DOT', '.'),
    ('COMMA', ','),
    ('AND', '&'),
    ('OR', '\|'),
    ('NOT', '!'),
    ('COLON', ':'),
    ('IMPLICATION', '=>'),
    ('POTENCIAL', '\*\*'),
    ('DESTRUCTIVE_ASSIGNMENT', ':='),
    ('COMP_EQ', '=='),
    ('COMP_NEQ', '!='),
    ('COMP_GT', '>'),
    ('COMP_LT', '<'),
    ('COMP_GTE', '>='),
    ('COMP_LTE', '<='),
    ('DOUBLE_AT', '@@'),
    # BUILT IN FUNCTIONS
    ('PRINT', 'print'),
    ('SQRT', 'sqrt'),
    ('SIN', 'sin'),
    ('COS', 'cos'),
    ('EXP', 'exp'),
    ('LOG', 'log'),
    ('RAND', 'rand'),
    ('RANGE', 'range'),
    # KEYWORDS
    ('PI', 'PI'),
    ('E', 'E'),
    ('FUNCTION', 'function'),
    ('LET', 'let'),
    ('IN', 'in'),
    ('IF', 'if'),
    ('ELSE', 'else'),
    ('TRUE', 'true'),
    ('FALSE', 'false'),
    ('ELIF', 'elif'),
    ('WHILE', 'while'),
    ('FOR', 'for'),
    ('TYPE', 'type'),
    ('SELF', 'self'),
    ('NEW', 'new'),
    ('INHERITS', 'inherits'),
    ('NUMBER', 'Number'),
    ('OBJECT', 'Object'),
    ('STRING', 'String'),
    ('BOOLEAN', 'Boolean'),
    ('IS', 'is'),
    ('AS', 'as'),
    ('PROTOCOL', 'protocol'),
    ('EXTENDS', 'extends'),
    ('ITERABLE', 'Iterable'),
    ('RANGE', 'Range'),
    # OTHERS
    ('string', f'"({letters}|{uppercase_letters}|0|{nonzero_digits}|{valid_string_symbols}|\t| |\\\\")*"'),#TODO: Add more symbols to this
    ('id', f'({letters}|{uppercase_letters})({letters}|{uppercase_letters}|0|{nonzero_digits}|{valid_id_symbols})*'),
    ('num', f'({natural_aster_numbers}|{floating_point_numbers})'),
    ('ws', f'({delim})({delim})*'),
], 'eof')

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