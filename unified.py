"""
TODO
* Resolve math behind CURE and DEATH
* Figure out point interpolation to make graph more pretty
* Label graph better
* Finishing touches
* web Interface?
"""

import arcadeplus as arcade
import time
import random

WIDTH = 1600
HEIGHT = 900

DOT_WIDTH = 640
DOT_HEIGHT = 480

INFECTION_RADIUS = 15
CHANCE_OF_INFECTION = 20
CURE_RATE = 300
DEATH_RATE = 1500
BASE_TIME = 11
PEOPLE_INFECTED = []

INFECTED = 0
DEAD = 0
CURED = 0

mouse_x = 0
mouse_y = 0
mouse_press = False
ball_pos = []
ball_mvmt = []
history = []
time_elapsed = 0
start = False
reset = True  # Button

slider_x = WIDTH / 2
slider_y = HEIGHT / 2
slide_color = arcade.color.BLUE
press = False  # Slider

slider_x1 = WIDTH / 2 - 70
slider_y1 = HEIGHT / 2 - 100
slide1_color = arcade.color.BLUE
press1 = False  # Slider

slider_x2 = WIDTH / 2 + 70
slider_y2 = HEIGHT / 2 - 200
slide2_color = arcade.color.BLUE
press2 = False  # Slider

population = 90
prev = 90
reset1 = False  # reset button
restart = False
graph_data = []

for i in range(population):
    ball_pos.append(
        [random.randrange(100, DOT_WIDTH - 100), random.randrange(100, DOT_HEIGHT - 100), arcade.color.BLACK, 0])
    ball_mvmt.append(random.randrange(-2, 3))
ball_pos[0][2] = arcade.color.RED
ball_pos[0][0] = DOT_WIDTH / 2
ball_pos[0][1] = DOT_HEIGHT / 2


def initilization():
    global ball_pos, population
    if population != prev:
        population = prev
        ball_pos = []
        for i in range(population):
            ball_pos.append(
                [random.randrange(100, DOT_WIDTH - 100), random.randrange(100, DOT_HEIGHT - 100), arcade.color.BLACK,
                 0])
            ball_mvmt.append(random.randrange(-2, 3))
        ball_pos[0][2] = arcade.color.RED
        ball_pos[0][0] = DOT_WIDTH / 2
        ball_pos[0][1] = DOT_HEIGHT / 2


def setup():
    arcade.open_window(WIDTH, HEIGHT, "TOHACKS SARS COV-2 Model")
    arcade.set_background_color(arcade.color.LIGHT_STEEL_BLUE)
    arcade.schedule(update, 1 / 60)

    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_mouse_press = on_mouse_press
    window.on_mouse_release = on_mouse_release
    window.on_mouse_motion = on_mouse_motion

    arcade.run()


def update(delta_time):
    if start:
        dots()
        graph_data.append([population - len(history) - 1, (len(history) + 1) - CURED - DEAD, CURED, DEAD, time_elapsed])
    elif not start:
        initilization()
    if restart:
        reset_data()


