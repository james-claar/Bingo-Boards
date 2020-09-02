"""
Program to convert one unit to another, which displays the divisions necessary to convert the units.
"""

import itertools
import math

# Every unit the program knows about
units = {
    "Liquid Volume":[
        # Metric
        "kl",
        "l",
    ],
    "Mass":[
        # Metric
        "kg",
        "g",
        "mg",
        "ug",
        "ng",
        "pg",
    ],
    "Weight":[
        # US
        "t",
        "st",
        "lb",
        "oz",

        # Metric
    ],
    "Distance":[
        # Metric
        "km",
        "m",
        "cm",
        "mm",
        "um",
        "nm",
    ],
    "Square Distance":[
        #AUTO GENERATED FROM DISTANCE
    ],
    "Cubic Distance":[
        #AUTO GENERATED FROM DISTANCE
    ],
}

# Every conversion relationship the program knows about
relationships = {
    "Between Types Conversions":[
        [[1, "ml", "Liquid Volume"], [1, "cm^3", "Cubic Distance"]],
    ],

    "Liquid Volume":[
        [[1, "kl"], [1000, "l"]],
        [[1, "l"], [1000, "ml"]],
    ],

    "Mass":[
        [[1, "kg"], [1000, "g"]],
        [[1, "g"], [1000, "mg"]],
        [[1, "mg"], [1000, "ug"]],
        [[1, "ug"], [1000, "ng"]],
        [[1, "ng"], [1000, "pg"]],
    ],

    "Weight":[
        [[1, "t"], [2000, "lb"]],
        [[1, "st"], [14, "lb"]],
        [[1, "lb"], [16, "oz"]],
    ],

    "Distance":[
        [[1, "km"], [1000, "m"]],
        [[1, "m"], [100, "cm"]],
        [[1, "m"], [1000, "mm"]],
        [[1, "mm"], [1000, "um"]],
        [[1, "um"], [1000, "nm"]],
        [[1, "nm"], [1000, "pm"]],

        [[1, "in"], [2.54, "cm"]],

        [[1, "mi"], [5280, "ft"]],
        [[1, "yd"], [3, "ft"]],
        [[1, "ft"], [12, "in"]],
    ],

    "Square Distance":[
        #AUTO GENERATED FROM DISTANCE
    ],

    "Cubic Distance": [
        # AUTO GENERATED FROM DISTANCE
    ]
}


def true_round(number, places):
    place = 10 ** places
    rounded = (int(number * place + 0.5 if number >= 0 else -0.5)) / place
    if rounded == int(rounded):
        rounded = int(rounded)
    return rounded


def generate_extra_units():  # Creates square and cubic distance units in the units list, and adds their relationships to the relationships list
    for i in range(len(units["Distance"])):
        units["Square Distance"].append(units["Distance"][i] + "^2")  # add a square distance
        units["Cubic Distance"].append(units["Distance"][i] + "^2")  # add a cubic distance

    for relationship in relationships["Distance"]:
        relationships["Square Distance"].append([[relationship[0][0]**2, relationship[0][1]+"^2"], [relationship[1][0]**2, relationship[1][1]+"^2"]]) # add a square relationship
        relationships["Cubic Distance"].append([[relationship[0][0]**3, relationship[0][1]+"^3"], [relationship[1][0]**3, relationship[1][1]+"^3"]]) # add a cubic relationship


def get_unit_type(unit): # Returns the field of measurement this unit is a part of, as a string: e.g. 'Distance'
    for key in relationships.keys():
        if not key == "Between Types Conversions":
            for relationship in relationships[key]:
                if unit in [relationship[0][1], relationship[1][1]]:
                    return key


def filter_list_of_relationships_by_unit(list_of_relationships, unit, second_unit=None): # Returns a list of the inner lists that include the specified unit, with that unit first.
    return_list = []
    for relationship in list_of_relationships:
        if second_unit:
            if relationship[0][2] in [unit, second_unit] and relationship[1][2] in [unit, second_unit]:
                if relationship[0][1] == unit:
                    return relationship
                else:
                    return list(reversed(relationship))
        else:
            if relationship[0][1] == unit: # The unit is in the first part of the relationship
                return_list.append(relationship)
            elif relationship[1][1] == unit: # The unit is in the second part of the relationship
                return_list.append(list(reversed(relationship)))
    return return_list


