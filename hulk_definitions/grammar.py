from tools.pycompiler import Grammar
import logging
logger = logging.getLogger(__name__)
from hulk_definitions.ast import *

logger.info("Creating Grammar")
G = Grammar()

#region Grammar Definition

#region NonTerminals Definition
program = G.NonTerminal('<program>', startSymbol=True)
stat_list, typed = G.NonTerminals('<stat_list> <typing>')
or_expr, and_expr, compare, arit = G.NonTerminals('<or-expr> <and-expr> <compare> <arit>')
protocol, define, define_block, def_list = G.NonTerminals('<protocol> <define> <define-block> <define-list>')
def_type, properties, methods, prop, method, method_block, type_corpse, inheritance = G.NonTerminals('<def-type> <properties> <methods> <property> <method> <method-block> <type-corpse> <inheritance>')
def_func, arg_list, definitions, if_br = G.NonTerminals('<def-func> <arg-list> <definitions> <if-branches>')
assign, assign_block, var_corpse = G.NonTerminals('<assign> <assign-block> <var-corpse>')
built_in, e_num, block, block_corpse = G.NonTerminals('<built-in> <e-num> <block> <block-corpse>')
expr, eexpr, expr_block, term, factor, power, atom = G.NonTerminals('<expr> <eexpr> <expr-block> <term> <factor> <power> <atom>')
func_call, expr_list, definition = G.NonTerminals('<func-call> <expr-list> <definition>')
#endregion

#region Terminals Definition
let, func, inx, ifx, elsex, elifx, whilex, forx, typex, base, newx = G.Terminals('LET FUNCTION IN IF ELSE ELIF WHILE FOR TYPE BASE NEW')
inheritsx, asx, proto, extends, iterx, dot = G.Terminals('INHERITS AS PROTOCOL EXTENDS ITERABLE DOT')
printx, sinx, cosx, expx, sqrtx, logx, randx, rangex = G.Terminals('PRINT SIN COS EXP SQRT LOG RAND RANGE')
semi, opar, cpar, obracket, cbracket, obrace, cbrace, arrow, comma = G.Terminals('SEMICOLON OPAR CPAR OBRACKET CBRACKET OBRACE CBRACE IMPLICATION COMMA')
equal, plus, minus, star, div, pow, dstar, atx, datx, modx, dassign, colon, dpipe = G.Terminals('EQUAL PLUS MINUS ASTERISK SLASH CIRCUMFLEX POTENCIAL AT DOUBLE_AT PERCENT DESTRUCTIVE_ASSIGNMENT COLON DOUBLE_PIPE')
dequal, nequal, gt, lt, gte, lte, isx, andx, orx, notx = G.Terminals('COMP_EQ COMP_NEQ COMP_GT COMP_LT COMP_GTE COMP_LTE IS AND OR NOT')
idx, num, string, true, false, pi, e = G.Terminals('id num string TRUE FALSE PI E')
strx, numx, objx, boolx = G.Terminals('STRING NUMBER OBJECT BOOLEAN')
eof = G.EOF
#endregion

#region Productions Definition
program %= stat_list, lambda h,s: Program(s[1]) #1

stat_list %= eexpr, lambda h,s: s[1] #2
stat_list %= definitions + eexpr, lambda h,s: s[1] + s[2] #3

definitions %= definition, lambda h,s: [s[1]] #4
definitions %= definition + definitions, lambda h,s: [s[1]] + s[2] #5

definition %= protocol, lambda h,s: s[1] #6
definition %= protocol + semi, lambda h,s: s[1] #6
definition %= def_type, lambda h,s: s[1] #7
definition %= def_type + semi, lambda h,s: s[1] #7
definition %= def_func, lambda h,s: s[1] #8

eexpr %= expr + semi, lambda h,s: [s[1]] #9
eexpr %= expr_block, lambda h,s: [s[1]] #10
eexpr %= expr_block + semi, lambda h,s: [s[1]] #11

