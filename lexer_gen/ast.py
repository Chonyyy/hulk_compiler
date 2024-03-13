
from lexer_gen.automatons import NFA, DFA, nfa_to_dfa
from lexer_gen.automatons import automaton_union, automaton_concatenation, automaton_closure, automaton_minimization

from tools.ast_base import AtomicNode, UnaryNode, BinaryNode

EPSILON = 'ε'

class EpsilonNode(AtomicNode):
    def evaluate(self) -> NFA:
        # Your code here!!!
        return NFA(1, [0], {})
    
class SymbolNode(AtomicNode):
    def evaluate(self) -> NFA:
        s = self.lex
        # Your code here!!!
        return NFA(2,[1],{(0,s):[1]})
    
class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value: NFA):
        # Your code here!!!
        return automaton_closure(value)
    
class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        # Your code here!!!
        return automaton_union(lvalue, rvalue)
    
class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        # Your code here!!!
        return automaton_concatenation(lvalue, rvalue)