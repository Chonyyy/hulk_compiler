class HulkLexerError(Exception):
    """Base class for lexer errors."""
    pass

class UnrecognizedTokenError(HulkLexerError):
    """Exception raised when encountering an unrecognized token."""
    def __init__(self, token):
        self.token = token
        super().__init__(f"Unrecognized token '{token}' at line {token.line}, column {token.column}.")

class TokenAlreadyDefinedError(HulkLexerError):
    """Exception raised when trying to define a token type that's already defined."""
    def __init__(self, token_type):
        self.token_type = token_type
        super().__init__(f"Token of type '{token_type}' is already defined.")

class HulkParserError(Exception):
    """Base class for parser errors."""
    pass

class UnexpectedTokenError(HulkParserError):
    """Exception raised when encountering an unexpected token during parsing."""
    def __init__(self, expected, found):
        self.expected = expected
        self.found = found
        super().__init__(f"Expected '{expected}', found '{found}' at line {found.line}, column {found.column}.")
