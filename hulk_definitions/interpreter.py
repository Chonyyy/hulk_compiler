from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError, Type
from tools import visitor
from tools.semantic import Scope, ScopeInterpreter
from typing import Callable
import math, random

class Interpreter(object):
    def __init__(self, context: Context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        

    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Program)
    def visit(self, node: Program):
        scope = ScopeInterpreter()
        scope.define_function('print', print)
        scope.define_function('sqrt', math.sqrt)
        scope.define_function('sin', math.sin)
        scope.define_function('cos', math.cos)
        scope.define_function('exp', math.exp)
        scope.define_function('log', math.log)
        scope.define_function('rand', random)
        scope.define_function('range', range)
        scope.define_protocol('Iterable', self.context.get_protocol('Iterable'))
        
        for child in node.statements:
           return_last_statement = self.visit(child, scope )
        return return_last_statement
    
    @visitor.when(Statement)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        pass

    @visitor.when(Let)
    def visit(self, node: Let, scope: ScopeInterpreter, type_def = None):
        child_scope = scope.create_child_scope()
        value_exp = self.visit(node.expr,scope, type_def)
        child_scope.define_variable(node.name, value_exp, node.type)
        
        # if value_exp in scope.local_types.values():
        #     value_body = self.visit( node.scope, child_scope , value_exp )
            
        value_body = self.visit( node.scope, child_scope , value_exp ) 
        return value_body
        
    @visitor.when(LetList)
    def visit(self, node: LetList, scope: ScopeInterpreter, type_def = None):
        return self.visit( node.child, scope, type_def)

    @visitor.when(Block)
    def visit(self, node: Block, scope: ScopeInterpreter, type_def = None):
        body = None
        if node.body:
            for statement in node.body:
                body = self.visit( statement, scope, type_def)
        return body
    
    @visitor.when(Function)
    def visit(self, node: Function, scope: ScopeInterpreter, type_def = None):
        body_scope = scope.create_child_scope()

        def fun (*args):
            for i in range(len(node.params)if node.params else 0):
                x = node.params[i][0]
                body_scope.define_variable(x, args[i], node.params[i][1])
                
            function_body: Callable = self.visit(node.body , body_scope, type_def)
            
            return function_body
        
        scope.define_function(node.name, fun)
        return fun

    @visitor.when(Conditional)
    def visit(self, node: Conditional, scope: ScopeInterpreter, type_def = None):
        body_scope = scope.create_child_scope()
        
        if_expr_value = self.visit(node.if_expr, scope)

        if if_expr_value:
            return self.visit(node.if_body, body_scope)
        else:
            return self.visit(node.else_body, body_scope)

    @visitor.when(Branch)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        condition_value = self.visit( node.condition, scope)
        if condition_value:
            return self.visit(node.body)
        else:
             pass

    @visitor.when(Expression)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        pass

    @visitor.when(Unary)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        right_value = self.visit(node.right, scope)
        return right_value

    @visitor.when(Number)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        return float(node.lex)
    
    @visitor.when(Pi)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        return math.pi
    
    @visitor.when(E)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        return math.e
    
    
    @visitor.when(Print)
    def visit(self, node: Print, scope: ScopeInterpreter, type_def = None):
        args = [self.visit(arg, scope, type_def) for arg in node.args]
        print(*args)
        
    @visitor.when(Plus)
    def visit(self, node: Plus, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope, type_def)
        right_value = self.visit(node.right, scope, type_def)
        return left_value + right_value

    @visitor.when(BinaryMinus)
    def visit(self, node: BinaryMinus, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value - right_value

    @visitor.when(Star)
    def visit(self, node: Star, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value * right_value

    @visitor.when(Pow)
    def visit(self, node: Pow, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope, type_def)
        right_value = self.visit(node.right, scope, TypeDef)
        return left_value ** right_value

    @visitor.when(Div)
    def visit(self, node: Div, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value / right_value

    @visitor.when(Mod)
    def visit(self, node: Mod, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value % right_value
    
    @visitor.when(Is)
    def visit(self, node: Is, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value is right_value

    @visitor.when(As)
    def visit(self, node: As, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value == right_value

    @visitor.when(At)
    def visit(self, node: At, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope, type_def)
        right_value = self.visit(node.right, scope, type_def)
        return str(left_value) + '' + str(right_value)

    @visitor.when(DoubleAt)
    def visit(self, node: DoubleAt, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope, type_def)
        right_value = self.visit(node.right, scope, type_def)
        return str(left_value) + '  ' + str(right_value)


    @visitor.when(Or)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value or right_value

    @visitor.when(And)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value and right_value

    @visitor.when(GreaterThan)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value > right_value

    @visitor.when(LessThan)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value < right_value

    @visitor.when(GreaterEqual)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value >= right_value

    @visitor.when(LessEqual)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value <= right_value

    @visitor.when(NotEqual)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value != right_value

    @visitor.when(CompareEqual)
    def visit(self, node: CompareEqual, scope: ScopeInterpreter, type_def = None):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value == right_value

    @visitor.when(Not)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        value = self.visit(node.right, scope)
        return not value

    @visitor.when(UnaryMinus)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        value = self.visit(node.right, scope)
        return -value

    @visitor.when(Atom)
    def visit(self, node: Atom, scope: ScopeInterpreter, type_def = None):
        return node.lex

    @visitor.when(Call)
    def visit(self, node: Call, scope: ScopeInterpreter, type_def = None):
        # Evaluar los argumentos de la llamada
        args = [self.visit(arg, scope) for arg in node.args]
        func = scope.get_local_function(node.idx)
        return func(*args)

    @visitor.when(Str)
    def visit(self, node: Str, scope: ScopeInterpreter, type_def = None):
        return str(node.lex)

    @visitor.when(Bool)
    def visit(self, node: Bool, scope: ScopeInterpreter, type_def = None):
        return bool(node.lex)

    @visitor.when(Invoke)
    def visit(self, node: Invoke, scope: ScopeInterpreter, type_def = None):
        child_scope = scope.create_child_scope()
        container_type = self.visit(node.container, scope, type_def)
        
        func = None
        
        if type_def is not None:
                func = type_def.call( node.lex)
        else:
            if node.container.lex == 'self':
                if type(node.lex) == str:
                    func = container_type.call(None, node.lex)
                else:
                    func = container_type.call(None, node.lex.lex)
            else:
                arg = node.lex.lex
                func = container_type.call(arg)
            
        try:
            return func()
        except:
            return func
        
             
    @visitor.when(Vector)
    def visit(self, node: Vector, scope: ScopeInterpreter, type_def = None):
        values = [self.visit(value, scope) for value in node.lex]
        return values

    @visitor.when(VectorComprehension)
    def visit(self, node: VectorComprehension, scope: ScopeInterpreter, type_def = None):
        
        a = self.visit(node.lex, scope)
        values = []
        for value in a:
            scope_body = scope.create_child_scope()
            scope_body.define_variable(node.operation[0], value, type(value))
            operation = self.visit(node.operation[1], scope_body)
            values.append(operation)
        
        return values

    @visitor.when(Var)
    def visit(self, node: Var, scope: ScopeInterpreter, type_def = None):
        var = scope.get_local_variable(node.lex)
        return var[0] if var else None

    @visitor.when(TypeDef)
    def visit(self, node: TypeDef, scope: ScopeInterpreter, type_def = None):
        # body_scope = scope.create_child_scope()
        visitor = self
        
        if node.inheritance:
            inher = scope.get_local_type(node.inheritance)
            
            class NewType(inher):
                def __init__(self, params = None):
                    self.typeScope = scope.create_child_scope()
                    self.vars = []
                    self.func = {}
                    
                    if len(node.args)if node.args else 0 > 0:
                        for i in range(len(params) if params else 0):
                            self.typeScope.define_variable(node.args[i][0], params[i])
                            self.vars.append((node.args[i][0],params[i]))
                    
                    if node.body:
                        for x in [x for x in node.body if type(x) is Property]:
                            if not self.typeScope.get_local_variable(x):
                                b = visitor.visit(x, self.typeScope, inher)
                                self.typeScope.define_variable(x.name, b)
                                scope.define_variable(x.name, b)
                                self.vars.append((x.name, b))
                    
                        for x in [x for x in node.body if type(x) is Function]:
                            self.func[x.name] = x
                            if scope.get_local_function(x.name):
                                visitor.visit(x, self.typeScope, inher)
                                continue
                            a = visitor.visit(x, scope, inher)
                
                def call(self, name):
                    if scope.get_local_function(name):
                        return scope.get_local_function(name)
                    else:
                        scope.get_local_variable(name) 
                
                def create_new_instance(params = None):
                    return NewType(params)
        else:
            class NewType:
                def __init__(self, params = None):
                    self.typeScope = scope.create_child_scope()
                    self.vars = []
                    self.func = {}
                    
                    if len(node.args)if node.args else 0 > 0:
                        for i in range(len(params) if params else 0):
                            self.typeScope.define_variable(node.args[i][0], params[i])
                            self.vars.append((node.args[i][0],params[i]))
                    
                    if node.body:
                        for x in [x for x in node.body if type(x) is Property]:
                            if not self.typeScope.get_local_variable(x):
                                b = visitor.visit(x, self.typeScope, NewType)
                                self.typeScope.define_variable(x.name, b)
                                scope.define_variable(x.name, b)
                                self.vars.append((x.name, b))
                    
                        for x in [x for x in node.body if type(x) is Function]:
                            self.func[x.name] = x
                            if scope.get_local_function(x.name):
                                continue
                            a = visitor.visit(x, scope, NewType)
                
                def call(self, name):
                    if scope.get_local_function(name):
                        return scope.get_local_function(name)
                    else:
                        scope.get_local_variable(name)
                
                def create_new_instance(params):
                    return NewType(params)       
                    
        scope.define_type(node.name, NewType)
        NewType()
        return NewType
    
    @visitor.when(Protocol)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
         pass
    
    @visitor.when(Assign)
    def visit(self, node: Assign, scope: ScopeInterpreter, type_def = None):
        value = self.visit(node.body, scope)
        scope.define_variable(node.lex.lex, value, None) 
        return value

    @visitor.when(Indexing)
    def visit(self, node: Indexing, scope: ScopeInterpreter, type_def = None):
        name_value = self.visit(node.lex, scope)
        index_value = int(self.visit(node.index, scope))
        return name_value[index_value]

    @visitor.when(Sin)
    def visit(self, node: Sin, scope: ScopeInterpreter, type_def = None):
        args = [self.visit(arg, scope) for arg in node.args]
        return math.sin(*args)

    @visitor.when(Cos)
    def visit(self, node: Cos, scope: ScopeInterpreter, type_def = None):
        args = [self.visit(arg, scope) for arg in node.args]
        return math.cos(*args)

    @visitor.when(Rand)
    def visit(self, node: Rand, scope: ScopeInterpreter, type_def = None):
        args = [self.visit(arg, scope) for arg in node.args]
        return random.random(*args)

    @visitor.when(Exp)
    def visit(self, node: Exp, scope: ScopeInterpreter, type_def = None):
        args = [self.visit(arg, scope) for arg in node.args]
        return math.exp(*args)

    @visitor.when(Log)
    def visit(self, node: Log, scope: ScopeInterpreter, type_def = None):
        args = [self.visit(arg, scope) for arg in node.args]
        return math.log(*args)

    @visitor.when(Sqrt)
    def visit(self, node: Sqrt, scope: ScopeInterpreter, type_def = None):
        args = [self.visit(arg, scope, type_def) for arg in node.args]
        return math.sqrt(*args)

    @visitor.when(Range)
    def visit(self, node: Range, scope: ScopeInterpreter, type_def = None):
        args = [self.visit(arg, scope) for arg in node.args]
        args_int = []
        for i in range(len(args)):
            args_int.append(int(args[i]))
        return list(range(*args_int))

    @visitor.when(While)
    def visit(self, node: While, scope: ScopeInterpreter, type_def = None):
        while self.visit(node.stop, scope):
            return self.visit(node.body, scope)

    @visitor.when(For)
    def visit(self, node: For, scope: ScopeInterpreter, type_def = None):
        if node.collection.lex == 'range':
            x = int(self.visit(node.collection.args[0],scope))
            y = int(self.visit(node.collection.args[1],scope))
            for item in range(x, y):
                body_scope = scope.create_child_scope()
                body_scope.define_variable(node.item.name, item, node.item.type)
                value = self.visit(node.body, body_scope)
        else:
            for item in self.visit(node.collection, scope):
                body_scope = scope.create_child_scope()
                body_scope.define_variable(node.item.name, item, node.item.type)
                value = self.visit(node.body, body_scope)
        return value    
        
    @visitor.when(Base)
    def visit(self, node: Base, scope: ScopeInterpreter, type_def = None):
        return type_def

    @visitor.when(Property)
    def visit(self, node: Property, scope: ScopeInterpreter, type_def = None):
        name = node.name
        body_value = self.visit(node.body, scope)
        scope.define_variable(name, body_value, node.type)
        return body_value

    @visitor.when(CreateInstance)
    def visit(self, node: CreateInstance, scope: ScopeInterpreter, type_def = None):
        params_value = [self.visit(param, scope, type_def ) for param in node.params]
        type_value = scope.get_local_type(node.type)
        return type_value.create_new_instance(params_value)