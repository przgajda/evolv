#!/usr/bin/env python
'''
Created on 2011-05-30

@author: quermit
'''
from pygooglechart import XYLineChart, GroupedVerticalBarChart, Axis

from agents.genetics import Phenotype
from controls.chart import LiveLog

def parseLive():
    stats = {}
    stats_time = {}

    fp = open("live.log", "r")
    lines = fp.readlines()
    header = [h.strip() for h in lines[0].split(",")]
    for line in lines[1:]:
        data = line.split(",")
        type = data[0].strip()
        time = int(float(data[1]) / 10) * 10
        generation = (int(data[2]) / 5) * 5
        livetime = float(data[3])
        event = data[4].strip()

        if type not in stats:
            stats[type] = {}
            stats_time[type] = {}
        if generation not in stats[type]:
            stats[type][generation] = {'livetime': [], 'event': []}
        if time not in stats_time[type]:
            stats_time[type][time] = {'livetime': [], 'event': []}

        d = stats[type][generation]
        t = stats_time[type][time]
        if livetime != 0.0:
            d['livetime'].append(livetime)
            t['livetime'].append(livetime)
        d['event'].append(event)
        t['event'].append(event)

    animalNum(stats_time)
    animalChanges(stats)
    animalChangesInTime(stats_time)

def animalChanges(stats):


    for creature in ['rabbit', 'wolf']:
        chart = GroupedVerticalBarChart(600, 300)

        WYborn = []
        WYage = []
        WYstarv = []
        WYeaten = []
        WX = []
        for t in sorted(stats[creature].keys()):
            WX.append(t)
            born, age, starv, eaten = 0, 0, 0, 0
            for event in stats[creature][t]['event']:
                if event == LiveLog.BIRTH:
                    born += 1
                elif event == LiveLog.AGE:
                    age += 1
                elif event == LiveLog.STARV:
                    starv += 1
                elif event == LiveLog.EATEN:
                    eaten += 1
            WYborn.append(born)
            WYage.append(age)
            WYstarv.append(starv)
            WYeaten.append(eaten)

          #  print born, creature, str(stats[creature][t]['event'])

        chart.set_bar_width(4)
        chart.set_bar_spacing(1)
        chart.set_group_spacing(20)

        chart.set_title("Population changes/generation: / %s" % (creature))
        chart.add_data(WYborn)
        chart.add_data(WYage)
        chart.add_data(WYstarv)
        chart.add_data(WYeaten)
        chart.set_legend(['born', 'old age', 'starvation', 'eaten'])
        chart.set_colours(['00ff00', '000000', 'ff0000', 'ddbbbb'])
        chart.set_axis_labels(Axis.BOTTOM, range(0, max(WX) + 1, 5))

        chart.download('born-deaths-%s.png' % (creature))

def animalChangesInTime(stats):

    stats_t = {'rabbit': {}, 'wolf': {}}
    for creature in ['rabbit', 'wolf']:
        for t in stats[creature].keys():
            new_t = (t / 100) * 100 #zmniejszamy ilosc
            if new_t not in stats_t[creature]:
                stats_t[creature][new_t] = []
            stats_t[creature][new_t] += stats[creature][t]['event']    #tylko eventy
            print stats[creature][t]['event']


    for creature in ['rabbit', 'wolf']:
        chart = GroupedVerticalBarChart(600, 300)

        WYborn = []
        WYage = []
        WYstarv = []
        WYeaten = []
        WYcount = []
        WX = []
        count = 0
        for t in sorted(stats_t[creature].keys()):
            WX.append(t)
            print t
            print stats_t[creature][t]
            born, age, starv, eaten = 0, 0, 0, 0
            for event in stats_t[creature][t]:
                if event == LiveLog.BIRTH:
                    born += 1
                    count += 1
                elif event == LiveLog.AGE:
                    age += 1
                    count -= 1
                elif event == LiveLog.STARV:
                    starv += 1
                    count -= 1
                elif event == LiveLog.EATEN:
                    eaten += 1
                    count -= 1
            WYborn.append(born)
            WYage.append(age)
            WYstarv.append(starv)
            WYeaten.append(eaten)
            WYcount.append(count)


        print WYborn
        print WYcount
        print WYeaten

        chart.set_bar_width(4)
        chart.set_bar_spacing(1)
        chart.set_group_spacing(20)

        chart.set_title("Population changes/time: / %s" % (creature))
        chart.add_data(WYborn)
        chart.add_data(WYage)
        chart.add_data(WYstarv)
        chart.add_data(WYeaten)
        chart.add_data(WYcount)
        chart.auto_scale = True
        chart.set_legend(['born', 'old age', 'starvation', 'eaten', 'population size'])
        chart.set_colours(['00ff00', '000000', 'ff0000', 'ddbbbb', 'aa00ee'])
        chart.set_axis_labels(Axis.BOTTOM, range(0, max(WX) + 1, 100))

        chart.download('life-%s.png' % (creature))


