import interpreter_helper as ch, strhelper as sh

# replace the var with the new generated var
def a_conversion(expr:sh.Expression,var:str, new_var:str):
    if expr.var == var:
        expr.var = new_var
    if not expr.is_var:
        a_conversion(expr.expr1,var,new_var)
        if expr.expr2 is not None:
            a_conversion(expr.expr2,var,new_var)

# do a-conversion if necessary return if (part of) a-conversion was implied
def a_conversion(expr:sh.Expression) -> bool:
    bound = ch.collect_bound_vars(expr.expr1)
    free = ch.collect_free_vars(expr.expr2)
    var = ""
    for el in bound:
        if el in free:
            var = el # intersection found a-conversion necessary
            break
    if var != "": # if necessary
        new_var = ch.generate_new_var(bound,free)
        a_conversion(expr,var,new_var)
        return True # has changed
    return False

def find_and_substitute(expr:sh.Expression, to_substitute:sh.Expression, var:str):
    if expr.expr1.is_var and expr.expr1.var == var:
        expr.expr1 = to_substitute


def b_reduction(expr:sh.Expression) -> bool:
    if expr.is_var:
        return False
    if expr.has_lambda and expr.expr2 is not None:
        changed = a_conversion(expr)
        has_changed = changed
        while changed: changed = a_conversion(expr) # if a-conversion was implied check if another one is possible
        return True
    if b_reduction(expr.expr1):
        return True
    if expr.expr2 is not None:
        if b_reduction(expr.expr2):
            return True
    return False
