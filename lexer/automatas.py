#TODO: Organize and polish all the code.
#FIXME: Fix operations between automatas. Closure is the most correct one.

class NFA:
    """
    A Non Deterministic Automata

    Parameters
    ----------
    """
    def __init__(self, states, finals, transitions, start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = { state: {} for state in range(states) }
        
        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)
            
        self.vocabulary.discard('')
        
    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()
            
    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        for (start, tran), destinations in self.map.items():
            tran = 'ε' if tran == '' else tran
            G.add_node(pydot.Node(start, shape='circle', style='bold' if start in self.finals else ''))
            for end in destinations:
                G.add_node(pydot.Node(end, shape='circle', style='bold' if end in self.finals else ''))
                G.add_edge(pydot.Edge(start, end, label=tran, labeldistance=2))

        G.add_edge(pydot.Edge('start', self.start, label='', style='dashed'))
        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass

class DFA(NFA):
    
    def __init__(self, states, finals, transitions, start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol):
        # Returns the next state from the next state given a symbol and the current state
        return self.transitions[self.current][symbol][0] if symbol in self.transitions[self.current] else -1
    
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string:str)->bool:
        self._reset()
        string_iterator = iter(string)
        c = next(string_iterator, '')
        while c != '':
            self.current = self._move(c)
            if self.current == -1: break
            c = next(string_iterator, '')

        return self.current in self.finals
    
def move(automaton:NFA, states, symbol) -> set:
    moves = set()
    transitions = automaton.transitions
    for state in states:
        moves.update(transitions[state].get(symbol, []))
    return moves

def epsilon_closure(automaton, states) -> set:
    pending = list(states)
    closure = set(states)
    
    while pending:
        state = pending.pop()
        closure.add(state)

        new_states = move(automaton, [state], '')
        pending.extend(new_states - closure)
        closure.update(new_states)
        
    return set(*closure)

def nfa_to_dfa(automaton) -> DFA:
    transitions = {}
    
    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0 
    id_count = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [ start ]

    pending = [ start ]
    while pending:
        state = pending.pop()
        
        for symbol in automaton.vocabulary:
            # Your code here
            new_state = epsilon_closure(automaton, move(automaton, state, symbol))

            if not new_state.set:
                continue
            
            if new_state in states:
                old_id = states.index(new_state)

                transitions[(state.id, symbol)] = old_id
                continue

            id_count += 1
            new_state.id = id_count
            new_state.is_final = any(s in automaton.finals for s in new_state)

            states.append(new_state)
            pending.append(new_state)

            transitions[(state.id, symbol)] = new_state.id

            # if state.id in transitions:
            #     transitions[state.id][symbol] = new_state.id
            # else:
            #     transitions[state.id] = {symbol:new_state.id}
            
            # ...
            try:
                transitions[state.id][symbol]
                # assert False, 'Invalid DFA!!!'
            except KeyError:
                # Your code here
                pass
    
    finals = [ state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    return dfa