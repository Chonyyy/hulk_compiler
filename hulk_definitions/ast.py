from abc import ABC, abstractmethod

class Node(ABC):
    pass

class Program(Node):
    def __init__(self, statements: "Statement"): 
       self.statements  = statements

class Statement(Node):
    pass

class Let(Statement):
    def __init__(self, name, expr, scope, type = None):
        self.name = name
        self.expr = expr
        self.scope = scope
        self.type = type

class LetList(Statement):
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

class Block(Statement):
    def __init__(self, body):
        self.body = body

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
        self.idx = idx
        self.args = args

class Number(Atom):
    def __init__(self, lex):
        super().__init__(lex)
        self.type = "Number"

class Str(Atom):
    def __init__(self, lex):
        super().__init__(lex)
        self.type = "String"

class Bool(Atom):
    def __init__(self, lex):
        super().__init__(lex)
        self.type = "Bool"

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

class ForVar(Var):
    def __init__(self, name, type = None):
        self.name = name
        self.type = type

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
    def __len__(self):#TODO: Parche arreglar esto
        return int(self.args[1].lex - self.args[0].lex)

class While(Statement):
    def __init__(self, stop, body):
        self.stop = stop
        self.body = body

class For(Statement):
    def __init__(self, item, collection, body):
        self.item = item
        self.collection = collection
        self.body = body

class Base(Call):
    def __init__(self, args):
        super().__init__("base", args)

class Property(Expression):
    def __init__(self, name, body, type = None):
        self.name = name
        self.body = body
        self.type = type

class CreateInstance(Expression):
    def __init__(self, type, params):
        self.type = type
        self.params = params