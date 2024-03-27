from tools.pycompiler import Grammar
import logging
logger = logging.getLogger(__name__)
from hulk_definitions.ast import *

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
equal, plus, minus, star, div, pow, dstar, atx, datx, modx, dassign, colon, dpipe = G.Terminals('EQUAL PLUS MINUS ASTERISK SLASH CIRCUMFLEX POTENCIAL AT DOUBLE_AT PERCENT DESTRUCTIVE_ASSIGNMENT COLON DOUBLE_PIPE')
dequal, nequal, gt, lt, gte, lte, isx, andx, orx, notx = G.Terminals('COMP_EQ COMP_NEQ COMP_GT COMP_LT COMP_GTE COMP_LTE IS AND OR NOT')
idx, num, string, true, false, pi, e = G.Terminals('id num string TRUE FALSE PI E')
strx, numx, objx, boolx = G.Terminals('STRING NUMBER OBJECT BOOLEAN')
eof = G.EOF
#endregion

#region Productions Definition
program %= stat_list, lambda h,s: Program(s[1])

stat_list %= stat + semi, lambda h,s: [s[1]] 
stat_list %= stat + semi + stat_list, lambda h,s: [s[1]] + s[3]
stat_list %= block, lambda h,s: [s[1]]
stat_list %= block + stat_list, lambda h,s: [s[1]] + s[2]
stat_list %= block + semi, lambda h,s: [s[1]]
stat_list %= block + semi + stat_list, lambda h,s: [s[1]] + s[2]
stat_list %= let_var_block, lambda h,s: [s[1]]
stat_list %= let_var_block + stat_list, lambda h,s: [s[1]] + s[2]
stat_list %= let_var_block + semi, lambda h,s: [s[1]]
stat_list %= let_var_block + semi + stat_list, lambda h,s: [s[1]] + s[2]
stat_list %= def_func_block, lambda h,s: [s[1]]
stat_list %= def_func_block + stat_list, lambda h,s: [s[1]] + s[2]
stat_list %= def_func_block + semi, lambda h,s: [s[1]]
stat_list %= def_func_block + semi + stat_list, lambda h,s: [s[1]] + s[2]

stat %= let_var, lambda h,s: s[1]
stat %= def_func, lambda h,s: s[1]
stat %= expr, lambda h,s: s[1]
stat %= assign, lambda h,s: s[1]
stat %= if_expr, lambda h,s: s[1]

let_var %= let + var_corpse + inx + stat, lambda h,s: LetList([Let(x[0], x[1], s[4], x[2]) for x in s[2]])
let_var_block %= let + var_corpse + inx + def_func_block, lambda h,s: LetList([Let(x[0], x[1], s[4], x[2]) for x in s[2]])
let_var_block %= let + var_corpse + inx + if_expr_block, lambda h,s: LetList([Let(x[0], x[1], s[4], x[2]) for x in s[2]])
let_var_block %= let + var_corpse + inx + let_var_block, lambda h,s: LetList([Let(x[0], x[1], s[4], x[2]) for x in s[2]])
let_var_block %= let + var_corpse + inx + block, lambda h,s: LetList([Let(x[0], x[1], s[4], x[2]) for x in s[2]])
assign %= atom + dassign + expr, lambda h,s: Assign(s[1], s[3])

var_corpse %= idx + equal + stat, lambda h,s: [[s[1], s[3], None]] 
var_corpse %= idx + equal + stat + comma + var_corpse, lambda h,s: [[s[1], s[3], None]] + s[5]
var_corpse %= idx + equal + stat + comma + let + var_corpse, lambda h,s: [[s[1], s[3], None]] + s[6]

var_corpse %= idx + typed + equal + stat, lambda h,s: [[s[1], s[4], s[2]]]
var_corpse %= idx + typed + equal + stat + comma + var_corpse, lambda h,s: [[s[1], s[4], s[2]]] + s[6]
var_corpse %= idx + typed + equal + stat + comma + let + var_corpse, lambda h,s: [[s[1], s[4], s[2]]] + s[7]

