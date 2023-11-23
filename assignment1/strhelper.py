def do_err(reason:str = "Something went wrong!", index:int = -1):
    print("ERROR: " + reason + (" | at char: " + str(index) if index >= 0 else ""), file=sys.stderr)
    exit(1)

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

def bracket_split(s:str, index:int, level:int, l:list) -> int:
    while index < len(s):
        if s[index] == '(':
            new_index = bracket_split(s,index + 1, level + 1, l)
            if index + 1 == new_index or s[index + 1:new_index] == ' ':
                do_err("Brackets without content!",index)
            l.append((level,s[index + 1:new_index],index))
            index = new_index
        elif s[index] == ')':
            if level == 0: do_err("Too many closed brackets!",index)
            return index
        index += 1
    if level != 0: do_err("Too many open brackets!", index)
