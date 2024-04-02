from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError, Type, topological_sort, Proto
from tools import visitor
from typing import Union


class TypeBuilder(object):
    def __init__(self, context: Context, errors=[]):
        self.context = context
        self.errors = errors

        self.current_type: Union[Type, Proto] = None
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Program)
    def visit(self, node: Program):
        types = [item for item in node.statements if isinstance(node, TypeDef)]
        types = topological_sort(types)

        if len(types) > 0:
            for child in node.statements:
                if isinstance(child, TypeDef) or isinstance(child, Protocol):
                    self.visit(child, self.context)
        else:
            self.errors.append(SemanticError('Types defined had a circular innheritance.'))

        return self.errors

    @visitor.when(TypeDef)
    def visit(self, node: TypeDef, ctx: Context):
        type_info: Type = ctx.get_type(node.name)
        try:
            if node.type:
                parent = ctx.get_type(node.type)
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
            if node.type:
                parent = ctx.get_protocol(node.type)
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
            return_type = None
            
            if node.type:
                return_type = ctx.get_type(node.type)
            current_type.define_method(node.name, node.params, return_type)
        except SemanticError as se:
            self.errors.append(se.text)