def animalNum(stats):

    chart = XYLineChart(400, 300)

    max_wx = 0
    for creature in ['rabbit', 'wolf']:
        WX = []
        WY = []
        count = 0
        for t in sorted(stats[creature].keys()):
            WX.append(t)
            for event in stats[creature][t]['event']:
                if event == LiveLog.BIRTH:
                    count += 1
                else:
                    count -= 1
          #  print count, creature, str(stats[creature][t]['event'])
            WY.append(count)

        chart.add_data(WX)
        chart.add_data(WY)
        max_wx = max(max_wx, max(WX))

    chart.set_title("Population size")
    chart.set_colours(['ff0000', '0000ff'])
    chart.set_legend(['rabbits', 'wolves'])
    chart.set_grid(0, 10, 3, 3)

    chart.set_axis_labels(Axis.BOTTOM, range(0, max_wx + 1, 100))
    chart.download('number.png')



def main():

    parseLive()

    stats = {}
    time_stats = {}

    fp = open("genetics.log", "r")
    lines = fp.readlines()
    header = [h.strip() for h in lines[0].split(",")]
    for line in lines[1:]:
        data = line.split(",")
        type = data[0].strip()
        generation = int(data[1])
        time = int(float(data[2]) / 10) * 10

        if type not in stats:
            stats[type] = {}
            time_stats[type] = {}
        if generation not in stats[type]:
            stats[type][generation] = {}
        if time not in time_stats[type]:
            time_stats[type][time] = {}

        d = stats[type][generation]
        t = time_stats[type][time]

        for phene, value in zip(header[3:], data[3:]):
            if phene not in d:
                d[phene] = []
            d[phene].append(float(value))
            if phene not in t:
                t[phene] = []
            t[phene].append(float(value))

    for s, name in [(stats, "generation"), (time_stats, "time")]:

        for feature in Phenotype.VALID:

            chart = XYLineChart(400, 300)

            max_wx = 0
            for creature in ['rabbit', 'wolf']:
                WX = []
                WYavg = []
                WYmin = []
                WYmax = []
                for g, phenes in sorted(s[creature].items()):
                    WX.append(g)
                    WYavg.append(sum(phenes[feature]) / len(phenes[feature]))
                    WYmin.append(min(phenes[feature]))
                    WYmax.append(max(phenes[feature]))

                if len(WX) < 2:
                    WX.append(2)

                chart.add_data(WX)
                chart.add_data(WYmin)
                chart.add_data(WX)
                chart.add_data(WYmax)
                chart.add_data(WX)
                chart.add_data(WYavg)



                max_wx = max(max_wx, max(WX))

            chart.set_title("Phenotype: %s / %s" % (feature, name))
            chart.set_colours(['ffe9bf', 'daffbf', 'ff0000', 'ebbfff', 'bffff5', '0000ff'])
            chart.set_legend(['rabbits-min', 'rabbits-max', 'rabbits-avg', 'wolves-min', 'wolves-max', 'wolves-avg'])
            chart.set_grid(0, 10, 3, 3)

            if name == "generation":
                chart.set_axis_labels(Axis.BOTTOM, range(0, max_wx + 1, 5))
            else:
                chart.set_axis_labels(Axis.BOTTOM, range(0, max_wx + 1, 100))
            chart.download("%s-%s.png" % (name, feature))





if __name__ == '__main__':
    main()
