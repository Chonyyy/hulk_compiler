from abc import ABC, abstractmethod
from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError, Type
from tools import visitor
from tools.semantic import Scope, Variable
from hulk_definitions.types import * 

class TypeInferer(object):
    def __init__(self, context: Context, errors=[]):
        self.context = context
        self.errors = errors

        self.type: Type = None
    
    def _get_safe_type(self, type, ctx: Context):
        try:
            type = ctx.get_protocol_or_type(type)            
            return type

        except SemanticError:
            self.errors.append(f'Name {type} is not a defined Type or Protocol.')

    def _infer(self, node: Expression, scope: Scope, new_type: Union[Type, Protocol]):
        if isinstance(node, Var):
            temp = scope.get_variable(node.value)
            var: Variable = temp[1]
            i: int = temp[0]

            if var.type is None:
                var.set_type(new_type)
                self.occurs = True

            elif isinstance(var.type, UnionType):
                itsc = var.type & new_type
                l = len(itsc)
                if 0 < l < len(var.type):
                    self.occurs = True

                    if l == 1:
                        type, *_ = itsc
                        var.set_type(type)
                    else:
                        var.set_type(itsc)

    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Number)
    def visit(self, node: Number):
        return NUMBER_TYPE
    
    @visitor.when(Str)
    def visit(self, node: Str):
        return STRING_TYPE
    
    @visitor.when(Bool)
    def visit(self, node: Bool):
        return BOOLEAN_TYPE
    
    @visitor.when(Function)
    def visit(self, node: Function, ctx: Context):
        pass

    @visitor.when(Program)
    def visit(self, node: Program):
        for child in node.statements:
            self.visit(child, self.context)

        return self.errors
    
    @visitor.when(CreateInstance)
    def visit(self, node: CreateInstance, ctx: Context, scope: Scope):
        for arg in node.args:
            self.visit(arg, ctx, scope)

        it = self._get_safe_type(node.type, ctx)
        for arg, pt in zip(node.args, it.params.values()):
            if pt is not None:
                self._infer(arg, scope, pt)

        return it

    @visitor.when(Let)
    def visit(self, node: Let, ctx: Context):
        if node.type != None:
            try:
                ctx.get_protocol_or_type(node.type)
                node.type = [node.type]
                
                return node.type

            except SemanticError:
                self.errors.append(f'Variable {node.name} is not a defined Type or Protocol.')

        else:
            types = []
            expr_type = self.visit(node.expr)
            
            if expr_type != None:
                types + expr_type
                node.type = types

            else:
                self.errors.append(f"Variable {node.name}'s type can't be enfered")
            
            return types

    @visitor.when(Assign)
    def visit(self, node: Assign, ctx: Context):
        pass

    @visitor.when(Conditional)
    def visit(self, node: Conditional, ctx: Context):
        pass

    @visitor.when(For)
    def visit(self, node: For, ctx: Context):
        pass

    @visitor.when(While)
    def visit(self, node: While, ctx: Context):
        pass

    @visitor.when(Block)
    def visit(self, node: Block, ctx: Context):
        pass

    @visitor.when(LetList)
    def visit(self, node: LetList, ctx: Context):
        pass

    @visitor.when(Branch)
    def visit(self, node: Branch, ctx: Context):
        pass

    @visitor.when(Plus)
    def visit(self, node: Block, ctx: Context):
        pass

    @visitor.when(BinaryMinus)
    def visit(self, node: BinaryMinus, ctx: Context):
        pass

    @visitor.when(UnaryMinus)
    def visit(self, node: UnaryMinus, ctx: Context):
        pass

    @visitor.when(Star)
    def visit(self, node: Star, ctx: Context):
        pass
 
    @visitor.when(Pow)
    def visit(self, node: Pow, ctx: Context):
        pass
 
    @visitor.when(Div)
    def visit(self, node: Div, ctx: Context):
        pass
 
    @visitor.when(Mod)
    def visit(self, node: Mod, ctx: Context):
        pass
 
    @visitor.when(Is)
    def visit(self, node: Is, ctx: Context):
        pass
 
    @visitor.when(As)
    def visit(self, node: As, ctx: Context):
        pass
 
    @visitor.when(At)
    def visit(self, node: At, ctx: Context):
        pass
 
    @visitor.when(DoubleAt)
    def visit(self, node: DoubleAt, ctx: Context):
        pass
 
    @visitor.when(Or)
    def visit(self, node: And, ctx: Context):
        pass
 
    @visitor.when(GreaterThan)
    def visit(self, node: GreaterThan, ctx: Context):
        pass
 
    @visitor.when(LessThan)
    def visit(self, node: LessThan, ctx: Context):
        pass
 
    @visitor.when(NotEqual)
    def visit(self, node: NotEqual, ctx: Context):
        pass
 
    @visitor.when(GreaterEqual)
    def visit(self, node: GreaterEqual, ctx: Context):
        pass
 
    @visitor.when(LessEqual)
    def visit(self, node: LessEqual, ctx: Context):
        pass
 
    @visitor.when(CompareEqual)
    def visit(self, node: CompareEqual, ctx: Context):
        pass
 
    @visitor.when(Not)
    def visit(self, node: Not, ctx: Context):
        pass

    @visitor.when(Call)
    def visit(self, node: Star, ctx: Context):
        pass
 
    @visitor.when(Invoke)
    def visit(self, node: Invoke, ctx: Context):
        pass

     
    @visitor.when(Vector)
    def visit(self, node: Vector, ctx: Context):
        pass

     
    @visitor.when(VectorComprehension)
    def visit(self, node: Vector, ctx: Context):
        pass
    
    @visitor.when(Var)
    def visit(self, node: Star, ctx: Context):
        pass
    
    @visitor.when(TypeDef)
    def visit(self, node: TypeDef, ctx: Context):
        pass
    
    @visitor.when(TypeCreation)
    def visit(self, node: TypeCreation, ctx: Context):
        pass
    
    @visitor.when(Protocol)
    def visit(self, node: Protocol, ctx: Context):
        pass

    @visitor.when(Assign)
    def visit(self, node: Assign, ctx: Context):
        pass
    
    @visitor.when(Pi)
    def visit(self, node: Pi, ctx: Context):
        return NUMBER_TYPE
    
    @visitor.when(E)
    def visit(self, node: E, ctx: Context):
        return NUMBER_TYPE
    
    @visitor.when(Indexing)
    def visit(self, node: Indexing, ctx: Context):
        pass

    @visitor.when(Sin)
    def visit(self, node: Sin, ctx: Context):
        return NUMBER_TYPE
    
    @visitor.when(Cos)
    def visit(self, node: Cos, ctx: Context):
        return NUMBER_TYPE
   
    @visitor.when(Rand)
    def visit(self, node: Rand, ctx: Context):
        return NUMBER_TYPE

    @visitor.when(Exp)
    def visit(self, node: Exp, ctx: Context):
        return NUMBER_TYPE

    @visitor.when(Log)
    def visit(self, node: Log, ctx: Context):
        return NUMBER_TYPE

    @visitor.when(Print)
    def visit(self, node: Print, ctx: Context):
        return STRING_TYPE

    @visitor.when(Base)
    def visit(self, node: Base, ctx: Context):
        return NUMBER_TYPE

    @visitor.when(Property)
    def visit(self, node: Property, ctx: Context):
        return NUMBER_TYPE

    @visitor.when(CreateInstance)
    def visit(self, node: CreateInstance, ctx: Context):
        return NUMBER_TYPE
