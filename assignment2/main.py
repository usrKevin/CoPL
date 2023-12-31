import strhelper as sh, sys, interpreter

DEBUG = False

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
    if inp.count('(') != inp.count(')'):
        print("Bracket count inequality!", file=sys.stderr)
        exit(1)
    expr = sh.Expression(inp,None,False)
    if DEBUG:
        print("#input tree:", inp)
        sh.print_expr_tree("#",expr,False)

    old_str = sh.tree_to_str(expr)
    expr = interpreter.b_reduction(expr,DEBUG) # first iteration of b-reduction
    new_str = sh.tree_to_str(expr)
    # if b-reduction was applied do another iteration to check if another is possible with the new tree
    while old_str != new_str:
        if DEBUG:
            print(f"#[b-reduction] {old_str} -> {new_str}")
        old_str = new_str
        expr = interpreter.b_reduction(expr,DEBUG) # do the b-reduction again
    expr = interpreter.b_reduction(expr,DEBUG)
    print(sh.tree_to_str(expr)) # print the final output
    if DEBUG:
        print("#output tree:",sh.tree_to_str(expr))
        sh.print_expr_tree("#",expr,False)