import sys

# init used characters
ALPHA = "abcdefghijklmnopqrstuvwxyz"
NUM = "0123456789"
ALLCHAR = ALPHA + NUM

# function for handling errors
def do_err(reason:str = "Something went wrong", index:int = -1):
    print("ERROR: " + reason + (f" | at char: {index}" if index >= 0 else ""), file=sys.stderr)
    exit(1)

# checks if given string is a legal var
def check_var(s:str,index:int = -1):
    if len(s) == 0: do_err("Empty var",index)
    if s[0] not in ALPHA: do_err("Var must start with a letter",index) # must start with letter
    # check if the var only contains legal characters stop at ( or )
    for c in s:
        if c == '(' or c == ')': break
        if c not in ALLCHAR: do_err("Illegal var name",index)

# find index of closing bracket which belongs to the opening bracket at char 0
def find_closing_bracket(s:str) -> int:
    open_count = 0
    for i in range(len(s)):
        if s[i] == '(': open_count += 1
        elif s[i] == ')':
            open_count -= 1
            if open_count == 0:
                return i
    do_err("Too many open brackets!")

class Expression: pass # for type hinting
class Expression: # class used for making a binary tree of tokens, recursively
    def __init__(self, content: str = "", index: int = -1, top:Expression = None, is_abstract:bool = False):
        self.index = index
        self.content = content
        # for expressions with only 1 child like 'expr = (expr)' only expr1 is used
        self.expr1:Expression = None
        self.expr2:Expression = None
        self.top = top
        # types of expression (var also counts as expression to keep it simple)
        self.is_lambda:bool = False
        self.is_var:bool = False
        self.has_lambda:bool = False
        self.var:str = ""

        if index == -1 or len(content) == 0: # end here if empty constructor
            return
        elif content[0] == '\\': # for lambda expressions
            # find the var (spaces between \ and var have already been removed)
            spl = content.find(' ')
            is_bracket = False
            # check if var and expr are separated by ( or space
            l_bracket_index = content.find('(')
            if l_bracket_index != -1 and (l_bracket_index < spl or spl == -1):
                spl = l_bracket_index
                is_bracket = True

            if is_abstract: # (\x a b)
                self.is_lambda = True # set type

                var_str = content[1:spl] # copy var out
                if not is_bracket: spl += 1 # if the seperation is done by a space we jump it
                check_var(var_str,index+1) # check if its legal
                self.var = var_str
                self.expr1 = Expression(content[spl:len(content)],index+spl,self) # define expression via recursion
            else: # '\x a' b
                if not is_bracket and content.count(' ') < 2:
                    self.expr1 = Expression(content,index, self, True)
                elif is_bracket:
                    self.has_lamda = True
                    closing_index = l_bracket_index + find_closing_bracket(content[l_bracket_index:]) + 1
                    self.expr1 = Expression(content[:closing_index],index, self, True)
                    self.expr2 = Expression(content[closing_index:], index + closing_index,self)
                else:
                    self.has_lamda = True
                    spl += 1
                    closing_index = content.find(' ') + 1 + content[content.find(' ') + 1:].find(' ') # find 2nd ' '
                    self.expr1 = Expression(content[:closing_index],index, self, True)
                    self.expr2 = Expression(content[closing_index + 1:], index + closing_index,self)

        elif content[0] == '(':
            closing_index = find_closing_bracket(content)
            if len(content) - 1 == closing_index: # check if there is only one (expr) and not (expr)(expr)
                self.expr1 = Expression(content[1:closing_index],index+1, self, True) # top is bracket (for lambda abstraction)
            else: # else we have to cut them into 2 expressions
                self.expr1 = Expression(content[0:closing_index+1],index,self)
                self.expr2 = Expression(content[closing_index+1:len(content)], closing_index+index+1,self)
        elif content.count(' ') == 0 and content.count('(') == 0: # check if its truly solely a var
            self.is_var = True
            check_var(content,index)
            self.var = content
        else: # for 2 expressions next to each other
            l_bracket_index = content.find('(')
            if l_bracket_index != -1: # for for example: "expr(expr)"
                self.expr1 = Expression(content[0:l_bracket_index],index,self)
                self.expr2 = Expression(content[l_bracket_index:len(content)], l_bracket_index+index,self)
            else: # for for example: "expr expr"
                space_index = content.find(' ')
                self.expr1 = Expression(content[0:space_index],index,self)
                self.expr2 = Expression(content[space_index+1:len(content)], space_index+index+1,self)
        if not self.is_var:
            self.has_lambda = self.expr1.is_lambda

def print_expr_tree(prefix:str, expr:Expression, is_left:bool): # prints binary tree using BT (for debug)
    if expr is None: return
    print(prefix + ("├──" if is_left else "└──") + expr.content)
    print_expr_tree(prefix + ("│   " if is_left else "    "), expr.expr1, True)
    print_expr_tree(prefix + ("│   " if is_left else "    "), expr.expr2, False)

def remove_excess_spaces(s:str) -> str:
    # remove excess spaces
    while s.count("  ") > 0:
        s = s.replace("  ", " ")
    # remove spaces after closing bracket
    l = list(s)
    i = 0
    is_bracket = False
    while i < len(l):
        if l[i] == ')':
            is_bracket = True
        elif l[i] == ' ':
            if is_bracket:
                l.pop(i)
                continue
        else:
            is_bracket = False
        i += 1
    # remove spaces before opening bracket
    i = len(l) - 1
    is_bracket = False
    while i >= 0:
        if l[i] == '(':
            is_bracket = True
        elif l[i] == ' ':
            if is_bracket:
                l.pop(i)
                continue
        else:
            is_bracket = False
        i -= 1
    i = 0
    is_lambda = False
    while i < len(l):
        if l[i] == '\\':
            is_lambda = True
        elif l[i] == ' ':
            if is_lambda:
                l.pop(i)
                continue
        else:
            is_lambda = False
        i += 1
    return "".join(l)

def tree_to_str(expr:Expression) -> str:
    if expr.is_lambda:
        if expr.expr1.is_var:
            return "\\" + expr.var + " " + tree_to_str(expr.expr1)
        else:
            return "(\\" + expr.var + " " + tree_to_str(expr.expr1) + ")"
    if expr.is_var:
        return expr.var
    if expr.expr2 is None:
        return f"{tree_to_str(expr.expr1)}"
    else:
        if expr.expr1.is_var:
            return f"{tree_to_str(expr.expr1)}({tree_to_str(expr.expr2)})"
        elif expr.expr2.is_var:
            return f"({tree_to_str(expr.expr1)}){tree_to_str(expr.expr2)}"
        else:
            return f"({tree_to_str(expr.expr1)})({tree_to_str(expr.expr2)})"