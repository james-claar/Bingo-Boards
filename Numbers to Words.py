"""
Converts numbers to words and vice versa. e.g. 1345 becomes 'one thousand three hundred forty five' and vice versa.

"""

import re

number_words = {"teens":["thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"],
                1:["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"],
                10:["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"],
                100:["hundred"],
                "thousand up":["thousand", "million", "billion", "trillion", "quadrillion", "quintillion", "sextillion", "septillion", "octillion", "nonillion", "decillion", "undecillion", "duodecillion", "tredecillion", "quattuordecillion", "quindecillion", "sexdecillion", "septendecillion", "octodecillion", "novemdecillion", "vigintillion"]}


number_values = {"zero":0, "one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9, "ten":10, "eleven":11, "twelve":12, "thirteen":13, "fourteen":14, "fifteen":15, "sixteen":16, "seventeen":17, "eighteen":18, "nineteen":19, "twenty":20, "thirty":30, "forty":40, "fifty":50, "sixty":60, "seventy":70, "eighty":80, "ninety":90, "hundred":100, "thousand":1000, "million":1000000, "billion":1000000000, "trillion":1000000000000, "quadrillion":1000000000000000, "quintillion":1000000000000000000, "sextillion":1000000000000000000000, "septillion":1000000000000000000000000, "octillion":1000000000000000000000000000, "nonillion":1000000000000000000000000000000, "decillion":1000000000000000000000000000000000, "undecillion":1000000000000000000000000000000000000, "duodecillion":1000000000000000000000000000000000000000, "tredecillion":1000000000000000000000000000000000000000000, "quattuordecillion":1000000000000000000000000000000000000000000000, "quindecillion":1000000000000000000000000000000000000000000000000, "sexdecillion":1000000000000000000000000000000000000000000000000000, "septendecillion":1000000000000000000000000000000000000000000000000000000, "octodecillion":1000000000000000000000000000000000000000000000000000000000, "novemdecillion":1000000000000000000000000000000000000000000000000000000000000, "vigintillion":1000000000000000000000000000000000000000000000000000000000000000}


def isint(num):
    checks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "."]
    for letter in str(num):
        is_an_int = False
        for i in checks:
            if str(i) == str(letter):
                is_an_int = True
        if not is_an_int:
            return False # if none of the characters is found
    return True


def phrase(word_list):
    temporary_list = []
    for i in word_list:
        if i in ["zero", "", None]:
            pass
        else:
            temporary_list.append(i)
    result = " ".join(temporary_list)
    return result


def list_index_split(some_list, *args):
    if args:
        args = (0,) + tuple(data+1 for data in args) + (len(some_list)+1,)
    my_list = []
    for start, end in zip(args, args[1:]):
        my_list.append(some_list[start:end])
    return my_list


def split_list(some_list, arg):
    where_arg_is = 0
    for item in range(len(some_list)):
        if some_list[item] == str(arg):
            where_arg_is = item

    result = list_index_split(some_list, where_arg_is)
    result[0].pop(-1)
    return result




def get_value(phrase_list):
    for i in range(len(phrase_list)):
        phrase_list[i] = number_values[phrase_list[i]]

    result = phrase_list[0]
    phrase_list.pop(0)
    if len(phrase_list) > 0:
        for i in range(len(phrase_list)):
            result = result * phrase_list[i]

    return result


def sort_into_phrases(word_list):
    result = []
    word_list = list(reversed(word_list))
    while len(word_list) > 0:
        if word_list[0] in number_words[1] or word_list[0] in number_words["teens"] or word_list[0] in number_words[10]:
            result.append([word_list[0]])
            word_list.pop(0)
        elif word_list[0] in number_words[100]:
            result.append(list(reversed(word_list[0:2])))
            for i in range(2):
                word_list.pop(0)
        elif word_list[0] in number_words["thousand up"]:
            if len(word_list) > 1:
                if word_list[1] in number_words[1] or word_list[1] in number_words["teens"] or word_list[1] in number_words[10]:
                    result.append([word_list[1], word_list[0]])
                    word_list.pop(1)
                elif word_list[1] in number_words[100]:
                    result.append([word_list[2], word_list[1], word_list[0]])
                    for i in range(2):
                        word_list.pop(1)
                elif word_list[1] in number_words["thousand up"]:
                    word_list.pop(0)
            else:
                word_list.pop(0)

    result = list(reversed(result))

    return result


