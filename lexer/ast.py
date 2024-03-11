from cmp.tools.automata import NFA, DFA, nfa_to_dfa
from cmp.tools.automata import automata_union, automata_concatenation, automata_closure, automata_minimization
#TODO: Change import for our implementation

EPSILON = 'ε'

class Node:
    def evaluate(self):
        raise NotImplementedError()
        
class AtomicNode(Node):
    def __init__(self, lex:str):
        self.lex = lex

class UnaryNode(Node):
    def __init__(self, node: Node):
        self.node = node
        
    def evaluate(self):
        value = self.node.evaluate() 
        return self.operate(value)
    
    @staticmethod
    def operate(value):
        raise NotImplementedError()
        
class BinaryNode(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right
        
    def evaluate(self):
        lvalue = self.left.evaluate() 
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)
    
    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()

class EpsilonNode(AtomicNode):
    def evaluate(self):
        # Your code here!!!
        return NFA(1, [0], {})
    
class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        # Your code here!!!
        return NFA(2,[1],{(0,s):[1]})
    
class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value: NFA):
        # Your code here!!!
        return automata_closure(value)
    
class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        # Your code here!!!
        return automata_union(lvalue, rvalue)
    
class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        # Your code here!!!
        return automata_concatenation(lvalue, rvalue)