from abc import ABC, abstractmethod
from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError, Type
from tools import visitor
from tools.semantic import Scope
from typing import Union

class SemanticChecker(object):
    def __init__(self, context: Context, errors=[]):
        self.errors = errors

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(Program)
    def visit(self, node: Program, scope: Scope=None):
        for child in node.statements:
            self.visit(child, scope)
        return self.errors

    @visitor.when(LetList)
    def visit(self, node, scope):
        if not scope.define_variable(node.id):
            self.errors.append(f"Variable {node.idx} already defined")
        self.visit(node.expr, scope)

    @visitor.when(Function)
    def visit(self, node, scope):
        if not scope.define_function(node.id, [p for p in node.params]):
            self.errors.append(
                f"Function {node.idx} with {len(node.params)} parameters already defined"
            )
        child_scope = scope.create_child_scope()
        for param in node.params:
            child_scope.define_variable(param)
        self.visit(node.body, child_scope)

    @visitor.when(Print)
    def visit(self, node, scope):
        self.visit(node.expr, scope)

    @visitor.when(Number)
    def visit(self, node, scope):
        return self.errors

    @visitor.when(Var)
    def visit(self, node, scope):
        if not scope.is_var_defined(node.lex):
            self.errors.append(f"Variable {node.lex} not defined")
        return self.errors

    @visitor.when(Call)
    def visit(self, node, scope):
        if not scope.is_func_defined(node.lex, len(node.args)):
            self.errors.append(
                f"Function {node.lex} with {len(node.args)} parameters not defined"
            )
        for arg in node.args:
            self.visit(arg, scope)
        return self.errors

    @visitor.when(Binary)
    def visit(self, node, scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        return self.errors