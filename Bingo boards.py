import random
import math

AMT_OF_BOARDS = 2
FREE_SPACE = True
DIAGONALS = True


class Board:
    def __init__(self, free_space):
        self.board = [
            [],
            [],
            [],
            [],
            []
        ]
        self.tokens = [
            [],
            [],
            [],
            [],
            []
        ]
        self.generate_random_board(free_space)

    def generate_random_board(self, free_space):
        seen_numbers = []
        for row in range(5):
            for column in range(5):
                random_num = None
                while random_num in seen_numbers or random_num is None:
                    random_num = random.randint(1,15)+(column*15)
                seen_numbers.append(random_num)
                self.board[row].append(random_num)
                self.tokens[row].append(False)

        if free_space:
            self.board[2][2] = 0
            self.tokens[2][2] = True

    def print_board(self):
        printing_board = [
            [],
            [],
            [],
            [],
            []
        ]

        for row in range(5):
            for column in range(5):
                printing_board[row].append("XX" if self.tokens[row][column] else str(self.board[row][column]).zfill(2))

            printing_board[row] = " ".join(printing_board[row])

        printing_board.insert(0, " ".join(["B ", "I ", "N ", "G ", "O "]))

        return printing_board

    def check_square(self, num):
        for row in range(5):
            for column in range(5):
                if self.board[row][column] == num:
                    self.tokens[row][column] = True

    def check_bingo(self, diagonals):
        for row in range(5):
            if False not in self.tokens[row]:
                return self.board[row]

        for column in range(5):
            false_yet = False
            for row in range(5):
                if not self.tokens[row][column]:
                    false_yet = True

            if not false_yet:
                return [self.board[0][column], self.board[1][column], self.board[2][column], self.board[3][column], self.board[4][column]]

        if diagonals:
            for diagonal in range(2):
                false_yet = False
                temp = []
                for row in range(0,5):
                    if diagonal == 0:
                        my_range = range(0,5)
                    else:
                        my_range = tuple(reversed(range(0,5)))

                    temp.append(self.board[row][my_range[row]])
                    if not self.tokens[row][my_range[row]]:
                        false_yet = True

                if not false_yet:
                    return temp

        return False


bingo_boards = []
for i in range(AMT_OF_BOARDS):
    bingo_boards.append(Board(FREE_SPACE))


def print_boards():
    boards_to_print = []
    for board in bingo_boards:
        boards_to_print.append(board.print_board())

    for row in range(6):
        for board in boards_to_print:
            print(board[row], end="           ")
        print()


def check_space(number_to_check):
    number_to_check = str(number_to_check)
    if number_to_check[0] not in "1234567890":
        number_to_check = number_to_check[1:]

    number_to_check = int(number_to_check)

    for board in bingo_boards:
        board.check_square(number_to_check)


def check_bingo():
    for board in bingo_boards:
        bingo_result = board.check_bingo(DIAGONALS)
        if bingo_result:
            for i in range(len(bingo_result)):
                bingo_result[i] = get_letter(bingo_result[i])

            print("BINGO! The numbers are " + ", ".join(bingo_result))


def get_letter(bingo_number):
    if bingo_number == 0:
        return "Free Space"
    else:
        if str(bingo_number).isdigit():
            return ["B", "I", "N", "G", "O"][int(math.ceil(bingo_number/15)-1)] + str(bingo_number)
        else:
            return bingo_number # If it's not a number, return it


if __name__ == "__main__":
    numbers = []
    while True:
        print()
        print("Numbers so far: " + ", ".join(numbers))
        print_boards()

        check_bingo()
        number = ""
        while not str(number).isdigit() and not (str(str(number)[1:]).isdigit() if len(str(number)) >= 2 else False):
            number = input("What number was called? >>> ")
        numbers.append(number)
        check_space(number)
