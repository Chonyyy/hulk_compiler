from abc import ABC, abstractmethod
from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError
from tools import visitor
from tools.semantic import Scope

class TypeInferer(object):
    def __init__(self, context: Context, errors=[]):
        self.context = context
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Program)
    def visit(self, node: Program):
        for child in node.statements:
            self.visit(child, self.context)

        return self.errors

    @visitor.when(Let)
    def visit(self, node: Let, ctx: Context):
        try:
            type_expr = self.visit(node.expr, ctx)
            if not type_expr.conforms(ctx.get_type(node.type)):
                self.errors.append(f'TypeError: Type {type_expr.name} does not conform to {node.type}')
        except SemanticError as se:
            self.errors.append(se.text)

    @visitor.when(Assign)
    def visit(self, node: Assign, ctx: Context):
        try:
            type_expr = self.visit(node.body, ctx)
            if not type_expr.conforms(ctx.get_type(node.type)):
                self.errors.append(f'TypeError: Type {type_expr.name} does not conform to {node.type}')
        except SemanticError as se:
            self.errors.append(se.text)

    @visitor.when(Conditional)
    def visit(self, node: Conditional, ctx: Context):
        try:
            type_expr = self.visit(node.if_expr, ctx)
            if type_expr.name != 'Bool':
                self.errors.append(f'TypeError: Type {type_expr.name} does not conform to Bool')
        except SemanticError as se:
            self.errors.append(se.text)

        self.visit(node.if_body, ctx)
        self.visit(node.else_body, ctx)

    @visitor.when(For)
    def visit(self, node: For, ctx: Context):
        try:
            type_expr = self.visit(node.collection, ctx)
            if type_expr.name != 'Vector':
                self.errors.append(f'TypeError: Type {type_expr.name} does not conform to Vector')
        except SemanticError as se:
            self.errors.append(se.text)

        self.visit(node.body, ctx)

    @visitor.when(While)
    def visit(self, node: While, ctx: Context):
        try:
            type_expr = self.visit(node.stop, ctx)
            if type_expr.name != 'Bool':
                self.errors.append(f'TypeError: Type {type_expr.name} does not conform to Bool')
        except SemanticError as se:
            self.errors.append(se.text)

        self.visit(node.body, ctx)  

    @visitor.when(Block)
    def visit(self, node: Block, ctx: Context):
        for child in node.body:
            self.visit(child, ctx)
