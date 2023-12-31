import strhelper as sh, sys

DEBUG = False

if __name__ == "__main__":
    times = 0
    if len(sys.argv) != 2:
        print("ERROR: No file argument or too many arguments were given", file=sys.stderr)
        exit(1)
    with open(sys.argv[1],"r") as f: lines = f.readlines()
    for line in lines:
        inp = line.replace('\n','').replace('\r','') # remove \r for windows to linux and the extra \n
        inp = sh.remove_excess_spaces(inp) # remove spaces
        if inp.count('(') != inp.count(')'):
            print("Bracket count inequality!", file=sys.stderr)
            exit(1)
        expr = sh.Expression(inp,0)
        print(sh.tree_to_str(expr))
        if DEBUG:
            sh.print_expr_tree("#",expr,False)
