#   CubeTimer

##  What is this project?
*   Rubik's Cube Stopwatch
*   Rubik's Cube Scramble recipe provider
*   Rubik's Cube Scramble Previewer
*   Rubik's Cube Simulator (currently available on `test_cube.py`)
##  How to use?
### Dependencies
*   python>3.10
*   PyQt5
*   numpy
### Installation
*   install dependencies
    *   `$ pip install PyQt5 numpy`
*   `$ git clone ~`d
*   `$ python main.py`

*   you can build this code on your own, by pyinstaller, etc.
    *   `$ pip install -U pyinstaller`
    *   `$ pyinstaller -w --onefile main.py`
### How to Use 
*   space bar
    *   stopwatch start-stop
    *   hold-and-release to start stopwatch
*   enter/return
    *   does same thing to reset button
*   history
    *   total average, total stddev, average of recent 5
    *   time, Used Scramble information
*   scramble
    *   provide fully random, but not redundant scramble
    *   provide scramble result image
*   Record
    *   save related records in same file
##  To be updated
*   save the files in user folder/directory, like `~`, or `%appdata%`
*   export recorded time in pretty image form
*   stylesheets
*   3d graphic aided Rubik's Cube Simulator
*   (hopefully) auto solver
