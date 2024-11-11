#Logan Marko, CS-125, Group 1
#Starting screen and game screen of space flight
from graphics5 import *


def screenTransition(x1,y1,x2,y2):
    """
    Draws and undraws a screen transition made up of expanding rectangles
    """
    screenTransitionSquare = Rectangle(Point(x1,y1), Point(x2,y2))
    screenTransitionSquare.draw(mainWindow)
    if (x1 < 500) and (y1 < 500) and (x2 < 500) and (y2 < 500):
        screenTransition((x1+5),(y1+5),(x2+10),(y2+10))
    for i in range(200):
        screenTransitionSquare.undraw()

def gameStart():
    """
    Converts from the title screen to the game level
    """
    title.undraw()
    playButtonText.undraw()
    playButton.undraw()
    screenTransition(0,0,10,10)
         
def startScreen():
    """
    Opens the main menu of SpaceFlight
    """
    global mainWindow
    global title
    global playButton
    global playButtonText
    mainWindow = GraphWin("SpaceFlight", 500, 500)
    title = Text(Point(250,100), "Space Flight")
    title.setSize(36)
    title.setFace("courier")
    title.setStyle("bold italic")
    title.draw(mainWindow)
    playButton = Rectangle(Point(100,250), Point(400,350))
    playButton.draw(mainWindow)
    playButtonText = Text(Point(250,300), "Play")
    playButtonText.setSize(20)
    playButtonText.setFace("courier")
    playButtonText.setStyle("bold")
    playButtonText.draw(mainWindow)
    while True:
        playButtonClickTest = mainWindow.getMouse()
        if (playButtonClickTest.getX() > 100) and (playButtonClickTest.getX() < 400) and (playButtonClickTest.getY() > 250) and (playButtonClickTest.getY() < 350):
            gameStart()
            break

startScreen()
        

