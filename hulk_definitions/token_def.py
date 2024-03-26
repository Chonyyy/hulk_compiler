from lexer_gen.lexer import Lexer
import os, logging
#TODO: FOR TESTING, MAKE GOOD LATER
from hulk_definitions.grammar import G
logger = logging.getLogger(__name__)

logger.info("Defining Terminals and Non Terminals")
all_symbols = '|'.join(chr(n) for n in range(255) if not n in [ord('\\'), ord('|'), ord('*'), ord('ε'), ord('('), ord(')'), ord('\n'), ord('"')])
escaped_regex_operations = '|'.join(s for s in "\| \* \( \) \ε".split())
nonzero_digits = '|'.join(str(n) for n in range(1,10))
letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))
uppercase_letters = '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1))
valid_string_symbols = '|'.join(c for c in " : ' ; , . _ - + / ^ % & ! = < > \\( \\) { } [ ] @".split())
valid_id_symbols = ['_']
delim = ' |\t|\n' 
natural_numbers = f'({nonzero_digits})({nonzero_digits}|0)*'
natural_aster_numbers = f'({natural_numbers})|0'
floating_point_numbers = f'({natural_aster_numbers}).(({natural_aster_numbers})({natural_aster_numbers})*)'

LEXER = Lexer([
    ('num', f'({natural_aster_numbers})|({floating_point_numbers})'),
    # SYMBOLS
    ('comment_line', f'//({letters}|{uppercase_letters}|0|{nonzero_digits}|\t| |\\\\")*(\n)*'),#TODO: Add more symbols to this; Why // not final state ?; Fix how ne_line orks 
    ('SEMICOLON', ';'),
    ('OPAR', '\('),
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
    ('DOUBLE_PIPE', '\|\|'),
    # BUILT IN FUNCTIONS
    ('PRINT', 'print'),
    ('SQRT', 'sqrt'),
    ('SIN', 'sin'),
    ('COS', 'cos'),
    ('COT', 'cot'),
    ('TAN', 'tan'),
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
    ('ws', f'({delim})({delim})*'),
], '$', G)

logger.info("Lexer Creation Done")

#[ ]:  CHECK THESE VALUES:
# 1. The STRING token ?
#[ ]: MISSING DEFINITIONS: