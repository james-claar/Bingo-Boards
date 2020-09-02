"""
Minesweeper implementation in python. Played through command prompt.
Note: Although this program has an auto-save feature, it lacks much normal user input error checking and therefore tends to crash upon unacceptable user input.
"""

import random

ROWS = 7
COLUMNS = 7
MINES = 10

AUTOSAVE_BOOL = True # Whether or not the program should save to a file.
SAVE_FILE = "autosave.txt"

mine_grid = [] # 0 is empty, 1 is mine
numerical_grid = [] # Numbers are how many mines are around the space
visual_grid = [] # 0 means the user can see this space, 1 means unseen and unmarked, 2 means unseen flagged, and 3 means unseen question marked

visible_grid = [] # This is the grid that will be put into the board for the user to see. Needs updated every move.


def create_empty_grids():
    global mine_grid
    global numerical_grid
    global visual_grid
    global visible_grid

    for row in range(ROWS):
        mine_grid.append([])
        numerical_grid.append([])
        visual_grid.append([])
        visible_grid.append([])
        for column in range(COLUMNS):
            mine_grid[row].append(0)
            numerical_grid[row].append(0)
            visual_grid[row].append(1)
            visible_grid[row].append("   ")


def generate_mines():
    for i in range(MINES):
        spawn_row = random.randint(0, ROWS - 1) # spawn the mine in a random location
        spawn_column = random.randint(0, COLUMNS - 1)

        while mine_grid[spawn_row][spawn_column] == 1: # if this location is already occupied by a mine, try another
            spawn_row = random.randint(0, ROWS - 1)
            spawn_column = random.randint(0, COLUMNS - 1)

        mine_grid[spawn_row][spawn_column] = 1


def generate_mine_numbers():
    for row in range(ROWS):
        for column in range(COLUMNS):
            surrounding_squares = get_surrounding_squares(row, column)

            mine_count = 0
            for square in range(len(surrounding_squares)):
                if mine_grid[surrounding_squares[square][0]][surrounding_squares[square][1]] == 1: # if this surrounding square is a mine
                    mine_count += 1 # add it to the square's number

            numerical_grid[row][column] = mine_count


def get_surrounding_squares(row, column):
    square_coords = (row, column)
    output = []
    for i in range(3): # examine the 3*3 area with square_coords as the center
        for j in range(3):
            if 0 <= square_coords[0] + (i-1) <= ROWS - 1: # if the square's X axis is inside the grid
                if 0 <= square_coords[1] + (j-1) <= COLUMNS - 1: # if the square's Y axis is inside the grid
                    if (square_coords[0] + (i-1), square_coords[1] + (j-1)) != square_coords: # if it isn't the input square
                        output.append((square_coords[0] + (i-1), square_coords[1] + (j-1)))

    return output


def update_visible_grid():
    global mine_grid
    global numerical_grid
    global visual_grid
    global visible_grid
    text_key = {
        "clear":"   ",
        "1":" 1 ",
        "2":" 2 ",
        "3":" 3 ",
        "4":" 4 ",
        "5":" 5 ",
        "6":" 6 ",
        "7":" 7 ",
        "8":" 8 ",
        "uncovered mine":"XXX",
        "hidden":"[ ]",
        "flag":"[X]",
        "question":"[?]"
    }
    for row in range(ROWS):
        for column in range(COLUMNS):
            if visual_grid[row][column] in [1,2,3]: # deal with all 3 hidden square types
                if visual_grid[row][column] == 1:
                    visible_grid[row][column] = text_key["hidden"]
                elif visual_grid[row][column] == 2:
                    visible_grid[row][column] = text_key["flag"]
                elif visual_grid[row][column] == 3:
                    visible_grid[row][column] = text_key["question"]
            else: # if it's not one of the three hidden square types:
                if mine_grid[row][column] == 1:  # deal with uncovered mines
                    visible_grid[row][column] = text_key["uncovered mine"]
                else: # if it's not a mine hint number:
                    if numerical_grid[row][column] in [1, 2, 3, 4, 5, 6, 7, 8]:  # deal with mine hint numbers
                        visible_grid[row][column] = text_key[str(numerical_grid[row][column])]
                    else: # it's not any of these
                        visible_grid[row][column] = text_key["clear"]


def print_visible_grid():
    """
    example grid
    +---+---+---+---+---+---+---+
    |PYSWEEP| 1 | 2 | 3 | 4 | 5 |
    + Mines +   +   +   +   +   +
    |   3   |   |   |   |   |   |
    +---+---+---+---+---+---+---+
    | 1     |   | 1 | 1 | 2 |[ ]|
    +---+---+---+---+---+---+---+
    | 2     | * | 1 |[X]|[ ]|[ ]|
    +---+---+---+---+---+---+---+
    | 3     |   | 2 | 4 |[ ]|[ ]|
    +---+---+---+---+---+---+---+
    | 4     |   | 1 |[X]|[?]|[ ]|
    +---+---+---+---+---+---+---+
    | 5     |   | 1 |[ ]|[ ]|[ ]|
    +---+---+---+---+---+---+---+
    star is coords (1,2)

    """

    flag_count = 0
    for row in range(ROWS): # Count how many unflagged mines there are on the grid
        for column in range(COLUMNS):
            if visual_grid[row][column] == 2: # this square is flagged
                flag_count += 1

    separator_row = "+---+---"
    clear_separator_row = "+ Mines "
    clear_data_row = "|  " + space_int(MINES - flag_count) + "  "
    for i in range(COLUMNS):
        separator_row = separator_row + "+---"
        clear_separator_row = clear_separator_row + "+   "
        clear_data_row = clear_data_row + "|   "
    separator_row = separator_row + "+"
    clear_separator_row = clear_separator_row + "+"
    clear_data_row = clear_data_row + "|"

    column_marker_row = "|PYSWEEP"
    for i in range(COLUMNS):
        column_marker_row = column_marker_row + "|" + space_int(i + 1)
    column_marker_row = column_marker_row + "|"

    print(separator_row)
    print(column_marker_row)
    print(clear_separator_row)
    print(clear_data_row)

    for row in range(ROWS):
        print(separator_row)

        data_row = "|" + space_int(row + 1) + "    "
        for column in range(COLUMNS):
            data_row = data_row + "|" + visible_grid[row][column]
        data_row = data_row + "|"

        print(data_row)


    print(separator_row)


def space_int(num):
    num = str(int(num)) # ensure that num comes out as a string, we wouldn't want to add spaces to an int!

    if len(num) == 1:
        output = " " + num + " "
    elif len(num) == 2:
        output = num + " "
    elif len(num) == 3:
        output = num
    else:
        output = "BIG"

    return output


def receive_user_commands():
    help_text = "open <coords>: Reveals a square.\n" \
                "flag <coords>: Flags a square as a mine.\n" \
                "clear <coords>: Removes flags or question marks in the square.\n" \
                "chord/openaround <coords>: Opens all non-flagged squares around the square. Only works if the number of flags around it equals the number in the square.\n" \
                "flags/flagaround <coords>: Flags all hidden spaces around a square, if the number of spaces equals the number in the square.\n" \
                "help/?: Pulls up this help list.\n" \
                "exit/stop/quit: Stops the game.\n" \
                "\n" \
                "Replace all <coords> with the square coordinates, in column,row format with no spaces, i.e. '2,4'.\n" \
                "Example command:\n" \
                "flag 2,3\n" \
                "Will place a flag in the space at column 2 and row 3."
    valid_commands = [
        "open", "flag", "clear", "chord", "openaround", "flags", "flagaround", "help", "?", "exit", "stop", "quit", "load"
    ]

    user_input = input("PYSWEEP >>>").split(" ")
    command = user_input[0].lower()
    if command not in valid_commands:
        print("'" + str(command) + "' is not a valid command. Try 'help' or '?' for a list of commands")
        return # end the function due to invalid command
    elif command in ["exit", "stop", "quit"]:
        exit(0)
    elif command in ["help", "?"]:
        print(help_text)
        return  # end the function so we don't continue and get errors for not having args
    elif command == "load":
        load_save()
        return # end the function so we don't continue and get errors for not having args


    square = list(user_input[1].split(","))
    if len(square) != 2:
        return # end the function due to bad coords
    square.reverse() # reverse list so that the first value in the tuple is the column, not the row
    square[0] = int(square[0]) - 1
    square[1] = int(square[1]) - 1

    if command == "open":
        open_square(square[0], square[1])
    elif command == "flag":
        if visual_grid[square[0]][square[1]] != 0: # We are a hidden square
            visual_grid[square[0]][square[1]] = 2
    elif command == "clear":
        if visual_grid[square[0]][square[1]] in [2,3]:  # We are a flag or a question mark
            visual_grid[square[0]][square[1]] = 1
    elif command in ["chord", "openaround"]:
        if visual_grid[square[0]][square[1]] == 0: # We can see this square
            if numerical_grid[square[0]][square[1]] in [1,2,3,4,5,6,7,8]: # It is a mine hint number
                surrounding_squares = get_surrounding_squares(square[0], square[1])

                mine_count = 0
                for adj_square in range(len(surrounding_squares)):
                    if visual_grid[surrounding_squares[adj_square][0]][surrounding_squares[adj_square][1]] == 2: # this is a flag
                        mine_count += 1

                if numerical_grid[square[0]][square[1]] == mine_count:
                    for adj_square in surrounding_squares:
                        if visual_grid[adj_square[0]][adj_square[1]] == 1: # this square is unseen and unmarked
                            open_square(adj_square[0], adj_square[1]) # open it
    elif command in ["flags", "flagaround"]:
        if visual_grid[square[0]][square[1]] == 0: # We can see this square
            if numerical_grid[square[0]][square[1]] in [1,2,3,4,5,6,7,8]: # It is a mine hint number
                surrounding_squares = get_surrounding_squares(square[0], square[1])

                hidden_count = 0
                for adj_square in range(len(surrounding_squares)):
                    if visual_grid[surrounding_squares[adj_square][0]][surrounding_squares[adj_square][1]] != 0: # this is a hidden square
                        hidden_count += 1

                if numerical_grid[square[0]][square[1]] == hidden_count:
                    for adj_square in range(len(surrounding_squares)):
                        if visual_grid[surrounding_squares[adj_square][0]][surrounding_squares[adj_square][1]] != 0: # if this square is hidden:
                            visual_grid[surrounding_squares[adj_square][0]][surrounding_squares[adj_square][1]] = 2 # flag this square


