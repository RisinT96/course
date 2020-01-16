from math import floor

int_to_roman_dict = {
    1000: 'M',
    900: 'CM',
    500: 'D',
    400: 'CD',
    100: 'C',
    90: 'XC',
    50: 'L',
    40: 'XL',
    10: 'X',
    9: 'IX',
    5: 'V',
    4: 'IV',
    1: 'I',
}

int_to_roman_sorted_list = sorted(int_to_roman_dict.items(), reverse=True)

can_repeat_romans = ['I', 'X', 'C', 'M']


def toroman(num):
    if not isinstance(num, int):
        raise TypeError(f'Expected {type(int)}, got {type(num)}')

    output = []

    while num > 0:
        for k, v in int_to_roman_sorted_list:
            if num < k:
                continue

            if v in can_repeat_romans:
                r = floor(num/k)
            else:
                r = 1

            output.append(v*r)
            num -= r*k
            break

    return ''.join(output)


print(toroman(1000))
print(toroman(100))
print(toroman(1100))
print(toroman(900))
print(toroman(800))
print(toroman(1111))
print(toroman(1611))
