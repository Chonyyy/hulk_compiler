from abc import ABC, abstractmethod
from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError, Type
from tools import visitor
from tools.semantic import Scope

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

