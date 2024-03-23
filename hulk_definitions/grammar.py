from cmp.pycompiler import Grammar
import logging
logger = logging.getLogger(__name__)

logger.info("Creating Grammar")
G = Grammar()

#region Grammar Definition

#region NonTerminals Definition
program = G.NonTerminal('<program>', startSymbol=True)
stat_list, stat = G.NonTerminals('<stat_list> <stat>')
let_var, let_var_block, def_func, def_func_block, arg_list = G.NonTerminals('<let-var> <let-var-bloack> <def-func> <def-func-block> <arg-list>')
assign, var_corpse = G.NonTerminals('<assign> <var-corpse>')
if_expr, if_br = G.NonTerminals('<if-expr> <if-branches>')
built_in, e_num, block = G.NonTerminals('<built-in> <e-num> <block>')
expr, term, factor, power, atom = G.NonTerminals('<expr> <term> <factor> <power> <atom>')
func_call, expr_list = G.NonTerminals('<func-call> <expr-list>')
#endregion

#region Terminals Definition
let, func, inx, ifx, elsex, elifx, whilex, forx, typex, selfx, newx = G.Terminals('LET FUNCTION IN IF ELSE ELIF WHILE FOR TYPE SELF NEW')
inheritsx, asx, proto, extends, iterx = G.Terminals('INHERITS AS PROTOCOL EXTENDS ITERABLE')
printx, sinx, cosx, expx, sqrtx, logx, randx, rangex = G.Terminals('PRINT SIN COS EXP SQRT LOG RAND RANGE')
semi, opar, cpar, obracket, cbracket, obrace, cbrace, arrow, comma = G.Terminals('SEMICOLON OPAR CPAR OBRACKET CBRACKET OBRACE CBRACE IMPLICATION COMMA')
equal, plus, minus, star, div, pow, dstar, atx, modx, dassign = G.Terminals('EQUAL PLUS MINUS ASTERISK SLASH CIRCUMFLEX POTENCIAL AT PERCENT DESTRUCTIVE_ASSIGNMENT')
dequal, nequal, gt, lt, gte, lte, isx, andx, orx, notx = G.Terminals('COMP_EQ COMP_NEQ COMP_GT COMP_LT COMP_GTE COMP_LTE IS AND OR NOT')
idx, num, string, true, false, pi, e = G.Terminals('id num string TRUE FALSE PI E')
strx, numx, objx, boolx = G.Terminals('String Number Object Boolean')
eof = G.EOF
#endregion

#region Productions Definition
program %= stat_list, lambda h,s: None

stat_list %= stat + semi, None # Your code here!!! (add rule)
stat_list %= stat + semi + stat_list, None # Your code here!!! (add rule)
stat_list %= block, None # Your code here!!! (add rule)
stat_list %= block + stat_list, None # Your code here!!! (add rule)
stat_list %= block + semi, None # Your code here!!! (add rule)
stat_list %= block + semi + stat_list, None # Your code here!!! (add rule)
stat_list %= let_var_block, None # Your code here!!! (add rule)
stat_list %= let_var_block + stat_list, None # Your code here!!! (add rule)
stat_list %= let_var_block + semi, None # Your code here!!! (add rule)
stat_list %= let_var_block + semi + stat_list, None # Your code here!!! (add rule)
stat_list %= def_func_block, None # Your code here!!! (add rule)
stat_list %= def_func_block + stat_list, None # Your code here!!! (add rule)
stat_list %= def_func_block + semi, None # Your code here!!! (add rule)
stat_list %= def_func_block + semi + stat_list, None # Your code here!!! (add rule)

stat %= let_var, None # Your code here!!! (add rule)
stat %= def_func, None # Your code here!!! (add rule)
stat %= expr, None # Your code here!!! (add rule)
stat %= assign, None # Your code here!!! (add rule)
stat %= if_expr, None # Your code here!!! (add rule)

let_var %= let + var_corpse + inx + stat, None # Your code here!!! (add rule)
let_var %= let + var_corpse + inx + def_func_block, None # Your code here!!! (add rule)
let_var %= let + var_corpse + inx + let_var_block, None # Your code here!!! (add rule)
let_var_block %= let + var_corpse + inx + block, None # Your code here!!! (add rule)
assign %= idx + dassign + expr, None # Your code here!!! (add rule)

var_corpse %= idx + equal + stat, None # Your code here!!! (add rule)
var_corpse %= idx + equal + stat + comma + var_corpse, None # Your code here!!! (add rule)
var_corpse %= idx + equal + stat + comma + let_var, None # Your code here!!! (add rule)

