from abc import ABC, abstractmethod
from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError, Type
from tools import visitor
from tools.semantic import Scope
from typing import Union

class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs=0):
        pass

    @visitor.when(Program)
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

    @visitor.when(Statement)
    def visit(self, node: Statement, tabs=0):
        return '\t' * tabs + f'\\__Statement: {node.__class__.__name__}'

    # @visitor.when(LetList)
    # def visit(self, node: LetList, tabs=0):
    #     for child in node.children:
    #         return f'{self.visit(child, tabs)}'

    @visitor.when(Assign)
    def visit(self, node:Assign, tabs=0):
        ans = '\t' * tabs + f'\\__Assign: {node.lex} = <expr>'
        expr = self.visit(node.body, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(Function)
    def visit(self, node: Function, tabs=0):
        params = "<no_params>"
        if node.params:
            params = ', '.join(f'{name}' for name in node.params)
        ans = '\t' * tabs + f'\\__Function: {node.name}({params}) -> <body>'
        body = ''.join(self.visit(node.body, tabs + 1))
        return f'{ans}\n{body}'

    @visitor.when(Protocol)
    def visit(self, node:Protocol, tabs=0):
        ans = '\t' * tabs + f'\\__Protocol: {node.name}'
        body = ''.join(self.visit(child, tabs + 1) for child in node.body)
        return f'{ans}\n{body}'

    @visitor.when(TypeDef)
    def visit(self, node:TypeDef, tabs=0):
        if node.inheritance is None:
            ans = '\t' * tabs + f'\\__TypeDef: {node.name}'
        else:
            ans = '\t' * tabs + f'\\__TypeDef: {node.name} inherits from {node.inheritance}'#TODO: Check this
        body = '<empty_body>'
        if node.body:
            body = '\n'.join(self.visit(child, tabs + 1) for child in node.body)
        return f'{ans}\n{body}'

    @visitor.when(Print)
    def visit(self, node:Print, tabs=0):
        ans = '\t' * tabs + f'\\__Print:(<args>)'
        # args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        args = ''
        for arg in node.args: #TODO parche
            if not arg:
                continue
            args += str(self.visit(arg,tabs + 1))
        return f'{ans}\n{args}'

    @visitor.when(Number)
    def visit(self, node: Number, tabs=0):
        return '\t' * tabs + f'\\__Number: {node.lex}'

    @visitor.when(For)
    def visit(self, node:For, tabs=0):
        ans = '\t' * tabs + f'\\__For: {node.item} in <collection> -> <body>'
        collection = self.visit(node.collection, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{collection}\n{body}'

    @visitor.when(Block)
    def visit(self, node: Block, tabs=0):
        if node.body:
            ans = '\t' * tabs + f'\\__Block: {len(node.body)} statements'
        else:
            ans = '\t' * tabs + f'\\__Block: {0} statements'
        print(type(node.body))
        body = ''.join(self.visit(node.body, tabs + 1))
        return f'{ans}\n{body}'

    @visitor.when(Let)
    def visit(self, node: Let, tabs=0):
        ans = '\t' * tabs + f'\\__Let: {node.name} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(Conditional)
    def visit(self, node: Conditional, tabs=0):
        ans = '\t' * tabs + f'\\__Conditional: if <expr> -> <body>'
        if_expr = self.visit(node.if_expr, tabs + 1)
        if_body = self.visit(node.if_body, tabs + 1)
        else_body = self.visit(node.else_body, tabs + 1)
        return f'{ans}\n{if_expr}\n{if_body}\n{else_body}'

    @visitor.when(Branch)
    def visit(self, node: Branch, tabs=0):
        ans = '\t' * tabs + f'\\__Branch: <condition> -> <body>'
        condition = self.visit(node.condition, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{condition}\n{body}'

    @visitor.when(Expression)
    def visit(self, node: Expression, tabs=0):
        return f'\t' * tabs + f'\\__Expression: {node.__class__.__name__}'

    @visitor.when(Unary)
    def visit(self, node: Unary, tabs=0):
        ans = '\t' * tabs + f'\\__Unary: {node.__class__.__name__} <expr>'
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{right}'

    @visitor.when(Binary)
    def visit(self, node: Binary, tabs=0):
        ans = '\t' * tabs + f'\\__Binary: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(Plus)
    def visit(self, node: Plus, tabs=0):
        ans = '\t' * tabs + f'\\__Plus: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(BinaryMinus)
    def visit(self, node: BinaryMinus, tabs=0):
        ans = '\t' * tabs + f'\\__BinaryMinus: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(Star)
    def visit(self, node: Star, tabs=0):
        ans = '\t' * tabs + f'\\__Star: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(Pow)
    def visit(self, node: Pow, tabs=0):
        ans = '\t' * tabs + f'\\__Pow: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(Div)
    def visit(self, node: Div, tabs=0):
        ans = '\t' * tabs + f'\\__Div: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(Mod)
    def visit(self, node: Mod, tabs=0):
        ans = '\t' * tabs + f'\\__Mod: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(Is)
    def visit(self, node: Is, tabs=0):
        ans = '\t' * tabs + f'\\__Is: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(As)
    def visit(self, node: As, tabs=0):
        ans = '\t' * tabs + f'\\__As: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(At)
    def visit(self, node: At, tabs=0):
        ans = '\t' * tabs + f'\\__At: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(DoubleAt)
    def visit(self, node: DoubleAt, tabs=0):
        ans = '\t' * tabs + f'\\__DoubleAt: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(Or)
    def visit(self, node: Or, tabs=0):
        ans = '\t' * tabs + f'\\__Or: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(And)
    def visit(self, node: And, tabs=0):
        ans = '\t' * tabs + f'\\__And: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(GreaterThan)
    def visit(self, node: GreaterThan, tabs=0):
        ans = '\t' * tabs + f'\\__GreaterThan: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(LessThan)
    def visit(self, node: LessThan, tabs=0):
        ans = '\t' * tabs + f'\\__LessThan: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(GreaterEqual)
    def visit(self, node: GreaterEqual, tabs=0):
        ans = '\t' * tabs + f'\\__GreaterEqual: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(LessEqual)
    def visit(self, node: LessEqual, tabs=0):
        ans = '\t' * tabs + f'\\__LessEqual: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(NotEqual)
    def visit(self, node: NotEqual, tabs=0):
        ans = '\t' * tabs + f'\\__NotEqual: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(CompareEqual)
    def visit(self, node: CompareEqual, tabs=0):
        ans = '\t' * tabs + f'\\__CompareEqual: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(Not)
    def visit(self, node: Not, tabs=0):
        ans = '\t' * tabs + f'\\__Not: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(UnaryMinus)
    def visit(self, node: UnaryMinus, tabs=0):
        ans = '\t' * tabs + f'\\__UnaryMinus: <expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(Atom)
    def visit(self, node:Atom, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'

    @visitor.when(Call)
    def visit(self, node:Call, tabs=0):
        ans = '\t' * tabs + f'\\__Call: <obj>.{node.idx}(<args>)'
        args = '<empty>'
        if node.args:
            args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{args}'

    @visitor.when(Str)
    def visit(self, node: Str, tabs=0):
        return '\t' * tabs + f'\\__Str: {node.lex}'
    
    @visitor.when(Bool)
    def visit(self, node: Bool, tabs=0):
        return '\t' * tabs + f'\\__Bool: {node.lex}'
    
    @visitor.when(Invoke)
    def visit(self, node: Invoke, tabs=0):
        ans = '\t' * tabs + f'\\__Invoke: <container>.{node.lex}'
        container = self.visit(node.container, tabs + 1)
        return f'{ans}\n{container}'
    
    @visitor.when(Vector)
    def visit(self, node: Vector, tabs=0):
        ans = '\t' * tabs + f'\\__Vector: <values> with length {node.len}'
        values = ''.join(self.visit(value, tabs + 1) for value in node.lex)
        return f'{ans}\n{values}'
    
    @visitor.when(VectorComprehension)
    def visit(self, node: VectorComprehension, tabs=0):
        ans = '\t' * tabs + f'\\__VectorComprehension: <values> with length {node.len} and operation <operation>'
        # values = ''.join(self.visit(value, tabs + 1) for value in node.lex)
        values = "TODO: FIx later"
        operation = self.visit(node.operation, tabs + 1)
        return f'{ans}\n{values}\n{operation}'
    
    @visitor.when(Var)
    def visit(self, node: Var, tabs=0):
        return '\t' * tabs + f'\\__Var: {node.lex}'

    @visitor.when(TypeCreation)
    def visit(self, node: TypeCreation, tabs=0):
        return '\t' * tabs + f'\\__TypeCreation: <type>'

    @visitor.when(Pi)
    def visit(self, node:Pi, tabs=0):
        return '\t' * tabs + f'\\__Pi'

    @visitor.when(E)
    def visit(self, node:E, tabs=0):
        return '\t' * tabs + f'\\__E'

    @visitor.when(Indexing)
    def visit(self, node:Indexing, tabs=0):
        ans = '\t' * tabs + f'\\__Indexing: {node.lex}[<index>]'
        index = self.visit(node.index, tabs + 1)
        return f'{ans}\n{index}'

    @visitor.when(Sin)
    def visit(self, node:Sin, tabs=0):
        ans = '\t' * tabs + f'\\__Sin:(<args>)'
        # args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        args = '\t'*tabs + f'<no-args>'
        if node.args:
            for arg in node.args: #TODO parche
                args += str(self.visit(arg,tabs + 1))
        return f'{ans}\n{args}'

    @visitor.when(Cos)
    def visit(self, node:Cos, tabs=0):
        ans = '\t' * tabs + f'\\__Cos:(<args>)'
        # args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        args = '\t'*tabs + f'<no-args>'
        if node.args:
            for arg in node.args: #TODO parche
                args += str(self.visit(arg,tabs + 1))
        return f'{ans}\n{args}'
    
    @visitor.when(Rand)
    def visit(self, node:Rand, tabs=0):
        ans = '\t' * tabs + f'\\__Rand:(<args>)'
        # args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        args = '\t'*tabs + f'<no-args>'
        if node.args:
            for arg in node.args: #TODO parche
                args += str(self.visit(arg,tabs + 1))
        return f'{ans}\n{args}'

    @visitor.when(Exp)
    def visit(self, node:Exp, tabs=0):
        ans = '\t' * tabs + f'\\__Exp:(<args>)'
        # args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        args = '\t'*tabs + f'<no-args>'
        if node.args:
            for arg in node.args: #TODO parche
                args += str(self.visit(arg,tabs + 1))
        return f'{ans}\n{args}'

    @visitor.when(Log)
    def visit(self, node:Log, tabs=0):
        ans = '\t' * tabs + f'\\__Log:(<args>)'
        # args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        args = '\t'*tabs + f'<no-args>'
        if node.args:
            for arg in node.args: #TODO parche
                args += str(self.visit(arg,tabs + 1))
        return f'{ans}\n{args}'

    @visitor.when(Sqrt)
    def visit(self, node:Sqrt, tabs=0):
        ans = '\t' * tabs + f'\\__Sqrt:(<args>)'
        # args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        args = '\t'*tabs + f'<no-args>'
        if node.args:
            for arg in node.args: #TODO parche
                args += str(self.visit(arg,tabs + 1))
        return f'{ans}\n{args}'

    @visitor.when(Range)
    def visit(self, node:Range, tabs=0):
        ans = '\t' * tabs + f'\\__Range:(<args>)'
        # args = ''.join(self.visit(arg, tabs + 1) for arg in node.args)
        args = '\t'*tabs + f'<no-args>'
        if node.args:
            for arg in node.args: #TODO parche
                args += str(self.visit(arg,tabs + 1))
        return f'{ans}\n{args}'

    @visitor.when(While)
    def visit(self, node:While, tabs=0):
        ans = '\t' * tabs + f'\\__While: <expr> -> <body>'
        expr = self.visit(node.stop, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{expr}\n{body}'

    @visitor.when(Self)
    def visit(self, node:Self, tabs=0):
        return '\t' * tabs + f'\\__Self'

    @visitor.when(Property)
    def visit(self, node:Property, tabs=0):
        ans = '\t' * tabs + f'\\__Property: {node.name} = <expr>'
        expr = self.visit(node.body, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(CreateInstance)
    def visit(self, node: CreateInstance, tabs=0):
        ans = '\t' * tabs + f'\\__CreateInstance: new {node.type}(<args>)'
        args = '<no-params>'
        if node.params:
            args = ''.join(self.visit(arg, tabs + 1) for arg in node.params)
        return f'{ans}\n{args}' 

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

class TypeBuilder(object):
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
        type_info = ctx.get_type(node.name)
        try:
            if node.inheritance:
                parent = ctx.get_type(node.inheritance)
                type_info.set_parent(parent)
        except SemanticError as se:
            self.errors.append(se.text)
        
        if node.args:
            for argument in node.args:
                try:
                    type_info.define_argument(argument[0], ctx.get_type(argument[1]))
                except SemanticError as se:
                    self.errors.append(se.text)
        
        if node.body:
            for stat in node.body:
                self.visit(stat, ctx, type_info)

    @visitor.when(Protocol)
    def visit(self, node: Protocol, ctx: Context):
        protocol_info = ctx.get_protocol(node.name)
        try:
            if node.extension:
                parent = ctx.get_protocol(node.extension)
                protocol_info.set_parent(parent)
        except SemanticError as se:
            self.errors.append(se.text)

        if node.body:
            for stat in node.body:
                self.visit(stat, ctx, protocol_info)

    @visitor.when(Property)
    def visit(self, node: Property, ctx: Context, current_type: Union[Type, Protocol]):
        try:
            current_type.define_attribute(node.name, ctx.get_type(node.type))
        except SemanticError as se:
            self.errors.append(se.text)
                
    @visitor.when(Function)
    def visit(self, node: Function, ctx: Context, current_type: Union[Type, Protocol]):
        try:
            # Divide the params into names and types from node.params: List[Tuple[str, str]
            param_names, param_types = [], []
            return_type = None
            if node.params:
                param_names, param_types = zip(*node.params)
            if node.type:
                return_type = ctx.get_type(node.type)
            current_type.define_method(node.name, param_names, param_types, return_type)
        except SemanticError as se:
            self.errors.append(se.text)

class GlobalScopeBuilder(object):
    def __init__(self, context: Context, errors=[]):
        self.context = context
        self.errors = errors
        self.global_scope = Scope()
        self.global_scope.define_function('print', ['msg'], self.context.get_type('String').name)
        self.global_scope.define_function('sin', ['x'], self.context.get_type('Number').name)
        self.global_scope.define_function('cos', ['x'], self.context.get_type('Number').name)
        
        self.global_scope.define_variable('Pi', self.context.get_type('Number').name)
        self.global_scope.define_variable('E', self.context.get_type('Number').name)
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Program)
    def visit(self, node: Program):
        for child in node.statements:
            self.visit(child, self.global_scope)

        return self.errors

    @visitor.when(Function)
    def visit(self, node: Function, scope: Scope):
        try:
            scope.define_function(node.name, [p for p in node.params], node.type)
        except SemanticError as se:
            self.errors.append(se.text)

        new_scope = scope.create_child_scope()

        for param_name, param_type in node.params:
            try:
                new_scope.define_variable(param_name, param_type)
            except SemanticError as se:
                self.errors.append(se.text)

        self.visit(node.body, new_scope)

    @visitor.when(Block)
    def visit(self, node: Block, scope: Scope):
        for child in node.body:
            self.visit(child, scope)

    @visitor.when(Binary)
    def visit(self, node: Binary, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

    @visitor.when(Call)
    def visit(self, node: Call, scope: Scope):
        if not scope.get_local_function_info(node.idx, len(node.args)):
            self.errors.append(f'Function {node.idx} not defined')

        for arg in node.args:
            self.visit(arg, scope)

    @visitor.when(Var)
    def visit(self, node: Var, scope: Scope):
        if not scope.get_local_variable(node.lex):
            self.errors.append(f'Variable {node.lex} not defined')

    @visitor.when(LetList)
    def visit(self, node: LetList, scope: Scope):
        self.visit(node.child, scope)

    @visitor.when(Let)
    def visit(self, node: Let, scope: Scope):
        new_scope = scope.create_child_scope()
        try:
            new_scope.define_variable(node.name, node.type)
        except SemanticError as se:
            self.errors.append(se.text)

        self.visit(node.scope, new_scope)

# class SemanticChecker(object):
#     def __init__(self, context: Context, errors=[]):
#         self.errors = errors

#     @visitor.on("node")
#     def visit(self, node, scope):
#         pass

#     @visitor.when(Program)
#     def visit(self, node: Program, scope: Scope=None):
#         for child in node.statements:
#             self.visit(child, scope)
#         return self.errors

#     @visitor.when(VarDeclarationNode)
#     def visit(self, node, scope):
#         if not scope.define_variable(node.id):
#             self.errors.append(f"Variable {node.idx} already defined")
#         self.visit(node.expr, scope)

#     @visitor.when(FuncDeclarationNode)
#     def visit(self, node, scope):
#         if not scope.define_function(node.id, [p for p in node.params]):
#             self.errors.append(
#                 f"Function {node.idx} with {len(node.params)} parameters already defined"
#             )
#         child_scope = scope.create_child_scope()
#         for param in node.params:
#             child_scope.define_variable(param)
#         self.visit(node.body, child_scope)

#     @visitor.when(PrintNode)
#     def visit(self, node, scope):
#         self.visit(node.expr, scope)

#     @visitor.when(ConstantNumNode)
#     def visit(self, node, scope):
#         return self.errors

#     @visitor.when(VariableNode)
#     def visit(self, node, scope):
#         if not scope.is_var_defined(node.lex):
#             self.errors.append(f"Variable {node.lex} not defined")
#         return self.errors

#     @visitor.when(CallNode)
#     def visit(self, node, scope):
#         if not scope.is_func_defined(node.lex, len(node.args)):
#             self.errors.append(
#                 f"Function {node.lex} with {len(node.args)} parameters not defined"
#             )
#         for arg in node.args:
#             self.visit(arg, scope)
#         return self.errors

#     @visitor.when(BinaryNode)
#     def visit(self, node, scope):
#         self.visit(node.left, scope)
#         self.visit(node.right, scope)
#         return self.errors

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

class TypeChecker(object):
    def __init__(self, context: Context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors
        
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(Program)
    def visit(self, node: Program, scope: Scope = None):
        if not scope:
            scope = Scope()
        for child in node.statements:
            self.visit(child, scope)
        return scope

    @visitor.when(Function)
    def visit(self, node: Function, scope: Scope):
        
        try:
            if node.type:
                return_type = self.context.get_type(node.type)
                scope.define_function(node.name, node.params, return_type)
        except SemanticError as se:
            self.errors.append(se.text)

        body_scope = scope.create_child_scope()
        for i in range(0,len(node.params)):
            body_scope.define_variable(node.params[i][0], node.params[i][1])
            
        # Verificar los parámetros de la función
        for param_name, param_type in node.params:
            # Asegurarse de que el tipo del parámetro esté definido en el contexto
            try:
                declared_type = self.context.get_type(param_type)
            except SemanticError as se:
                self.errors.append(se.text)
                continue
    
    
        # Verificar el cuerpo de la función
        body_type = self.visit(node.body, body_scope)

        declared_return_type = None
        # Verificar que el tipo de retorno de la función sea compatible con el tipo declarado
        if node.type is not None:
            declared_return_type = self.context.get_type(node.type)
            if not body_type.conforms(declared_return_type):
                self.errors.append(f'TypeError: Return type {body_type.name} does not conform to declared return type {node.type}')
            
    
        # Devolver el tipo de retorno de la función
        return declared_return_type
    
    
    @visitor.when(Call)
    def visit(self, node: Call, scope: Scope):
        # Obtener la función llamada por su nombre
        try:
            function = scope.get_local_function_info(node.lex, len(node.args))
        except SemanticError as se:
            self.errors.append(se.text)
            return self.context.get_type('ErrorType') # Retornar un tipo de error como marcador de posición
    
        # Verificar que el número de argumentos sea correcto
        if len(node.args) != len(function.params):
            self.errors.append(f'TypeError: Incorrect number of arguments for function {node.idx}')
            return self.context.get_type('ErrorType') # Retornar un tipo de error como marcador de posición
    
        # Verificar que los tipos de los argumentos sean compatibles con los parámetros de la función
        for arg, param_type in zip(node.args, function.params):
            # arg_type = self.visit(arg, scope)
            if arg.lex in ["Pi","E"]: #TODO arreglar
                arg_type = self.context.get_type("Number")
            else:
                arg_type = self.context.get_type(scope.get_local_variable(arg.lex))
            
            param_type = self.context.get_type(param_type[1])
            if not arg_type.conforms(param_type):
                self.errors.append(f'TypeError: Argument type {arg_type.name} does not conform to parameter type {param_type.name} in function call {node.idx}')
    
        # Devolver el tipo de retorno de la función
        return function.function_type
    
    @visitor.when(Block)
    def visit(self, node: Block, scope: Scope):
        # Crear un nuevo alcance para el bloque
        # block_scope = scope.create_child_scope()
    
        # Recorrer cada uno de los nodos hijos y realizar el chequeo de tipos
        for child in node.body:
            type = self.visit(child, scope)
    
        return type
    
    @visitor.when(LetList)
    def visit(self, node: Let, scope: Scope):
        return self.visit(node.child, scope)
    
    @visitor.when(Let)
    def visit(self, node: Let, scope: Scope):
        
        child_scope = scope.create_child_scope()
        # Realizar el chequeo de tipos para la expresión asignada
        type_expr = self.visit(node.expr, scope)
        
        # Verificar que el tipo de la expresión sea compatible con el tipo declarado
        if node.type is not None:
            try:
                declared_type = self.context.get_type(node.type)
            except:
                declared_type = self.context.get_protocol(node.type)
                
            if not type_expr.conforms(declared_type):
                self.errors.append(f'TypeError: Type {type_expr.name} does not conform to {node.type}')
        
        # Agregar la variable al alcance actual con su tipo
        child_scope.define_variable(node.name, node.type)
        self.visit(node.scope, child_scope)
        return child_scope

    @visitor.when(Plus)
    def visit(self, node: Plus, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es el tipo de los operandos
        return left_type
    
    @visitor.when(BinaryMinus)
    def visit(self, node: BinaryMinus, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es el tipo de los operandos
        return left_type
    
    @visitor.when(Star)
    def visit(self, node: Star, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es el tipo de los operandos
        return left_type
    
    @visitor.when(Pow)
    def visit(self, node: Pow, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es el tipo de los operandos
        return left_type
    
    @visitor.when(Div)
    def visit(self, node: Div, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es el tipo de los operandos
        return left_type
    
    @visitor.when(Mod)
    def visit(self, node: Mod, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es el tipo de los operandos
        return left_type
    
    @visitor.when(Is)
    def visit(self, node: Is, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es el tipo de los operandos
        return left_type
    
    @visitor.when(As)
    def visit(self, node: As, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es el tipo de los operandos
        return left_type
    
    @visitor.when(At)
    def visit(self, node: At, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es el tipo de los operandos
        return left_type
    
    @visitor.when(DoubleAt)
    def visit(self, node: DoubleAt, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es el tipo de los operandos
        return left_type
    
    @visitor.when(Or)
    def visit(self, node: Or, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es el tipo de los operandos
        return left_type
    
    @visitor.when(And)
    def visit(self, node: And, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es el tipo de los operandos
        return left_type
    
    @visitor.when(GreaterThan)
    def visit(self, node: GreaterThan, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of GreaterThan operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es Bool
        return self.context.get_type('Boolean')
    
    
    @visitor.when(LessThan)
    def visit(self, node: LessThan, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of GreaterThan operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es Bool
        return self.context.get_type('Boolean')
    
    @visitor.when(GreaterEqual)
    def visit(self, node: GreaterEqual, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of GreaterThan operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es Bool
        return self.context.get_type('Boolean')
    
    @visitor.when(LessEqual)
    def visit(self, node: LessEqual, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of GreaterThan operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es Bool
        return self.context.get_type('Boolean')
    
    @visitor.when(NotEqual)
    def visit(self, node: NotEqual, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of GreaterThan operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es Bool
        return self.context.get_type('Boolean')
    
    @visitor.when(CompareEqual)
    def visit(self, node: CompareEqual, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of GreaterThan operation must be of the same type')
    
        # Devolver el tipo de la expresión, que es Bool
        return self.context.get_type('Boolean')
    
    @visitor.when(Not)
    def visit(self, node: Not, scope: Scope):
        # Verificar que el operando de la operación sea del tipo correcto
        operand_type = self.visit(node.right, scope)
        if not operand_type.conforms(self.context.get_type('Bool')):
            self.errors.append(f'TypeError: Operand of Not operation must be of type Bool')
    
        # Devolver el tipo de la expresión, que es Bool
        return self.context.get_type('Boolean')
    
    @visitor.when(Print)
    def visit(self, node: Print, scope: Scope):
        # Verificar que los argumentos de la función print sean del tipo correcto
        for arg in node.args:
            arg_type = self.visit(arg, scope)
          
        return self.context.get_type('Object')
    
    @visitor.when(Conditional)
    def visit(self, node: Conditional, scope: Scope):
        # Verificar que el tipo de la expresión condicional sea Bool
        if_expr_type = self.visit(node.if_expr, scope)
        if not if_expr_type.conforms(self.context.get_type('Boolean')):
            self.errors.append(f'TypeError: Conditional expression must be of type Bool')
    
        # Realizar el chequeo de tipos para el cuerpo del if
        self.visit(node.if_body, scope)
    
        # Realizar el chequeo de tipos para el cuerpo del else
        self.visit(node.else_body, scope)
    
        # Si hay ramas adicionales, realizar el chequeo de tipos para cada una de ellas
        if node.branches:
            for branch in node.branches:
                self.visit(branch, scope)
    
        return self.context.get_type('Object')
    
    @visitor.when(For)
    def visit(self, node: For, scope: Scope):
        
        body_scope = scope.create_child_scope()
        # Verificar que el tipo de la colección sea Vector
        collection_type = self.visit(node.collection, scope)
        if not collection_type.conforms(self.context.get_type('Vector')):
            self.errors.append(f'TypeError: For loop collection must be of type Vector')
    
        body_scope.define_variable(node.item.name, node.item.type)
        # Realizar el chequeo de tipos para el cuerpo del bucle
        self.visit(node.body, body_scope)
    
        return self.context.get_type('Object')
    
    @visitor.when(While)
    def visit(self, node: While, scope: Scope):
        # Verificar que el tipo de la expresión de parada sea Bool
        stop_expr_type = self.visit(node.stop, scope)
        if not stop_expr_type.conforms(self.context.get_type('Boolean')):
            self.errors.append(f'TypeError: While loop stop condition must be of type Bool')
    
        # Realizar el chequeo de tipos para el cuerpo del bucle
        self.visit(node.body, scope)
    
        return self.context.get_type('Object')
    
    @visitor.when(Var)
    def visit(self, node: Var, scope: Scope):
        # Buscar el tipo de la variable en el alcance actual
        try:
            var_info = scope.get_local_variable(node.lex)
            return self.context.get_type(var_info.var_type)
        except SemanticError as se:
            self.errors.append(se.text)
           

    @visitor.when(Str)
    def visit(self, node: Number, scope: Scope):
        # El tipo de un Number es predefinido como "Number"
        return self.context.get_type('String')
    
    @visitor.when(Number)
    def visit(self, node: Number, scope: Scope):
        # El tipo de un Number es predefinido como "Number"
        return self.context.get_type('Number')
    
    @visitor.when(Bool)
    def visit(self, node: Number, scope: Scope):
        # El tipo de un Number es predefinido como "Number"
        return self.context.get_type('Bool')
    
    @visitor.when(Vector)
    def visit(self, node: Vector, scope: Scope):
        # Verificar que los valores del vector sean del tipo correcto
        for value in node.lex:
            value_type = self.visit(value, scope)
            # Aquí asumimos que el tipo correcto para los valores del vector es Number
            if not value_type.conforms(self.context.get_type('Number')):
                self.errors.append(f'TypeError: Vector values must be of type Number')
    
        # Verificar que la longitud del vector sea un número entero
        if not isinstance(node.len, int):
            self.errors.append(f'TypeError: Vector length must be an integer')
    
        # Devolver el tipo de la expresión vector, que es Vector
        return self.context.get_type('Vector')
    
    @visitor.when(Sin)
    def visit(self, node: Sin, scope: Scope):
        # Verificar que el argumento de la función sin es del tipo correcto
        # for arg in node.args:
        #     type_arg = scope.get_local_variable(arg.lex) # TODO DEVOLVER EL TIPO DE LA VAR DEL SCOPE
        #     if not type_arg.conforms(self.context.get_type('Number')):
        #         self.errors.append(f'TypeError: Argument of sin function must be of type Number')
        # Devolver el tipo de la función sin, que es Number
        return self.context.get_type('Number')
    
    @visitor.when(Cos)
    def visit(self, node: Cos, scope: Scope):
        # Verificar que el argumento de la función cos es del tipo correcto
        # for arg in node.args:
        #     type_arg = self.visit(arg, scope)
        #     if not type_arg.conforms(self.context.get_type('Number')): #TODO LO MISMO
        #         self.errors.append(f'TypeError: Argument of cos function must be of type Number')
        # Devolver el tipo de la función cos, que es Number
        return self.context.get_type('Number')
    
    @visitor.when(Log)
    def visit(self, node: Log, scope: Scope):
        # Verificar que los argumentos de la función log sean del tipo correcto
        for arg in node.args:
            arg_type = self.visit(arg, scope)
            if not arg_type.conforms(self.context.get_type('Number')):
                self.errors.append(f'TypeError: Argument of log function must be of type Number')
        # Devolver el tipo de la función log, que es Number
        return self.context.get_type('Number')
    
    @visitor.when(Sqrt)
    def visit(self, node: Sqrt, scope: Scope):
        # Verificar que los argumentos de la función sqrt sean del tipo correcto
        for arg in node.args:
            arg_type = self.visit(arg, scope)
            if not arg_type.conforms(self.context.get_type('Number')):
                self.errors.append(f'TypeError: Argument of sqrt function must be of type Number')
        # Devolver el tipo de la función sqrt, que es Number
        return self.context.get_type('Number')
    
    @visitor.when(Range)
    def visit(self, node: Range, scope: Scope):
        # Verificar que los argumentos de la función range sean del tipo correcto
        for arg in node.args:
            arg_type = self.visit(arg, scope)
            if not arg_type.conforms(self.context.get_type('Number')):
                self.errors.append(f'TypeError: Argument of range function must be of type Number')
    
        # Devolver el tipo de la expresión range, que es Vector
        return self.context.get_type('Vector')