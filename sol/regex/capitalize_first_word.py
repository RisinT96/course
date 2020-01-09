import re

find_pattern = r"""([\w])([\w\s']*\.?)"""
pattrn = re.compile(find_pattern,re.DOTALL)

def capitalize_first_group(match):
    return f'{match.group(1).upper()}{match.group(2)}'

def capitalize(input_string):
    return pattrn.sub(repl=capitalize_first_group, string=input_string)


print(capitalize('''sentences are seperated by dots. asdasdasd.
don't forget the first sentence.
the last sentence might not end with a dot.
lgjsdlgkj 0934j dfsklj564lj;'''))