def test_path(path, unit_from, unit_to):
    if path[0][0][1] == unit_from: # The first part of the first conversion must be the unit we want to convert from
        if path[-1][1][1] == unit_to: # The last part of the last conversion must be the unit we want to convert to
            for i in range(len(path) - 1):
                if not path[i][1][1] == path[i + 1][0][1]: # The last unit of the current conversion must be the same as the first unit in the second conversion
                    return False

            # If we reach this point it means we have passed all the tests.
            return True

        else:
            return False
    else:
        return False


def fix_path_looping(path): # This function assumes that there will not be three redundant conversions in a row. If this happens, it will delete too many items.
    redundant = []
    for i in range(len(path)-1): # Check if we are changing back and forth on conversions, e.g. '(100 cm/1 m) * (1 m/100 cm)'
        if path[i] == list(reversed(path[i + 1])):
            redundant.append(i)
            redundant.append(i+1)

    redundant = list(reversed(redundant))
    for i in sorted(redundant, reverse=True):
        del path[i]

    return path


def find_conversion_path(unit_from, unit_to, extra_relationships=None):
    type_from = get_unit_type(unit_from)
    type_to = get_unit_type(unit_to)

    if type_from == type_to or extra_relationships:
        possible_relationships = relationships[type_from] # Get all relevant relationships

        if extra_relationships:
            possible_relationships.extend(extra_relationships)

        for relationship in range(len(possible_relationships)):
            possible_relationships.append(list(reversed(possible_relationships[relationship])))

        for i in range(len(possible_relationships)): # Iter over all the permutations in increasing length until a good permutation has been found
            permutations = tuple(itertools.permutations(possible_relationships, i+1))

            for permutation in permutations:
                if test_path(permutation, unit_from, unit_to):
                    permutation = fix_path_looping(list(permutation))

                    return permutation
    else: # Our path requires a change of unit types
        best_transfer_relationship = [filter_list_of_relationships_by_unit(relationships["Between Types Conversions"], get_unit_type(unit_from), get_unit_type(unit_to))]

        start_path = list(find_conversion_path(unit_from, best_transfer_relationship[0][1][1], best_transfer_relationship)) # Find the shortest path to the chosen between types conversion
        end_path = list(find_conversion_path(best_transfer_relationship[0][1][1], unit_to))

        start_path.extend(end_path)

        return start_path


def find_significant_figures(number):
    # change all the 'E' to 'e'
    number = str(number)
    number = number.lower()
    if 'e' in number:
        # return the length of the numbers before the 'e'
        my_str = number.split('e')
        return len(my_str[0]) - 1  # to compensate for the decimal point
    else:
        # put it in e format and return the result of that
        ### NOTE: because of the 8 below, it may do crazy things when it parses 9 significant figures
        n = ('%.*e' % (8, float(number))).split('e')
        # remove and count the number of removed user added zeroes. (these are sig figs)
        if '.' in number:
            s = number.replace('.', '')
            # number of zeroes to add back in
            l = len(s) - len(s.rstrip('0'))
            # strip off the python added zeroes and add back in the ones the user added
            n[0] = n[0].rstrip('0') + ''.join(['0' for _ in range(l)])
        else:
            # the user had no trailing zeroes so just strip them all
            n[0] = n[0].rstrip('0')
        # pass it back to the beginning to be parsed
    return find_significant_figures('e'.join(n))


def pad_spaces(string, length):
    while len(string) < length:  # Pad spaces until the string reaches a certain length
        string = string + " " # Add a space on the right

        if len(string) == length: # Break the loop if we are already at the right length
            break
        else:
            string = " " + string # Add a space on the left

        # The while loop should catch if it is at the right length now

    return string


