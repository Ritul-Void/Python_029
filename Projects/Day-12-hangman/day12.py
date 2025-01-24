import random

# Function to check if a character is a valid lowercase letter
def is_valid_guess(guess):
    return guess.isalpha() and guess.islower() and len(guess) == 1

# Function to display the current state of the word with placeholders for unguessed letters
def display_word(secret_word, guessed):
    for letter in secret_word:
        if letter in guessed:
            print(letter, end=" ")
        else:
            print("_", end=" ")
    print()

# Function to generate a random word from a file
def get_random_word_from_file(filename):
    with open(filename, "r") as file:
        words = file.readlines()
        return random.choice(words).strip().lower()

def main():
    secret_word = get_random_word_from_file("words.txt")
    guessed = set()
    max_attempts = 6
    attempts = 0

    print("Welcome to Hangman!")
    print("Try to guess the word!")

    while attempts < max_attempts:
        print("Word:", end=" ")
        display_word(secret_word, guessed)

        guess = input("Guess a letter: ").lower()

        if not is_valid_guess(guess):
            print("Invalid guess. Please enter a lowercase letter.")
            continue

        if guess in guessed:
            print("You've already guessed that letter.")
            continue

        guessed.add(guess)

        if guess not in secret_word:
            attempts += 1
            print("Incorrect guess. Attempts remaining:", max_attempts - attempts)
        elif all(letter in guessed for letter in secret_word):
            print("Congratulations! You've guessed the word:", secret_word)
            break

    if attempts == max_attempts:
        print("Sorry, you've run out of attempts. The word was:", secret_word)

    play_again = input("Do you want to play again? (Y/N): ").lower()
    if play_again == 'y':
        main()
    else:
        print("Thanks for playing!")

if __name__ == "__main__":
    main()