#TODO: Organize and polish all the code.
#FIXME: All the import shenanigans
from lexer.utils import ContainerSet
from lexer.utils import DisjointSet
#FIXME: Fix operations between automatas. Closure is the most correct one.

#region Automaton implementations

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

class State:
    def __init__(self, state, final=False, formatter=lambda x: str(x), shape='circle'):
        self.state = state
        self.final = final
        self.transitions = {}
        self.epsilon_transitions = set()
        self.tag = None
        self.formatter = formatter
        self.shape = shape

    # The method name is set this way from compatibility issues.
    def set_formatter(self, value, attr='formatter', visited=None):
        if visited is None:
            visited = set()
        elif self in visited:
            return

        visited.add(self)
        self.__setattr__(attr, value)
        for destinations in self.transitions.values():
            for node in destinations:
                node.set_formatter(value, attr, visited)
        for node in self.epsilon_transitions:
            node.set_formatter(value, attr, visited)
        return self

    def has_transition(self, symbol):
        return symbol in self.transitions

    def add_transition(self, symbol, state):
        try:
            self.transitions[symbol].append(state)
        except:
            self.transitions[symbol] = [state]
        return self

    def add_epsilon_transition(self, state):
        self.epsilon_transitions.add(state)
        return self

    def recognize(self, string):
        states = self.epsilon_closure
        for symbol in string:
            states = self.move_by_state(symbol, *states)
            states = self.epsilon_closure_by_state(*states)
        return any(s.final for s in states)

    def to_deterministic(self, formatter=lambda x: str(x)):
        closure = self.epsilon_closure
        start = State(tuple(closure), any(s.final for s in closure), formatter)

        closures = [ closure ]
        states = [ start ]
        pending = [ start ]

        while pending:
            state = pending.pop()
            symbols = { symbol for s in state.state for symbol in s.transitions }

            for symbol in symbols:
                move = self.move_by_state(symbol, *state.state)
                closure = self.epsilon_closure_by_state(*move)

                if closure not in closures:
                    new_state = State(tuple(closure), any(s.final for s in closure), formatter)
                    closures.append(closure)
                    states.append(new_state)
                    pending.append(new_state)
                else:
                    index = closures.index(closure)
                    new_state = states[index]

                state.add_transition(symbol, new_state)

        return start

    @staticmethod
    def from_nfa(nfa, get_states=False):
        states = []
        for n in range(nfa.states):
            state = State(n, n in nfa.finals, shape= 'square' if n == nfa.start else 'circle')
            states.append(state)

        for (origin, symbol), destinations in nfa.map.items():
            origin = states[origin]
            origin[symbol] = [ states[d] for d in destinations ]

        if get_states:
            return states[nfa.start], states
        return states[nfa.start]

    @staticmethod
    def move_by_state(symbol, *states):
        return { s for state in states if state.has_transition(symbol) for s in state[symbol]}

    @staticmethod
    def epsilon_closure_by_state(*states):
        closure = { state for state in states }

        l = 0
        while l != len(closure):
            l = len(closure)
            tmp = [s for s in closure]
            for s in tmp:
                for epsilon_state in s.epsilon_transitions:
                        closure.add(epsilon_state)
        return closure

    @property
    def epsilon_closure(self):
        return self.epsilon_closure_by_state(self)

    @property
    def name(self):
        return self.formatter(self.state)

    def get(self, symbol):
        target = self.transitions[symbol]
        assert len(target) == 1
        return target[0]

    def __getitem__(self, symbol):
        if symbol == '':
            return self.epsilon_transitions
        try:
            return self.transitions[symbol]
        except KeyError:
            return None

    def __setitem__(self, symbol, value):
        if symbol == '':
            self.epsilon_transitions = value
        else:
            self.transitions[symbol] = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.state)

    def __hash__(self):
        return hash(self.state)

    def __iter__(self):
        yield from self._visit()

    def _visit(self, visited=None):
        if visited is None:
            visited = set()
        elif self in visited:
            return

        visited.add(self)
        yield self

        for destinations in self.transitions.values():
            for node in destinations:
                yield from node._visit(visited)
        for node in self.epsilon_transitions:
            yield from node._visit(visited)

    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        visited = set()
        def visit(start):
            ids = id(start)
            if ids not in visited:
                visited.add(ids)
                G.add_node(pydot.Node(ids, label=start.name, shape=self.shape, style='bold' if start.final else ''))
                for tran, destinations in start.transitions.items():
                    for end in destinations:
                        visit(end)
                        G.add_edge(pydot.Edge(ids, id(end), label=tran, labeldistance=2))
                for end in start.epsilon_transitions:
                    visit(end)
                    G.add_edge(pydot.Edge(ids, id(end), label='ε', labeldistance=2))

        visit(self)
        G.add_edge(pydot.Edge('start', id(self), label='', style='dashed'))

        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass

    def write_to(self, fname):
        return self.graph().write_svg(fname)

#endregion

#region Basic automaton operations

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
        
    return ContainerSet(*closure)

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

