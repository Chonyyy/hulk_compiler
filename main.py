import os
from hulk_definitions.token_def import LEXER
from hulk_definitions.grammar import G
from parser_gen.parser_lr1 import LR1Parser as My_Parser
from tools.evaluation import evaluate_reverse_parse
from hulk_definitions.visitor import FormatVisitor, TypeCollector
from code_gen.cil import run_pipeline

import sys,logging

logger = logging.getLogger(__name__)

def main(debug = True, verbose = False, force = False):
    file_path = './hulk_compiler.log'

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"The file {file_path} has been deleted.")

    logging.basicConfig(filename='hulk_compiler.log', level=logging.DEBUG)
    files = os.listdir('./hulk_examples')
    logger.info('Program Started')
    logger.info('=== Generating Parser ===')
    my_parser = My_Parser(G, 'parsing_table.dat')

    for i, file in enumerate(files):
        with open(f'./hulk_examples/{file}', 'r') as f:
            
            logger.info(f'=== Reading file: {file} ===')
            text = f.read()
            
            logger.info('=== Tokenizing Text ===')
            tokens = LEXER(text)
            right_parse, operations = my_parser(tokens)
            
            logger.info(f'=== Generating AST for file: {file} ===')
            ast = evaluate_reverse_parse(right_parse, operations, tokens)
            
            logger.info('=== Visualizing AST ===')
            formatter = FormatVisitor()
            tree = formatter.visit(ast)
            print(tree)
            
            logger.info('=== Collecting Types ===')
            errors = []
            collector = TypeCollector(errors)
            collector.visit(ast)
            context = collector.context
            print('Errors:', errors)
            print('Context:')
            print(context)
            
            # Code generation CIL
            ast, errors, context, scope, cil_ast = run_pipeline(G, text)

if __name__ == "__main__":
    main()