"""
Brute force solves the board game Mastermind. For more information about the game, see https://en.wikipedia.org/wiki/Mastermind_(board_game)

"""


import random
import itertools
from collections import Counter

# Orang Purpl Yelow Pink Blue
def display_board(positions):
    chars = {
        "horizontal divider":"-",
        "vertical divider":"|",
        "cross divider":"+",
        "empty key pin":".",
        "empty code pin":"  .  ",
        "empty":" "
    }
    row_types = [
        "div",
        "key",
        "empty",
        "key",
        "div",
        "code",
        "empty",
        "code",
        "empty",
        "code",
        "empty",
        "code",
        "div"
    ]

    for piece in range(MAX_GUESSES): # Fill empty spaces with dots
        for i in range(4 - len(positions["Guesses"][piece]["Guess"])):
            positions["Guesses"][piece]["Guess"].append(chars["empty code pin"])

        for i in range(4 - len(positions["Guesses"][piece]["Answer"])):
            positions["Guesses"][piece]["Answer"].append(chars["empty key pin"])

    columns = []

    divider_column = []

    for i in range(len(row_types)): # Create divider column
        if row_types[i] == "div":
            divider_column.append(chars["cross divider"])
        else:
            divider_column.append(chars["vertical divider"])


    columns.append(divider_column)
    for piece in range(MAX_GUESSES): # Create columns for each piece
        column = []
        for i in range(len(row_types)): # Create first column of piece
            if row_types[i] == "div":
                column.append(chars["horizontal divider"])
            elif row_types[i] == "key":
                if i == 1: # If we have the upper left key square
                    column.append(positions["Guesses"][piece]["Answer"][0])
                elif i == 3: # If we have the lower left key square
                    column.append(positions["Guesses"][piece]["Answer"][2])
            elif row_types[i] == "empty":
                column.append(chars["empty"])
            elif row_types[i] == "code":
                if i == 5: # If we have the top code
                    column.append(positions["Guesses"][piece]["Guess"][3])
                elif i == 7: # If we have the second from the top
                    column.append(positions["Guesses"][piece]["Guess"][2])
                elif i == 9: # If we have the third from the top
                    column.append(positions["Guesses"][piece]["Guess"][1])
                elif i == 11: # If we have the bottom
                    column.append(positions["Guesses"][piece]["Guess"][0])

        columns.append(column)
        column = []

        for x in range(3): # Create second, third and fourth columns
            for i in range(len(row_types)): # Create second column of piece
                if row_types[i] == "div":
                    column.append(chars["horizontal divider"])
                elif row_types[i] in ["key", "empty"]:
                    column.append(chars["empty"])
                elif row_types[i] == "code":
                    column.append("")

            columns.append(column)
            column = []

        for i in range(len(row_types)): # Create fifth column
            if row_types[i] == "div":
                column.append(chars["horizontal divider"])
            elif row_types[i] == "key":
                if i == 1:  # If we have the upper right key square
                    column.append(positions["Guesses"][piece]["Answer"][1])
                elif i == 3:  # If we have the upper left key square
                    column.append(positions["Guesses"][piece]["Answer"][3])
            elif row_types[i] == "code":
                column.append("")
            elif row_types[i] == "empty":
                column.append(" ")

        columns.append(column)
        columns.append(divider_column)


    lines = []
    for row in range(len(row_types)):
        lines.append([])

    for column in range(len(columns)):
        for row in range(len(columns[column])):
            lines[row].append(columns[column][row])


    for line in lines:
        print("".join(line))


def get_guess_from_user():
    result = []
    while len(result) < CODE_LENGTH:
        result = input("What is your guess?").split(" ")

    for item in range(len(result)):
        result[item] = colormap[result[item]]
    return result


