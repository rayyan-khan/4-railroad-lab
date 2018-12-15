import tkinter

# input files:
rrNodes = open('rrNodes.txt', 'r')  # id, latitude, longitude
rrEdges = open('rrEdges.txt', 'r')  # id1, id2 (an edge exists between them)
rrNodeCity = open('rrNodeCity.txt', 'r')  # id, city name

# Station class -- each node is a station on the railroad
class Station():
    name = ''  # name of the station, if it has one (not all do)
    id = ''  # id number of the station (all have one)
    latitude = 0
    longitude = 0
    neighbors = set()  # other stations that it has an edge to

    def __init__(self, id, latitude, longitude, name = '', neighbors = set()):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.neighbors = neighbors

    def setNeighbor(self, neighbor):
        self.neighbors.add(neighbor)

    def getNeighbors(self):
        return self.neighbors

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def getId(self):
        return self.id

    def getLatitude(self):
        return self.latitude

    def getLongitude(self):
        return self.longitude

    def getCoordinates(self):
        return (self.latitude, self.longitude)

# global variables
ALL_STATIONS = {}  # dict of stations = {id: Station}
for line in rrNodes:  # id, latitude, longitude on each line
    line = line.split(' ')
    id = line[0].strip()
    latitude = float(line[1].strip())
    longitude = float(line[2].strip())
    ALL_STATIONS[id] = Station(id, latitude, longitude)

k = 0
for edgePair in rrEdges:  # each line = station1, station2, that have an edge between them
    #if k == 3:
    #    quit()
    #k += 1
    edgePair = edgePair.split(' ')
    station1 = edgePair[0]
    station2 = edgePair[1][0:7]
    #print(station1, station2)
    #print(ALL_STATIONS[station1].getNeighbors())
    #print(ALL_STATIONS[station2].getNeighbors())
    ALL_STATIONS[station1].setNeighbor(station2)  # add Station2 to Station1's neighbors
    #print(ALL_STATIONS[station1].getNeighbors())
    #print(ALL_STATIONS[station2].getNeighbors())
    ALL_STATIONS[station2].setNeighbor(station1)  # and vice-versa
    #print('station1 nbrs', station1, ALL_STATIONS[station1].getNeighbors())
    #print('station2 nbrs', station2, ALL_STATIONS[station2].getNeighbors())

for station in ALL_STATIONS:
    print('Station id: {} Latitude: {} Longitude: {} Neighbors: {}'
          .format(ALL_STATIONS[station].getId(),
                  ALL_STATIONS[station].getLatitude(),
                  ALL_STATIONS[station].getLongitude(),
                  ALL_STATIONS[station].getNeighbors()))

k = 0
station = 0
for key in ALL_STATIONS:
    if k == 1:
        quit()
    k = k + 1
    station = ALL_STATIONS[key]
    print('id: {}, neighbors: {}'.format(station.getId(), station.getNeighbors()))