def on_draw():
    arcade.start_render()
    arcade.draw_rectangle_filled(WIDTH * 1 / 5 + 20, HEIGHT / 4 + 30, 640, 480, arcade.color.LIGHT_GREEN)
    for i in range(len(ball_pos)):
        arcade.draw_circle_filled(ball_pos[i][0], ball_pos[i][1], 5, ball_pos[i][2])
    for i in range(len(history)):
        arcade.draw_line(ball_pos[history[i][0]][0], ball_pos[history[i][0]][1], ball_pos[history[i][1]][0],
                         ball_pos[history[i][1]][1], arcade.color.RED)
    arcade.draw_circle_filled(10, 740, 5, arcade.color.BLACK)  # Unaffected
    arcade.draw_circle_filled(10, 720, 5, arcade.color.RED)  # Infected
    arcade.draw_circle_filled(10, 700, 5, arcade.color.GRAY)  # Cured
    arcade.draw_circle_filled(10, 680, 5, arcade.color.YELLOW)  # Dead
    arcade.draw_text(
        f'Number unaffected: {population - len(history) - 1}\nNumber infected: {(len(history) + 1)-CURED-DEAD}\nNumber cured: {CURED}\nNumber deceased: {DEAD}\nTime elapsed: {(time_elapsed):.2f}',
        20, HEIGHT / 2 + 200,
        arcade.color.BLACK, 18)
    if not start:
        draw_button(WIDTH - 100, 50, 100, 30, arcade.color.GREEN, 'Start', arcade.color.LIGHT_GREEN, arcade.color.RED)
    else:
        draw_button(WIDTH - 100, 50, 100, 30, arcade.color.GREEN, 'Pause', arcade.color.LIGHT_GREEN, arcade.color.RED)
    sliders()
    sliders1()
    sliders2()
    draw_reset_button(WIDTH / 2, HEIGHT / 2 - 300, 150, 50, arcade.color.RED, "Reset", arcade.color.SALMON_PINK,
                      arcade.color.PINK)
    graph()


def graph():
    middle_x = WIDTH * 3/4 + 70
    middle_y = HEIGHT * 3/4 - 100
    length = 500
    width = 500
    arcade.draw_rectangle_filled(middle_x, middle_y, length, width, arcade.color.WHITE)
    arcade.draw_line(middle_x - width/2, middle_y - length/2 + 20, middle_x + width/2, middle_y - length/2 + 20, arcade.color.BLACK)
    arcade.draw_line(middle_x - width/2 + 20, middle_y - length/2, middle_x - width/2 + 20, middle_y + length/2, arcade.color.BLACK)
    for point in graph_data:
        arcade.draw_point(point[4] * 3 + middle_x - width/2 + 20, point[0] * 3 + middle_y - length/2 + 20, arcade.color.BLACK, 5)
        arcade.draw_point(point[4] * 3 + middle_x - width/2 + 20, point[1] * 3 + middle_y - length/2 + 20, arcade.color.RED, 5)
        arcade.draw_point(point[4] * 3 + middle_x - width/2 + 20, point[2] * 3 + middle_y - length/2 + 20, arcade.color.GRAY, 5)
        arcade.draw_point(point[4] * 3 + middle_x - width/2 + 20, point[3] * 3 + middle_y - length/2 + 20, arcade.color.YELLOW, 5)


def dots():
    global ball_mvmt, position, ball_pos, time_elapsed, INFECTED
    for i in range(len(ball_mvmt)):
        if random.randrange(50) == 0:
            ball_mvmt[i] = random.randrange(-2, 3)
            if (ball_mvmt[i] == 0 and random.randrange(2) == 1):
                ball_mvmt[i] = 2
            elif ball_mvmt[i] == 0:
                ball_mvmt[i] = -2
    for i in range(len(ball_pos)):
        k = random.randrange(5)
        if ball_pos[i][0] >= DOT_WIDTH - 100 or ball_pos[i][1] >= DOT_HEIGHT - 100:
            ball_mvmt[i] = -1 * (abs(ball_mvmt[i]))
        if ball_pos[i][1] <= 100 or ball_pos[i][0] <= 100:
            ball_mvmt[i] = abs(ball_mvmt[i])
        if k == 0:
            ball_pos[i][0] += ball_mvmt[i]
            ball_pos[i][1] += ball_mvmt[i]
        elif k == 1:
            ball_pos[i][0] += ball_mvmt[i]
        elif k == 2:
            ball_pos[i][1] += ball_mvmt[i]
        elif k == 3:
            ball_pos[i][0] += ball_mvmt[i]
            ball_pos[i][1] -= ball_mvmt[i]
        else:
            ball_pos[i][0] -= ball_mvmt[i]
            ball_pos[i][1] += ball_mvmt[i]
    for i in range(len(ball_pos)):
        for j in range(i + 1, len(ball_pos)):
            if ball_pos[j][2] != ball_pos[i][2]:
                distance = ((ball_pos[j][0] - ball_pos[i][0]) ** 2 + (ball_pos[j][1] - ball_pos[i][1]) ** 2) ** (1 / 2)
                if distance <= INFECTION_RADIUS and random.randrange(1000) < 150:
                    if ball_pos[i][2] == arcade.color.RED and ball_pos[j][2] == arcade.color.BLACK:
                        ball_pos[j][2] = arcade.color.RED
                        ball_pos[j][3] = time.time()
                        INFECTED += 1
                        if [i, j] not in history:
                            history.append([i, j])
                        if ball_pos[j] not in PEOPLE_INFECTED:
                            PEOPLE_INFECTED.append(ball_pos[j])
                    elif ball_pos[j][2] == arcade.color.RED and ball_pos[i][2] == arcade.color.BLACK:
                        ball_pos[i][2] = arcade.color.RED
                        ball_pos[i][3] = time.time()
                        INFECTED += 1
                        if [j, i] not in history:
                            history.append([j, i])
                        if ball_pos[i] not in PEOPLE_INFECTED:
                            PEOPLE_INFECTED.append(ball_pos[i])
    time_elapsed += 0.05
    cure()
    mortality()


