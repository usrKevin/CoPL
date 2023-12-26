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
    if expr.is_lambda: return [expr.var]
    if expr.is_var: return []
    left = collect_bound_vars(expr.expr1)
    if expr.expr2 is not None:
        right = collect_bound_vars(expr.expr2)
        for el in right:
            if el not in left:
                left.append(el)
    return left

# generates next usable var name
def generate_new_var(bound_vars:list, free_vars:list) -> str:
    used_vars = []
    for el in free_vars:
        used_vars.append(el)
    for el in bound_vars:
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

def deep_tree_copy(to_copy:sh.Expression) -> sh.Expression:
    new_obj = sh.Expression()