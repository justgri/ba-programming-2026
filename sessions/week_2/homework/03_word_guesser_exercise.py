# Word Guesser
# Reveal the word by guessing letters. Six incorrect guesses end the game.
# For the basic version, assume each entry is a new lowercase letter.

import random

words = ["lecture", "library", "seminar", "campus", "zurich"]
secret = random.choice(words)  # Use "tram" while testing.
guessed = ""
mistakes = 0

print("Word:", "_" * len(secret))

while mistakes < 6:
    letter = input("Your letter: ")

    # Add letter to guessed.

    if letter not in secret:
        # Increase mistakes by one.
        pass

    visible = ""
    for character in secret:
        if character in guessed:
            # Add character to visible.
            pass
        else:
            # Add an underscore to visible.
            pass

    print("Word:", visible)
    print("Mistakes left:", 6 - mistakes)

    if visible == secret:
        # Print a winning message and break the loop.
        pass

if mistakes == 6:
    print("The word was:", secret)

# With secret = "tram", try t, r, a, m: the word should be revealed.
# Try six different letters absent from the word: the game should end.

# Optional extensions:
# - Reject entries that are not a single letter.
# - Skip letters already guessed without counting another mistake.
# - Convert uppercase input to lowercase and strip outer spaces.
# - Let the player enter /stop to quit.
