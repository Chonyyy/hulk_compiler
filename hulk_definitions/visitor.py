from abc import ABC, abstractmethod
from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError, Type
from tools import visitor
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

    @visitor.when(LetList)
    def visit(self, node: LetList, tabs=0):
        for child in node.children:
            return f'{self.visit(child, tabs)}'

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

    @visitor.when(Call)
    def visit(self, node: Call, ctx: Context):
        try:
            obj_type = self.visit(node.obj, ctx)
            if not obj_type.has_method(node.idx):
                self.errors.append(f'TypeError: Type {obj_type.name} does not have method {node.idx}')
            else:
                method = obj_type.get_method(node.idx)
                if len(node.args) != len(method.params):
                    self.errors.append(f'TypeError: Method {node.idx} expects {len(method.params)} arguments, got {len(node.args)}')
                else:
                    for arg, param in zip(node.args, method.params):
                        arg_type = self.visit(arg, ctx)
                        if not arg_type.conforms(param):
                            self.errors.append(f'TypeError: Type {arg_type.name} does not conform to {param}')
        except SemanticError as se:
            self.errors.append(se.text)

    @visitor.when(Invoke)
    def visit(self, node: Invoke, ctx: Context):
        try:
            obj_type = self.visit(node.container, ctx)
            if not obj_type.has_attribute(node.lex):
                self.errors.append(f'TypeError: Type {obj_type.name} does not have attribute {node.lex}')
        except SemanticError as se:
            self.errors.append(se.text)

    @visitor.when(Indexing)
    def visit(self, node: Indexing, ctx: Context):
        try:
            obj_type = self.visit(node.lex, ctx)
            if obj_type.name != 'Vector':
                self.errors.append(f'TypeError: Type {obj_type.name} does not conform to Vector')
            else:
                index_type = self.visit(node.index, ctx)
                if index_type.name != 'Number':
                    self.errors.append(f'TypeError: Type {index_type.name} does not conform to Number')
        except SemanticError as se:
            self.errors.append(se.text)

    @visitor.when(VectorComprehension)
    def visit(self, node: VectorComprehension, ctx: Context):
        try:
            operation_type = self.visit(node.operation, ctx)
            if operation_type.name != 'Number':
                self.errors.append(f'TypeError: Type {operation_type.name} does not conform to Number')
        except SemanticError as se:
            self.errors.append(se.text)

    @visitor.when(Unary)
    def visit(self, node: Unary, ctx: Context):
        return self.visit(node.right, ctx)
    
    @visitor.when(Binary)
    def visit(self, node: Binary, ctx: Context):
        left = self.visit(node.left, ctx)
        right = self.visit(node.right, ctx)
        if left.name != right.name:
            self.errors.append(f'TypeError: Type {left.name} does not conform to {right.name}')
        return left
    
    @visitor.when(Plus)
    def visit(self, node: Plus, ctx: Context):
        return self.visit(node.left, ctx)
    
    @visitor.when(BinaryMinus)
    def visit(self, node: BinaryMinus, ctx: Context):
        return self.visit(node.left, ctx)
    
    @visitor.when(Star)
    def visit(self, node: Star, ctx: Context):
        return self.visit(node.left, ctx)
    
    @visitor.when(Pow)
    def visit(self, node: Pow, ctx: Context):
        return self.visit(node.left, ctx)
    
    @visitor.when(Div)
    def visit(self, node: Div, ctx: Context):
        return self.visit(node.left, ctx)
    
    @visitor.when(Mod)
    def visit(self, node: Mod, ctx: Context):
        return self.visit(node.left, ctx)
    
    @visitor.when(Is)
    def visit(self, node: Is, ctx: Context):
        return self.visit(node.left, ctx)
    
    @visitor.when(As)
    def visit(self, node: As, ctx: Context):
        return self.visit(node.left, ctx)