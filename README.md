# JuliaPlayground
Julia Playground is an interactive gui (tkinter), built in python that allows the user to display and interact with the mandelbrot set and corresponding Julia sets.

![Screenshot of JuliaPlayground](https://github.com/FrontRowWithJ/JuliaPlayground/blob/master/Julia_PlayGround_Screenshot.png)
#### Use
`Windows:` Double-click on `__init__.py` or if you're using cmd, navigate to the file directiory where the scripts are located and type: `python __init__.py` _(I recommend the later approach because it will be easier to figure out what dependencies are missing.)_  
`Linux/macOS: ` Open the cli and type: `python3 __init__.py`
  
#### Dependencies
* `Python 3 or later`
* `Tkinter`
* `Numba`
* `Numpy`
  
#### Installation  
`Windows` For installing the libraries, I recommend using pip instead of Anaconda to avoid the potential error of missing DLL files.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Anaconda:  `conda install [library name]` or `conda update [library name]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pip:  (The command for Windows installation is the same as Linux/macOS)  
`Linux/macOS:` If you have pip installed, open the cli and type `pip install [library name]`

#### Issues
One major issue I have found is finding a fast enough image renderer that could allow dynamically updating the julia set with a reasonable framerate. If you could suggest any, please feel free to email me at `adebusum@tcd.ie`
