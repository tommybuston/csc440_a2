import copy
from tkinter import Button
from tkinter import Canvas
from tkinter import Label
from tkinter import Tk
from tkinter import Frame

from convex_hull import compute_hull
# from convex_hull import base_case_hull

previous_lines = set()

def draw_point(canvas, x, y):
    return canvas.create_text(x, y, text="({}, {})".format(x, y))


def add_point(event):
    draw_point(w, event.x, event.y)
    points.append((event.x, event.y))
    return


def update_status_bar(event):
    status_bar.config(text="Mouse position: ({}, {})".format(event.x, event.y))


def draw_hull():
    # hull = copy.copy(compute_hull(points))
    hull = copy.copy(compute_hull(points))
    print('*' * 80)
    print(f'Convex Hull: {hull}')
    print(f'Points:      {points}')

    for line in previous_lines:
        w.create_line(line[0], line[1], line[2], line[3], width=3, fill='red')

    for i in range(0, len(hull)):
        current_index = i
        next_index = (current_index + 1) % len(hull)

        x1 = hull[current_index][0]
        y1 = hull[current_index][1]
        x2 = hull[next_index][0]
        y2 = hull[next_index][1]
        w.create_line(x1, y1, x2, y2, width=3)

        previous_lines.add((x1, y1, x2, y2))

    return


def clear():
    w.delete("all")
    points.clear()
    previous_lines.clear()
    return


if __name__ == '__main__':
    master, points = Tk(), list()

    master.title("Convex Hull Canvas")

    buttons = Frame(master)
    buttons.pack(side="top")

    submit_button = Button(master, text="Draw Hull", command=draw_hull)
    clear_button = Button(master, text="Clear Canvas", command=clear)
    quit_button = Button(master, text="Quit", command=master.quit)

    paddingx = 5
    paddingy = 0
    submit_button.pack(in_=buttons, side="left", padx=paddingx, pady=paddingy)
    clear_button.pack(in_=buttons, side="left", padx=paddingx, pady=paddingy)
    quit_button.pack(in_=buttons, side="right", padx=paddingx, pady=paddingy)

    canvas_width = 1200
    canvas_height = 600
    w = Canvas(master,
               width=canvas_width,
               height=canvas_height)

    status_bar = Label(master, text="Mouse position: ", bd=1, relief="sunken", anchor="w")
    status_bar.pack(side="bottom", fill="x")

    w.pack()
    w.bind('<Button-1>', add_point)
    w.bind('<Motion>', update_status_bar)

    w.mainloop()
