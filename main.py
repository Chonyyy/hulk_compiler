import os
from hulk_definitions.token_def import LEXER
from hulk_definitions.grammar import G
from parser_gen.parser_lr1 import LR1Parser as My_Parser
from tools.evaluation import evaluate_reverse_parse
from cmp.tools.parsing import LR1Parser
from hulk_definitions.visitor import FormatVisitor

import sys,logging

logger = logging.getLogger(__name__)

sys.setrecursionlimit(10000000)

def main(debug = True, verbose = False, force = False):
    file_path = './hulk_compiler.log'

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"The file {file_path} has been deleted.")

    if debug:
        logging.basicConfig(filename='hulk_compiler.log', level=logging.DEBUG)
        files = os.listdir('./hulk_examples')
        logger.info('Program Started')
        logger.info('=== Generating Parser ===')
        # parser = LR1Parser(G, True)
        my_parser = None
        
        my_parser = My_Parser(G)

        for i, file in enumerate(files):
            with open(f'./hulk_examples/{file}', 'r') as f:
                logger.info(f'=== Reading file: {file} ===')
                text = f.read()
                logger.info('=== Tokenizing Text ===')
                tokens = LEXER(text)
                right_parse, operations = my_parser(tokens)
                logger.info(f'=== Derivation Secuence for File {file} ===')
                for derivation in right_parse:
                    logger.info(f'{derivation}')
                print(f'file {i} is parsed.')
                ast = evaluate_reverse_parse(right_parse, operations, tokens)
                formatter = FormatVisitor()
                tree = formatter.visit(ast)
                print(tree)

if __name__ == "__main__":
    main()