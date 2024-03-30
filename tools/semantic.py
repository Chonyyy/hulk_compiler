import itertools as itt
from collections import OrderedDict
from typing import Tuple, Union
from typing import Callable
class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]

class Attribute:
    def __init__(self, name, typex):
        self.name = name
        self.type = typex

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)

class Function:
    def __init__(self, name, params, return_type):
        self.name = name
        self.params = params
        self.return_type = return_type

    # def __str__(self):
    #     params = ', '.join(f'{n}:{t.name}' for n,t in zip(self.param_names, self.param_types))
    #     return f'[method] {self.name}({params}): {self.return_type.name if self.return_type.name else "None"};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types

class FunctionDef:
    def __init__(self, name, param_names, params_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type

    def __str__(self):
        params = ', '.join(f'{n}:{t.name}' for n,t in zip(self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'
    
    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types

class Type:
    def __init__(self, name:str):
        self.name = name
        self.attributes = []
        self.methods = []
        self.args = []
        self.parent = None

    def conforms(self, other):
        if other.name == "Object":
            return True
        # Si el tipo actual es el mismo que el otro tipo, entonces conforma
        if self == other:
            return True
        # Si el tipo actual tiene un tipo padre y este conforma con el otro tipo, entonces también conforma
        elif self.parent is not None and self.parent.conforms(other):
            return True
        # Si el tipo actual es un tipo especial que puede conformar con cualquier otro tipo, entonces conforma
        elif self.bypass():
            return True
        # En cualquier otro caso, el tipo actual no conforma con el otro tipo
        else:
            return False
    
    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name:str, typex):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')

    def get_argument(self, name:str):
        try:
            return next(arg for arg in self.args if arg[0] == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Argument "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_argument(name)
            except SemanticError:
                raise SemanticError(f'Argument "{name}" is not defined in {self.name}.')

    def define_argument(self, name:str, typex):
        try:
            self.get_argument(name)
        except SemanticError:
            self.args.append((name, typex))
        else:
            raise SemanticError(f'Argument "{name}" is already defined in {self.name}.')

    def get_method(self, name:str):
        try:
            return next(method for method in self.methods_def if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Function "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Function "{name}" is not defined in {self.name}.')

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Function "{name}" already defined in {self.name}')
        
        method = Function(name, param_names, param_types, return_type)
        self.methods.append(method)
        return method

    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def bypass(self):
        return False

    def __str__(self):
        output = f'type {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes)
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)

class Protocol(Type):
    def __init__(self, name:str):
        super().__init__(name)
        self.methods_def = []

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name in (method.name for method in self.methods_def):
            raise SemanticError(f'Function "{name}" already defined in {self.name}')

        method = FunctionDef(name, param_names, param_types, return_type)
        self.methods_def.append(method)
        return method

    def get_attribute(self, name: str):
        raise SemanticError(f'Protocol "{self.name}" has no attributes.')
    
    def define_attribute(self, name: str, typex):
        raise SemanticError(f'Protocol "{self.name}" has no attributes.')

    def all_attributes(self, clean=True):
        raise SemanticError(f'Protocol "{self.name}" has no attributes.')

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)

class VoidType(Type):
    def __init__(self):
        Type.__init__(self, '<void>')

    def conforms_to(self, other):
        raise Exception('Invalid type: void type.')

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, VoidType)

class IntType(Type):
    def __init__(self):
        Type.__init__(self, 'int')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)

class Variable:
    def __init__(self, name, var_type):
        self.name = name
        self.var_type = var_type

