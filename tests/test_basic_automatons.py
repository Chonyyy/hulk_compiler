'''
for guidance:
assertEqual
assertNotEqual
assertTrue
assertFalse
assertIs
assertIsNot
assertIsNone
assertIsNotNone
assertIn
assertNotIn
assertIsInstance
assertNotIsInstance
'''

import unittest
from lexer.automatons import *

class TestAutomaton(unittest.TestCase):  
    def setUp(self):
        self.nfa = NFA(states=3, finals=[2], transitions={
            (0, 'a'): [0],
            (0, 'b'): [0, 1],
            (1, 'a'): [2]
        })#(a|b)*ba
        self.dfa = DFA(states=3, finals=[2], transitions={
            (0, 'a'): 0,
            (0, 'b'): 1,
            (1, 'a'): 2,
            (1, 'b'): 1,
            (2, 'a'): 0,
            (2, 'b'): 1,
        })#(a|b)*ba

        self.automaton_a = NFA(states=6, finals=[3, 5], transitions={
            (0, ''): [ 1, 2 ],
            (1, ''): [ 3 ],
            (1,'b'): [ 4 ],
            (2,'a'): [ 4 ],
            (3,'c'): [ 3 ],
            (4, ''): [ 5 ],
            (5,'d'): [ 5 ]
        })#c*|(a|b)d*

        self.automaton_b = NFA(states=3, finals=[2], transitions={
            (0,'a'): [ 0 ],
            (0,'b'): [ 0, 1 ],
            (1,'a'): [ 2 ],
            (1,'b'): [ 2 ],
        })

        self.automaton_c = NFA(states=5, finals=[4], transitions={
            (0,'a'): [ 0, 1 ],
            (0,'b'): [ 0, 2 ],
            (0,'c'): [ 0, 3 ],
            (1,'a'): [ 1, 4 ],
            (1,'b'): [ 1 ],
            (1,'c'): [ 1 ],
            (2,'a'): [ 2 ],
            (2,'b'): [ 2, 4 ],
            (2,'c'): [ 2 ],
            (3,'a'): [ 3 ],
            (3,'b'): [ 3 ],
            (3,'c'): [ 3, 4 ],
        })

    def test_nfa_construction(self):
        test_case = {0: {'a': [0], 'b': [0, 1]}, 1: {'a': [2]}, 2: {}}
        msg = f'NFA creation failed, expected transitions dict: \n{test_case}\nResulting transition dict:\n {self.nfa.transitions}'
        self.assertEqual(self.nfa.transitions, test_case, msg)
    
    def test_dfa_construction(self):
        test_case = {0: {'a': [0], 'b': [1]}, 1: {'a': [2], 'b': [1]}, 2: {'a': [0], 'b': [1]}}
        msg = f'NFA creation failed, expected transitions dict: \n{test_case}\nResulting transition dict:\n {self.dfa.transitions}'
        self.assertEqual(self.dfa.transitions, test_case, msg)

    def test_recognition(self):
        positive_test = ["ba", "aababbaba"]
        negative_test = ["", "aabaa", "aababb"]
        for string in positive_test:
            if not self.dfa.recognize(string):
                self.fail(f'The DFA failed to recognize string: {string}')

        for string in negative_test:
            if self.dfa.recognize(string):
                self.fail(f'The DFA recognized the string ({string}) when it should\'nt have')

    def test_move(self):
        transitions = [
            ([1], '', {3}), 
            ([1], 'a', set()), 
            ([2], 'a', {4}), 
            ([1, 5], 'd', {5})
        ]
        for (states, symbol, result) in transitions:
            transition_result = move(self.automaton_a, states, symbol)
            if not transition_result == result:
                self.fail(f'The result for aplying move from {states} with symbol {symbol} was:\n{transition_result}\n And the expected result was:\n{result}')

    def test_epsilon_closure(self):
        test_cases =[
            ([0], {0,1,2,3}),
            ([0, 4], {0,1,2,3,4,5}),
            ([1, 2, 4], {1,2,3,4,5})
        ]
        for (states, control_sets) in test_cases:
            closure = epsilon_closure(self.automaton_a, states)
            if not closure == control_sets:
                self.fail(f'Failed to calculate the epsilon closure of {states}, result given:\n{closure}\nExpected result:\n{control_sets}')

    def test_nfa_to_dfa_conversion(self):
        positive_control = ['', 'a', 'b', 'cccccc', 'adddd', 'bdddd']
        negative_control = ['dddddd', 'cdddd', 'aa', 'ab', 'ddddc']
        converted_automaton = nfa_to_dfa(self.automaton_a)

        for string in positive_control:
            if not converted_automaton.recognize(string):
                self.fail(f'The DFA failed to recognize string: {string}')

        for string in negative_control:
            if converted_automaton.recognize(string):
                self.fail(f'The DFA recognized the string ({string}) when it should\'nt have')

    def testing_more_languages(self):
        move_test_cases2 = [
            ([0,1], 'a', {0,2}),
            ([0,1], 'b', {0,1,2})
        ]
        
        for (states, symbol, control) in move_test_cases2:
            transition_result = move(self.automaton_b, states, symbol)
            if not transition_result == control:
                self.fail(f'The result for aplying move to automaton2 from {states} with symbol {symbol} was:\n{transition_result}\n And the expected result was:\n{control}')

        convertion2 = nfa_to_dfa(self.automaton_b)
        convertion3 = nfa_to_dfa(self.automaton_c)
        
        converted_states2 = 4
        converted_states3 = 15
        converted_finals2 = 2
        converted_finals3 = 7

        if convertion2.states != converted_states2:
            self.fail(f'Expected {converted_states2} states in automaton2 convertion, got {convertion2.states}')
        if convertion3.states != converted_states3:
            self.fail(f'Expected {converted_states3} states in automaton3 convertion, got {convertion3.states}')

        if len(convertion2.finals) != converted_finals2:
            self.fail(f'Expected {converted_finals2} final states in automaton2 convertion, got {len(convertion2.finals)}')
        if len(convertion3.finals) != converted_finals3:
            self.fail(f'Expected {converted_finals3} final states in automaton3 convertion, got {len(convertion3.finals)}')

        converted_positive_control2 = ['aba', 'bb', 'aaaaaaaaaaaba']
        converted_positive_control3 = ['abccac', 'bbbbbbbbaa', 'cac']
        converted_negative_control2 = ['aaa', 'ab', 'b', '']
        converted_negative_control3 = ['abbbbc', 'a', '', 'acacacaccab']

        for string in converted_positive_control2:
            if not convertion2.recognize(string):
                self.fail(f'The automaton2 failed to recognize string: {string}')

        for string in converted_negative_control2:
            if convertion2.recognize(string):
                self.fail(f'The automaton2 recognized the string ({string}) when it should\'nt have')

        for string in converted_positive_control3:
            if not convertion3.recognize(string):
                self.fail(f'The automaton3 failed to recognize string: {string}')

        for string in converted_negative_control3:
            if convertion3.recognize(string):
                self.fail(f'The automaton recognized the string ({string}) when it should\'nt have')

