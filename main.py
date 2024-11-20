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


from graphics import *
import random
import time

# Screen dimensions
WIDTH, HEIGHT = 500, 500

# Load assets
PLAYER_IMAGE = "Assets/player1.png"
ENEMY_IMAGE = "Assets/player2.png"
BULLET_IMAGE = "Assets/Bullets/1.png"
ENEMY_BULLET_IMAGE = "Assets/Bullets/2.png"
LOGO_IMAGE = "Assets/image.png"

# Classes for game objects
class Player:
    def __init__(self, x, y, win):
        self.x = x
        self.y = y
        self.health = 100
        self.speed = 15
        self.win = win
        self.image = Image(Point(self.x, self.y), PLAYER_IMAGE)
        self.image.draw(win)

    def draw(self):
        self.image.move(0, 0)  # Keeps image intact without redrawing

    def move(self, key):
        if key == "Left" and self.x > 20:
            self.image.move(-self.speed, 0)
            self.x -= self.speed
        elif key == "Right" and self.x < WIDTH - 20:
            self.image.move(self.speed, 0)
            self.x += self.speed

    def shoot(self):
        return Bullet(self.x, self.y - 20, BULLET_IMAGE, -10, self.win)

class Enemy:
    def __init__(self, x, y, win):
        self.x = x
        self.y = y
        self.speed = 3
        self.win = win
        self.image = Image(Point(self.x, self.y), ENEMY_IMAGE)
        self.image.draw(win)

    def move(self):
        self.y += self.speed
        self.image.move(0, self.speed)

    def shoot(self):
        return Bullet(self.x, self.y + 20, ENEMY_BULLET_IMAGE, 5, self.win)

class Bullet:
    def __init__(self, x, y, image_file, speed, win):
        self.x = x
        self.y = y
        self.speed = speed
        self.win = win
        self.image = Image(Point(self.x, self.y), image_file)
        self.image.draw(win)

    def move(self):
        self.y += self.speed
        self.image.move(0, self.speed)

# Start screen
def start_screen(win):
    win.setBackground("black")
    logo = Image(Point(WIDTH // 2, HEIGHT // 3), LOGO_IMAGE)
    logo.draw(win)
    message = Text(Point(WIDTH // 2, HEIGHT // 2 + 50), "Tap to Play")
    message.setSize(20)
    message.setTextColor("white")
    message.draw(win)

    win.getMouse()
    logo.undraw()
    message.undraw()

# Outro screen
def outro_screen(win, score):
    win.setBackground("black")
    score_text = Text(Point(WIDTH // 2, HEIGHT // 3), f"Your Score: {score}")
    score_text.setSize(20)
    score_text.setTextColor("white")
    score_text.draw(win)

    restart_button = Rectangle(Point(WIDTH // 2 - 70, HEIGHT // 2), Point(WIDTH // 2 + 70, HEIGHT // 2 + 40))
    restart_button.setFill("green")
    restart_button.draw(win)
    restart_label = Text(restart_button.getCenter(), "Restart")
    restart_label.setSize(16)
    restart_label.draw(win)

    home_button = Rectangle(Point(WIDTH // 2 - 70, HEIGHT // 2 + 60), Point(WIDTH // 2 + 70, HEIGHT // 2 + 100))
    home_button.setFill("blue")
    home_button.draw(win)
    home_label = Text(home_button.getCenter(), "Home")
    home_label.setSize(16)
    home_label.draw(win)

    while True:
        click = win.getMouse()
        if restart_button.getP1().getX() <= click.getX() <= restart_button.getP2().getX() and \
           restart_button.getP1().getY() <= click.getY() <= restart_button.getP2().getY():
            score_text.undraw()
            restart_button.undraw()
            restart_label.undraw()
            home_button.undraw()
            home_label.undraw()
            return "restart"

        if home_button.getP1().getX() <= click.getX() <= home_button.getP2().getX() and \
           home_button.getP1().getY() <= click.getY() <= home_button.getP2().getY():
            score_text.undraw()
            restart_button.undraw()
            restart_label.undraw()
            home_button.undraw()
            home_label.undraw()
            return "home"

# Game loop
def game_loop(win):
    player = Player(WIDTH // 2, HEIGHT - 40, win)
    enemies = []
    bullets = []
    enemy_bullets = []
    score = 0
    running = True

    while running:
        key = win.checkKey()

        if key == "BackSpace":
            running = False

        if key in ["Left", "Right"]:
            player.move(key)

        player.draw()

        # Spawn enemies
        if random.randint(0, 100) < 3:
            enemies.append(Enemy(random.randint(20, WIDTH - 20), 20, win))

        # Update and draw enemies
        for enemy in enemies[:]:
            enemy.move()

            if random.randint(0, 100) < 3:
                enemy_bullets.append(enemy.shoot())

            if enemy.y > HEIGHT:
                enemies.remove(enemy)

        # Update and draw bullets
        for bullet in bullets[:]:
            bullet.move()

            for enemy in enemies[:]:
                if abs(bullet.x - enemy.x) < 20 and abs(bullet.y - enemy.y) < 20:
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 10
                    break

            if bullet.y < 0:
                bullets.remove(bullet)

        for e_bullet in enemy_bullets[:]:
            e_bullet.move()

            if abs(e_bullet.x - player.x) < 20 and abs(e_bullet.y - player.y) < 20:
                running = False
                break

            if e_bullet.y > HEIGHT:
                enemy_bullets.remove(e_bullet)

        time.sleep(0.02)

    return score

# Main function
def main():
    win = GraphWin("Aero Blasters", WIDTH, HEIGHT)
    while True:
        start_screen(win)
        score = game_loop(win)
        action = outro_screen(win, score)
        if action == "home":
            continue
        elif action == "restart":
            pass

    win.close()

if __name__ == "__main__":
    main()
