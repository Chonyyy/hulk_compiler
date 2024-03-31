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
        self.types = {}

        self.invoke = None

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
        scope.define_function('rand', random.randint)
        scope.define_function('range', range)
        scope.define_protocol('Iterable', self.context.get_protocol('Iterable'))
        
        for child in node.statements:
           return_last_statement = self.visit(child, scope )
        return return_last_statement[0]
    
    @visitor.when(Statement)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        pass

    @visitor.when(Let)
    def visit(self, node: Let, scope: ScopeInterpreter, type_def = None):
        child_scope = scope.create_child_scope()
        value_exp, value_type = self.visit(node.expr, scope, type_def)
        child_scope.define_variable(node.name, value_exp, value_type)
            
        value_body = self.visit( node.value, child_scope , value_exp ) 
        return value_body
        
    @visitor.when(LetList)
    def visit(self, node: LetList, scope: ScopeInterpreter, type_def = None):
        return self.visit( node.child, scope, type_def)

    @visitor.when(Block)
    def visit(self, node: Block, scope: ScopeInterpreter, type_def = None):
        body = None
        if node.value:
            for statement in node.value:
                body = self.visit( statement, scope, type_def)
        return body #TODO: add return to print
    
    @visitor.when(Function)
    def visit(self, node: Function, scope: ScopeInterpreter, type_def = None):
        body_scope = scope.create_child_scope()

        def fun (*rargs):#TODO: args ?
            for i in range(len(node.params)if node.params else 0):
                x = node.params[i][0]
                    
                body_scope.define_variable(x, rargs[i][0], rargs[i][1])
                
            function_body, function_type = self.visit(node.body , body_scope, type_def)
            
            return function_body, function_type
        
        scope.define_function(node.name, fun)

    @visitor.when(Conditional)
    def visit(self, node: Conditional, scope: ScopeInterpreter, type_def = None):
        body_scope = scope.create_child_scope()
        
        if_expr_value, _ = self.visit(node.if_expr, scope)

        if if_expr_value:
            return self.visit(node.if_body, body_scope)
        
        for branch in node.branches:
            v = self.visit(branch, scope)
            if v:
                return v
        
        return self.visit(node.else_body, body_scope)

    @visitor.when(Branch)
    def visit(self, node: Branch, scope: ScopeInterpreter, type_def = None):
        condition_value, _ = self.visit(node.condition, scope)
        branch_scope = scope.create_child_scope()
        if condition_value:
            return self.visit(node.value, branch_scope)
        else:
            return False

    @visitor.when(Expression)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        pass

    @visitor.when(Unary)
    def visit(self, node: Unary, scope: ScopeInterpreter, type_def = None):
        right_value = self.visit(node.value, scope)
        return right_value

    @visitor.when(Number)
    def visit(self, node: Number, scope: ScopeInterpreter, type_def = None):
        return (float(node.value), 'Number')
    
    @visitor.when(Pi)
    def visit(self, node: Pi, scope: ScopeInterpreter, type_def = None):
        return (math.pi, 'Number')
    
    @visitor.when(E)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
        return (math.e, 'Number')
    
    
    @visitor.when(Print)
    def visit(self, node: Print, scope: ScopeInterpreter, type_def = None):
        args, type = [self.visit(arg, scope, type_def) for arg in node.args][0]
        print(args)
        return (args, type)
        
    @visitor.when(Plus)
    def visit(self, node: Plus, scope: ScopeInterpreter, type_def = None):
        left_value, left_type= self.visit(node.left, scope, type_def)
        right_value, right_type= self.visit(node.value, scope, type_def)
        return (left_value + right_value, 'Number')

    @visitor.when(BinaryMinus)
    def visit(self, node: BinaryMinus, scope: ScopeInterpreter, type_def = None):
        left_value, left_type= self.visit(node.left, scope)
        right_value, right_type= self.visit(node.value, scope)
        return (left_value - right_value, 'Number')

    @visitor.when(Star)
    def visit(self, node: Star, scope: ScopeInterpreter, type_def = None):
        left_value, left_type= self.visit(node.left, scope)
        right_value, right_type= self.visit(node.value, scope)
        return (left_value * right_value, 'Number')

    @visitor.when(Pow)
    def visit(self, node: Pow, scope: ScopeInterpreter, type_def = None):
        left_value, left_type = self.visit(node.left, scope, type_def)
        right_value, right_type = self.visit(node.value, scope, TypeDef)
        return (left_value ** right_value, 'Number')

    @visitor.when(Div)
    def visit(self, node: Div, scope: ScopeInterpreter, type_def = None):
        left_value, left_type = self.visit(node.left, scope)
        right_value, right_type = self.visit(node.value, scope)
        return (left_value / right_value, 'Number')

    @visitor.when(Mod)
    def visit(self, node: Mod, scope: ScopeInterpreter, type_def = None):
        left_value, left_type = self.visit(node.left, scope)
        right_value, right_type = self.visit(node.value, scope)
        return (left_value % right_value, 'Number')
    
    @visitor.when(Is)
    def visit(self, node: Is, scope: ScopeInterpreter, type_def = None):
        left_value, left_type = self.visit(node.left, scope)
        right_value, right_type = self.visit(node.value, scope)
        return (left_value is right_value, 'Boolean')

    @visitor.when(As)
    def visit(self, node: As, scope: ScopeInterpreter, type_def = None):
        left_value, left_type = self.visit(node.left, scope)
        right_value,  right_type = self.visit(node.value, scope)
        return left_value == right_value

    @visitor.when(At)
    def visit(self, node: At, scope: ScopeInterpreter, type_def = None):
        left_value, left_type = self.visit(node.left, scope, type_def)
        right_value, right_type = self.visit(node.value, scope, type_def)
        return (str(left_value) + str(right_value), 'String')

    @visitor.when(DoubleAt)
    def visit(self, node: DoubleAt, scope: ScopeInterpreter, type_def = None):
        left_value, left_type = self.visit(node.left, scope, type_def)
        right_value, right_type = self.visit(node.value, scope, type_def)
        return (str(left_value) + ' ' + str(right_value), 'String')


    @visitor.when(Or)
    def visit(self, node: Or, scope: ScopeInterpreter, type_def = None):
        left_value, left_type = self.visit(node.left, scope)
        right_value, right_type = self.visit(node.value, scope)
        return (left_value or right_value, 'Boolean')

    @visitor.when(And)
    def visit(self, node: And, scope: ScopeInterpreter, type_def = None):
        left_value, left_type= self.visit(node.left, scope)
        right_value, right_type= self.visit(node.value, scope)
        return (left_value and right_value, 'Boolean')

    @visitor.when(GreaterThan)
    def visit(self, node: GreaterThan, scope: ScopeInterpreter, type_def = None):
        left_value, left_type= self.visit(node.left, scope)
        right_value, right_type= self.visit(node.value, scope)
        return (left_value > right_value, 'Boolean')

    @visitor.when(LessThan)
    def visit(self, node: LessThan, scope: ScopeInterpreter, type_def = None):
        left_value, left_type= self.visit(node.left, scope)
        right_value, right_type= self.visit(node.value, scope)
        return (left_value < right_value, 'Boolean')

    @visitor.when(GreaterEqual)
    def visit(self, node: GreaterEqual, scope: ScopeInterpreter, type_def = None):
        left_value, left_type= self.visit(node.left, scope)
        right_value, right_type= self.visit(node.value, scope)
        return (left_value >= right_value, 'Boolean')

    @visitor.when(LessEqual)
    def visit(self, node: LessEqual, scope: ScopeInterpreter, type_def = None):
        left_value, left_type= self.visit(node.left, scope)
        right_value, right_type= self.visit(node.value, scope)
        return (left_value <= right_value, 'Boolean')

    @visitor.when(NotEqual)
    def visit(self, node: NotEqual, scope: ScopeInterpreter, type_def = None):
        left_value, left_type= self.visit(node.left, scope)
        right_value, right_type= self.visit(node.value, scope)
        return (left_value != right_value, 'Boolean')

    @visitor.when(CompareEqual)
    def visit(self, node: CompareEqual, scope: ScopeInterpreter, type_def = None):
        left_value, left_type= self.visit(node.left, scope)
        right_value, right_type= self.visit(node.value, scope)
        return (left_value == right_value, 'Boolean')

    @visitor.when(Not)
    def visit(self, node: Not, scope: ScopeInterpreter, type_def = None):
        value, type = self.visit(node.value, scope)
        return (not value, 'Boolean')

    @visitor.when(UnaryMinus)
    def visit(self, node: UnaryMinus, scope: ScopeInterpreter, type_def = None):
        value, type= self.visit(node.value, scope)
        return (-value, 'Number')

    @visitor.when(Call)
    def visit(self, node: Call, scope: ScopeInterpreter, type_def = None):
        # Evaluar los argumentos de la llamada
        args = [self.visit(arg, scope) for arg in node.args]
        func = scope.get_local_function(node.value)

        return func(*args)

    @visitor.when(Str)
    def visit(self, node: Str, scope: ScopeInterpreter, type_def = None):
        #TODO: change \" for "
        return (str(node.value[1:-1]), "String")

    @visitor.when(Bool)
    def visit(self, node: Bool, scope: ScopeInterpreter, type_def = None):
        return (bool(node.value), 'Boolean')

    @visitor.when(Invoke)
    def visit(self, node: Invoke, scope: ScopeInterpreter, type_def = None):
        container, type = self.visit(node.value, scope, type_def)
        #region warever
        # func = None
        # if type_def is not None:
        #     if node.value.value == 'self':
        #         if type(node.value) == str:
        #             func = container_type.call(None, node.value)
        #         else:
        #             func = container_type.call(None, node.value.value)
        #     else:
        #         func = type_def.call( node.value)
        
        # if node.value.value == 'self':
        #     if type(node.value) == str:
        #         func = container_type.call(None, node.value)
        #     else:
        #         func = container_type.call(None, node.value.value)
        # else:
        #     arg = node.value.value
        #     func = container_type.call(arg)
            
        # try:
        #     return func()
        # except:
        #     return func
        #endregion
        self.invoke = None
             
    @visitor.when(Vector)
    def visit(self, node: Vector, scope: ScopeInterpreter, type_def = None):
        values = [self.visit(value, scope) for value in node.value]
        return (values, 'Vector')

    @visitor.when(VectorComprehension)
    def visit(self, node: VectorComprehension, scope: ScopeInterpreter, type_def = None):
        
        a = self.visit(node.value, scope)
        values = []
        for value in a:
            scope_body = scope.create_child_scope()
            scope_body.define_variable(node.operation[0], value, type(value))
            operation = self.visit(node.operation[1], scope_body)
            values.append(operation)
        
        return (values, 'Vector')

    @visitor.when(Var)
    def visit(self, node: Var, scope: ScopeInterpreter, type_def = None):
        var = scope.get_local_variable(node.value)
        return var if var else None

    @visitor.when(TypeDef)
    def visit(self, node: TypeDef, scope: ScopeInterpreter, type_def = None):
        definition_scope = scope.create_child_scope()
        if node.args:
            for arg in node.args:
                definition_scope.define_variable(arg[0], None, None)
        def fact(*args):
            father_scope = None
            if node.type:
                parent_type = self.context.get_protocol_or_type(node.type)
                if parent_type.args:
                    father_scope = self.types[node.type](*args)
                else:
                    father_scope = self.types[node.type]()
            else:
                father_scope = definition_scope.create_child_scope()

            class_scope = father_scope.create_child_scope()
            arg_dict = {}
            if node.args:
                for i, argument in enumerate(args):
                        definition_scope.local_vars[node.args[i][0]] = (argument[0], argument[1])
                        definition_scope.get_local_variable
            elif args:
                for i, argument in enumerate(args):
                    if argument:
                        father_scope.local_vars[node.args[i][0]] = (argument[0], argument[1])
                    else:
                        break
                
            for statemment in node.body:
                # if isinstance(statemment, Function):
                #     continue
                self.visit(statemment, class_scope)

            
            return class_scope, node.name

        self.types[node.name] = fact

    @visitor.when(Protocol)
    def visit(self, node, scope: ScopeInterpreter, type_def = None):
         pass
    
    @visitor.when(Assign)
    def visit(self, node: Assign, scope: ScopeInterpreter, type_def = None):
        value, type = self.visit(node.body, scope)
        scope.define_variable(node.value.value, value, type) 
        return (value, type)

    @visitor.when(Indexing)
    def visit(self, node: Indexing, scope: ScopeInterpreter, type_def = None):
        name_value, _ = self.visit(node.value, scope)
        index_value, _ = int(self.visit(node.index, scope))
        return name_value[index_value]

    @visitor.when(Sin)
    def visit(self, node: Sin, scope: ScopeInterpreter, type_def = None):
        rargs = [self.visit(arg, scope) for arg in node.args]
        args = []
        for arg in rargs:
            args.append(arg[0])
        return (math.sin(*args), 'Number')

    @visitor.when(Cos)
    def visit(self, node: Cos, scope: ScopeInterpreter, type_def = None):
        rargs = [self.visit(arg, scope) for arg in node.args]
        args = []
        for arg in rargs:
            args.append(arg[0]) 
        
        return (math.cos(*args), 'Number')

    @visitor.when(Rand)
    def visit(self, node: Rand, scope: ScopeInterpreter, type_def = None):
        rargs = [self.visit(arg, scope) for arg in node.args]
        args = []
        for arg in rargs:
            args.append(arg[0]) 
        
        return (random.random(*args), 'Number')

    @visitor.when(Exp)
    def visit(self, node: Exp, scope: ScopeInterpreter, type_def = None):
        rargs = [self.visit(arg, scope) for arg in node.args]
        args = []
        for arg in rargs:
            args.append(arg[0]) 
        
        return (math.exp(*args), 'Number')

    @visitor.when(Log)
    def visit(self, node: Log, scope: ScopeInterpreter, type_def = None):
        rargs = [self.visit(arg, scope) for arg in node.args]
        args = []
        for arg in rargs:
            args.append(arg[0]) 
        return (math.log(*args), 'Number')

    @visitor.when(Sqrt)
    def visit(self, node: Sqrt, scope: ScopeInterpreter, type_def = None):
        rargs = [self.visit(arg, scope, type_def) for arg in node.args]
        args = []
        for arg in rargs:
            args.append(arg[0]) 
        
        return (math.sqrt(*args), 'Number')

    @visitor.when(Range)
    def visit(self, node: Range, scope: ScopeInterpreter, type_def = None):
        args = [self.visit(arg, scope) for arg in node.args]
        args_int = []
        for i in range(len(args)):
            args_int.append(int(args[i]))
        return (list(range(*args_int)), 'Vector')

    @visitor.when(While)
    def visit(self, node: While, scope: ScopeInterpreter, type_def = None):
        while self.visit(node.stop, scope)[0]:
            return self.visit(node.value, scope)

    @visitor.when(For)
    def visit(self, node: For, scope: ScopeInterpreter, type_def = None):
        if node.collection.value == 'range':
            x = int(self.visit(node.collection.args[0],scope))
            y = int(self.visit(node.collection.args[1],scope))
            for item in range(x, y):
                body_scope = scope.create_child_scope()
                body_scope.define_variable(node.item, item, 'Number')
                value = self.visit(node.value, body_scope)
        else:
            for item in self.visit(node.collection, scope):
                body_scope = scope.create_child_scope()
                body_scope.define_variable(node.item, item, node.item.type)
                value = self.visit(node.value, body_scope)
        return value    
        
    @visitor.when(Base)
    def visit(self, node: Base, scope: ScopeInterpreter, type_def = None):
        return type_def

    @visitor.when(Property)
    def visit(self, node: Property, scope: ScopeInterpreter, type_def = None):
        # name = node.name
        # body_value = self.visit(node.body, scope)
        # scope.define_variable(name, body_value, node.type)
        # return body_value
        value_exp, value_type = self.visit(node.value, scope, type_def)
        scope.define_variable(node.name, value_exp, value_type)
            
        value_body = self.visit( node.value, scope , value_exp ) 
        return value_body

    @visitor.when(CreateInstance)
    def visit(self, node: CreateInstance, scope: ScopeInterpreter, type_def = None):
        if node.params:
            params_value = [self.visit(param, scope, type_def ) for param in node.params]
        else:
            params_value = []
        type_value = self.types[node.value]
        type_scope = type_value(*params_value)
        return type_scope