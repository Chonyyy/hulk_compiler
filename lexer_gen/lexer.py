from lexer_gen.rgx_engine import Regex
from lexer_gen.automatons import State, automaton_minimization
from lexer_gen.utils import Token
import math, logging
logger = logging.getLogger(__name__)

class Lexer:
    def __init__(self, table, eof, grammar):
        self.eof = eof
        logger.info("Building Regexs Automatons")
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
        self.G = grammar
    
    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            logger.debug(f'Building regex for {token_type} with regex : {regex}')
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
        logger.debug(f'Building automaton for {len(self.regexs)} regexs')
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
        tokens = []
        for lex, ttype in self._tokenize(text):
            if ttype in ['ws']:
                continue
            if lex == self.eof:
                tokens.append(Token(lex, self.G.EOF))
                continue
            tokens.append(Token(lex, self.G.symbDict[ttype]))
        return tokens
        # return [ Token(lex, self.G.symbDict[ttype]) for lex, ttype in self._tokenize(text)]