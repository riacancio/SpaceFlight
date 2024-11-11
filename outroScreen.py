from graphics import *

# Function to display the outro screen
def show_outro(score, game_window):
    # Create a new window for the outro
    outro_window = GraphWin("Game Over", 500, 500)
    outro_window.setBackground("black")

    # Display the player's score
    score_text = Text(Point(250, 100), f"Your Score: {score}")
    score_text.setSize(20)
    score_text.setTextColor("white")
    score_text.draw(outro_window)

    # Create the Home button
    home_button = Rectangle(Point(150, 200), Point(350, 250))
    home_button.setfill("blue")
    home_button.draw(outro.window)
    home_text = Text(Point(250, 225), "Home")
    home_text.setTextColor("white")
    home_text.draw(outro_window)

    # Create the Restart button
    restart_button = Rectangle(Point(150, 275), Point(350, 325))
    restart_button.setFill("green")
    restart_button.draw(outro_window)
    restart_text = Text(Point(250, 300), "Restart")
    restart_text.setTextColor("white")
    restart_text.draw(outro_window)

    # Wait for mouse click
    click_point = outro_window.getMouse()

    # Check if Home button was clicked
    if home_button.getP1().getX90 < click_point.getX() < home_button.getP2().getX() and \
       home_button.getP1().getY() < click_point.getY() < home_button.getP2().getY():
        outro_window.close()
        # Return to home screen here
        print("Home button clicked")
        # define home screen here: show_home_screen()

    # Check if Restart button was clicked
    elif restart_button.getP1().getX() < click_point.getX() < restart_button.getP2().getX() and \
         restart_button.getP1().getY() < click_point.getY() < restart_button.getP2().getY():
          outro_window.close()
        # Here you would restart the game (reset the game state)
          print("Restart button clicked")
        # Call your restart function here

def toggle_mute():
    global is_muted
    
    if is_muted:
        # Unmute: restore the original volume
        background_music.set_volume(original_volume)
        shoot_sound.set_volume(1.0)  # Full volume for shooting sounds
        explosion_sound.set_volume(1.0)  # Full volume for explosion sounds
    else:
        # Mute: set the volume to 0
        background_music.set_volume(0)
        shoot_sound.set_volume(0)
        explosion_sound.set_volume(0)
    
    # Toggle mute state
    is_muted = not is_muted
    print("Muted" if is_muted else "Unmuted")


    
          
        

    

    
