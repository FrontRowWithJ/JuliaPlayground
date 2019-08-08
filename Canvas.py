"""Canvas Class."""
import tkinter as tk


class Canvas:
    """Tkinter GUI for the JuliaPlayground Class."""

    def __init__(self, width, height, jp):
        """Initialise the tkinter canvas with dimensions (width x height)."""
        self.WIDTH = width
        self.HEIGHT = height
        self.jp = jp
        self.cx, self.cy = -1, -1
        self.colorCodeStart = [0x55, 0x1A, 0x8B]
        self.colorCodeEnd = [0x00, 0xFF, 0xFF]
        self.colors = [0 for i in range(0xFF + 1)]
        self.screenWidth1 = self._W(0.4, False)
        self.screenWidth2 = self._W(0.4, False)
        self.screenHeight1 = self._H(0.6, False)
        self.screenHeight2 = self._H(0.6, False)
        self.screen1x = (self.WIDTH // 2 - self.screenWidth1) // 2
        self.screen2x = (self.WIDTH // 2 -
                         self.screenWidth2) // 2 + self.WIDTH // 2
        self.screen1y = self._H(0.01, False)
        self.screen2y = self.screen1y  # self._H(0.1, False)
        self.window = tk.Tk()
        self.instructionText = None
        self.canvas = tk.Canvas(
            height=self.HEIGHT, width=self.WIDTH, bg="black")
        self.imageLeft = tk.PhotoImage(
            width=self.screenWidth1 - 1, height=self.screenHeight1 - 1)
        self.imageRight = tk.PhotoImage(
            width=self.screenWidth2 - 1, height=self.screenHeight2 - 1)
        self.scaleWidth = self._W(0.2)
        self.scaleHeight = self._H(0.08)
        self.scaleX1 = self._W(0.05, False)
        self.scaleX2 = self.scaleX1 + int(self.scaleWidth)
        self.yOffset = -self._H(0.03)
        self.scaleDict = {}
        # Calling set up functions
        self.jp.set_width(self.screenWidth1)
        self.jp.set_height(self.screenHeight1)
        self._update_colors()
        self._gen_instuction_text()
        self.canvas.create_line(self.WIDTH / 2, 0, self.WIDTH / 2, self.HEIGHT,
                                fill="white", dash=(4, 4))
        self.instructionText.place(
            x=self.screen2x + 1, y=self.screen2y + 1, width=self.screenWidth2 - 1, height=self.screenHeight2 - 1)
        self.draw_rect(self.screen1x, self.screen1y, self.screenWidth1,
                       self.screenHeight1, "red")
        self.draw_rect(self.screen2x, self.screen2y, self.screenWidth2,
                       self.screenHeight2, "blue")
        self.canvas.create_image(
            self.screen1x + 1, self.screen1y + 1, image=self.imageLeft, anchor=tk.NW)
        self.canvas.create_image(self.screen2x + 1, self.screen2y + 1,
                                 image=self.imageRight, anchor=tk.NW)
        self.canvas.bind(
            "<Button-1>", lambda event: self._draw_julia(event.x, event.y))
        self.canvas.pack()
        self.draw_axis(self._W(0.05), self._H(0.62),
                       self.screenWidth1, 11, jp.xmin_mandel, jp.xmax_mandel)
        self.draw_axis(self._W(0.05) - 8, self._H(0.01),
                       self.screenHeight1, 11, jp.ymin_mandel, jp.ymax_mandel, False)
        self.draw_fractal(self.jp.mandelbrot())

        # zExponent
        self._gen_scale("zExponent", 0, 3, "orange", "Z Exponent", self.scaleX1, self._H(
            0.7, False) + self.yOffset, 0.1, "update_zExponent", self.jp.zExponent)

        # niter
        self._gen_scale("niter", 0, 1024, "yellow", "# Iterations", self.scaleX2 + 1, self._H(0.7,
                                                                                              False) + self.yOffset, 1, "update_niter", self.jp.niter)
        # bound
        self._gen_scale("bound", 0, 4, "pink", "Bound", self.scaleX1, self._H(
            0.78, False) + self.yOffset, 0.1, "update_bound", self.jp.bound)

        # xmin
        self._gen_scale("xmin", -3, 3, "green", "xmin", self.scaleX2 + 1,
                        self._H(0.78, False) + self.yOffset, 0.05, "update_xmin_mandel", self.jp.xmin_mandel)

        # ymin
        self._gen_scale("ymin", -3, 3, "red", "ymin", self.scaleX1,
                        self._H(0.86, False) + 1 + self.yOffset, 0.05, "update_ymin_mandel", self.jp.ymin_mandel)

        # xmax
        self._gen_scale("xmax", -3, 3, "blue", "xmax", self.scaleX2 + 1,
                        self._H(0.86, False) + 1 + self.yOffset, 0.05, "update_xmax_mandel", self.jp.xmax_mandel)

        # ymax
        self._gen_scale("ymax", -3, 3, "purple", "ymax", self.scaleX1,
                        self._H(0.94, False) + 1 + self.yOffset, 0.05, "update_ymax_mandel", self.jp.ymax_mandel)

        x1 = self.screen2x
        x2 = self.screen2x + self.scaleWidth + 1
        y = self.screenHeight2 + self.screen2y + self._H(0.05)
        yOff = self.scaleHeight + 1

        # Red start
        self._gen_color_scale("redStart", "red", "Start ColorCode: Red", 0, self.colorCodeStart,
                              x1, y)

        # Red end
        self._gen_color_scale("redEnd", "red", "End ColorCode: Red", 0, self.colorCodeEnd,
                              x2, y)

        # Green start
        self._gen_color_scale("greenStart", "green", "Start ColorCode: Green",
                              1, self.colorCodeStart, x1, y + yOff)

        # Green End
        self._gen_color_scale("greenEnd", "green", "End ColorCode: Green",
                              1, self.colorCodeEnd, x2, y + yOff)

        # Blue Start
        self._gen_color_scale("blueStart", "blue", "Start ColorCode: Blue",
                              2, self.colorCodeStart, x1, y + yOff * 2)

        # Blue End
        self._gen_color_scale(
            "blueEnd", "blue", "End ColorCode: Blue", 2, self.colorCodeEnd, x2, y + yOff * 2)
        self.draw_window()

    def _H(self, percent, isFloat=True):
        """Return a percentage of the screen height."""
        return (self.HEIGHT * percent) if isFloat else int(self.HEIGHT * percent)

    def _W(self, percent, isFloat=True):
        """Return a percentage of the screen width."""
        return (self.WIDTH * percent) if isFloat else int(self.WIDTH * percent)

    def _translate(self, c, x1, y1, x2, y2):
        """Translate c from range x1,y1 to x2,y2."""
        return (c-x1) / (y1 - x1) * (y2 - x2) + x2

    def _update_colors(self):
        """Update the color array with new start and begin color values."""
        for i in range(0xFF + 1):
            self.colors[i] = "#" + hex(int(self._translate(i, 0, 255, self.colorCodeStart[0], self.colorCodeEnd[0])))[2:].zfill(2) \
                + hex(int(self._translate(i, 0, 255, self.colorCodeStart[1], self.colorCodeEnd[1])))[2:].zfill(2) \
                + hex(int(self._translate(i, 0, 255,
                                          self.colorCodeStart[2], self.colorCodeEnd[2])))[2:].zfill(2) + " "

    def draw_fractal(self, fractal, isImageLeft=True):
        """Convert the fractal matrix to color codes and draw them to the canvas."""
        img = self.imageLeft if isImageLeft else self.imageRight
        res = ""
        for i in range(fractal.shape[0]):
            string = ""
            for j in range(fractal.shape[1]):
                string += self.colors[fractal[i, j]]
            res += "{" + string + "} "
        img.put(res, to=(0, 0))

    def draw_rect(self, x, y, width, height, color="white"):
        """Draw a rectangle to the canvas at the point (x, y) with dimensions width x height."""
        self.canvas.create_rectangle(
            x, y, x + width, y + height, outline=color)

    def _gen_instuction_text(self):
        """Draw the instruction text that tells the user how to generate a julia set from the mandelbrot set."""
        self.instructionText = tk.Label(self.canvas, bg="black", fg="white", font=(
            "Helvetica", 30), wraplength=self.screenWidth2, text="Click on the Mandelbrot to Generate the Corresponding Julia Set")

    def draw_axis(self, x1, y1, length, ninter, from_, to, isHorizontal=True, color="white", inter_length=8):
        """Draw a horizontal or vertical axis of length 'length' from the point (x1, y1) width 'ninter' intervals in the range 'from_' - 'to'."""
        if isHorizontal:
            self.canvas.create_line(x1, y1, x1 + length, y1, fill=color)
        else:
            self.canvas.create_line(x1, y1, x1, y1 + length, fill=color)
        offset = length / (ninter - 1)
        margin = (to - from_) / (ninter - 1)
        for i in range(ninter):
            if isHorizontal:
                x = x1 + offset * i
                yBegin = y1 - inter_length / 2
                yEnd = y1 + inter_length / 2
                self.canvas.create_line(x, yBegin, x, yEnd, fill=color)
                text = tk.Text(self.canvas, fg="white", bg="black",
                               bd=-1, font=("Arial", 9), exportselection=False)
                n = from_ + margin * i
                text.insert(tk.INSERT, "{}.{}".format(
                    int(n), str(int(abs(n) * 100 % 100)).zfill(2)))
                text.place(x=x, y=yEnd, width=offset, height=30)
            else:
                y = y1 + offset * i
                xBegin = x1 - inter_length / 2
                xEnd = x1 + inter_length / 2
                self.canvas.create_line(xBegin, y, xEnd, y, fill=color)
                text = tk.Text(self.canvas, fg="white", bg="black",
                               bd=-1, font=("Arial", 9), exportselection=False)
                n = to - (margin * i)
                text.insert(tk.INSERT, "{:10.2f}".format(n))
                w = 50
                text.place(x=xEnd - w - inter_length,
                           y=y - inter_length, width=w)

    def _set_color_code(self, index, colorCode, colorArray):
        """Update the color sprectrum for the fractals."""
        colorArray[index] = colorCode
        self._update_colors()
        self.draw_fractal(self.jp.mandelbrot())
        self.draw_fractal(self.jp.julia(self.cx, self.cy), False)

    def draw_window(self):
        """Call the main loop of the window."""
        self.window.mainloop()

    def draw(self, value, funcName):
        """Call an update function from the JuliaPlayground object with the function name string and redraw the fractals with the newly specified values."""
        updateFunc = getattr(self.jp, funcName)
        fractals = updateFunc(value)
        self.draw_fractal(fractals[0])
        self.draw_fractal(fractals[1], False)
        self.draw_axis(self._W(0.05), self._H(0.62),
                       self.screenWidth1, 11, self.jp.xmin_mandel, self.jp.xmax_mandel)
        self.draw_axis(self._W(0.05) - 8, self._H(0.01),
                       self.screenHeight1, 11, self.jp.ymin_mandel, self.jp.ymax_mandel, False)

    def _gen_scale(self, scaleName, from_, to, color, label, xpos, ypos, res, funcName, startValue):
        """Generate a scale that alters the values for the fractals."""
        self.scaleDict[scaleName] = tk.Scale(self.canvas, from_=from_, to=to, orient=tk.HORIZONTAL, bg="black",
                                             fg="white", resolution=res, troughcolor="black", highlightbackground=color, label=label)
        self.scaleDict[scaleName].bind(
            "<ButtonRelease-1>", lambda event, fn=funcName: self.draw(event.widget.get(), funcName))
        self.draw_rect(xpos, ypos, self.scaleWidth, self.scaleHeight, color)
        self.scaleDict[scaleName].place(
            x=xpos + 1, y=ypos + 1, width=self.scaleWidth - 1, height=self.scaleHeight-1)
        self.scaleDict[scaleName].set(startValue)

    def _gen_color_scale(self, scaleName, color, label, index, array, xpos, ypos):
        self.scaleDict[scaleName] = tk.Scale(self.canvas, from_=0, to=255, orient=tk.HORIZONTAL,
                                             bg="black", fg="white", troughcolor="black", highlightbackground=color, label=label)
        self.scaleDict[scaleName].bind(
            "<ButtonRelease-1>", lambda event: self._set_color_code(index, event.widget.get(), array))
        self.draw_rect(xpos, ypos, self.scaleWidth,
                       self.scaleHeight, color=color)
        self.scaleDict[scaleName].place(
            x=xpos + 1, y=ypos + 1, width=self.scaleWidth-1, height=self.scaleHeight-1)
        self.scaleDict[scaleName].set(array[index])

    def _draw_julia(self, xpos, ypos):
        if xpos > self.screen1x and xpos < (self.screen1x + self.screenWidth1) and ypos > self.screen1y and ypos < (self.screen1y + self.screenHeight1):
            if self.instructionText:
                self.instructionText.destroy()
                self.instructionText = None
            self.cx = self._translate(xpos, self.screen1x, self.screen1x +
                                      self.screenWidth1, self.jp.xmin_mandel, self.jp.xmax_mandel)
            self.cy = self._translate(ypos, self.screen1y, self.screen1y +
                                      self.screenHeight1, self.jp.ymin_mandel, self.jp.ymin_mandel)
            fractal = self.jp.julia(self.cx, self.cy)
            self.draw_fractal(fractal, False)
