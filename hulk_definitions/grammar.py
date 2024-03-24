from cmp.pycompiler import Grammar
import logging
logger = logging.getLogger(__name__)

logger.info("Creating Grammar")
G = Grammar()

#region Grammar Definition

#region NonTerminals Definition
program = G.NonTerminal('<program>', startSymbol=True)
stat_list, stat, typed = G.NonTerminals('<stat_list> <stat> <typing>')
protocol, define, define_block, def_list = G.NonTerminals('<protocol> <define> <define-block> <define-list>')
def_type, properties, methods, prop, method, method_block, type_corpse, inheritance = G.NonTerminals('<def-type> <properties> <methods> <property> <method> <method-block> <type-corpse> <inheritance>')
loop_expr, while_expr, while_expr_block, for_expr, for_expr_block = G.NonTerminals('<loop-expr> <while-expr> <while-expr-block> <for-expr> <for-expr-block>')
let_var, let_var_block, def_func, def_func_block, arg_list = G.NonTerminals('<let-var> <let-var-block> <def-func> <def-func-block> <arg-list>')
assign, var_corpse = G.NonTerminals('<assign> <var-corpse>')
if_expr, if_br, if_expr_block, if_br_block = G.NonTerminals('<if-expr> <if-branches> <if-expr-block> <if-branches-block>')
built_in, e_num, block = G.NonTerminals('<built-in> <e-num> <block>')
expr, term, factor, power, atom = G.NonTerminals('<expr> <term> <factor> <power> <atom>')
func_call, expr_list = G.NonTerminals('<func-call> <expr-list>')
#endregion

#region Terminals Definition
let, func, inx, ifx, elsex, elifx, whilex, forx, typex, selfx, newx = G.Terminals('LET FUNCTION IN IF ELSE ELIF WHILE FOR TYPE SELF NEW')
inheritsx, asx, proto, extends, iterx, dot = G.Terminals('INHERITS AS PROTOCOL EXTENDS ITERABLE DOT')
printx, sinx, cosx, expx, sqrtx, logx, randx, rangex = G.Terminals('PRINT SIN COS EXP SQRT LOG RAND RANGE')
semi, opar, cpar, obracket, cbracket, obrace, cbrace, arrow, comma = G.Terminals('SEMICOLON OPAR CPAR OBRACKET CBRACKET OBRACE CBRACE IMPLICATION COMMA')
equal, plus, minus, star, div, pow, dstar, atx, datx, modx, dassign, colon = G.Terminals('EQUAL PLUS MINUS ASTERISK SLASH CIRCUMFLEX POTENCIAL AT DOUBLE_AT PERCENT DESTRUCTIVE_ASSIGNMENT COLON')
dequal, nequal, gt, lt, gte, lte, isx, andx, orx, notx = G.Terminals('COMP_EQ COMP_NEQ COMP_GT COMP_LT COMP_GTE COMP_LTE IS AND OR NOT')
idx, num, string, true, false, pi, e = G.Terminals('id num string TRUE FALSE PI E')
strx, numx, objx, boolx = G.Terminals('STRING NUMBER OBJECT BOOLEAN')
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
let_var_block %= let + var_corpse + inx + def_func_block, None # Your code here!!! (add rule) 21
let_var_block %= let + var_corpse + inx + if_expr_block, None # Your code here!!! (add rule) 22
let_var_block %= let + var_corpse + inx + let_var_block, None # Your code here!!! (add rule) 23
let_var_block %= let + var_corpse + inx + block, None # Your code here!!! (add rule) 24
assign %= atom + dassign + expr, None # Your code here!!! (add rule) 25

var_corpse %= idx + equal + stat, None # Your code here!!! (add rule) 26
var_corpse %= idx + equal + stat + comma + var_corpse, None # Your code here!!! (add rule) 27
var_corpse %= idx + equal + stat + comma + let + var_corpse, None # Your code here!!! (add rule) 28

