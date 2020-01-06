from collections import Counter


def char_count(string,  most_common=None):
    if(most_common is None):
        return dict(Counter(string))

    return dict(Counter(string).most_common(most_common))


def word_count(string, most_common=None):
    if(most_common is None):
        return dict(Counter(string.split()))

    return dict(Counter(string.split()).most_common(most_common))


print(char_count("aabbba"))
print(word_count("How much wood would a woodfuck fuck if a woodchuck could fuck wood", 1))
