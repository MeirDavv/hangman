import random
#import constant variables
import constant


# List of potential secret words
word_list = ["python", "hangman", "programming", "challenge"]
# Select a random word from the secret words
secret_word = random.choice(word_list)
correct_guesses = set()
incorrect_guesses = set()
attempts_left = constant.ATTEMPTS

# Function to display the current game state
def display_game_state():
    #Display the secret word with guessed letters revealed
    displayed_word = "".join([letter if letter in correct_guesses else "_" for letter in secret_word])
    print(f"word: {displayed_word}")
    print(f"incorrect Guesses: {' '.join(incorrect_guesses)}")
    print(f"Attempts Left: {attempts_left}")

# Main game loop
while True:
    display_game_state()
    guess = input("Enter your guess: ").lower()

    # Check if the guess is in the secret word
    if guess in secret_word:
        correct_guesses.add(guess)
        # Check for win condition
        if set(secret_word).issubset(correct_guesses):
            print("Congratulations! Youv'e guessed the word!")
            break
    else:
        incorrect_guesses.add(guess)
        attempts_left -= 1
        #Check for lose condition
        if attempts_left == 0:
            print("Game Over! Youv'e run out of attempts.")
            print(f"The word is {secret_word}")
            break