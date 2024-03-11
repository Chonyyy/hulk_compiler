from typing import Any
from cmp.utils import Token
from lexer.automatons import DFA, nfa_to_dfa
from lexer.pycompiler import Grammar
from lexer import G
from cmp.tools.parsing import metodo_predictivo_no_recursivo #FIXME: Change for actual parser later
from cmp.tools.evaluation import evaluate_parse

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
        left_parse = parser(tokens)
        ast = evaluate_parse(left_parse, tokens)
        nfa = ast.evaluate()
        self.automaton = nfa_to_dfa(nfa)
    
    def __call__(self, string) -> bool:
        return self.automaton.recognize(string)