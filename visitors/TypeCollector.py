from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError
from tools import visitor

class TypeCollector(object):
    def __init__(self, context: Context, errors=[]):
        self.context = context
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Program)
    def visit(self, node: Program):
        for child in node.statements:
            if isinstance(child, TypeDef) or isinstance(child, Protocol):
                self.visit(child, self.context)

        return self.errors

    @visitor.when(TypeDef)
    def visit(self, node: TypeDef, ctx: Context):
        try:
            ctx.create_type(node.name)
        except SemanticError as se:
            self.errors.append(se.text)

    @visitor.when(Protocol)
    def visit(self, node: Protocol, ctx: Context):
        try:
            ctx.create_protocol(node.name)
        except SemanticError as se:
            self.errors.append(se.text)
