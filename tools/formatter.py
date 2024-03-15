import cmp.visitor as visitor
from lexer_gen.ast import *

class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(UnionNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\UnionNode [<left>; ... <right>;]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in [node.right, node.left])
        return f'{ans}\n{statements}'
    
    @visitor.when(ConcatNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\ConcatNode [<left>; ... <right>;]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in [node.right, node.left])
        return f'{ans}\n{statements}'
    
    @visitor.when(ClosureNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VarDeclarationNode: let {node.id} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(AtomicNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'