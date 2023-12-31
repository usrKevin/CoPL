import strhelper as sh, sys, type_checker as tc

DEBUG = False

if __name__ == "__main__":
    times = 0
    if len(sys.argv) != 2:
        print("ERROR: No file argument or too many arguments were given", file=sys.stderr)
        exit(1)

    with open(sys.argv[1],"r") as f:
        if not f.readable():
            sh.do_err(f"File \'{sys.argv[1]}\' not readable!")
        lines = f.readlines()
    for line in lines:
        inp = line.replace('\n','').replace('\r','') # remove \r for windows to linux and the extra \n
        inp = sh.remove_excess_spaces(inp) # remove spaces
        if inp.count('(') != inp.count(')'):
            sh.do_err("Bracket count inequality!")
        if inp.count(':') != 1:
            sh.do_err("Multiple or no judgements in string!")

        expr = sh.Expression(inp) # tree creation
        if DEBUG:
            print(f"# Formatted input: {inp}")
            sh.print_expr_tree("#",expr,False)
        tc.check_tree(expr,DEBUG) # check the tree for any errors
        print(sh.tree_to_str(expr))
