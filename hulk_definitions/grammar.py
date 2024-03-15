from cmp.pycompiler import Grammar

G = Grammar()

program = G.NonTerminal('<program>', startSymbol=True)
stat_list, stat, expr, expr_list, code_list = G.NonTerminals('<stat_list> <stat> <expr> <expr-list> <code-list>')
let_var, def_func, print_stat, arg_list, protocol = G.NonTerminals('<let-var> <def-func> <print-stat> <arg-list> <protocol>')
simple_expr, block_expr, block_corpse = G.NonTerminals('<simple-expr> <block-expr> <block-corpse>')
call_expr, str_expr, arthmetic_expr, dest_expr = G.NonTerminals('<call-expr> <str-expr> <arithmetic-expr> <dest-expr>') 
conditional_expr, loop_expr, param = G.NonTerminals('<conditional-expr> <loop-expr> <param>')
method_list, method = G.NonTerminals('<metod-list> <method>')
var_corpse, branches, branch, while_loop, for_loop = G.NonTerminals('<var-corpse> <branches> <branch> <while-loop> <for-loop>')
type_anoted, type_set, protocol_set, protocol_sand = G.NonTerminals('<type-anoted> <type-set> <protocol-set> <protocol-sand>')
def_type, new_expr, func_call, param_list = G.NonTerminals('<def-type> <new-expr> <func-call> <param-list>')
arit_expr, term, factor, atom = G.NonTerminals('<arit-expr> <term> <factor> <atom>')
bool_expr, and_expr, batom = G.NonTerminals('<bool-expr> <and-expr> <batom>')



let, inx, defx, printx = G.Terminals('let in def print')
typex, create, inherits, protocolx = G.Terminals('type new inherits protocol')
wloop, floop = G.Terminals('while for') 
semi, comma, opar, cpar, okey, ckey, obracket, cbracket, arrow, dot, ddot = G.Terminals('; , ( ) { } [ ] -> . :')
ifx, elsex, elifx = G.Terminals('if else elif')
equal, plus, minus, star, pow, stard, div = G.Terminals('== + - * ^ ** /')
quote = G.Terminal("'")
dquote, strx = G.Terminals('" str')
asignment, dest = G.Terminals('= :=')
land, lor, lnot = G.Terminals('& | !')
isx, asx = G.Terminals('is as')
idx, num = G.Terminals('id int')
boolx = G.Terminal('bool')
nline = G.Terminal(r'\n')

program %= code_list, None #TODO

code_list %= code_list + expr_list, lambda h,s: s[1] + s[2]
code_list %= code_list + stat_list, lambda h,s: s[1] + s[2]

type_anoted %= idx, None #TODO
type_anoted %= idx + ddot + idx, None #TODO

stat_list %= stat, lambda h,s: [s[1]]
stat_list %= stat + stat_list, lambda h,s: s[1] + s[2]

expr_list %= expr, lambda h,s: [s[1]]
expr_list %= expr + expr_list, lambda h,s: s[1] + s[2]

stat %= def_func, lambda h,s: s[1]
stat %= print_stat, lambda h,s: s[1]
stat %= protocol, lambda h,s: s[1]

expr %= simple_expr, lambda h,s: s[1]
expr %= block_expr, lambda h,s: s[1]

simple_expr %= call_expr, None #TODO
simple_expr %= str_expr, None #TODO
simple_expr %= arit_expr, None #TODO
simple_expr %= dest_expr, None #TODO
simple_expr %= bool_expr, None #TODO
simple_expr %= let_var, None #TODO
simple_expr %= loop_expr, None #TODO
simple_expr %= conditional_expr, None #TODO

block_expr %= simple_expr, None #TODO
block_expr %= okey + simple_expr + semi + block_expr + ckey, None #TODO

let_var %= let + var_corpse + inx + expr, None #TODO

var_corpse %= type_anoted + equal + expr, None #TODO
var_corpse %= type_anoted + equal + expr + comma + var_corpse, None #TODO

call_expr %= idx, None #TODO
call_expr %= func_call, None #TODO
call_expr %= create + func_call, None #TODO
call_expr %= call_expr + dot + idx, None #TODO
call_expr %= call_expr + asx + type_set, None #TODO
call_expr %= call_expr + dot + func_call, None #TODO
call_expr %= call_expr + obracket + call_expr + cbracket, None #TODO

type_set %= idx, None #TODO
type_set %= idx + lor + type_set, None #TODO

protocol_set %= protocol_sand, None #TODO
protocol_set %= protocol_set + lor + protocol_sand, None #TODO

protocol_sand %= idx, None #TODO
protocol_sand %= protocol_sand + land + idx, None #TODO

str_expr %= quote + strx + quote, None #TODO
str_expr %= dquote + strx + dquote, None #TODO

dest_expr %= call_expr + dest + expr, None #TODO

conditional_expr %= ifx + opar + expr + cpar + expr + elifx + expr, None # TODO
conditional_expr %= ifx + opar + expr + cpar + expr + branches + elsex + expr, None #TODO

branches %= branch, None #TODO
branches %= branches + branch, None #TODO

branch %= elifx + opar + expr + cpar + expr, None #TODO

bool_expr %= and_expr + lor + bool_expr, None #TODO
bool_expr %= and_expr, None #TODO

and_expr %= batom, None #TODO
and_expr %= and_expr + land + batom, None #TODO

batom %= boolx, None #TODO
batom %= call_expr, None #TODO
batom %= lnot + batom, None #TODO
batom %= call_expr + isx + idx, None #TODO
batom %= opar + bool_expr + cpar, None #TODO

def_func %= defx + idx + opar + arg_list + cpar + arrow + expr, None # TODO

print_stat %= printx + expr, None # TODO

arg_list %= type_anoted, None # TODO
arg_list %= type_anoted + comma + arg_list, None # TODO

arit_expr %= arit_expr + plus + term, None # TODO
arit_expr %= arit_expr + minus + term, None # TODO
arit_expr %= term, None # TODO

term %= term + star + factor, None # TODO
term %= term + div + factor, None # TODO
term %= factor, None # TODO

factor %= atom, None # TODO
factor %= opar + expr + cpar, None # TODO
factor %= factor + pow + factor, None # TODO
factor %= factor + stard + factor, None # TODO

atom %= num, None # TODO
atom %= call_expr, None # TODO

func_call %= call_expr + opar + cpar, None #TODO
func_call %= call_expr + opar + param_list + cpar, None # TODO

param_list %= param, None #TODO
param_list %= param + comma + param_list, None #TODO

expr_list %= expr, None # TODO
expr_list %= expr + comma + expr_list, None # TODO

protocol %= protocolx + idx + okey + method_list + ckey, None #TODO

method_list %= method + semi, None #TODO
method_list %= method + semi + method_list, None #TODO