class TestAutomatonOperations(unittest.TestCase):
    def setUp(self):
        self.automaton_a = DFA(states=2, finals=[1], transitions={
            (0,'a'):  0,
            (0,'b'):  1,
            (1,'a'):  0,
            (1,'b'):  1,
        })#(a|b)*b

        self.automaton_b = DFA(states=3, finals=[2], transitions={
            (0, 'a'): 0,
            (0, 'b'): 1,
            (1, 'a'): 2,
            (1, 'b'): 1,
            (2, 'a'): 0,
            (2, 'b'): 1,
        })#(a|b)*ba

        self.automaton_c = DFA(states=5, finals=[4], transitions={
            (0, 'a'): 1,
            (0, 'b'): 2,
            (1, 'a'): 1,
            (1, 'b'): 3,
            (2, 'a'): 1,
            (2, 'b'): 2,
            (3, 'a'): 1,
            (3, 'b'): 4,
            (4, 'a'): 1,
            (4, 'b'): 2,
        })

    def test_automaton_union(self):
        union = automaton_union(self.automaton_a, self.automaton_a)
        recognize = nfa_to_dfa(union).recognize

        if union.states != 2 * self.automaton_a.states + 2:
            self.fail(f'Expected {2 * self.automaton_a.states + 2} states in the union, got {union.states}')
        
        positive_control = ['b', 'abbb', 'abaaababab']
        negative_control = ['', 'a', 'abbbbaa']

        for string in positive_control:
            if not recognize(string):
                self.fail(f'The union failed to recognize string: {string}')

        for string in negative_control:
            if recognize(string):
                self.fail(f'The union recognized the string ({string}) when it should\'nt have')

    def test_automaton_concatenation(self):
        concatenation = automaton_concatenation(self.automaton_a, self.automaton_a)
        recognize = nfa_to_dfa(concatenation).recognize

        if concatenation.states != 2 * self.automaton_a.states + 1:
            self.fail(f'Expected {2 * self.automaton_a.states + 1} states in the concatenation, got {concatenation.states}')
        
        positive_control = ['bb', 'abb', 'abaaababab']
        negative_control = ['', 'a', 'b', 'ab', 'aaaab', 'abbbbaa']

        for string in positive_control:
            if not recognize(string):
                self.fail(f'The concatenation failed to recognize string: {string}')

        for string in negative_control:
            if recognize(string):
                self.fail(f'The concatenation recognized the string ({string}) when it should\'nt have')

    def test_automaton_closure(self):
        closure = automaton_closure(self.automaton_a)
        recognize = nfa_to_dfa(closure).recognize

        if closure.states != self.automaton_a.states + 2:
            self.fail(f'Expected {self.automaton_a.states + 2} states in the closure, got {closure.states}')
        
        positive_control = ['', 'b', 'ab', 'bb', 'abbb', 'abaaababab']
        negative_control = ['a', 'abbbbaa']

        for string in positive_control:
            if not recognize(string):
                self.fail(f'The closure failed to recognize string: {string}')

        for string in negative_control:
            if recognize(string):
                self.fail(f'The closure recognized the string ({string}) when it should\'nt have')

    def test_state_minimization(self):
        states = state_minimization(self.automaton_c)

        for members in states.groups:
            all_in_finals = all(m.value in self.automaton_c.finals for m in members)
            none_in_finals = all(m.value not in self.automaton_c.finals for m in members)
        
        assert len(states) == 4, f'Expected 4 states in the minimization, got {len(states)}'
        assert states[0].representative == states[2].representative, f'Expected states 0 and 2 to be in the same group, got {states[0].representative} and {states[2].representative}'
        assert states[1].representative == states[1], f'Expected state 1 to be in the same group, got {states[1].representative}'
        assert states[3].representative == states[3], f'Expected state 3 to be in the same group, got {states[3].representative}'
        assert states[4].representative == states[4], f'Expected state 4 to be in the same group, got {states[4].representative}'

    def test_automaton_minimization(self):
        mini = automaton_minimization(self.automaton_c)

        assert mini.states == 4, f'Expected 4 states in the minimization, got {mini.states}'

        positive_control = ['abb', 'ababbaabb']
        negative_control = ['', 'ab', 'aaaaa', 'bbbbb', 'abbabababa']

        for string in positive_control:
            if not mini.recognize(string):
                self.fail(f'The minimization failed to recognize string: {string}')

        for string in negative_control:
            if mini.recognize(string):
                self.fail(f'The minimization recognized the string ({string}) when it should\'nt have')

if __name__ == '__main__':
    unittest.main()