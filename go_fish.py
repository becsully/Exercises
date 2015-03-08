import random
from pprint import pprint


class Card():

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value


    def __str__(self):
        string = "%s of %s" % (self.value, self.suit)
        return string


class Deck():

    def __init__(self): #cards is a list of Card objects
        values = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
        suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
        self.cards = []
        for i in range(4):
            suit = suits[i]
            for j in range(13):
                value = values[j]
                newcard = Card(suit, value)
                self.cards.append(newcard)


    def __str__(self):
        return self.cards


    def test(self):
        self.cards = []


    def remove(self, card): #card is a Card object
        self.cards.pop(self.cards.index(card))


    def cards_in_deck(self):
        if len(self.cards) == 0:
            return False
        else:
            return True


class Player():

    def __init__(self, name, cards=None): #string, list of Card objects
        self.name = name
        if cards is None:
            self.cards = []
        else:
            self.cards = cards
        self.sets = {}
        self.guess_history = []


    def __str__(self):
        printdict = {"Cards": self.cards, "Sets": self.sets, "Guess history": self.guess_history}
        return printdict


    def print_cards(self):
        print "%s is holding %i cards. Here they are:" % (self.name, self.cardnum())
        for card in sorted(self.cards, key=lambda card: card.value):
            print "-- ",
            print card
        print ""
        if self.sets == {}:
            print "%s has not yet collected any sets." % self.name
        else:
            print "Here are the sets %s has acquired." % self.name
            for set in self.sets:
                print "--",
                if set == "Six":
                    print "Sixes"
                else:
                    print "%ss" % set


    def cardnum(self):
        return len(self.cards)


    def draw(self, deck): #deck is the current Deck object
        drawn_card = random.choice(deck.cards)
        deck.remove(drawn_card)
        self.cards.append(drawn_card)
        return drawn_card


    def remove(self, card): #card is a Card object
        self.cards.pop(self.cards.index(card))


    def valid(self, guess):
        values = []
        for card in self.cards:
            values.append(card.value)
        if guess in values:
            return True
        else:
            return False


    def taketurn(self, deck, opponent): # deck is Deck object. opponent is a Player object.
        if self.cardnum() == 0:
            if not deck.cards_in_deck():
                print "You have no cards and cannot draw. You have to pass."
                return False
            else:
                self.draw(deck)
        print ""
        print "It's %s's turn!" % self.name
        print ""
        self.print_cards()
        guess = raw_input("What's your guess? ")
        while not self.valid(guess):
            guess = raw_input("Try again, must be a card you currently have. ")
        print ""
        opponent.remember(guess)
        woncards = []
        lostcards = []
        for card in opponent.cards:
            cardcount = 0
            if card.value == guess:
                cardcount += 1
                if cardcount == 1:
                    print "Nice! %s had at least one %s. Here's what he hands over:" % (opponent.name, guess)
                self.cards.append(card)
                lostcards.append(card)
                woncards.append(card)
                print "--",
                print card
            else: pass
        for card in lostcards:
            opponent.remove(card)
        if woncards == []:
            print "Yikes! Sorry. Go fish."
            if deck.cards_in_deck():
                drawncard = self.draw(deck)
                cardname = drawncard.__str__()
                print "You drew the %s." % cardname
                if drawncard.value == guess:
                    print "What luck! You get to go again."
                    self.setcheck()
                    if self.cardnum() == 0:
                        print "You're out of cards! It's %s's turn now." % opponent.name
                        return False
                    else:
                        return True
                else:
                    print "It's the end of your turn."
                    self.setcheck()
                    return False
            else:
                print "Sorry! There are no cards left in the deck."
                return False
        else:
            self.setcheck()
            if self.cardnum() == 0:
                print "You're out of cards! It's %s's turn now." % opponent.name
                return False
            else: return True


    def setcheck(self):
        counts = {}
        for card in self.cards:
            if card.value in counts:
                counts[card.value] += 1
            else:
                counts[card.value] = 1
        cards_to_remove = []
        for value in counts:
            if counts[value] == 4:
                self.sets[value] = []
                if value == "Six":
                    print "%s has collected all four Sixes!" % self.name
                else:
                    print "%s has collected all four %ss!" % (self.name, value)
                print ""
        for card in self.cards:
            if card.value in self.sets:
                self.sets[card.value].append(card)
                cards_to_remove.append(card)
            else: pass
        for card in cards_to_remove:
            self.remove(card)


