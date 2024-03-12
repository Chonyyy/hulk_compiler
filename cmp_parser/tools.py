from cmp_parser.pycompiler import Grammar
from cmp_parser.utils import ContainerSet


# # Test
# from pycompiler import Grammar
# from utils import ContainerSet

# G = Grammar()
# E = G.NonTerminal('E', True)
# T,F,X,Y = G.NonTerminals('T F X Y')
# plus, minus, star, div, opar, cpar, num = G.Terminals('+ - * / ( ) num')

# E %= T + X
# X %= plus + T + X | minus + T + X | G.Epsilon
# T %= F + Y
# Y %= star + F + Y | div + F + Y | G.Epsilon
# F %= num | opar + E + cpar


class ContainerSet:
    def __init__(self, *values, contains_epsilon=False):
        self.set = set(values)
        self.contains_epsilon = contains_epsilon
        
    def add(self, value):
        n = len(self.set)
        self.set.add(value)
        return n != len(self.set)
        
        
    def set_epsilon(self, value=True):
        last = self.contains_epsilon
        self.contains_epsilon = value
        return last != self.contains_epsilon
        
    def update(self, other):
        n = len(self.set)
        self.set.update(other.set)
        return n != len(self.set)
    
    def epsilon_update(self, other):
        return self.set_epsilon(self.contains_epsilon | other.contains_epsilon)
    
    def hard_update(self, other):
        return self.update(other) | self.epsilon_update(other)
    
    def __len__(self):
        return len(self.set) + int(self.contains_epsilon)
    
    def __str__(self):
        return '%s-%s' % (str(self.set), self.contains_epsilon)
    
    def __repr__(self):
        return str(self)
    
    def __iter__(self):
        return iter(self.set)
    
    def __eq__(self, other):
        return isinstance(other, ContainerSet) and self.set == other.set and self.contains_epsilon == other.contains_epsilon

# Computes First(alpha), given First(Vt) and First(Vn) 
# alpha in (Vt U Vn)*
def compute_local_first(G,firsts, alpha: str):
    first_alpha = ContainerSet()
    
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False
    
    if alpha_is_epsilon:
        first_alpha.contains_epsilon = True

    else:
        for symbol in alpha:
            if symbol in firsts:

                if symbol in G.terminals:
                    first_alpha.add(symbol)

                if symbol in G.nonTerminals:
                    first_alpha.update(firsts[symbol])
                    if firsts[symbol].contains_epsilon:
                        first_alpha.add_epsilon()
            break

    return first_alpha

# Computes First(Vt) U First(Vn) U First(alpha)
# P: X -> alpha
def compute_firsts(G):
    firsts = {}
    change = True
    
    # init First(Vt)
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
        
    # init First(Vn)
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
    
    while change:
        change = False
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            # get current First(X)
            first_X = firsts[X]
                
            # init First(alpha)
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
            
            # CurrentFirst(alpha)???
            local_first = compute_local_first(G,firsts, alpha)
            
            # update First(X) and First(alpha) from CurrentFirst(alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)
                    
    # First(Vt) + First(Vt) + First(RightSides)
    return firsts

def compute_follows(G, firsts):
    follows = { }
    change = True
    
    local_firsts = {}
    
    # init Follow(Vn)
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)
    
    while change:
        change = False
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            follow_X = follows[X]
            
            ###################################################
            # X -> zeta Y beta
            # First(beta) - { epsilon } subset of Follow(Y)
            # beta ->* epsilon or X -> zeta Y ? Follow(X) subset of Follow(Y)
            ###################################################
            #                   <CODE_HERE>                   #
            
            for i in range(len(alpha)):
                if alpha[i] in G.nonTerminals:

                    follow_symbol = follows[alpha[i]]
                    
                    if i < len(alpha) - 1:
                        # If the next symbol is a terminal add it
                        if alpha[i + 1] in G.terminals:
                            if alpha[i + 1] not in follows[alpha[i]]:
                                follows[alpha[i]].add(alpha[i + 1])
                                change = True
                        # If the next symbol is a non terminal add its first set (without epsilon)
                        else:
                            first_i = firsts[alpha[i + 1]]
                            if not first_i.set.issubset(follows[alpha[i]]):
                                follows[alpha[i]].update(first_i )
                                change = True

                            if first_i.contains_epsilon:
                                if not follow_X.set.issubset(follows[alpha[i]]):
                                    follows[alpha[i]].update(follow_X)
                                    change = True

                    # For the last non-terminal symbol add follow_X
                    else:
                        if follow_X != follows[alpha[i]] :
                            follows[alpha[i]].update(follow_X)
                            #change = True
                        # if follow_symbol != follows[alpha[i]]:
                        #     change = True
                    
            ###################################################

    # Follow(Vn)
    return follows

# firsts = compute_firsts(G)
# follows = compute_follows(G, firsts)
# # print(firsts)
# print(follows)