def sliders():
    global slide_color, slider_x, press, prev
    if slider_x - 5 <= mouse_x <= slider_x + 5 and slider_y - 13 <= mouse_y <= slider_y + 13:
        slide_color = arcade.color.GRAY
        if mouse_press:
            slide_color = arcade.color.DARK_GRAY
            press = True
            if 700 < slider_x < 900:
                slider_x = mouse_x
    elif not mouse_press and press:
        slide_color = arcade.color.BLUE
        press = False
    elif press:
        if 700 < slider_x < 900:
            slider_x = mouse_x
            slide_color = arcade.color.DARK_GRAY
    else:
        slide_color = arcade.color.BLUE
    if slider_x >= 900:
        slider_x = 899
    elif slider_x <= 700:
        slider_x = 701
    arcade.draw_rectangle_outline(WIDTH / 2, HEIGHT / 2, 200, 5, arcade.color.BLACK)
    arcade.draw_rectangle_filled(slider_x, slider_y, 10, 25, slide_color)
    arcade.draw_text(f'Population: {((slider_x - 700) // 2) + 40}', WIDTH / 2 - 20, HEIGHT / 2 - 30, arcade.color.BLACK)
    prev = int(((slider_x - 700) // 2) + 40)


def sliders1():
    global slide1_color, slider_x1, press1, DEATH_RATE
    if slider_x1 - 5 <= mouse_x <= slider_x1 + 5 and slider_y1 - 13 <= mouse_y <= slider_y1 + 13:
        slide1_color = arcade.color.GRAY
        if mouse_press:
            slide1_color = arcade.color.DARK_GRAY
            press1 = True
            if 700 < slider_x1 < 900:
                slider_x1 = mouse_x
    elif not mouse_press and press1:
        slide1_color = arcade.color.BLUE
        press1 = False
    elif press1:
        if 700 < slider_x1 < 900:
            slider_x1 = mouse_x
            slide1_color = arcade.color.DARK_GRAY
    else:
        slide1_color = arcade.color.BLUE
    if slider_x1 >= 900:
        slider_x1 = 899
    elif slider_x1 <= 700:
        slider_x1 = 701
    arcade.draw_rectangle_outline(WIDTH / 2, HEIGHT / 2 - 100, 200, 5, arcade.color.BLACK)
    arcade.draw_rectangle_filled(slider_x1, slider_y1, 10, 25, slide1_color)
    if slider_x1 >= 833:
        arcade.draw_text(f'Death Rate: High', WIDTH / 2 - 20, HEIGHT / 2 - 130,
                         arcade.color.BLACK)
    elif slider_x1 <= 777:
        arcade.draw_text(f'Death Rate: Low', WIDTH / 2 - 20, HEIGHT / 2 - 130,
                         arcade.color.BLACK)
    else:
        arcade.draw_text(f'Death Rate: Medium', WIDTH / 2 - 20, HEIGHT / 2 - 130,
                         arcade.color.BLACK)


    DEATH_RATE = (200 - (slider_x1 - 700)) * 10


def sliders2():
    global slide2_color, slider_x2, press2, CURE_RATE
    if slider_x2 - 5 <= mouse_x <= slider_x2 + 5 and slider_y2 - 13 <= mouse_y <= slider_y2 + 13:
        slide2_color = arcade.color.GRAY
        if mouse_press:
            slide2_color = arcade.color.DARK_GRAY
            press2 = True
            if 700 < slider_x2 < 900:
                slider_x2 = mouse_x
    elif not mouse_press and press2:
        slide2_color = arcade.color.BLUE
        press2 = False
    elif press2:
        if 700 < slider_x2 < 900:
            slider_x2 = mouse_x
            slide2_color = arcade.color.DARK_GRAY
    else:
        slide2_color = arcade.color.BLUE
    if slider_x2 >= 900:
        slider_x2 = 899
    elif slider_x2 <= 700:
        slider_x2 = 701
    arcade.draw_rectangle_outline(WIDTH / 2, HEIGHT / 2 - 200, 200, 5, arcade.color.BLACK)
    arcade.draw_rectangle_filled(slider_x2, slider_y2, 10, 25, slide2_color)

    if slider_x2 >= 833:
        arcade.draw_text(f'Cure Rate: High', WIDTH / 2 - 20, HEIGHT / 2 - 230,
                         arcade.color.BLACK)
    elif slider_x2 <= 777:
        arcade.draw_text(f'Cure Rate: Low', WIDTH / 2 - 20, HEIGHT / 2 - 230,
                         arcade.color.BLACK)
    else:
        arcade.draw_text(f'Cure Rate: Medium', WIDTH / 2 - 20, HEIGHT / 2 - 230,
                         arcade.color.BLACK)

    CURE_RATE = (200 - (slider_x2 - 700)) * 10


def draw_button(x, y, button_width, button_height, colour_default, text,
                colour_hover, colour_press):
    global start, reset
    if x + (button_width / 2) > mouse_x > x - (button_width / 2) and \
            y - (button_height / 2) < mouse_y < y + (button_height / 2) and \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, button_width, button_height,
                                     colour_press)
        if not start and reset:
            start = True
            reset = False
        elif start and reset:
            start = False
            reset = False
    elif x + (button_width / 2) > mouse_x > x - (button_width / 2) and \
            y - (button_height / 2) < mouse_y < y + (button_height / 2) and \
            not mouse_press:
        arcade.draw_rectangle_filled(x, y, button_width, button_height,
                                     colour_hover)
        reset = True
    else:
        arcade.draw_rectangle_filled(x, y, button_width, button_height,
                                     colour_default)
    arcade.draw_text(text, x - 25, y - 7, arcade.color.BLACK, 12, bold=True)


def draw_reset_button(x, y, button_width, button_height, colour_default, text,
                      colour_hover, colour_press):
    global restart, reset1
    if x + (button_width / 2) > mouse_x > x - (button_width / 2) and \
            y - (button_height / 2) < mouse_y < y + (button_height / 2) and \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, button_width, button_height,
                                     colour_press)
        if not start and reset:
            restart = True
            reset1 = False
        elif start and reset:
            restart = False
            reset1 = False
    elif x + (button_width / 2) > mouse_x > x - (button_width / 2) and \
            y - (button_height / 2) < mouse_y < y + (button_height / 2) and \
            not mouse_press:
        arcade.draw_rectangle_filled(x, y, button_width, button_height,
                                     colour_hover)
        reset1 = True
    else:
        arcade.draw_rectangle_filled(x, y, button_width, button_height,
                                     colour_default)
    arcade.draw_text(text, x - 25, y - 7, arcade.color.BLACK, 12, bold=True)


