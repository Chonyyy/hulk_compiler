import os
from hulk_definitions.token_def import LEXER
from hulk_definitions.grammar import G
from parser_gen.parser_lr1 import LR1Parser as My_Parser
from tools.evaluation import evaluate_reverse_parse
from tools.semantic import Context, Scope
from hulk_definitions.visitor import FormatVisitor, TypeCollector, TypeBuilder, TypeChecker

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
        # if i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17]:
        #     continue
        with open(f'./hulk_examples/{file}', 'r') as f:
            print(f'=== Reading file: {file} ===')
            text = f.read()
            
            logger.info('=== Tokenizing Text ===')
            tokens = LEXER(text)
            right_parse, operations = my_parser(tokens)
            
            logger.info(f'=== Generating AST for file: {file} ===')
            ast = evaluate_reverse_parse(right_parse, operations, tokens)
            
            logger.info('=== Visualizing AST ===')
            # formatter = FormatVisitor()
            # tree = formatter.visit(ast)
            # print(tree)
            
            logger.info('=== Collecting Types ===')
            errors = []
            context = Context()
            built_in_types = ["Object", "Number", "String", "Boolean", "Vector"]
            built_in_protocols = ["Iterable"]

            for bi_type in built_in_types:
                context.create_type(bi_type)
            for bi_protocol in built_in_protocols:
                context.create_protocol(bi_protocol)

            collector = TypeCollector(context, errors)
            collector.visit(ast)
            context = collector.context

            logger.info('=== Building Types ===')
            builder = TypeBuilder(context, errors)
            builder.visit(ast)
            context = builder.context
            # print('Errors:', errors)
            # print('Context:')
            # print(context)

            global_scope = Scope()
            logger.info('=== Type Inference ===')

            logger.info('=== Type Checking ===')
            checker = TypeChecker(context,  errors)
            checker.visit(ast)
            context = checker.context
            global_scope = checker.scope
            


if __name__ == "__main__":
    main()