var_corpse %= idx + typed + equal + stat, None # Your code here!!! (add rule) 29
var_corpse %= idx + typed + equal + stat + comma + var_corpse, None # Your code here!!! (add rule) 30
var_corpse %= idx + typed + equal + stat + comma + let + var_corpse, None # Your code here!!! (add rule) 31

def_func %= func + idx + opar + arg_list + cpar + arrow + stat, None # Your code here!!! (add rule) 32
def_func_block %= func + idx + opar + arg_list + cpar + arrow + let_var_block, None # Your code here!!! (add rule) 33
def_func_block %= func + idx + opar + arg_list + cpar + arrow + def_func_block, None # Your code here!!! (add rule) 34
def_func_block %= func + idx + opar + arg_list + cpar + arrow + def_func_block, None # Your code here!!! (add rule) 35
def_func_block %= func + idx + opar + arg_list + cpar + block, None # Your code here!!! (add rule) 36

def_func %= func + idx + opar + arg_list + cpar + typed + arrow + stat, None # Your code here!!! (add rule) 37
def_func_block %= func + idx + opar + arg_list + cpar + typed + arrow + let_var_block, None # Your code here!!! (add rule) 38
def_func_block %= func + idx + opar + arg_list + cpar + typed + arrow + if_expr_block, None # Your code here!!! (add rule) 39
def_func_block %= func + idx + opar + arg_list + cpar + typed + arrow + def_func_block, None # Your code here!!! (add rule) 40
def_func_block %= func + idx + opar + arg_list + cpar + typed + block, None # Your code here!!! (add rule) 41

arg_list %= idx, None # Your code here!!! (add rule) 42
arg_list %= idx + typed, None # Your code here!!! (add rule) 43
arg_list %= idx + comma + arg_list, None # Your code here!!! (add rule) 44
arg_list %= idx + typed + comma + arg_list, None # Your code here!!! (add rule) 45

block %= obracket + stat_list + cbracket, None # Your code here!!! (add rule) 46
block %= obracket + cbracket, None # Your code here!!! (add rule) 47

if_expr %= ifx + opar + expr + cpar + stat + elsex + stat, None # Your code here!!! (add rule) 48
if_expr %= ifx +  opar + expr + cpar + block + elsex + stat, None # Your code here!!! (add rule) 49
if_expr %= ifx + opar + expr + cpar + let_var_block + elsex + stat, None # Your code here!!! (add rule) 50
if_expr %= ifx + opar + expr + cpar + def_func_block + elsex + stat, None # Your code here!!! (add rule) 51

if_expr %= ifx + opar + expr + cpar + stat + if_br + elsex + stat, None # Your code here!!! (add rule) 52
if_expr %= ifx +  opar + expr + cpar + block + if_br + elsex + stat, None # Your code here!!! (add rule) 53
if_expr %= ifx + opar + expr + cpar + let_var_block + if_br + elsex + stat, None # Your code here!!! (add rule) 54
if_expr %= ifx + opar + expr + cpar + def_func_block + if_br + elsex + stat, None # Your code here!!! (add rule) 55

if_expr_block %= ifx + opar + expr + cpar + stat + elsex + def_func_block, None # Your code here!!! (add rule) 56
if_expr_block %= ifx +  opar + expr + cpar + block + elsex + def_func_block, None # Your code here!!! (add rule) 57
if_expr_block %= ifx + opar + expr + cpar + let_var_block + elsex + def_func_block, None # Your code here!!! (add rule) 58
if_expr_block %= ifx + opar + expr + cpar + def_func_block + elsex + def_func_block, None # Your code here!!! (add rule) 59

if_expr_block %= ifx + opar + expr + cpar + stat + elsex + let_var_block, None # Your code here!!! (add rule) 60
if_expr_block %= ifx +  opar + expr + cpar + block + elsex + let_var_block, None # Your code here!!! (add rule) 61
if_expr_block %= ifx + opar + expr + cpar + let_var_block + elsex + let_var_block, None # Your code here!!! (add rule) 62
if_expr_block %= ifx + opar + expr + cpar + def_func_block + elsex + let_var_block, None # Your code here!!! (add rule) 63

