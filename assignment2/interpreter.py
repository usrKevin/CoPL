import interpreter_helper as ih, strhelper as sh

# replace the var with the new generated var
def a_conversion_rec(expr:sh.Expression,var:str, new_var:str):
    if expr.var == var:
        expr.var = new_var
        if expr.is_var:
            expr.content = new_var
        elif expr.is_lambda:
            expr.content = "\\" + new_var + expr.content[2:] # only replace first occurence
    if not expr.is_var:
        a_conversion_rec(expr.expr1,var,new_var)
        if expr.expr2 is not None:
            a_conversion_rec(expr.expr2,var,new_var)

# do a-conversion if necessary return if (part of) a-conversion was implied
# starter function for
def a_conversion(to_convert:sh.Expression, expr2:sh.Expression) -> bool:
    bound = ih.collect_bound_vars(to_convert)
    free = ih.collect_free_vars(expr2)
    free1 = ih.collect_free_vars(to_convert)
    var = ""
    for el in bound:
        if el in free:
            var = el # intersection found a-conversion necessary
            break
    if var != "": # if necessary
        new_var = ih.generate_new_var(bound,free,free1)
        a_conversion_rec(to_convert,var,new_var)
        return True # has changed
    return False

# finds the instances of the var that should be substituted and does it
def find_and_substitute(expr:sh.Expression, to_substitute:sh.Expression, var:str) -> sh.Expression:
    if expr.is_var:
        if expr.var == var:
            return ih.tree_copy(to_substitute,expr.top)
        else:
            return expr
    else:
        new_expr = ih.tree_copy(expr,expr.top,False)
        new_expr.expr1 = find_and_substitute(expr.expr1,to_substitute,var)
        if expr.expr2 is not None:
            new_expr.expr2 = find_and_substitute(expr.expr2,to_substitute,var)
        return new_expr

# tries to apply b-reduction
def b_reduction(expr:sh.Expression, debug:bool = False) -> sh.Expression:
    if expr.is_var:
        return expr

    if expr.expr2 is not None:
        expr.expr2 = b_reduction(expr.expr2,debug)
    expr.expr1 = b_reduction(expr.expr1,debug)


    expr_lambda = expr
    expr_sub = expr.expr2

    # check first if the expression is lambda
    if expr.is_lambda:
        # if the lambda expression has no 2nd expression it could be in the brackets above
        # so we search for it with a loop. If it doesnt exist no b-reduction is possible
        if expr_sub is None:
            tmp_expr = expr.top
            tmp_expr2 = tmp_expr
            while tmp_expr is not None and not tmp_expr.is_double and not tmp_expr.is_lambda:
                if tmp_expr.top is None: break
                tmp_expr = tmp_expr.top
                if tmp_expr.expr2 is tmp_expr2:
                    tmp_expr = None
                    break
                tmp_expr2 = tmp_expr
            if tmp_expr is not None and tmp_expr.is_double:
                expr_sub = tmp_expr.expr2
        # if a 2nd expression is found we first check if a-conversion is necessary and apply it
        if expr_sub is not None:
            expr_sub.top.expr2 = None

            old_content = sh.tree_to_str(expr)
            changed = a_conversion(expr_lambda,expr_sub)

            # if an a-conversion was applied we check if another iteration is necessary and apply it
            while changed:
                new_content = sh.tree_to_str(expr)
                if debug:
                    print(f"#[a-conversion] {old_content} -> {new_content}")
                old_content = new_content
                changed = a_conversion(expr_lambda,expr_sub) # if a-conversion was implied check if another one is possible

            # find the variables to substitue and substitute them
            new_expr = find_and_substitute(expr_lambda.expr1,expr_sub,expr_lambda.var)
            new_content = sh.tree_to_str(new_expr)
            if old_content != new_content and debug and expr.top is None:
                print(f"#[partial b-reduction] {old_content} -> {new_content}")
            return new_expr

    return expr
