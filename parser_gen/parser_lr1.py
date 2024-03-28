from cmp_parser.tools import compute_firsts, compute_follows, compute_local_first
from cmp_parser.pycompiler import Grammar
from cmp_parser.pycompiler import Item
from lexer_gen.utils import Symbol
from cmp_parser.utils import ContainerSet
from cmp_parser.automata import State, multiline_formatter
from pandas import DataFrame
from os import path
import logging
logger = logging.getLogger(__name__)

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
    logger.info("Building LR1 automaton")
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
    
    def __init__(self, G):
        print("initializing parser")
        self.G = G
        self.action = {}
        self.goto = {}
        # self._build_parsing_table()
    
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
            logger.info(f'Parsing {w[cursor:]}')
            logger.info(f"State: {state}, Lookahead: {lookahead}, Stack: {stack}, Cursor: {cursor}")
            
            # Detect error
            if lookahead == '$' and state ==  0:
                logger.info("Error: No se puede reconocer la cadena.")
                return False
            a = list(self.action.keys())
            
            action, tag = self.action.get((state, lookahead), (None, None))
            if action == None and tag == None:
                action, tag = self.action.get((state, lookahead.Name), (None, None))
            logger.info(f'Realizando {action} a {tag}')
            operations.append(action)
            
            # Shift case
            if action == self.SHIFT:
                stack.append(tag)
                cursor +=  1
                logger.info(f'Shift {tag}')
            
            # Reduce case
            elif action == self.REDUCE:
                body_size = len(self.G.Productions[tag].Right)
                for _ in range(body_size):
                    stack.pop()
                    
                try:
                    stack.append(self.goto[(stack[-1], self.G.Productions[tag].Left)])
                except:
                    stack.append(self.goto[(stack[-1], self.G.Productions[tag].Left.Name)])
                output.append(self.G.Productions[tag])
                
                logger.info(f'Reduce {tag}')
            
            # OK case
            elif action == self.OK:
                logger.info("OK")
                return output , operations
            
            # Invalid case
            else:
                logger.error("Error: Acción inválida.")
                raise NotImplementedError(f'Invalid token {w[cursor].token_type}')
                # return False
        
class LR1Parser(ShiftReduceParser):
    def __init__(self, G, path, force = False):
        super().__init__(G)
        if self._load_table(path) and not force:
            logger.info('Parser table has been loaded')
        else:
            logger.info("Parser table can't be loaded")
            self._build_parsing_table(path)

    def _build_parsing_table(self, path):
        G = self.G.AugmentedGrammar(True)
        automaton = build_LR1_automaton(G)

        logger.info("Building parsing table")
        for i, node in enumerate(automaton):
            logger.info(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            logger.info(f'{i}')
            for state in node.state:
                logger.info(f'\t {state}')
            node.idx = i

        for node in automaton:
            idx = node.idx
            logger.info(f'Node {idx}')
            for item in node.state:
                logger.info(f'\t{item}')
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
        
        if self._save_table(path):
            logger.info('Parsing table has been saved.')
        else:
            logger.info("Error! The parsing table can't be saved")
                          
        
    @staticmethod
    def _register(table, key, value):
        logger.info(f"Registering {key} -> {value}")
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value       

    def _save_table(self, path) -> bool:
        logger.info(f'Saving parser table in {path}')
        with open(path, "w", encoding="utf-8") as table:
            for key in list(self.action.keys()):
                try:
                    value = self.action[key]
                    logger.info(f'Saving {key} -> {value} as:')
                    origin, la = key
                    action, destiny = value
                    logger.info(f'\t{str(origin)} {la} -> {action} {str(destiny)}')
                    table.write(f'{str(origin)} {la} {action} {str(destiny)}\n')
                except:
                    return False
                
            table.write('GOTO\n')
            for key in list(self.goto.keys()):
                try:
                    value = self.goto[key]
                    logger.info(f'Saving {key} -> {value} as:')
                    origin, la = key
                    destiny = value
                    logger.info(f'\t{str(origin)} {la} -> {str(destiny)}')
                    table.write(f'{str(origin)} {la} {str(destiny)}\n')
                except:
                    return False

        return True
    
    def _load_table(self, path) -> bool:
        logger.info(f'Loading parser table of {path}')
        try:
            with open(path, 'r', encoding = "utf-8") as table:
                lines = table.readlines()
                goto = False
                for rline in lines:
                    if 'GOTO' in rline:
                        goto = True
                        continue
                    line = rline.split(' ')
                    if not goto:

                        try:

                            origin = int(line[0])
                            la = line[1]
                            action = line[2]
                            if 'None' not in line[3]:
                                destiny = int(line[3])
                            else:
                                destiny = None

                        except:

                            logger.info('Table record is damaged')
                            return False

                        key = (origin, la)
                        value = (action, destiny)
                        self.action[key] = value
                    else:
                        try:

                            origin = int(line[0])
                            la = line[1]
                            if 'None' not in line[2]:
                                destiny = int(line[2])
                            else:
                                destiny = None

                        except:

                            logger.info('Table record is damaged')
                            return False

                        key = (origin, la)
                        value = destiny
                        self.goto[key] = value

                return goto
        except:
            logger.info(f'file {path} does not exist.')
            return False
                    

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
    parser = LR1Parser(G)
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