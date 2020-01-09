import re

find_pattern = r"(?P<bob>\b[kK][a-zA-Z]*)"

def replace_with_bob(in_string):
    return re.sub(pattern=find_pattern,repl='bob', string=in_string)


print(replace_with_bob('ass kass cake kace'))
print(replace_with_bob('A knight with a knife'))