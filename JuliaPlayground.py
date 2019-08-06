import tkinter as tk
import numpy
from Julia import *
# import wx
# Acquiring the dimensions of the screen
# app = wx.App(False)
WIDTH, HEIGHT = 1000, 700  # wx.GetDisplaySize()


def H(percentage, isFloat=True):
    return (HEIGHT * percentage) if isFloat else int(HEIGHT * percentage)


def W(percentage, isFloat=True):
    return (WIDTH * percentage) if isFloat else int(WIDTH * percentage)


def translate(c, a1, b1, a2, b2):
    return ((c - a1) / (b1 - a1)) * (b2 - a2) + a2


startColor = [0x55, 0x1A, 0x8B]
endColor = [0x00, 0xFF, 0xFF]
colors = [0 for i in range(0xFF + 1)]


def update_colors(array):
    for i in range(0xFF + 1):
        array[i] = "#" + hex(int(translate(i, 0, 255, startColor[0], endColor[0])))[2:].zfill(2) + hex(int(translate(i, 0, 255,
                                                                                                                     startColor[1], endColor[1])))[2:].zfill(2) + hex(int(translate(i, 0, 255, startColor[2], endColor[2])))[2:].zfill(2) + " "


update_colors(colors)


def draw_fractal(canvas, matrix, img):
    res = ""
    for i in range(matrix.shape[0]):
        string = ""
        for j in range(matrix.shape[1]):
            string += colors[matrix[i, j]]
        res += "{" + string + "} "
    img.put(res, to=(0, 0))


def draw_rect(canvas, x1, y1, width, height, color="white"):
    canvas.create_rectangle(x1, y1, x1 + width, y1 + height, outline=color)


def draw_axis(canvas, x1, y1, length, ninter, from_, to, isHorizontal, color="white", inter_length=8):
    if isHorizontal:
        canvas.create_line(x1, y1, x1 + length, y1, fill=color)
    else:
        canvas.create_line(x1, y1, x1, y1 + length, fill=color)
    offset = length / (ninter - 1)
    margin = (to - from_) / (ninter - 1)
    for i in range(ninter):
        if isHorizontal:
            x = x1 + offset * i
            yBegin = y1 - inter_length / 2
            yEnd = y1 + inter_length / 2
            canvas.create_line(x, yBegin, x, yEnd, fill=color)
            text = tk.Text(canvas, fg="white", bg="black",
                           bd=-1, font=("Arial", 10), exportselection=False)
            n = from_ + margin * i
            text.insert(tk.INSERT, "{}.{}".format(int(n), str(int(abs(n) * 100 % 100)).zfill(2)))
            text.place(x=x, y=yEnd, width=offset, height=30)
        else:
            y = y1 + offset * i
            xBegin = x1 - inter_length / 2
            xEnd = x1 + inter_length / 2
            canvas.create_line(xBegin, y, xEnd, y, fill=color)
            text = tk.Text(canvas, fg="white", bg="black",
                           bd=-1, font=("Arial", 10), exportselection=False)
            n = to - (margin * i)
            text.insert(tk.INSERT, "{}.{}".format(int(n), str(int(abs(n) * 100 % 100)).zfill(2)))
            w = 30
            text.place(x=xEnd - w - inter_length,
                       y=y - inter_length, width=w)