expr %= atom + dassign + expr, lambda h,s: Assign(s[1], s[3]) #12
expr %= let + var_corpse + inx + expr, lambda h,s: LetList([Let(x[0], x[1], s[4], x[2]) for x in s[2]]) #13
expr %= idx + asx + idx, lambda h,s: As(s[1], s[3]) #14
expr %= idx + asx + strx, lambda h,s: As(s[1], s[3]) #15
expr %= idx + asx + numx, lambda h,s: As(s[1], s[3]) #16
expr %= idx + asx + objx, lambda h,s: As(s[1], s[3]) #17
expr %= idx + asx + boolx, lambda h,s: As(s[1], s[3]) #18
expr %= newx + func_call, lambda h,s: CreateInstance(s[2].value, s[2].args) #19
expr %= or_expr, lambda h,s: s[1] #20
expr %= or_expr + datx + expr, lambda h,s: DoubleAt(s[1], s[3]) #21
expr %= or_expr + atx + expr, lambda h,s: At(s[1], s[3]) #22
expr %= ifx + opar + expr + cpar + expr + elsex + expr, lambda h,s: Conditional(s[3], s[5], s[7]) #23
expr %= ifx + opar + expr + cpar + expr_block + elsex + expr, lambda h,s: Conditional(s[3], s[5], s[7]) #24
expr %= ifx + opar + expr_block + cpar + expr + elsex + expr, lambda h,s: Conditional(s[3], s[5], s[7]) #25
expr %= ifx + opar + expr_block + cpar + expr_block + elsex + expr, lambda h,s: Conditional(s[3], s[5], s[7]) #26
expr %= ifx + opar + expr + cpar + expr + if_br + elsex + expr, lambda h,s: Conditional(s[3], s[5], s[8], s[6]) #27
expr %= ifx + opar + expr + cpar + expr_block + if_br + elsex + expr, lambda h,s: Conditional(s[3], s[5], s[8], s[6]) #28
expr %= ifx + opar + expr_block + cpar + expr + if_br + elsex + expr, lambda h,s: Conditional(s[3], s[5], s[8], s[6]) #29
expr %= ifx + opar + expr_block + cpar + expr_block + if_br + elsex + expr, lambda h,s: Conditional(s[3], s[5], s[8], s[6]) #30
expr %= whilex + opar + expr + cpar + expr, lambda h,s: While(s[3], s[5]) #30
expr %= whilex + opar + expr_block + cpar + expr, lambda h,s: While(s[3], s[5]) #31
expr %= forx + opar + idx + inx + expr + cpar + expr, lambda h,s: For(s[3], s[5], s[7]) #32
expr %= forx + opar + idx + inx + expr_block + cpar + expr, lambda h,s: For(s[3], s[5], s[7]) #33

expr_block %= obracket + block_corpse + cbracket, lambda h,s: Block(s[2]) #34
expr_block %= atom + dassign + expr_block, lambda h,s: Assign(s[1], s[3]) #35
expr_block %= or_expr + datx + expr_block, lambda h,s: DoubleAt(s[1], s[3]) 
expr_block %= or_expr + atx + expr_block, lambda h,s: At(s[1], s[3])
expr_block %= let + var_corpse + inx + expr_block, lambda h,s: LetList([Let(x[0], x[1], s[4], x[2]) for x in s[2]]) #36
expr_block %= ifx + opar + expr + cpar + expr + elsex + expr_block, lambda h,s: Conditional(s[3], s[5], s[7]) #37
expr_block %= ifx + opar + expr + cpar + expr_block + elsex + expr_block, lambda h,s: Conditional(s[3], s[5], s[7]) #38
expr_block %= ifx + opar + expr_block + cpar + expr + elsex + expr_block, lambda h,s: Conditional(s[3], s[5], s[7]) #39
expr_block %= ifx + opar + expr_block + cpar + expr_block + elsex + expr_block, lambda h,s: Conditional(s[3], s[5], s[7]) #40
expr_block %= ifx + opar + expr + cpar + expr + if_br + elsex + expr_block, lambda h,s: Conditional(s[3], s[5], s[8], s[6]) #41
expr_block %= ifx + opar + expr + cpar + expr + if_br + elsex + expr_block, lambda h,s: Conditional(s[3], s[5], s[8], s[6]) #42
expr_block %= ifx + opar + expr_block + cpar + expr + if_br + elsex + expr_block, lambda h,s: Conditional(s[3], s[5], s[8], s[6]) #43
expr_block %= ifx + opar + expr_block + cpar + expr + if_br + elsex + expr_block, lambda h,s: Conditional(s[3], s[5], s[8], s[6]) #44
expr_block %= whilex + opar + expr + cpar + expr_block, lambda h,s: While(s[3], s[5]) #45
expr_block %= whilex + opar + expr_block + cpar + expr_block, lambda h,s: While(s[3], s[5]) #46
expr_block %= forx + opar + idx + inx + expr + cpar + expr_block, lambda h,s: For(s[3], s[5], s[7]) #47
expr_block %= forx + opar + idx + inx + expr_block + cpar + expr_block, lambda h,s: For(s[3], s[5], s[7]) #48

