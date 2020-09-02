"""
Humorous turn-based battle game I made as a project.

"""

import time
import random
import sys

MAX_TURNS_PER_PLAYER=15

class NewPlayer:
    def __init__(self):
        self.max_health = 0
        self.health = 0
        self.autochoose = ""
        self.name = ""
        self.accuracy = 0
        self.kits = 0
        self.choices = []
        self.status_effects = {}


    def config_autochoose(self):
        self.autochoose = input("AutoChoose Configuration: What do you want to keep choosing? It is ")
        self.choose_turn()


    def shoot(self, shot_at, bullet_type):
        print(self.name + " shoots at " + shot_at.name)
        time.sleep(sleep_time)
        if random.randint(0, 100) <= self.accuracy:
            print("The shot is a hit!")
            if bullet_type == "normal":
                damage = random.randint(15, 30)
                waiting_effect = False
            elif bullet_type == "poison":
                damage = 5
                waiting_effect = "poison"
            elif bullet_type == "THE BULLET OF UNSAID AND TRUE AND ULTIMATE POWER... Stuff...":
                damage = 1
                waiting_effect = False
            else:
                damage = 0
                waiting_effect = False
            shot_at.health -= damage
            if waiting_effect:
                shot_at.add_status_effect(waiting_effect, 3)
        else:
            print("The shot is a miss.")
            damage = 0
        time.sleep(sleep_time)
        if shot_at.health < 0:
            shot_at.health = 0
        print(shot_at.name + " takes " + str(damage) + " damage and has " + str(shot_at.health) + " health left.")
        check_player_death(shot_at)


    def use_kit(self):
        if self.kits > 0:
            self.health += 45
            self.kits -= 1
            print(self.name + " uses a first aid kit and gains 45 health.")
            time.sleep(sleep_time)
            print(self.name + " has " + str(self.health) + " health.")
        else:
            print("You do not have enough kits!")
            time.sleep(sleep_time)
            print("Since it takes time sitting around searching your pack for one, it is now the next player's turn.")


    def choose_turn(self):

        print(self.name + "'s turn.")

        if self.health > 0:
            choice = None
            if self.autochoose:
                choice = self.autochoose
            time.sleep(sleep_time)
            print("")
            if "a" in self.choices:
                print("A.) Shoot: fires your gun at someone.")
            if "b" in self.choices:
                print("B.) First Aid: Heals you. Keep in mind it can only be used once.")
            if "c" in self.choices:
                print("C.) Wait: Skips your turn.")
            if "d" in self.choices:
                print("D.) AutoChoose: Keeps choosing a certain choice.")
            if "e" in self.choices:
                print("E.) Run away: Notice an opponent's bazooka, try to get away, and get blown up.")
            while choice not in self.choices:
                choice = input("You would like to: ").lower()
            
            print("\n")
            if choice == "a":
                print(self.name + " has decided to fire a gun.\n")
                time.sleep(sleep_time)
                playernames = []
                for player in players:
                    playernames.append(player.name)
                print("Players are " + str(playernames).translate(str.maketrans(dict.fromkeys("[]'"))) + ".")
                who_to_shoot = str(input("Shoot at what player? "))
                print("Bullet types are " + str(all_bullet_types).translate(str.maketrans(dict.fromkeys("[]'"))) + ".")
                shoot_type = str(input("What type of bullet do you want to shoot? "))
                if who_to_shoot.isdigit():
                    who_to_shoot = int(who_to_shoot) - 1
                else:
                    who_to_shoot = who_to_shoot.lower()
                    for player in players:
                        if who_to_shoot == player.name.lower():
                            who_to_shoot = int(player.id)
                if shoot_type.isdigit():
                    shoot_type = all_bullet_types[int(shoot_type) - 1]

                self.shoot(players[who_to_shoot], shoot_type)
            elif choice == "b":
                print(self.name + " has decided to use a first aid kit.\n")
                time.sleep(sleep_time)
                self.use_kit()
            elif choice == "c":
                print(self.name + " has decided to wait.\n")
                time.sleep(sleep_time)
            elif choice == "d":
                print(self.name + " has decided to configure their autochoose.\n")
                time.sleep(sleep_time)
                self.choices.pop(3)
                self.config_autochoose()
            elif choice == "e":
                print(self.name + " has decided to run away.\n")
                time.sleep(sleep_time)
                self.health = 0
                print(self.name + " noticed an opponent's bazooka, got scared, tried to run away, and realized that his rear didn't have armor.")
            elif choice == "poop on the floor":
                print(self.name + " has pooped on the floor.\n")
                time.sleep(sleep_time)
                print("Mom smells the poop, tracks " + self.name + " down, and spanks " + self.name + " soundly. " + self.name + " promises not to do it again and takes 20 damage.")
                self.health -= 20
                self.add_status_effect("sore bottom", 3)
            elif choice == "eat cake":
                print(self.name + " has eaten cake.\n")
                time.sleep(sleep_time)
                print("It turns out that was dad's birthday cake. He catches " + self.name + " red-handed and gives " + self.name + " a very hard spanking. " + self.name + " promises not to do it again and takes 30 damage.")
                self.health -= 30
                self.add_status_effect("sore bottom", 5)
            else:
                print("Sorry, the selected option is not available due to in internal error.")

            if "poison" in self.status_effects:
                print(self.name + " is hurt by their poison.")
                time.sleep(sleep_time)
                print(self.name + " takes 10 damage.\n")
                self.health -= 10
                self.status_effect_used("poison")
                time.sleep(sleep_time)
            if "sore bottom" in self.status_effects:
                print(self.name + "'s bottom is sore.")
                time.sleep(sleep_time)
                print(self.name + " takes 5 damage.\n")
                self.health -= 5
                self.status_effect_used("sore bottom")
                time.sleep(sleep_time)

            check_player_death(self)
            print_all_healths()

        else:
            time.sleep(sleep_time)
            print(self.name + " cannot move because " + self.name + " is dead.")
        check_death_all()


    def add_status_effect(self, effect, turns):
        time.sleep(sleep_time)
        if effect in self.status_effects:
            print(self.name + " is already under the effect " + effect + ", so " + self.name + " is immune. However, it is lengthened to " + str(turns) + " turns.")
            self.status_effects[effect] = turns
        else:
            print(self.name + " receives the effect " + effect + " for " + str(turns) + " turns.")
            self.status_effects[effect] = turns


    def status_effect_used(self, effect):
        if self.status_effects[effect] <= 0:
            print(self.name + " is no longer under the effect " + effect + ".")
            self.status_effects.pop(effect, 0)
        else:
            self.status_effects[effect] -= 1



