from cmp.pycompiler import Grammar
import logging
logger = logging.getLogger(__name__)

logger.info("Creating Grammar")
G = Grammar()

#region Grammar Definition

#region NonTerminals Definition
program = G.NonTerminal('<program>', startSymbol=True)
stat_list, stat = G.NonTerminals('<stat_list> <stat>')
def_type, properties, methods, prop, method, type_corpse = G.NonTerminals('<def-type> <properties> <methods> <property> <method> <type-corpse>')
loop_expr, while_expr, while_expr_block, for_expr, for_expr_block = G.NonTerminals('<loop-expr> <while-expr> <while-expr-block> <for-expr> <for-expr-block>')
let_var, let_var_block, def_func, def_func_block, arg_list = G.NonTerminals('<let-var> <let-var-block> <def-func> <def-func-block> <arg-list>')
assign, var_corpse = G.NonTerminals('<assign> <var-corpse>')
if_expr, if_br = G.NonTerminals('<if-expr> <if-branches>')
built_in, e_num, block = G.NonTerminals('<built-in> <e-num> <block>')
expr, term, factor, power, atom = G.NonTerminals('<expr> <term> <factor> <power> <atom>')
func_call, expr_list = G.NonTerminals('<func-call> <expr-list>')
#endregion

#region Terminals Definition
let, func, inx, ifx, elsex, elifx, whilex, forx, typex, selfx, newx = G.Terminals('LET FUNCTION IN IF ELSE ELIF WHILE FOR TYPE SELF NEW')
inheritsx, asx, proto, extends, iterx, dot = G.Terminals('INHERITS AS PROTOCOL EXTENDS ITERABLE DOT')
printx, sinx, cosx, expx, sqrtx, logx, randx, rangex = G.Terminals('PRINT SIN COS EXP SQRT LOG RAND RANGE')
semi, opar, cpar, obracket, cbracket, obrace, cbrace, arrow, comma = G.Terminals('SEMICOLON OPAR CPAR OBRACKET CBRACKET OBRACE CBRACE IMPLICATION COMMA')
equal, plus, minus, star, div, pow, dstar, atx, datx, modx, dassign = G.Terminals('EQUAL PLUS MINUS ASTERISK SLASH CIRCUMFLEX POTENCIAL AT DOUBLE_AT PERCENT DESTRUCTIVE_ASSIGNMENT')
dequal, nequal, gt, lt, gte, lte, isx, andx, orx, notx = G.Terminals('COMP_EQ COMP_NEQ COMP_GT COMP_LT COMP_GTE COMP_LTE IS AND OR NOT')
idx, num, string, true, false, pi, e = G.Terminals('id num string TRUE FALSE PI E')
strx, numx, objx, boolx = G.Terminals('String Number Object Boolean')
eof = G.EOF
#endregion

#region Productions Definition
program %= stat_list, lambda h,s: None # 0

stat_list %= stat + semi, None # Your code here!!! (add rule) 1
stat_list %= stat + semi + stat_list, None # Your code here!!! (add rule) 2
stat_list %= block, None # Your code here!!! (add rule) 3
stat_list %= block + stat_list, None # Your code here!!! (add rule) 4
stat_list %= block + semi, None # Your code here!!! (add rule) 5
stat_list %= block + semi + stat_list, None # Your code here!!! (add rule) 6
stat_list %= let_var_block, None # Your code here!!! (add rule) 7
stat_list %= let_var_block + stat_list, None # Your code here!!! (add rule) 8
stat_list %= let_var_block + semi, None # Your code here!!! (add rule) 9
stat_list %= let_var_block + semi + stat_list, None # Your code here!!! (add rule) 10
stat_list %= def_func_block, None # Your code here!!! (add rule) 11
stat_list %= def_func_block + stat_list, None # Your code here!!! (add rule) 12
stat_list %= def_func_block + semi, None # Your code here!!! (add rule) 13
stat_list %= def_func_block + semi + stat_list, None # Your code here!!! (add rule) 14

stat %= let_var, None # Your code here!!! (add rule) 15
stat %= def_func, None # Your code here!!! (add rule) 16
stat %= expr, None # Your code here!!! (add rule) 17
stat %= assign, None # Your code here!!! (add rule) 18
stat %= if_expr, None # Your code here!!! (add rule) 19

let_var %= let + var_corpse + inx + stat, None # Your code here!!! (add rule) 20
let_var %= let + var_corpse + inx + def_func_block, None # Your code here!!! (add rule) 21
let_var %= let + var_corpse + inx + let_var_block, None # Your code here!!! (add rule) 22
let_var_block %= let + var_corpse + inx + block, None # Your code here!!! (add rule) 23
assign %= idx + dassign + expr, None # Your code here!!! (add rule) 24