def_func %= func + idx + opar + arg_list + cpar + arrow + stat, lambda h,s: Function(s[2], s[4], s[7])
def_func_block %= func + idx + opar + arg_list + cpar + arrow + let_var_block, lambda h,s: Function(s[2], s[4], s[7])
def_func_block %= func + idx + opar + arg_list + cpar + arrow + def_func_block, lambda h,s: Function(s[2], s[4], s[7])
def_func_block %= func + idx + opar + arg_list + cpar + arrow + def_func_block, lambda h,s: Function(s[2], s[4], s[7])
def_func_block %= func + idx + opar + arg_list + cpar + block, lambda h,s: Function(s[2], s[4], s[6])

def_func %= func + idx + opar + arg_list + cpar + typed + arrow + stat, lambda h,s: Function(s[2], s[4], s[8], s[6])
def_func_block %= func + idx + opar + arg_list + cpar + typed + arrow + let_var_block, lambda h,s: Function(s[2], s[4], s[8], s[6])
def_func_block %= func + idx + opar + arg_list + cpar + typed + arrow + if_expr_block, lambda h,s: Function(s[2], s[4], s[8], s[6])
def_func_block %= func + idx + opar + arg_list + cpar + typed + arrow + def_func_block, lambda h,s: Function(s[2], s[4], s[8], s[6])
def_func_block %= func + idx + opar + arg_list + cpar + typed + block, lambda h,s: Function(s[2], s[4], s[7], s[6])

arg_list %= idx, lambda h,s: [(s[1], None)]
arg_list %= idx + typed, lambda h,s: [(s[1], s[2])]
arg_list %= idx + comma + arg_list, lambda h,s: [(s[1], None)] + s[3]
arg_list %= idx + typed + comma + arg_list, lambda h,s: [(s[1], s[2])] + s[4]

block %= obracket + stat_list + cbracket, lambda h,s: Block(s[2])
block %= obracket + cbracket, lambda h,s: Block(None)

if_expr %= ifx + opar + expr + cpar + stat + elsex + stat, lambda h,s: Conditional(s[3], s[5], s[7])
if_expr %= ifx + opar + expr + cpar + block + elsex + stat, lambda h,s: Conditional(s[3], s[5], s[7])
if_expr %= ifx + opar + expr + cpar + let_var_block + elsex + stat, lambda h,s: Conditional(s[3], s[5], s[7])
if_expr %= ifx + opar + expr + cpar + def_func_block + elsex + stat, lambda h,s: Conditional(s[3], s[5], s[7])

if_expr %= ifx + opar + expr + cpar + stat + if_br + elsex + stat, lambda h,s: Conditional(s[3], s[5], s[8], s[6])
if_expr %= ifx + opar + expr + cpar + block + if_br + elsex + stat, lambda h,s: Conditional(s[3], s[5], s[8], s[6])
if_expr %= ifx + opar + expr + cpar + let_var_block + if_br + elsex + stat, lambda h,s: Conditional(s[3], s[5], s[8], s[6])
if_expr %= ifx + opar + expr + cpar + def_func_block + if_br + elsex + stat, lambda h,s: Conditional(s[3], s[5], s[8], s[6])

if_expr_block %= ifx + opar + expr + cpar + stat + elsex + def_func_block, lambda h,s: Conditional(s[3], s[5], s[7])
if_expr_block %= ifx + opar + expr + cpar + block + elsex + def_func_block, lambda h,s: Conditional(s[3], s[5], s[7])
if_expr_block %= ifx + opar + expr + cpar + let_var_block + elsex + def_func_block, lambda h,s: Conditional(s[3], s[5], s[7])
if_expr_block %= ifx + opar + expr + cpar + def_func_block + elsex + def_func_block, lambda h,s: Conditional(s[3], s[5], s[7])

if_expr_block %= ifx + opar + expr + cpar + stat + elsex + let_var_block, lambda h,s: Conditional(s[3], s[5], s[7])
if_expr_block %= ifx + opar + expr + cpar + block + elsex + let_var_block, lambda h,s: Conditional(s[3], s[5], s[7])
if_expr_block %= ifx + opar + expr + cpar + let_var_block + elsex + let_var_block, lambda h,s: Conditional(s[3], s[5], s[7])
if_expr_block %= ifx + opar + expr + cpar + def_func_block + elsex + let_var_block, lambda h,s: Conditional(s[3], s[5], s[7])