def print_all_healths():
    for player in players:
        print(player.name + " has " + str(player.health) + " health left.")
        print_health_bar(1, player.max_health / 5, player.health, player.max_health)


def check_player_death(player):
    if player.health <= 0:
        print(player.name + " is dead. Sorry " + player.name + "!")
        player.health = 0


def print_health_bar(height, width, health, max_health):
    start_character = "["
    end_character = "]"
    none_character = " "
    used_character = "="
    facing = "Best Display"
    height = int(round(height))
    width = int(round(width))
    health = int(round(health))
    max_health = int(round(max_health))


    if facing == "Best Display":
        if height > width:
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


def next_turn():
    global turn

    turn += 1
    if turn == len(players):
        turn = 0


def check_death_all():
    alive = []
    for player in players:
        if player.health > 0:
            alive.append(player)
    if len(alive) == 0:
        print("All players have died. Thank you for playing.\n")
        exit(0)
    elif len(alive) == 1:
        print(alive[0].name + " is the winner! Thanks for playing.\n")
        exit(0)


players = []

turn = 0
sleep_time = 1.5

all_bullet_types = ["normal", "poison"]
all_status_effects = ["poison", "sore bottom"]


def setup_game():
    global turn
    global sleep_time
    setup_complexity = None #      SETUP COMPLEXITY | N/A | y, n, super, ''
    while setup_complexity not in ["y", "n", "super", ""]:
        setup_complexity = input("Advanced game setup? y/n/''/super: ")
    if setup_complexity == "":
        setup_complexity = "n"

    amount_of_players = 0 #     AMOUNT OF PLAYERS | necessary | 2-10
    while amount_of_players < 2 or amount_of_players > 10:
        amount_of_players = int(input("How many players from 2 - 10 should there be? "))

    if setup_complexity == "n":
        setup_max_health = int(input("How much health should everyone start with? "))
        setup_kits = int(input("How many kits can everyone use? "))
        setup_accuracy = 75
    elif setup_complexity == "y":
        setup_accuracy = int(input("How much accuracy should everyone have? "))
        setup_max_health = 0
        setup_kits = 0
    elif setup_complexity == "super":
        turn = int(input("What player number should start first? ")) - 1
        sleep_time = float(input("What time should the program use for the wait between text? "))
        setup_accuracy = 0
        setup_max_health = 0
        setup_kits = 0
    else:
        sleep_time = 1.5
        turn = 0
        setup_accuracy = 0
        setup_max_health = 0
        setup_kits = 0

    for p in range(amount_of_players): #     CREATING PLAYERS WITH ATTRIBUTES | necessary | N/A
        print("\nSETTING UP PLAYER " + str(p+1))
        players.append(NewPlayer())
        players[p].id = p
        players[p].choices = ["a", "b", "c", "d", "e", "poop on the floor", "eat cake"]
            

        #NESSECARY
        players[p].name = str(input("What do you want to name player #" + str(p+1) + "? "))

        #COMPLEX
        if setup_complexity in ["y", "super"]:
            players[p].autochoose = input("Should " + players[p].name + " have an autochoose? y/n: ")
            if players[p].autochoose == "y":
                players[p].autochoose = str(input("What should " + players[p].name + "'s autochoose be? "))
            else:
                players[p].autochoose = ""
            players[p].max_health = int(input("What should be " + players[p].name + "'s max health? "))
            players[p].kits = int(input("How many kits should " + players[p].name + " start with? "))
            players[p].status_effects = str(input("Should " + players[p].name + " start with any status effects? y/n: "))
            if players[p].status_effects == "y":
                players[p].status_effects = {}
                for s in range(len(all_status_effects)):
                    status_effect_boolean = input("Should " + players[p].name + " be under the effect " + all_status_effects[s] + "? y/n: ")
                    if status_effect_boolean == "y":
                        players[p].status_effects[all_status_effects[s]] = int(input("How many turns should " + all_status_effects[s] + " last? "))
            else:
                players[p].status_effects = {}

        else:
            players[p].autochoose = ""
            players[p].max_health = setup_max_health
            players[p].kits = setup_kits
            players[p].status_effects = {}
            
        #SUPER COMPLEX
        if setup_complexity == "super":
            players[p].accuracy = int(input("How much should " + players[p].name + "'s accuracy be? "))
            players[p].health = int(input("How much health should "+ players[p].name + " start with? "))
        else:
            players[p].accuracy = setup_accuracy
            players[p].health = players[p].max_health


setup_game()

print("\n\nLet the game begin!\n\n")

for i in range(MAX_TURNS_PER_PLAYER * len(players)):
    players[turn].choose_turn()
    next_turn()

print("Because the battle lasted too long, all the surviving players got bored and ran away!.\nThanks for playing!")
