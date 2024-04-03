from abc import ABC, abstractmethod
from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError, Type
from tools import visitor
from tools.semantic import Scope
from hulk_definitions.types import * 
from hulk_definitions.names import *

class TypeInferer(object):
    def __init__(self, context: Context, scope: Scope, errors=[]):
        self.context = context
        self.errors: list = errors
        self.scope = scope

        self.type: Type = None
        self.current_method: Function = None

    def _infer(self, node: Expression, scope: Scope, new_type: Union[Type, Proto]):
        if isinstance(node, Var):
            var, nscope = scope.get_variable_and_scope(node.value)

            if var.var_type is None:
                var.set_type(new_type)
                self.occurs = True

            elif isinstance(var.var_type, UnionType):
                itsc = var.var_type & new_type
                l = len(itsc)
                if 0 < l < len(var.var_type):
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
        is_method = self.current_method is not None

        f = self.current_method if is_method else scope.find_function(node.name)

        child_scope: Scope = scope.to_root().create_child_scope(is_function_scope=True)
        for name, pt in f.params:
            child_scope.define_variable(name, pt)

        if is_method and INSTANCE_NAME not in f.params:
            child_scope.define_variable(INSTANCE_NAME, self.type)

        rt = self.visit(node.body, ctx, child_scope)

        # infer function param types
        for name, pt in f.params:
            if pt is None:
                var, _ = child_scope.get_variable_and_scope(name)
                if var.type is not None:
                    f.set_param_type(name, var.type)

        if f.type is None and rt is not None:
            f.set_type(rt)
            self.occurs = True

    @visitor.when(Program)
    def visit(self, node: Program, ctx: Context, scope: Scope):
        while True:
            self.occurs = False

            for decl in node.statements:
                if not isinstance(decl, Protocol):
                    self.visit(decl, ctx, scope)

            if self.occurs == False:
                break

        for type in ctx.types.values():
            for arg in type.args:
                name = arg[0]
                ptype = arg[1]
                if ptype is None:
                    self.errors.append(
                        f"Couldn't infer type of constructor param '{name}' of type '{type.name}'."
                    )

            for attr in type.attributes:
                if attr[1].type is None:
                    self.errors.append(
                        f"Couldn't infer type of attribute '{attr[1].name}' of type '{type.name}'."
                    )

            for method in type.methods:
                for param in method[1].params:
                    name = param[0]
                    ptype = param[1]
                    if ptype is None:
                        self.errors.append(
                            f"Couldn't infer type of param '{name}' of method '{type.name}.{method.name}'."
                        )

                if method.return_type is None:
                    self.errors.append(
                        f"Couldn't infer return type of method '{type.name}.{method.name}'."
                    )

        for f in scope.local_funcs:
            for param in f[1].params:
                name = param[0]
                type = param[1]
                if type is None:
                    self.errors.append(
                        f"Couldn't infer type of param '{name}' of function '{f[1].name}'."
                    )

            if f[1].return_type is None:
                self.errors.append(
                    f"Couldn't infer return type of function '{f[1].name}'."
                )

        return node

    @visitor.when(Let)
    def visit(self, node: Let, ctx: Context, scope: Scope):
        vt = self.visit(node.value, ctx, scope)
        at = ctx.get_protocol_or_type(node.type, ctx)

        child_scope = scope.create_child_scope()
        child_scope.define_variable(node.name, at if at is not None else vt)

        return self.visit(node.value, ctx, child_scope)

    @visitor.when(Conditional)
    def visit(self, node: Conditional, ctx: Context, scope: Scope):
        branch_types = []
        
        tt = self.visit(node.if_body, ctx, scope.create_child_scope())
        self._infer(node.if_expr, scope, BOOLEAN_TYPE)
        for cond, branch in node.branches:
            self.visit(cond, ctx, scope)

            bt = self.visit(branch, ctx, scope.create_child_scope())
            branch_types.append(bt)

        et = self.visit(node.else_body, ctx, scope.create_child_scope())
        branch_types.append(et)
        branch_types.append(tt)

        for cond, _ in node.branches:
            self._infer(cond, scope, BOOLEAN_TYPE)

        if any(bt is None for bt in branch_types):
            return None

        return union_type(*branch_types)

    @visitor.when(For)
    def visit(self, node: For, ctx: Context, scope: Scope):
        self.visit(node.collection, ctx, scope)
        bt = self.visit(node.value, ctx, scope.create_child_scope())

        self._infer(node.collection, scope, VectorType(OBJECT_TYPE))

        if bt is None:
            return None

        return bt

    @visitor.when(While)
    def visit(self, node: While, ctx: Context, scope: Scope):
        self.visit(node.stop, ctx, scope)
        bt = self.visit(node.value, ctx, scope.create_child_scope())

        self._infer(node.stop, scope, BOOLEAN_TYPE)

        if bt is None:
            return None

        return bt

    @visitor.when(Block)
    def visit(self, node: Block, ctx: Context, scope: Scope):
        type = None
        for expr in node.value:
            type = self.visit(expr, ctx, scope.create_child_scope())

        return type

    @visitor.when(LetList)
    def visit(self, node: LetList, ctx: Context, scope: Scope):
        self.visit(node.child, ctx, scope)

    @visitor.when(Branch)
    def visit(self, node: Branch, ctx: Context, scope: Scope):
        self.visit(node.left, ctx, scope)
        self.visit(node.value, ctx, scope)

        self._infer(node.left, scope, NUMBER_TYPE)
        self._infer(node.value, scope, NUMBER_TYPE)

        return NUMBER_TYPE

    @visitor.when(Plus)
    def visit(self, node: Block, ctx: Context, scope: Scope):
        self.visit(node.left, ctx, scope)
        self.visit(node.value, ctx, scope)

        self._infer(node.left, scope, NUMBER_TYPE)
        self._infer(node.value, scope, NUMBER_TYPE)

        return NUMBER_TYPE

    @visitor.when(BinaryMinus)
    def visit(self, node: BinaryMinus, ctx: Context, scope: Scope):
        self.visit(node.left, ctx, scope)
        self.visit(node.value, ctx, scope)

        self._infer(node.left, scope, NUMBER_TYPE)
        self._infer(node.value, scope, NUMBER_TYPE)

        return NUMBER_TYPE

    @visitor.when(UnaryMinus)
    def visit(self, node: UnaryMinus, ctx: Context, scope: Scope):
        self.visit(node.value, ctx, scope)

        self._infer(node.value, scope, NUMBER_TYPE)

        return NUMBER_TYPE

    @visitor.when(Star)
    def visit(self, node: Star, ctx: Context, scope: Scope):
        self.visit(node.left, ctx, scope)
        self.visit(node.value, ctx, scope)

        self._infer(node.left, scope, NUMBER_TYPE)
        self._infer(node.value, scope, NUMBER_TYPE)

        return NUMBER_TYPE
 
    @visitor.when(Pow)
    def visit(self, node: Pow, ctx: Context, scope: Scope):
        self.visit(node.left, ctx, scope)
        self.visit(node.value, ctx, scope)

        self._infer(node.left, scope, NUMBER_TYPE)
        self._infer(node.value, scope, NUMBER_TYPE)

        return NUMBER_TYPE
 
    @visitor.when(Div)
    def visit(self, node: Div, ctx: Context, scope: Scope):
        self.visit(node.left, ctx, scope)
        self.visit(node.value, ctx, scope)

        self._infer(node.left, scope, NUMBER_TYPE)
        self._infer(node.value, scope, NUMBER_TYPE)

        return NUMBER_TYPE
 
    @visitor.when(Mod)
    def visit(self, node: Mod, ctx: Context, scope: Scope):
        self.visit(node.left, ctx, scope)
        self.visit(node.value, ctx, scope)

        self._infer(node.left, scope, NUMBER_TYPE)
        self._infer(node.value, scope, NUMBER_TYPE)

        return NUMBER_TYPE
 
    @visitor.when(Is)
    def visit(self, node: Is, ctx: Context, scope: Scope):
        self.visit(node.value, ctx, scope)

        return BOOLEAN_TYPE
 
    @visitor.when(As)
    def visit(self, node: As, ctx: Context, scope: Scope):
        self.visit(node.value, ctx, scope)
        try:
            type = ctx.get_protocol_or_type(node.left, ctx)
        except SemanticError as se:
            self.errors.append(se.text)
        return type
 
    @visitor.when(At)
    def visit(self, node: At, ctx: Context, scope: Scope):
        self.visit(node.left, ctx, scope)
        self.visit(node.value, ctx, scope)

        ut = union_type(NUMBER_TYPE, STRING_TYPE)
        self._infer(node.left, scope, ut)
        self._infer(node.value, scope, ut)

        return STRING_TYPE
 
    @visitor.when(DoubleAt)
    def visit(self, node: DoubleAt, ctx: Context, scope: Scope):
        self.visit(node.left, ctx, scope)
        self.visit(node.value, ctx, scope)

        ut = union_type(NUMBER_TYPE, STRING_TYPE)
        self._infer(node.left, scope, ut)
        self._infer(node.value, scope, ut)

        return STRING_TYPE
 
    @visitor.when(Or)
    def visit(self, node: And, ctx: Context, scope: Scope):
        self.visit(node.left, ctx, scope)
        self.visit(node.value, ctx, scope)

        self._infer(node.left, scope, BOOLEAN_TYPE)
        self._infer(node.value, scope, BOOLEAN_TYPE)

        return BOOLEAN_TYPE
 
    @visitor.when(GreaterThan)
    def visit(self, node: GreaterThan, ctx: Context, scope: Scope):
        lt = self.visit(node.left, ctx, scope)
        rt = self.visit(node.value, ctx, scope)

        self._infer(node.left, scope, NUMBER_TYPE)
        self._infer(node.value, scope, NUMBER_TYPE)

        return BOOLEAN_TYPE
 
    @visitor.when(LessThan)
    def visit(self, node: LessThan, ctx: Context, scope: Scope):
        lt = self.visit(node.left, ctx, scope)
        rt = self.visit(node.value, ctx, scope)

        self._infer(node.left, scope, NUMBER_TYPE)
        self._infer(node.value, scope, NUMBER_TYPE)

        return BOOLEAN_TYPE
 
    @visitor.when(NotEqual)
    def visit(self, node: NotEqual, ctx: Context, scope: Scope):
        lt = self.visit(node.left, ctx, scope)
        rt = self.visit(node.value, ctx, scope)

        self._infer(node.left, scope, NUMBER_TYPE)
        self._infer(node.value, scope, NUMBER_TYPE)

        return BOOLEAN_TYPE
 
    @visitor.when(GreaterEqual)
    def visit(self, node: GreaterEqual, ctx: Context, scope: Scope):
        lt = self.visit(node.left, ctx, scope)
        rt = self.visit(node.value, ctx, scope)

        self._infer(node.left, scope, NUMBER_TYPE)
        self._infer(node.value, scope, NUMBER_TYPE)

        return BOOLEAN_TYPE
 
    @visitor.when(LessEqual)
    def visit(self, node: LessEqual, ctx: Context, scope: Scope):
        lt = self.visit(node.left, ctx, scope)
        rt = self.visit(node.value, ctx, scope)

        self._infer(node.left, scope, NUMBER_TYPE)
        self._infer(node.value, scope, NUMBER_TYPE)

        return BOOLEAN_TYPE
 
    @visitor.when(CompareEqual)
    def visit(self, node: CompareEqual, ctx: Context, scope: Scope):
        lt = self.visit(node.left, ctx, scope)
        rt = self.visit(node.value, ctx, scope)

        self._infer(node.left, scope, NUMBER_TYPE)
        self._infer(node.value, scope, NUMBER_TYPE)

        return BOOLEAN_TYPE
 
    @visitor.when(Not)
    def visit(self, node: Not, ctx: Context, scope: Scope):
        self.visit(node.value, ctx, scope)

        self._infer(node.value, scope, BOOLEAN_TYPE)

        return BOOLEAN_TYPE

    @visitor.when(Call)
    def visit(self, node: Call, ctx: Context, scope: Scope):
        # CASE: id (...)
        if isinstance(node.value, Var):
            func_name = node.value

            for arg in node.args:
                self.visit(arg, ctx, scope)

            if func_name == BASE_FUNC_NAME:
                if (
                    self.current_method is not None
                    and self.type is not None
                    and self.type.parent != OBJECT_TYPE
                    and INSTANCE_NAME not in self.current_method.params
                    and scope.get_variable_and_scope(
                        INSTANCE_NAME
                    )[1].is_function
                ):
                    try:
                        method: Function = self.type.parent.get_method(
                            self.current_method.name
                        )
                    except:
                        pass
                    else:
                        for arg, pt in zip(node.args, method.params):
                            if pt is not None:
                                self._infer(arg, scope, pt)

                        return method.type

                return None
 
    @visitor.when(Invoke)
    def visit(self, node: Invoke, ctx: Context, scope: Scope):
        # CASE expr . id
        self.visit(node.value, ctx, scope)

        # only valid case is when expr = self
        if (
            self.current_method is not None
            and isinstance(node.value, Var)
            and node.value.value == INSTANCE_NAME
            and node.value.value not in self.current_method.params
            and scope.get_variable_and_scope(node.value.value)[1].is_function
        ):
            # 'self' refers to current type
            try:
                return self.type.get_attribute(node.prop).type
            except SemanticError:
                pass

        return None
     
    @visitor.when(Vector)
    def visit(self, node: Vector, ctx: Context, scope: Scope):
        item_types = []
        for item in node.value:
            item_t = self.visit(item, ctx, scope)
            if item_t is not None:
                item_types.append(item_t)

        if len(item_types) > 0:
            ut = union_type(*item_types)
            for item in node.value:
                self._infer(item, scope, ut)

            return VectorType(ut)

        return VectorType(OBJECT_TYPE)

    @visitor.when(VectorComprehension)
    def visit(self, node: VectorComprehension, ctx: Context):
        return VectorType(OBJECT_TYPE)
    
    @visitor.when(Var)
    def visit(self, node: Star, ctx: Context, scope: Scope):
        if (
            self.current_method is not None
            and node.value == INSTANCE_NAME
            and node.value not in self.current_method.params
            and scope.get_variable_and_scope(node.value)[1].is_function
        ):
            # 'self' refers to current type
            return self.type

        var, _ = scope.get_variable_and_scope(node.value)
        if var is not None:
            return var.var_type

        return None
    
    @visitor.when(TypeDef)
    def visit(self, node: TypeDef, ctx: Context, scope: Scope):
        type: Type = ctx.get_protocol_or_type(node.type, ctx)
        self.current_type = type

        child_scope = scope.create_child_scope()
        for arg in type.args:
            name = arg[0]
            type = arg[1]
            child_scope.define_variable(name, type)

        # infer attr types
        property_nodes = [
            node for node in node.body if isinstance(node, Property)
        ]
        for attr, pn in zip(type.attributes, property_nodes):
            pnt = self.visit(pn.value, ctx, child_scope)
            if attr.type is None and pnt is not None:
                attr.set_type(pnt)
                self.occurs = True

        # infer type param types by attr init
        for arg in type.args:
            name = arg[0]
            at = arg[1]
            if at is None:
                var, _ = child_scope.get_variable_and_scope(name)
                if var.type is not None:
                    type.set_param_type(name, var.type)

        if node.inner_args:
            child_scope = scope.create_child_scope()
            for arg in type.args:
                name = arg[0]
                type = arg[1]
                child_scope.define_variable(name, type)

            for arg in node.inner_args:
                self.visit(arg, ctx, child_scope)

            # infer type param types by parent type args
            for name, pt in type.params.items():
                if pt is None:
                    var, _ = child_scope.get_variable_and_scope(name)
                    if var.type is not None:
                        type.set_param_type(name, var.type)

        method_nodes = [
            node for node in node.body if isinstance(node, Function)
        ]
        for method, mnode in zip(type.methods, method_nodes):
            self.current_method = method
            self.visit(mnode, ctx, scope)
            self.current_method = None

        self.current_type = None
    
    @visitor.when(Protocol)
    def visit(self, node: Protocol, ctx: Context):
        pass

    @visitor.when(Assign)
    def visit(self, node: Assign, ctx: Context, scope: Scope):
        self.visit(node.body, ctx, scope)

        vt = self.visit(node.value, ctx, scope)
        if vt is not None:
            self._infer(node.body, scope, vt)

        return vt
    
    @visitor.when(Pi)
    def visit(self, node: Pi, ctx: Context):
        return NUMBER_TYPE
    
    @visitor.when(E)
    def visit(self, node: E, ctx: Context):
        return NUMBER_TYPE

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
        pass

    @visitor.when(CreateInstance)
    def visit(self, node: CreateInstance, ctx: Context, scope: Scope):
        for arg in node.params:
            self.visit(arg, ctx, scope)

        try:    
            it: Type = ctx.get_protocol_or_type(node.value, ctx)
        except SemanticError as se:
            self.errors.append(se.text)
        for arg, pt in zip(node.params, it.args):
            if pt is not None:
                self._infer(arg, scope, pt)

        return it

    @visitor.when(Indexing)
    def visit(self, node: Indexing, ctx: Context, scope: Scope):
        tt = self.visit(node.value, ctx, scope)
        self.visit(node.index, ctx, scope)

        if isinstance(tt, VectorType):
            return tt.item_type

        self._infer(node.value, scope, VectorType(OBJECT_TYPE))
        return OBJECT_TYPE