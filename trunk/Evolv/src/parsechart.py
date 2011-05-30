'''
Created on 2011-05-30

@author: quermit
'''
from pygooglechart import XYLineChart


def main():
    stats = {}

    fp = open("genetics.log", "r")
    lines = fp.readlines()
    header = lines[9]
    for line in lines[1:]:
        data = line.split(",")
        type = data[0]
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







if __name__ == '__main__':
    main()
