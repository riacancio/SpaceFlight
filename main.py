'''from graphics5 import *
import time
import random

# Setup Game Window
win_width, win_height = 288, 512
win = GraphWin("AeroBlasters", win_width, win_height)
win.setBackground("black")

# Colors
WHITE = "white"
BLUE = color_rgb(30, 144, 255)
RED = "red"
GREEN = "green"

# Load Images
player_img = "player.png"    # Image for player
enemy_img = "enemy.png"      # Image for enemy
bullet_img = "bullet.png"    # Image for bullet

# Classes for Game Elements

class Player:
    def __init__(self, x, y):
        self.shape = Image(Point(400, 300), "player1.png")  # Replacing rectangle with player image
        self.shape.draw(win)
        self.health = 100
        self.fuel = 100
        self.powerup = 0
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.shape.move(dx, dy)
        self.x += dx
        self.y += dy

    def shoot(self):
        # Create bullet(s) at the player's current position
        return Bullet(self.x, self.y - 15)  # Shoot bullet upwards

    def update_health_fuel(self):
        self.health -= 1  # Example health decrement
        self.fuel -= 0.1  # Example fuel decrement

    def is_alive(self):
        return self.health > 0 and self.fuel > 0

class Enemy:
    def __init__(self, x, y, type):
        self.shape = Image(Point(x, y), enemy_img)  # Replacing rectangle with enemy image
        self.shape.draw(win)
        self.x = x
        self.y = y
        self.health = 100
        self.type = type

    def move(self):
        self.shape.move(0, 5)  # Move enemy downward
        self.y += 5

    def is_off_screen(self):
        return self.y > win_height

class Bullet:
    def __init__(self, x, y):
        self.shape = Image(Point(x, y), bullet_img)  # Replacing rectangle with bullet image
        self.shape.draw(win)
        self.x = x
        self.y = y

    def move(self):
        self.shape.move(0, -10)  # Move bullet upward
        self.y -= 10

    def is_off_screen(self):
        return self.y < 0

def detect_collision(obj1, obj2):
    # Simplified collision detection based on object positions
    dx = abs(obj1.x - obj2.x)
    dy = abs(obj1.y - obj2.y)
    return dx < 15 and dy < 15

def update_health_fuel_bar(player):
    # Health Bar
    health_bar = Rectangle(Point(20, 20), Point(20 + player.health, 30))
    health_bar.setFill(GREEN)
    health_bar.draw(win)
    # Fuel Bar
    fuel_bar = Rectangle(Point(20, 35), Point(20 + int(player.fuel), 45))
    fuel_bar.setFill(RED if player.fuel < 40 else GREEN)
    fuel_bar.draw(win)

# Main Game Loop

player = Player(win_width // 2, win_height - 50)
enemies = []
bullets = []

score = 0
running = True

while running:
    # Handle keyboard input
    key = win.checkKey()
    if key == "Left" and player.x > 20:
        player.move(-5, 0)
    elif key == "Right" and player.x < win_width - 20:
        player.move(5, 0)
    elif key == "space":
        bullets.append(player.shoot())

    # Generate new enemies periodically
    if random.randint(0, 100) < 5:
        enemy = Enemy(random.randint(10, win_width - 10), -50, random.randint(1, 3))
        enemies.append(enemy)

    # Update and move enemies
    for enemy in enemies[:]:
        enemy.move()
        if enemy.is_off_screen():
            enemy.shape.undraw()
            enemies.remove(enemy)
        elif detect_collision(player, enemy):
            player.health -= 10
            enemy.shape.undraw()
            enemies.remove(enemy)

    # Update and move bullets
    for bullet in bullets[:]:
        bullet.move()
        if bullet.is_off_screen():
            bullet.shape.undraw()
            bullets.remove(bullet)
        else:
            for enemy in enemies[:]:
                if detect_collision(bullet, enemy):
                    score += 10
                    enemy.shape.undraw()
                    enemies.remove(enemy)
                    bullet.shape.undraw()
                    bullets.remove(bullet)
                    break

    # Update player's health and fuel
    player.update_health_fuel()

    # Draw the health and fuel bars
    update_health_fuel_bar(player)

    # Check game over condition
    if not player.is_alive():
        game_over_text = Text(Point(win_width // 2, win_height // 2), "GAME OVER")
        game_over_text.setSize(24)
        game_over_text.setTextColor(RED)
        game_over_text.draw(win)
        running = False

    time.sleep(0.016)  # 60 FPS delay

win.close()'''


from graphics5 import *
import time
import random

# Global variables for mute state and score
is_muted = False
score = 0

# Start Screen Function
def start_screen():
    win = GraphWin("Aero Blasters", 500, 500)
    win.setBackground("black")

    title = Text(Point(250, 150), "Aero Blasters")
    title.setSize(36)
    title.setTextColor("white")
    title.setStyle("bold")
    title.draw(win)

    play_button = Rectangle(Point(150, 250), Point(350, 300))
    play_button.setFill("blue")
    play_button.draw(win)

    play_text = Text(Point(250, 275), "Tap to Play")
    play_text.setSize(20)
    play_text.setTextColor("white")
    play_text.draw(win)

    while True:
        click = win.getMouse()
        if 150 <= click.getX() <= 350 and 250 <= click.getY() <= 300:
            win.close()
            return True  # Proceed to the game screen