def reset_data():
    global history, ball_pos, ball_mvmt, time_elapsed, start, reset, slider_x, slider_y, slide_color, press, slider_x1, slider_y1, slide1_color, press1, slider_x2
    global slider_y2, slide2_color, press2, population, prev, restart, graph_data, CURED, INFECTED, DEAD
    global INFECTION_RADIUS
    global CHANCE_OF_INFECTION
    global DEATH_RATE, CURE_RATE, BASE_TIME, PEOPLE_INFECTED
    history = []
    ball_pos = []
    ball_mvmt = []
    time_elapsed = 0
    start = False
    reset = True  # Button

    slider_x = WIDTH / 2
    slider_y = HEIGHT / 2
    slide_color = arcade.color.BLUE
    press = False  # Slider

    slider_x1 = WIDTH / 2 - 70
    slider_y1 = HEIGHT / 2 - 100
    slide1_color = arcade.color.BLUE
    press1 = False  # Slider

    slider_x2 = WIDTH / 2 + 70
    slider_y2 = HEIGHT / 2 - 200
    slide2_color = arcade.color.BLUE
    press2 = False  # Slider
    graph_data = []

    population = 90
    prev = 90
    for i in range(population):
        ball_pos.append(
            [random.randrange(100, DOT_WIDTH - 100), random.randrange(100, DOT_HEIGHT - 100), arcade.color.BLACK, 0])
        ball_mvmt.append(random.randrange(-2, 3))
    for i in range(1):
        ball_pos[0][2] = arcade.color.RED
    restart = False
    CURED = 0
    INFECTED = 0
    DEAD = 0
    INFECTION_RADIUS = 15
    CHANCE_OF_INFECTION = 20
    CURE_RATE = 300
    DEATH_RATE = 1500
    BASE_TIME = 11
    PEOPLE_INFECTED = []