#endregion

#region Operation between automatons

def automaton_union(a1:NFA, a2:NFA):
    transitions = {}
    
    start = 0
    d1 = 1 # displacement of a1 ?
    d2 = a1.states + d1 # displacement of a2 ?
    final = a2.states + d2 # final state ?

    for (origin, symbol), destinations in a1.map.items():
        ## Relocate a1 transitions ...
        # Your code here
        transitions[(origin + d1, symbol)] = []
        for destination in destinations:
            transitions[(origin + d1, symbol)].append(destination + d1)

    for (origin, symbol), destinations in a2.map.items():
        ## Relocate a2 transitions ...
        # Your code here
        transitions[(origin + d2, symbol)] = []
        for destination in destinations:
            transitions[(origin + d2, symbol)].append(destination + d2)
    
    ## Add transitions from start state ...
    # Your code here
    transitions[(0, '')] = [d1, d2]
    
    ## Add transitions to final state ...
    # Your code here
    for final_state in a1.finals:
        transitions[(final_state + d1, '')] = [final]
    for final_state in a2.finals:
        transitions[(final_state + d2, '')] = [final]

    states = a1.states + a2.states + 2
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def automaton_concatenation(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        ## Relocate a1 transitions ...
        # Your code here
        transitions[(origin + d1, symbol)] = []
        for destination in destinations:
            transitions[(origin + d1, symbol)].append(destination + d1)

    for (origin, symbol), destinations in a2.map.items():
        ## Relocate a2 transitions ...
        # Your code here
        transitions[(origin + d2, symbol)] = []
        for destination in destinations:
            transitions[(origin + d2, symbol)].append(destination + d2)
    
    ## Add transitions to final state ...
    # Your code here
    for final_state in a1.finals:
        transitions[(final_state + d1, '')] = [a2.start + d2]

    for final_state in a2.finals:
        transitions[(final_state + d2, '')] = [final]
    
    states = a1.states + a2.states + 1
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def automaton_closure(a1):
    transitions = {}
    
    start = 0
    d1 = 1
    final = a1.states + d1
    
    for (origin, symbol), destinations in a1.map.items():
        ## Relocate automaton transitions ...
        # Your code here
        transitions[(origin + d1, symbol)] = []
        for destination in destinations:
            transitions[(origin + d1, symbol)].append(destination + d1)
    
    ## Add transitions from start state ...
    # Your code here
    transitions[(start, '')] = [a1.start + d1, final]
    
    ## Add transitions to final state and to start state ...
    # Your code here
    for final_state in a1.finals:
        if not (final_state + d1, '') in transitions:
            transitions[(final_state + d1, '')] = [final]
        transitions[(final_state + d1, '')] += [final]
    transitions[(final, '')] = [start]
            
    states = a1.states +  2
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def distinguish_states(group, automaton:DFA, partition):
    split = {}
    vocabulary = tuple(automaton.vocabulary)

    for member in group:
        # Your code here
        transitions = automaton.transitions[member.value]
        member_key = []
        for (symbol, destiny) in transitions.items():
            member_key.append((symbol, partition[destiny[0]].representative.value))

        if not tuple(member_key) in split:
            split[tuple(member_key)] = [member.value]
        else: 
            split[tuple(member_key)].append(member.value)
        pass

    return [ group for group in split.values()]

def state_minimization(automaton):
    partition = DisjointSet(*range(automaton.states))
    
    ## partition = { NON-FINALS | FINALS }
    # Your code here
    not_finals = [state for state in range(automaton.states) if state not in automaton.finals]
    partition.merge(not_finals)
    # finish my input
    while True:
        new_partition = DisjointSet(*range(automaton.states))
        
        ## Split each group if needed (use distinguish_states(group, automaton, partition))
        # Your code here
        for group in partition.groups:
            new_groups = distinguish_states(group, automaton, partition)
            for new_group in new_groups:
                new_partition.merge(new_group)
        # finish myinput
        
        if len(new_partition) == len(partition):
            break

        partition = new_partition
        
    return partition

def automaton_minimization(automaton):
    #(a|b)*abb
    # partition = state_minimization(automaton)
    #TODO: DELETE THIS!!!! TESTING PORPUSSES ONLY:
    partition = DisjointSet(*range(automaton.states))
    partition.merge([0, 2])
    
    states = [s.value for s in partition.representatives]
    
    transitions = {}
    for i, state in enumerate(states):
        ## origin = ???
        # Your code here
        origin = state
        #finish my input
        for symbol, destinations in automaton.transitions[origin].items():
            # Your code here 
            transitions[(i, symbol)] = states.index(partition[destinations[0]].representative.value)
            # finish my input

            try:
                transitions[i,symbol]
                # assert False
            except KeyError:
                # Your code here
                pass
    
    ## finals = ???
    ## start  = ???
    # Your code here
    finals = [states.index(state.value) for state in partition.representatives if state.value in automaton.finals]
    
    return DFA(len(states), finals, transitions)

#endregion