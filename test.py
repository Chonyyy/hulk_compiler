from lexer.lexer import Lexer
import os

# nonzero_digits = '|'.join(str(n) for n in range(1,10))
# letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))

# print('Non-zero digits:', nonzero_digits)
# print('Letters:', letters)

# lexer = Lexer([
#     ('num', f'({nonzero_digits})(0|{nonzero_digits})*'),
#     ('for' , 'for'),
#     ('foreach' , 'foreach'),
#     ('space', ' *'),
#     ('id', f'({letters})({letters}|0|{nonzero_digits})*')
# ], 'eof')

# text = '5465 for 45foreach fore'
# print(f'\n>>> Tokenizando: "{text}"')
# tokens = lexer(text)
# print(tokens)
# assert [t.token_type for t in tokens] == ['num', 'space', 'for', 'space', 'num', 'foreach', 'space', 'id', 'eof']
# assert [t.lex for t in tokens] == ['5465', ' ', 'for', ' ', '45', 'foreach', ' ', 'fore', '$']

# text = '4forense forforeach for4foreach foreach 4for'
# print(f'\n>>> Tokenizando: "{text}"')
# tokens = lexer(text)
# print(tokens)
# assert [t.token_type for t in tokens] == ['num', 'id', 'space', 'id', 'space', 'id', 'space', 'foreach', 'space', 'num', 'for', 'eof']
# assert [t.lex for t in tokens] == ['4', 'forense', ' ', 'forforeach', ' ', 'for4foreach', ' ', 'foreach', ' ', '4', 'for', '$']


# TESTING WITH HULK #

all_symbols = '|'.join(chr(n) for n in range(255) if not n in [ord('\\'), ord('|'), ord('*'), ord('ε'), ord('('), ord(')'), ord('\n'), ord('"')])
escaped_regex_operations = '|'.join(s for s in "\| \* \( \) \ε".split())
nonzero_digits = '|'.join(str(n) for n in range(1,10))
letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))
uppercase_letters = '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1))
valid_name_symbols = ['_']
delim = ' |\t|\n' 


lexer = Lexer([
    # ('string', f'"(0|{all_symbols})*"'),
    ('string', f'"({letters}|{uppercase_letters}|0|{nonzero_digits}| |\t|\\\\")*"'),
    # SYMBOLS
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
    ('num', f'({nonzero_digits})(0|{nonzero_digits})*'),
    # ('CLOSURE_PROBLEM', f'(asdasdasd)*'),
    ('id', f'({letters})({letters}|0|{nonzero_digits}|{valid_name_symbols})*'),
    ('ws', f'({delim})({delim})*'),
], 'eof')

#[ ]:  CHECK THESE VALUES:
# 1. The SELF token ?
# 2. The NUMBER token ?
# 1. The STRING token ?
#[ ]: MISSING DEFINITIONS:

# READING EXAMPLES FROM FILES
# files addr: ./hulk_examples
files = os.listdir('./hulk_examples')
for file in files:
    with open(f'./hulk_examples/{file}', 'r') as f:
        text = f.read()
        print(f'\n>>> Tokenizing file: {file}')
        tokens = lexer(text)
        print([t.token_type for t in tokens])
        print('---'*20)
        print('\n')