screenWidth_1 = W(0.4, False)
screenWidth_2 = W(0.4, False)
screenHeight_1 = H(0.6, False)
screenHeight_2 = H(0.6, False)
screen1X = (WIDTH // 2 - screenWidth_1) // 2
screen2X = (WIDTH // 2 - screenWidth_2) // 2 + WIDTH // 2
screen1Y = H(0.01)  # (HEIGHT - screenHeight) // 2
screen2Y = H(0.01)  # (HEIGHT - screenHeight) // 2


def julia(self, event, arg):
    if instructionText:
        instructionText.destroy()
    if event.x > screen1X and event.x < screen1X + screenWidth_1 and event.y > screen1Y and event.y < screen1Y + screenHeight_1:
        arg["xpos"] = translate(
            event.x, screen1X, screen1X + screenWidth_1, arg["xmin"], arg["xmax"])
        arg["ypos"] = translate(
            event.y, screen1Y, screen1Y + screenHeight_1, arg["ymin"], arg["ymax"])
        matrix = gen_julia_set(screenWidth_2, screenHeight_2, arg["xpos"], arg["ypos"], arg["xmin"],
                               arg["xmax"], arg["ymin"], arg["ymax"], arg["zExponent"], arg["niter"], arg["bound"])
        draw_fractal(arg["canvas"], matrix, arg["img0"])


def mandelbrot(args):
    matrix = gen_mandelbrot(screenWidth_1, screenHeight_1, args["mandelXmin"], args["mandelXmax"], args["mandelYmin"],
                            args["mandelYmax"], args["zExponent"], args["niter"], args["bound"])
    draw_fractal(args["canvas"], matrix, args["img"])


def change_zExponent(event):
    args["zExponent"] = event.widget.get()
    mandelbrot(args)
    matrix = gen_julia_set(screenWidth_2, screenHeight_2, args["xpos"], args["ypos"],
                           args["xmin"], args["xmax"], args["ymin"], args["ymax"], args["zExponent"], args["niter"], args["bound"])
    draw_fractal(args["canvas"], matrix, args["img0"])


def change_niter(event):
    args["niter"] = event.widget.get()
    mandelbrot(args)
    matrix = gen_julia_set(screenWidth_2, screenHeight_2, args["xpos"], args["ypos"],
                           args["xmin"], args["xmax"], args["ymin"], args["ymax"], args["zExponent"], args["niter"], args["bound"])
    draw_fractal(args["canvas"], matrix, args["img0"])


def change_bound(event):
    args["bound"] = event.widget.get()
    mandelbrot(args)
    matrix = gen_julia_set(screenWidth_2, screenHeight_2, args["xpos"], args["ypos"],
                           args["xmin"], args["xmax"], args["ymin"], args["ymax"], args["zExponent"], args["niter"], args["bound"])
    draw_fractal(args["canvas"], matrix, args["img0"])


def change_xmin(event):
    args["mandelXmin"] = event.widget.get()
    mandelbrot(args)
    draw_axis(canvas, W(0.05), H(0.62), screenWidth_1,
              11, args["mandelXmin"], args["mandelXmax"], True)


def change_xmax(event):
    args["mandelXmax"] = event.widget.get()
    mandelbrot(args)
    draw_axis(canvas, W(0.05), H(0.62), screenWidth_1,
              11, args["mandelXmin"], args["mandelXmax"], True)


def change_ymin(event):
    args["mandelYmin"] = event.widget.get()
    mandelbrot(args)
    draw_axis(canvas, W(0.05) - 8, H(0.01), screenHeight_1,
              11, args["mandelYmin"], args["mandelYmax"], False)


def change_ymax(event):
    args["mandelYmax"] = event.widget.get()
    mandelbrot(args)
    draw_axis(canvas, W(0.05) - 8, H(0.01), screenHeight_1,
              11, args["mandelYmin"], args["mandelYmax"], False)


def change_color(index, array, color):
    array[index] = color
    update_colors(colors)
    mandelbrot(args)
    matrix = gen_julia_set(screenWidth_2, screenHeight_2, args["xpos"], args["ypos"],
                           args["xmin"], args["xmax"], args["ymin"], args["ymax"], args["zExponent"], args["niter"], args["bound"])
    draw_fractal(args["canvas"], matrix, args["img0"])


window = tk.Tk()
canvas = tk.Canvas(window, height=HEIGHT, width=WIDTH, bg="black")
canvas.create_line((WIDTH - 1) / 2, 0, (WIDTH - 1) / 2,
                   HEIGHT, fill="white", dash=(4, 4))
instructionText = tk.Label(canvas, bg="black", fg="white", font=(
    "Helvetica", 30), wraplength=screenWidth_2, text="Click on the Mandelbrot to Generate the Corresponding Julia Set")
instructionText.place(x=screen2X + 1, y=screen2Y + 1,
                      width=screenWidth_2 - 1, height=screenHeight_2 - 1)
draw_rect(canvas, screen1X, screen1Y, screenWidth_1, screenHeight_1, "red")
draw_rect(canvas, screen2X, screen2Y, screenWidth_2, screenHeight_2, "blue")
img = tk.PhotoImage(width=screenWidth_1 - 1, height=screenHeight_1 - 1)
img0 = tk.PhotoImage(width=screenWidth_2 - 1, height=screenHeight_2 - 1)
canvas.create_image(screen1X + 1, screen1Y + 1, image=img, anchor=tk.NW)
canvas.create_image(screen2X + 1, screen2Y + 1, image=img0, anchor=tk.NW)


args = {}
args["xpos"] = 0
args["ypos"] = 0
args["img"] = img
args["img0"] = img0
args["canvas"] = canvas
args["mandelXmin"] = -2
args["mandelXmax"] = 1
args["mandelYmin"] = -1.3
args["mandelYmax"] = 1.3
args["xmin"] = -2
args["xmax"] = 2
args["ymin"] = -2
args["ymax"] = 2
args["zExponent"] = 2
args["niter"] = 256
args["bound"] = 4.0

draw_axis(canvas, W(0.05), H(0.62), screenWidth_1, 11, args["mandelXmin"], args["mandelXmax"], True)
draw_axis(canvas, W(0.05) - 8, H(0.01),
          screenHeight_1, 11, args["mandelYmin"], args["mandelYmax"], False)
matrix = gen_mandelbrot(screenWidth_1, screenHeight_1, args["mandelXmin"], args["mandelXmax"], args["mandelYmin"],
                        args["mandelYmax"], args["zExponent"], args["niter"], args["bound"])
scaleWidth = W(0.2)
scaleHeight = H(0.08)
x1 = W(0.05, False)
x2 = x1 + int(scaleWidth)
yOffset = -(H(0.03))


# zExponent
zExponentScale = tk.Scale(canvas, from_=0, to=3, orient=tk.HORIZONTAL, bg="black", bd=(
    0), fg="white", resolution=0.1, troughcolor="black", highlightbackground="orange", label="Z Exponent")
zExponentScale.bind("<ButtonRelease-1>", change_zExponent)
draw_rect(canvas, x1, H(0.7, False) + yOffset,
          scaleWidth, scaleHeight, "orange")
zExponentScale.place(x=x1 + 1, y=H(0.7) + yOffset,
                     width=scaleWidth - 1, height=scaleHeight - 1)
zExponentScale.set(args["zExponent"])


# niter
niterScale = tk.Scale(canvas, from_=0, to=1024, orient=tk.HORIZONTAL, bg="black",
                      fg="white", troughcolor="black", highlightbackground="yellow", label="# Iterations")
niterScale.bind("<ButtonRelease-1>", change_niter)
draw_rect(canvas, x2 + 1, H(0.7, False) + yOffset,
          scaleWidth, scaleHeight, "yellow")
niterScale.place(x=x2 + 2, y=H(0.7) + yOffset,
                 width=scaleWidth - 1, height=scaleHeight - 1)
niterScale.set(args["niter"])


# bound
boundScale = tk.Scale(canvas, from_=0, to=4, orient=tk.HORIZONTAL, bg="black", fg="white",
                      troughcolor="black", resolution=0.1, highlightbackground="pink", label="Bound")
boundScale.bind("<ButtonRelease-1>", change_bound)
draw_rect(canvas, x1, H(0.78, False) + yOffset,
          scaleWidth, scaleHeight, "pink")
boundScale.place(x=x1 + 1, y=H(0.78, False) + 1 + yOffset,
                 width=scaleWidth - 1, height=scaleHeight - 1)
boundScale.set(args["bound"])

# xmin
xminScale = tk.Scale(canvas, from_=-3, to=3, orient=tk.HORIZONTAL, bg="black", fg="white",
                     troughcolor="black", resolution=0.05, highlightbackground="green", label="xmin")
xminScale.bind("<ButtonRelease-1>", change_xmin)
draw_rect(canvas, x2 + 1, H(0.78, False) + yOffset,
          scaleWidth, scaleHeight, "green")
xminScale.place(x=x2 + 2, y=H(0.78) + 1 + yOffset,
                width=scaleWidth - 1, height=scaleHeight - 1)
xminScale.set(args["mandelXmin"])

# ymin
yminScale = tk.Scale(canvas, from_=-3, to=3, orient=tk.HORIZONTAL, bg="black", fg="white",
                     troughcolor="black", resolution=0.05, highlightbackground="red", label="ymin")
yminScale.bind("<ButtonRelease-1>", change_ymin)
draw_rect(canvas, x1, H(0.86, False) + 1 +
          yOffset, scaleWidth, scaleHeight, "red")
yminScale.place(x=x1 + 1, y=H(0.86, False) + 2 + yOffset,
                width=scaleWidth - 1, height=scaleHeight - 1)
yminScale.set(args["mandelYmin"])

# xmax
xmaxScale = tk.Scale(canvas, from_=-3, to=3, orient=tk.HORIZONTAL, bg="black", fg="white",
                     troughcolor="black", resolution=0.05, highlightbackground="blue", label="xmax")
xmaxScale.bind("<ButtonRelease-1>", change_xmax)
draw_rect(canvas, x2 + 1, H(0.86, False) + 1 +
          yOffset, scaleWidth, scaleHeight, "blue")
xmaxScale.place(x=x2 + 2, y=H(0.86, False) + 2 + yOffset,
                width=scaleWidth - 1, height=scaleHeight - 1)
xmaxScale.set(args["mandelXmax"])

# ymax
ymaxScale = tk.Scale(canvas, from_=-3, to=3, orient=tk.HORIZONTAL, bg="black", fg="white",
                     troughcolor="black", resolution=0.05, highlightbackground="purple", label="ymax")
ymaxScale.bind("<ButtonRelease-1>", change_ymax)
draw_rect(canvas, x1, H(0.94, False) + 1 + yOffset,
          scaleWidth, scaleHeight, "purple")
ymaxScale.place(x=x1 + 1, y=H(0.94, False) + 2 + yOffset,
                width=scaleWidth - 1, height=scaleHeight - 1)
ymaxScale.set(args["mandelYmax"])


width = screenWidth_2 / 2
height = H(0.08)
x1 = screen2X
x2 = screen2X + width
y1 = screenHeight_2 + screen2Y + H(0.05)


# rStart
rStartScale = tk.Scale(canvas, from_=0, to=255, orient=tk.HORIZONTAL, bg="black",
                       fg="white", troughcolor="black", highlightbackground="red", label="Start Color:Red")
rStartScale.bind("<ButtonRelease-1>",
                 lambda event: change_color(0, startColor, event.widget.get()))
draw_rect(canvas, x1, y1, width, height, color="red")
rStartScale.place(x=x1 + 1, y=y1 + 1, width=width - 1, height=height - 1)
rStartScale.set(startColor[0])


# rEnd
rEndScale = tk.Scale(canvas, from_=0, to=255, orient=tk.HORIZONTAL, bg="black",
                     fg="white", troughcolor="black", highlightbackground="red", label="End Color:Red")
rEndScale.bind("<ButtonRelease-1>",
               lambda event: change_color(0, endColor, event.widget.get()))
draw_rect(canvas, x2 + 1, y1, width, height, color="red")
rEndScale.place(x=x2 + 2, y=y1 + 1, width=width-1, height=height-1)
rEndScale.set(endColor[0])


# gStart
gStartScale = tk.Scale(canvas, from_=0, to=255, orient=tk.HORIZONTAL, bg="black",
                       fg="white", troughcolor="black", highlightbackground="green", label="Start Color:Green")
gStartScale.bind("<ButtonRelease-1>",
                 lambda event: change_color(1, startColor, event.widget.get()))
draw_rect(canvas, x1, y1 + height + 1, width, height, color="green")
gStartScale.place(x=x1 + 1, y=y1 + height + 2, width=width-1, height=height-1)
gStartScale.set(startColor[1])


# gEnd
gEndScale = tk.Scale(canvas, from_=0, to=255, orient=tk.HORIZONTAL, bg="black",
                     fg="white", troughcolor="black", highlightbackground="green", label="End Color:Green")
gEndScale.bind("<ButtonRelease-1>",
               lambda event: change_color(1, endColor, event.widget.get()))
draw_rect(canvas, x2 + 1, y1 + height + 1, width, height, color="green")
gEndScale.place(x=x2 + 2, y=y1 + height + 2, width=width-1, height=height-1)
gEndScale.set(endColor[1])

# bStart
bStartScale = tk.Scale(canvas, from_=0, to=255, orient=tk.HORIZONTAL, bg="black",
                       fg="white", troughcolor="black", highlightbackground="blue", label="Start Color:Blue")
bStartScale.bind("<ButtonRelease-1>",
                 lambda event: change_color(2, startColor, event.widget.get()))
draw_rect(canvas, x1, y1 + (height + 1) * 2, width, height, color="blue")
bStartScale.place(x=x1 + 1, y=y1 + (height + 1) * 2 +
                  1, width=width-1, height=height-1)
bStartScale.set(startColor[2])

# bEnd
bEndScale = tk.Scale(canvas, from_=0, to=255, orient=tk.HORIZONTAL, bg="black",
                     fg="white", troughcolor="black", highlightbackground="blue", label="End Color:Blue")
bEndScale.bind("<ButtonRelease-1>",
               lambda event: change_color(2, endColor, event.widget.get()))
draw_rect(canvas, x2 + 1, y1 + (height + 1) * 2, width, height, color="blue")
bEndScale.place(x=x2 + 2, y=y1 + (height + 1) * 2 +
                1, width=width-1, height=height-1)
bEndScale.set(endColor[1])

draw_fractal(canvas, matrix, img)
canvas.pack()
canvas.bind("<Button-1>", lambda event, arg=args: julia(None, event, arg))
window.mainloop()
