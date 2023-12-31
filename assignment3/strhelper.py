import sys

# init used characters
ALPHA = "abcdefghijklmnopqrstuvwxyz"
ALPHA_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUM = "0123456789"
ALLCHAR = ALPHA + NUM + ALPHA_UPPER

# function for handling errors
def do_err(reason:str = "Something went wrong", content:str = ""):
    print("ERROR: " + reason + (f" | in: \'{content}\'" if content != "" else ""), file=sys.stderr)
    exit(1)

# checks if given string is a legal var
def check_var(s:str,is_upper:bool = False, in_str:str = ""):
    if len(s) == 0: do_err("Empty var")
    if is_upper:
        if s[0] not in ALPHA_UPPER: # must start with uppercase letter
           do_err("Uvar must start with an uppercase letter",s)
    elif s[0] not in ALPHA:
        do_err("Var must start with a letter",s) # must start with lowercase letter
        # check if the var only contains legal characters stop at ( or )
    for c in s:
        if c == '(' or c == ')':
            do_err('Bracket in var!',s)
        if c not in ALLCHAR:
            do_err("Illegal var name",s)

# find index of closing bracket which belongs to the opening bracket at char 0
def find_closing_bracket(s:str) -> int:
    open_count = 0
    for i in range(len(s)):
        if s[i] == '(': open_count += 1
        elif s[i] == ')':
            open_count -= 1
            if open_count == 0:
                return i
    do_err("Too many open brackets!",s)

class Type: pass # for type hinting
class Type: # class for the new type grammar
    def __init__(self, content: str = "", top:Type = None, top_expr:bool = False):
        self.content = content
        self.top = top
        self.is_var:bool = False
        self.var:str = ""
        self.type1:Type = None
        self.type2:Type = None
        self.top_expr:bool = top_expr # if the type comes from an expression

        if len(content) == 0:
            return
        elif content[0] == '(':
            closing_index = find_closing_bracket(content)
            index = content.rfind('->')
            if closing_index != len(content) - 1 and closing_index < index: # check for (A) -> B
                self.type1 = Type(content[:index],self)
                self.type2 = Type(content[index+2:],self)
            else: # check for (A)
                self.type1 = Type(content[1:len(content)-1],self)
        elif '->' not in content: # soley a var
            check_var(content,True) # check if the uvar is legal
            self.is_var = True
            self.var = content
        else: # check for A->B
            index = content.find('->')
            self.type1 = Type(content[:index],self)
            self.type2 = Type(content[index+2:],self)


class Expression: pass # for type hinting
class Expression: # class used for making a binary tree of tokens, recursively
    def __init__(self, content: str = "", top:Expression = None):
        self.content = content
        # for expressions with only 1 child like 'expr = (expr)' only expr1 is used
        self.expr1:Expression = None
        self.expr2:Expression = None
        self.top:Expression = top
        self.type:Type = None
        # types of expression (var, lambda, judgement also counts as expression to keep it simple)
        self.is_lambda:bool = False
        self.is_var:bool = False
        self.has_lambda:bool = False
        self.is_double:bool = False
        self.is_judgement:bool = False
        self.var:str = ""

        if len(content) == 0: # end here if empty constructor
            return
        elif ':' in content:
            index = content.find(':')
            self.is_judgement = True
            self.expr1 = Expression(content[:index])
            self.type = Type(content[index+1:])
        elif content[0] == '\\': # for lambda expressions
            self.is_lambda = True
            if '^' not in content:
                do_err("\'^\' expected in lambda expression",content)
            index = content.find('^')
            rest_str = content[index+1:] # skip over the ^
            is_bracket = False
            # find the closing_index of the type to split the type from the expression
            if rest_str[0] == '(':
                closing_index = find_closing_bracket(rest_str) + 1
                is_bracket = True
            else:
                closing_index = rest_str.find(' ')
                l_bracket_index = rest_str.find('(')
                if l_bracket_index != -1:
                    if l_bracket_index < closing_index or closing_index == -1:
                        is_bracket = True
                        closing_index = l_bracket_index
                elif closing_index == -1:
                    do_err("Invalid lambda expression!",content)
            self.var = content[1:index]
            check_var(self.var) # check if the var is legal
            # split the rest string into type and expression
            self.type = Type(content[index+1:index+closing_index+1],top_expr=True)
            self.expr1 = Expression(content[index+closing_index+1 + (not is_bracket):],self)
        elif content[0] == '(':
            closing_index = find_closing_bracket(content)
            if len(content) - 1 == closing_index: # check if there is only one (expr) and not (expr)(expr)
                self.expr1 = Expression(content[1:closing_index],self, True) # top is bracket (for lambda abstraction)
            else: # else we have to cut them into 2 expressions
                self.is_double = True
                self.expr1 = Expression(content[0:closing_index+1],self)
                self.expr2 = Expression(content[closing_index+1:len(content)],self)
        elif content.count(' ') == 0 and content.count('(') == 0: # check if its truly solely a var
            self.is_var = True
            check_var(content) # check if the var is legal
            self.var = content
        else: # for 2 expressions next to each other
            l_bracket_index = content.find('(')
            index = content.find(' ')
            if index == -1 or (l_bracket_index < index and l_bracket_index != -1):
                index = l_bracket_index
            self.expr1 = Expression(content[:index],self)
            self.expr2 = Expression(content[index+1:],self)
        if not self.is_var:
            self.has_lambda = self.expr1.is_lambda

