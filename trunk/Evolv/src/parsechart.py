#!/usr/bin/env python
'''
Created on 2011-05-30

@author: quermit
'''
from pygooglechart import XYLineChart, Axis

from agents.genetics import Phenotype


def main():
    stats = {}

    fp = open("genetics.log", "r")
    lines = fp.readlines()
    header = [h.strip() for h in lines[0].split(",")]
    for line in lines[1:]:
        data = line.split(",")
        type = data[0].strip()
        generation = int(data[1])

        if type not in stats:
            stats[type] = {}
        if generation not in stats[type]:
            stats[type][generation] = {}

        d = stats[type][generation]

        for phene, value in zip(header[2:], data[2:]):
            if phene not in d:
                d[phene] = []
            d[phene].append(float(value))


    for feature in Phenotype.VALID:

        chart = XYLineChart(400, 300)

        max_wx = 0
        for creature in ['rabbit', 'wolf']:
            WX = []
            WYavg = []
            WYmin = []
            WYmax = []
            for g, phenes in stats[creature].items():
                WX.append(g)
                WYavg.append(sum(phenes[feature]) / len(phenes[feature]))
                WYmin.append(min(phenes[feature]))
                WYmax.append(max(phenes[feature]))

            if len(WX) < 2:
                WX.append(2)

            chart.add_data(WX)
            chart.add_data(WYavg)
            chart.add_data(WX)
            chart.add_data(WYmin)
            chart.add_data(WX)
            chart.add_data(WYmax)



            max_wx = max(max_wx, max(WX))

        chart.set_title("Phenotype: %s / generation" % feature)
        chart.set_colours(['ff0000', 'ffe9bf', 'daffbf', '0000ff', 'ebbfff', 'bffff5'])
        chart.set_legend(['rabbits-avg', 'rabbits-min', 'rabbits-max', 'wolves-avg', 'wolves-min', 'wolves-max'])
        chart.set_grid(0, 10, 3, 3)

        chart.set_axis_labels(Axis.BOTTOM, range(max_wx + 1, 5))

        chart.download('genetics-%s.png' % feature)



if __name__ == '__main__':
    main()
