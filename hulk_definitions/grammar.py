from cmp.pycompiler import Grammar
import logging
logger = logging.getLogger(__name__)

logger.info("Creating Grammar")
G = Grammar()

#region symbol declaration


# Distinguished
program = G.NonTerminal('<program>', startSymbol=True)
# Arithmetic Expression Non Terminal
arit_expr, term, factor, power, atom = G.NonTerminals('<arit-expr> <term> <factor> <power> <atom>')
# Boolean Expression Non Terminals
bool_expr, and_expr, batom, rel_expr, rel_term = G.NonTerminals('<bool-expr> <and-expr> <batom> <rel-expr> <rel-term>')
# Function Definition Non Terminals
arg_list, func_type = G.NonTerminals('<arg-list> <func-type>')
# Type Anotation Non Terminals
type_anoted, ntype = G.NonTerminals('<type-anoted> <ntype>')
# Code Non Terminals
stat_list, stat, expr, expr_list, code_list = G.NonTerminals('<stat_list> <stat> <expr> <expr-list> <code-list>')
# Statement Non Terminals
prinr_stat, protocol, def_func_inline, def_func_block = G.NonTerminals('<print-stat> <protocol> <def-func-inline> <def-func-block>')
# Expressions Non Terminals
block_expr = G.NonTerminal('<block-expr>')
# Simple Expression Non Terminals
let_var, call_expr, str_expr, arthmetic_expr, dest_expr = G.NonTerminals('<let-var> <call-expr> <str-expr> <arithmetic-expr> <dest-expr>') 
conditional_expr, loop_expr = G.NonTerminals('<conditional-expr> <loop-expr>')
# Function Call Non Terminals
param, param_list = G.NonTerminals('<param> <param-list>')
# Statement Non Terminals
def_type, new_expr, func_call = G.NonTerminals('<def-type> <new-expr> <func-call>')
method_list, method, prop_list = G.NonTerminals('<metod-list> <method> <prop-list>')
# Property list Non Terminals
prop = G.NonTerminal('<prop>')
# Let Expression Non Terminals
var_corpse = G.NonTerminal('<var-corpse>')
# Conditional Expression Non Terminals
branches, branch = G.NonTerminals('<branches> <branch>')
# Loop Expression Non Terminals
while_loop, for_loop = G.NonTerminals('<while-loop> <for-loop>')
# Others Non Terminals
type_set, protocol_set, protocol_sand = G.NonTerminals('<type-set> <protocol-set> <protocol-sand>')
# Type Declaration Non Terminals
type_body = G.NonTerminal('<type-body>')


let, inx, defx, printx = G.Terminals('LET IN FUNCTION PRINT')
typex, create, inherits, protocolx = G.Terminals('TYPE NEW INHERITS PROTOCOL')
wloop, floop = G.Terminals('WHILE FOR') 
semi, comma, opar, cpar, okey, ckey, obracket, cbracket, dot, ddot, iline = G.Terminals('SEMICOLON COMMA OPAR CPAR OBRACKET CBRACKET OBRACE CBRACE DOT COLON IMPLICATION')
ifx, elsex, elifx = G.Terminals('IF ELSE ELIF')
plus, minus, star, pow, dstar, div = G.Terminals('PLUS MINUS ASTERISK CIRCUMFLEX POTENCIAL SLASH')
strx = G.Terminal('string')
equal, dest = G.Terminals('EQUAL DESTRUCTIVE_ASSIGNMENT')
land, lor, lnot, cequal, nequal, gthan, lthan, mequal, lequal = G.Terminals('AND OR NOT COMP_EQ COMP_NEQ COMP_GT COMP_LT COMP_GTE COMP_LTE')
isx, asx, at = G.Terminals('IS AS AT')
idx, num = G.Terminals('id num')
ws = G.Terminal('ws')
pi, e = G.Terminals('PI E')
sqrt, sin, cos, exp, log, rand = G.Terminals('SQRT SIN COS EXP LOG RAND')
boolx = G.Terminal('bool')
eof = G.EOF


#endregion

#region production declaration


# # HULK's Program
# program %= code_list, None #TODO #1

# # Valid Code in HULK
# code_list %= expr_list, lambda h,s: s[1] #2.1
# code_list %= code_list + expr_list, lambda h,s: s[1] + s[2] #2
# code_list %= stat_list, lambda h,s: s[1] #4
# code_list %= code_list + stat_list, lambda h,s: s[1] + s[2] #3

# # Statement List
# stat_list %= stat, lambda h,s: [s[1]]#4
# stat_list %= stat + stat_list, lambda h,s: s[1] + s[2]#5

# # Statement
# stat %= def_func, lambda h,s: s[1]#8
# stat %= protocol, lambda h,s: s[1]#9
# stat %= def_type, lambda h,s: s[1]#10
# stat %= prop_list, lambda h,s: s[1]#11
# stat %= method_list, lambda h,s: s[1]#12
# stat %= prinr_stat + semi, lambda h,s: s[1]#13

# # Type Definition
# def_type %= typex + idx + okey + stat_list + ckey, None #TODO 14
# def_type %= typex + idx + opar + arg_list + cpar + okey + stat_list + ckey, None #TODO 15

