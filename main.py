import os
from hulk_definitions.token_def import LEXER
from hulk_definitions.grammar import G
from parser_gen.parser_lr1 import LR1Parser as My_Parser
from tools.evaluation import evaluate_reverse_parse
from cmp.tools.parsing import LR1Parser
import sys

sys.setrecursionlimit(100000)

# READING EXAMPLES FROM FILES
files = os.listdir('./hulk_examples')
for file in files:
    with open(f'./hulk_examples/{file}', 'r') as f:
        text = f.read()
        print(f'\n>>> Tokenizing file: {file}')
        parser = LR1Parser(G, True)
        # my_parser = My_Parser(G, True)
        # assert parser == my_parser
        tokens = LEXER(text)
        # right_parse, operations = parser(tokens)
        # print(right_parse.reverse())        