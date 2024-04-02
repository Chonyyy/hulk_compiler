from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError, Type
from tools import visitor
from tools.semantic import Scope, ScopeInterpreter
from typing import Callable
from hulk_definitions.ast import *
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
    def visit(self, node, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        pass

    @visitor.when(Let)
    def visit(self, node: Let, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        child_scope = scope.create_child_scope()
        value_exp, value_type = self.visit(node.expr, scope, func_name, parent_scope)
        child_scope.define_variable(node.name, value_exp, value_type)
            
        value_body = self.visit( node.value, child_scope , func_name ) 
        return value_body
        
    @visitor.when(LetList)
    def visit(self, node: LetList, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        return self.visit( node.child, scope, func_name, parent_scope)

    @visitor.when(Block)
    def visit(self, node: Block, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        body = None
        if node.value:
            for statement in node.value:
                body = self.visit( statement, scope, func_name, parent_scope)
        return body #TODO: add return to print
    
    @visitor.when(Function)
    def visit(self, node: Function, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        func_name = node.name
        body_scope = scope.create_child_scope()

        def fun (*rargs):
            for i in range(len(node.params)if node.params else 0):
                x = node.params[i][0]
                    
                body_scope.define_variable(x, rargs[i][0], rargs[i][1])
                
            function_body, function_type = self.visit(node.body , body_scope, func_name, parent_scope)
            
            return function_body, function_type
        
        scope.define_function(node.name, fun)

    @visitor.when(Conditional)
    def visit(self, node: Conditional, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        body_scope = scope.create_child_scope()
        
        if_expr_value, _ = self.visit(node.if_expr, scope, func_name, parent_scope)

        if if_expr_value:
            return self.visit(node.if_body, body_scope, func_name, parent_scope)
        
        if node.branches:
            for branch in node.branches:
                v = self.visit(branch, scope, func_name, parent_scope)
                if v:
                    return v
        
        return self.visit(node.else_body, body_scope, func_name, parent_scope)

    @visitor.when(Branch)
    def visit(self, node: Branch, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        condition_value, _ = self.visit(node.condition, scope, func_name, parent_scope)
        branch_scope = scope.create_child_scope()
        if condition_value:
            return self.visit(node.value, branch_scope, func_name, parent_scope)
        else:
            return False

    @visitor.when(Expression)
    def visit(self, node, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        pass

    @visitor.when(Unary)
    def visit(self, node: Unary, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        right_value = self.visit(node.value, scope, func_name, parent_scope)
        return right_value

    @visitor.when(Number)
    def visit(self, node: Number, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        return (float(node.value), 'Number')
    
    @visitor.when(Pi)
    def visit(self, node: Pi, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        return (math.pi, 'Number')
    
    @visitor.when(E)
    def visit(self, node, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        return (math.e, 'Number')
    
    @visitor.when(Print)
    def visit(self, node: Print, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        args, type = [self.visit(arg, scope, func_name, parent_scope) for arg in node.args][0]
        print(args)
        return (args, type)
        
    @visitor.when(Plus)
    def visit(self, node: Plus, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type= self.visit(node.left, scope, func_name, parent_scope)
        right_value, right_type= self.visit(node.value, scope, func_name, parent_scope)
        return (left_value + right_value, 'Number')

    @visitor.when(BinaryMinus)
    def visit(self, node: BinaryMinus, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type= self.visit(node.left, scope, func_name, parent_scope)
        right_value, right_type= self.visit(node.value, scope, func_name, parent_scope)
        return (left_value - right_value, 'Number')

    @visitor.when(Star)
    def visit(self, node: Star, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type= self.visit(node.left, scope, func_name, parent_scope)
        right_value, right_type= self.visit(node.value, scope, func_name, parent_scope)
        return (left_value * right_value, 'Number')

    @visitor.when(Pow)
    def visit(self, node: Pow, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type = self.visit(node.left, scope, func_name, parent_scope)
        right_value, right_type = self.visit(node.value, scope, func_name, parent_scope)
        return (left_value ** right_value, 'Number')

    @visitor.when(Div)
    def visit(self, node: Div, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type = self.visit(node.left, scope, func_name, parent_scope)
        right_value, right_type = self.visit(node.value, scope, func_name, parent_scope)
        return (left_value / right_value, 'Number')

    @visitor.when(Mod)
    def visit(self, node: Mod, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type = self.visit(node.left, scope, func_name, parent_scope)
        right_value, right_type = self.visit(node.value, scope, func_name, parent_scope)
        return (left_value % right_value, 'Number')
    
    @visitor.when(Is)
    def visit(self, node: Is, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type = self.visit(node.left, scope, func_name, parent_scope)
        return (left_type == node.value, 'Boolean')

    @visitor.when(As)
    def visit(self, node: As, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type = self.visit(node.left, scope, func_name, parent_scope)
        right_value,  right_type = self.visit(node.value, scope, func_name, parent_scope)
        return left_value == right_value

    @visitor.when(At)
    def visit(self, node: At, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type = self.visit(node.left, scope, func_name, parent_scope)
        right_value, right_type = self.visit(node.value, scope, func_name, parent_scope)
        return (str(left_value) + str(right_value), 'String')

    @visitor.when(DoubleAt)
    def visit(self, node: DoubleAt, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type = self.visit(node.left, scope, func_name, parent_scope)
        right_value, right_type = self.visit(node.value, scope, func_name, parent_scope)
        return (str(left_value) + ' ' + str(right_value), 'String')

    @visitor.when(Or)
    def visit(self, node: Or, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type = self.visit(node.left, scope, func_name, parent_scope)
        right_value, right_type = self.visit(node.value, scope, func_name, parent_scope)
        return (left_value or right_value, 'Boolean')

    @visitor.when(And)
    def visit(self, node: And, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type= self.visit(node.left, scope, func_name, parent_scope)
        right_value, right_type= self.visit(node.value, scope, func_name, parent_scope)
        return (left_value and right_value, 'Boolean')

    @visitor.when(GreaterThan)
    def visit(self, node: GreaterThan, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type= self.visit(node.left, scope, func_name, parent_scope)
        right_value, right_type= self.visit(node.value, scope, func_name, parent_scope)
        return (left_value > right_value, 'Boolean')

    @visitor.when(LessThan)
    def visit(self, node: LessThan, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type= self.visit(node.left, scope, func_name, parent_scope)
        right_value, right_type= self.visit(node.value, scope, func_name, parent_scope)
        return (left_value < right_value, 'Boolean')

    @visitor.when(GreaterEqual)
    def visit(self, node: GreaterEqual, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type= self.visit(node.left, scope, func_name, parent_scope)
        right_value, right_type= self.visit(node.value, scope, func_name, parent_scope)
        return (left_value >= right_value, 'Boolean')

    @visitor.when(LessEqual)
    def visit(self, node: LessEqual, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type= self.visit(node.left, scope, func_name, parent_scope)
        right_value, right_type= self.visit(node.value, scope, func_name, parent_scope)
        return (left_value <= right_value, 'Boolean')

    @visitor.when(NotEqual)
    def visit(self, node: NotEqual, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type= self.visit(node.left, scope, func_name, parent_scope)
        right_value, right_type= self.visit(node.value, scope, func_name, parent_scope)
        return (left_value != right_value, 'Boolean')

    @visitor.when(CompareEqual)
    def visit(self, node: CompareEqual, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        left_value, left_type= self.visit(node.left, scope, func_name, parent_scope)
        right_value, right_type= self.visit(node.value, scope, func_name, parent_scope)
        return (left_value == right_value, 'Boolean')

    @visitor.when(Not)
    def visit(self, node: Not, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        value, type = self.visit(node.value, scope, func_name, parent_scope)
        return (not value, 'Boolean')

    @visitor.when(UnaryMinus)
    def visit(self, node: UnaryMinus, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        value, type= self.visit(node.value, scope, func_name, parent_scope)
        return (-value, 'Number')

    @visitor.when(Call)
    def visit(self, node: Call, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        args = []
        if node.args:
            args = [self.visit(arg, scope, func_name, parent_scope) for arg in node.args]
        func = scope.get_local_function(node.value)

        return func(*args)

    @visitor.when(Str)
    def visit(self, node: Str, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        #TODO: change \" for "
        return (str(node.value[1:-1]), "String")

    @visitor.when(Bool)
    def visit(self, node: Bool, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        return (bool(node.value), 'Boolean')

    @visitor.when(Invoke)
    def visit(self, node: Invoke, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        container, data_type = self.visit(node.value, scope, func_name, parent_scope)
        if data_type in self.types:
            if isinstance(node.prop, Invoke):
                if isinstance(node.prop.value, Call):
                    return self.visit(node.prop, container['function'], func_name, parent_scope)
                return self.visit(node.prop, container['atributes'], func_name, parent_scope)
            if isinstance(node.prop, Call):
                container['atributes'].define_variable('self', container, data_type)
                return_value = self.visit(node.prop, container['functions'], func_name, parent_scope)
                container['atributes'].remove_local_variable('self')
                return return_value
            return self.visit(node.prop, container['atributes'], func_name, parent_scope)

    @visitor.when(Vector)
    def visit(self, node: Vector, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        values = [self.visit(value, scope, func_name, parent_scope) for value in node.value]
        return (values, 'Vector')

    @visitor.when(VectorComprehension)
    def visit(self, node: VectorComprehension, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        
        a = self.visit(node.value, scope, func_name, parent_scope)
        values = []
        for value in a:
            scope_body = scope.create_child_scope()
            scope_body.define_variable(node.operation[0], value, type(value))
            operation = self.visit(node.operation[1], scope_body, func_name, parent_scope)
            values.append(operation)
        
        return (values, 'Vector')

    @visitor.when(Var)
    def visit(self, node: Var, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        var = scope.get_local_variable(node.value)
        return var if var else None

    @visitor.when(TypeDef)
    def visit(self, node: TypeDef, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        definition_scope = scope.create_child_scope()
        if node.args:
            for arg in node.args:
                definition_scope.define_variable(arg[0], None, None)

        def fact(*args):
            father_scope = None
            parent_scope = None
            if node.type:
                parent_type = self.context.get_type(node.type)
                father_instance = self.types[node.type](*args)
                parent_scope = father_instance[0]['functions']
            else:
                father_scope = (definition_scope.create_child_scope(), "Object")
                father_attr_scope = (father_scope[0].create_child_scope())
                father_func_scope = (father_scope[0].create_child_scope())
                father_instance = ({
                    'atributes': father_attr_scope,
                    'functions': father_func_scope
                }, "Object")

            attr_scope = father_instance[0]['atributes'].create_child_scope()
            arg_dict = {}
            if node.args:# TODO Revisar esto
                for i, argument in enumerate(args):
                        definition_scope.local_vars[node.args[i][0]] = (argument[0], argument[1])
            
            if node.body:
                for statement in node.body:
                    if isinstance(statement, Function):
                        continue
                    self.visit(statement, attr_scope, func_name, parent_scope)
            if node.args:
                for argument in node.args:
                    definition_scope.remove_local_variable(argument[0])
            
            func_scope = father_instance[0]['functions'].create_child_scope()
            if node.body:
                for statement in node.body:
                    if isinstance(statement, Function):
                        self.visit(statement, func_scope, func_name, parent_scope)
            
            type_instance = {
                "functions": func_scope,
                "atributes": attr_scope
            }
            definition_scope.define_variable(
                'self',
                {
                'atributes': attr_scope,
                'functions': func_scope
                },
                node.name
                )
            return type_instance, node.name#TODO Return Both Scopes

        self.types[node.name] = fact

    @visitor.when(Protocol)
    def visit(self, node, scope: ScopeInterpreter, func_name = None, parent_scope = None):
         pass
    
    @visitor.when(Assign)
    def visit(self, node: Assign, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        value, type = self.visit(node.body, scope, func_name, parent_scope)
        _, nscope = scope.get_variable(node.value.value) 
        if nscope:
            nscope.local_vars[node.value.value] = (value, type)
        return (value, type)

    @visitor.when(Indexing)
    def visit(self, node: Indexing, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        name_value, _ = self.visit(node.value, scope, func_name, parent_scope)
        index_value, _ = int(self.visit(node.index, scope, func_name, parent_scope))
        return name_value[index_value]

    @visitor.when(Sin)
    def visit(self, node: Sin, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        rargs = [self.visit(arg, scope, func_name, parent_scope) for arg in node.args]
        args = []
        for arg in rargs:
            args.append(arg[0])
        return (math.sin(*args), 'Number')

    @visitor.when(Cos)
    def visit(self, node: Cos, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        rargs = [self.visit(arg, scope, func_name, parent_scope) for arg in node.args]
        args = []
        for arg in rargs:
            args.append(arg[0]) 
        
        return (math.cos(*args), 'Number')

    @visitor.when(Rand)
    def visit(self, node: Rand, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        if node.args:
            rargs = [self.visit(arg, scope, func_name, parent_scope) for arg in node.args]
        else:
            rargs = []
        args = []
        for arg in rargs:
            args.append(arg[0]) 
        
        return (random.random(*args), 'Number')

    @visitor.when(Exp)
    def visit(self, node: Exp, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        rargs = [self.visit(arg, scope, func_name, parent_scope) for arg in node.args]
        args = []
        for arg in rargs:
            args.append(arg[0]) 
        
        return (math.exp(*args), 'Number')

    @visitor.when(Log)
    def visit(self, node: Log, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        rargs = [self.visit(arg, scope, func_name, parent_scope) for arg in node.args]
        args = []
        for arg in rargs:
            args.append(arg[0]) 
        return (math.log(*args), 'Number')

    @visitor.when(Sqrt)
    def visit(self, node: Sqrt, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        rargs = [self.visit(arg, scope, func_name, parent_scope) for arg in node.args]
        args = []
        for arg in rargs:
            args.append(arg[0]) 
        
        return (math.sqrt(*args), 'Number')

    @visitor.when(Range)
    def visit(self, node: Range, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        args = [self.visit(arg, scope, func_name, parent_scope) for arg in node.args]
        args_int = []
        for i in range(len(args)):
            args_int.append(int(args[i]))
        return (list(range(*args_int)), 'Vector')

    @visitor.when(While)
    def visit(self, node: While, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        stop = self.visit(node.stop, scope, func_name, parent_scope)[0]

        if not stop:
            body, body_type = self.visit(node.value, scope, func_name, parent_scope)
            if body_type == 'Number':
                return (0, body_type)
            elif body_type == 'String':
                return ('', body_type)
            elif body_type == 'Boolean':
                return (False, body_type)
            else:
                return (None, body_type)
        while stop:
            body, body_type = self.visit(node.value, scope, func_name, parent_scope)

            stop, _ = self.visit(node.stop, scope, func_name, parent_scope)

        return body, body_type

    @visitor.when(For)
    def visit(self, node: For, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        if node.collection.value == 'range':
            x = int(self.visit(node.collection.args[0],scope, func_name, parent_scope))
            y = int(self.visit(node.collection.args[1],scope, func_name, parent_scope))
            for item in range(x, y):
                body_scope = scope.create_child_scope()
                body_scope.define_variable(node.item, item, 'Number')
                value = self.visit(node.value, body_scope, func_name, parent_scope)
        else:
            for item in self.visit(node.collection, scope, func_name, parent_scope):
                body_scope = scope.create_child_scope()
                body_scope.define_variable(node.item, item, node.item.type)
                value = self.visit(node.value, body_scope, func_name, parent_scope)
        return value    
        
    @visitor.when(Base)
    def visit(self, node: Base, scope: ScopeInterpreter, func_name = None, parent_scope: ScopeInterpreter = None):
        args = []
        if node.args:
            args = [self.visit(arg, scope, func_name, parent_scope) for arg in node.args]
        func = parent_scope.get_local_function(func_name)

        return func(*args)

    @visitor.when(Property)
    def visit(self, node: Property, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        value_exp, value_type = self.visit(node.value, scope, func_name, parent_scope)
        scope.define_variable(node.name, value_exp, value_type)
            
        value_body = self.visit( node.value, scope, func_name, parent_scope) 
        return value_body

    @visitor.when(CreateInstance)
    def visit(self, node: CreateInstance, scope: ScopeInterpreter, func_name = None, parent_scope = None):
        if node.params:
            params_value = [self.visit(param, scope, func_name, parent_scope) for param in node.params]
        else:
            params_value = []
        type_value = self.types[node.value]
        type_scope = type_value(*params_value)
        return type_scope