from tkinter import *
from math import pi, acos, sin, cos
import heapq
import sys

# bug in Merida-Seattle
# having trouble getting lines to show up live

# input
if len(sys.argv) == 3:
    startCity, endCity = sys.argv[1], sys.argv[2]

# files with railroad info
rrNodes = open('rrNodes.txt', 'r')  # id, latitude, longitude
rrEdges = open('rrEdges.txt', 'r')  # id1, id2 (an edge exists between them)
rrNodeCity = open('rrNodeCity.txt', 'r')  # id, name

# helper methods
def addNeighbor(station, neighbor):
    if len(dictNodes[station]) == 3:
        dictNodes[station][2].add(neighbor)
    else:
        dictNodes[station] = (dictNodes[station][0], dictNodes[station][1], {neighbor})

def calcDist(y1, x1, y2, x2):  # copy-pasted from the compsci website
    #
    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees

    # if (and only if) the input is strings
    # use the following conversions

    y1 = float(y1)
    x1 = float(x1)
    y2 = float(y2)
    x2 = float(x2)
    #
    R = 3958.76  # miles = 6371 km
    #
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0
    #
    # approximate great circle distance with law of cosines
    #
    return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * R

def transformLatitude(latitude):
    latitude = latitude + 137.1
    return latitude * 10.18

def transformLongitude(longitude):
    longitude = longitude * -1 + 63
    return longitude * 11.8

def getPath(station, closedSet, lvl):
    path = []
    while closedSet[station] != 0:
        for nbr in dictNodes[station][2]:
            nbr = str(nbr)
            if nbr in closedSet and closedSet[nbr] == lvl - 1:
                lvl = lvl - 1
                station = nbr
                path.insert(0, nbr)
    return path

def pathDist(path):
    dist = 0
    for station in range(len(path)-1):
        stationLat = dictNodes[path[station]][0]
        stationLon = dictNodes[path[station]][1]
        nextLat = dictNodes[path[station + 1]][0]
        nextLon = dictNodes[path[station + 1]][1]
        dist += calcDist(stationLat, stationLon, nextLat, nextLon)
    return round(dist)

def drawLines(listPoints, color):
    for pair in listPoints:
        point1, point2 = pair
        if point1 == point2:
            continue
        x1 = transformLatitude(dictNodes[point1][0])
        y1 = transformLongitude(dictNodes[point1][1])
        x2 = transformLatitude(dictNodes[point1][0])
        y2 = transformLongitude(dictNodes[point2][1])
        canvas.create_line(x1, y1, x2, y2, fill=color)

def calcDist1(id1, id2): # breaks things not sure why don't use
    id1Lat, id1Lon = dictNodes[id1][0], dictNodes[id1][1]
    id2Lat, id2Lon = dictNodes[id2][0], dictNodes[id2][0]
    return calcDist(id1Lat, id1Lon, id2Lat, id2Lon)

# setting up the stations
dictNodes = {}  # dictNodes = {id: (latitude, longitude, {neighbors)}
for id in rrNodes:  # set up id, latitude, longitude
    id = id.strip().split(' ')
    dictNodes[id[0]] = (float(id[1]), float(id[2]))

for edge in rrEdges:  # set up neighbors
    edge = edge.strip().split(' ')
    station1, station2 = edge[0], edge[1]
    addNeighbor(station1, station2)
    addNeighbor(station2, station1)

dictNames = {}
for line in rrNodeCity:
    line = line.strip()
    firstSpace = line.index(' ')
    stationId = line[0:firstSpace]
    cityName = line[firstSpace + 1:]
    dictNames[cityName] = stationId
    dictNodes[stationId] = (dictNodes[stationId][0], dictNodes[stationId][1],
                            dictNodes[stationId][2], cityName)


# tkinter things
# set US map to background
window = Tk()
window.title('Railroad Lab')
window.config(bg='white')

photo = PhotoImage(file='map2.gif')
w = photo.width()
h = photo.height()
window.geometry('{}x{}'.format(w, h))

canvas = Canvas(window, width=w, height=h)
canvas.pack()

canvas.create_image(w/2, h/2, image=photo)

rrEdges = open('rrEdges.txt', 'r')

for pair in rrEdges:  # station1, station2, that are connected
    pair = pair.strip().split(' ')
    point1 = pair[0]  # first station id
    point2 = pair[1]  # second station id

    p1Latitude = transformLatitude(dictNodes[point1][1])
    p1Longitude = transformLongitude(dictNodes[point1][0])
    p2Latitude = transformLatitude(dictNodes[point2][1])
    p2Longitude = transformLongitude(dictNodes[point2][0])

    canvas.create_line(p1Latitude, p1Longitude, p2Latitude, p2Longitude, fill='red')


# a-star
def astar(start, goal):
    if start not in dictNames or goal not in dictNames:
        print('The railroad doesnt go to one of these cities.')
        quit()
    if start == goal:
        print('{} and {} are the same city.'.format(start, goal))
        quit()

    start, goal = dictNames[start], dictNames[goal]
    startLat, startLon = dictNodes[start][0], dictNodes[start][1]
    goalLat, goalLon = dictNodes[goal][0], dictNodes[goal][1]

    dist = calcDist(startLat, startLon, goalLat, goalLon)  # dist start-goal
    openSet = [(dist, 0, start, 0)]  # est, level, station, currentDist
    heapq.heapify(openSet)
    closedSet = {}  # {id: lvl}

    while True:
        est, lvl, station, currentDist = heapq.heappop(openSet)
        stationLat, stationLon = dictNodes[station][0], dictNodes[station][1]

        if station == goal:
            closedSet[start] = 0
            closedSet[goal] = lvl
            return getPath(station, closedSet, lvl)
        if station in closedSet:
            continue
        else:
            closedSet[station] = lvl

        for nbr in dictNodes[station][2]:  # dictNodes = {id: latitude, longitude, {neighbors}}
            if nbr in closedSet:
                continue
            else:
                nbrLat, nbrLon = dictNodes[nbr][0], dictNodes[nbr][1]
                nbrDist = currentDist + calcDist(nbrLat, nbrLon, stationLat, stationLon)
                newEst = nbrDist + calcDist(nbrLat, nbrLon, goalLat, goalLon)
                # est = dist from start-neighbor + dist from neighbor-goal
                heapq.heappush(openSet, (newEst, lvl + 1, nbr, nbrDist))  # nbrDist gets popped off
                                                                          # as new currentDist


path = astar('Atlanta', 'Austin')
print(pathDist(path))  # should be 903
path = astar('Merida', 'Seattle')
print(pathDist(path))  # should be 3698

#mainloop()