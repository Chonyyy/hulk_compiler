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

    @visitor.when(Conditional)
    def visit(self, node: Conditional, scope: Scope):
        raise Exception('Error: Conditional not implemented')
    
    @visitor.when(Branch)
    def visit(self, node: Branch, scope: Scope):
        raise Exception('Error: Branch not implemented')
    
    @visitor.when(At)
    def visit(self, node: At, scope: Scope):
        raise Exception('Error: At not implemented')
    
    @visitor.when(DoubleAt)
    def visit(self, node: DoubleAt, scope: Scope):
        raise Exception('Error: DoubleAt not implemented')
    
    @visitor.when(Or)
    def visit(self, node: Or, scope: Scope):
        raise Exception('Error: Or not implemented')
    
    @visitor.when(Plus)
    def visit(self, node: Plus, scope: Scope):
        raise Exception('Error: Plus not implemented')
    
    @visitor.when(BinaryMinus)
    def visit(self, node: BinaryMinus, scope: Scope):
        raise Exception('Error: BinaryMinus not implemented')
    
    @visitor.when(Star)
    def visit(self, node: Star, scope: Scope):
        raise Exception('Error: Star not implemented')
    
    @visitor.when(Div)
    def visit(self, node: Div, scope: Scope):
        raise Exception('Error: Div not implemented')
    
    @visitor.when(Mod)
    def visit(self, node: Mod, scope: Scope):
        raise Exception('Error: Mod not implemented')
    
    @visitor.when(And)
    def visit(self, node: And, scope: Scope):
        raise Exception('Error: And not implemented')
    
    @visitor.when(Not)
    def visit(self, node: Not, scope: Scope):
        raise Exception('Error: Not not implemented')
    
    @visitor.when(UnaryMinus)
    def visit(self, node: UnaryMinus, scope: Scope):
        raise Exception('Error: UnaryMinus not implemented')
    
    @visitor.when(GreaterThan)
    def visit(self, node: GreaterThan, scope: Scope):
        raise Exception('Error: GreaterThan not implemented')
    
    @visitor.when(LessThan)
    def visit(self, node: LessThan, scope: Scope):
        raise Exception('Error: LessThan not implemented')
    
    @visitor.when(GreaterEqual)
    def visit(self, node: GreaterEqual, scope: Scope):
        raise Exception('Error: GreaterEqual not implemented')
    
    @visitor.when(LessEqual)
    def visit(self, node: LessEqual, scope: Scope):
        raise Exception('Error: LessEqual not implemented')	
    
    @visitor.when(CompareEqual)
    def visit(self, node: CompareEqual, scope: Scope):
        raise Exception('Error: CompareEqual not implemented')
    
    @visitor.when(NotEqual)
    def visit(self, node: NotEqual, scope: Scope):
        raise Exception('Error: NotEqual not implemented')
    
    @visitor.when(Is)
    def visit(self, node: Is, scope: Scope):
        raise Exception('Error: Is not implemented')
    
    @visitor.when(Pow)
    def visit(self, node: Pow, scope: Scope):
        raise Exception('Error: Pow not implemented')
    
    @visitor.when(Number)
    def visit(self, node: Number, scope: Scope):
        raise Exception('Error: Number not implemented')
    
    @visitor.when(Var)
    def visit(self, node: Var, scope: Scope):
        raise Exception('Error: Var not implemented')
    
    @visitor.when(Bool)
    def visit(self, node: Bool, scope: Scope):
        raise Exception('Error: Bool not implemented')
    
    @visitor.when(Str)
    def visit(self, node: Str, scope: Scope):
        raise Exception('Error: Str not implemented')
    
    @visitor.when(As)
    def visit(self, node: As, scope: Scope):
        raise Exception('Error: As not implemented')
    
    @visitor.when(Vector)
    def visit(self, node: Vector, scope: Scope):
        raise Exception('Error: Vector not implemented')
    
    @visitor.when(VectorComprehension)
    def visit(self, node: VectorComprehension, scope: Scope):
        raise Exception('Error: VectorComprehension not implemented')
    
    @visitor.when(Sin)
    def visit(self, node: Sin, scope: Scope):
        raise Exception('Error: Sin not implemented')
    
    @visitor.when(Cos)
    def visit(self, node: Cos, scope: Scope):
        raise Exception('Error: Cos not implemented')
    
    @visitor.when(Rand)
    def visit(self, node: Rand, scope: Scope):
        raise Exception('Error: Rand not implemented')
    
    @visitor.when(Exp)
    def visit(self, node: Exp, scope: Scope):
        raise Exception('Error: Exp not implemented')
    
    @visitor.when(Log)
    def visit(self, node: Log, scope: Scope):
        raise Exception('Error: Log not implemented')
    
    @visitor.when(Sqrt)
    def visit(self, node: Sqrt, scope: Scope):
        raise Exception('Error: Sqrt not implemented')
    
    @visitor.when(Print)
    def visit(self, node: Print, scope: Scope):
        raise Exception('Error: Print not implemented')
    
    @visitor.when(Range)
    def visit(self, node: Range, scope: Scope):
        raise Exception('Error: Range not implemented')
    
    @visitor.when(Pi)
    def visit(self, node: Pi, scope: Scope):
        raise Exception('Error: Pi not implemented')
    
    @visitor.when(E)
    def visit(self, node: E, scope: Scope):
        raise Exception('Error: E not implemented')
    
    @visitor.when(Call)
    def visit(self, node: Call, scope: Scope):
        raise Exception('Error: Call not implemented')
    
    @visitor.when(While)
    def visit(self, node: While, scope: Scope):
        raise Exception('Error: While not implemented')
    
    @visitor.when(For)
    def visit(self, node: For, scope: Scope):
        raise Exception('Error: For not implemented')
    
    @visitor.when(ForVar)
    def visit(self, node: ForVar, scope: Scope):
        raise Exception('Error: ForVar not implemented')
    
    @visitor.when(Invoke)
    def visit(self, node: Invoke, scope: Scope):
        raise Exception('Error: Invoke not implemented')
    
    @visitor.when(Indexing)
    def visit(self, node: Indexing, scope: Scope):
        raise Exception('Error: Indexing not implemented')
    
    @visitor.when(TypeDef)
    def visit(self, node: TypeDef, scope: Scope):
        raise Exception('Error: TypeDef not implemented')
    
    @visitor.when(Base)
    def visit(self, node: Base, scope: Scope):
        raise Exception('Error: Base not implemented')
    
    @visitor.when(Property)
    def visit(self, node: Property, scope: Scope):
        raise Exception('Error: Property not implemented')
    
    @visitor.when(CreateInstance)
    def visit(self, node: CreateInstance, scope: Scope):
        raise Exception('Error: CreateInstance not implemented')
    
    @visitor.when(Protocol)
    def visit(self, node: Protocol, scope: Scope):
        raise Exception('Error: Protocol not implemented')
