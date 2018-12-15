from tkinter import *

# set US map to background
window = Tk()
window.title('Railroad Lab')
window.config(bg='white')

photo = PhotoImage(file = 'map.gif')
w = photo.width()
h = photo.height()
window.geometry('{}x{}'.format(w, h))

canvas = Canvas(window, width=w, height=h)
canvas.pack()

canvas.create_image(w/2, h/2, image=photo)
canvas.create_line(0, 0, 500, 500, fill='red')

mainloop()