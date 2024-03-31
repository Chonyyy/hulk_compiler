from abc import ABC, abstractmethod
from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError, Type, Tuple
from tools import visitor
from tools.semantic import Scope, Variable
from tools.semantic import Function as Func
from hulk_definitions.types import * 
from hulk_definitions.names import *

class TypeInferer(object):
    def __init__(self, context: Context, scope: Scope, errors=[]):
        self.context: Context = context
        self.errors = errors
        self.scope: Scope = scope

        self.current_method: Func = None
        self.current_type: Type = None 

    def _infer(self, node: Expression, scope: Scope, new_type: Union[Type, Protocol]):
        if isinstance(node, Var):
            temp: Tuple[int, Variable] = scope.get_variable(node.value)
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
    def visit(self, node: Function, ctx: Context, scope: Scope):
        
        temp = scope.get_function(node.name)
        i: int = temp[0]
        f: Func = temp[1]
        child_scope: Scope = scope.children[i]

        rt = self.visit(node.body, ctx, child_scope)

        for name, pt in f.params:
            if pt is None:
                var: Variable = child_scope.get_variable(name)[1]
                if var.type is not None:
                    v = f.set_param_type(name, var.type)
                    if v is SemanticError:
                        self.errors.append(v.text)

        if f.return_type is None and rt is not None:
            f.set_return_type(rt)
            self.occurs = True

    @visitor.when(Program)
    def visit(self, node: Program, scope: Scope):

        for i, child in enumerate(node.statements):
            self.visit(child, self.context, scope.children[i])

        return self.errors

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
                self.errors.append(f"Variable {node.name}'s type can't be infered")
            
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
    def visit(self, node: Var, ctx: Context, scope: Scope):
        if (
            self.current_method is not None
            and node.value == INSTANCE_NAME
            and node.value not in self.current_method.params
            ):
            pscope = self._find_scope(node.lex)
            if pscope.is_function:
                return self.current_type

        i, var = scope.get_variable(node.value)
        if var is not None:
            return var.type

        return FUNCTION_TYPE
    
    def _find_var_scope(self, name: str, scope: Scope):
        if scope.get_local_variable(name) != None:
            return scope
        else:
            v = self._find_var_scope(name, scope.parent)
            if v != None:
                return v
            else:
                raise SemanticError(f'Variable {name} is not defined.')
    
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
