# Bulls and cows

# store secret word
secret = "1234"

# iterate through 4 digits
continue_game = True

while continue_game:
    bulls = 0
    cows = 0

    # prompt user to enter the number
    guess = input("Guess your number: ")

    # iterate through 4 digits
    for i in range(4):

        # if digit matches at exact position
        if guess[i] == secret[i]:
            bulls += 1

        # if digit elsewhere, not exact position
        elif guess[i] in secret:
            cows += 1

    print(f"Bulls: {bulls}, cows: {cows}")

    if bulls == 4:
        print("Great, you're the best!")
        continue_game = False
    else:
        print("Try again!")