if_expr_block %= ifx + opar + expr + cpar + stat + elsex + block, None # Your code here!!! (add rule) 64
if_expr_block %= ifx +  opar + expr + cpar + block + elsex + block, None # Your code here!!! (add rule) 65
if_expr_block %= ifx + opar + expr + cpar + let_var_block + elsex + block, None # Your code here!!! (add rule) 66
if_expr_block %= ifx + opar + expr + cpar + def_func_block + elsex + block, None # Your code here!!! (add rule) 67

if_expr_block %= ifx + opar + expr + cpar + stat + if_br + elsex + def_func_block, None # Your code here!!! (add rule) 68
if_expr_block %= ifx +  opar + expr + cpar + block + if_br + elsex + def_func_block, None # Your code here!!! (add rule) 69
if_expr_block %= ifx + opar + expr + cpar + let_var_block + if_br + elsex + def_func_block, None # Your code here!!! (add rule) 70
if_expr_block %= ifx + opar + expr + cpar + def_func_block + if_br + elsex + def_func_block, None # Your code here!!! (add rule) 71

if_expr_block %= ifx + opar + expr + cpar + stat + if_br + elsex + let_var_block, None # Your code here!!! (add rule) 72
if_expr_block %= ifx +  opar + expr + cpar + block + if_br + elsex + let_var_block, None # Your code here!!! (add rule) 73
if_expr_block %= ifx + opar + expr + cpar + let_var_block + if_br + elsex + let_var_block, None # Your code here!!! (add rule) 74
if_expr_block %= ifx + opar + expr + cpar + def_func_block + if_br + elsex + let_var_block, None # Your code here!!! (add rule) 75

if_expr_block %= ifx + opar + expr + cpar + stat + if_br + elsex + block, None # Your code here!!! (add rule) 76
if_expr_block %= ifx +  opar + expr + cpar + block + if_br + elsex + block, None # Your code here!!! (add rule) 77
if_expr_block %= ifx + opar + expr + cpar + let_var_block + if_br + elsex + block, None # Your code here!!! (add rule) 78
if_expr_block %= ifx + opar + expr + cpar + def_func_block + if_br + elsex + block, None # Your code here!!! (add rule) 79

if_br %= elifx + opar + expr + cpar + stat, None # Your code here!!! (add rule) 80
if_br %= elifx + opar + expr + cpar + block, None # Your code here!!! (add rule) 81
if_br %= elifx + opar + expr + cpar + let_var_block, None # Your code here!!! (add rule) 82
if_br %= elifx + opar + expr + cpar + def_func_block, None # Your code here!!! (add rule) 83
if_br %= elifx + opar + expr + cpar + stat + if_br, None # Your code here!!! (add rule) 84
if_br %= elifx + opar + expr + cpar + block + if_br, None # Your code here!!! (add rule) 85
if_br %= elifx + opar + expr + cpar + let_var_block + if_br, None # Your code here!!! (add rule) 86
if_br %= elifx + opar + expr + cpar + def_func_block + if_br, None # Your code here!!! (add rule) 87

expr %= term, None # Your code here!!! (add rule) 88
expr %= expr + atx + term, None # Your code here!!! (add rule) 89
expr %= expr + datx + term, None # Your code here!!! (add rule) 90
expr %= expr + orx + term, None # Your code here!!! (add rule) 91
expr %= expr + plus + term, None # Your code here!!! (add rule) 92
expr %= expr + minus + term, None # Your code here!!! (add rule) 93
expr %= opar + let_var + cpar, None # Your code here!!! (add rule) 94