if_expr_block %= ifx + opar + expr + cpar + stat + elsex + block, lambda h,s: Conditional(s[3], s[5], s[7])
if_expr_block %= ifx + opar + expr + cpar + block + elsex + block, lambda h,s: Conditional(s[3], s[5], s[7])
if_expr_block %= ifx + opar + expr + cpar + let_var_block + elsex + block, lambda h,s: Conditional(s[3], s[5], s[7])
if_expr_block %= ifx + opar + expr + cpar + def_func_block + elsex + block, lambda h,s: Conditional(s[3], s[5], s[7])

if_expr_block %= ifx + opar + expr + cpar + stat + if_br + elsex + def_func_block, lambda h,s: Conditional(s[3], s[5], s[8], s[6])
if_expr_block %= ifx + opar + expr + cpar + block + if_br + elsex + def_func_block, lambda h,s: Conditional(s[3], s[5], s[8], s[6])
if_expr_block %= ifx + opar + expr + cpar + let_var_block + if_br + elsex + def_func_block, lambda h,s: Conditional(s[3], s[5], s[8], s[6])
if_expr_block %= ifx + opar + expr + cpar + def_func_block + if_br + elsex + def_func_block, lambda h,s: Conditional(s[3], s[5], s[8], s[6])

if_expr_block %= ifx + opar + expr + cpar + stat + if_br + elsex + let_var_block, lambda h,s: Conditional(s[3], s[5], s[8], s[6])
if_expr_block %= ifx + opar + expr + cpar + block + if_br + elsex + let_var_block, lambda h,s: Conditional(s[3], s[5], s[8], s[6])
if_expr_block %= ifx + opar + expr + cpar + let_var_block + if_br + elsex + let_var_block, lambda h,s: Conditional(s[3], s[5], s[8], s[6])
if_expr_block %= ifx + opar + expr + cpar + def_func_block + if_br + elsex + let_var_block, lambda h,s: Conditional(s[3], s[5], s[8], s[6])

if_expr_block %= ifx + opar + expr + cpar + stat + if_br + elsex + block, lambda h,s: Conditional(s[3], s[5], s[8], s[6])
if_expr_block %= ifx + opar + expr + cpar + block + if_br + elsex + block, lambda h,s: Conditional(s[3], s[5], s[8], s[6])
if_expr_block %= ifx + opar + expr + cpar + let_var_block + if_br + elsex + block, lambda h,s: Conditional(s[3], s[5], s[8], s[6])
if_expr_block %= ifx + opar + expr + cpar + def_func_block + if_br + elsex + block, lambda h,s: Conditional(s[3], s[5], s[8], s[6])

if_br %= elifx + opar + expr + cpar + stat, lambda h,s: [Branch(s[3], s[5])]
if_br %= elifx + opar + expr + cpar + block, lambda h,s: [Branch(s[3], s[5])]
if_br %= elifx + opar + expr + cpar + let_var_block, lambda h,s: [Branch(s[3], s[5])]
if_br %= elifx + opar + expr + cpar + def_func_block, lambda h,s: [Branch(s[3], s[5])]
if_br %= elifx + opar + expr + cpar + stat + if_br, lambda h,s: [Branch(s[3], s[5])] + s[6]
if_br %= elifx + opar + expr + cpar + block + if_br, lambda h,s: [Branch(s[3], s[5])] + s[6]
if_br %= elifx + opar + expr + cpar + let_var_block + if_br, lambda h,s: [Branch(s[3], s[5])] + s[6]
if_br %= elifx + opar + expr + cpar + def_func_block + if_br, lambda h,s: [Branch(s[3], s[5])] + s[6]

expr %= term, lambda h,s: s[1]
expr %= expr + atx + term, lambda h,s: At(s[1], s[3])
expr %= expr + datx + term, lambda h,s: DoubleAt(s[1], s[3])
expr %= expr + orx + term, lambda h,s: Or(s[1], s[3])
expr %= expr + plus + term, lambda h,s: Plus(s[1], s[3])
expr %= expr + minus + term, lambda h,s: BinaryMinus(s[1], s[3])

term %= factor, lambda h,s: s[1]
term %= term + star + factor, lambda h,s: Star(s[1], s[3])
term %= term + div + factor, lambda h,s: Div(s[1], s[3])
term %= term + modx + factor, lambda h,s: Mod(s[1], s[3])
term %= term + andx + factor, lambda h,s: And(s[1], s[3])

