import interpreter_helper as ih, strhelper as sh

# replace the var with the new generated var
def a_conversion(expr:sh.Expression,var:str, new_var:str):
    if expr.var == var:
        expr.var = new_var
        if expr.is_var:
            expr.content = new_var
        elif expr.is_lambda:
            expr.content = "\\" + new_var + expr.content[2:] # only replace first occurence
    if not expr.is_var:
        a_conversion(expr.expr1,var,new_var)
        if expr.expr2 is not None:
            a_conversion(expr.expr2,var,new_var)

# do a-conversion if necessary return if (part of) a-conversion was implied
def a_conversion(expr:sh.Expression) -> bool:
    bound = ih.collect_bound_vars(expr.expr1)
    free = ih.collect_free_vars(expr.expr2)
    free1 = ih.collect_free_vars(expr.expr1)
    var = ""
    for el in bound:
        if el in free:
            var = el # intersection found a-conversion necessary
            break
    if var != "": # if necessary
        new_var = ih.generate_new_var(bound,free,free1)
        a_conversion(expr,var,new_var)
        return True # has changed
    return False

# finds the instances of the var that should be substituted and does it
def find_and_substitute(expr:sh.Expression, to_substitute:sh.Expression, var:str):
    if expr.expr1.is_var:
        if expr.expr1.var == var:
            expr.expr1 = ih.deep_tree_copy(to_substitute,expr)
            expr.content = expr.content.replace(var,to_substitute.content)
    else:
        find_and_substitute(expr.expr1,to_substitute,var)
        if expr.expr2 is not None:
            find_and_substitute(expr.expr2,to_substitute,var)


def b_reduction(expr:sh.Expression, debug:bool = False) -> sh.Expression:
    if expr.is_var:
        return expr
    if expr.has_lambda and expr.expr2 is not None:
        old_content = expr.content
        changed = a_conversion(expr)

        while changed:
            if debug:
                print(f"[a-conversion] {old_content} -> {expr.content}")
                old_content = expr.content
            changed = a_conversion(expr) # if a-conversion was implied check if another one is possible

        find_and_substitute(expr.expr1,expr.expr2,expr.expr1.var)

        expr = expr.expr1.expr1 # set current pointer to substituted expression from the underneath lambda
        return expr
    if b_reduction(expr.expr1):
        return expr
    if expr.expr2 is not None:
        if b_reduction(expr.expr2):
            return expr
    return None