term %= factor, None # Your code here!!! (add rule) 95
term %= term + star + factor, None # Your code here!!! (add rule) 96
term %= term + div + factor, None # Your code here!!! (add rule) 97
term %= term + modx + factor, None # Your code here!!! (add rule) 98
term %= term + andx + factor, None # Your code here!!! (add rule) 99

factor %= power, None # Your code here!!! (add rule) 100
factor %= notx + factor, None # Your code here!!! (add rule) 101
factor %= minus + factor, None # Your code here!!! (add rule) 102
factor %= power + pow + factor, None # Your code here!!! (add rule) 103
factor %= power + dstar + factor, None # Your code here!!! (add rule) 104
factor %= power + gt + factor, None # Your code here!!! (add rule) 105
factor %= power + lt + factor, None # Your code here!!! (add rule) 106
factor %= power + gte + factor, None # Your code here!!! (add rule) 107
factor %= power + lte + factor, None # Your code here!!! (add rule) 108
factor %= power + dequal + factor, None # Your code here!!! (add rule) 109
factor %= power + nequal + factor, None # Your code here!!! (add rule) 110
factor %= power + isx + factor, None # Your code here!!! (add rule) 111

power %= atom, None # Your code here!!! (add rule) 112
power %= opar + expr + cpar, None # Your code here!!! (add rule) 113

atom %= num, None # Your code here!!! (add rule) 114
atom %= idx, None # Your code here!!! (add rule) 115
atom %= true, None # Your code here!!! (add rule) 116
atom %= false, None # Your code here!!! (add rule) 117
atom %= string, None # Your code here!!! (add rule) 118
atom %= func_call, None # Your code here!!! (add rule) 119
atom %= e_num, None # Your code here!!! (add rule) 120
atom %= built_in, None # Your code here!!! (add rule) 121
atom %= atom + asx + idx, None # Your code here!!! (add rule) 122
atom %= atom + asx + strx, None # Your code here!!! (add rule) 123
atom %= atom + asx + numx, None # Your code here!!! (add rule) 124
atom %= atom + asx + objx, None # Your code here!!! (add rule) 125
atom %= atom + asx + boolx, None # Your code here!!! (add rule) 126
atom %= obrace + expr_list + cbrace, None # Your code here!!! (add rule) 127

built_in %= sinx + opar + expr_list + cpar, None # Your code here!!! (add rule) 128
built_in %= cosx + opar + expr_list + cpar, None # Your code here!!! (add rule) 129
built_in %= randx + opar + expr_list + cpar, None # Your code here!!! (add rule) 130
built_in %= randx + opar + cpar, None # Your code here!!! (add rule) 131
built_in %= expx + opar + expr_list + cpar, None # Your code here!!! (add rule) 132
built_in %= logx + opar + expr_list + cpar, None # Your code here!!! (add rule) 133
built_in %= sqrtx + opar + expr_list + cpar, None # Your code here!!! (add rule) 134
built_in %= printx + opar + expr_list + cpar, None # Your code here!!! (add rule) 135
built_in %= rangex + opar + expr_list + cpar, None # Your code here!!! (add rule) 136

e_num %= pi, None # Your code here!!! (add rule) 137
e_num %= e, None # Your code here!!! (add rule) 138

func_call %= idx + opar + expr_list + cpar, None # Your code here!!! (add rule) 139

expr_list %= stat, None # Your code here!!! (add rule) 140
expr_list %= stat + comma + expr_list, None # Your code here!!! (add rule) 141

loop_expr %= while_expr, None # Your code here!!! (add rule) 142
loop_expr %= for_expr, None # Your code here!!! (add rule) 143

while_expr %= whilex + opar + expr + cpar + stat, None # Your code here!!! (add rule) 144
while_expr_block %= whilex + opar + expr + cpar + block, None # Your code here!!! (add rule) 145
while_expr_block %= whilex + opar + expr + cpar + if_expr_block, None # Your code here!!! (add rule) 146
while_expr_block %= whilex + opar + expr + cpar + let_var_block, None # Your code here!!! (add rule) 147
while_expr_block %= whilex + opar + expr + cpar + def_func_block, None # Your code here!!! (add rule) 148