class Opponent(Player):

    def __init__(self, name, cards=None):
        Player.__init__(self, name, cards)
        self.memory = []


    def __str__(self):
        printdict = {"Cards": self.cards, "Sets": self.sets, "Guess history": self.guess_history, "Memory": self.memory}
        return printdict


    def print_cards(self):
        num = len(self.cards)
        print "%s is holding %i cards." % (self.name, num)
        print ""
        if self.sets == {}:
            print "%s has not yet collected any sets." % self.name
        else:
            print "Here are the sets %s has acquired." % self.name
            for set in self.sets:
                print "--",
                if set == "Six":
                    print "Sixes"
                else:
                    print "%ss" % set


    def guess(self):
        values = []
        for card in self.cards:
            if card.value not in values:
                values.append(card.value)
            else: pass
        if self.guess_history == []:
            return random.choice(values)
        if len(values) == 1:
            return values[0]
        guess = ""
        if self.memory[-1] in values:
            guess = self.memory[-1]
            self.memory.pop(self.memory.index(guess))
        elif len(self.memory) > 1:
            if self.memory[-2] in values:
                guess = self.memory[-2]
                self.memory.pop(self.memory.index(guess))
        if guess is not "":
            return guess
        if len(values) > 1 and len(self.guess_history) >= 1:
            if len(values) > len(self.guess_history):
                times = len(self.guess_history)
            else:
                times = len(values) - 1
            for i in range (1,times):
                bad_guess = self.guess_history[i * -1]
                if bad_guess in values:
                    values.pop(values.index(bad_guess))
            return random.choice(values)
        else:
            guess = random.choice(values)
            return guess


    def remember(self, guess): #guess is a string that is one of the card values.
        self.memory.append(guess)


    def taketurn(self, deck, opponent): # deck is Deck object. opponent is a Player object.
        if self.cardnum() == 0:
            if not deck.cards_in_deck():
                print "%s has no cards and cannot draw. He has to pass." % self.name
                return False
            else:
                self.draw(deck)
        print ""
        print "It's %s's turn!" % self.name
        print ""
        self.print_cards()
        myguess = self.guess()
        if myguess == "Six":
            print "The computer has asked if you have any Sixes."
        else:
            print "The computer has asked if you have any %ss." % myguess
        print ""
        self.guess_history.append(myguess)
        woncards = []
        lostcards = []
        for card in opponent.cards:
            count = 0
            if card.value == myguess:
                count += 1
                if count == 1:
                    print "Aha! You do!"
                self.cards.append(card)
                lostcards.append(card)
                cardname = str(card.value + " of " + card.suit)
                woncards.append(cardname)
            else: pass
        for card in lostcards:
            opponent.remove(card)
        if woncards == []:
            print "Yikes, you say! Sorry, %s. Go fish. He draws a card." % self.name
            print ""
            if deck.cards_in_deck():
                drawncard = self.draw(deck)
                if drawncard.value == myguess:
                    print "What luck! %s drew a %s!" % (self.name, myguess)
                    print ""
                    self.setcheck()
                    if self.cardnum() == 0:
                        print "%s is out of cards! It's your turn again." % self.name
                        if deck.cards_in_deck():
                            self.draw(deck)
                        return False
                    else:
                        return True
                else:
                    self.setcheck()
                    return False
            else:
                print "%s was unable to draw -- there are no cards left in the deck." % self.name
                return False
        else:
            print "You give %s these cards: " % self.name
            for card in woncards:
                print "--",
                print card
            self.setcheck()
            if self.cardnum() == 0:
                print "%s ran out of cards! It's your turn again." % self.name
                self.draw(deck)
                return False
            else:
                return True


def begin_game(player,opponent): #two strings for the names
    mydeck = Deck()
    player_list = [Player(player), Opponent(opponent)]
    for i in range(5):
        for j in range(2):
            drawingplayer = player_list[j]
            drawingplayer.draw(mydeck)
    mygame = {"Deck": mydeck, "Player": player_list[0], "Opponent": player_list[1]}
    return mygame


def gameover(mydeck, player, computer):
    if not mydeck.cards_in_deck() and player.cardnum() == 0 and computer.cardnum() == 0:
        return True
    else:
        return False


def gofish(gamedict): #takes gamedict with Deck, Player, and Opponent
    mydeck = gamedict["Deck"]
    player = gamedict["Player"]
    computer = gamedict["Opponent"]
    count = 0
    while not gameover(mydeck, player, computer):
        count += 1
        if count % 2 == 0:
            go_again = computer.taketurn(mydeck, player)
            while go_again:
                go_again = computer.taketurn(mydeck, player)
        else:
            go_again = player.taketurn(mydeck, computer)
            while go_again:
                go_again = player.taketurn(mydeck, computer)
        print "\n***\n"
        print "There are %i cards left in the deck." % len(mydeck.cards)
    print ""
    print "GAME OVER!"
    print ""
    print victor(gamedict)


def victor(gamedict):
    player1 = len(gamedict["Player"].sets)
    player2 = len(gamedict["Opponent"].sets)
    if player1 > player2:
        winner = gamedict["Player"]
        loser = gamedict["Opponent"]
    else:
        winner = gamedict["Opponent"]
        loser = gamedict["Player"]
    print "With %i sets to %i, the winner is..." % (len(winner.sets), len(loser.sets))
    print ""
    print "*" * 30
    print "*" + " " * 28 + "*"
    print "*" + (winner.name).center(28) + "*"
    print "*" + " " * 28 + "*"
    print "*" * 30


def main():
    print "#" * 40
    print "#" + " " * 38 + "#"
    print "#" + "WELCOME TO PYTHON GO FISH!".center(38) + "#"
    print "#" + " " * 38 + "#"
    print "#" * 40
    print ""
    while True:
        answer = raw_input("Play a game of Go Fish? Y/N: ")
        if answer == "Y" or answer == "y":
            name1 = raw_input("What's the Player's name? ")
            name2 = raw_input("What's the Computer's name? ")
            mygame = begin_game(name1, name2)
            print ""
            gofish(mygame)
        else:
            print ""
            print "Thanks for playing!"
            break


if __name__ == "__main__":
    main()