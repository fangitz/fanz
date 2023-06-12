import random

LEXICON_FILE = "files\Lexicon.txt"    # File to read word list from
INITIAL_GUESSES = 8             # Max number of guesses per game


def play_game(secret_word):
    dash = ""
    count = INITIAL_GUESSES
    print(secret_word)
    
    for i in range(len(secret_word)):   #print dashes representing the word characters
        dash += "-"
    print("The word now looks like this:", dash, '\n'"You have", count, "guess left")
    
    while count > 0:
        ch = input("Type a single letter here, then press enter:")
        ch = ch.upper()
        if ch == "" or len(ch) > 1:     #if no charactor or more than 1 characters are input
            print("Guess should only be a single character"'\n'"The word now looks like this:", dash)
            print("You have", count, "guess left")
        elif ch in secret_word:     #character is in the word
            for i in range(len(secret_word)):
                if ch == secret_word[i]:
                    dash = dash[0:i] + ch + dash[i+1:len(secret_word)]
            if dash == secret_word:     #if the guessed word is same as the secret word
                print("Congratulations, the word is:", dash)
                break
            else:
                print("That guess is correct."'\n'"The word now looks like this:", dash)
                print("You have", count, "guess left")
        else:   #if the input is not within the word
            count -= 1
            print("There are no " + ch + "'s in the word")
            if count == 0:
                print("Sorry, you lost. The secret word was:", secret_word)
            else:
                print("The word now looks like this:", dash)
                print("You have", count, "guess left")
                
                
def get_word():
    """
    This function returns a secret word that the player is trying
    to guess in the game.  This function initially has a very small
    list of words that it can select from to make it easier for you
    to write and debug the main game playing program.  In Part II of
    writing this program, you will re-implement this function to
    select a word from a much larger list by reading a list of words
    from the file specified by the constant LEXICON_FILE.
    """
    
    lines=[]
    with open(LEXICON_FILE) as file:
        for line in file: 
            line = line.strip()
            lines.append(line)
    i= random.randint(0, len(lines))
    secret_word = lines[i]
    return secret_word

def main():
    """
    To play the game, we first select the secret word for the
    player to guess and then play the game using that secret word.
    """
    secret_word = get_word()
    play_game(secret_word)


# This provided line is required at the end of a Python file
# to call the main() function.
if __name__ == "__main__":
    main()