block_corpse %= eexpr, lambda h,s: s[1] #49
block_corpse %= block_corpse + eexpr, lambda h,s: s[1] + s[2] #50

var_corpse %= idx + equal + expr, lambda h,s: [[s[1], s[3], None]] #51
var_corpse %= idx + equal + expr + comma + var_corpse, lambda h,s: [[s[1], s[3], None]] + s[5] #52
var_corpse %= idx + equal + expr + comma + let + var_corpse, lambda h,s: [[s[1], s[3], None]] + s[6] #53

var_corpse %= idx + equal + expr_block, lambda h,s: [[s[1], s[3], None]] #54
var_corpse %= idx + equal + expr_block + comma + var_corpse, lambda h,s: [[s[1], s[3], None]] + s[5] #55
var_corpse %= idx + equal + expr_block + comma + let + var_corpse, lambda h,s: [[s[1], s[3], None]] + s[6] #56

var_corpse %= idx + typed + equal + expr, lambda h,s: [[s[1], s[4], s[2]]] #57
var_corpse %= idx + typed + equal + expr + comma + var_corpse, lambda h,s: [[s[1], s[4], s[2]]] + s[6] #58
var_corpse %= idx + typed + equal + expr + comma + let + var_corpse, lambda h,s: [[s[1], s[4], s[2]]] + s[7] #59

var_corpse %= idx + typed + equal + expr_block, lambda h,s: [[s[1], s[4], s[2]]] #60
var_corpse %= idx + typed + equal + expr_block + comma + var_corpse, lambda h,s: [[s[1], s[4], s[2]]] + s[6] #61
var_corpse %= idx + typed + equal + expr_block + comma + let + var_corpse, lambda h,s: [[s[1], s[4], s[2]]] + s[7] #62

def_func %= func + idx + opar + arg_list + cpar + arrow + eexpr, lambda h,s: Function(s[2], s[4], s[6]) #63
def_func %= func + idx + opar + arg_list + cpar + typed + arrow + eexpr, lambda h,s: Function(s[2], s[4], s[7], s[5]) #64
def_func %= func + idx + opar + arg_list + cpar + expr_block, lambda h,s: Function(s[2], s[4], s[6]) #65
def_func %= func + idx + opar + arg_list + cpar + typed + expr_block, lambda h,s: Function(s[2], s[4], s[7], s[5]) #66
def_func %= func + idx + opar + arg_list + cpar + expr_block + semi, lambda h,s: Function(s[2], s[4], s[6]) #65
def_func %= func + idx + opar + arg_list + cpar + typed + expr_block + semi, lambda h,s: Function(s[2], s[4], s[7], s[5]) #66

arg_list %= idx, lambda h,s: [(s[1], None)] #67
arg_list %= idx + typed, lambda h,s: [(s[1], s[2])] #68
arg_list %= idx + comma + arg_list, lambda h,s: [(s[1], None)] + s[3] #69
arg_list %= idx + typed + comma + arg_list, lambda h,s: [(s[1], s[2])] + s[4] #70