# version of print_expr_tree for types
def print_type_tree(prefix:str, type:Type, is_left:bool): # prints binary tree using BT (for debug)
    if type is None: return
    print(prefix + ("├──" if is_left else "└──") + type_to_str(type))
    print_type_tree(prefix + ("│   " if is_left else "    "), type.type1, True)
    print_type_tree(prefix + ("│   " if is_left else "    "), type.type2, False)

def print_expr_tree(prefix:str, expr:Expression, is_left:bool): # prints binary tree using BT (for debug)
    if expr is None: return
    print(prefix + ("├──" if is_left else "└──") + tree_to_str(expr))
    if expr.type is not None:
        print_type_tree(prefix + ("│t  " if is_left else "    "), expr.type, True) # t means start of type tree
        print_expr_tree(prefix + ("│   " if is_left else "    "), expr.expr1, False)
    else:
        print_expr_tree(prefix + ("│   " if is_left else "    "), expr.expr1, True)
        print_expr_tree(prefix + ("│   " if is_left else "    "), expr.expr2, False)

# updated to remove spaces surrounding ':'
def remove_excess_spaces(s:str) -> str:
    # remove excess spaces
    while s.count("  ") > 0:
        s = s.replace("  ", " ")
    # remove spaces after closing bracket
    l = list(s)
    i = 0
    should_pop = False
    # remove spaces after [(,:,),^]
    while i < len(l):
        if l[i] == '(' or l[i] == ':' or l[i] == '^' or l[i] == ')':
            should_pop = True
        elif l[i] == '>':
            if l[i-1] != '-': do_err("Missing - before \''>\'",s)
            should_pop = True
        elif l[i] == ' ':
            if should_pop:
                l.pop(i)
                continue
        else:
            should_pop = False
        i += 1
    # remove spaces before [(,:,),^]
    i = len(l) - 1
    should_pop = False
    while i >= 0:
        if l[i] == ')' or l[i] == ':' or l[i] == '^' or l[i] == '(':
            should_pop = True
        elif l[i] == '-':
            if l[i+1] != '>': do_err("Missing > after \''-\'",s)
            should_pop = True
        elif l[i] == ' ':
            if should_pop:
                l.pop(i)
                continue
        else:
            should_pop = False
        i -= 1
    i = 0
    is_lambda = False
    while i < len(l):# remove spaces between lambda and var
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

# converts type subtree into string
def type_to_str(type:Type, has_brackets:bool = False) -> str:
    if type.is_var:
        return type.var
    if type.type2 is None:
        if has_brackets:
            return type_to_str(type.type1,True)
        return f"({type_to_str(type.type1,True)})"
    else:
        if has_brackets:
            return f"{type_to_str(type.type1,False)}->{type_to_str(type.type2,False)}"
        return f"({type_to_str(type.type1,False)}->{type_to_str(type.type2,False)})"

# converts expression subtree into string
def tree_to_str(expr:Expression, has_brackets:bool = False) -> str:
    if expr.is_judgement:
        return f"{tree_to_str(expr.expr1)}:{type_to_str(expr.type)}"
    if expr.is_lambda:
        return f"\\{expr.var}^{type_to_str(expr.type)}{'' if expr.expr1.content[0] == '(' else ' '}{tree_to_str(expr.expr1)}"
    if expr.is_var:
        return expr.var
    if expr.expr2 is None:
        if has_brackets:
            return tree_to_str(expr.expr1,True)
        #if not has_brackets and expr.top is not None and expr.top.is_double:
        return f"({tree_to_str(expr.expr1,True)})"
    else:
        if expr.expr1.is_var:
            return f"{tree_to_str(expr.expr1)}({tree_to_str(expr.expr2,True)})"
        elif expr.expr2.is_var:
            return f"({tree_to_str(expr.expr1,True)}){tree_to_str(expr.expr2)}"
        else:
            return f"({tree_to_str(expr.expr1,True)})({tree_to_str(expr.expr2,True)})"