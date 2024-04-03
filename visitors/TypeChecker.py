from abc import ABC, abstractmethod
from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError, Type
from tools import visitor
from tools.semantic import Scope

class TypeChecker(object):
    def __init__(self, context: Context,scope: Scope, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors
        self.scope = scope
        self.last_visited_func = -1
        self.last_visited_type = -1
        self.scope_iter = iter(scope)
        next(self.scope_iter)
            
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(Program)
    def visit(self, node: Program):
        if not self.scope:
            scope = Scope()
        for child in node.statements:
            if isinstance(child, Function):
                next_scope = next(self.scope_iter)
                self.visit(child, next_scope)
            else:
                self.visit(child, self.scope)
        return self.scope

    @visitor.when(Function)
    def visit(self, node: Function, scope: Scope):
        
        try:
            if node.type:
                return_type = self.context.get_protocol_or_type(node.type)
            else:
                return_type = self.context.get_protocol_or_type("Dinamic")
                fun = scope.get_function_info(node.name, len(node.params)if node.params else 0)
                fun.return_type = return_type
    
        except SemanticError as se:
            self.errors.append(se.text)
            
        # Verificar el cuerpo de la función
        
        body_type = self.visit(node.body, scope)

        if isinstance(node.body, Invoke):
            body_type = self.context.get_type("Dinamic")
        
        if not body_type.conforms(return_type):
            self.errors.append(f'TypeError: Return type {body_type.name} does not conform to declared return type {node.type}')
            
    
        # Devolver el tipo de retorno de la función
        return return_type
    
    @visitor.when(Call)
    def visit(self, node: Call, scope: Scope):
        # Obtener la función llamada por su nombre
        try:
            function = scope.get_function_info(node.value, len(node.args))
        except SemanticError as se:
            self.errors.append(se.text)
            return self.context.get_protocol_or_type('ErrorType') # Retornar un tipo de error como marcador de posición
    
        # Verificar que el número de argumentos sea correcto
        if len(node.args) != len(function.params):
            self.errors.append(f'TypeError: Incorrect number of arguments for function {node.idx}')
            return self.context.get_protocol_or_type('ErrorType') # Retornar un tipo de error como marcador de posición
    
        # Verificar que los tipos de los argumentos sean compatibles con los parámetros de la función
        for arg, param_type in zip(node.args, function.params):
            # arg_type = self.visit(arg, scope)
            
            try:
                arg_type = self.context.get_protocol_or_type(scope.get_variable(arg.value))
            except:
                arg_type = self.context.get_protocol_or_type("Dinamic")
                
            try:
                param_type = self.context.get_protocol_or_type(param_type.name)
            except:
                param_type = self.context.get_protocol_or_type("Dinamic")
            
           
            if not arg_type.conforms(param_type):
                self.errors.append(f'TypeError: Argument type {arg_type.name} does not conform to parameter type {param_type.name} in function call {node.idx}')
    
        # Devolver el tipo de retorno de la función
        return function.return_type
    
    @visitor.when(Block)
    def visit(self, node: Block, scope: Scope):
        for child in node.value:
            type = self.visit(child, scope)
    
        return type
    
    @visitor.when(LetList)
    def visit(self, node: LetList, scope: Scope):
        return self.visit(node.child, scope)
    
    @visitor.when(Let)
    def visit(self, node: Let, scope: Scope):
        scope = next(self.scope_iter)
        # Realizar el chequeo de tipos para la expresión asignada
        type_expr = self.visit(node.expr, scope)
        
        # Verificar que el tipo de la expresión sea compatible con el tipo declarado
        if node.type is not None:
            declared_type = self.context.get_protocol_or_type(node.type)
            if not type_expr.conforms(declared_type):
                self.errors.append(f'TypeError: Type {type_expr.name} does not conform to {node.type}')
        else:
            declared_type = self.context.get_protocol_or_type('Dinamic')
            if not type_expr.conforms(declared_type):
                self.errors.append(f'TypeError: Type {type_expr.name} does not conform to {node.type}')
            
        body_type = self.visit(node.value, scope)
        return body_type
    
    @visitor.when(Property)
    def visit(self, node: Property, scope: Scope):
        try:
            var_info = scope.get_variable(node.name)
            if var_info.var_type:
                return self.context.get_protocol_or_type(var_info.var_type)
            else:
                return self.context.get_protocol_or_type("Dinamic")
        
        except SemanticError as se:
            self.errors.append(se.text)
    
    @visitor.when(TypeDef)
    def visit(self, node: TypeDef, scope: Scope):
        scope = next(self.scope_iter)
        
        if node.args:
            for i in len(node.args):
                if not node.args[i].conform(node.inner_args[i]):
                    self.errors.append(f'TypeError: Type {node.args[i]} does not conform to {node.inner_args[i]}')
        
        attr_scope = scope.class_def['atributes']
        if node.body:
            for statement in node.body:
                if isinstance(statement, Function):
                    continue
                type_fun = self.visit(statement, attr_scope)    
               
        funcs_scope = scope.class_def['functions']
        if node.body:
            for statement in node.body:
                if isinstance(statement, Property):
                    continue
                type_prop = self.visit(statement, funcs_scope) 
    
    @visitor.when(Invoke)
    def visit(self, node: Invoke, scope: Scope):
        
        if node.value.value == "self":
            return self.context.get_type("Dinamic")
         
    @visitor.when(Plus)
    def visit(self, node: Plus, scope: Scope):
        
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        number_type = self.context.get_protocol_or_type("Number")
        if (not left_type.conforms(number_type)) and (not right_type.conforms(number_type)):
            self.errors.append(f'TypeError: Operands of Plus operation must conform to Number type')
        
        return number_type
    
    @visitor.when(BinaryMinus)
    def visit(self, node: BinaryMinus, scope: Scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        number_type = self.context.get_protocol_or_type("Number")
        if (not left_type.conforms(number_type)) and (not right_type.conforms(number_type)):
            self.errors.append(f'TypeError: Operands of Minus operation must conform to Number type')
        
        return number_type
    
    @visitor.when(Star)
    def visit(self, node: Star, scope: Scope):
        
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        number_type = self.context.get_protocol_or_type("Number")
        if (not left_type.conforms(number_type)) and (not right_type.conforms(number_type)):
            self.errors.append(f'TypeError: Operands of Star operation must conform to Number type')
        
        return number_type
    
    @visitor.when(Pow)
    def visit(self, node: Pow, scope: Scope):
        
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        number_type = self.context.get_protocol_or_type("Number")
        if (not left_type.conforms(number_type)) and (not right_type.conforms(number_type)):
            self.errors.append(f'TypeError: Operands of Pow operation must conform to Number type')
        
        return number_type
    
    @visitor.when(Div)
    def visit(self, node: Div, scope: Scope):
        
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        number_type = self.context.get_protocol_or_type("Number")
        if (not left_type.conforms(number_type)) and (not right_type.conforms(number_type)):
            self.errors.append(f'TypeError: Operands of Div operation must conform to Number type')
        
        return number_type
    
    @visitor.when(Mod)
    def visit(self, node: Mod, scope: Scope):
        
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        
        return left_type
    
    @visitor.when(Is)
    def visit(self, node: Is, scope: Scope):
        
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
           
        return left_type
    
    @visitor.when(As)
    def visit(self, node: As, scope: Scope):
        
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        return left_type
    
    @visitor.when(At)
    def visit(self, node: At, scope: Scope):
        
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        string_type = self.context.get_protocol_or_type("String")
        number_type = self.context.get_protocol_or_type("Number")
        if (not left_type.conforms(number_type)) and (not right_type.conforms(number_type)):
            self.errors.append(f'TypeError: Operands of At operation must conform to String or Number type')
        if (not left_type.conforms(string_type)) and (not right_type.conforms(string_type)):
            self.errors.append(f'TypeError: Operands of At operation must conform to String or Number type')
        
        return string_type
    
    @visitor.when(DoubleAt)
    def visit(self, node: DoubleAt, scope: Scope):
        
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        return left_type
    
    @visitor.when(Or)
    def visit(self, node: Or, scope: Scope):
        
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        return left_type
    
    @visitor.when(And)
    def visit(self, node: And, scope: Scope):
       
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of Plus operation must be of the same type')
    
        return left_type
    
    @visitor.when(GreaterThan)
    def visit(self, node: GreaterThan, scope: Scope):
        
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of GreaterThan operation must be of the same type')
    
        return self.context.get_protocol_or_type('Boolean')
    
    
    @visitor.when(LessThan)
    def visit(self, node: LessThan, scope: Scope):
        
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of GreaterThan operation must be of the same type')
    
        return self.context.get_protocol_or_type('Boolean')
    
    @visitor.when(GreaterEqual)
    def visit(self, node: GreaterEqual, scope: Scope):
        
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of GreaterThan operation must be of the same type')
    
        return self.context.get_protocol_or_type('Boolean')
    
    @visitor.when(LessEqual)
    def visit(self, node: LessEqual, scope: Scope):   
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of GreaterThan operation must be of the same type')
    
        return self.context.get_protocol_or_type('Boolean')
    
    @visitor.when(NotEqual)
    def visit(self, node: NotEqual, scope: Scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of GreaterThan operation must be of the same type')
    
        return self.context.get_protocol_or_type('Boolean')
    
    @visitor.when(CompareEqual)
    def visit(self, node: CompareEqual, scope: Scope):
        # Verificar que los operandos de la operación sean del tipo correcto
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.value, scope)
        if not left_type.conforms(right_type):
            self.errors.append(f'TypeError: Operands of GreaterThan operation must be of the same type')
    
        return self.context.get_protocol_or_type('Boolean')
    
    @visitor.when(Not)
    def visit(self, node: Not, scope: Scope):
        operand_type = self.visit(node.value, scope)
        if not operand_type.conforms(self.context.get_protocol_or_type('Bool')):
            self.errors.append(f'TypeError: Operand of Not operation must be of type Bool')
    
        return self.context.get_protocol_or_type('Boolean')
    
    @visitor.when(Print)
    def visit(self, node: Print, scope: Scope):
        for arg in node.args:
            arg_type = self.visit(arg, scope)
        
        if  (not arg_type.conforms(self.context.get_protocol_or_type("Number"))) and (not arg_type.conforms(self.context.get_protocol_or_type("String"))):
            self.errors.append(SemanticError("Print arguments must be of type Number or String"))# TODO: Make this with conforms
        
        return self.context.get_protocol_or_type('Dinamic')
    
    @visitor.when(Branch)
    def visit(self, node: Branch, scope: Scope):
        condicion_type = self.visit(node.condition, scope)
        if not condicion_type.conforms(self.context.get_protocol_or_type('Boolean')):
            self.errors.append(f'TypeError: Conditional expression must be of type Bool')
        self.visit(node.value, scope)
        return self.context.get_protocol_or_type('Dinamic')
    
        
    @visitor.when(Conditional)
    def visit(self, node: Conditional, scope: Scope):
        
        if_expr_type = self.visit(node.if_expr, scope)
        if not if_expr_type.conforms(self.context.get_protocol_or_type('Boolean')):
            self.errors.append(f'TypeError: Conditional expression must be of type Bool')
    
        # Realizar el chequeo de tipos para el cuerpo del if
        self.visit(node.if_body, scope)
    
        # Realizar el chequeo de tipos para el cuerpo del else
        self.visit(node.else_body, scope)
    
        # Si hay ramas adicionales, realizar el chequeo de tipos para cada una de ellas
        if node.branches:
            for branch in node.branches:
                self.visit(branch, scope)
    
        return self.context.get_protocol_or_type('Dinamic')
    
    @visitor.when(For)
    def visit(self, node: For, scope: Scope):
        
        # Verificar que el tipo de la colección sea Vector
        collection_type = self.visit(node.collection, scope)
        if not collection_type.conforms(self.context.get_protocol_or_type('Vector')):
            self.errors.append(f'TypeError: For loop collection must be of type Vector')
    
        # Realizar el chequeo de tipos para el cuerpo del bucle
        self.visit(node.body, scope) # TODO moverme scope
    
        return self.context.get_protocol_or_type('Dinamic')
    
    @visitor.when(While)
    def visit(self, node: While, scope: Scope):
        # Verificar que el tipo de la expresión de parada sea Bool
        stop_expr_type = self.visit(node.stop, scope)
        if not stop_expr_type.conforms(self.context.get_protocol_or_type('Boolean')):
            self.errors.append(f'TypeError: While loop stop condition must be of type Bool')
    
        # Realizar el chequeo de tipos para el cuerpo del bucle
        self.visit(node.value, scope)
    
        return self.context.get_protocol_or_type('Dinamic')
    
    @visitor.when(Var)
    def visit(self, node: Var, scope: Scope):
        # Buscar el tipo de la variable en el alcance actual
        try:
            var_info = scope.get_variable(node.value)
            if var_info.var_type:
                return self.context.get_protocol_or_type(var_info.var_type)
            else:
                return self.context.get_protocol_or_type("Dinamic")
        except SemanticError as se:
            self.errors.append(se.text)
           

    @visitor.when(Str)
    def visit(self, node: Number, scope: Scope):
        return self.context.get_protocol_or_type('String')
    
    @visitor.when(Number)
    def visit(self, node: Number, scope: Scope):
        return self.context.get_protocol_or_type('Number')
    
    @visitor.when(Bool)
    def visit(self, node: Number, scope: Scope):
        return self.context.get_protocol_or_type('Bool')
    
    @visitor.when(Vector)
    def visit(self, node: Vector, scope: Scope):
        # Verificar que los valores del vector sean del tipo correcto
        for value in node.lex:
            value_type = self.visit(value, scope)
            # Aquí asumimos que el tipo correcto para los valores del vector es Number
            if not value_type.conforms(self.context.get_protocol_or_type('Number')):
                self.errors.append(f'TypeError: Vector values must be of type Number')
    
        # Verificar que la longitud del vector sea un número entero
        if not isinstance(node.len, int):
            self.errors.append(f'TypeError: Vector length must be an integer')
    
        # Devolver el tipo de la expresión vector, que es Vector
        return self.context.get_protocol_or_type('Vector')
    
    @visitor.when(Sin)
    def visit(self, node: Sin, scope: Scope):
        # Verificar que el argumento de la función sin es del tipo correcto
        for arg in node.args:
            type_arg = self.visit(arg, scope)
            if not type_arg.conforms(self.context.get_protocol_or_type('Number')):
                self.errors.append(f'TypeError: Argument of sin function must be of type Number')
        # Devolver el tipo de la función sin, que es Number
        return self.context.get_protocol_or_type('Number')
    
    @visitor.when(Cos)
    def visit(self, node: Cos, scope: Scope):
        # Verificar que el argumento de la función cos es del tipo correcto
        for arg in node.args:
            type_arg = self.visit(arg, scope)
            if not type_arg.conforms(self.context.get_protocol_or_type('Number')):
                self.errors.append(f'TypeError: Argument of cos function must be of type Number')
        # Devolver el tipo de la función sin, que es Number
        return self.context.get_protocol_or_type('Number')
    
    @visitor.when(Log)
    def visit(self, node: Log, scope: Scope):
        # Verificar que los argumentos de la función log sean del tipo correcto
        for arg in node.args:
            type_arg = self.visit(arg, scope)
            if not type_arg.conforms(self.context.get_protocol_or_type('Number')):
                self.errors.append(f'TypeError: Argument of log function must be of type Number')
        # Devolver el tipo de la función sin, que es Number
        return self.context.get_protocol_or_type('Number')
    
    @visitor.when(Sqrt)
    def visit(self, node: Sqrt, scope: Scope):
        # Verificar que los argumentos de la función sqrt sean del tipo correcto
        for arg in node.args:
            type_arg = self.visit(arg, scope)
            if not type_arg.conforms(self.context.get_protocol_or_type('Number')):
                self.errors.append(f'TypeError: Argument of sqrt function must be of type Number')
        # Devolver el tipo de la función sin, que es Number
        return self.context.get_protocol_or_type('Number')
    
    @visitor.when(Range)
    def visit(self, node: Range, scope: Scope):
        # Verificar que los argumentos de la función range sean del tipo correcto
        for arg in node.args:
            arg_type = self.visit(arg, scope)
            if not arg_type.conforms(self.context.get_protocol_or_type('Number')):
                self.errors.append(f'TypeError: Argument of range function must be of type Number')
    
        # Devolver el tipo de la expresión range, que es Vector
        return self.context.get_protocol_or_type('Vector')
    
    @visitor.when(Assign)
    def visit(self, node: Assign, scope: Scope):
        
        node_type = self.visit(node.value, scope)
        body_type = self.visit(node.body, scope)
        
        if not body_type.conforms(node_type):
            self.errors.append(f'TypeError: errorrr')

        return body_type
    
    @visitor.when(Pi)
    def visit(self, node:Pi, scope: Scope):
        return self.context.get_protocol_or_type("Number")
    
    @visitor.when(E)
    def visit(self, node:E, scope: Scope):
        return self.context.get_protocol_or_type("Number")