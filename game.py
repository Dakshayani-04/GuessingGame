import random
import time
import os
import sys

# File to store scores
SCORE_FILE = "scores.txt"

# Color codes
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    END = "\033[0m"

# Animated thinking dots
def thinking_animation():
    print(Colors.MAGENTA + "🤔 Thinking of a number", end="")
    for _ in range(5):
        print(".", end="")
        sys.stdout.flush()
        time.sleep(0.5)
    print(Colors.END)

def welcome():
    print(Colors.CYAN + """
***************************************
   🎮 Welcome to the Number Guessing Game App 🎮
***************************************
    """ + Colors.END)

def choose_level():
    print("Choose a difficulty level:")
    print("1. Easy (1-10, 5 guesses)")
    print("2. Medium (1-50, 7 guesses)")
    print("3. Hard (1-100, 10 guesses)")
    
    while True:
        level = input("Enter 1, 2, or 3: ")
        if level in ['1', '2', '3']:
            return int(level)
        else:
            print(Colors.RED + "Invalid choice. Try again." + Colors.END)

def set_game_parameters(level):
    if level == 1:
        return 10, 5
    elif level == 2:
        return 50, 7
    else:
        return 100, 10

def give_hint(guess, number):
    if guess < number:
        print(Colors.YELLOW + "⬆️ Go higher!" + Colors.END)
    elif guess > number:
        print(Colors.YELLOW + "⬇️ Go lower!" + Colors.END)

def save_score(player_name, attempts):
    scores = []
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as file:
            for line in file:
                name, score = line.strip().split(",")
                scores.append((name, int(score)))
    scores.append((player_name, attempts))
    scores.sort(key=lambda x: x[1])
    with open(SCORE_FILE, "w") as file:
        for name, score in scores[:5]:
            file.write(f"{name},{score}\n")

def show_leaderboard():
    print(Colors.CYAN + "\n🏆 Leaderboard 🏆" + Colors.END)
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as file:
            for idx, line in enumerate(file, 1):
                name, score = line.strip().split(",")
                print(f"{idx}. {name} - {score} attempts")
    else:
        print("No scores yet. Be the first to play!")

def play_game():
    welcome()
    player_name = input("Enter your name: ")
    
    while True:
        level = choose_level()
        max_number, max_attempts = set_game_parameters(level)

        thinking_animation()
        number = random.randint(1, max_number)

        print(f"\n{Colors.CYAN}I have chosen a number between 1 and {max_number}.")
        print(f"You have {max_attempts} attempts to guess it.{Colors.END}\n")

        attempts = 0
        while attempts < max_attempts:
            guess = input(f"Attempt {attempts+1}: Enter your guess: ")

            if not guess.isdigit():
                print(Colors.RED + "⚠️ Please enter a valid number." + Colors.END)
                continue

            guess = int(guess)
            attempts += 1

            if guess == number:
                print(Colors.GREEN + f"""
🎉🎉 Congratulations {player_name}! 🎉🎉
You guessed the number {number} in {attempts} attempts!
                """ + Colors.END)
                save_score(player_name, attempts)
                break
            else:
                give_hint(guess, number)
                print(Colors.MAGENTA + "💡 Keep trying! 💡\n" + Colors.END)
        else:
            print(Colors.RED + f"""
😢 Game Over! 😢
The number was {number}. Better luck next time!
            """ + Colors.END)

        show_leaderboard()

        choice = input("\nDo you want to play again? (yes/no): ").lower()
        if choice != "yes":
            print(Colors.CYAN + "\nThanks for playing! 👋 See you next time!" + Colors.END)
            break

if __name__ == "__main__":
    play_game()
