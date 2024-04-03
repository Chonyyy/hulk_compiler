from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError
from tools import visitor
from tools.semantic import Scope

class GlobalScopeBuilder(object):
    def __init__(self, context: Context, errors=[]):
        self.context = context
        self.errors = errors
        self.global_scope = Scope()
        self.global_scope.define_function('print', ['msg'], self.context.get_type('String').name)
        self.global_scope.define_function('sin', ['x'], self.context.get_type('Number').name)
        self.global_scope.define_function('cos', ['x'], self.context.get_type('Number').name)
        self.global_scope.define_function('range', ['start', 'end'], self.context.get_type('Vector').name)
        self.global_scope.define_function('base', [], 'Dinamic')
        
        self.global_scope.define_variable('Pi', self.context.get_type('Number').name)
        self.global_scope.define_variable('E', self.context.get_type('Number').name)
    
    @visitor.on('node')
    def visit(self, node):
        raise Exception(f'Error: Node {node} not valid for GlobalScopeBuilder')
    
    @visitor.when(Program)
    def visit(self, node: Program):
        for child in node.statements:
            self.visit(child, self.global_scope)

        return self.errors

    @visitor.when(Function)
    def visit(self, node: Function, scope: Scope, defining_type: str = None):
        params = [] if not node.params else node.params
        try:
            scope.define_function(node.name, [p for p in params], node.type)
        except SemanticError as se:
            self.errors.append(se.text)

        new_scope = scope.create_child_scope()
        new_scope.is_function = True
        for param_name, param_type in params:
            try:
                new_scope.define_variable(param_name, param_type)
            except SemanticError as se:
                self.errors.append(se.text)

        self.visit(node.body, new_scope, defining_type)

    @visitor.when(Block)
    def visit(self, node: Block, scope: Scope, defining_type: str = None):
        for child in node.value:
            self.visit(child, scope, defining_type)

    @visitor.when(Binary)
    def visit(self, node: Binary, scope: Scope, defining_type: str = None):
        self.visit(node.left, scope, defining_type)
        self.visit(node.value, scope, defining_type)

    @visitor.when(Call)
    def visit(self, node: Call, scope: Scope, defining_type: str = None):
        if not scope.get_function_info(node.value, len(node.args)):
            self.errors.append(f'Function {node.value} not defined')

        for arg in node.args:
            self.visit(arg, scope, defining_type)

    @visitor.when(Var)
    def visit(self, node: Var, scope: Scope, defining_type: str = None):
        if not scope.get_variable(node.value):
            self.errors.append(f'Variable {node.value} not defined')

    @visitor.when(LetList)
    def visit(self, node: LetList, scope: Scope, defining_type: str = None):
        self.visit(node.child, scope, defining_type)

    @visitor.when(Let)
    def visit(self, node: Let, scope: Scope, defining_type: str = None):
        new_scope = scope.create_child_scope()
        try:
            new_scope.define_variable(node.name, node.type)
        except SemanticError as se:
            self.errors.append(se.text)

        self.visit(node.value, new_scope, defining_type)

    @visitor.when(Conditional)
    def visit(self, node: Conditional, scope: Scope, defining_type: str = None):
        condition_scope = scope.create_child_scope()
        if_scope = scope.create_child_scope()
        else_scope = scope.create_child_scope()
        self.visit(node.if_expr, condition_scope, defining_type)
        self.visit(node.if_body, if_scope, defining_type)
        self.visit(node.else_body, else_scope, defining_type)
    
    @visitor.when(Branch)
    def visit(self, node: Branch, scope: Scope, defining_type: str = None):
        raise Exception('Error: Branch not implemented')
    
    @visitor.when(Not)
    def visit(self, node: Not, scope: Scope, defining_type: str = None):
        raise Exception('Error: Not not implemented')
    
    @visitor.when(UnaryMinus)
    def visit(self, node: UnaryMinus, scope: Scope, defining_type: str = None):
        self.visit(node.value, scope)
    
    @visitor.when(NotEqual)
    def visit(self, node: NotEqual, scope: Scope, defining_type: str = None):
        raise Exception('Error: NotEqual not implemented')
    
    @visitor.when(Number)
    def visit(self, node: Number, scope: Scope, defining_type: str = None):
        pass
    
    @visitor.when(Var)
    def visit(self, node: Var, scope: Scope, defining_type: str = None):
        if scope.get_variable(node.value) is None:
            self.errors.append(SemanticError(f'Variable {node.value} not defined'))
    
    @visitor.when(Vector)
    def visit(self, node: Vector, scope: Scope, defining_type: str = None):
        raise Exception('Error: Vector not implemented')
    
    @visitor.when(VectorComprehension)
    def visit(self, node: VectorComprehension, scope: Scope, defining_type: str = None):
        raise Exception('Error: VectorComprehension not implemented')
    
    @visitor.when(Pi)
    def visit(self, node: Pi, scope: Scope, defining_type: str = None):
        raise Exception('Error: Pi not implemented')
    
    @visitor.when(E)
    def visit(self, node: E, scope: Scope, defining_type: str = None):
        raise Exception('Error: E not implemented')
    
    @visitor.when(Call)
    def visit(self, node: Call, scope: Scope, defining_type: str = None):
        args = node.args if node.args else []
        if scope.get_function_info(node.value, len(args)) is None:
            self.errors.append(SemanticError(f'Function {node.value} not defined'))
    
    @visitor.when(While)
    def visit(self, node: While, scope: Scope, defining_type: str = None):
        new_scope = scope.create_child_scope()
        self.visit(node.stop, scope, defining_type)
        self.visit(node.value, new_scope, defining_type)

    
    @visitor.when(For)
    def visit(self, node: For, scope: Scope, defining_type: str = None):
        new_scope = scope.create_child_scope()
        new_scope.define_variable(node.item, None)
        self.visit(node.collection, scope, defining_type)
        self.visit(node.value, new_scope, defining_type)
    
    @visitor.when(ForVar)
    def visit(self, node: ForVar, scope: Scope, defining_type: str = None):
        raise Exception('Error: ForVar not implemented')
    
    @visitor.when(Invoke)
    def visit(self, node: Invoke, scope: Scope, defining_type: str = None):
        if not (node.value.value and node.value.value == 'self'):
            self.visit(node.value, scope, defining_type)
        try:
            scope.get_variable(node.value.value)
        except SemanticError as se:
            self.errors.append(se.text)

    
    @visitor.when(Indexing)
    def visit(self, node: Indexing, scope: Scope, defining_type: str = None):
        self.visit(node.value, scope, defining_type)
    
    @visitor.when(TypeDef)
    def visit(self, node: TypeDef, scope: Scope):
        new_scope = scope.create_child_scope()
        body = [] if not node.body else node.body
        for item in body:
            self.visit(item, new_scope, node.name)
    
    @visitor.when(Property)
    def visit(self, node: Property, scope: Scope, defining_type: str = None):
        pass
    
    @visitor.when(Assign)
    def visit(self, node: Assign, scope: Scope, defining_type: str = None):
        self.visit(node.value, scope, defining_type)
        self.visit(node.body, scope, defining_type)
    
    @visitor.when(CreateInstance)
    def visit(self, node: CreateInstance, scope: Scope, defining_type: str = None):
        raise Exception('Error: CreateInstance not implemented')
