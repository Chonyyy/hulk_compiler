from lexer.rgx_engine import Regex
from lexer.automatons import State, automaton_minimization
from lexer.utils import Token
import math

class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
    
    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            # Your code here!!!
            # - Remember to tag the final states with the token_type and priority.
            # - <State>.tag might be useful for that purpose ;-)
            dfa = Regex(regex).automaton #TODO: Minimize ?
            start_state, states = State.from_nfa(dfa, get_states= True)
            for state in dfa.finals:
                final_state = states[state]
                final_state.tag = {
                    "priority":n,
                    "token_type": token_type
                }

            regexs.append(start_state)
        return regexs
    
    def _build_automaton(self):
        start = State('start')
        # Your code here!!!
        for start_state in self.regexs:
            start.add_epsilon_transition(start_state)
        return start.to_deterministic()
    
        
    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''
        
        for symbol in string:
            # Your code here!!!
            lex += symbol
            if not (symbol in state.transitions):
                if lex == '':
                    raise NotImplementedError(f'symbol {symbol} not a valid lexer starter')
                break
            state = state.transitions[symbol][0]
            if state.final:# this has a list of non deterministic final states, select the one with highest 
                max_priority = math.inf
                for nd_state in state.state:
                    if nd_state.final and nd_state.tag['priority'] < max_priority:
                        final = nd_state.tag['token_type']
                        max_priority = nd_state.tag['priority']
                final_lex = lex
            
        return final, final_lex
    
    def _tokenize(self, text):
        # Your code here!!!
        last_end_state = None
        buffer_index = 0
        while buffer_index < len(text):
            final_state, lex = self._walk(text[buffer_index:])
            if lex == '':
                raise NotImplementedError(f'No valid token found for {text[buffer_index:]}')
            buffer_index += len(lex)
            yield lex, final_state
        # en of my input
        yield '$', self.eof
    
    def __call__(self, text):
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]