# Importing the pygame library to create graphics in the game
# Random is imported to create random integers
import pygame
import random

# The imported libraries are then assigned to variables for easier use
rand = random
pg = pygame
# pygame is initialized
pg.init()

# Here the window dimensions are created, and the clock variable is created to keep track of the timing in the game
screen_width = 1024
screen_height = 640
dimensions = (screen_width, screen_height)
clock = pg.time.Clock()

# Common colors are being made to be used later on that would fit the theme
black = (0, 0, 0)
gray = (75, 75, 75)
dark_gray = (50, 50, 50)
white = (255, 255, 255)

# Lines 25-26 create the window of the game and set a caption to the window
game_screen = pg.display.set_mode(dimensions)
pg.display.set_caption("Asteroids")

# Lines 30-32 initialize positions for "stars" that will be in the background of the screen in the list assigned to
# "positions"
positions = []
for i in range(150):
    positions.append([rand.randint(3, screen_width - 3), rand.randint(3, screen_height - 3)])

# Lines 35-39 load an image for a spaceship with no background and change its size to desired dimensions in lines 36-37
shooter = pg.image.load("Images/spaceship.png").convert()
shooter.set_colorkey(white)
shooter_w = 90
shooter_h = 90
shooter = pg.transform.scale(shooter, (shooter_w, shooter_h))

# Lines 43-45 initialize a list for the positions of the objective
# There is also the width and height of the objective
ores = []
ore_w = 50
ore_h = 50

# This variable is created to keep track of points
points = 0


# The abstraction stars() first fills the screen with black, and then iterates through the list with
# the star positions and draws circles at those coordinates
def stars():
    game_screen.fill(black)
    for j in range(len(positions)):
        x_y = [positions[j][0], positions[j][1]]
        pg.draw.circle(game_screen, white, x_y, 2)


