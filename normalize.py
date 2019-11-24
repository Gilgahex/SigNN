import json
import os
from statistics import mean, stdev
from string import ascii_uppercase

import numpy as np
import matplotlib.pyplot as plt

PATH = "/home/ari/Desktop/SigNN/training_data/"

def norm(hands):
    assert isinstance(hands, list)
    assert all(isinstance(hand, list) for hand in hands)
    normHands = []
    for hand in hands:
        xCoords = [x for x in hand[::2]]
        yCoords = [y for y in hand[1::2]]

        normXCoords = [x / max(xCoords) for x in xCoords]
        normYCoords = [y / max(yCoords) for y in yCoords]

        normHand = [None]*(len(normXCoords)+len(normYCoords))
        normHand[::2] = normXCoords
        normHand[1::2] = normYCoords
        normHands.append(normHand)

    return normHands

def loadHands(jsonFile):
    assert ".json" in jsonFile, 'Must be a json file!'
    file = open(os.path.join(PATH, jsonFile))
    jsonData = json.load(file)
    hands = jsonData['coordinates']
    return hands

def analyzeHands(hands):
    assert isinstance(hands, list)
    assert all(isinstance(hand, list) for hand in hands)
    VALUES_PER_HAND = len(hands[0])
    assert all(len(hand) == VALUES_PER_HAND for hand in hands), "Not all hands have {} points".format(VALUES_PER_HAND)

    averagePoints = []
    stDevs = []
    minPoints = []
    maxPoints = []
    
    for point in range(0, VALUES_PER_HAND):
        means = mean(x[point] for x in hands)
        devs = stdev(x[point] for x in hands)
        mins = min(x[point] for x in hands)
        maxs = max(x[point] for x in hands)
        averagePoints.append(means)
        stDevs.append(devs)
        minPoints.append(mins)
        maxPoints.append(maxs)


    return {
        "mean" : averagePoints,
        "stdev" : stDevs,
        'max' : maxPoints,
        'min' : minPoints
    }


def plot(hand):
    COLORS = ['red', 'blue', 'green', 'purple', 'black']
    x = [max(xx for xx in hand[::2]) - x for x in hand[::2]]
    y = [max(yy for yy in hand[1::2]) - y for y in hand[1::2]]

    text = [z for z in range(0, len(x))]
    assert len(x) == len(y), "Uneven x and y coordnates. {} x and {} y".format(len(x), len(y))
    plt.scatter(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('square')

    for i, txt in enumerate(text):
        plt.annotate(txt, (x[i], y[i]))

    for finger, color in zip(range(1, 21, 4), COLORS):
        plt.plot(x[finger:finger+4], y[finger:finger+4], 'ro-', color=color)

    plt.show()

HANDS = {}
for x in ascii_uppercase:
    fileName = x + ".json"
    try:
        loadedHands = norm(loadHands(fileName))
    except:
        print("{} is not in dataset".format(x))
        continue
    averageHand = norm(loadedHands)
    HANDS[x] = analyzeHands(averageHand)['mean']

file = open("averageHands.json", "w+")
json.dump(HANDS, file)

# plot(analyzeHands(norm(loadHands("L.json")))['mean'])
# plot(loadHands("L.json")[0])
# [plot(loadHands("L.json")[x]) for x in range(6)]
# print(analyzeHands(norm(loadHands("L.json"))))