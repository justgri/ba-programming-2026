# Rock, Paper, Scissors
# Rock beats scissors; scissors beats paper; paper beats rock.
# For the basic version, assume the player enters a valid lowercase move.

import random

moves = ["rock", "paper", "scissors"]


# Complete the rules. Return "win", "draw", or "loss" for the player.
def compare_moves(player, opponent):
    if player == opponent:
        return "draw"
    elif player == "rock":
        # Win against scissors; otherwise lose.
        pass
    elif player == "paper":
        # Compare with the opponent and return the result.
        pass
    else:  # The player chose scissors.
        # Compare with the opponent and return the result.
        pass


# Uncomment these examples after completing the function:
# print(compare_moves("paper", "rock"))       # Expected: win
# print(compare_moves("rock", "paper"))       # Expected: loss
# print(compare_moves("scissors", "scissors")) # Expected: draw

# Play five rounds.
for round_number in range(1, 6):
    print("Round:", round_number)
    player = input("rock, paper, or scissors: ")
    opponent = random.choice(moves)
    print("Computer:", opponent)

    # Call compare_moves with the two moves and print the returned result.

# Optional extensions:
# - Reject entries that are not in moves; ask again without using a round.
# - Convert uppercase input to lowercase and strip outer spaces.
# - Let the player enter q to quit.
# - Count wins, draws, and losses across the five rounds.
# - Simulate 600 rounds using random choices for both players.
#   Print the totals and calculate wins / 600 * 100 as the win percentage.