# the text_render abstraction uses various parameters to create a surface on which some text will be displayed
# then text is rendered onto that surface and the surface is rendered onto the main screen
def text_render(text, x, y, width, height, font_size):
    font = pygame.font.Font('freesansbold.ttf', font_size)
    message = font.render(text, True, white)
    text_rect = message.get_rect()
    text_rect.center = (x + width // 2, y + height // 2)
    game_screen.blit(message, text_rect)


# draw_rect draws a rectangle using the given parameters
def draw_rect(x, y, width, height, color):
    pg.draw.rect(game_screen, color, [x, y, width, height])


# the button method creates a button that can create an event
# the method first assigns the status of a mouse press and its position to two variables
# then it checks for the the position of the cursor to see what color the rectangle should be drawn, if the mouse is
# on the button it changes color, and when it isn't the button goes back to the normal color, on top of the rectangle
# text is drawn if the cursor hovers on the button and it presses down, the event occurs
def button(x, y, width, height, font_size, r_color, p_color, text, event=None):
    mouse_pos = pg.mouse.get_pos()
    press_stat = pg.mouse.get_pressed(3)

    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        draw_rect(x, y, width, height, p_color)
        if press_stat[0] == 1 and event is not None:
            event()

    else:
        draw_rect(x, y, width, height, r_color)
    text_render(text, x, y, width, height, font_size)


# The set_bg method takes an image, loads it, makes it more transparent and then renders it on the screen
def set_bg(img):
    bg = pg.image.load(img).convert_alpha()
    bg.set_alpha(120)
    game_screen.blit(bg, (0, 0))


# draw_shooter takes x and y coordinates as parameters and then draws the spaceship on the screen
def draw_shooter(x, y):
    game_screen.blit(shooter, (x, y))


# draw_ast uses x-y coordinates to draw an asteroid onto the screen, this is a gray circle
def draw_ast(x, y):
    pg.draw.circle(game_screen, dark_gray, (x, y), 35)


# the spawn method takes the coordinates of the shooter as parameters
# these coordinates are used to create spawn coordinates for the objective of the game for 9 objectives
# for 9 iterations, a random coordinate is created for an "ore" then, the coordinate is checked to see if it is close
# to the spaceship
# while the coordinate is close, a new coordinate is created until it is far enough from the shooter
# then the image for the ore is loaded and transformed, after this, the coordinates, the image and a False value are
# added to the "ores" list as a smaller list
# the False value is added to represent whether or not the ore has been collected
def spawn(s_x, s_y):
    for o in range(9):
        o_x = rand.randint(50, screen_width - 50)
        while s_x - 100 < o_x < s_x + shooter_w + 100:
            o_x = rand.randint(27, screen_width - 50)
        o_y = rand.randint(50, screen_height - 50)
        while s_y - 100 < o_y < s_y + shooter_h + 100:
            o_y = rand.randint(50, screen_height - 50)
        ore = pg.image.load("Images/gold_ore.png").convert()
        ore.set_colorkey(black)
        ore = pg.transform.scale(ore, (ore_w, ore_h))

        ores.append([(o_x, o_y), False, ore])


# the check method is another algorithm that uses the shooter coordinates to check if the shooter has collected an ore
# it iterates through all the lists in the ores list to compare positions through if statements
# if the shooter is on the ore, the points variable increases and the ore's status is changed to true so it is not
# drawn anymore
def check(s_x, s_y):
    global points
    for obj in ores:
        o_x = obj[0][0]
        o_y = obj[0][1]
        if o_y < s_y < o_y + ore_h or o_y < s_y + shooter_h < o_y + ore_h:
            if o_x < s_x < o_x + ore_w or o_x < s_x + shooter_w < o_x + ore_w:
                if obj[1] is False:
                    obj[1] = True
                    points += 1


# This method is an abstraction for the main screen, this is done so that with a button press the screen can be changed
# On the main screen there is the background, there is text with the name of the game, and there are two buttons to
# start the game or quit the game
# In the method there is an event loop which checks for user input to trigger an event in the game, this is controlled
# by the closed variable, as long as it is false the loop continues
# At the end of the method, there is an update command and a tick command which tells the game to update a certain
# number of times per second
def main_screen():
    closed = False
    set_bg("Images/space.jpg")

    while not closed:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        text_render("Asteroids", 400, 100, 200, 100, 75)
        button(250, 450, 150, 75, 30, black, gray, "START", ingame_loop)
        button(600, 450, 150, 75, 30, black, gray, "QUIT", quit)

        pg.display.update()
        clock.tick(20)


# This is similar to main screen, but, it is triggered when the player wins the game, there are two buttons to either
# play again or quit the game
def win():
    closed = False

    while not closed:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        text_render("YOU WON", 400, 100, 200, 100, 75)
        button(250, 450, 200, 75, 30, dark_gray, gray, "PLAY AGAIN", ingame_loop)
        button(600, 450, 150, 75, 30, dark_gray, gray, "QUIT", quit)

        pg.display.update()
        clock.tick(20)


# This method starts off by initializing coordinates for the shooter, and the asteroid
# The speed for the shooter is also changed
# Then the spawn algorithm is used to create the coordinates for the ores
def ingame_loop():
    # These statements are to use variables defined outside of the method
    global points
    global ores

    closed = False

    s_x = screen_width / 2 - 40
    s_y = screen_height / 2 - 40

    ast_x = -35
    ast_y = rand.randint(36, screen_height - 36)
    asp = 10
    ast_r = 35

    vert_move = 0
    side_move = 0

    spawn(s_x, s_y)

    # The event loop checks for arrow key inputs to control the movement of the ship
    while not closed:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    side_move -= 4
                if event.key == pg.K_RIGHT:
                    side_move += 4
                if event.key == pg.K_UP:
                    vert_move -= 4
                if event.key == pg.K_DOWN:
                    vert_move += 4
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                    side_move = 0
                if event.key == pg.K_UP or event.key == pg.K_DOWN:
                    vert_move = 0

        s_y += vert_move
        s_x += side_move

        # The next if statements check for the shooters position to be able to draw it on the opposite edge if it goes
        # off screen
        if s_x > screen_width:
            s_x = -shooter_w
        elif s_x + shooter_w < 0:
            s_x = screen_width

        if s_y + shooter_h < 0:
            s_y = screen_height
        elif s_y > screen_height:
            s_y = -shooter_h

        # The stars are drawn
        stars()

        # The text keeping track of score is drawn
        text_render('Score: {}'.format(points), 0, 0, 100, 50, 25)

        # This checks if the ship has been hit by an asteroid, and if so it opens the "hit" screen
        if ast_y - ast_r < s_y < ast_y + ast_r or ast_y - ast_r < s_y + shooter_h < ast_y + ast_r:
            if ast_x - ast_r < s_x < ast_x + ast_r or ast_x - ast_r < s_x + shooter_w < ast_x + ast_r:
                points = 0
                ores = []
                hit()

        # The ores are drawn
        for obj in ores:
            if obj[1] is False:
                game_screen.blit(obj[2], (obj[0][0], obj[0][1]))

        # If the player collects all ores, the win screen is opened
        if points == 9:
            points = 0
            ores = []
            win()

        # The check algorithm is used to see if the player collected an ore
        check(s_x, s_y)

        # This changes the asteroid x position from left to right
        ast_x += asp

        # This if statement checks if the asteroid has left the screen, if true it spawns the asteroid back on the left
        # side
        if ast_x > screen_width + 35:
            ast_x = -35
            ast_y = rand.randint(36, screen_height - 36)
            asp *= 1.08

        # The asteroid is drawn at specified coordinates
        draw_ast(ast_x, ast_y)
        # The shooter is drawn at specified coordinates
        draw_shooter(s_x, s_y)

        # The screen updates 60 times a second
        pg.display.update()
        clock.tick(60)


# This opens he hit screen when the player is hit by an asteroid, it has buttons for the player to play again or quit
def hit():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        text_render("Your ship has been hit", screen_width // 2 - 75, screen_height * 0.25, 200, 100, 75)

        pg.display.update()
        clock.tick(30)

        button(screen_width // 2 - 80, 300, 150, 75, 20, dark_gray, gray, "PLAY AGAIN", ingame_loop)
        button(screen_width // 2 - 80, 400, 150, 75, 30, dark_gray, gray, "QUIT", quit)


# The main screen method is used, and from there the player can play the game
# After the method terminates, the game closes
main_screen()
pg.quit()
quit()

# The pygame library used in this program code is an open source library maintained by the pygame community
# That library is used throughout the program, the citation for the code if below

##################################################
# Title: pygame
# Author: pygame community
# Date: April 10th, 2021
# Code Version: 2.0.1
# Availability: https://github.com/pygame/pygame
##################################################