def generate_guess(positions, possible_codes=None):
    global possibles
    if not possible_codes:
        duplicated_colors = []
        for i in range(len(colors)):
            for x in range(CODE_LENGTH):
                duplicated_colors.append(colors[i])

        possible_codes = list(itertools.permutations(duplicated_colors, CODE_LENGTH)) # Generate all possible permutations of the colors

    temp = []

    assert tuple(positions["Code"]) in possible_codes

    for possible_code in range(len(possible_codes)): # For each permutation, if it is valid with each of the previous guesses, add it to the list of permutations
        valid_guess = True
        for piece in range(len(positions["Guesses"])):
            if positions["Guesses"][piece]["Guess"] != ["  .  ", "  .  ", "  .  ", "  .  "]:
                if calculate_answer(positions["Guesses"][piece]["Guess"], possible_codes[possible_code]) != list(filter(lambda x: x != ".", positions["Guesses"][piece]["Answer"])): # If it is not valid
                    valid_guess = False
        if valid_guess:
            temp.append(possible_codes[possible_code])

    possible_codes = temp
    possibles = possible_codes

    print("Possible codes: " + str(len(possible_codes)))

    my_guess = possible_codes[random.randint(0, int(len(possible_codes) - 1))]

    return my_guess


def calculate_answer(guessed_code, code):
    result = []

    indices = []

    # Count the number of each color in each code
    guessed_count = Counter(list(guessed_code))
    code_count = Counter(list(code))

    # Get number of right guesses regardless of order
    temp_a = guessed_count - code_count # Subtract counter variables both ways, to get any differences without worrying about order
    temp_b = code_count - guessed_count

    sum_of_differences = sum(temp_a.values()) + sum(temp_b.values())

    same_type_number = len(guessed_code) - sum_of_differences

    # Find any pieces of the guess that are exactly right
    exact_number = 0
    for j in range(len(guessed_code)):
        if guessed_code[j] == code[j]:
            exact_number += 1
            same_type_number -= 1 # This would have shown up on the previous calculation. Remove it.

    # Return results
    for j in range(exact_number):
        result.append(key_colors["right place"])
    for j in range(same_type_number):
        result.append(key_colors["right color"])

    return result


key_colors = {"right color":"W", "right place":"R"}
colors = ["Purpl", "Orang", "Yelow", "Green", "Blue ", "Pink "]
full_color_names = ["Purple", "Orange", "Yellow", "Green", "Blue", "Pink"]
reverse_colormap = {
    "Purpl":"Purple", "Orang":"Orange", "Yelow":"Yellow", "Green":"Green", "Blue ":"Blue", "Pink ":"Pink"
}
colormap = {
    "P":"Purpl", "O":"Orang", "Y":"Yelow", "G":"Green", "B":"Blue ", "Pi":"Pink ",
    "Purple":"Purpl", "Orange":"Orang", "Yellow":"Yelow", "Green":"Green", "Blue":"Blue ", "Pink":"Pink "
}

board = {
    "Code":[], # Will be picked randomly
    "Guesses":[]
}

CODE_LENGTH = 4 # ABSOLUTELY MUST BE 4
MAX_GUESSES = 8

possibles = []

for i in range(MAX_GUESSES):
    board["Guesses"].append({"Guess":[], "Answer":[]})
for i in range(CODE_LENGTH): # Pick random secret code
    board["Code"].append(colors[random.randint(0, len(colors) - 1)]) # add a random color to secret code


for i in range(MAX_GUESSES):
    display_board(board)
    print("Valid colors are " + ", ".join(full_color_names))
    if possibles:
        guess = generate_guess(board, possibles)
    else:
        guess = generate_guess(board)

    board["Guesses"][i]["Guess"] = guess # Put guess on board
    board["Guesses"][i]["Answer"] = calculate_answer(guess, board["Code"])

    if board["Guesses"][i]["Answer"] == [key_colors["right place"], key_colors["right place"], key_colors["right place"], key_colors["right place"]]:
        print("You win!")
        break

display_board(board)
code_display = []
for i in range(len(board["Code"])):
    code_display.append(reverse_colormap[board["Code"][i]])
print("The secret code was " + " ".join(code_display))