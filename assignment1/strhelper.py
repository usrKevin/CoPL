import sys

ALPHA = "abcdefghijklmnopqrstuvwxyz"
NUM = "0123456789"
ALLCHAR = ALPHA + NUM

def do_err(reason:str = "Something went wrong", index:int = -1):
    print("ERROR: " + reason + (f" | at char: {index}" if index >= 0 else ""), file=sys.stderr)
    exit(1)


def check_var(s:str,index:int = -1):
    if len(s) == 0: do_err("Empty var",index)
    if s[0] not in ALPHA: do_err("Var must start with a letter",index)
    for c in s:
        if c == '(' or c == ')': break
        if c not in ALLCHAR: do_err("Illegal var name",index)

def find_closing_bracket(s:str) -> int:
    open_count = 0
    for i in range(len(s)):
        #print(f"{s} | {s[i]} | {open_count}")
        if s[i] == '(': open_count += 1
        elif s[i] == ')':
            open_count -= 1
            if open_count == 0:
                return i
    do_err("Too many open brackets!")



class Expression: pass # for type hinting
class Expression:
    expr1:Expression = None
    expr2:Expression = None
    var:str = ""
    is_lambda:bool = False
    is_var:bool = False


    def __init__(self, content: str, index: int):
        self.index = index
        self.content = content
        if len(content) == 0: pass
        elif content[0] == '\\':
            self.is_lambda = True
            spl = content.find(' ')
            is_bracket = False
            if content.find('(') < spl or spl == -1:
                spl = content.find('(')
                is_bracket = True
            var_str = content[1:spl]
            if not is_bracket: spl += 1
            check_var(var_str,index+1)
            self.var = var_str
            self.expr1 = Expression(content[spl:index+len(content)],index+spl)
        elif content[0] == '(':
            closing_index = find_closing_bracket(content)
            if len(content) - 1 == closing_index:
                self.expr1 = Expression(content[1:closing_index],index+1)
            else:
                self.expr1 = Expression(content[0:closing_index+1],index)
                self.expr2 = Expression(content[closing_index+1:len(content)], closing_index+index+1)
        elif content.count(' ') == 0:
            self.is_var = True
            check_var(content,index)

def print_expr_tree(prefix:str, expr:Expression, is_left:bool):
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
        elif i+1<len(l) and l[i]+l[i+1] == '  ':
            if is_lambda:
                l.pop(i)
                continue
        else:
            is_lambda = False
        i += 1
    return "".join(l)

def bracket_split(s:str, index:int, level:int, l:list) -> int:
    while index < len(s):
        if s[index] == '(':
            new_index = bracket_split(s,index + 1, level + 1, l)
            if index + 1 == new_index or s[index + 1:new_index] == ' ':
                do_err("Brackets without content",index)
            new_el = (level,s[index + 1:new_index],index)
            l.append(new_el)
            #if parent is not None: parent.children.append(new_el)
            index = new_index
        elif s[index] == ')':
            if level == 0: do_err("Too many closed brackets",index)
            return index
        index += 1
    if level != 0: do_err("Too many open brackets", index)
