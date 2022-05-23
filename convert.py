import xml.etree.cElementTree as ET
import pandas as pd
import random
import copy

def convertparam(param):
    switcher2 = {
        0:[-1],
        1:[1],
        2:[1,2],
        3:[1,2,3],
        4:[1,2,3,4],
        5:[1,2,3,4,5],
        6:[1,2,3,4,5,6],
        7:[1,2,3,4,5],
        8:[1,2,3,4],
        9:[1,2,3],
        10:[1,2],
        11:[1],
        12:[-1]

    }
    twonote = switcher2.get(param, [-1])
    switcher3 = {
        0:[-1],
        1:[-1],
        2:[-1],
        3:[-1],
        4:[-1],
        5:[-1],
        6:[-1],
        7:[6],
        8:[5,6],
        9:[4,5,6],
        10:[3,4,5,6],
        11:[2,3,4,5,6],
        12:[1,2,3,4,5,6]

    }
    if param > 12:
        threenote = switcher3.get(param, [1,2,3,4,5,6])
    else:
        threenote = switcher3.get(param, [-1])

    return twonote, threenote


def typetotime_num(note_type, note_dot):
    combined = note_type + note_dot
    switcher = {
        'eighthnodot': '1',
        'quarternodot': '1',
        'halfnodot': '1',
        'wholenodot': '1',
        '16thnodot': '1',
        '32ndnodot': '1',
        'eighthdot': '3',
        'quarterdot': '3',
        'halfdot': '3',
        'wholedot': '3',
        '16thdot': '3',
        'eighthdotdot': '7',
        'quarterdotdot': '7',
        'halfdotdot': '7',
        'wholedotdot': '7'
    }
    return switcher.get(combined, '1')

def typetotime_den(note_type, note_dot):
    combined = note_type + note_dot
    switcher = {
        'eighthnodot': '8',
        'quarternodot': '4',
        'halfnodot': '2',
        'wholenodot': '1',
        '16thnodot': '16',
        '32ndnodot': '32',
        'eighthdot': '16',
        'quarterdot': '8',
        'halfdot': '4',
        'wholedot': '2',
        '16thdot': '32',
        'eighthdotdot': '32',
        'quarterdotdot': '16',
        'halfdotdot': '8',
        'wholedotdot': '4'
    }
    return switcher.get(combined, '4')