factor %= power, lambda h,s: s[1]
factor %= notx + factor, lambda h,s: Not(s[2])
factor %= minus + factor, lambda h,s: UnaryMinus(s[2])
factor %= power + gt + factor, lambda h,s: GreaterThan(s[1], s[3])
factor %= power + lt + factor, lambda h,s: LessThan(s[1], s[3])
factor %= power + gte + factor, lambda h,s: GreaterEqual(s[1], s[3])
factor %= power + lte + factor, lambda h,s: LessEqual(s[1], s[3])
factor %= power + dequal + factor, lambda h,s: CompareEqual(s[1], s[3])
factor %= power + nequal + factor, lambda h,s: NotEqual(s[1], s[3])
factor %= power + isx + factor, lambda h,s: Is(s[1], s[3])

power %= atom, lambda h,s: s[1]
power %= atom + pow + power, lambda h,s: Pow(s[1], s[3])
power %= atom + dstar + power, lambda h,s: Pow(s[1], s[3])

atom %= opar + let_var + cpar, lambda h,s: s[2]
atom %= opar + expr + cpar, lambda h,s: s[2]
atom %= num, lambda h,s: Number(float(s[1]))
atom %= idx, lambda h,s: Var(s[1])
atom %= true, lambda h,s: Bool(True)
atom %= false, lambda h,s: Bool(False)
atom %= string, lambda h,s: Str(s[1])
atom %= func_call, lambda h,s: s[1]
atom %= e_num, lambda h,s: s[1]
atom %= built_in, lambda h,s: s[1]
atom %= atom + asx + idx, lambda h,s: As(s[1], s[3])
atom %= atom + asx + strx, lambda h,s: As(s[1], s[3])
atom %= atom + asx + numx, lambda h,s: As(s[1], s[3])
atom %= atom + asx + objx, lambda h,s: As(s[1], s[3])
atom %= atom + asx + boolx, lambda h,s: As(s[1], s[3])
atom %= obrace + expr_list + cbrace, lambda h,s: Vector(s[2], len(s[2]))
atom %= obrace + expr + dpipe + idx + inx + expr + cbrace, lambda h,s: VectorComprehension(s[6], len(s[6]), (s[4], s[2]))

built_in %= sinx + opar + expr_list + cpar, lambda h,s: Sin(s[3])
built_in %= cosx + opar + expr_list + cpar, lambda h,s: Cos(s[3])
built_in %= randx + opar + expr_list + cpar, lambda h,s: Rand(s[3])
built_in %= randx + opar + cpar, lambda h,s: Rand(None)
built_in %= expx + opar + expr_list + cpar, lambda h,s: Exp(s[3])
built_in %= logx + opar + expr_list + cpar, lambda h,s: Log(s[3])
built_in %= sqrtx + opar + expr_list + cpar, lambda h,s: Sqrt(s[3])
built_in %= printx + opar + expr_list + cpar, lambda h,s: Print(s[3])
built_in %= rangex + opar + expr_list + cpar, lambda h,s: Range(s[3])

e_num %= pi, lambda h,s: Pi()
e_num %= e, lambda h,s: E()

func_call %= idx + opar + expr_list + cpar, lambda h,s: Call(s[1], s[3])

expr_list %= stat, lambda h,s: [s[1]]
expr_list %= stat + comma + expr_list, lambda h,s: [s[1]] + s[3]

loop_expr %= while_expr, lambda h,s: s[1]
loop_expr %= for_expr, lambda h,s: s[1]

while_expr %= whilex + opar + expr + cpar + stat, lambda h,s: While(s[3], s[5])
while_expr_block %= whilex + opar + expr + cpar + block, lambda h,s: While(s[3], s[5])
while_expr_block %= whilex + opar + expr + cpar + if_expr_block, lambda h,s: While(s[3], s[5])
while_expr_block %= whilex + opar + expr + cpar + let_var_block, lambda h,s: While(s[3], s[5])
while_expr_block %= whilex + opar + expr + cpar + def_func_block, lambda h,s: While(s[3], s[5])

