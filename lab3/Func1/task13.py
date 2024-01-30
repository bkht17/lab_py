import random
def guessnum():
    print("Hello! What is your name?")
    name = str(input())
    print(f"Well, {name}, I am thinking of a number between 1 and 20. \nTake a guess.")

    count = 0
    number = int(random.random() * 20)
    print(number)

    while True:
        count += 1
        guess = int(input())

        if guess == number:
            print(f"Good job, {name}! You guessed my number in {count} guesses!")
            break
        else:
            print("Your guess is too low.\nTake a guess.")
            continue

guessnum()

