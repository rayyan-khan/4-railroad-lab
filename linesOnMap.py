from tkinter import *

# set US map to background
window = Tk()
window.title('Railroad Lab')
window.config(bg='white')

photo = PhotoImage(file = 'map.gif')
w = photo.width()
h = photo.height()
window.geometry('{}x{}'.format(w, h))

print(w, h)

canvas = Canvas(window, width=w, height=h)
canvas.pack()

canvas.create_image(w/2, h/2, image=photo)


# import files
rrNodes = open('rrNodes.txt', 'r')  # id, latitude, longitude
rrEdges = open('rrEdges.txt', 'r')  # id1, id2 (an edge exists between them)

dictNodes = {} # dictNodes = {id: (latitude, longitude)}
for id in rrNodes:
    id = id.strip().split(' ')
    dictNodes[id[0]] = (float(id[1]), float(id[2]))

def transformLatitude(latitude):
    latitude = latitude + 146
    return latitude*6.5

def transformLongitude(longitude):
    longitude = longitude*-1 + 81
    return longitude*9

for pair in rrEdges:  # station1, station2, that are connected
    pair = pair.strip().split(' ')
    point1 = pair[0]  # first station id
    point2 = pair[1]  # second station id

    p1Latitude = transformLatitude(dictNodes[point1][1])
    p1Longitude = transformLongitude(dictNodes[point1][0])
    p2Latitude = transformLatitude(dictNodes[point2][1])
    p2Longitude = transformLongitude(dictNodes[point2][0])

    canvas.create_line(p1Latitude, p1Longitude, p2Latitude, p2Longitude, fill='red')

mainloop()