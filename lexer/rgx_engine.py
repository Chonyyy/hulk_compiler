from typing import Any
from lexer.pycompiler import Grammar
from lexer.utils import Token

class Regex:
    def __init__(self, rgx):
        pass

    def __call__(self, string) -> Any:
        pass

    def regex_tokenizer(text, G:Grammar, skip_whitespaces=True):
        tokens = []
        # > fixed_tokens = ???
        # Your code here!!!
        fixed_tokens = "| * ( ) ε".split()
        # End of my input
        for char in text:
            if skip_whitespaces and char.isspace():
                continue
            # Your code here!!!
            elif char in fixed_tokens:
                tokens.append(Token(char,G.symbDict[char]))
            else:
                tokens.append(Token(char,G.symbDict["symbol"]))
        # End of my input
        tokens.append(Token('$', G.EOF))
        return tokens