# Main Game Screen Function
def game_screen():
    global score
    win_width, win_height = 500, 500
    win = GraphWin("Aero Blasters", win_width, win_height)
    win.setBackground("black")

    # Player Class
    class Player:
        def __init__(self, x, y):
            self.shape = Image(Point(x, y), "Assets/player1.png")
            self.shape.draw(win)
            self.health = 100
            self.fuel = 100
            self.x = x
            self.y = y

        def move(self, dx, dy):
            self.shape.move(dx, dy)
            self.x += dx
            self.y += dy

        def shoot(self):
            return Bullet(self.x, self.y - 15)

        def update_health_fuel(self):
            self.health -= 1
            self.fuel -= 0.1

        def is_alive(self):
            return self.health > 0 and self.fuel > 0

    # Enemy Class
    class Enemy:
        def __init__(self, x, y):
            self.shape = Image(Point(x, y), "Assets/player2.png")
            self.shape.draw(win)
            self.x = x
            self.y = y

        def move(self):
            self.shape.move(0, 5)
            self.y += 5

        def is_off_screen(self):
            return self.y > win_height

    # Bullet Class
    class Bullet:
        def __init__(self, x, y):
            self.shape = Image(Point(x, y), "Assets/2.png")
            self.shape.draw(win)
            self.x = x
            self.y = y

        def move(self):
            self.shape.move(0, -10)
            self.y -= 10

        def is_off_screen(self):
            return self.y < 0

    # Helper Functions
    def detect_collision(obj1, obj2):
        dx = abs(obj1.x - obj2.x)
        dy = abs(obj1.y - obj2.y)
        return dx < 15 and dy < 15

    def update_health_fuel_bar(player):
        health_bar = Rectangle(Point(20, 20), Point(20 + player.health, 30))
        health_bar.setFill("green")
        health_bar.draw(win)
        fuel_bar = Rectangle(Point(20, 35), Point(20 + int(player.fuel), 45))
        fuel_bar.setFill("red" if player.fuel < 40 else "green")
        fuel_bar.draw(win)

    player = Player(win_width // 2, win_height - 50)
    enemies = []
    bullets = []
    score = 0
    running = True

    while running:
        key = win.checkKey()
        if key == "Left" and player.x > 20:
            player.move(-10, 0)
        elif key == "Right" and player.x < win_width - 20:
            player.move(10, 0)
        elif key == "space":
            bullets.append(player.shoot())

        if random.randint(0, 100) < 5:
            enemies.append(Enemy(random.randint(20, win_width - 20), -50))

        for enemy in enemies[:]:
            enemy.move()
            if enemy.is_off_screen():
                enemy.shape.undraw()
                enemies.remove(enemy)
            elif detect_collision(player, enemy):
                player.health -= 10
                enemy.shape.undraw()
                enemies.remove(enemy)

        for bullet in bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                bullet.shape.undraw()
                bullets.remove(bullet)
            else:
                for enemy in enemies[:]:
                    if detect_collision(bullet, enemy):
                        score += 10
                        enemy.shape.undraw()
                        enemies.remove(enemy)
                        bullet.shape.undraw()
                        bullets.remove(bullet)
                        break

        player.update_health_fuel()
        update_health_fuel_bar(player)

        if not player.is_alive():
            running = False

        time.sleep(0.016)

    win.close()
    return score

# Outro Screen Function
def outro_screen(score):
    win = GraphWin("Game Over", 500, 500)
    win.setBackground("black")

    score_text = Text(Point(250, 150), f"Your Score: {score}")
    score_text.setSize(20)
    score_text.setTextColor("white")
    score_text.draw(win)

    home_button = Rectangle(Point(100, 300), Point(200, 350))
    home_button.setFill("blue")
    home_button.draw(win)

    restart_button = Rectangle(Point(300, 300), Point(400, 350))
    restart_button.setFill("green")
    restart_button.draw(win)

    home_text = Text(Point(150, 325), "Home")
    home_text.setSize(15)
    home_text.setTextColor("white")
    home_text.draw(win)

    restart_text = Text(Point(350, 325), "Restart")
    restart_text.setSize(15)
    restart_text.setTextColor("white")
    restart_text.draw(win)

    while True:
        click = win.getMouse()
        if 100 <= click.getX() <= 200 and 300 <= click.getY() <= 350:
            win.close()
            return "home"
        elif 300 <= click.getX() <= 400 and 300 <= click.getY() <= 350:
            win.close()
            return "restart"

# Main Game Loop
while True:
    if start_screen():
        game_score = game_screen()
        choice = outro_screen(game_score)
        if choice == "home":
            continue
        elif choice == "restart":
            pass

