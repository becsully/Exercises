__author__ = 'bsullivan'

from pprint import pprint
from math import sqrt


#0
def fibonacci(times):
    sequence = [1,1]
    for i in range(times):
        sum = sequence[-1] + sequence[-2]
        sequence.append(sum)
    return sequence


#1
def div7not5():
    list = []
    for i in range(2000,3201):
        if (i % 7) == 0 and (i % 5) > 0:
            list.append(str(i))
    print ",".join(list)


#2
def factorial(num):
    answer = 1
    if num != 0:
        for i in range(2,num+1):
            answer = answer * i
    return answer


#3
def dict_squares():
    num = int(raw_input("Enter a number: "))
    dict = {}
    for i in range (1,num+1):
        dict[i] = i ** 2
    print dict


#4
def listtuple():
    entry = raw_input("What's the sequence? ")
    list = entry.split(",")
    tup = tuple(list)
    print list
    print tup


#5
class Practice_string():

    def __init__(self):
        self.string = ""

    def getString(self):
        self.string = raw_input("What's the new string? ")

    def printString(self):
        print self.string.upper()


def practice():
    answer = Practice_string()
    answer.getString()
    answer.printString()


#6
def calc():
    input = raw_input("Enter list: ")
    # 100,150,180
    d_list = input.split(",")
    q_list = []
    c = 50
    h = 30
    for d in d_list:
        q = ( ( 2 * c * int(d) ) / h ) ** 0.5
        q_list.append(str(int(q)))
    print ",".join(q_list)


#7
def twodarray():
    startxy = raw_input("X,Y? ")
    newxy = startxy.split(",")
    x, y = int(newxy[0]), int(newxy[1])
    xlist = []
    for i in range(x):
        ylist = []
        for j in range(y):
            sum = i * j
            ylist.append(sum)
        xlist.append(ylist)
    print xlist


#8
def wordsort():
    rawstring = raw_input("String? ")
    wordlist = rawstring.split(",")
    wordlist.sort()
    print ",".join(wordlist)


#9
def capitalize():
    rawlist = []
    while True:
        raw = raw_input("String? ")
        if raw:
            rawlist.append(raw)
        else:
            break
    for line in rawlist:
        print line.upper()


#10
def removerepeats():
    raw = raw_input("String? ")
    wordlist = raw.split(" ")
    print " ".join(sorted(list(set(wordlist))))


#11
def binary_by_5():
    numlist = [x for x in raw_input("Input? ").split(",")]
    newlist = []
    for i in numlist:
        dec_i = int(i,2)
        if dec_i % 5 == 0:
            newlist.append(i)
    print " ".join(newlist)