def relationship_to_text_fraction(relationship):
    relationship[0] = str(relationship[0][0]) + " " + relationship[0][1] # Would turn something like [23, 'cm'] into '23 cm'
    relationship[1] = str(relationship[1][0]) + " " + relationship[1][1] # Does the same thing to the other side of the relationship

    length = max(len(relationship[0]), len(relationship[1])) # Find out which string is longest

    relationship[0] = pad_spaces(relationship[0], length) # Get both strings at the right length by padding with spaces
    relationship[1] = pad_spaces(relationship[1], length)

    div_bar = ""
    for i in range(length):
        div_bar = div_bar + "-"

    return [
        relationship[0],
        div_bar,
        relationship[1]
    ]


def add_strings_within_list(list_one, list_two):
    return_list = []

    for i in range(len(list_one)):
        return_list.append(list_one[i] + list_two[i])

    return return_list


def to_precision(x,p):
    """
    returns a string representation of x formatted with a precision of p

    Based on the webkit javascript implementation taken from here:
    https://code.google.com/p/webkit-mirror/source/browse/JavaScriptCore/kjs/number_object.cpp
    """

    x = float(x)

    if x == 0.:
        return "0." + "0"*(p-1)

    out = []

    if x < 0:
        out.append("-")
        x = -x

    e = int(math.log10(x))
    tens = math.pow(10, e - p + 1)
    n = math.floor(x/tens)

    if n < math.pow(10, p - 1):
        e = e -1
        tens = math.pow(10, e - p+1)
        n = math.floor(x / tens)

    if abs((n + 1.) * tens - x) <= abs(n * tens -x):
        n = n + 1

    if n >= math.pow(10,p):
        n = n / 10.
        e = e + 1

    m = "%.*g" % (p, n)

    if e < -2 or e >= p:
        out.append(m[0])
        if p > 1:
            out.append(".")
            out.extend(m[1:p])
        out.append('e')
        if e > 0:
            out.append("+")
        out.append(str(e))
    elif e == (p -1):
        out.append(m)
    elif e >= 0:
        out.append(m[:e+1])
        if e+1 < len(m):
            out.append(".")
            out.extend(m[e+1:])
    else:
        out.append("0.")
        out.extend(["0"]*-(e+1))
        out.append(m)

    return "".join(out)


def calculate_number_from_path(path, number, significant=False):
    significant_figures = find_significant_figures(number)

    if "." in str(number): # Turn the number into something we can calculate on, while preserving the decimal point if there is one
        number = float(number)
    else:
        number = int(number)

    for i in range(len(path)): # Perform the operations on this number
        number = number * (path[i][1][0] / path[i][0][0])

    if significant:
        new_significant_figures = find_significant_figures(number)
        if new_significant_figures != significant_figures:
            number = to_precision(number, significant_figures)



    return str(number)


def print_path(path, number, unit, end_unit):
    to_print = relationship_to_text_fraction([[number, unit], [" 1", ""]]) # Turn our first number into a fraction over one

    for relationship in path:
        to_print = add_strings_within_list(to_print, ["   ", " x ", "   "]) # Add the multiplication symbol between fractions

        to_print = add_strings_within_list(to_print, relationship_to_text_fraction(list(reversed(relationship)))) # Add the relationship as a fraction, reversing it so that everything can cancel

    to_print[1] = to_print[1] + " = " # Add the equals sign

    calculated_number = calculate_number_from_path(path, number)

    to_print[1] = to_print[1] + str(calculated_number) + " " + end_unit

    for line in to_print:
        print(line)


# Create square and cubic units
generate_extra_units()

# Get the first part of the conversion: '5 cm^2' for example
raw_user_input = ""

while not raw_user_input and not " " in raw_user_input:
    print("Welcome to measurement converter. Please type in conversion amount WITH THE UNIT. For example: '4 ml', '3 km', '5 m^3'")
    raw_user_input = input(" > ")



raw_user_input = raw_user_input.split(" ")
number_to_convert = raw_user_input[0]
unit_to_convert_from = raw_user_input[1]


# Get the unit to convert to
raw_user_input = ""

while not raw_user_input:
    print("\nNow, please type in the unit you would like to convert to. For example: 'mm', 'l'")
    raw_user_input = input(" > ")

unit_to_convert_to = raw_user_input

print()

print_path(find_conversion_path(unit_to_convert_from, unit_to_convert_to), number_to_convert, unit_to_convert_from, unit_to_convert_to)