# # Properties List
# prop_list %= prop + semi, None #TODO 16
# prop_list %= prop + semi + prop_list, None # TODO 17

# # Property
# prop %= idx + equal + expr, None #TODO 18

# # Expressions
# expr_list %= expr, None #TODO 19
# expr_list %= expr + expr_list, None #TODO 20


# expr %= simple_expr + semi, lambda h,s: s[1]# 19
# expr %= block_expr, lambda h,s: s[1]# 21

# expr %= block_expr, lambda h,s: s[1]
# expr %= okey + block_expr + ckey, lambda h,s: s[2]# 20
# expr %= okey + block_expr + ckey + semi, lambda h,s: s[2]# 21

# # Simple Expressions
# # this expr must end with a semicolon
# simple_expr %= str_expr, None #TODO 22
# simple_expr %= call_expr, None #TODO 23
# simple_expr %= arit_expr, None #TODO 24
# simple_expr %= dest_expr, None #TODO 25
# simple_expr %= bool_expr, None #TODO 26

# simple_expr %= let_var, None #TODO 27
# simple_expr %= loop_expr, None #TODO 28
# simple_expr %= conditional_expr, None #TODO 29

# Block Expressions
# block_expr %= simple_expr, None #TODO 30
# block_expr %= okey + expr_list + okey , None #TODO 31

# # Multiple Variables Declaration
# var_corpse %= type_anoted + equal + expr, None #TODO 32  
# var_corpse %= type_anoted + equal + expr + comma + var_corpse, None #TODO 33

# # Call Expression
# call_expr %= idx, None #TODO 34
# call_expr %= func_call, None #TODO 35
# call_expr %= create + func_call, None #TODO 36
# call_expr %= call_expr + dot + idx, None #TODO 37
# call_expr %= call_expr + dot + func_call, None #TODO 38
# call_expr %= call_expr + asx + bool_expr, None #TODO 39
# call_expr %= call_expr + obracket + call_expr + cbracket, None #TODO 40

# # Destructive Asignation Expression
# dest_expr %= call_expr + dest + expr, None #TODO 41

# # Conditional Expression
# conditional_expr %= ifx + opar + bool_expr + cpar + block_expr + elsex + block_expr, None # TODO 42
# conditional_expr %= ifx + opar + bool_expr + cpar + block_expr + branches + elsex + block_expr, None #TODO 43

# branches %= branch, None #TODO 44
# branches %= branches + branch, None #TODO 45

# branch %= elifx + opar + expr + cpar + expr, None #TODO 46

# # Print Statement
# prinr_stat %= printx + opar + expr + cpar, None # TODO: Change to expression 47


# param_list %= param, None #TODO 50
# param_list %= param + comma + param_list, None #TODO 51

# # Protocol Statement
# protocol %= protocolx + idx + okey + method_list + ckey, None #TODO 54

# # Methods 
# method_list %= method + semi, None #TODO 55
# method_list %= method + semi + method_list, None #TODO 56

# # Method Declaration
# method %= idx + opar + arg_list + cpar + ntype + expr, None #TODO 57

# # Function Definition Statement
# def_func %= defx + idx + iline + simple_expr + semi, None # TODO 58

# func_type %= opar + arg_list + cpar, None # TODO 59
# func_type %= opar + arg_list + cpar + ntype, None # TODO 60

# arg_list %= type_anoted, None # TODO 61
# arg_list %= type_anoted + comma + arg_list, None # TODO 62

# # Type Anotation Format
# type_anoted %= idx, None #TODO 63
# type_anoted %= idx + ntype, None #TODO 64

# ntype %= ddot + idx, None #TODO 65

# # let var Expression
# let_var %= let + var_corpse + inx + simple_expr, None #TODO 66
# let_var %= let + var_corpse + inx + opar + block_expr + cpar, None #TODO 67

# # String Expression
# str_expr %= dquote + strx + dquote, None #TODO 68

# # Boolean Expression
# bool_expr %= and_expr, None #TODO 69
# bool_expr %= and_expr + lor + bool_expr, None #TODO 70

# and_expr %= batom, None #TODO 71
# and_expr %= and_expr + land + batom, None #TODO 72

# batom %= rel_expr, None #TODO 73
# batom %= lnot + batom, None #TODO 74
# batom %= opar + bool_expr + cpar, None #TODO 75

# rel_expr %= rel_expr + isx + rel_term, None #TODO 76
# rel_expr %= rel_expr + lthan + rel_term, None # TODO 77
# rel_expr %= rel_expr + gthan + rel_term, None # TODO 78
# rel_expr %= rel_expr + cequal + rel_term, None # TODO 79
# rel_expr %= rel_expr + nequal + rel_term, None # TODO 80
# rel_expr %= rel_expr + lequal + rel_term, None # TODO 81
# rel_expr %= rel_expr + mequal + rel_term, None # TODO 82

# rel_term %= num, None # TODO 83
# rel_term %= boolx, None # TODO 84
# rel_term %= call_expr, None # TODO 85

