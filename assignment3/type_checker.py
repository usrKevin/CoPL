import strhelper as sh

def find_types(type_list:list[sh.Type], expr:sh.Expression):
    if expr.is_lambda:
        type_list.append(expr.type)
        return
    if expr.expr1 is not None:
        find_types(type_list,expr.expr1)
        if expr.expr2 is not None:
            find_types(type_list,expr.expr2)

def find_vars(set_vars:list[str], all_vars:list[str], expr:sh.Expression):
    if expr.is_var:
        all_vars.append(expr.var)
        return
    elif expr.is_lambda:
        set_vars.append(expr.var)

    find_vars(set_vars,all_vars,expr.expr1)
    if expr.expr2 is not None:
        find_vars(set_vars,all_vars,expr.expr2)

def compare_type(type1:sh.Type, type2:sh.Type) -> bool:
    if type1.is_var and type2.is_var:
        return type1.var == type2.var
    if type1.type2 is None:
        if type2.type2 is None:
            return compare_type(type1.type1,type2.type1)
        else:
            return False

    if type1.is_var != type2.is_var or type2.type2 is not None:
        return False

    # both (1->2)
    return compare_type(type1.type1,type2.type1) and compare_type(type1.type2,type2.type2)

def check_if_set(type:sh.Type, check_type:sh.Type) -> bool:
    if type.is_var:
        return check_type.is_var and type.var == check_type.var
    if type.type2 is None:
        return check_if_set(type.type1,check_type)
    if compare_type(type.type1,check_type):
        return True
    if check_if_set(type.type1,check_type):
        return True
    return check_if_set(type.type2,check_type)

def check_tree(expr:sh.Expression, debug:bool):
    type_list = []
    set_vars = []
    all_vars = []
    find_types(type_list,expr.expr1)
    find_vars(set_vars,all_vars,expr.expr1)
    for var in all_vars:
        if var not in set_vars:
            sh.do_err(f"Var: \'{var}\' has an unknown type!")
    for type in type_list: # check if all types are set
        if not check_if_set(expr.type,type):
            sh.do_err(f"Type: \'{sh.type_to_str(type)}\' does not match any type!")