def_func %= func + idx + opar + arg_list + cpar + arrow + stat, None # Your code here!!! (add rule)
def_func %= func + idx + opar + arg_list + cpar + arrow + let_var_block, None # Your code here!!! (add rule)
def_func %= func + idx + opar + arg_list + cpar + arrow + def_func_block, None # Your code here!!! (add rule)
def_func_block %= func + idx + opar + arg_list + cpar + block, None # Your code here!!! (add rule)

arg_list %= idx, None # Your code here!!! (add rule)
arg_list %= idx + comma + arg_list, None # Your code here!!! (add rule)

block %= obracket + stat_list + cbracket, None # Your code here!!! (add rule)

if_expr %= ifx + opar + expr + cpar + stat + if_br, None # Your code here!!! (add rule)
if_expr %= ifx +  opar + expr + cpar + block + if_br, None # Your code here!!! (add rule)
if_expr %= ifx + opar + expr + cpar + let_var_block + if_br, None # Your code here!!! (add rule)
if_expr %= ifx + opar + expr + cpar + def_func_block + if_br, None # Your code here!!! (add rule)

if_br %= elsex + stat, None # Your code here!!! (add rule)
if_br %= elsex + block, None # Your code here!!! (add rule)
if_br %= elsex + let_var_block, None # Your code here!!! (add rule)
if_br %= elsex + def_func_block, None # Your code here!!! (add rule)
if_br %= elifx + opar + expr + cpar + stat + if_br, None # Your code here!!! (add rule)
if_br %= elifx + opar + expr + cpar + block + if_br, None # Your code here!!! (add rule)
if_br %= elifx + opar + expr + cpar + let_var_block + if_br, None # Your code here!!! (add rule)
if_br %= elifx + opar + expr + cpar + def_func_block + if_br, None # Your code here!!! (add rule)

expr %= term, None # Your code here!!! (add rule)
expr %= expr + atx + term, None # Your code here!!! (add rule)
expr %= expr + orx + term, None # Your code here!!! (add rule)
expr %= expr + plus + term, None # Your code here!!! (add rule)
expr %= expr + minus + term, None # Your code here!!! (add rule)
expr %= opar + let_var + cpar, None # Your code here!!! (add rule)

term %= factor, None # Your code here!!! (add rule)
term %= term + star + factor, None # Your code here!!! (add rule)
term %= term + div + factor, None # Your code here!!! (add rule)
term %= term + modx + factor, None # Your code here!!! (add rule)
term %= term + andx + factor, None # Your code here!!! (add rule)

factor %= power, None # Your code here!!! (add rule)
factor %= notx + factor, None # Your code here!!! (add rule)
factor %= minus + factor, None # Your code here!!! (add rule)
factor %= power + pow + factor, None # Your code here!!! (add rule)
factor %= power + dstar + factor, None # Your code here!!! (add rule)
factor %= power + gt + factor, None # Your code here!!! (add rule)
factor %= power + lt + factor, None # Your code here!!! (add rule)
factor %= power + gte + factor, None # Your code here!!! (add rule)
factor %= power + lte + factor, None # Your code here!!! (add rule)
factor %= power + dequal + factor, None # Your code here!!! (add rule)
factor %= power + nequal + factor, None # Your code here!!! (add rule)
factor %= power + isx + factor, None # Your code here!!! (add rule)

power %= atom, None # Your code here!!! (add rule) 
power %= opar + expr + cpar, None # Your code here!!! (add rule)

atom %= num, None # Your code here!!! (add rule)
atom %= idx, None # Your code here!!! (add rule)
atom %= true, None # Your code here!!! (add rule)
atom %= false, None # Your code here!!! (add rule)
atom %= string, None # Your code here!!! (add rule)
atom %= func_call, None # Your code here!!! (add rule)
atom %= e_num, None # Your code here!!! (add rule)
atom %= built_in, None # Your code here!!! (add rule)

built_in %= sinx + opar + expr_list + cpar, None # Your code here!!! (add rule)
built_in %= cosx + opar + expr_list + cpar, None # Your code here!!! (add rule)
built_in %= randx + opar + expr_list + cpar, None # Your code here!!! (add rule)
built_in %= expx + opar + expr_list + cpar, None # Your code here!!! (add rule)
built_in %= logx + opar + expr_list + cpar, None # Your code here!!! (add rule)
built_in %= sqrtx + opar + expr_list + cpar, None # Your code here!!! (add rule)
built_in %= printx + opar + expr_list + cpar, None # Your code here!!! (add rule)

e_num %= pi, None # Your code here!!! (add rule)
e_num %= e, None # Your code here!!! (add rule)

func_call %= idx + opar + expr_list + cpar, None # Your code here!!! (add rule)

expr_list %= stat, None # Your code here!!! (add rule)
expr_list %= stat + comma + expr_list, None # Your code here!!! (add rule)

#endregion
#endregion

logger.info("Grammar created")
for i, production in  enumerate(G.Productions):
    logger.info("Production %d: %s" % (i, production))