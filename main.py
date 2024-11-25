#Python Co-Design Project, Group 1
#Space Flight, a Space Invaders-esque game
#Riya Bhurki
#CJ Gordon
#Isabella Aikey
#Logan Marko


from graphics5 import *
import time
import random


# load in the assets
playerShipImage = "Assets/mediumPlayer.png"
enemyShipImage = "Assets/mediumEnemy.png"
logoImage = "Assets/sfLogo.png"


# define the window size
windowWidth, windowHeight = 400, 600

# define the start screen
def startScreen(win):
    win.setBackground("black")
    
    logo = Image(Point(windowWidth // 2, windowHeight // 3), logoImage)
    logo.draw(win)
    
    # Button for clicking to play
    playButton = Rectangle(Point(windowWidth // 2 - 100, windowHeight // 2 + 20), 
                           Point(windowWidth // 2 + 100, windowHeight // 2 + 80))
    playButton.setFill("blue")
    playButton.draw(win)
    
    playMessage = Text(Point(windowWidth // 2, windowHeight // 2 + 50), "Click to Play")
    playMessage.setSize(20)
    playMessage.setTextColor("white")
    playMessage.draw(win)
    
    # Wait for the user to click the button
    while True:
        click = win.getMouse()
        # Check if the click is inside the button
        if (playButton.getP1().getX() <= click.getX() <= playButton.getP2().getX()) and \
           (playButton.getP1().getY() <= click.getY() <= playButton.getP2().getY()):
            break  # Proceed to the next screen when clicked

    # Remove the button and message after clicking
    playButton.undraw()
    playMessage.undraw()
    logo.undraw()


# define the player, enemies, and their respective laser bullets
class Player:
    def __init__(self, win, x, y):
        self.x = x
        self.y = y
        self.image = Image(Point(self.x, self.y), playerShipImage)
        self.image.draw(win)
        self.health = 100
        self.speed = 5

    def draw(self):
        self.image.move(0, 0)  # keeps the image intact without redrawing

    def move(self, key):
        if key == "Left" and self.x > 20:
            self.image.move(-self.speed, 0)
            self.x -= self.speed
        elif key == "Right" and self.x < windowWidth - 20:
            self.image.move(self.speed, 0)
            self.x += self.speed
        
    def shoot(self, win):
        return laserBullet(win, self.x, self.y - 10)

    def isAlive(self):
        return self.health > 0

    def destroy(self):
        self.image.undraw()


class Enemy:
    def __init__(self, win, x, y):
        self.x = x
        self.y = y
        self.speed = 1
        self.win = win
        self.image = Image(Point(self.x, self.y), enemyShipImage)
        self.image.draw(win)

    def move(self):
        self.y += self.speed
        self.image.move(0, self.speed)

    def shoot(self, win):
        return enemyLaserBullet(win, self.x, self.y + 10)

    def destroy(self):
        self.image.undraw()

    def isOffScreen(self):
        return self.y > windowHeight


class laserBullet:
    def __init__(self, win, x, y):
        self.shape = Rectangle(Point(x - 10, y - 10), Point(x + 10, y + 20))
        self.shape.setFill("white")
        self.shape.draw(win)
        self.x = x
        self.y = y

    def playerMove(self):
        self.shape.move(0, -10)  # move player's bullets upward
        self.y -= 5

    def isOffScreen(self):
        return self.y < 0


class enemyLaserBullet:
    def __init__(self, win, x, y):
        self.shape = Rectangle(Point(x - 10, y - 10), Point(x + 10, y + 20))
        self.shape.setFill("red")
        self.shape.draw(win)
        self.x = x
        self.y = y

    def enemyMove(self): # move enemy's bullets downward
        self.shape.move(0, 10) 
        self.y += 10

    def isOffScreen(self):
        return self.y < 0


def detectCollision(obj1, obj2):
    # simplified collision detection based on object positions
    dx = abs(obj1.x - obj2.x)
    dy = abs(obj1.y - obj2.y)
    return dx < 15 and dy < 15


def gameLoop(win):
    global player
    player = Player(win, windowWidth // 2, windowHeight - 50)
    global laserBullets 
    laserBullets = []
    global enemies
    enemies = []
    global enemyLaserBullets
    enemyLaserBullets = []

    score = 0
    running = True

    # Initialize the last enemy spawn time
    last_enemy_spawn_time = time.time()  # This tracks when the last enemy was spawned
    spawn_interval = 2  # Time interval for spawning enemies (2 seconds)

    while running:
        # handle keyboard input
        key = win.checkKey()
        if key == "BackSpace":
            running = False
        if key == "Left" and player.x > 20:
            player.move(key)
        elif key == "Right" and player.x < windowWidth - 20:
            player.move(key)
        elif key == "space":
            laserBullets.append(player.shoot(win)) 

        # Spawns enemies with a delay of 2 seconds
        current_time = time.time()  # Get the current time
        if len(enemies) < 3 and (current_time - last_enemy_spawn_time > spawn_interval):
            enemies.append(Enemy(win, random.randint(20, windowWidth - 20), 20))
            last_enemy_spawn_time = current_time  # Reset the timer after spawning an enemy

        for enemy in enemies[:]:
            enemy.move()
            if enemy.isOffScreen():
                enemy.destroy()
                enemies.remove(enemy)
            if detectCollision(player, enemy):
                player.health -= 10
                enemy.destroy()
                enemies.remove(enemy)
            if random.randint(0, 250) < 2:
                enemyLaserBullets.append(enemy.shoot(win))
        
        # update and move all bullets
        for laserBullet in laserBullets[:]:
            laserBullet.playerMove()
            if laserBullet.isOffScreen():
                laserBullet.shape.undraw()
                laserBullets.remove(laserBullet)
            else:
                for enemy in enemies[:]:
                    if abs(laserBullet.x - enemy.x) < 65 and abs(laserBullet.y - enemy.y) < 65:
                        enemy.destroy()
                        enemies.remove(enemy)
                        laserBullet.shape.undraw()
                        laserBullets.remove(laserBullet)
                        score += 10
                        break
        
        for enemyLaserBullet in enemyLaserBullets[:]:
            enemyLaserBullet.enemyMove()
            if abs(enemyLaserBullet.x - player.x) < 30 and abs(enemyLaserBullet.y - player.y) < 30:
                player.health -= 100
            if enemyLaserBullet.isOffScreen():
                enemyLaserBullet.shape.undraw()
                enemyLaserBullets.remove(enemyLaserBullet)

        # check game over condition
        if not player.isAlive():
            return score

        time.sleep(0.016)  # 60 FPS delay


def outroScreen(win, score):
    win.setBackground("black")
    scoreText = Text(Point(windowWidth // 2, windowHeight // 3), f"Your Score: {score}")
    scoreText.setSize(20)
    scoreText.setTextColor("white")
    scoreText.draw(win)

    homeButton = Rectangle(Point(windowWidth // 2 - 70, windowHeight // 2), Point(windowWidth // 2 + 70, windowHeight // 2 + 40))
    homeButton.setFill("green")
    homeButton.draw(win)
    homeLabel = Text(homeButton.getCenter(), "Home")
    homeLabel.setSize(16)
    homeLabel.draw(win)

    closeButton = Rectangle(Point(windowWidth // 2 - 70, windowHeight // 2 + 60), Point(windowWidth // 2 + 70, windowHeight // 2 + 100))
    closeButton.setFill("blue")
    closeButton.draw(win)
    closeLabel = Text(closeButton.getCenter(), "Close")
    closeLabel.setSize(16)
    closeLabel.draw(win)

    while True:
        click = win.getMouse()
        if (closeButton.getP1().getX() <= click.getX() <= closeButton.getP2().getX()) and \
           (closeButton.getP1().getY() <= click.getY() <= closeButton.getP2().getY()):
            scoreText.undraw()
            closeButton.undraw()
            closeLabel.undraw()
            homeButton.undraw()
            homeLabel.undraw()
            player.destroy()
            for enemy in enemies[:]:
                enemy.destroy()
            for laserBullet in laserBullets[:]:
                laserBullet.shape.undraw()
            for enemyLaserBullet in enemyLaserBullets[:]:
                enemyLaserBullet.shape.undraw()
            return "close"
        
        
        if (homeButton.getP1().getX() <= click.getX() <= homeButton.getP2().getX()) and \
           (homeButton.getP1().getY() <= click.getY() <= homeButton.getP2().getY()):
            scoreText.undraw()
            closeButton.undraw()
            closeLabel.undraw()
            homeButton.undraw()
            homeLabel.undraw()
            player.destroy()
            for enemy in enemies[:]:
                enemy.destroy()
            for laserBullet in laserBullets[:]:
                laserBullet.shape.undraw()
            for enemyLaserBullet in enemyLaserBullets[:]:
                enemyLaserBullet.shape.undraw()
            return "home"


def main():
    gameWindow = GraphWin("Space Flight", windowWidth, windowHeight)
    while True:
        startScreen(gameWindow)
        finalScore = gameLoop(gameWindow)
        playAgain = outroScreen(gameWindow, finalScore)
        if playAgain == "close":
            gameWindow.close()
            break
        elif playAgain == "home":
            continue


if __name__ == "__main__":
    main()
