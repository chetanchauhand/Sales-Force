#Number Guessing Game 

import random

number = random.randint(1, 100)

print("Guess the number between 1 and 100")

while True:
    guess = int(input("Enter your guess: "))

    if guess < number:
        print("Too Low! ")
    
    elif guess > number:
        print("Too High! ")

    else:
        print(" Correct! You won!")
        break