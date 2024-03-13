'''
This module contains the base classes for the AST nodes.
'''


class Node:
    '''
    Base class for all AST nodes.
    '''
    def evaluate(self):
        '''
        Evaluate the node and return the result.
        '''
        raise NotImplementedError()
        
class AtomicNode(Node):
    '''
    Base class for atomic nodes, i.e. nodes that do not have children.

    Attributes:
        lex: str - the lexeme of the token that this node represents. 
    '''
    def __init__(self, lex:str):
        '''
        The constructor for the AtomicNode class.

        Params:
            lex: str - the lexeme of the token that this node represents.
        '''
        self.lex = lex

class UnaryNode(Node):
    '''
    Base class for unary nodes, i.e. nodes that have a single child.

    Attributes:
        node: Node - the child node.
    '''
    def __init__(self, node: Node):
        '''
        The constructor for the UnaryNode class.

        Params:
            node: Node - the child node.
        '''
        self.node = node
        
    def evaluate(self)->any:
        '''
        Evaluate the child node, and performs the operation on it, then returns the result.
        '''
        value = self.node.evaluate() 
        return self.operate(value)
    
    @staticmethod
    def operate(value: any):
        '''
        Perform the operation on the value.
        Params:
            value: any - the value to perform the operation on.
        '''
        raise NotImplementedError()
        
class BinaryNode(Node):
    '''
    Base class for binary nodes, i.e. nodes that have two children.

    Attributes:
        left: Node - the left child node.
        right: Node - the right child node.
    '''
    def __init__(self, left: Node, right: Node):
        '''
        The constructor for the BinaryNode class.

        Params:
            left: Node - the left child node.
            right: Node - the right child node.
        '''
        self.left = left
        self.right = right
        
    def evaluate(self)->any:
        '''
        Evaluate the left and right child nodes, and performs the operation on them, then returns the result.
        '''
        lvalue = self.left.evaluate() 
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)
    
    @staticmethod
    def operate(lvalue:any, rvalue:any):
        '''
        Perform the operation on the values.
        Params:
            lvalue: any - the left value to perform the operation on.
            rvalue: any - the right value to perform the operation on.
        '''
        raise NotImplementedError()