for_expr %= forx + opar + idx + inx + expr + cpar + stat, lambda h,s: For(s[3], s[5], s[7])
for_expr_block %= forx + opar + idx + inx + expr + cpar + block, lambda h,s: For(s[3], s[5], s[7])
for_expr_block %= forx + opar + idx + inx + expr + cpar + if_expr_block, lambda h,s: For(s[3], s[5], s[7])
for_expr_block %= forx + opar + idx + inx + expr + cpar + let_var_block, lambda h,s: For(s[3], s[5], s[7])
for_expr_block %= forx + opar + idx + inx + expr + cpar + def_func_block, lambda h,s: For(s[3], s[5], s[7])

stat %= loop_expr, lambda h,s: s[1]

atom %= atom + dot + idx, lambda h,s: Invoke(s[1], s[3])
atom %= atom + dot + func_call, lambda h,s: Invoke(s[1], s[3])
atom %= atom + obrace + atom + cbrace, lambda h,s: Indexing(s[1], s[3])

func_call %= idx + opar + cpar, lambda h,s: Call(s[1], None)

let_var_block %= let + var_corpse + inx + while_expr_block, lambda h,s: LetList([Let(x[0], x[1], s[4], x[2]) for x in s[2]])
let_var_block %= let + var_corpse + inx + for_expr_block, lambda h,s: LetList([Let(x[0], x[1], s[4], x[2]) for x in s[2]])

def_func_block %= func + idx + opar + arg_list + cpar + while_expr_block, lambda h,s: Function(s[2], s[4], s[7])
def_func_block %= func + idx + opar + arg_list + cpar + for_expr_block, lambda h,s: Function(s[2], s[4], s[7])

def_func_block %= func + idx + opar + arg_list + cpar + typed + while_expr_block, lambda h,s: Function(s[2], s[4], s[7], s[6])
def_func_block %= func + idx + opar + arg_list + cpar + typed + for_expr_block, lambda h,s: Function(s[2], s[4], s[7], s[6])

def_func %= func + idx + opar + arg_list + cpar + arrow + while_expr_block, lambda h,s: Function(s[2], s[4], s[7])#TODO: type is giving errors
def_func %= func + idx + opar + arg_list + cpar + arrow + for_expr_block, lambda h,s: Function(s[2], s[4], s[8], s[6])

def_func %= func + idx + opar + arg_list + cpar + typed + arrow + while_expr_block, lambda h,s: Function(s[2], s[4], s[8], s[6])
def_func %= func + idx + opar + arg_list + cpar + typed + arrow + for_expr_block, lambda h,s: Function(s[2], s[4], s[8], s[6])

def_type %= typex + idx + obracket + cbracket, lambda h,s: TypeDef(s[2], None, None)
def_type %= typex + idx + inheritsx + idx + obracket + cbracket, lambda h,s: TypeDef(s[2], None, None, s[4])
def_type %= typex + idx + inheritsx + idx + opar + expr_list + cpar + obracket + cbracket, lambda h,s: TypeDef(s[2], None, None, s[4], s[6])

def_type %= typex + idx + opar + arg_list + cpar + obracket + cbracket, lambda h,s: TypeDef(s[2], None, s[4])
def_type %= typex + idx + opar + arg_list + cpar + inheritsx + idx + obracket + cbracket, lambda h,s: TypeDef(s[2], None, s[4], s[7])
def_type %= typex + idx + opar + arg_list + cpar + inheritsx + idx + opar + expr_list + cpar + obracket + cbracket, lambda h,s: TypeDef(s[2], None, s[4], s[7], s[9])

def_type %= typex + idx + obracket + type_corpse + cbracket, lambda h,s: TypeDef(s[2], s[4], None)
def_type %= typex + idx + inheritsx + idx + obracket + type_corpse + cbracket, lambda h,s: TypeDef(s[2], s[6], None, s[4])
def_type %= typex + idx + inheritsx + idx + opar + expr_list + cpar + obracket + type_corpse + cbracket, lambda h,s: TypeDef(s[2], s[9], None, s[4], s[6])

def_type %= typex + idx + opar + arg_list + cpar + obracket + type_corpse + cbracket, lambda h,s: TypeDef(s[2], s[7], s[4])
def_type %= typex + idx + opar + arg_list + cpar + inheritsx + idx + obracket + type_corpse + cbracket, lambda h,s: TypeDef(s[2], s[9], s[4], s[7])
def_type %= typex + idx + opar + arg_list + cpar + inheritsx + idx + opar + expr_list + cpar + obracket + type_corpse + cbracket, lambda h,s: TypeDef(s[2], s[12], s[4], s[7], s[9])

