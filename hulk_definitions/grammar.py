from cmp.pycompiler import Grammar

G = Grammar()
# Distinguished
program = G.NonTerminal('<program>', startSymbol=True)
# Arithmetic Expression Non Terminal
arit_expr, term, factor, power, atom = G.NonTerminals('<arit-expr> <term> <factor> <power> <atom>')
# Boolean Expression Non Terminals
bool_expr, and_expr, batom = G.NonTerminals('<bool-expr> <and-expr> <batom>')
# Function Definition Non Terminals
arg_list, func_type = G.NonTerminals('<arg-list> <func-type>')
# Type Anotation Non Terminals
type_anoted, ntype = G.NonTerminals('<type-anoted> <ntype>')
# Code Non Terminals
stat_list, stat, expr, expr_list, code_list = G.NonTerminals('<stat_list> <stat> <expr> <expr-list> <code-list>')
# Statement Non Terminals
prinr_stat, protocol, def_func = G.NonTerminals('<print-stat> <protocol> <def-func>')
# Expressions Non Terminals
block_expr, simple_expr = G.NonTerminals('<block-expr> <simple-expr>')
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




let, inx, defx, printx = G.Terminals('let in def print')
typex, create, inherits, protocolx = G.Terminals('type new inherits protocol')
wloop, floop = G.Terminals('while for') 
semi, comma, opar, cpar, okey, ckey, obracket, cbracket, dot, ddot, iline = G.Terminals('; , ( ) { } [ ] . : =>')
ifx, elsex, elifx = G.Terminals('if else elif')
plus, minus, star, pow, dstar, div = G.Terminals('+ - * ^ ** /')
dquote, strx = G.Terminals('" str')
asignment, dest = G.Terminals('= :=')
land, lor, lnot, equal, nequal = G.Terminals('& | ! == !=')
isx, asx = G.Terminals('is as')
idx, num = G.Terminals('id int')
# sqrt, sin, cos, exp, log, rand = G.Terminals('sqrt sin ')
boolx = G.Terminals('bool')

# HULK's Program
program %= code_list, None #TODO

# Valid Code in HULK
code_list %= code_list + expr_list, lambda h,s: s[1] + s[2]
code_list %= code_list + stat_list, lambda h,s: s[1] + s[2]

# Statement List
stat_list %= stat, lambda h,s: [s[1]]
stat_list %= stat + stat_list, lambda h,s: s[1] + s[2]

# Expression List
expr_list %= expr, lambda h,s: [s[1]]
expr_list %= expr + expr_list, lambda h,s: s[1] + s[2]

# Statement
stat %= def_func, lambda h,s: s[1]
stat %= protocol, lambda h,s: s[1]
stat %= def_type, lambda h,s: s[1]
stat %= prop_list, lambda h,s: s[1]
stat %= method_list, lambda h,s: s[1]
stat %= prinr_stat + semi, lambda h,s: s[1]

# Type Definition
def_type %= typex + idx + okey + stat_list + ckey, None #TODO
def_type %= typex + idx + opar + arg_list + cpar + okey + stat_list + ckey, None #TODO

# Properties List
prop_list %= prop + semi, None #TODO
prop_list %= prop + semi + prop_list, None # TODO

# Property
prop %= idx + equal + expr, None #TODO

# Expressions
expr %= simple_expr + semi, lambda h,s: s[1]

expr %= block_expr, lambda h,s: s[1]
expr %= okey + block_expr + ckey, lambda h,s: s[2]
expr %= okey + block_expr + ckey + semi, lambda h,s: s[2]

# Simple Expressions
# this expr must end with a semicolon
simple_expr %= str_expr, None #TODO
simple_expr %= call_expr, None #TODO
simple_expr %= arit_expr, None #TODO
simple_expr %= dest_expr, None #TODO
simple_expr %= bool_expr, None #TODO

simple_expr %= let_var, None #TODO
simple_expr %= loop_expr, None #TODO
simple_expr %= conditional_expr, None #TODO

# Block Expressions
block_expr %= block_expr + expr_list, None #TODO
block_expr %= block_expr + stat_list, None #TODO

