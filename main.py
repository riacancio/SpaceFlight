from graphics import *
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

# Classes for Game Elements

class Player:
    def __init__(self, x, y):
        self.shape = Rectangle(Point(x - 15, y - 15), Point(x + 15, y + 15))
        self.shape.setFill(BLUE)
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
        self.shape = Rectangle(Point(x - 15, y - 15), Point(x + 15, y + 15))
        self.shape.setFill(RED)
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
        self.shape = Rectangle(Point(x - 2, y - 5), Point(x + 2, y + 5))
        self.shape.setFill(WHITE)
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

win.close()
