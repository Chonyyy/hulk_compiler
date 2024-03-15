from tools.pycompiler import EOF
from parser_gen.parser_lr1 import ShiftReduceParser

def evaluate_reverse_parse(right_parse, operations, tokens):
    if not right_parse or not operations or not tokens:
        return

    right_parse = iter(right_parse)
    tokens = iter(tokens)
    stack = []
    for operation in operations:
        if operation == ShiftReduceParser.SHIFT:
            token = next(tokens)
            stack.append(token.lex)
        elif operation == ShiftReduceParser.REDUCE:
            production = next(right_parse)
            head, body = production
            attributes = production.attributes
            assert all(rule is None for rule in attributes[1:]), 'There must be only synteticed attributes.'
            rule = attributes[0]

            if len(body):
                synteticed = [None] + stack[-len(body):]
                value = rule(None, synteticed)
                stack[-len(body):] = [value]
            else:
                stack.append(rule(None, None))
        else:
            raise Exception('Invalid action!!!')

    assert len(stack) == 1
    assert isinstance(next(tokens).token_type, EOF)
    return stack[0]

def evaluate_parse(left_parse, tokens):
    if not left_parse or not tokens:
        return

    left_parse = iter(left_parse)
    tokens = iter(tokens)
    result = evaluate(next(left_parse), left_parse, tokens)

    assert isinstance(next(tokens).token_type, EOF)
    return result


def evaluate(production, left_parse, tokens, inherited_value=None):
    head, body = production
    attributes = production.attributes

    # Insert your code here ...
    # > synteticed = ...
    # > inherited = ...
    # Anything to do with inherited_value?
    synteticed = [None] * (len(body) + 1)
    inherited = [None] * (len(body) + 1)

    inherited[0] = inherited_value

    for i, symbol in enumerate(body, 1):
        if symbol.IsTerminal:
            assert inherited[i] is None
            # Insert your code here ...
            token = next(tokens)
            synteticed[i] = token.lex
        else:
            next_production = next(left_parse)
            assert symbol == next_production.Left
            # Insert your code here ...
            if not attributes[i] is None:
                inherited[i] = attributes[i](inherited, synteticed)
            synteticed[i] = evaluate(next_production, left_parse, tokens, inherited[i])

    return attributes[0](inherited, synteticed)
