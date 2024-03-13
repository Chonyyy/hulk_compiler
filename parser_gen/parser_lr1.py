from cmp_parser.tools import compute_firsts, compute_follows, compute_local_first
from cmp_parser.pycompiler import Grammar
from cmp_parser.pycompiler import Item
from cmp_parser.utils import ContainerSet
from cmp_parser.automata import State, multiline_formatter
from pandas import DataFrame

def expand(item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []
    
    lookaheads = ContainerSet()
    
    prev = item.Preview()
    # for preview in prev:
    #     lookaheads.extend(firsts[preview[0]])

    for preview in prev:
        for i in range(len(preview)):
            if preview[i].IsTerminal:
                lookaheads.extend(firsts[preview[i]])
                break
            elif preview[i].IsNonTerminal:
                lookaheads.extend(firsts[preview[i]])
                if not any(item.IsEpsilon for item in preview[i].productions):# TODO: me parece que los IsEpsilon se estan guardando mal porque X se va a epsilon y aqui me da false
                    break
        
    assert not lookaheads.contains_epsilon
    
    result = []
    for i in next_symbol.productions:
        itm = Item(i, 0, lookaheads=lookaheads)
        result.append(itm)
        result += expand(itm, firsts)
    return result

def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)
    
    return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }

def closure_lr1(items, firsts):
    closure = ContainerSet(*items)
    
    changed = True
    while changed:
        changed = False
        
        new_items = ContainerSet()
        
        for itm in closure:
            new_items.extend(expand(itm,firsts) )
        
        changed = closure.update(new_items)
        
    return compress(closure)

def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)

def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
    
    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)
    
    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    
    start = frozenset([start_item])

    closure = closure_lr1(start, firsts)
    automaton = State(frozenset(closure), True)
    
    pending = [ start ]
    visited = { start: automaton }
    
    while pending:
        current = pending.pop()
        current_state = visited[current]    
        
        for symbol in G.terminals + G.nonTerminals:
            
            set = frozenset(goto_lr1(current_state.state, symbol, firsts))
            if len(set) == 0: continue
            next_state = State(set, True)
            if set in visited.keys(): 
                current_state.add_transition(symbol.Name, visited[set])
                continue
            visited[set] = next_state
            pending.append(set)
            current_state.add_transition(symbol.Name, next_state)
            

    automaton.set_formatter(multiline_formatter)
    return automaton

class ShiftReduceParser:

    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    
    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()
    
    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [0]
        cursor =  0
        output = []
        operations = []
        
        while True:
            state = stack[-1]
            lookahead = w[cursor].token_type
            if self.verbose: print(stack, '<---||--->', w[cursor:])
            
            # Detect error
            if lookahead == '$' and state ==  0:
                if self.verbose: print("Error: No se puede reconocer la cadena.")
                return False
            action, tag = self.action.get((state, lookahead), (None, None))
            operations.append(action)
            
            # Shift case
            if action == self.SHIFT:
                stack.append(tag)
                cursor +=  1
                if self.verbose: print("Shift", tag)
            
            # Reduce case
            elif action == self.REDUCE:
                body_size = len(self.G.Productions[tag].Right)
                for _ in range(body_size):
                    stack.pop()
                    
                stack.append(self.goto[(stack[-1],self.G.Productions[tag].Left)])
                output.append(self.G.Productions[tag])
                
                if self.verbose: print("Reduce", tag)
            
            # OK case
            elif action == self.OK:
                if self.verbose: print("OK")
                return output , operations
            
            # Invalid case
            else:
                if self.verbose: print("Error: Acción inválida.")
                # return False
        
class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        
        automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:
                next_symbol = item.NextSymbol
                
                if next_symbol in G.terminals:
                    if node.has_transition(next_symbol.Name):
                        next_state = node.transitions[item.NextSymbol.Name][0]
                        self._register(self.action, (idx,next_symbol), (self.SHIFT, next_state.idx))
                
                if next_symbol in G.nonTerminals:
                    if node.has_transition(next_symbol.Name):
                        next_state = node.transitions[item.NextSymbol.Name][0]
                        self._register(self.goto, (idx, next_symbol),  next_state.idx)
                
                if next_symbol is None: 
                    for l in item.lookaheads:
                        if item.production.Left == G.startSymbol and l == G.EOF:
                            self._register(self.action, (idx,l), (self.OK, None))
                            break
                        
                        k = G.Productions.index(item.production)
                        self._register(self.action, (idx,l),  (self.REDUCE, k))
                          
            
        
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value
        

def encode_value(value):
    try:
        action, tag = value
        if action == ShiftReduceParser.SHIFT:
            return 'S' + str(tag)
        elif action == ShiftReduceParser.REDUCE:
            return repr(tag)
        elif action ==  ShiftReduceParser.OK:
            return action
        else:
            return value
    except TypeError:
        return value

def table_to_dataframe(table):
    d = {}
    for (state, symbol), value in table.items():
        value = encode_value(value)
        try:
            d[state][symbol] = value
        except KeyError:
            d[state] = { symbol: value }

    return DataFrame.from_dict(d, orient='index', dtype=str)

if __name__ == "__main__":
    G = Grammar()
    E = G.NonTerminal('E', True)
    A= G.NonTerminal('A')

    equal, plus, num = G.Terminals('= + int')

    E %=  A + equal + A | num
    A %= num + plus + A | num

    item = Item(E.productions[0], 0, lookaheads=[G.EOF])


    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)
    parser = LR1Parser(G, verbose=False)
    # print("FFFF")
    # print(firsts)
    # print(" ")

    # follows = compute_follows(G,firsts)
    # print(" ")
    # print("FFFF")
    # print(follows)
    # print(" ")
    derivation = parser([num, plus, num, equal, num, plus, num, G.EOF])

    assert str(derivation) == '[A -> int, A -> int + A, A -> int, A -> int + A, E -> A = A]'

    print(derivation)