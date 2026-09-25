# Bulls and Cows
# Bull: correct digit in the correct position.
# Cow: correct digit in a different position.
# For the basic version, assume each guess has four different digits.

secret = "4271"

print("Guess the four-digit code.")

while True:
    guess = input("Your guess: ")

    bulls = 0
    cows = 0

    for i in range(4):
        # If guess[i] matches secret[i], add one bull.
        # Otherwise, if guess[i] is in secret, add one cow.
        # Use if / elif so a digit is not counted twice.
        pass

    # Print the number of bulls and cows.

    # If there are four bulls, print a winning message and break the loop.

# Try 1234: 1 bull, 2 cows. Try 4271: 4 bulls, 0 cows; game ends.

# Optional extensions:
# - Reject guesses whose length is not four.
# - Accept only digits 0-9.
# - Reject repeated digits.
#   Check these before the for loop; use continue to ask again if invalid.
# - Let the player enter q to quit.
# - Count guesses or set an attempt limit.
# - Generate a random secret with four different digits.