# # Arithmetic Expression
# arit_expr %= term, None # TODO 86
# arit_expr %= arit_expr + plus + term, None # TODO 87
# arit_expr %= arit_expr + minus + term, None # TODO 88

# term %= factor, None # TODO 89
# term %= term + div + factor, None # TODO 90
# term %= term + star + factor, None # TODO 91

# factor %= power, None # TODO 92
# factor %= factor + pow + power, None # TODO 93
# factor %= factor + dstar + power, None # TODO 94

# power %= atom, None # TODO 95
# power %= minus + atom, None # TODO 96

# atom %= num, None # TODO 97
# atom %= call_expr, None # TODO 98
# atom %= opar + expr + cpar, None # TODO 99

# Loop Expression
#endregion

#region newproduction Declaration

# # HULK's Program
# program %= expr_list + eof, None #TODO

# #region Expressions
# expr_list %= expr + expr_list, None #TODO
# expr_list %= expr, None #TODO

# expr %= simple_expr + semi, lambda h,s: s[1]
# expr %= block_expr, lambda h,s: s[1]
# #endregion

# #region Simple Expressions
# # this expr must end with a semicolon
# simple_expr %= strx, None #TODO
# simple_expr %= arit_expr, None #TODO
# #endregion

# #region Call Expression
# call_expr %= idx, None #TODO
# call_expr %= func_call, None #TODO
# #endregion

# #region Function Call Expression
# func_call %= idx + opar + cpar, None #TODO
# func_call %= idx + opar + param_list + cpar, None #TODO
# func_call %= atom + opar + param_list + cpar, None #TODO
# atom %= sqrt, None #TODO
# atom %= sin, None #TODO
# atom %= cos, None #TODO
# atom %= exp, None #TODO
# atom %= log, None #TODO
# atom %= rand, None #TODO
# atom %= printx, None #TODO

# param_list %= param, None #TODO 50
# param_list %= param + comma + param_list, None #TODO 51

# param %= simple_expr, None #TODO
# #endregion

# #region Arithmetic Expression
# arit_expr %= term, None # TODO
# arit_expr %= arit_expr + plus + term, None # TODO
# arit_expr %= arit_expr + minus + term, None # TODO

# term %= factor, None # TODO
# term %= term + div + factor, None # TODO 
# term %= term + star + factor, None # TODO

# factor %= atom, None # TODO
# factor %= factor + pow + atom, None # TODO
# factor %= factor + dstar + atom, None # TODO

# atom %= num, None # TODO
# atom %= call_expr, None # TODO
# atom %= opar + simple_expr + cpar, None # TODO
#endregion

#region Block Expressions
# block_expr %= okey + expr_list + ckey + semi, lambda h,s: s[2]
# block_expr %= okey + expr_list + ckey, lambda h,s: s[2]
#endregion


#endregion

#region newnewproduction declaration

program %= expr_list, None #TODO

expr_list %= block_expr + semi + expr_list, None #TODO
expr_list %= block_expr + expr_list, None #TODO
expr_list %= block_expr + semi, None #TODO
expr_list %= block_expr, None #TODO
expr_list %= expr + semi + expr_list, None #TODO
expr_list %= expr + semi, None #TODO
expr_list %= stat,None #TODO

stat %= def_func_block,None #TODO

def_func_block %= defx + idx + func_type + block_expr, None #TODO

block_expr %= okey + expr_list + ckey, None #TODO

expr %= term, None # TODO
expr %= term + plus + expr, None #TODO'
expr %= term + minus + expr, None #TODO
expr %= term + at + expr, None #TODO
expr %= def_func_inline, None #TODO

def_func_inline %= defx + idx + func_type + iline + expr, None #TODO

func_type %= opar + arg_list + cpar + ntype, None #TODO
func_type %= opar + arg_list + cpar, None #TODO

arg_list %= expr, None #TODO
arg_list %= expr + ntype, None #TODO
arg_list %= expr + comma + arg_list, None #TODO
arg_list %= expr + ntype + comma + arg_list, None #TODO

ntype %= ddot + idx, None #TODO

param_list %= expr, None #TODO
param_list %= expr + comma + param_list, None #TODO

term %= factor, None #TODO
term %= factor + div + term, None #TODO
term %= factor + star + term, None #TODO

factor %= atom, None #TODO
factor %= atom + pow + factor, None #TODO
factor %= atom + dstar + factor, None #TODO

atom %= opar + expr + cpar, None #TODO
atom %= atom + opar + param_list + cpar, None #TODO
atom %= atom + opar + cpar, None #TODO
atom %= atom + dot + idx, None #TODO
atom %= num, None #TODO
atom %= pi, None #TODO
atom %= e, None #TODO
atom %= idx, None #TODO
atom %= strx, None #TODO
atom %= sqrt, None #TODO
atom %= sin, None #TODO
atom %= cos, None #TODO
atom %= exp, None #TODO
atom %= log, None #TODO
atom %= rand, None #TODO
atom %= printx, None #TODO

#endregion

logger.info("Grammar created")
for i, production in  enumerate(G.Productions):
    logger.info("Production %d: %s" % (i, production))