if_br %= elifx + opar + expr + cpar + expr, lambda h,s: [Branch(s[3], s[5])] #71
if_br %= elifx + opar + expr + cpar + expr_block, lambda h,s: [Branch(s[3], s[5])] #72
if_br %= elifx + opar + expr_block + cpar + expr, lambda h,s: [Branch(s[3], s[5])] #73
if_br %= elifx + opar + expr_block + cpar + expr_block, lambda h,s: [Branch(s[3], s[5])] #74

or_expr %= and_expr, lambda h,s: s[1] #75
or_expr %= or_expr + orx + and_expr, lambda h,s: Or(s[1], s[3]) #76

and_expr %= compare, lambda h,s: s[1] #77
and_expr %= and_expr + andx + compare, lambda h,s: And(s[1], s[3]) #78

compare %= arit + gt + arit, lambda h,s: GreaterThan(s[1], s[3]) #79
compare %= arit + lt + arit, lambda h,s: LessThan(s[1], s[3]) #80
compare %= arit + gte + arit, lambda h,s: GreaterEqual(s[1], s[3]) #81
compare %= arit + lte + arit, lambda h,s: LessEqual(s[1], s[3]) #82
compare %= arit + dequal + arit, lambda h,s: CompareEqual(s[1], s[3]) #83
compare %= arit + nequal + arit, lambda h,s: NotEqual(s[1], s[3]) #84
compare %= arit + isx + idx, lambda h,s: Is(s[1], s[3]) #85
compare %= arit, lambda h,s: s[1] #86

arit %= term, lambda h,s: s[1] #87
arit %= arit + plus + term, lambda h,s: Plus(s[1], s[3]) #88
arit %= arit + minus + term, lambda h,s: BinaryMinus(s[1], s[3]) #89

term %= factor, lambda h,s: s[1] #90
term %= term + star + factor, lambda h,s: Star(s[1], s[3]) #91
term %= term + div + factor, lambda h,s: Div(s[1], s[3]) #92
term %= term + modx + factor, lambda h,s: Mod(s[1], s[3]) #93

factor %= power, lambda h,s: s[1] #94
factor %= notx + factor, lambda h,s: Not(s[2]) #95
factor %= minus + factor, lambda h,s: UnaryMinus(s[2]) #96

power %= atom, lambda h,s: s[1] #97
power %= atom + pow + power, lambda h,s: Pow(s[1], s[3]) #98
power %= atom + dstar + power, lambda h,s: Pow(s[1], s[3]) #99

atom %= opar + expr + cpar, lambda h,s: s[2] #100
atom %= opar + expr_block + cpar, lambda h,s: s[2] #101
atom %= num, lambda h,s: Number(float(s[1])) #102
atom %= idx, lambda h,s: Var(s[1]) #103
atom %= true, lambda h,s: Bool(True) #104
atom %= false, lambda h,s: Bool(False) #105
atom %= string, lambda h,s: Str(s[1]) #106
atom %= func_call, lambda h,s: s[1] #107
atom %= e_num, lambda h,s: s[1] #108
atom %= built_in, lambda h,s: s[1] #109
atom %= obrace + expr_list + cbrace, lambda h,s: Vector(s[2]) #110
atom %= obrace + expr + dpipe + idx + inx + expr + cbrace, lambda h,s: VectorComprehension(s[6], (s[2], s[4])) #111
atom %= atom + dot + idx, lambda h,s: Invoke(s[1], s[3]) #112
atom %= atom + dot + func_call, lambda h,s: Invoke(s[1], s[3]) #113
atom %= atom + obrace + expr + cbrace, lambda h,s: Indexing(s[1], s[3]) #114
atom %= atom + obrace + expr_block + cbrace, lambda h,s: Indexing(s[1], s[3]) #115