for_expr %= forx + opar + idx + inx + expr + cpar + stat, None # Your code here!!! (add rule) 149
for_expr_block %= forx + opar + idx + inx + expr + cpar + block, None # Your code here!!! (add rule) 150
for_expr_block %= forx + opar + idx + inx + expr + cpar + if_expr_block, None # Your code here!!! (add rule) 151
for_expr_block %= forx + opar + idx + inx + expr + cpar + let_var_block, None # Your code here!!! (add rule) 152
for_expr_block %= forx + opar + idx + inx + expr + cpar + def_func_block, None # Your code here!!! (add rule) 153

stat %= loop_expr, None # Your code here!!! (add rule) 154

atom %= atom + dot + idx, None # Your code here!!! (add rule) 155
atom %= atom + dot + func_call, None # Your code here!!! (add rule) 156
atom %= atom + obrace + atom + cbrace, None # Your code here!!! (add rule) 157

func_call %= idx + opar + cpar, None # Your code here!!! (add rule) 158

let_var_block %= let + var_corpse + inx + while_expr_block, None # Your code here!!! (add rule) 159
let_var_block %= let + var_corpse + inx + for_expr_block, None # Your code here!!! (add rule) 160

def_func_block %= func + idx + opar + arg_list + cpar + while_expr_block, None # Your code here!!! (add rule) 161
def_func_block %= func + idx + opar + arg_list + cpar + for_expr_block, None # Your code here!!! (add rule) 162

def_func_block %= func + idx + opar + arg_list + cpar + typed + while_expr_block, None # Your code here!!! (add rule) 163
def_func_block %= func + idx + opar + arg_list + cpar + typed + for_expr_block, None # Your code here!!! (add rule) 164

def_func %= func + idx + opar + arg_list + cpar + arrow + while_expr_block, None # Your code here!!! (add rule) 165
def_func %= func + idx + opar + arg_list + cpar + arrow + for_expr_block, None # Your code here!!! (add rule) 166

def_func %= func + idx + opar + arg_list + cpar + typed + arrow + while_expr_block, None # Your code here!!! (add rule) 167
def_func %= func + idx + opar + arg_list + cpar + typed + arrow + for_expr_block, None # Your code here!!! (add rule) 168

def_type %= typex + idx + obracket + cbracket, None # Your code here!!! (add rule) 169
def_type %= typex + idx + inheritsx + idx + obracket + cbracket, None # Your code here!!! (add rule) 170
def_type %= typex + idx + inheritsx + idx + opar + expr_list + cpar + obracket + cbracket, None # Your code here!!! (add rule) 171

def_type %= typex + idx + opar + arg_list + cpar + obracket + cbracket, None # Your code here!!! (add rule) 172
def_type %= typex + idx + opar + arg_list + cpar + inheritsx + idx + obracket + cbracket, None # Your code here!!! (add rule) 173
def_type %= typex + idx + opar + arg_list + cpar + inheritsx + idx + opar + expr_list + cpar + obracket + cbracket, None # Your code here!!! (add rule) 174

def_type %= typex + idx + obracket + type_corpse + cbracket, None # Your code here!!! (add rule) 175
def_type %= typex + idx + inheritsx + idx + obracket + type_corpse + cbracket, None # Your code here!!! (add rule) 176
def_type %= typex + idx + inheritsx + idx + opar + expr_list + cpar + obracket + type_corpse + cbracket, None # Your code here!!! (add rule) 177

def_type %= typex + idx + opar + arg_list + cpar + obracket + type_corpse + cbracket, None # Your code here!!! (add rule) 178
def_type %= typex + idx + opar + arg_list + cpar + inheritsx + idx + obracket + type_corpse + cbracket, None # Your code here!!! (add rule) 179
def_type %= typex + idx + opar + arg_list + cpar + inheritsx + idx + opar + expr_list + cpar + obracket + type_corpse + cbracket, None # Your code here!!! (add rule) 180

