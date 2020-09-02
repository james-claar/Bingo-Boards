"""
This is a (rather inefficient) program designed to test a theory in an old book (1990's) that explained the rate computers could process punch-cards. According to this program, they can be processed much faster than 30 min today, even inefficiently.

"""
from datetime import datetime
import random
import sys

total_number_of_problems = 20000000
number_of_problems = int(total_number_of_problems / 200000)
amount_of_prices = 30
pass_amount_min = 20  # Will pass the test if pass_amount_min
fail_amount_max = 21  # is true and fail_amount_max is false


first_total_end_time = datetime.now() - datetime.now()
total_end_time = datetime.now() - datetime.now()
people_that_passed = 0

problems = []
finished_problems = []


def print_health_bar(height, width, health, max_health):
    start_character = "["
    end_character = "]"
    none_character = " "
    used_character = "#"
    facing = "Best Display"

    if facing == "Best Display":
        if height >= width:
            facing = "Vertical"
        else:
            facing = "Horizontal"
    elif facing == "Random":
        if random.randint(1, 2) == 1:
            facing = "Vertical"
        else:
            facing = "Horizontal"

    if facing == "Vertical":
        for b in range(height):
            health_percentage = float(health) / float(max_health) * 100
            filled_rows = int(health_percentage * height / 100)
            li = [start_character]
            if height - b <= filled_rows:
                for x in range(width):
                    li.append(used_character)
            else:
                for x in range(width):
                    li.append(none_character)
            li.append(end_character)
            print("".join(li))

    elif facing == "Horizontal":
        for b in range(height):
            health_percentage = float(health) / float(max_health) * 100
            filled_rows = int(health_percentage * width / 100)
            li = [start_character]
            for x in range(width):
                if x + 1 <= filled_rows:
                    li.append(used_character)
                else:
                    li.append(none_character)
            li.append(end_character)
            print("".join(li))
    else:
        sys.exit(
            "\nVALIDATION ERROR\nVariable facing must be \"Vertical\", \"Horizontal\", \"Best Display\", or \"Random\""
            ".\nChecking is case sensitive.")


def setup_lists():
    global problems
    i = 0
    while i < number_of_problems:
        temporary_problem = []
        rand = random.randint(1, amount_of_prices)
        for j in range(amount_of_prices):
            if j >= rand:
                temporary_problem.append(0)
            else:
                temporary_problem.append(1)
        problems.append(temporary_problem)
        i += 1


def figure_problems():
    global problems
    global finished_problems
    global people_that_passed
    # Generate list of values
    for i in reversed(range(number_of_problems)):
        problem_solver_list = problems[i]
        problem_solver_var = 0
        for j in range(amount_of_prices):
            if problem_solver_list[j]:
                problem_solver_var += 1

        finished_problems.append(problem_solver_var)
    # Find out how many people spent more than a certain amount
    for k in range(number_of_problems):
        if pass_amount_min <= finished_problems[k] < fail_amount_max:
            people_that_passed += 1

print("Randomizing and computing. This may take a while.")
program_start_time = datetime.now()

for problem in range(int(total_number_of_problems/number_of_problems)):
    if problem % 1000 == 0:
        print(problem)
    first_start_time = datetime.now()

    setup_lists()

    first_end_time = datetime.now() - first_start_time
    start_time = datetime.now()

    figure_problems()

    end_time = datetime.now() - start_time

    first_total_end_time += first_end_time
    total_end_time += end_time

program_end_time = datetime.now() - program_start_time
print("RESULTS")
print("The lists took " + str(first_total_end_time) + " to randomize.")
print("It took " + str(total_end_time) + " to compute, and " + str(people_that_passed) + "/" + str(total_number_of_problems) + " people spent between $" + str(pass_amount_min * 100) + " and $" + str(fail_amount_max * 100) + " on their automobiles.")
print("The entire program took " + str(program_end_time) + " to complete.")