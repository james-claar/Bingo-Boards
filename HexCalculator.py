"""
Calculates properties of large hexagons made out of smaller hexagons called HexTiles in this program.

"""

import math
import sys


def add_commas(number):
    if number < 0:
        return '-' + add_commas(-number)
    result = ''
    while number >= 1000:
        number, r = divmod(number, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (number, result)


def omit_commas(number):
    try:
        number = str(number)
    except ValueError:
        sys.exit("\nVALUE ERROR\nThe value entered is not a number.")
    except number is None:
        sys.exit("\nEMPTY NUMBER ERROR\nYou need to enter a value.")
    return int(number.replace(",", ""))

# This is for hexagons made of certain units.


print("What do you want to enter about your hexagon?\nA. Length of its sides\nB. Its radius(including the center)"
      "\nC. Its diameter\nD. Its circumference\nE. Its area")
decision = None
while decision not in ["a", "b", "c", "d", "e"]:
    decision = input("You choose ")
    decision = decision.lower()
if decision == "a":
    try:
        side_length = omit_commas(input("How long are the sides of the hexagon?: "))
    except ValueError:
        sys.exit("\nVALUE ERROR\nThe value entered is not a number.")
elif decision == "b":
    try:
        side_length = omit_commas(input("How much is the radius?: "))
    except ValueError:
        sys.exit("\nVALUE ERROR\nThe value entered is not a number.")
elif decision == "c":
    diameter = omit_commas(input("How much is the diameter?: "))
    side_length = (diameter + 1) / 2
    if diameter % 2 == 0:
        sys.exit("\nUNEQUAL HEXAGON SIDE ERROR\nDiameter must be odd, found it even.")
elif decision == "d":
    circumference = omit_commas(input("How much is the circumference?: "))
    side_length = circumference / 6 + 1
    if circumference % 6 != 0:
        sys.exit("\nUNEQUAL HEXAGON SIDE ERROR\nCircumference must be a multiple of 6")
elif decision == "e":
    try:
        side_length = (omit_commas(input("How many HexTiles are in the hexagon?: ")))
    except ValueError:
        sys.exit("\nVALUE ERROR\nThe value entered is not a number.")
    counter_amount = 1
    counter = 0
    while counter_amount < side_length:
        counter += 1
        counter_amount += counter * 6
    if counter_amount > side_length:
        sys.exit("\nUNEQUAL HEXAGON SIDE ERROR\nYour hexagon is unequal at the sides, or not a hexagon at all.")
    else:
        side_length = counter + 1
else:
    if decision == "":
        sys.exit("\nEMPTY STRING ERROR\nYou must enter a value.")
    else:
        sys.exit("\nINCOMPATIBLE ERROR\nValue entered is not compatible.")
print("")
triangle = sum(range(int(side_length)))
answer = (triangle * 6) + 1
if decision != "a":
    print("Length of sides = " + str(add_commas(side_length)))
if decision != "b":
    print("Radius = " + str(add_commas(side_length)))
if decision != "c":
    print("Diameter = " + str(add_commas(side_length * 2 - 1)))
if decision != "d":
    print("Circumference = " + str(add_commas((side_length - 1) * 6)))
if decision != "e":
    print("Area = " + str(add_commas(answer)))
print("")
print("1/6 of hexagon(excluding center HexTile): " + str(add_commas(triangle)))
print("1/3 or 2/6 of hexagon(excluding center HexTile): " + str(add_commas(triangle * 2)))
print("1/2 or 3/6 of hexagon(excluding center HexTile): " + str(add_commas(triangle * 3)))
print("2/3 or 4/6 of hexagon(excluding center HexTile): " + str(add_commas(triangle * 4)))
print("5/6 of hexagon(excluding center HexTile): " + str(add_commas(triangle * 5)))
print("Full hexagon(excluding center HexTile): " + str(add_commas(triangle * 6)))
try:
    how_much_do_you_have = int(omit_commas(input("How many HexTiles do you have?: ")))
    if how_much_do_you_have is None:
        sys.exit("\nEMPTY NUMBER ERROR\nYou must enter a value.")
except ValueError:
    sys.exit("\nVALUE ERROR\nThe value entered was not a number.")

if math.floor(how_much_do_you_have % answer) != 1 and math.floor(((how_much_do_you_have % answer) - answer) * -1) != 1:
    print("\nThat would make " + str(add_commas(int(math.floor(how_much_do_you_have / answer)))) + " of these hexagons"
          " and you would have " + str(add_commas(int(math.floor(how_much_do_you_have % answer)))) + " HexTiles left."
          "\nYou would need " + str(add_commas(int(math.floor(((how_much_do_you_have % answer) - answer) * -1)))) +
          " more HexTiles to make 1 more hexagon.")
elif math.floor(how_much_do_you_have % answer) == 1 and math.floor(((how_much_do_you_have % answer) - answer) * -1) != 1:
    print("\nThat would make " + str(add_commas(int(math.floor(how_much_do_you_have / answer)))) + " of these hexagons"
          " and you would have 1 HexTile left."
          "\nYou would need " + str(add_commas(int(math.floor(((how_much_do_you_have % answer) - answer) * -1)))) +
          " more HexTiles to make 1 more hexagon.")
elif math.floor(how_much_do_you_have % answer) != 1 and math.floor(((how_much_do_you_have % answer) - answer) * -1) == 1:
    print("\nThat would make " + str(add_commas(int(math.floor(how_much_do_you_have / answer)))) + " of these hexagons"
          " and you would have " + str(add_commas(int(math.floor(how_much_do_you_have % answer)))) + " HexTiles left."
          "\nYou would need 1 more HexTile to make 1 more hexagon.")
elif math.floor(how_much_do_you_have % answer) == 1 and math.floor(((how_much_do_you_have % answer) - answer) * -1) == 1:
    print("\nThat would make " + str(add_commas(int(math.floor(how_much_do_you_have / answer)))) + " of these hexagons"
          " and you would have 1 HexTile left."
          "\nYou would need 1 more HexTile to make 1 more hexagon.")
else:
    sys.exit("\nVERIFICATION ERROR\nWhen checking for ones, found invalid syntax.")
i = 0
already_said = 0
divisible_by = []
for i in range(int(math.ceil(answer / 2))):
    if i != 0 and i != 1 and i != answer:
        if answer % i == 0:
            if already_said == 0:
                print("\nYour hexagon(" + str(add_commas(answer)) + " HexTiles) can be divided by "
                      "" + str(add_commas(i)) + " to get " + str(add_commas(answer / i)) + ".")
                divisible_by.append(i)
                already_said = 1
            elif not answer / i in divisible_by:
                print("The hexagon(" + str(add_commas(answer)) + " HexTiles) is also divisible "
                      "by " + str(add_commas(i)) + " to get " + str(add_commas(answer / i)) + ".")
if already_said == 0:
    print("\nThe hexagon(" + str(add_commas(answer)) + " HexTiles) is only divisible by 1 and itself("
          "" + str(add_commas(answer)) + ").")

# Diagrams
"""
     █ █ █ █ ▒
    ▒ █ █ █ ▒ ▒
   ▒ ▒ █ █ ▒ ▒ ▒
  ▒ ▒ ▒ █ ▒ ▒ ▒ ▒
 ▒ ▒ ▒ ▒ C █ █ █ █ ◄ User inputs 5 for the length.
  █ █ █ █ ▒ █ █ █ ◄ Range gets '0, 1, 2, 3, 4'.
   █ █ █ ▒ ▒ █ █ ◄ Sum adds them up to get the number of HexTiles in this triangle.
    █ █ ▒ ▒ ▒ █ ◄ Multiply by six to get hexagon and add 1 for the center.
     █ ▒ ▒ ▒ ▒

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
All of the below are sent up to length of sides to be processed

     ▒ ▒ ▒ ▒ ▒
    ▒ ▒ ▒ ▒ ▒ ▒
   ▒ ▒ ▒ ▒ ▒ ▒ ▒
  ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒
 ▒ ▒ ▒ ▒ █ █ █ █ █ ◄ User inputs 5 for radius.
  ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ◄ Since with all equal hexagons, radius = side length, so radius is unchanged.
   ▒ ▒ ▒ ▒ ▒ ▒ ▒
    ▒ ▒ ▒ ▒ ▒ ▒
     ▒ ▒ ▒ ▒ ▒



     █ █ █ █ █
    █ ▒ ▒ ▒ ▒ █
   █ ▒ ▒ ▒ ▒ ▒ █
  █ ▒ ▒ ▒ ▒ ▒ ▒ █
 █ ▒ ▒ ▒ C ▒ ▒ ▒ █ ◄ User inputs 24 for the circumference.
  █ ▒ ▒ ▒ ▒ ▒ ▒ █ ◄ Program gets length of sides by dividing by six and then adding 1.
   █ ▒ ▒ ▒ ▒ ▒ █ ◄ Checks circumference for unequal side errors.
    █ ▒ ▒ ▒ ▒ █
     █ █ █ █ █



     ▒ ▒ ▒ ▒ █
    ▒ ▒ ▒ ▒ █ ▒
   ▒ ▒ ▒ ▒ █ ▒ ▒
  ▒ ▒ ▒ ▒ █ ▒ ▒ ▒
 ▒ ▒ ▒ ▒ C ▒ ▒ ▒ ▒ ◄ User inputs 9 for the diameter.
  ▒ ▒ ▒ █ ▒ ▒ ▒ ▒ ◄ Checks diameter for unequal side errors.
   ▒ ▒ █ ▒ ▒ ▒ ▒ ◄ Adds 1.
    ▒ █ ▒ ▒ ▒ ▒ ◄ Divides by 2 to get radius which is equal to side length.
     █ ▒ ▒ ▒ ▒



     ▒ ▒ ▒ ▒ ▒
    ▒ █ █ █ █ ▒
   ▒ █ ▒ ▒ ▒ █ ▒
  ▒ █ ▒ █ █ ▒ █ ▒
 ▒ █ ▒ █ C █ ▒ █ ▒ ◄ User inputs 61 for the area.
  ▒ █ ▒ █ █ ▒ █ ▒ ◄ Adds 1 for the center.
   ▒ █ ▒ ▒ ▒ █ ▒ ◄ Loop keeps adding imaginary rings around the center until it equals the area.
    ▒ █ █ █ █ ▒ ◄ The side length is the amount of rings added to the center plus 1.
     ▒ ▒ ▒ ▒ ▒ ◄ If the area the rings create is more than the area in the input, trigger an unequal side error.
"""
