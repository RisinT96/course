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

can_repeat_romans = ['I', 'X', 'C', 'M']


def toroman(num):
    if not isinstance(num, int):
        raise TypeError(f'Expected {type(int)}, got {type(num)}')

    output = []

    while num > 0:
        if num >= 1000:
            output.append(int_to_roman_dict[1000])
            num -= 1000
            continue

        if num >= 900:
            output.append(int_to_roman_dict[100])
            output.append(int_to_roman_dict[1000])
            num -= 900
            continue

        if num >= 500:
            output.append(int_to_roman_dict[500])
            num -= 500
            continue

        if num >= 400:
            output.append(int_to_roman_dict[100])
            output.append(int_to_roman_dict[500])
            num -= 400
            continue

        if num >= 100:
            r = floor(num/100)
            output.append(int_to_roman_dict[100]*r)
            num -= r*100
            continue

        if num >= 90:
            output.append(int_to_roman_dict[10])
            output.append(int_to_roman_dict[100])
            num -= 90
            continue

        if num >= 50:
            output.append(int_to_roman_dict[50])
            num -= 50
            continue

        if num >= 40:
            output.append(int_to_roman_dict[10])
            output.append(int_to_roman_dict[50])
            num -= 40
            continue

        if num >= 10:
            r = floor(num/10)
            output.append(int_to_roman_dict[10]*r)
            num -= r*10
            continue

        if num >= 9:
            output.append(int_to_roman_dict[1])
            output.append(int_to_roman_dict[10])
            num -= 9
            continue

        if num >= 5:
            output.append(int_to_roman_dict[5])
            num -= 5
            continue

        if num >= 4:
            output.append(int_to_roman_dict[1])
            output.append(int_to_roman_dict[5])
            num -= 4
            continue

        if num >= 1:
            r = floor(num/1)
            output.append(int_to_roman_dict[1]*r)
            num -= r*1
            continue

    return ''.join(output)


print(toroman(1000))
print(toroman(100))
print(toroman(1100))
print(toroman(900))
print(toroman(800))
print(toroman(1111))
print(toroman(1611))
