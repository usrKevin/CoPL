#git push --set-upstream origin main


def remove_lambda_spaces(s:str) -> str:
    i = 0
    is_lambda = False
    l = list(s)
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
    is_bracket = False
    i = len(l) - 1
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
    return "".join(l)

if __name__ == "__main__":
    print(remove_lambda_spaces(remove_excess_spaces("1  2e  ()  \\   9 (65u6) p")))
    print("run")
