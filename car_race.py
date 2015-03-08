from __future__ import division
from random import randrange
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties


class Car:

    def __init__(self,driver,sponsor):
        self.driver = driver
        self.sponsor = sponsor
        self.odometer = 0
        self.speed = randrange(1,500)

    def restart(self):
        self.odometer = 0
        self.speed = randrange(1,500)

    def updateMinute(self):
        self.odometer = self.odometer + self.speed * (1/60)

    def updateFiveMinute(self):
        self.speed = randrange(1,500)

    def getOdometer(self):
        return self.odometer


def createCar():
    driver = raw_input("What's the driver's name? ")
    sponsor = raw_input("What's the sponsor? ")
    new_car = Car(driver,sponsor)
    return new_car


def race(car_list):
    count = 0
    finished = False
    standings = {}
    odometer_dict = {}
    for car in car_list:
        odometer_dict[car] = [0]
    while finished == False:
        count += 1
        for car in car_list:
            car.updateMinute()
            if car.odometer > 500:
                winner = car
                finished = True
            else:
                pass
        if count % 5 == 0:
            for car in car_list:
                car.updateFiveMinute()
                odometer_dict[car].append(car.getOdometer())
        if count % 120 == 0:
            print "..."
            hours = count / 60
            print "%i hours into the race, here are the standings:" % hours
            for car in car_list:
                standings[car.driver] = car.odometer
            new_count = 0
            for driver in sorted(standings, key=standings.get, reverse=True):
                new_count += 1
                print "%d. %s has traveled %.2f miles." % (new_count, driver, standings[driver])
    return winner, count, odometer_dict


def is_num(value):
    try:
        int(value)
    except ValueError:
        print "Try again with an integer."
        return False
    value = int(value)
    if value > 10 or value < 2:
        print "Try again with a number between 2 and 10."
        return False
    else:
        return True


def min_to_hr(raw):
    hours = raw // 60
    new_min = raw % 60
    result = "%i:%02d" % (hours, new_min)
    return result


def graph(odometers,time): #odometers is a dictionary of lists of where the cars were at at each juncture
    drivers = []
    times = []
    miles = [] # will become a list of lists of odometer readings
    xlabels = []
    colors = [((31/255),(119/255),(180/255)),((255/255),(127/255),(14/255)),((44/255),(160/255),(44/255)),
              ((214/255),(39/255),(40/255)),((148/255),(103/255),(189/255)),((140/255),(86/255),(75/255)),
              ((227/255),(119/255),(194/255)),((127/255),(127/255),(127/255)),((188/255),(189/255),(34/255)),
              ((23/255),(190/255),(207/255))]

    for car in odometers:
        drivers.append(car.driver)
        miles.append(odometers[car])

    for i in range(0,time+1,5):
        times.append(i)
        xlabels.append(min_to_hr(i))

    fontP = FontProperties()
    fontP.set_size('small')

    fig = plt.figure()
    graph = fig.add_subplot(111)

    graph.set_xticklabels(xlabels)
    for i in range(len(miles)):
        graph.plot(times, miles[i], linewidth=2, color=colors[i],label=drivers[i])
    graph.set_xticks(times)
    plt.legend(loc='upper center', bbox_to_anchor=(.5, .98), ncol=3, prop=fontP)
    plt.show()



"""
car_list = []
num_bool = False
while num_bool == False:
    num_of_cars = raw_input("How many cars are racing today? ")
    if is_num(num_of_cars):
        num_bool = True
num = int(num_of_cars)
for i in range(num):
    car = createCar()
    car_list.append(car)
"""

car1 = Car("Jeff Gordon","DuPont")
car2 = Car("Jimmie Johnson","Lowe's")
car3 = Car("Tony Stewart","The Home Depot")
car4 = Car("Matt Kenseth","Citi Financial")
car5 = Car("Kyle Busch","M&M's")
car6 = Car("Kevin Harvick","Budweiser")
car7 = Car("Kurt Busch","Monster")
car8 = Car("Denny Hamlin","FedEx")
car9 = Car("Carl Edwards","Arris Group")
car10 = Car("Dale Earnhardt, Jr.","National Guard")

car_list = [car1, car2, car3, car4, car5, car6, car7, car8, car9, car10]

print "#" * 35
print "#" + " " * 33 + "#"
print "#" + ("WELCOME TO THE PYTHON 500!!").center(33) + "#"
print "#" + " " * 33 + "#"
print "#" * 35
print ""
print "Today's competitors are: "
count = 0
for car in car_list:
    count += 1
    print str(count) + ". " + car.driver + " (sponsored by " + car.sponsor + ")"
print ""
while True:
    print "THE RACE HAS BEGUN!"
    print "..."
    winner, winning_time, odometers = race(car_list)
    print ""
    print "... AND THE WINNER IS: "
    print "%s, in %s! (sponsored by %s)" % (winner.driver, min_to_hr(winning_time), winner.sponsor)
    print "He averaged %.2f mph." % (winner.odometer / winning_time * 60)
    print ""
    print graph(odometers,winning_time)
    query = raw_input("Race again? Y/N: ")
    if query == "Y":
        for car in car_list:
            car.restart()
    else:
        break

"""
1. Jeff Gordon (sponsored by DuPont)
2. Jimmie Johnson (sponsored by Lowe's)
3. Tony Stewart (sponsored by The Home Depot)
4. Matt Kenseth (sponsored by Citi Financial)
5. Kyle Busch (sponsored by M&M's)
6. Kevin Harvick (sponsored by Budweiser)
7. Kurt Busch (sponsored by Monster)
8. Denny Hamlin (sponsored by FedEx)
9. Carl Edwards (sponsored by Arris Group)
10. Dale Earnhardt, Jr. (sponsored by National Guard)
"""