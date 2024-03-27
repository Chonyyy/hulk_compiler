from abc import ABC, abstractmethod
from cmp.visitor import on, when
from hulk_definitions.ast import *

class FormatVisitor(object):
    @on('node')
    def visit(self, node, tabs=0):
        pass

    @when(Program)
    def visit(self, node: Program, tabs=0):
        print("Program")
        ans = '\t' * tabs + f'\\__Program: {len(node.statements)} statements'
        statements = ''
        for statement in node.statements:
            # print(type(statement))
            asd = self.visit(statement, tabs + 1)
            print(asd)
            statements.join(asd) 
        # statements = '\n'.join(self.visit(child, tabs + 1) for child in node.statements)
        return f'{ans}\n{statements}'

    @when(Statement)
    def visit(self, node: Statement, tabs=0):
        return '\t' * tabs + f'\\__Statement: {node.__class__.__name__}'

    @when(LetList)
    def visit(self, node: LetList, tabs=0):
        for child in node.children:
            return f'{self.visit(child, tabs)}'

    @when(Assign)
    def visit(self, node:Assign, tabs=0):
        ans = '\t' * tabs + f'\\__Assign: {node.lex} = <expr>'
        expr = self.visit(node.body, tabs + 1)
        return f'{ans}\n{expr}'

    @when(Function)
    def visit(self, node: Function, tabs=0):
        params = "<no_params>"
        if node.params:
            params = ', '.join(f'{name}' for name in node.params)
        ans = '\t' * tabs + f'\\__Function: {node.name}({params}) -> <body>'
        body = ''.join(self.visit(node.body, tabs + 1))
        return f'{ans}\n{body}'

    @when(Protocol)
    def visit(self, node:Protocol, tabs=0):
        ans = '\t' * tabs + f'\\__Protocol: {node.name}'
        body = ''.join(self.visit(child, tabs + 1) for child in node.body)
        return f'{ans}\n{body}'

    @when(TypeDef)
    def visit(self, node:TypeDef, tabs=0):
        if node.inheritance is None:
            ans = '\t' * tabs + f'\\__TypeDef: {node.name}'
        else:
            ans = '\t' * tabs + f'\\__TypeDef: {node.name} inherits from {node.inheritance}'#TODO: Check this
        body = '<empty_body>'
        if node.body:
            body = '\n'.join(self.visit(child, tabs + 1) for child in node.body)
        return f'{ans}\n{body}'

    @when(Print)
    def visit(self, node:Print, tabs=0):
        ans = '\t' * tabs + f'\\__Print:(<args>)'
        # args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        args = ''
        for arg in node.args: #TODO parche
            if not arg:
                continue
            args += str(self.visit(arg,tabs + 1))
        return f'{ans}\n{args}'

    @when(Number)
    def visit(self, node: Number, tabs=0):
        return '\t' * tabs + f'\\__Number: {node.lex}'

    @when(For)
    def visit(self, node:For, tabs=0):
        ans = '\t' * tabs + f'\\__For: {node.item} in <collection> -> <body>'
        collection = self.visit(node.collection, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{collection}\n{body}'

    @when(Block)
    def visit(self, node: Block, tabs=0):
        if node.body:
            ans = '\t' * tabs + f'\\__Block: {len(node.body)} statements'
        else:
            ans = '\t' * tabs + f'\\__Block: {0} statements'
        print(type(node.body))
        body = ''.join(self.visit(node.body, tabs + 1))
        return f'{ans}\n{body}'

    @when(Let)
    def visit(self, node: Let, tabs=0):
        ans = '\t' * tabs + f'\\__Let: {node.name} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'


    @when(Conditional)
    def visit(self, node: Conditional, tabs=0):
        ans = '\t' * tabs + f'\\__Conditional: if <expr> -> <body>'
        if_expr = self.visit(node.if_expr, tabs + 1)
        if_body = self.visit(node.if_body, tabs + 1)
        else_body = self.visit(node.else_body, tabs + 1)
        return f'{ans}\n{if_expr}\n{if_body}\n{else_body}'

    @when(Branch)
    def visit(self, node: Branch, tabs=0):
        ans = '\t' * tabs + f'\\__Branch: <condition> -> <body>'
        condition = self.visit(node.condition, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{condition}\n{body}'

    @when(Expression)
    def visit(self, node: Expression, tabs=0):
        return f'\t' * tabs + f'\\__Expression: {node.__class__.__name__}'

    @when(Unary)
    def visit(self, node: Unary, tabs=0):
        ans = '\t' * tabs + f'\\__Unary: {node.__class__.__name__} <expr>'
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{right}'

    @when(Binary)
    def visit(self, node: Binary, tabs=0):
        ans = '\t' * tabs + f'\\__Binary: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(Plus)
    def visit(self, node: Plus, tabs=0):
        ans = '\t' * tabs + f'\\__Plus: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(BinaryMinus)
    def visit(self, node: BinaryMinus, tabs=0):
        ans = '\t' * tabs + f'\\__BinaryMinus: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(Star)
    def visit(self, node: Star, tabs=0):
        ans = '\t' * tabs + f'\\__Star: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(Pow)
    def visit(self, node: Pow, tabs=0):
        ans = '\t' * tabs + f'\\__Pow: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(Div)
    def visit(self, node: Div, tabs=0):
        ans = '\t' * tabs + f'\\__Div: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(Mod)
    def visit(self, node: Mod, tabs=0):
        ans = '\t' * tabs + f'\\__Mod: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(Is)
    def visit(self, node: Is, tabs=0):
        ans = '\t' * tabs + f'\\__Is: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(As)
    def visit(self, node: As, tabs=0):
        ans = '\t' * tabs + f'\\__As: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(At)
    def visit(self, node: At, tabs=0):
        ans = '\t' * tabs + f'\\__At: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(DoubleAt)
    def visit(self, node: DoubleAt, tabs=0):
        ans = '\t' * tabs + f'\\__DoubleAt: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(Or)
    def visit(self, node: Or, tabs=0):
        ans = '\t' * tabs + f'\\__Or: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(And)
    def visit(self, node: And, tabs=0):
        ans = '\t' * tabs + f'\\__And: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(GreaterThan)
    def visit(self, node: GreaterThan, tabs=0):
        ans = '\t' * tabs + f'\\__GreaterThan: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(LessThan)
    def visit(self, node: LessThan, tabs=0):
        ans = '\t' * tabs + f'\\__LessThan: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(GreaterEqual)
    def visit(self, node: GreaterEqual, tabs=0):
        ans = '\t' * tabs + f'\\__GreaterEqual: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(LessEqual)
    def visit(self, node: LessEqual, tabs=0):
        ans = '\t' * tabs + f'\\__LessEqual: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(NotEqual)
    def visit(self, node: NotEqual, tabs=0):
        ans = '\t' * tabs + f'\\__NotEqual: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(CompareEqual)
    def visit(self, node: CompareEqual, tabs=0):
        ans = '\t' * tabs + f'\\__CompareEqual: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(Not)
    def visit(self, node: Not, tabs=0):
        ans = '\t' * tabs + f'\\__Not: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @when(UnaryMinus)
    def visit(self, node: UnaryMinus, tabs=0):
        ans = '\t' * tabs + f'\\__UnaryMinus: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @when(Atom)
    def visit(self, node:Atom, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'

    @when(Call)
    def visit(self, node:Call, tabs=0):
        ans = '\t' * tabs + f'\\__Call: <obj>.{node.idx}(<args>)'
        args = '<empty>'
        if node.args:
            args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{args}'

    
    @when(Str)
    def visit(self, node: Str, tabs=0):
        return '\t' * tabs + f'\\__Str: {node.lex}'
    
    @when(Bool)
    def visit(self, node: Bool, tabs=0):
        return '\t' * tabs + f'\\__Bool: {node.lex}'
    
    @when(Invoke)
    def visit(self, node: Invoke, tabs=0):
        ans = '\t' * tabs + f'\\__Invoke: <container>.{node.lex}'
        container = self.visit(node.container, tabs + 1)
        return f'{ans}\n{container}'
    
    @when(Vector)
    def visit(self, node: Vector, tabs=0):
        ans = '\t' * tabs + f'\\__Vector: <values> with length {node.len}'
        values = ''.join(self.visit(value, tabs + 1) for value in node.lex)
        return f'{ans}\n{values}'
    
    @when(VectorComprehension)
    def visit(self, node: VectorComprehension, tabs=0):
        ans = '\t' * tabs + f'\\__VectorComprehension: <values> with length {node.len} and operation <operation>'
        # values = ''.join(self.visit(value, tabs + 1) for value in node.lex)
        values = "TODO: FIx later"
        operation = self.visit(node.operation, tabs + 1)
        return f'{ans}\n{values}\n{operation}'
    
    @when(Var)
    def visit(self, node: Var, tabs=0):
        return '\t' * tabs + f'\\__Var: {node.lex}'


    @when(TypeCreation)
    def visit(self, node: TypeCreation, tabs=0):
        return '\t' * tabs + f'\\__TypeCreation: <type>'

 
    @when(Pi)
    def visit(self, node:Pi, tabs=0):
        return '\t' * tabs + f'\\__Pi'

    @when(E)
    def visit(self, node:E, tabs=0):
        return '\t' * tabs + f'\\__E'

    @when(Indexing)
    def visit(self, node:Indexing, tabs=0):
        ans = '\t' * tabs + f'\\__Indexing: {node.lex}[<index>]'
        index = self.visit(node.index, tabs + 1)
        return f'{ans}\n{index}'

    @when(Sin)
    def visit(self, node:Sin, tabs=0):
        ans = '\t' * tabs + f'\\__Sin:(<args>)'
        # args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        args = '\t'*tabs + f'<no-args>'
        if node.args:
            for arg in node.args: #TODO parche
                args += str(self.visit(arg,tabs + 1))
        return f'{ans}\n{args}'

    @when(Cos)
    def visit(self, node:Cos, tabs=0):
        ans = '\t' * tabs + f'\\__Cos:(<args>)'
        # args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        args = '\t'*tabs + f'<no-args>'
        if node.args:
            for arg in node.args: #TODO parche
                args += str(self.visit(arg,tabs + 1))
        return f'{ans}\n{args}'
    

    @when(Rand)
    def visit(self, node:Rand, tabs=0):
        ans = '\t' * tabs + f'\\__Rand:(<args>)'
        # args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        args = '\t'*tabs + f'<no-args>'
        if node.args:
            for arg in node.args: #TODO parche
                args += str(self.visit(arg,tabs + 1))
        return f'{ans}\n{args}'

    @when(Exp)
    def visit(self, node:Exp, tabs=0):
        ans = '\t' * tabs + f'\\__Exp:(<args>)'
        # args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        args = '\t'*tabs + f'<no-args>'
        if node.args:
            for arg in node.args: #TODO parche
                args += str(self.visit(arg,tabs + 1))
        return f'{ans}\n{args}'

    @when(Log)
    def visit(self, node:Log, tabs=0):
        ans = '\t' * tabs + f'\\__Log:(<args>)'
        # args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        args = '\t'*tabs + f'<no-args>'
        if node.args:
            for arg in node.args: #TODO parche
                args += str(self.visit(arg,tabs + 1))
        return f'{ans}\n{args}'

    @when(Sqrt)
    def visit(self, node:Sqrt, tabs=0):
        ans = '\t' * tabs + f'\\__Sqrt:(<args>)'
        # args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        args = '\t'*tabs + f'<no-args>'
        if node.args:
            for arg in node.args: #TODO parche
                args += str(self.visit(arg,tabs + 1))
        return f'{ans}\n{args}'


    @when(Range)
    def visit(self, node:Range, tabs=0):
        ans = '\t' * tabs + f'\\__Range:(<args>)'
        # args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        args = '\t'*tabs + f'<no-args>'
        if node.args:
            for arg in node.args: #TODO parche
                args += str(self.visit(arg,tabs + 1))
        return f'{ans}\n{args}'

    @when(While)
    def visit(self, node:While, tabs=0):
        ans = '\t' * tabs + f'\\__While: <expr> -> <body>'
        expr = self.visit(node.stop, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{expr}\n{body}'

    @when(Self)
    def visit(self, node:Self, tabs=0):
        return '\t' * tabs + f'\\__Self'

    @when(Property)
    def visit(self, node:Property, tabs=0):
        ans = '\t' * tabs + f'\\__Property: {node.name} = <expr>'
        expr = self.visit(node.body, tabs + 1)
        return f'{ans}\n{expr}'

    @when(CreateInstance)
    def visit(self, node: CreateInstance, tabs=0):
        ans = '\t' * tabs + f'\\__CreateInstance: new {node.type}(<args>)'
        args = '<no-params>'
        if node.params:
            args = ''.join(self.visit(arg, tabs + 1) for arg in node.params)
        return f'{ans}\n{args}' 
