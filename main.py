import os
from hulk_definitions.token_def import LEXER
from hulk_definitions.grammar import G
from parser_gen.parser_lr1 import LR1Parser as My_Parser
from tools.evaluation import evaluate_reverse_parse
from tools.semantic import Context, Scope
from visitors.Formatter import FormatVisitor
from visitors.ScopeGen import GlobalScopeBuilder
from visitors.SemanticChecker import SemanticChecker
from visitors.TypeCollector import TypeCollector
from visitors.TypeBuilder import TypeBuilder
from visitors.interpreter import Interpreter

import logging

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
        if file in [
            "1_example_expressions.hlk",
            # "2_example_functions.hlk",
            # "3_example_variables.hlk",
            # "4_example_conditionals.hlk",
            # "5_example_loops.hlk",
            # "6_example_types.hlk",
            # "7_example_type_checking.hlk",
            # "8_example_protocol.hlk",
            "9_example_vector.hlk",
            "11_example_expressions.hlk",
            "12_example_functions.hlk",
            "13_example_variables.hlk",
            "14_example_conditionals.hlk",
            "15_example_loops.hlk",
            "16_example_types.hlk",
            "17_example_type_checking.hlk",
            "18_example_protocol.hlk",
            "19_example_vector.hlk",
            "testing_TypeChecker.hlk",
            "TODO"
        ]:
            continue
        with open(f'./hulk_examples/{file}', 'r') as f:
            print(f'=== Reading file: {file} ===')
            text = f.read()
            
            logger.info('=== Tokenizing Text ===')
            tokens = LEXER(text)
            right_parse, operations = my_parser(tokens)
            
            logger.info(f'=== Generating AST for file: {file} ===')
            ast = evaluate_reverse_parse(right_parse, operations, tokens)
            
            logger.info('=== Visualizing AST ===')
            formatter = FormatVisitor()
            # tree = formatter.visit(ast)
            # print(tree)
            
            logger.info('=== Collecting Types ===')
            errors = []
            context = Context()
            built_in_types = ["Object", "Number", "String", "Boolean", "Vector", "Dinamic"]
            built_in_protocols = ["Iterable"]

            for bi_type in built_in_types:
                context.create_type(bi_type)
            for bi_protocol in built_in_protocols:
                context.create_protocol(bi_protocol)
                if bi_protocol == "Iterable":
                    iterable_protocol = context.get_protocol(bi_protocol)
                    iterable_protocol.define_method("next", [], "Object")
                    iterable_protocol.define_method("current", [], "Object")

            print('=== Collecting Types ===')
            collector = TypeCollector(context, errors)
            collector.visit(ast)
            context = collector.context
            print("=== Done ===")
            print('Errors', errors)

            print('=== Building Types ===')
            builder = TypeBuilder(context, errors)
            builder.visit(ast)
            context = builder.context
            print("=== Done ===")
            print('Errors', errors)

            print('=== Building Global Scope ===')
            global_scope_builder = GlobalScopeBuilder(context, errors)
            global_scope_builder.visit(ast)
            global_scope = global_scope_builder.global_scope
            print("=== Done ===")
            print('Errors', errors)

            print("=== AST Interpreter ===")
            tree_interpreter = Interpreter(context)
            tree_interpreter.visit(ast)

            # logger.info('=== Type Inference ===')

            # logger.info('=== Type Checking ===')
            # checker = TypeChecker(context,  errors)
            # checker.visit(ast)
            # context = checker.context
            # global_scope = checker.scope
            


if __name__ == "__main__":
    main()