from abc import ABC, abstractmethod
from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError, Type
from tools import visitor
from tools.semantic import Scope
from typing import Union