def cure():
    global CURED, INFECTED, CURE_RATE

    pop_list = []

    for i in range(len(PEOPLE_INFECTED)):
        if random.randrange(CURE_RATE) < 0.5 and (time.time() - PEOPLE_INFECTED[i][3]) >= BASE_TIME:
            pop_list.append(PEOPLE_INFECTED.index(PEOPLE_INFECTED[i]))
            PEOPLE_INFECTED[i][2] = arcade.color.GRAY

            CURED += 1
            INFECTED -= 1

    for i in sorted(pop_list, reverse=True):
        del PEOPLE_INFECTED[i]


def mortality():
    global DEAD, INFECTED, DEATH_RATE
    pop_list = []

    for i in range(len(PEOPLE_INFECTED)):
        if random.randrange(DEATH_RATE) < 0.5 and (time.time() - PEOPLE_INFECTED[i][3]) >= BASE_TIME:
            pop_list.append(PEOPLE_INFECTED.index(PEOPLE_INFECTED[i]))
            PEOPLE_INFECTED[i][2] = arcade.color.YELLOW

            DEAD += 1
            INFECTED -= 1

    for i in sorted(pop_list, reverse=True):
        del PEOPLE_INFECTED[i]


class Person:
    infected = False
    position = []

    def __init__(self, infected, position):
        self.infected = infected
        self.position = position


def on_mouse_press(x, y, button, modifiers):
    global mouse_press
    if button == arcade.MOUSE_BUTTON_LEFT:
        mouse_press = True


def on_mouse_release(x, y, button, modifiers):
    global mouse_press
    if button == arcade.MOUSE_BUTTON_LEFT:
        mouse_press = False


def on_mouse_motion(x, y, dx, dy):
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = y


if __name__ == '__main__':
    setup()
