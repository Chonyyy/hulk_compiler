from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError
from tools import visitor
from tools.semantic import Scope, Type

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
        self.type_w_inheritance = None
        self.type_def = False
        self.defining_function = None
        
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
        self.defining_function = node.name
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

        self.visit(node.body, new_scope)
        
        self.defining_function = None

    @visitor.when(Block)
    def visit(self, node: Block, scope: Scope, defining_type: str = None):
        for child in node.value:
            self.visit(child, scope)

    @visitor.when(Binary)
    def visit(self, node: Binary, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.value, scope)

    @visitor.when(Call)
    def visit(self, node: Call, scope: Scope, defining_type: str = None):
        if not scope.get_function_info(node.value, len(node.args)):
            self.errors.append(f'Function {node.value} not defined')

        for arg in node.args:
            self.visit(arg, scope)

    @visitor.when(Var)
    def visit(self, node: Var, scope: Scope, defining_type: str = None):
        if not scope.get_variable(node.value):
            self.errors.append(f'Variable {node.value} not defined')

    @visitor.when(LetList)
    def visit(self, node: LetList, scope: Scope, defining_type: str = None):
        self.visit(node.child, scope)

    @visitor.when(Let)
    def visit(self, node: Let, scope: Scope, defining_type: str = None):
        new_scope = scope.create_child_scope()
        try:
            new_scope.define_variable(node.name, node.type)
            self.visit(node.expr, new_scope)
        except SemanticError as se:
            self.errors.append(se.text)

        self.visit(node.value, new_scope)

    @visitor.when(Conditional)
    def visit(self, node: Conditional, scope: Scope, defining_type: str = None):
        self.visit(node.if_expr, scope)
        self.visit(node.if_body, scope)
        self.visit(node.else_body, scope)
        if node.branches:
            for branch in node.branches:
                self.visit(branch, scope)
    
    @visitor.when(Branch)
    def visit(self, node: Branch, scope: Scope, defining_type: str = None):
        self.visit(node.condition, scope)
        self.visit(node.value)
    
    @visitor.when(Not)
    def visit(self, node: Not, scope: Scope, defining_type: str = None):
        pass
    
    @visitor.when(UnaryMinus)
    def visit(self, node: UnaryMinus, scope: Scope, defining_type: str = None):
        self.visit(node.value, scope)
    
    @visitor.when(NotEqual)
    def visit(self, node: NotEqual, scope: Scope, defining_type: str = None):
        pass
    
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
    
    # @visitor.when(Pi)
    # def visit(self, node: Pi, scope: Scope, defining_type: str = None):
    #     raise Exception('Error: Pi not implemented')
    
    # @visitor.when(E)
    # def visit(self, node: E, scope: Scope, defining_type: str = None):
    #     raise Exception('Error: E not implemented')
    
    @visitor.when(Call)
    def visit(self, node: Call, scope: Scope, defining_type: str = None):
        args = node.args if node.args else []
        if scope.get_function_info(node.value, len(args)) is None:
            self.errors.append(SemanticError(f'Function {node.value} not defined'))
    
    @visitor.when(While)
    def visit(self, node: While, scope: Scope, defining_type: str = None):
        self.visit(node.stop, scope)
        self.visit(node.value, scope)

    
    @visitor.when(For)
    def visit(self, node: For, scope: Scope, defining_type: str = None):
        new_scope = scope.create_child_scope()
        new_scope.define_variable(node.item, None)
        self.visit(node.collection, scope)
        self.visit(node.value, new_scope)
    
    @visitor.when(ForVar)
    def visit(self, node: ForVar, scope: Scope, defining_type: str = None):
        raise Exception('Error: ForVar not implemented')
    
    @visitor.when(Invoke)
    def visit(self, node: Invoke, scope: Scope, defining_type: str = None):
        if not (node.value.value and node.value.value == 'self'):
            self.visit(node.value, scope)
        try:
            scope.get_variable(node.value.value)
        except SemanticError as se:
            self.errors.append(se.text)

    
    @visitor.when(Indexing)
    def visit(self, node: Indexing, scope: Scope, defining_type: str = None):
        self.visit(node.value, scope)
    
    @visitor.when(TypeDef)
    def visit(self, node: TypeDef, scope: Scope):
        self.type_def = node.name
        definition_scope = scope.create_child_scope()
        if node.args:
            for arg, arg_type in node.args:
                definition_scope.define_variable(arg, arg_type)
                
        if node.type:
            self.type_w_inheritance = node.type
            parent_type:Type = self.context.get_protocol_or_type(node.type)
            if len(node.inner_args if node.inner_args else []) != len(parent_type.args):
                self.errors.append(SemanticError(f'Parent has {len(parent_type.args)} and {len(node.inner_args)} where given'))
        
        attr_scope = Scope()
        if node.body:
            for statement in node.body:
                if isinstance(statement, Property):
                    self.visit(statement, attr_scope)
        
        funcs_scope = Scope()
        definition_scope.define_variable("self", node.name)

        if node.body:
            for statement in node.body:
                if isinstance(statement, Function):
                    self.visit(statement, funcs_scope)  
            
        definition_scope.class_def = {
            'atributes': attr_scope,
            'functions': funcs_scope
        }      
        
        self.type_w_inheritance = None
        self.type_def = None
        
    @visitor.when(Property)
    def visit(self, node: Property, scope: Scope, defining_type: str = None):
        scope.define_variable(node.name, node.type)
        self.visit(node.value, scope)
    
    @visitor.when(Base)
    def visit(self, node: Property, scope: Scope):
        if not self.type_w_inheritance:
            self.errors.append(SemanticError('Can not call a base function in a type without inheritance'))
            return
        function_name = self.defining_function
        if not function_name:
            self.errors.append(SemanticError('Can not call a base function outside of a function definition'))
            return
        
        Parent_type: Type = self.context.get_type(self.type_w_inheritance)
        parent_method = None
        
        while(Parent_type):
            try:
                parent_method: Function = Parent_type.get_method(function)
            except Exception as e:
                Parent_type = Parent_type.parent if Parent_type.parent else None
                
        if not parent_method:
            self.errors.append(SemanticError(f'The method {function_name} is not in any of the type\'s ancestors'))
            return
            
        if len(node.args) != len(parent_method.params):
            self.errors.append(SemanticError(f'The method {function_name} has {len(parent_method.params)} arguments and {len(node.args)} where given'))
            return
                
    
    @visitor.when(Assign)
    def visit(self, node: Assign, scope: Scope, defining_type: str = None):
        self.visit(node.value, scope)
        self.visit(node.body, scope)
    
    @visitor.when(CreateInstance)
    def visit(self, node: CreateInstance, scope: Scope, defining_type: str = None):
        try:
            self.context.get_type(node.value)
        except SemanticError as e:
            self.errors.append(e)


    @visitor.when(Print)
    def visit(self, node: Print, scope: Scope, defining_type: str = None):
        if not scope.get_function_info(node.value, len(node.args)):
            self.errors.append(f'Function {node.value} not defined')

        for arg in node.args:
            self.visit(arg, scope)

    @visitor.when(Sqrt)
    def visit(self, node: Sqrt, scope: Scope, defining_type: str = None):
        if not scope.get_function_info(node.value, len(node.args)):
            self.errors.append(f'Function {node.value} not defined')

        for arg in node.args:
            self.visit(arg, scope)

    @visitor.when(Log)
    def visit(self, node: Log, scope: Scope, defining_type: str = None):
        if not scope.get_function_info(node.value, len(node.args)):
            self.errors.append(f'Function {node.value} not defined')

        for arg in node.args:
            self.visit(arg, scope)

    @visitor.when(Exp)
    def visit(self, node: Exp, scope: Scope, defining_type: str = None):
        if not scope.get_function_info(node.value, len(node.args)):
            self.errors.append(f'Function {node.value} not defined')

        for arg in node.args:
            self.visit(arg, scope)

    @visitor.when(Rand)
    def visit(self, node: Rand, scope: Scope, defining_type: str = None):
        if not scope.get_function_info(node.value, len(node.args)if node.args else 0):
            self.errors.append(f'Function {node.value} not defined')
        if node.args:
            for arg in node.args:
                self.visit(arg, scope)

    @visitor.when(Cos)
    def visit(self, node: Cos, scope: Scope, defining_type: str = None):
        if not scope.get_function_info(node.value, len(node.args)):
            self.errors.append(f'Function {node.value} not defined')

        for arg in node.args:
            self.visit(arg, scope)

    @visitor.when(Sin)
    def visit(self, node: Sin, scope: Scope, defining_type: str = None):
        if not scope.get_function_info(node.value, len(node.args)):
            self.errors.append(f'Function {node.value} not defined')

        for arg in node.args:
            self.visit(arg, scope)