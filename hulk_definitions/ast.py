from abc import ABC, abstractmethod

class Node(ABC):
    pass

class Program(Node):
    def __init__(self, statements: "Statement"): 
       self.statements  = statements

class Statement(Node):
    def __init__(self, name, body, type = None):
        self.name = name
        self.body = body
        self.type = type

class Expression(Node):
    def __init__(self, value):
        self.value = value

class Let(Expression):
    def __init__(self, name, expr, scope, type = None):
        super().__init__(scope)
        self.name = name
        self.expr = expr
        self.type = type

class LetList(Node):
    def __init__(self, let_statements: list[Let]):
        self.child = None
        current = self.child
        for let in let_statements:
            if self.child is None:
                self.child = let
                current = let
            else:
                current.scope = let
                current = let

class Block(Expression):
    def __init__(self, body):
        super().__init__(body)

class Function(Statement):
    def __init__(self, name, params, body, type = None):
        super().__init__(name, body, type)
        self.params = params

class Conditional(Expression):
    def __init__(self, if_expr, if_body, else_body, branches = None):
        super().__init__(None)
        self.if_expr = if_expr
        self.if_body = if_body
        self.branches = branches
        self.else_body = else_body

class Branch(Expression):
    def __init__(self, condition, body):
        super().__init__(body)
        self.condition = condition

class Unary(Expression):
    def __init__(self, right):
        super().__init__(right)

class Binary(Expression):
    def __init__(self, left, right):
        super().__init__(right)
        self.left = left


class Plus(Binary):
    pass

class BinaryMinus(Binary):
    pass

class Star(Binary):
    pass

class Pow(Binary):
    pass

class Div(Binary):
    pass

class Mod(Binary):
    pass

class Is(Binary):
    pass

class As(Binary):
    pass

class At(Binary):
    pass

class DoubleAt(Binary):
    pass

class Or(Binary):
    pass

class And(Binary):
    pass

class GreaterThan(Binary):
    pass

class LessThan(Binary):
    pass

class GreaterEqual(Binary):
    pass

class LessEqual(Binary):
    pass

class NotEqual(Binary):
    pass

class CompareEqual(Binary):
    pass

class Not(Unary):
    pass

class UnaryMinus(Unary):
    pass

class Atom(Expression):
    def __init__(self, lex):
        super().__init__(lex)

class Call(Atom):
    def __init__(self, idx, args):
        Atom.__init__(self, idx)
        self.args = args

class Number(Atom):
    def __init__(self, lex):
        super().__init__(lex)

class Str(Atom):
    def __init__(self, lex):
        super().__init__(lex)

class Bool(Atom):
    def __init__(self, lex):
        super().__init__(lex)

class Invoke(Atom):
    def __init__(self, container, prop):
        Atom.__init__(self, container)
        self.prop = prop

class Vector(Atom):
    def __init__(self, values):
        Atom.__init__(self, values)

class VectorComprehension(Expression):
    def __init__(self, values, operation):
        Vector.__init__(self, values)
        self.operation = operation

class Var(Atom):
    pass

class ForVar(Var):
    def __init__(self, name, type = None):
        super().__init__(name)
        self.type = type

class TypeDef(Statement):
    def __init__(self, name, body, args, inheritance = None, inner_args = None):
        super().__init__(name, body, inheritance)
        self.args = args
        self.inner_args = inner_args

class TypeCreation(Atom):
    pass

class Protocol(Statement):
    def __init__(self, name, body, extension = None):
        super().__init__(name, body, extension)

class Assign(Atom):
    def __init__(self, name, body):
        Atom.__init__(self, name)
        self.body = body

class Pi(Expression):
    def __init__(self):
        self.lex = "Pi"

class E(Expression):
    def __init__(self):
        self.lex = "E"

class Indexing(Atom):
    def __init__(self, name, index):
        Atom.__init__(self, name)
        self.index = index

class Sin(Call):
    def __init__(self, args):
        super().__init__("sin",args)
        
class Cos(Call):
    def __init__(self, args):
        super().__init__("cos",args)

class Rand(Call):
    def __init__(self, args):
        super().__init__("rand",args)

class Exp(Call):
    def __init__(self, args):
        super().__init__("exp",args)

class Log(Call):
    def __init__(self, args):
        super().__init__("log",args)

class Sqrt(Call):
    def __init__(self, args):
        super().__init__("sqrt",args)

class Print(Call):
    def __init__(self, args):
        super().__init__("print",args)

class Range(Call):
    def __init__(self, args):
        super().__init__("range",args)
    def __len__(self):
        return int(self.args[1].lex - self.args[0].lex)

class While(Expression):
    def __init__(self, stop, body):
        super().__init__(body)
        self.stop = stop

class For(Expression):
    def __init__(self, item, collection, body):
        super().__init__(body)
        self.item = item
        self.collection = collection

class Base(Call):
    def __init__(self, args):
        super().__init__("base", args)

class Property(Expression):
    def __init__(self, name, body, type = None):
        super().__init__(body)
        self.name = name
        self.type = type

class CreateInstance(Expression):
    def __init__(self, type, params):
        super.__init__(self, type)
        self.params = params