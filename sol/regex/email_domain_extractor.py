import re

with open('sol/regex/tlds.txt','rt') as f:
    tlds = f.readlines()

top_level_domains = [x.strip() for x in tlds]
top_level_domains = [x.lower() for x in top_level_domains] + [x.upper() for x in top_level_domains]
top_level_domains_pattern =  '|'.join(top_level_domains)

valid_normal_characters = r'[0-9a-zA-Z_\-+]'
valid_quoted_characters = valid_normal_characters + "|" + r'[\(\)\[\]\<\>,:;]|\\ |\\\\'
valid_email_names_pattern = fr'(:?{valid_normal_characters})+'

# Unfinished
pattern = fr"(?:{valid_normal_characters}\.?)+@([0-9a-zA-Z]+)\.(?:[0-9a-zA-Z]+\.)*(?:{top_level_domains_pattern})"

pat = re.compile(pattern)

print(re.findall(pattern,"sdfsdf@google.ass.COM"))