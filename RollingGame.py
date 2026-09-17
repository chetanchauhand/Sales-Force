#Dic Rolling Game:

import random

while True:
    choice = input("Roll the dice? (y/n): ")

    if choice.lower() == "y":
        dice = random.randint(1, 6)
        print("You got:", dice)

    elif choice.lower() == "n":
        print("Game Over!")
        break

    else:
        print("Please enter y or n")