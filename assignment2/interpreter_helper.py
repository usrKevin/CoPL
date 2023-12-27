import strhelper as sh

ALPHA = "abcdefghijklmnopqrstuvwxyz"

def collect_free_vars(expr:sh.Expression) -> list:
    if expr.is_var: return [expr.var]
    left = collect_free_vars(expr.expr1)
    if expr.expr2 is not None:
        right = collect_free_vars(expr.expr2)
        for el in right:
            if el not in left:
                left.append(el)
    return left

def collect_bound_vars(expr:sh.Expression) -> list:
    if expr is None:
        return []
    left = []
    if expr.is_lambda:
        left.append(expr.var)
    left.extend(collect_bound_vars(expr.expr1))
    if expr.expr2 is not None:
        right = collect_bound_vars(expr.expr2)
        for el in right:
            if el not in left:
                left.append(el)
    return left

# generates next usable var name
def generate_new_var(bound_vars:list, free_vars:list, free_vars1:list) -> str:
    used_vars = []
    used_vars.extend(bound_vars)
    for el in free_vars:
        if el not in used_vars:
            used_vars.append(el)
    for el in free_vars1:
        if el not in used_vars:
            used_vars.append(el)
    length = 1
    while True:
        for i in range(26 ** length):
            current_string = ""
            for j in range(length):
                current_string = chr(ord('a') + i % 26) + current_string
                i //= 26
            if current_string not in used_vars:
                return current_string
        length += 1

def tree_copy(to_copy:sh.Expression, top:sh.Expression, deep:bool = True) -> sh.Expression:
    if to_copy is None:
        return None
    new_obj = sh.Expression()
    # copy values over
    new_obj.content = to_copy.content
    new_obj.index = to_copy.index
    new_obj.var = to_copy.var
    new_obj.is_var = to_copy.is_var
    new_obj.is_lambda = to_copy.is_lambda
    new_obj.has_lambda = to_copy.has_lambda
    # fill in tree values
    new_obj.top = top
    ## recursion to reach the rest of the tree
    if deep:
        new_obj.expr1 = tree_copy(to_copy.expr1,new_obj,True)
        new_obj.expr2 = tree_copy(to_copy.expr2,new_obj,True)
    return new_obj

