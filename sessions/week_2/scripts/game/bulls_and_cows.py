secret = "4271"

print("Welcome to Bulls and Cows!")
print("Guess the 4-digit number.")

while True:

    guess = input("Your guess: ")

    bulls = 0
    cows = 0

    for i in range(4):

        if guess[i] == secret[i]:
            bulls = bulls + 1

        elif guess[i] in secret:
            cows = cows + 1

    print("Bulls:", bulls)
    print("Cows:", cows)

    if bulls == 4:
        print("You win!")
        break
