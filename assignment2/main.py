import strhelper as sh, sys, interpreter

DEBUG = True

if __name__ == "__main__":
    if DEBUG:
        print("#DEBUG output enabled, debug output marked with \'#\' at the beginning of the line")
    times = 0
    if len(sys.argv) != 2:
        print("ERROR: No file argument or too many arguments were given", file=sys.stderr)
        exit(1)
    with open(sys.argv[1],"r") as f: line = f.readlines()[0]
    inp = line.replace('\n','').replace('\r','') # remove \r for windows to linux and the extra \n
    inp = sh.remove_excess_spaces(inp) # remove spaces
    expr = sh.Expression(inp,0,None,False)
    if DEBUG:
        print("#input tree:", inp)
        sh.print_expr_tree("#",expr,False)

    old_str = sh.tree_to_str(expr)
    expr = interpreter.b_reduction(expr,True)
    new_str = sh.tree_to_str(expr)
    while old_str != new_str:
        if DEBUG:
            print(f"#[b-reduction] {old_str} -> {new_str}")
        old_str = new_str
        expr = interpreter.b_reduction(expr,True)
    expr = interpreter.b_reduction(expr,True)
    print(sh.tree_to_str(expr))
    if DEBUG:
        print("#output tree:",sh.tree_to_str(expr))
        sh.print_expr_tree("#",expr,False)