# Multiple Variables Declaration
var_corpse %= type_anoted + equal + expr, None #TODO
var_corpse %= type_anoted + equal + expr + comma + var_corpse, None #TODO

# Call Expression
call_expr %= idx, None #TODO
call_expr %= func_call, None #TODO
call_expr %= create + func_call, None #TODO
call_expr %= call_expr + dot + idx, None #TODO
call_expr %= call_expr + asx + type_set, None #TODO
call_expr %= call_expr + dot + func_call, None #TODO
call_expr %= call_expr + obracket + call_expr + cbracket, None #TODO

# Set of types
type_set %= idx, None #TODO
type_set %= idx + lor + type_set, None #TODO

# Protocol Statement
protocol_set %= protocol_sand, None #TODO
protocol_set %= protocol_set + lor + protocol_sand, None #TODO

protocol_sand %= idx, None #TODO
protocol_sand %= protocol_sand + land + idx, None #TODO

# Destructive Asigantion Expression
dest_expr %= call_expr + dest + expr, None #TODO

# Conditional Expression
conditional_expr %= ifx + opar + expr + cpar + expr + elifx + expr, None # TODO
conditional_expr %= ifx + opar + expr + cpar + expr + branches + elsex + expr, None #TODO

branches %= branch, None #TODO
branches %= branches + branch, None #TODO

branch %= elifx + opar + expr + cpar + expr, None #TODO

# Print Statement
prinr_stat %= printx + expr, None # TODO

# Function Call Expression
func_call %= call_expr + opar + cpar, None #TODO
func_call %= call_expr + opar + param_list + cpar, None # TODO

param_list %= param, None #TODO
param_list %= param + comma + param_list, None #TODO

# Expression List
expr_list %= expr, None # TODO
expr_list %= expr + semi + expr_list, None # TODO

# Protocol Statement
protocol %= protocolx + idx + okey + method_list + ckey, None #TODO

# Methods 
method_list %= method + semi, None #TODO
method_list %= method + semi + method_list, None #TODO

# Method Declaration
method %= idx + opar + arg_list + cpar + ntype + expr, None #TODO

# Function Definition Statement
def_func %= defx + idx + iline + simple_expr + semi, None # TODO

func_type %= opar + arg_list + cpar, None # TODO
func_type %= opar + arg_list + cpar + ntype, None # TODO

arg_list %= type_anoted, None # TODO
arg_list %= type_anoted + comma + arg_list, None # TODO

# Type Anotation Format
type_anoted %= idx, None #TODO
type_anoted %= idx + ntype, None #TODO

ntype %= ddot + idx, None #TODO

# let var Expression
let_var %= let + var_corpse + inx + expr, None #TODO
let_var %= let + var_corpse + inx + opar + expr_list + cpar, None #TODO

# String Expression
str_expr %= dquote + strx + dquote, None #TODO

# Boolean Expression
bool_expr %= and_expr + lor + bool_expr, None #TODO
bool_expr %= and_expr, None #TODO

and_expr %= batom, None #TODO
and_expr %= and_expr + land + batom, None #TODO

batom %= boolx, None #TODO
batom %= call_expr, None #TODO
batom %= lnot + batom, None #TODO
batom %= batom + equal + batom, None #TODO
batom %= batom + nequal + batom, None #TODO
batom %= call_expr + isx + idx, None #TODO
batom %= opar + bool_expr + cpar, None #TODO

# Arithmetic Expression
arit_expr %= term, None # TODO
arit_expr %= arit_expr + plus + term, None # TODO
arit_expr %= arit_expr + minus + term, None # TODO

term %= factor, None # TODO
term %= term + div + factor, None # TODO
term %= term + star + factor, None # TODO

factor %= power, None # TODO
factor %= factor + pow + power, None # TODO
factor %= factor + dstar + power, None # TODO

power %= atom, None # TODO
power %= minus + atom, None # TODO

atom %= num, None # TODO
atom %= call_expr, None # TODO
atom %= opar + expr + cpar, None # TODO