built_in %= sinx + opar + expr_list + cpar, lambda h,s: Sin(s[3]) #116
built_in %= cosx + opar + expr_list + cpar, lambda h,s: Cos(s[3]) #117
built_in %= randx + opar + expr_list + cpar, lambda h,s: Rand(s[3]) #118
built_in %= randx + opar + cpar, lambda h,s: Rand(None) #119
built_in %= expx + opar + expr_list + cpar, lambda h,s: Exp(s[3]) #120
built_in %= logx + opar + expr_list + cpar, lambda h,s: Log(s[3]) #121
built_in %= sqrtx + opar + expr_list + cpar, lambda h,s: Sqrt(s[3]) #122
built_in %= printx + opar + expr_list + cpar, lambda h,s: Print(s[3]) #123
built_in %= rangex + opar + expr_list + cpar, lambda h,s: Range(s[3]) #124
built_in %= base + opar + expr_list + cpar, lambda h,s: Base(s[3]) #125
built_in %= base + opar + cpar, lambda h,s: Base(None) #126

e_num %= pi, lambda h,s: Pi() #127
e_num %= e, lambda h,s: E() #128

func_call %= idx + opar + expr_list + cpar, lambda h,s: Call(s[1], s[3]) #129
func_call %= idx + opar + cpar, lambda h,s: Call(s[1], None) #130

expr_list %= expr, lambda h,s: [s[1]] #131
expr_list %= expr_block, lambda h,s: [s[1]] #132
expr_list %= expr + comma + expr_list, lambda h,s: [s[1]] + s[3] #133
expr_list %= expr_block + comma + expr_list, lambda h,s: [s[1]] + s[3] #134

def_type %= typex + idx + obracket + cbracket, lambda h,s: TypeDef(s[2], None, None) #135
def_type %= typex + idx + inheritsx + idx + obracket + cbracket, lambda h,s: TypeDef(s[2], None, None, s[4]) #136
def_type %= typex + idx + inheritsx + idx + opar + expr_list + cpar + obracket + cbracket, lambda h,s: TypeDef(s[2], None, None, s[4], s[6]) #137

def_type %= typex + idx + opar + arg_list + cpar + obracket + cbracket, lambda h,s: TypeDef(s[2], None, s[4]) #138
def_type %= typex + idx + opar + arg_list + cpar + inheritsx + idx + obracket + cbracket, lambda h,s: TypeDef(s[2], None, s[4], s[7]) #139
def_type %= typex + idx + opar + arg_list + cpar + inheritsx + idx + opar + expr_list + cpar + obracket + cbracket, lambda h,s: TypeDef(s[2], None, s[4], s[7], s[9]) #140

def_type %= typex + idx + obracket + type_corpse + cbracket, lambda h,s: TypeDef(s[2], s[4], None) #141
def_type %= typex + idx + inheritsx + idx + obracket + type_corpse + cbracket, lambda h,s: TypeDef(s[2], s[6], None, s[4]) #142
def_type %= typex + idx + inheritsx + idx + opar + expr_list + cpar + obracket + type_corpse + cbracket, lambda h,s: TypeDef(s[2], s[9], None, s[4], s[6]) #143

def_type %= typex + idx + opar + arg_list + cpar + obracket + type_corpse + cbracket, lambda h,s: TypeDef(s[2], s[7], s[4]) #144
def_type %= typex + idx + opar + arg_list + cpar + inheritsx + idx + obracket + type_corpse + cbracket, lambda h,s: TypeDef(s[2], s[9], s[4], s[7]) #145
def_type %= typex + idx + opar + arg_list + cpar + inheritsx + idx + opar + expr_list + cpar + obracket + type_corpse + cbracket, lambda h,s: TypeDef(s[2], s[12], s[4], s[7], s[9]) #146