def translate_number_to_word(untranslated):
    if float(untranslated) < 0: # untranslated is negative
        negative = True
        untranslated = abs(float(untranslated))
    else:
        negative = False

    untranslated = str(untranslated)
    if int(float(untranslated)) == float(untranslated) and not untranslated.isdigit():
        untranslated = str(int(float(untranslated)))
    if "." in untranslated:
        untranslated = untranslated.split(".")
        temp_decimal = 'point'
        for i in untranslated[1]:
            temp_decimal = temp_decimal + ' ' + translate_number_to_word(i)
        decimal = temp_decimal
        untranslated = int(untranslated[0])
    else:
        decimal = ''
        untranslated = int(untranslated)

    assert isinstance(untranslated, int)

    if untranslated <= 12:
        untranslated = number_words[1][untranslated]
    elif 13 <= untranslated <= 19: # If it is one of the 'teen numbers' from thirteen to nineteen
        untranslated = number_words["teens"][untranslated - 13]
    elif 20 <= untranslated <= 99: # Between twenty and ninety nine
        untranslated = phrase([number_words[10][int(str(untranslated)[0]) - 2], translate_number_to_word(int(str(untranslated)[1]))])
    elif 100 <= untranslated <= 999:
        untranslated = phrase([translate_number_to_word(int(str(untranslated)[0])), number_words[100][0], translate_number_to_word(int(str(untranslated)[1:]))])
    elif untranslated >= 1000:
        untranslated = str(untranslated)
        temp = ''
        if len(untranslated) % 3 != 0:
            temp = temp + phrase([translate_number_to_word(untranslated[:len(untranslated) % 3]), number_words["thousand up"][int(len(untranslated[len(untranslated) % 3:]) / 3 - 1)]])
            untranslated = untranslated[len(untranslated) % 3:]
        else:
            temp = temp + phrase([translate_number_to_word(untranslated[:3]), number_words["thousand up"][int(len(untranslated[3:]) / 3 - 1)]])
            untranslated = untranslated[3:]

        assert len(untranslated) % 3 == 0
        untranslated = re.findall("...", untranslated)
        for i in range(len(untranslated)):
            if int(untranslated[i]) != 0:
                if len(untranslated) == 1 or i == 0 or untranslated[i - 1] == "000":
                    filler = ''
                else:
                    filler = number_words["thousand up"][-i + len(untranslated) - 1]
                temp = phrase([temp, filler, translate_number_to_word(untranslated[i])])
        untranslated = temp

    if decimal:
        result = phrase([untranslated, decimal])
    else:
        result = untranslated

    if negative:
        result = "negative " + result

    return result


def translate_word_to_number(untranslated):
    untranslated = untranslated.lower().split(" ")

    if untranslated[0] == "negative": # untranslated is negative
        negative = True
        untranslated.pop(0)
    else:
        negative = False

    if "point" in untranslated: # Split decimal numbers
        untranslated = split_list(untranslated, "point")
        temp_decimal = "."
        for i in untranslated[1]:
            temp_decimal = temp_decimal + str(translate_word_to_number(i))
        decimal = temp_decimal
        untranslated = untranslated[0]
    else:
        decimal = ""

    phrases = sort_into_phrases(untranslated)


    result = 0
    for x in phrases:
        result += get_value(x)


    if decimal:
        result = float(str(result) + str(decimal))
    else:
        result = int(result)

    if negative:
        result = abs(result) * -1

    return result

user_input = input("Number or words to translate: ")

if isint(user_input):
    print(translate_number_to_word(user_input))
else:
    print(translate_word_to_number(user_input))