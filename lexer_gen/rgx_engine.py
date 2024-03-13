from typing import Any
from cmp.utils import Token
from lexer_gen.automatons import DFA, nfa_to_dfa
from lexer_gen.pycompiler import Grammar
from lexer_gen import G
from cmp.tools.parsing import metodo_predictivo_no_recursivo #FIXME: Change for actual parser later
from parser_gen.parser_lr1 import LR1Parser
from cmp.tools.evaluation import evaluate_parse
# TODO: change parsing tools for ours

def regex_tokenizer(text:str, G:Grammar, skip_whitespaces=True):
    tokens = []
    # > fixed_tokens = ???
    # Your code here!!!
    fixed_tokens = "| * ( ) ε".split() #TODO: ADD BACKSLASH TO ESCAPE SPECIAL CHARACTERS
    # End of my input
    escape = False
    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        # Your code here!!!
        elif char == '\\' and not escape:
            escape = True
        elif char in fixed_tokens and not escape:
            tokens.append(Token(char,G.symbDict[char]))
        else:
            escape = False
            tokens.append(Token(char,G.symbDict["symbol"]))
    # End of my input
    tokens.append(Token('$', G.EOF))
    return tokens

class Regex:
    def __init__(self, rgx):
        tokens = regex_tokenizer(rgx, G, skip_whitespaces=False)
        parser = metodo_predictivo_no_recursivo(G)
        other_parser = LR1Parser(G)
        # parser = LR1Parser(G)
        left_parse:list = parser(tokens)
        other_left_parse:list = other_parser(tokens)#[ ]: Does the LR1 Parser give me a right parse ?
        other_left_parse.reverse()
        assert len(left_parse) == len(other_left_parse)
        for i in range(len(left_parse)):
            assert left_parse[i] in other_left_parse, f'LEFT PARSE DERIVATION:{left_parse[i]}   O LEFT PARSE DERIVATION:{other_left_parse[i]}'
        # left_parse.reverse()
        ast = evaluate_parse(left_parse, tokens)# FIXME: Why does it give errors with my left parse ?
        nfa = ast.evaluate()
        self.automaton = nfa_to_dfa(nfa)
    
    def __call__(self, string) -> bool:
        return self.automaton.recognize(string)