class Scope:
    def __init__(self, parent = None, index = 0):
        self.local_vars: list[Tuple[int, Variable]] = []
        self.local_funcs: list[Tuple[int, Function]] = []
        self.local_types: list[Tuple[int, Type]] = []
        self.local_protocols: list[Tuple[int, Protocol]] = []
        self.parent: Scope = parent
        self.children: list[Tuple[int, Scope]] = []
        self.index: int = 1
        self.index_at_parent: int = index
        # self.func_index_at_parent = 0 if parent is None else len(parent.local_funcs)
        # self.type_index_at_parent = 0 if parent is None else len(parent.local_types)
        # self.protocol_index_at_parent = 0 if parent is None else len(parent.local_protocols)
        
    def create_child_scope(self) -> "Scope":
        self.index += 1

        child_scope = Scope(self)
        child_scope.index_at_parent = self.index
        self.children.append((self.index, child_scope))
        return child_scope

    def define_variable(self, var_name:str, var_type:str) -> None:
        self.index += 1
        if self.get_local_variable(var_name):
            raise SemanticError(f'Variable "{var_name}" is already defined.')
        self.local_vars.append((self.index, Variable(var_name, var_type)))
    
    def define_function(self, func_name:str, params:list[Tuple[str, str]], return_type:str) -> None:
        self.index += 1
        if self.get_local_function_info(func_name, len(params)):
            raise SemanticError(f'Function "{func_name}" is already defined.')
        self.local_funcs.append((self.index, Function(func_name, params, return_type)))

    def define_type(self, type_name: str) -> None:
        self.index += 1
        self.local_types.append((self.index, type_name))

    def get_local_variable(self, var_name: str, current_index = None) -> Union[Variable, SemanticError]:
        for index, var in self.local_vars:
            if current_index and index > current_index:
                continue
            if var_name == var.name:
                return var

        return self.parent.get_local_variable(var_name, self.index_at_parent) if self.parent else None
    
    def get_local_function_info(self, fun_name:str, params_num:int, current_index = None) -> Union[Function, SemanticError]:
        for index, fun in self.local_funcs:
            if current_index and index > current_index:
                continue
            if fun_name == fun.name and len(fun.params) == params_num:
                return fun

        return self.parent.get_local_function_info(fun_name, params_num, self.index_at_parent) if self.parent else None

    # def is_var_defined(self, vname):
    #     if vname not in [var[0] for var in self.local_vars]:
    #         if self.parent:
    #             return self.parent.is_var_defined(vname)
    #         else:
    #             return False
    #     return True
    
    # def is_func_defined(self, fname, n):
    #     if (fname, n) not in [(fun[0][0], len(fun[0][1])) for fun in self.local_funcs]:
    #         if self.parent:
    #             return self.parent.is_func_defined(fname, n)
    #         else:
    #             return False
    #     return True

    # def is_local_var(self, vname):
    #     return self.get_local_variable(vname) is not None
    
    # def is_local_func(self, fname, n):
        return self.get_local_function_info(fname, n) is not None


class ScopeInterpreter:
    def __init__(self, parent = None, index = 0):
        self.local_vars: dict = {}
        self.local_funcs: dict = {}
        self.local_types: dict = {}
        self.local_protocols: dict = {}
        self.parent: ScopeInterpreter = parent
        self.children: list[Tuple[int, ScopeInterpreter]] = []
        self.index: int = 1
        self.index_at_parent: int = index
        
    def create_child_scope(self) -> "ScopeInterpreter":
        self.index += 1

        child_scope = ScopeInterpreter(self)
        child_scope.index_at_parent = self.index
        self.children.append((self.index, child_scope))
        return child_scope

    def define_variable(self, var_name:str, var, var_type = None) -> None:
        self.index += 1
        # if self.get_local_variable(var_name):
        #     raise SemanticError(f'Variable "{var_name}" is already defined.')
        self.local_vars[var_name] = (var,var_type)
    
    def define_function(self, func_name:str, func: Callable) -> None:
        self.index += 1
        if self.get_local_function(func_name):
            raise SemanticError(f'Function "{func_name}" is already defined.')
        self.local_funcs[func_name] = func
        
    def define_protocol(self, var_name:str, var_type) -> None:
        if self.get_local_protocol(var_name):
            raise SemanticError(f'Protocol "{var_name}" is already defined.')
        self.local_protocols[var_name] = var_type
    
    def define_type(self, var_name:str, var_type) -> None:
        if self.get_local_type(var_name):
            raise SemanticError(f'Type "{var_name}" is already defined.')
        self.local_types[var_name] = var_type

    def get_local_variable(self, var_name: str) -> Union[Variable, SemanticError]:
        for var in self.local_vars:
            if var_name == var:
                return self.local_vars[var]

        return self.parent.get_local_variable(var_name) if self.parent else None
    
    def get_local_function(self, fun_name:str) -> Union[Function, SemanticError]:
        for fun in self.local_funcs:
            if fun_name == fun:
                return self.local_funcs[fun_name]

        return self.parent.get_local_function(fun_name) if self.parent else None

    def get_local_protocol(self, fun_name:str):
        for fun in self.local_protocols:
            if fun_name == fun:
                return self.local_protocols[fun_name]

        return self.parent.get_local_protocol(fun_name) if self.parent else None

    def get_local_type(self, fun_name:str):
        for fun in self.local_types:
            if fun_name == fun:
                return self.local_types[fun_name]

        return self.parent.get_local_type(fun_name) if self.parent else None


class Context:
    def __init__(self):
        self.types = {}
        self.protocols = {}

    def create_type(self, name:str):
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = Type(name)
        return typex

    def create_protocol(self, name:str):
        if name in self.protocols:
            raise SemanticError(f'Protocol with the same name ({name}) already in context.')
        protocolx = self.protocols[name] = Protocol(name)
        return protocolx

    def get_type(self, name:str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')

    def get_protocol(self, name:str):
        try:
            return self.protocols[name]
        except KeyError:
            raise SemanticError(f'Protocol "{name}" is not defined.')

    def get_protocol_or_type(self, name:str):
        try:
            return self.get_protocol(name)
        except SemanticError:
            return self.get_type(name)

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)