var_corpse %= idx + equal + stat, None # Your code here!!! (add rule) 25
var_corpse %= idx + equal + stat + comma + var_corpse, None # Your code here!!! (add rule) 26
var_corpse %= idx + equal + stat + comma + let + var_corpse, None # Your code here!!! (add rule) 27

def_func %= func + idx + opar + arg_list + cpar + arrow + stat, None # Your code here!!! (add rule) 28
def_func %= func + idx + opar + arg_list + cpar + arrow + let_var_block, None # Your code here!!! (add rule) 29
def_func %= func + idx + opar + arg_list + cpar + arrow + def_func_block, None # Your code here!!! (add rule) 30
def_func_block %= func + idx + opar + arg_list + cpar + block, None # Your code here!!! (add rule) 31

arg_list %= idx, None # Your code here!!! (add rule) 32
arg_list %= idx + comma + arg_list, None # Your code here!!! (add rule) 33

block %= obracket + stat_list + cbracket, None # Your code here!!! (add rule) 34

if_expr %= ifx + opar + expr + cpar + stat + if_br, None # Your code here!!! (add rule) 35
if_expr %= ifx +  opar + expr + cpar + block + if_br, None # Your code here!!! (add rule) 36
if_expr %= ifx + opar + expr + cpar + let_var_block + if_br, None # Your code here!!! (add rule) 37
if_expr %= ifx + opar + expr + cpar + def_func_block + if_br, None # Your code here!!! (add rule) 38

if_br %= elsex + stat, None # Your code here!!! (add rule) 39
if_br %= elsex + block, None # Your code here!!! (add rule) 40
if_br %= elsex + let_var_block, None # Your code here!!! (add rule) 41
if_br %= elsex + def_func_block, None # Your code here!!! (add rule) 42
if_br %= elifx + opar + expr + cpar + stat + if_br, None # Your code here!!! (add rule) 43
if_br %= elifx + opar + expr + cpar + block + if_br, None # Your code here!!! (add rule) 44
if_br %= elifx + opar + expr + cpar + let_var_block + if_br, None # Your code here!!! (add rule) 45
if_br %= elifx + opar + expr + cpar + def_func_block + if_br, None # Your code here!!! (add rule) 46

expr %= term, None # Your code here!!! (add rule) 47
expr %= expr + atx + term, None # Your code here!!! (add rule) 48
expr %= expr + datx + term, None # Your code here!!! (add rule) 48
expr %= expr + orx + term, None # Your code here!!! (add rule) 49
expr %= expr + plus + term, None # Your code here!!! (add rule) 50
expr %= expr + minus + term, None # Your code here!!! (add rule) 51
expr %= opar + let_var + cpar, None # Your code here!!! (add rule) 52

term %= factor, None # Your code here!!! (add rule) 53
term %= term + star + factor, None # Your code here!!! (add rule) 54
term %= term + div + factor, None # Your code here!!! (add rule) 55
term %= term + modx + factor, None # Your code here!!! (add rule) 56
term %= term + andx + factor, None # Your code here!!! (add rule) 57

factor %= power, None # Your code here!!! (add rule) 58
factor %= notx + factor, None # Your code here!!! (add rule) 59
factor %= minus + factor, None # Your code here!!! (add rule) 60
factor %= power + pow + factor, None # Your code here!!! (add rule) 61
factor %= power + dstar + factor, None # Your code here!!! (add rule) 62
factor %= power + gt + factor, None # Your code here!!! (add rule) 63
factor %= power + lt + factor, None # Your code here!!! (add rule) 64
factor %= power + gte + factor, None # Your code here!!! (add rule) 65
factor %= power + lte + factor, None # Your code here!!! (add rule) 66
factor %= power + dequal + factor, None # Your code here!!! (add rule) 67
factor %= power + nequal + factor, None # Your code here!!! (add rule) 68
factor %= power + isx + factor, None # Your code here!!! (add rule) 69

power %= atom, None # Your code here!!! (add rule) 70
power %= opar + expr + cpar, None # Your code here!!! (add rule) 71

atom %= num, None # Your code here!!! (add rule) 72
atom %= idx, None # Your code here!!! (add rule) 73
atom %= true, None # Your code here!!! (add rule) 74
atom %= false, None # Your code here!!! (add rule) 75
atom %= string, None # Your code here!!! (add rule) 76
atom %= func_call, None # Your code here!!! (add rule) 77
atom %= e_num, None # Your code here!!! (add rule) 78
atom %= built_in, None # Your code here!!! (add rule) 78

