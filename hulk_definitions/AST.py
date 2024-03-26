from abc import ABC, abstractmethod

class Node(ABC):
    pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

class Statement(Node):
    pass

class Block(Statement):
    def __init__(self, body):
        self.body = body

class Let(Statement):
    def __init__(self, name, expr, scope, type = None):
        self.name = name
        self.expr = expr
        self.scope = scope
        self.type = type

class Function(Statement):
    def __init__(self, name, params, body, type = None):
        self.name = name
        self.params = params
        self.body = body
        self.type = type

class Conditional(Statement):
    def __init__(self, if_expr, if_body, else_body, branches = None):
        self.if_expr = if_expr
        self.if_body = if_body
        self.branches = branches
        self.else_body = else_body

class Branch(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Expression(Statement):
    pass

class Unary(Expression):
    def __init__(self, right):
        self.right = right

class Binary(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

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
        self.lex = lex

class Call(Atom):
    def __init__(self, idx, args):
        Atom.__init__(self, idx)
        self.args = args

class Number(Atom):
    pass

class Str(Atom):
    pass

class Bool(Atom):
    pass

class Invoke(Atom):
    def __init__(self, container, property):
        Atom.__init__(self, property)
        self.container = container

class Vector(Atom):
    def __init__(self, values, len):
        Atom.__init__(self, values)
        self.len = len

class VectorComprehension(Vector):
    def __init__(self, values, len, operation):
        Vector.__init__(self, values, len)
        self.operation = operation

class Var(Atom):
    pass

class TypeDef(Statement):
    def __init__(self, name, body, args, inheritance = None, inner_args = None):
        self.name = name
        self.body = body
        self.inheritance = inheritance
        self.args = args
        self.inner_args = inner_args

class TypeCreation(Atom):
    pass

class Protocol(Statement):
    def __init__(self, name, body, extension = None):
        self.name = name
        self.body = body
        self.extension = extension

class Assign(Atom):
    def __init__(self, name, body):
        Atom.__init__(self, name)
        self.body = body

class Pi(Expression):
    pass

class E(Expression):
    pass

class Indexing(Atom):
    def __init__(self, name, index):
        Atom.__init__(self, name)
        self.index = index

class Sin(Call):
    pass

class Cos(Call):
    pass

class Rand(Call):
    pass

class Exp(Call):
    pass

class Log(Call):
    pass

class Sqrt(Call):
    pass

class Print(Call):
    pass

class Range(Call):
    pass

class While(Statement):
    def __init__(self, stop, body):
        self.stop = stop
        self.body = body

class For(Statement):
    def __init__(self, item, collection, body):
        self.item = item
        self.collection = collection
        self.body = body

class Self(Atom):
    pass

class Property(Expression):
    def __init__(self, name, body, type = None):
        self.name = name
        self.body = body
        self.type = type

class CreateInstance(Expression):
    def __init__(self, type, params):
        self.type = type
        self.params = params