type_corpse %= prop + semi, lambda h,s: [s[1]] #147
type_corpse %= prop + semi + type_corpse, lambda h,s: [s[1]] + s[3] #148
type_corpse %= method + semi, lambda h,s: [s[1]] #149
type_corpse %= method + semi + type_corpse, lambda h,s: [s[1]] + s[3] #150
type_corpse %= method_block, lambda h,s: [s[1]] #151
type_corpse %= method_block + semi, lambda h,s: [s[1]] #152
type_corpse %= method_block + type_corpse, lambda h,s: [s[1]] + s[2] #153
type_corpse %= method_block + semi + type_corpse, lambda h,s: [s[1]] + s[3] #154
type_corpse %= def_type, lambda h,s: [s[1]] #155
type_corpse %= def_type + type_corpse, lambda h,s: [s[1]] + s[2] #156

prop %= idx + equal + expr, lambda h,s: Property(s[1], s[3]) #157
prop %= idx + equal + expr_block, lambda h,s: Property(s[1], s[3]) #158
prop %= idx + typed + equal + expr, lambda h,s: Property(s[1], s[4], s[2]) #159
prop %= idx + typed + equal + expr_block, lambda h,s: Property(s[1], s[4], s[2]) #160

method %= idx + opar + arg_list + cpar + arrow + expr, lambda h,s: Function(s[1], s[3], s[6]) #161
method %= idx + opar + cpar + arrow + expr, lambda h,s: Function(s[1], None, s[5]) #162
method_block %= idx + opar + arg_list + cpar + expr_block, lambda h,s: Function(s[1], s[3], s[5]) #163
method_block %= idx + opar + cpar + expr_block, lambda h,s: Function(s[1], None, s[4]) #164

method %= idx + opar + arg_list + cpar + typed + arrow + expr, lambda h,s: Function(s[1], s[3], s[7], s[5]) #165
method %= idx + opar + cpar + typed + arrow + expr, lambda h,s: Function(s[1], None, s[6], s[4]) #166
method_block %= idx + opar + arg_list + cpar + typed + expr_block, lambda h,s: Function(s[1], s[3], s[6], s[5]) #167
method_block %= idx + opar + cpar + typed + expr_block, lambda h,s: Function(s[1], None, s[5], s[4]) #168

typed %= colon + idx, lambda h,s: s[2] #169
typed %= colon + strx, lambda h,s: s[2] #170
typed %= colon + numx, lambda h,s: s[2] #171
typed %= colon + objx, lambda h,s: s[2] #172
typed %= colon + boolx, lambda h,s: s[2] #173

protocol %= proto + idx + obracket + def_list + cbracket, lambda h,s: Protocol(s[2], s[4]) #174
protocol %= proto + idx + extends + idx + obracket + def_list + cbracket, lambda h,s: Protocol(s[2], s[6], s[4]) #175

def_list %= define + semi, lambda h,s: [s[1]] #176
def_list %= define_block, lambda h,s: [s[1]] #177
def_list %= define + semi + def_list, lambda h,s: [s[1]] + s[3] #178
def_list %= define_block + semi, lambda h,s: [s[1]] #179
def_list %= define_block + def_list, lambda h,s: [s[1]] + s[2] #180
def_list %= define_block + semi + def_list, lambda h,s: [s[1]] + s[2] #181

define_block %= idx + opar + cpar + obracket + cbracket, lambda h,s: Function(s[1], None, None) #182
define_block %= idx + opar + arg_list + cpar + obracket + cbracket, lambda h,s: Function(s[1], s[3], None) #183
define_block %= idx + opar + cpar + typed + obracket + cbracket, lambda h,s: Function(s[1], None, None, s[4]) #184
define_block %= idx + opar + arg_list + cpar + typed + obracket + cbracket, lambda h,s: Function(s[1], s[3], None, s[5]) #185

define %= idx + opar + cpar, lambda h,s: Function(s[1], None, None) #186
define %= idx + opar + arg_list + cpar, lambda h,s: Function(s[1], s[3], None) #187
define %= idx + opar + cpar + typed, lambda h,s: Function(s[1], None, None, s[4]) #188
define %= idx + opar + arg_list + cpar + typed, lambda h,s: Function(s[1], s[3], None, s[5]) #189


#endregion
#endregion

logger.info("Grammar created")
for i, production in  enumerate(G.Productions):
    logger.info("Production %d: %s" % (i, production))