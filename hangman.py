import random
import string


def display(misses):
    hangman_dict = {0: "O", 1: "|", 2: "/", 3: "\\", 4: "/", 5: "\\"}
    game_dict = {0: " ", 1: " ", 2: " ", 3: " ", 4: " ", 5: " "}
    if misses:
        for i in range(len(misses)):
            game_dict[i] = hangman_dict[i]
    print """
 _____
 |  \|
 %s   |
%s%s%s  |
%s %s  |
     |
 ======
""" % (game_dict[0], game_dict[2], game_dict[1], game_dict[3], game_dict[4], game_dict[5])
    print "MISSES:",
    for letter in misses:
        print letter,
    print "\n" * 2


def random_word():
    choice = random.randint(0,608324) # 608325 is the number of lines in wordlist.txt
    with open("wordlist.txt") as raw_words:
        raw_lines = raw_words.readlines()
        word = raw_lines[choice].strip("\n")
    return word


def choose_word(difficulty):
    choosing = True
    while choosing:
        word = random_word()
        if difficulty == "hard" and len(word) <= 5 and "'" not in word:
            break
        elif difficulty == "easy" and len(word) > 5 and "'" not in word:
            break
    return word


def valid(guess, misses):
    if guess not in string.ascii_letters:
        print "Guess again! Must be a letter."
        return False
    if guess in misses:
        "You've already guessed that!"
        return False
    else:
        return True


def hangman(difficulty):
    print "WELCOME TO HANGMAN!"
    print
    raw_word = choose_word(difficulty).upper()
    word = list(raw_word)
    display_word = []
    for i in word:
        if i in string.punctuation:
            display_word.append(i)
        else:
            display_word.append("_")
    misses = []
    while True:
        for letter in display_word:
            print letter,
        print
        display(misses)
        while True:
            guess = (raw_input("What letter to guess? ")).upper()
            print
            if valid(guess, misses):
                break
        if guess in word:
            for i in range(len(word)):
                if word[i] == guess:
                    display_word[i] = guess
        else:
            misses.append(guess)
        if display_word == word:
            print
            for letter in display_word:
                print letter,
            print "\n\nCongratulations! You win!\n"
            winner = "player"
            break
        if len(misses) == 6:
            print "\nUh-oh. That was your last chance. The word was %s!\n" % raw_word
            display(misses)
            print
            winner = "computer"
            break
    return winner


def main():
    print "#" * 30
    print "#" + " " * 28 + "#"
    print "#" + "PYTHON HANGMAN!!".center(28) + "#"
    print "#" + " " * 28 + "#"
    print "#" * 30
    win_dict = {"player": 0, "computer":0}
    keep_going = True
    while keep_going:
        print
        print "1. Easy Hangman (longer words)"
        print "2. Hard Hangman (shorter words)"
        print "3. Quit"
        print
        choice = raw_input("Play some hangman? ")
        print
        if choice == "1":
            win_dict[hangman("easy")] += 1
        elif choice == "2":
            win_dict[hangman("hard")] += 1
        else:
            print "Thanks for playing!"
            print "The player won %i times. The computer won %i times." % (win_dict["player"], win_dict["computer"])
            keep_going = False


if __name__ == "__main__":
    main()
