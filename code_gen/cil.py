import tools.nbpackage
import tools.visitor as visitor
import tools.cil as cil
from tools.semantic import Scope, VariableInfo
from tools.cil import get_formatter
# from cp15 import run_pipeline as deprecated_pipeline

from hulk_definitions.ast import *

class BaseCOOLToCILVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context
    
    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property
    def instructions(self):
        return self.current_function.instructions
    
    def register_local(self, vinfo):
        vinfo.name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = cil.LocalNode(vinfo.name)
        self.localvars.append(local_node)
        return vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
    
    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'
    
    def register_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node
    
    def register_type(self, name):
        type_node = cil.TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node
    
class MiniCOOLToCILVisitor(BaseCOOLToCILVisitor):
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Program)
    def visit(self, node, scope):
        ######################################################
        # node.statements -> [ Statement ... ]
        ######################################################
        
        self.current_function = self.register_function('entry')# Registra una función de entrada llamada 'entry'. Esta función es el punto de inicio del programa.
        instance = self.define_internal_local()# Define una variable local interna para almacenar una instancia de la clase principal.
        result = self.define_internal_local()# Define otra variable local interna para almacenar el resultado de la llamada a la función principal.
        main_method_name = self.to_function_name('main', 'Main')#Genera el nombre de la función principal basado en el nombre de la clase principal ('Main').
        self.register_instruction(cil.AllocateNode('Main', instance))# Genera una instrucción CIL para asignar memoria para una instancia de la clase principal.
        self.register_instruction(cil.ArgNode(instance))# Genera una instrucción CIL para pasar la instancia de la clase principal como argumento a la función principal.
        self.register_instruction(cil.StaticCallNode(main_method_name, result))#Genera una instrucción CIL para llamar a la función principal y almacenar el resultado en la variable result.
        self.register_instruction(cil.ReturnNode(0))# Genera una instrucción CIL para retornar desde la función de entrada.
        self.current_function = None
        
        #El bucle for itera sobre cada declaración de clase en node.statements y llama al método visit para cada una, pasando la declaración de clase y el alcance correspondiente (child_scope). Esto permite que el compilador procese cada clase individualmente y genere el código CIL correspondiente.
        for statements, child_scope in zip(node.statements, scope.children):
            self.visit(statements, child_scope)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(Statement)
    def visit(self, node):
        pass
    
    @visitor.when(LetList)
    def visit(self, node: LetList, scope):
        for statement in node.children:
            self.visit(statement, scope)

    @visitor.when(Block)
    def visit(self, node: Block, scope):
        for statement in node.body:
            self.visit(statement, scope)

    @visitor.when(Let)
    def visit(self, node: Let, scope): # TODO revisar esto
        result = self.visit(node.expr, scope)
        local_var_name = self.define_internal_local()
        self.register_instruction(cil.AssignNode(local_var_name, result))
        self.register_local(VariableInfo(node.name, node.type, scope))


    @visitor.when(Function)
    def visit(self, node: Function, scope):# TODO revisar
        function_name = self.visit(node.body, scope)
        self.register_function(VariableInfo(node.name, node.params, node.type, function_name))

    @visitor.when(Conditional)
    def visit(self, node: Conditional, scope):
        # Para Conditional, visitamos la expresión de condición y luego visitamos el cuerpo del if y el else.
        condition_result = self.visit(node.if_expr, scope)
        if_label = self.define_internal_local()
        else_label = self.define_internal_local()
        end_label = self.define_internal_local()
        self.register_instruction(cil.GotoIfNode(condition_result, if_label))
        self.register_instruction(cil.GotoNode(else_label))
        self.register_instruction(cil.LabelNode(if_label))
        self.visit(node.if_body, scope)
        self.register_instruction(cil.GotoNode(end_label))
        self.register_instruction(cil.LabelNode(else_label))
        self.visit(node.else_body, scope)
        self.register_instruction(cil.LabelNode(end_label))

    @visitor.when(Branch)
    def visit(self, node: Branch, scope):
        # Para Branch, visitamos la condición y luego visitamos el cuerpo del branch.
        condition_result = self.visit(node.condition, scope)
        if_label = self.define_internal_local()
        end_label = self.define_internal_local()
        self.register_instruction(cil.GotoIfNode(condition_result, if_label))
        self.register_instruction(cil.GotoNode(end_label))
        self.register_instruction(cil.LabelNode(if_label))
        self.visit(node.body, scope)
        self.register_instruction(cil.LabelNode(end_label))

    @visitor.when(Expression)
    def visit(self, node):
        pass
    
    @visitor.when(Binary)
    def visit(self, node: Binary, scope):
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        result = self.define_internal_local()
        self.register_instruction(cil.ArithmeticNode(result, left, right))
        return result
    
    @visitor.when(Unary)
    def visit(self, node: Unary, scope):
        self.visit(node,scope)

    @visitor.when(Plus)
    def visit(self, node: Plus, scope):
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        result = self.define_internal_local()
        self.register_instruction(cil.PlusNode(result, left, right))
        return result
    
    @visitor.when(BinaryMinus)
    def visit(self, node, scope):
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        result = self.define_internal_local()
        self.register_instruction(cil.MinusNode(result, left, right))
        return result

    @visitor.when(Star)
    def visit(self, node:Star, scope):
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        result = self.define_internal_local()
        self.register_instruction(cil.StarNode(result,left, right))
        return result

    @visitor.when(Pow)
    def visit(self, node: Pow, scope):
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        result = self.define_internal_local()
        self.register_instruction(cil.ArithmeticNode(result, left, right))
        return result
    
    @visitor.when(Div)
    def visit(self, node: Div, scope):
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        result = self.define_internal_local()
        self.register_instruction(cil.DivNode(result, left, right))
        return result
    
    @visitor.when(Mod)
    def visit(self, node: Mod, scope):
        # Para Mod, visitamos los dos operandos y luego generamos una instrucción CIL para la operación de módulo.
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        result_var = self.define_internal_local()
        self.register_instruction(cil.ArithmeticNode(result_var, left_result, right_result))
        return result_var

    @visitor.when(Is)
    def visit(self, node: Is, scope):
        # Para Is, visitamos los dos operandos y luego generamos una instrucción CIL para la operación de igualdad.
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        result_var = self.define_internal_local()
        self.register_instruction(cil.ArithmeticNode(result_var, left_result, right_result))
        return result_var

    @visitor.when(As)
    def visit(self, node: As, scope):
        # Para As, visitamos los dos operandos y luego generamos una instrucción CIL para la operación de asignación.
        # Esto es un caso especial donde necesitamos asegurarnos de que el lado derecho se evalúa primero.
        right_result = self.visit(node.right, scope)
        self.register_instruction(cil.AssignNode(node.left.name, right_result))
        return right_result

    @visitor.when(At)
    def visit(self, node: At, scope):
        # Para At, visitamos los dos operandos y luego generamos una instrucción CIL para la operación de acceso a atributo.
        # Esto dependerá de cómo manejes los atributos en tu lenguaje de programación objetivo.
        # Aquí, asumimos que 'self.visit' devuelve el nombre de la variable local donde se almacena el resultado.
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        result_var = self.define_internal_local()
        self.register_instruction(cil.ArithmeticNode(result_var, left_result, right_result))
        return result_var

    @visitor.when(DoubleAt)
    def visit(self, node: DoubleAt, scope):
        # Para DoubleAt, visitamos los dos operandos y luego generamos una instrucción CIL para la operación de acceso a atributo de atributo.
        # Esto es similar a At, pero con una operación adicional.
        left_result = self.visit(node.left, scope)
        middle_result = self.visit(node.middle, scope)
        right_result = self.visit(node.right, scope)
        intermediate_var = self.define_internal_local()
        self.register_instruction(cil.ArithmeticNode(intermediate_var, left_result, middle_result))
        result_var = self.define_internal_local()
        self.register_instruction(cil.ArithmeticNode(result_var, intermediate_var, right_result))
        return result_var

    @visitor.when(Or)
    def visit(self, node: Or, scope):
        # Para Or, visitamos los dos operandos y luego generamos una instrucción CIL para la operación lógica OR.
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        result_var = self.define_internal_local()
        self.register_instruction(cil.ArithmeticNode(result_var, left_result, right_result))
        return result_var
    
    @visitor.when(And)
    def visit(self, node: And, scope):
        # Para And, visitamos los dos operandos y luego generamos una instrucción CIL para la operación lógica AND.
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        result_var = self.define_internal_local()
        self.register_instruction(cil.ArithmeticNode(result_var, left_result, right_result))
        return result_var
    
    @visitor.when(GreaterThan)
    def visit(self, node: GreaterThan, scope):
        # Para GreaterThan, visitamos los dos operandos y luego generamos una instrucción CIL para la operación de comparación mayor que.
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        result_var = self.define_internal_local()
        self.register_instruction(cil.ArithmeticNode(result_var, left_result, right_result))
        return result_var
    
    @visitor.when(LessThan)
    def visit(self, node: LessThan, scope):
        # Para LessThan, visitamos los dos operandos y luego generamos una instrucción CIL para la operación de comparación menor que.
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        result_var = self.define_internal_local()
        self.register_instruction(cil.ArithmeticNode(result_var, left_result, right_result))
        return result_var
    
    @visitor.when(GreaterEqual)
    def visit(self, node: GreaterEqual, scope):
        # Para GreaterEqual, visitamos los dos operandos y luego generamos una instrucción CIL para la operación de comparación mayor o igual que.
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        result_var = self.define_internal_local()
        self.register_instruction(cil.ArithmeticNode(result_var, left_result, right_result))
        return result_var
    
    @visitor.when(LessEqual)
    def visit(self, node: LessEqual, scope):
        # Para LessEqual, visitamos los dos operandos y luego generamos una instrucción CIL para la operación de comparación menor o igual que.
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        result_var = self.define_internal_local()
        self.register_instruction(cil.ArithmeticNode(result_var, left_result, right_result))
        return result_var
    
    @visitor.when(NotEqual)
    def visit(self, node: NotEqual, scope):
        # Para NotEqual, visitamos los dos operandos y luego generamos una instrucción CIL para la operación de comparación de desigualdad.
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        result_var = self.define_internal_local()
        self.register_instruction(cil.ArithmeticNode(result_var, left_result, right_result))
        return result_var
    
    @visitor.when(CompareEqual)
    def visit(self, node: CompareEqual, scope):
        # Para CompareEqual, visitamos los dos operandos y luego generamos una instrucción CIL para la operación de comparación de igualdad.
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        result_var = self.define_internal_local()
        self.register_instruction(cil.ArithmeticNode(result_var, left_result, right_result))
        return result_var
    
    @visitor.when(Not)
    def visit(self, node: Not, scope):
        # Para Not, visitamos el operando y luego generamos una instrucción CIL para la operación lógica NOT.
        operand_result = self.visit(node.right, scope)
        result_var = self.define_internal_local()
        self.register_instruction(cil.InstructionNode(result_var, operand_result)) # TODO revisar
        return result_var
    
    @visitor.when(UnaryMinus)
    def visit(self, node: UnaryMinus, scope):
        # Para UnaryMinus, visitamos el operando y luego generamos una instrucción CIL para la operación de negación unaria.
        operand_result = self.visit(node.right, scope)
        result_var = self.define_internal_local()
        self.register_instruction(cil.InstructionNode(result_var, operand_result))# TODO revisar
        return result_var
    
    @visitor.when(Atom)
    def visit(self, node: Atom, scope):
        # Para Atom, simplemente devolvemos el valor léxico.
        return node.lex
    
    @visitor.when(Call)
    def visit(self, node: Call, scope):
        # node.lex -> Atom
        # node.id -> str
        # node.args -> [ Expression... ]
        lex = self.visit(node.lex, scope)
        method_name = self.to_function_name(node.idx, self.current_type.name)
        args = [self.visit(arg, scope) for arg in node.args]
        result = self.define_internal_local()
        self.register_instruction(cil.DynamicCallNode(lex, method_name, args, result))
        return result
    
    
    @visitor.when(Number)
    def visit(self, node: Number, scope):
        # Para Number, creamos una instrucción CIL para asignar el valor numérico a una variable.
        result_var = self.define_internal_local()
        self.register_instruction(cil.AssignNode(result_var, node.lex))
        return result_var
    
    @visitor.when(Str)
    def visit(self, node: Str, scope):
        # Para Str, creamos una instrucción CIL para asignar el valor de cadena a una variable.
        result_var = self.define_internal_local()
        self.register_instruction(cil.AssignNode(result_var, node.lex))
        return result_var
    
    @visitor.when(Bool)
    def visit(self, node: Bool, scope):
        # Para Bool, creamos una instrucción CIL para asignar el valor booleano a una variable.
        result_var = self.define_internal_local()
        self.register_instruction(cil.AssignNode(result_var, node.lex))
        return result_var
    
    @visitor.when(Invoke)
    def visit(self, node: Invoke, scope):
        # Para Invoke, visitamos el contenedor y luego generamos una instrucción CIL para la invocación de método.
        container_result = self.visit(node.container, scope)
        result_var = self.define_internal_local()
        self.register_instruction(cil.DynamicCallNode(container_result, node.lex, result_var))
        return result_var
    
    @visitor.when(Vector)
    def visit(self, node: Vector, scope):
        # Para Vector, visitamos cada valor y luego generamos una instrucción CIL para la creación de un vector.
        values_result = [self.visit(value, scope) for value in node.lex]
        result_var = self.define_internal_local()
        self.register_instruction(cil.ArrayNode(result_var, node.len, values_result))
        return result_var
    
    @visitor.when(VectorComprehension)
    def visit(self, node: VectorComprehension, scope):
        # Para VectorComprehension, visitamos cada valor y luego generamos una instrucción CIL para la creación de un vector con comprensión.
        values_result = [self.visit(value, scope) for value in node.lex]
        operation_result = self.visit(node.operation, scope)
        result_var = self.define_internal_local()
        self.register_instruction(cil.ArrayNode(result_var, node.len, values_result, operation_result))
        return result_var

    @visitor.when(Var)
    def visit(self, node: Var, scope):
        # node.lex -> str
        return cil.LocalNode(node.lex)

    @visitor.when(TypeDef) # TODO: esto es d phind revisar
    def visit(self, node: TypeDef, scope):
        # Para TypeDef, creamos una instrucción CIL para definir un nuevo tipo.
        type_node = cil.TypeNode(node.name)
        self.register_instruction(type_node)
    
        # Visitamos el cuerpo y los argumentos para definir atributos y métodos.
        for attr in node.body:
            if hasattr(attr, 'params'): # Asumimos que los métodos tienen un atributo 'params'
                # Crear un nodo de método en CIL
                method_node = cil.FunctionNode(attr.name, attr.params, [], [])
                type_node.methods.append(method_node)
            else:
                # Crear un nodo de atributo en CIL
                attr_node = cil.AttributeNode(attr.name, attr.type)
                type_node.attributes.append(attr_node)
    
        # Visitamos los argumentos para definir los parámetros del tipo.
        for arg in node.args:
            # Asumimos que 'Arg' es una clase que representa un argumento en tu lenguaje.
            arg_cil = self.visit(arg, scope)
            type_node.args.append(arg_cil)
    
        # Si hay herencia, también la visitamos.
        if node.inheritance:
            inheritance_cil = self.visit(node.inheritance, scope)
            type_node.inheritance = inheritance_cil
    
        # Si hay argumentos internos, también los visitamos.
        if node.inner_args:
            for inner_arg in node.inner_args:
                inner_arg_cil = self.visit(inner_arg, scope)
                type_node.inner_args.append(inner_arg_cil)
    
        return type_node
    
    @visitor.when(TypeCreation)
    def visit(self, node: TypeCreation, scope):
        # Para TypeCreation, creamos una instrucción CIL para crear una instancia de un tipo.
        result_var = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(node.lex, result_var))
        return result_var
    
    @visitor.when(Protocol) #TODO: phind
    def visit(self, node: Protocol, scope):
        # Para Protocol, creamos una instrucción CIL para definir un nuevo protocolo.
        protocol_node = cil.TypeNode(node.name)
        self.register_instruction(protocol_node)

        # Visitamos el cuerpo para definir los métodos del protocolo.
        for method in node.body:
            # Asumimos que cada método en el cuerpo es un objeto con propiedades como 'name' y 'params'.
            method_node = cil.FunctionNode(method.name, method.params, [], [])
            protocol_node.methods.append(method_node)

        # Si hay una extensión, también la visitamos.
        if node.extension:
            extension_cil = self.visit(node.extension, scope)
            protocol_node.extension = extension_cil

        return protocol_node
    
    @visitor.when(Assign)
    def visit(self, node: Assign, scope):
        # Para Assign, visitamos el cuerpo y luego generamos una instrucción CIL para la asignación.
        value_result = self.visit(node.body, scope)
        self.register_instruction(cil.AssignNode(node.lex, value_result))
    
    @visitor.when(Pi)
    def visit(self, node: Pi, scope):
        # Para Pi, creamos una instrucción CIL para asignar el valor de Pi a una variable.
        result_var = self.define_internal_local()
        self.register_instruction(cil.AssignNode(result_var, 3.141592653589793))
        return result_var
    
    @visitor.when(E)
    def visit(self, node: E, scope):
        # Para E, creamos una instrucción CIL para asignar el valor de E a una variable.
        result_var = self.define_internal_local()
        self.register_instruction(cil.AssignNode(result_var, 2.718281828459045))
        return result_var
    
    @visitor.when(Indexing)
    def visit(self, node: Indexing, scope):
        # Para Indexing, visitamos el nombre y el índice y luego generamos una instrucción CIL para el acceso a un índice.
        name_result = self.visit(node.lex, scope)
        index_result = self.visit(node.index, scope)
        result_var = self.define_internal_local()
        self.register_instruction(cil.GetIndexNode(result_var, name_result, index_result))
        return result_var
    
    @visitor.when(Sin)
    def visit(self, node: Sin, scope):
        # Para Sin, visitamos los argumentos y luego generamos una instrucción CIL para la función sin.
        args_result = [self.visit(arg, scope) for arg in node.args]
        result_var = self.define_internal_local()
        self.register_instruction(cil.StaticCallNode("sin", result_var, args_result))
        return result_var   
    
    @visitor.when(Cos)
    def visit(self, node: Cos, scope):
        # Para Cos, visitamos los argumentos y luego generamos una instrucción CIL para la función cos.
        args_result = [self.visit(arg, scope) for arg in node.args]
        result_var = self.define_internal_local()
        self.register_instruction(cil.StaticCallNode("cos", result_var, args_result))
        return result_var
    
    @visitor.when(Rand)
    def visit(self, node: Rand, scope):
        # Para Rand, visitamos los argumentos y luego generamos una instrucción CIL para la función rand.
        args_result = [self.visit(arg, scope) for arg in node.args]
        result_var = self.define_internal_local()
        self.register_instruction(cil.StaticCallNode("rand", result_var, args_result))
        return result_var
    
    @visitor.when(Exp)
    def visit(self, node: Exp, scope):
        # Para Exp, visitamos los argumentos y luego generamos una instrucción CIL para la función exp.
        args_result = [self.visit(arg, scope) for arg in node.args]
        result_var = self.define_internal_local()
        self.register_instruction(cil.StaticCallNode("exp", result_var, args_result))
        return result_var
    
    @visitor.when(Log)
    def visit(self, node: Log, scope):
        # Para Log, visitamos los argumentos y luego generamos una instrucción CIL para la función log.
        args_result = [self.visit(arg, scope) for arg in node.args]
        result_var = self.define_internal_local()
        self.register_instruction(cil.StaticCallNode("log", result_var, args_result))
        return result_var
    
    @visitor.when(Sqrt)
    def visit(self, node: Sqrt, scope):
        # Para Sqrt, visitamos los argumentos y luego generamos una instrucción CIL para la función sqrt.
        args_result = [self.visit(arg, scope) for arg in node.args]
        result_var = self.define_internal_local()
        self.register_instruction(cil.StaticCallNode("sqrt", result_var, args_result))
        return result_var
    
    @visitor.when(Print)
    def visit(self, node: Print, scope):
        # Para Print, visitamos los argumentos y luego generamos una instrucción CIL para la función print.
        args_result = [self.visit(arg, scope) for arg in node.args]
        self.register_instruction(cil.PrintNode(args_result))
    
    @visitor.when(Range)
    def visit(self, node: Range, scope):
        # Para Range, visitamos los argumentos y luego generamos una instrucción CIL para la función range.
        args_result = [self.visit(arg, scope) for arg in node.args]
        result_var = self.define_internal_local()
        self.register_instruction(cil.StaticCallNode("range", result_var, args_result))
        return result_var
    
    @visitor.when(While)
    def visit(self, node: While, scope):
        # Para While, visitamos la condición y el cuerpo, y luego generamos una instrucción CIL para el bucle while.
        condition_result = self.visit(node.stop, scope)
        body_result = self.visit(node.body, scope)
        while_node = cil.WhileNode(condition_result, body_result)
        self.register_instruction(while_node)
    
    @visitor.when(For)
    def visit(self, node: For, scope):
        # Para For, visitamos el ítem, la colección y el cuerpo, y luego generamos una instrucción CIL para el bucle for.
        item_result = self.visit(node.item, scope)
        collection_result = self.visit(node.collection, scope)
        body_result = self.visit(node.body, scope)
        for_node = cil.ForNode(item_result, collection_result, body_result)
        self.register_instruction(for_node)
    
    @visitor.when(Self)
    def visit(self, node: Self, scope):
        # Para Self, simplemente devolvemos una referencia al objeto actual.
        return "self"
    
    @visitor.when(Property)
    def visit(self, node: Property, scope):
        # Para Property, visitamos el cuerpo y luego generamos una instrucción CIL para la propiedad.
        body_result = self.visit(node.body, scope)
        property_node = cil.PropertyNode(node.name, body_result, node.type)
        self.register_instruction(property_node)
        return property_node
    
    @visitor.when(CreateInstance)
    def visit(self, node: CreateInstance, scope):
        # Para CreateInstance, visitamos los parámetros y luego generamos una instrucción CIL para la creación de instancia.
        params_result = [self.visit(param, scope) for param in node.params]
        result_var = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(node.type, result_var))
        for param in params_result:
            self.register_instruction(cil.ArgNode(param))
        self.register_instruction(cil.StaticCallNode(node.type, result_var))
        return result_var
    
