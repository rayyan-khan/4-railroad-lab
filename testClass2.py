from tkinter import *

# working, kinda

# import files
rrNodes = open('rrNodes.txt', 'r')  # id, latitude, longitude
rrEdges = open('rrEdges.txt', 'r')  # id1, id2 (an edge exists between them)
rrNodeCity = open('rrNodeCity.txt', 'r') # id, name

# helper methods
def addNeighbor(station, neighbor):
    if len(dictNodes[station]) == 3:
        dictNodes[station][2].add(neighbor)
    else:
        dictNodes[station] = (dictNodes[station][0], dictNodes[station][1], {neighbor})

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

for line in rrNodeCity:
    line = line.strip()
    firstSpace = line.index(' ')
    stationId = line[0:firstSpace]
    cityName = line[firstSpace + 1:]
    dictNodes[stationId] = (dictNodes[stationId][0], dictNodes[stationId][1],
                            dictNodes[stationId][2], cityName)
    print(dictNodes[stationId])

# tkinter things
# set US map to background
window = Tk()
window.title('Railroad Lab')
window.config(bg='white')

photo = PhotoImage(file = 'map2.gif')
w = photo.width()
h = photo.height()
window.geometry('{}x{}'.format(w, h))

canvas = Canvas(window, width=w, height=h)
canvas.pack()

canvas.create_image(w/2, h/2, image=photo)

def transformLatitude(latitude):
    latitude = latitude + 137.1
    return latitude*10.18

def transformLongitude(longitude):
    longitude = longitude*-1 + 63
    return longitude*11.8

for pair in rrEdges:  # station1, station2, that are connected
    pair = pair.strip().split(' ')
    point1 = pair[0]  # first station id
    point2 = pair[1]  # second station id

    p1Latitude = transformLatitude(dictNodes[point1][1])
    p1Longitude = transformLongitude(dictNodes[point1][0])
    p2Latitude = transformLatitude(dictNodes[point2][1])
    p2Longitude = transformLongitude(dictNodes[point2][0])

    canvas.create_line(p1Latitude, p1Longitude, p2Latitude, p2Longitude, fill='red')

#mainloop()