def shift_mines_from_square(row, column):
    global mine_grid
    surrounding_squares = get_surrounding_squares(row, column)
    surrounding_squares.append((row, column))

    mines_around_bool = True
    while mines_around_bool:
        for adj_square in surrounding_squares:
            if mine_grid[adj_square[0]][adj_square[1]] == 1:
                mine_grid[adj_square[0]][adj_square[1]] = 0

                spawn_row = random.randint(0, ROWS - 1)  # spawn the mine in a random location
                spawn_column = random.randint(0, COLUMNS - 1)

                while mine_grid[spawn_row][spawn_column] == 1:  # if this location is already occupied by a mine, try another
                    spawn_row = random.randint(0, ROWS - 1)
                    spawn_column = random.randint(0, COLUMNS - 1)

                mine_grid[spawn_row][spawn_column] = 1

        temp = False
        for adj_square in surrounding_squares:
            if mine_grid[adj_square[0]][adj_square[1]] == 1:
                temp = True
        mines_around_bool = temp

    generate_mine_numbers() # update the mine numbers


def open_square(row, column):
    global first_square_opened
    if first_square_opened:
        shift_mines_from_square(row, column)
        first_square_opened = False

    if visual_grid[row][column] == 2: # this square is flagged
        visual_grid[row][column] = 3 # set it to a question mark
    elif visual_grid[row][column] == 3: # this square has a question mark
        visual_grid[row][column] = 1 # remove the question mark
    elif mine_grid[row][column] == 1: # we hit a non-flagged mine
        game_over()
    elif numerical_grid[row][column] in [1,2,3,4,5,6,7,8]: # we hit a mine hint number
        visual_grid[row][column] = 0
    else: # we hit a blank space
        visual_grid[row][column] = 0
        surrounding_squares = get_surrounding_squares(row, column)
        for square in range(len(surrounding_squares)):
            if visual_grid[surrounding_squares[square][0]][surrounding_squares[square][1]] != 0:
                open_square(surrounding_squares[square][0], surrounding_squares[square][1])


def check_win():
    possible_win = True
    for row in range(ROWS): # If we can see every space that is not a mine, we win
        for column in range(COLUMNS):
            if visual_grid[row][column] != 0 and mine_grid[row][column] == 0: # If we cannot see this space but it is not a mine, we do not win
                possible_win = False
    if possible_win:
        print("You win! Yay!")
        exit(0)


def game_over():
    for row in range(ROWS): # reveal all of the spaces
        for column in range(COLUMNS):
            visual_grid[row][column] = 0

    update_visible_grid()
    print_visible_grid()

    print("You have triggered a mine! Better luck next time!")

    exit(0)


def auto_save():
    with open(SAVE_FILE, "w+") as f:
        f.write(str(ROWS) + "\n")
        f.write(str(COLUMNS) + "\n")
        f.write(str(MINES) + "\n")

        for row in range(ROWS): # save the mine grid
            for column in range(COLUMNS):
                f.write(str(mine_grid[row][column]) + "/")
        f.write("\n") # we skip the numerical grid, because it can be generated from the mine grid
        for row in range(ROWS): # save the visual grid
            for column in range(COLUMNS):
                f.write(str(visual_grid[row][column]) + "/")


def load_save():
    global ROWS
    global COLUMNS
    global MINES
    global mine_grid
    global numerical_grid
    global visual_grid
    global first_square_opened
    first_square_opened = False # otherwise we will shift mines away from the first click

    with open("Pysweeper Saves\\autosave.txt", "r") as f:
        lines = f.readlines()
    ROWS = int(lines[0])
    COLUMNS = int(lines[1])
    MINES = int(lines[2])

    temp = lines[3][:-2].split("/") # Load the mine grid
    for row in range(ROWS):
        for column in range(COLUMNS):
            mine_grid[row][column] = int(temp[(row * COLUMNS) + column])
    generate_mine_numbers()

    temp = lines[4].split("/") # Load the visual grid
    for row in range(ROWS):
        for column in range(COLUMNS):
            visual_grid[row][column] = int(temp[(row * COLUMNS) + column])



first_square_opened = True
create_empty_grids()
generate_mines()
generate_mine_numbers()
update_visible_grid()
print_visible_grid()
while True:
    receive_user_commands()
    if AUTOSAVE_BOOL:
        auto_save()
    update_visible_grid()
    print_visible_grid()
    check_win()
