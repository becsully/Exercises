from __future__ import division
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from pprint import pprint

## http://www.sports-reference.com/cbb/conferences/atlantic-10/2014-schedule.html

def web_results(conf_name, year):
    results = []
    bb_url = "http://www.sports-reference.com/cbb/conferences/%s/%i-schedule.html" % (conf_name, year)
    bb_html = requests.get(bb_url)
    bb_soup = BeautifulSoup(bb_html.text)
    table = bb_soup.find('table', attrs={'class':'sortable  stats_table'})
    rows = table.findAll('tr')
    for row in rows:
        if len(row.find_all('td')) < 5:
            pass
        else:
            tds = row.find_all('td')
            print "%s: Visitor: %s, Home Team: %s, Score: %s-%s" % (tds[0].text, tds[1].text, tds[3].text, tds[2].text, tds[4].text)
            # price = row.find('span', 'price').get_text()
            """
            create_date = row.find('span', 'date').get_text()
            title = row.find_all('a')[1].get_text()
            w_team =
            w_score =
            l_team =
            l_score =
            results.append({'winner': w_team, 'winning score': w_score, 'loser': l_team, 'losing score': l_score})
            """
    return results


def web_crawl():
    conferences = ["big-12", "big-ten","acc","pac-10","big-east","wac","missouri-valley","big-sky","mountain-west","sec"]
    years = []
    for i in range(2000,2014):
        years.append(i)

    web_results("atlantic-10", 2014)


def text_results(cbb_txt):
    score_pairs = []
    with open(cbb_txt, "r") as stats:
        count = 0
        for line in stats:
            count += 1
            game = line.split(",")
            if len(game) < 5 or game[0] == "Date":
                pass
            else:
                scores = sorted([game[2], game[4]])
                score_pairs.append(scores)
    print "Counting up %i games..." % count
    return score_pairs


def percent(num, total):
    raw_percent = num / total
    perc = round((raw_percent * 100), 1)
    return perc


def array_creator(scores): #takes list of score pairs
    windict = {}
    for i in range(10):
        windict[i] = {}
        for j in range(10):
            windict[i].update({j:0})
    total = 0
    for game in scores:
        total += 1
        winner, loser = digits(game)
        windict[winner][loser] += 1
    return windict


def totals(windict):
    losing_dict = {}
    for i in windict:
        for j in windict[i]:
            if j not in losing_dict:
                losing_dict[j] = 0
            losing_dict[j] += windict[i][j]
    pprint(losing_dict)
    return losing_dict


def digits(game): #takes list of two numbers.
    game = sorted(game)
    win_digit = int((game[1])[-1])
    lose_digit = int((game[0])[-1])
    return win_digit, lose_digit


def formatter(windict):
    total = totals(windict)
    print "#" + "=" * 65 + "#"
    print "#|   |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |#"
    print "#|---" + "|-----" * 10 + "|#"
    for j in range(10):
        print "#| %i" % j,
        for i in range(10):
            if len(str(windict[j][i])) == 3:
                print "| %i" % windict[j][i],
            else:
                print "|  %i" % windict[j][i],
        print "|#"
    print "#|---" + "|-----" * 10 + "|#"
    print "TOT:",
    for i in range(10):
        print "| %i" % total[i],
    print "|#"
    print "#" + "=" * 65 + "#"


def differences(scores):
    diff_dict = {}
    for score in scores:
        winner, loser = digits(score)
        difference = winner - loser
        if difference < 0:
            difference += 10
        if difference not in diff_dict:
            diff_dict[difference] = 1
        else:
            diff_dict[difference] += 1
    pprint(diff_dict)
    return diff_dict


def line_graph(windict):
    winning_digits = []
    losing_digits = [] # will be a list of lists
    colors = [((31/255),(119/255),(180/255)),((255/255),(127/255),(14/255)),((44/255),(160/255),(44/255)),
              ((214/255),(39/255),(40/255)),((148/255),(103/255),(189/255)),((140/255),(86/255),(75/255)),
              ((227/255),(119/255),(194/255)),((127/255),(127/255),(127/255)),((188/255),(189/255),(34/255)),
              ((23/255),(190/255),(207/255))]

    for win_score in windict:
        winning_digits.append(win_score)
        losings = []
        for lose_score in windict[win_score]:
            losings.append(windict[win_score][lose_score])
        losing_digits.append(losings)

    pprint(winning_digits)
    pprint(losing_digits)

    fontP = FontProperties()
    fontP.set_size('small')

    fig = plt.figure()
    graph = fig.add_subplot(111)

    graph.set_xticklabels([0,1,2,3,4,5,6,7,8,9])
    for i in range(len(losing_digits)):
        graph.plot(winning_digits, losing_digits[i], linewidth=2, color=colors[i], label = str(i))
    graph.set_xticks([0,1,2,3,4,5,6,7,8,9])
    plt.legend(loc='upper center', bbox_to_anchor=(.5, .98), ncol=3, prop=fontP)
    plt.show()


def bar_graph(differences): #differences is a dictionary with ten keys for each winning difference 0-9.
    x_list = [] #differences, a list of 0-9
    y_list = [] #num of games

    for entry in differences:
        x_list.append(entry)
        y_list.append(differences[entry])

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    for entry in x_list:
        print "hello"



filename = "cbb_stats.txt"
scores = text_results(filename)
windict = array_creator(scores)
formatter(windict)


print "LOSING SCORE TOTAL: "
totals(windict)

print
print "DIFFERENCES: "
diff = differences(scores)
#bar_graph(diff)