built_in %= sinx + opar + expr_list + cpar, None # Your code here!!! (add rule) 80
built_in %= cosx + opar + expr_list + cpar, None # Your code here!!! (add rule) 81
built_in %= randx + opar + expr_list + cpar, None # Your code here!!! (add rule) 82
built_in %= expx + opar + expr_list + cpar, None # Your code here!!! (add rule) 83
built_in %= logx + opar + expr_list + cpar, None # Your code here!!! (add rule) 84
built_in %= sqrtx + opar + expr_list + cpar, None # Your code here!!! (add rule) 85
built_in %= printx + opar + expr_list + cpar, None # Your code here!!! (add rule) 86
built_in %= rangex + opar + expr_list + cpar, None # Your code here!!! (add rule) 87

e_num %= pi, None # Your code here!!! (add rule) 88
e_num %= e, None # Your code here!!! (add rule) 89

func_call %= idx + opar + expr_list + cpar, None # Your code here!!! (add rule) 90

expr_list %= stat, None # Your code here!!! (add rule) 91
expr_list %= stat + comma + expr_list, None # Your code here!!! (add rule) 92

loop_expr %= while_expr, None # Your code here!!! (add rule) 93
loop_expr %= for_expr, None # Your code here!!! (add rule) 94

while_expr %= whilex + opar + expr + cpar + stat, None # Your code here!!! (add rule) 95
while_expr_block %= whilex + opar + expr + cpar + block, None # Your code here!!! (add rule) 96
while_expr_block %= whilex + opar + expr + cpar + let_var_block, None # Your code here!!! (add rule) 97
while_expr_block %= whilex + opar + expr + cpar + def_func_block, None # Your code here!!! (add rule) 98

for_expr %= forx + opar + idx + inx + expr + cpar + stat, None # Your code here!!! (add rule) 99
for_expr_block %= forx + opar + idx + inx + expr + cpar + block, None # Your code here!!! (add rule) 100
for_expr_block %= forx + opar + idx + inx + expr + cpar + let_var_block, None # Your code here!!! (add rule) 101
for_expr_block %= forx + opar + idx + inx + expr + cpar + def_func_block, None # Your code here!!! (add rule) 102

stat %= loop_expr, None # Your code here!!! (add rule) 103

atom %= atom + dot + idx, None # Your code here!!! (add rule) 104
atom %= atom + dot + func_call, None # Your code here!!! (add rule) 105
atom %= atom + obrace + atom + cbrace, None # Your code here!!! (add rule) 106

func_call %= idx + opar + cpar, None # Your code here!!! (add rule) 107

let_var_block %= let + var_corpse + inx + while_expr_block, None # Your code here!!! (add rule) 108
let_var_block %= let + var_corpse + inx + for_expr_block, None # Your code here!!! (add rule) 109
def_func_block %= func + idx + opar + arg_list + cpar + while_expr_block, None # Your code here!!! (add rule) 110
def_func_block %= func + idx + opar + arg_list + cpar + for_expr_block, None # Your code here!!! (add rule) 111
def_func %= func + idx + opar + arg_list + cpar + arrow + while_expr_block, None # Your code here!!! (add rule) 112
def_func %= func + idx + opar + arg_list + cpar + arrow + for_expr_block, None # Your code here!!! (add rule) 113

def_type %= typex + idx + obracket + type_corpse + cbracket, None # Your code here!!! (add rule)
def_type %= typex + idx + opar + arg_list + cpar + obracket + type_corpse + cbracket, None # Your code here!!! (add rule)

def_type %= typex + idx + obracket + cbracket, None # Your code here!!! (add rule)
def_type %= typex + idx + opar + arg_list + cpar + obracket + cbracket, None # Your code here!!! (add rule)

type_corpse %= type_corpse + properties, None # Your code here!!! (add rule)
type_corpse %= type_corpse + methods, None # Your code here!!! (add rule)
type_corpse %= properties, None # Your code here!!! (add rule)
type_corpse %= methods, None # Your code here!!! (add rule)

properties %= prop, None # Your code here!!! (add rule)
properties %= prop + semi + properties, None # Your code here!!! (add rule)

methods %= method, None # Your code here!!! (add rule)
methods %= method + semi + methods, None # Your code here!!! (add rule)

atom %= selfx, None # Your code here!!! (add rule)

prop %= idx + equal + atom, None # Your code here!!! (add rule)

method %= idx + opar + arg_list + cpar + arrow + stat, None # Your code here!!! (add rule)
method %= idx + opar + cpar + arrow + stat, None # Your code here!!! (add rule)

stat_list %= def_type, None # Your code here!!! (add rule)

#endregion
#endregion

logger.info("Grammar created")
for i, production in  enumerate(G.Productions):
    logger.info("Production %d: %s" % (i, production))