formatter = get_formatter()

# def run_pipelinecp14(G, text):
#     ast = deprecated_pipeline(G, text)
#     print('============== COLLECTING TYPES ===============')
#     errors = []
#     collector = TypeCollector(errors)
#     collector.visit(ast)
#     context = collector.context
#     print('Errors:', errors)
#     print('Context:')
#     print(context)
#     print('=============== BUILDING TYPES ================')
#     builder = TypeBuilder(context, errors)
#     builder.visit(ast)
#     print('Errors: [')
#     for error in errors:
#         print('\t', error)
#     print(']')
#     print('Context:')
#     print(context)
#     return ast, errors, context

# def run_pipelinecp15(G, text):
#     ast, errors, context = deprecated_pipeline(G, text)
#     print('=============== CHECKING TYPES ================')
#     checker = TypeChecker(context, errors)
#     scope = checker.visit(ast)
#     print('Errors: [')
#     for error in errors:
#         print('\t', error)
#     print(']')
#     return ast, errors, context, scope

def run_pipeline(G, text):
    ast, errors, context, scope = deprecated_pipeline(G, text)
    print('============= TRANSFORMING TO CIL =============')
    cool_to_cil = MiniCOOLToCILVisitor(context)
    cil_ast = cool_to_cil.visit(ast, scope)
    formatter = get_formatter()
    print(formatter(cil_ast))
    return ast, errors, context, scope, cil_ast