type_corpse %= method + semi + type_corpse, lambda h,s: [s[1]] + s[3]
type_corpse %= prop + semi + type_corpse, lambda h,s: [s[1]] + s[3]
type_corpse %= method + semi, lambda h,s: [s[1]]
type_corpse %= method_block, lambda h,s: [s[1]]
type_corpse %= method_block + semi, lambda h,s: [s[1]]
type_corpse %= method_block + type_corpse, lambda h,s: [s[1]] + s[2]
type_corpse %= method_block + semi + type_corpse, lambda h,s: [s[1]] + s[3]
type_corpse %= prop + semi, lambda h,s: [s[1]]

atom %= selfx, lambda h,s: Self(s[1])

prop %= idx + equal + expr, lambda h,s: Property(s[1], s[3])
prop %= idx + typed + equal + expr, lambda h,s: Property(s[1], s[4], s[2])

method %= idx + opar + arg_list + cpar + arrow + stat, lambda h,s: Function(s[1], s[3], s[6])
method %= idx + opar + cpar + arrow + stat, lambda h,s: Function(s[1], None, s[5])
method_block %= idx + opar + arg_list + cpar + block, lambda h,s: Function(s[1], s[3], s[5])
method_block %= idx + opar + cpar + block, lambda h,s: Function(s[1], None, s[4])

method %= idx + opar + arg_list + cpar + typed + arrow + stat, lambda h,s: Function(s[1], s[3], s[7], s[5])
method %= idx + opar + cpar + typed + arrow + stat, lambda h,s: Function(s[1], None, s[6], s[4])
method_block %= idx + opar + arg_list + cpar + typed + block, lambda h,s: Function(s[1], s[3], s[6], s[5])
method_block %= idx + opar + cpar + typed + block, lambda h,s: Function(s[1], None, s[5], s[4])

stat_list %= def_type, lambda h,s: [s[1]]
stat_list %= def_type + stat_list, lambda h,s: [s[1]] + s[2]

expr %= newx + func_call, lambda h,s: CreateInstance(s[2].idx, s[2].args)

typed %= colon + idx, lambda h,s: s[2]
typed %= colon + strx, lambda h,s: s[2]
typed %= colon + numx, lambda h,s: s[2]
typed %= colon + objx, lambda h,s: s[2]
typed %= colon + boolx, lambda h,s: s[2]

protocol %= proto + idx + obracket + def_list + cbracket, lambda h,s: Protocol(s[2], s[4])
protocol %= proto + idx + extends + idx + obracket + def_list + cbracket, lambda h,s: Protocol(s[2], s[6], s[4])

def_list %= define + semi, lambda h,s: [s[1]]
def_list %= define_block, lambda h,s: [s[1]]
def_list %= define + semi + def_list, lambda h,s: [s[1]] + s[3]
def_list %= define_block + def_list, lambda h,s: [s[1]] + s[2]

define_block %= idx + opar + cpar + obracket + cbracket, lambda h,s: Function(s[1], None, None)
define_block %= idx + opar + arg_list + cpar + obracket + cbracket, lambda h,s: Function(s[1], s[3], None)
define_block %= idx + opar + cpar + typed + obracket + cbracket, lambda h,s: Function(s[1], None, None, s[4])
define_block %= idx + opar + arg_list + cpar + typed + obracket + cbracket, lambda h,s: Function(s[1], s[3], None, s[5])

define %= idx + opar + cpar, lambda h,s: Function(s[1], None, None)
define %= idx + opar + arg_list + cpar, lambda h,s: Function(s[1], s[3], None)
define %= idx + opar + cpar + typed, lambda h,s: Function(s[1], None, None, s[4])
define %= idx + opar + arg_list + cpar + typed, lambda h,s: Function(s[1], s[3], None, s[5])

stat_list %= protocol, lambda h,s: [s[1]]
stat_list %= protocol + stat_list, lambda h,s: [s[1]] + s[2]

#endregion
#endregion

logger.info("Grammar created")
for i, production in  enumerate(G.Productions):
    logger.info("Production %d: %s" % (i, production))