type_corpse %= method + semi + type_corpse, None # Your code here!!! (add rule) 181
type_corpse %= prop + semi + type_corpse, None # Your code here!!! (add rule) 182
type_corpse %= method + semi, None # Your code here!!! (add rule) 183
type_corpse %= method_block, None # Your code here!!! (add rule) 183
type_corpse %= method_block + semi, None # Your code here!!! (add rule) 183
type_corpse %= method_block + type_corpse, None # Your code here!!! (add rule) 183
type_corpse %= method_block + semi + type_corpse, None # Your code here!!! (add rule) 183
type_corpse %= prop + semi, None # Your code here!!! (add rule) 184

atom %= selfx, None # Your code here!!! (add rule) 185

prop %= idx + equal + atom, None # Your code here!!! (add rule) 186
prop %= idx + typed + equal + atom, None # Your code here!!! (add rule) 187

method %= idx + opar + arg_list + cpar + arrow + stat, None # Your code here!!! (add rule) 188
method %= idx + opar + cpar + arrow + stat, None # Your code here!!! (add rule) 189
method_block %= idx + opar + arg_list + cpar + block, None # Your code here!!! (add rule) 190
method_block %= idx + opar + cpar + block, None # Your code here!!! (add rule) 191

method %= idx + opar + arg_list + cpar + typed + arrow + stat, None # Your code here!!! (add rule) 192
method %= idx + opar + cpar + typed + arrow + stat, None # Your code here!!! (add rule) 193
method_block %= idx + opar + arg_list + cpar + typed + block, None # Your code here!!! (add rule) 194
method_block %= idx + opar + cpar + typed + block, None # Your code here!!! (add rule) 195

stat_list %= def_type, None # Your code here!!! (add rule) 196
stat_list %= def_type + stat_list, None # Your code here!!! (add rule) 197

expr %= newx + func_call, None # Your code here!!! (add rule) 198

typed %= colon + idx, None # Your code here!!! (add rule) 199
typed %= colon + strx, None # Your code here!!! (add rule) 200
typed %= colon + numx, None # Your code here!!! (add rule) 201
typed %= colon + objx, None # Your code here!!! (add rule) 202
typed %= colon + boolx, None # Your code here!!! (add rule) 203

protocol %= proto + idx + obracket + def_list + cbracket, None # Your code here!!! (add rule) 204
protocol %= proto + idx + extends + idx + obracket + def_list + cbracket, None # Your code here!!! (add rule) 205

def_list %= define + semi, None # Your code here!!! (add rule) 206
def_list %= define_block, None # Your code here!!! (add rule) 207
def_list %= define + semi + def_list, None # Your code here!!! (add rule) 208
def_list %= define_block + def_list, None # Your code here!!! (add rule) 209

define_block %= idx + opar + cpar + obracket + cbracket, None # Your code here!!! (add rule) 210
define_block %= idx + opar + arg_list + cpar + obracket + cbracket, None # Your code here!!! (add rule) 211
define_block %= idx + opar + cpar + typed + obracket + cbracket, None # Your code here!!! (add rule) 212
define_block %= idx + opar + arg_list + cpar + typed + obracket + cbracket, None # Your code here!!! (add rule) 213

define %= idx + opar + cpar, None # Your code here!!! (add rule) 214
define %= idx + opar + arg_list + cpar, None # Your code here!!! (add rule) 215
define %= idx + opar + cpar + typed, None # Your code here!!! (add rule) 216
define %= idx + opar + arg_list + cpar + typed, None # Your code here!!! (add rule) 217

stat_list %= protocol, None # Your code here!!! (add rule) 218
stat_list %= protocol + stat_list, None # Your code here!!! (add rule) 219

#endregion
#endregion

logger.info("Grammar created")
for i, production in  enumerate(G.Productions):
    logger.info("Production %d: %s" % (i, production))