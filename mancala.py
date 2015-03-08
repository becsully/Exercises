__author__ = 'bsullivan'

from pprint import pprint

class Board():

    def __init__(self):
        self.boxes = {}
        self.order = []
        for letter in ["T","B"]:
            for i in range(6,0,-1):
                newbox = {"Distance": i, "Pieces": 4, "Type": "Box", "Player": letter}
                name = letter + str(i)
                self.boxes[name] = newbox
                self.order.append(name)
            newchest = {"Distance": 0, "Pieces": 0, "Type": "Chest", "Player": letter}
            chestname = str("chest" + letter)
            self.boxes[chestname] = newchest
            self.order.append(chestname)
        self.order *= 2


    def __str__(self):
        pprint(self.order)


    def setTest(self):
        for box in self.boxes:
            self.boxes[box]["Pieces"] = 0
        self.boxes["B5"]["Pieces"] = 5
        self.boxes["B3"]["Pieces"] = 3


    def printBoard(self):
        print "#" * 35
        print "#    | %i | %i | %i | %i | %i | %i |    #" % (self.boxes["T1"]["Pieces"], self.boxes["T2"]["Pieces"],
                                                             self.boxes["T3"]["Pieces"], self.boxes["T4"]["Pieces"],
                                                             self.boxes["T5"]["Pieces"], self.boxes["T6"]["Pieces"])
        print "#" + str(self.boxes["chestT"]["Pieces"]).center(4) + "|" + "=" * 23 + "|" + str(self.boxes["chestB"]["Pieces"]).center(4) + "#"
        print "#    | %i | %i | %i | %i | %i | %i |    #" % (self.boxes["B6"]["Pieces"], self.boxes["B5"]["Pieces"],
                                                             self.boxes["B4"]["Pieces"], self.boxes["B3"]["Pieces"],
                                                             self.boxes["B2"]["Pieces"], self.boxes["B1"]["Pieces"])
        print "#" * 35


    def check_move(self,player):
        goodlist = []
        for box in self.boxes:
            if self.boxes[box]["Player"] == player:
                if self.boxes[box]["Type"] == "Chest":
                    pass
                else:
                    test = self.boxes[box]
                    if test["Pieces"] == test["Distance"]:
                        goodlist.append(box)
                    else: pass
        if len(goodlist) == 0:
            return False, None
        elif len(goodlist) == 1:
            return True, goodlist[0]
        else:
            index_list = []
            for box in goodlist:
                index_list.append(self.order.index(box))
            winner = max(index_list)
            return True, self.order[winner]


    def couldcontinue(self, box):
        if self.boxes[box]["Pieces"] == self.boxes[box]["Distance"]:
            return True
        else:
            return False


    def make_move(self, box):
        print ""
        print "...moving box %s..." % box
        value = self.boxes[box]["Pieces"]
        location = self.order.index(box) + 1
        for i in range(value):
            newslice = location + i
            self.boxes[(self.order[newslice])]["Pieces"] += 1
        print ""
        self.boxes[box]["Pieces"] = 0
        self.printBoard()


def validmove(move, board, player):
    if move in board.order:
        if board.boxes[move]["Type"] == "Box" and board.boxes[move]["Pieces"] > 0 and board.boxes[move]["Player"] == player:
            valid = True
            if board.couldcontinue(move):
                last = False
            else:
                last = True
        else:
            valid = last = False
    else:
        valid = last = False
    return valid,last


def automove(board,player):
    while True:
        can_score, box = board.check_move(player)
        if can_score:
            board.make_move(box)
        else: break


def taketurn(comp, board, player):
    if comp == "Y":
        automove(board, player)
    canmove = turncheck(board, player)
    while canmove:
        move = raw_input("Which box should move? ")
        valid, last = validmove(move, board, player)
        if valid:
            board.make_move(move)
            canmove = turncheck(board, player)
            if last:
                break
        else:
            print "Must be a valid board move: either choose a box with pieces in it, or choose your own box!"
    else:
        print "Sorry. You have no play!"


def compcheck(player):
    while True:
        assist = raw_input("Does " + player + " want the computer's assistance? Y/N: ")
        if assist == "Y":
            comp = "Y"
            break
        elif assist == "N":
            comp = "N"
            break
        else:
            print "Try again: type Y or N."
    return comp


def turncheck(board,player):
    p_boxes = []
    for i in range(1,7):
        p_boxes.append(board.boxes[player + str(i)]["Pieces"])
    if p_boxes == [0,0,0,0,0,0]:
        return False
    else:
        return True


def gamecheck(board):
    boxes = []
    for letter in ["T","B"]:
        for i in range (1,7):
            boxes.append(board.boxes[letter + str(i)]["Pieces"])
    if boxes == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
        return False
    else:
        return True


def gameplay(board):
    name1 = raw_input("What's Player 1's name? ")
    name2 = raw_input("What's Player 2's name? ")
    count = 0
    bcomp = compcheck(name1)
    tcomp = compcheck(name2)
    print ""
    board.printBoard()
    while gamecheck(board):
        count += 1
        if count % 2 == 0:
            print ""
            print "It's %s's turn!" % name2
            taketurn(tcomp,board,"T")
        else:
            print ""
            print "It's %s's turn!" % name1
            taketurn(bcomp,board,"B")
    print ""
    print "GAME OVER!"
    if board.boxes["chestT"]["Pieces"] > board.boxes["chestB"]["Pieces"]:
        print "%s is the winner, %i pieces to %i." % (name2, board.boxes["chestT"]["Pieces"],
                                                      board.boxes["chestB"]["Pieces"])
    else:
        print "%s is the winner, %i pieces to %i." % (name1, board.boxes["chestB"]["Pieces"],
                                                      board.boxes["chestT"]["Pieces"])
    print ""


print "#" * 40
print "#" + " " * 38 + "#"
print "#" + ("WELCOME TO PYTHON MANCALA!!").center(38) + "#"
print "#" + " " * 38 + "#"
print "#" * 40
print ""
while True:
    answer = raw_input("Play a game of mancala? Y/N: ")
    if answer == "Y":
        mancala = Board()
        gameplay(mancala)
    else:
        print ""
        print "Thanks for playing!"
        break