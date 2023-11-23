import strhelper as sh

#git push --set-upstream origin main

if __name__ == "__main__":
    inp = input()
    inp = sh.remove_excess_spaces(inp) # remove spaces
    bracket_list = []
    sh.bracket_split(inp, 0, 0, bracket_list) # also checks for bracket err
    #inp = sh.remove_excess_brackets(inp, bracket_list)
    print(inp)
