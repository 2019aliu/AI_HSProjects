# @author ALiu
# @date 06/05/18
# Firefly Assignment

import math
import random
from tkinter import *
import time
import winsound

import pprint

# Firefly specs
# time = 0  # necessary?
deltaT = 0.05  # when tau is 1, this constant controls how fast the fireflies learn (0.05 or so is good)
tau = 1  # this is the time constant
bumpConst = 0.005
threshold = 0.95

# Graphics scaling
width = 800
height = 600
xfactor = 1.3  # Scaling factor in x direction
yfactor = 1.33 * xfactor  # Scaling factor in y direction
xoffset = 90  # offset of the map in x direction
yoffset = 80  # offset of the map in y direction
radius = 5  # Set radius of the circle
minx = 0
miny = 0
maxx = 1
maxy = 1
xrn = maxx - minx
yrn = maxy - miny
xscale = width / (xrn * xfactor)
yscale = width / (yrn * yfactor)

def display(root, canvas, charges, coords):
    canvas.delete("all")
    for index in range(len(charges)):

        xcenter = (coords[index][0] - minx) * xscale + xoffset
        ycenter = (coords[index][1] - miny) * yscale + yoffset
        # intensity = 255 if round(charges[index] * 255) > 255 else round(charges[index] * 255)
        intensity = 0 if charges[index] <= threshold else 255  # once everything works
        ct_hex = "%02x%02x%02x" % (intensity, intensity, 0)
        bg_color = '#' + "".join(ct_hex)
        canvas.create_oval(xcenter - radius, ycenter - radius, xcenter + radius, ycenter + radius, fill=bg_color)
    canvas.pack()
    root.update_idletasks()
    root.update()
    time.sleep(0.001)

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def main():
    # tkinter graphics: window setup
    root = Tk()
    root.title("Fireflies")
    scwidth = root.winfo_screenwidth()     # Use screen dimensions and window dimensions to place window
    scheight = root.winfo_screenheight()
    xdim = (scwidth / 2) - (width / 2)
    ydim = (scheight * 5 / 12) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, xdim, ydim))  # Opens window in specified position and size
    canvas = Canvas(root, width=width, height=height, background="black")

    # generate the random charges
    charges = [random.uniform(0, 1) for initCharge in range(100)]
    coords = [(random.uniform(0, 1), random.uniform(0, 1)) for initCoords in range(100)]

    # initial display
    display(root, canvas, charges, coords)

    # play music
    winsound.PlaySound('Fireflies-daf67SCo5_s.wav', winsound.SND_LOOP + winsound.SND_ASYNC)

    # infinite loop (until window closed)
    while True:
        updated = False
        while not updated:
            for cIndex in range(len(charges)):
                charges[cIndex] += deltaT * (1 - charges[cIndex]) / tau
                if charges[cIndex] > threshold:
                    for newIndex in range(len(charges)):
                        if newIndex != cIndex:
                            charges[newIndex] += bumpConst * (distance(coords[cIndex][0], coords[cIndex][1], coords[newIndex][0], coords[newIndex][1]))**2
                        elif newIndex == cIndex:
                            charges[newIndex] = 0
                    continue
            updated = True
        try:
            display(root, canvas, charges, coords)
        except:
            print("Thanks for using this program. I hope you enjoyed it!")
            break

if __name__ == '__main__':
    main()
