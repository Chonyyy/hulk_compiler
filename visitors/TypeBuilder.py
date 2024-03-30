from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError, Type
from tools import visitor
from typing import Union

class TypeBuilder(object):
    def __init__(self, context: Context, errors=[]):
        self.context = context
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Program)
    def visit(self, node: Program):
        for child in node.statements:
            if isinstance(child, TypeDef) or isinstance(child, Protocol):
                self.visit(child, self.context)

        return self.errors

    @visitor.when(TypeDef)
    def visit(self, node: TypeDef, ctx: Context):
        type_info = ctx.get_type(node.name)
        try:
            if node.inheritance:
                parent = ctx.get_type(node.inheritance)
                type_info.set_parent(parent)
        except SemanticError as se:
            self.errors.append(se.text)
        
        if node.args:
            for arg_name, arg_type in node.args:
                try:
                    type_info.define_argument(arg_name, arg_type)
                except SemanticError as se:
                    self.errors.append(se.text)
        
        if node.body:
            for stat in node.body:
                self.visit(stat, ctx, type_info)

    @visitor.when(Protocol)
    def visit(self, node: Protocol, ctx: Context):
        protocol_info = ctx.get_protocol(node.name)
        try:
            if node.extension:
                parent = ctx.get_protocol(node.extension)
                protocol_info.set_parent(parent)
        except SemanticError as se:
            self.errors.append(se.text)

        if node.body:
            for stat in node.body:
                self.visit(stat, ctx, protocol_info)

    @visitor.when(Property)
    def visit(self, node: Property, ctx: Context, current_type: Union[Type, Protocol]):
        attr_type = ctx.get_type(node.type) if node.type else None
        try:
            current_type.define_attribute(node.name, attr_type)
        except SemanticError as se:
            self.errors.append(se.text)
                
    @visitor.when(Function)
    def visit(self, node: Function, ctx: Context, current_type: Union[Type, Protocol]):
        try:
            # Divide the params into names and types from node.params: List[Tuple[str, str]]
            param_names, param_types = [], []
            return_type = None
            
            if node.type:
                return_type = ctx.get_type(node.type)
            current_type.define_method(node.name, node.params, return_type)
        except SemanticError as se:
            self.errors.append(se.text)
