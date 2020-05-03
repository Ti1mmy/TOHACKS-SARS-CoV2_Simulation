import arcade
import time
import random

WIDTH = 640
HEIGHT = 480

INFECTION_RADIUS = 10
CHANCE_OF_INFECTION = 20
CURE_RATE = 1
BASE_TIME = 3000000000
PEOPLE_INFECTED = []
SOCIAL_DISTANCING = True
SOCIAL_DISTANCE = 60

mouse_x = 0
mouse_y = 0
mouse_press = False
ball_pos = []
ball_mvmt = []
history = []
time_elapsed = 0

for i in range(90):
    ball_pos.append([random.randrange(100, WIDTH-100), random.randrange(100, HEIGHT-100), arcade.color.BLACK, 0])
    ball_mvmt.append(random.randrange(-2, 3))
for i in range(1):
    ball_pos[0][2] = arcade.color.RED


def setup():
    arcade.open_window(WIDTH, HEIGHT, "TOHACKS SARS COV-2 Model")
    arcade.set_background_color(arcade.color.WHITE)
    arcade.schedule(update, 1/60)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release
    window.on_mouse_press = on_mouse_press
    window.on_mouse_release = on_mouse_release
    window.on_mouse_motion = on_mouse_motion

    arcade.run()


def update(delta_time):
    global ball_mvmt, position, ball_pos, time_elapsed, SOCIAL_DISTANCING
    k = 0
    min_distance = 100000
    cls = -1
    for i in range(len(ball_mvmt)):
        if random.randrange(30) == 0:
            ball_mvmt[i] = random.randrange(-2, 3)
            if(ball_mvmt[i] == 0 and random.randrange(2)==1): ball_mvmt[i] = 2
            elif ball_mvmt[i] == 0: ball_mvmt[i] = -2
    #if time_elapsed >= 5:
    #    SOCIAL_DISTANCING = True
    for i in range(len(ball_pos)):
        if SOCIAL_DISTANCING :
            for j in range(len(ball_pos)):
                distance = ((ball_pos[j][0] - ball_pos[i][0]) ** 2 + (ball_pos[j][1] - ball_pos[i][1]) ** 2) ** (1 / 2)
                if distance <= SOCIAL_DISTANCE and distance <= min_distance:
                    cls = j
            if cls != -1:
                if ball_mvmt[cls] < 0:
                    ball_mvmt[i] = -1*abs(ball_mvmt[i])
                else: ball_mvmt[i] = abs(ball_mvmt[i])
                cls = -1

        k = random.randrange(4)
        if ball_pos[i][0] >= 250 or ball_pos[i][1] >= 250:
            ball_mvmt[i] = -1*abs(ball_mvmt[i])
        if ball_pos[i][1] <= 100 or ball_pos[i][0] <= 100:
            ball_mvmt[i] = abs(ball_mvmt[i])

        if k == 0: # Move along y = x
            ball_pos[i][0] += ball_mvmt[i]
            ball_pos[i][1] += ball_mvmt[i]
        elif k == 1:
            ball_pos[i][0] += ball_mvmt[i]
        elif k == 2:
            ball_pos[i][1] += ball_mvmt[i]
        else: # Move along y = -x
            ball_pos[i][0] += ball_mvmt[i]
            ball_pos[i][1] -= ball_mvmt[i]

    for i in range(len(ball_pos)):
        for j in range(i + 1, len(ball_pos)):
            if ball_pos[j][2] != ball_pos[i][2]:
                distance = ((ball_pos[j][0] - ball_pos[i][0]) ** 2 + (ball_pos[j][1] - ball_pos[i][1]) ** 2) ** (1 / 2)
                if distance <= INFECTION_RADIUS and random.randrange(100) < CHANCE_OF_INFECTION:
                    if ball_pos[i][2] == arcade.color.RED:
                        ball_pos[j][2] = arcade.color.RED
                        ball_pos[j][3] = time.time()
                        if [i, j] not in history:
                            history.append([i, j])
                    elif ball_pos[j][2] == arcade.color.RED:
                        ball_pos[i][2] = arcade.color.RED
                        ball_pos[i][3] = time.time()
                        if [j, i] not in history:
                            history.append([j, i])

                    if ball_pos[i] not in PEOPLE_INFECTED:
                        PEOPLE_INFECTED.append(ball_pos[i])

                    if ball_pos[j] not in PEOPLE_INFECTED:
                        PEOPLE_INFECTED.append(ball_pos[j])
    time_elapsed += 0.05
    cure()
    print(history)


def cure():
    pop_list = []

    for i in range(len(PEOPLE_INFECTED)):
        if random.randrange(100) < CURE_RATE and time.time() - PEOPLE_INFECTED[i][3] >= BASE_TIME:
            luckyBoi = random.choice(PEOPLE_INFECTED)
            pop_list.append(PEOPLE_INFECTED.index(luckyBoi))
            luckyBoi[2] = arcade.color.BLACK

    for i in range(0, len(pop_list), -1):
        PEOPLE_INFECTED.pop(pop_list[i])


class Person:
    infected = False
    position = []

    def __init__(self, infected, position):
        self.infected = infected
        self.position = position


def on_draw():
    arcade.start_render()
    # Draw in here...
    # arcade.draw_circle_filled(mouse_x, mouse_y, 25, ball_color)
    for i in range(len(ball_pos)):
        arcade.draw_circle_filled(ball_pos[i][0], ball_pos[i][1], 5, ball_pos[i][2])
    for i in range(len(history)):
        arcade.draw_line(ball_pos[history[i][0]][0], ball_pos[history[i][0]][1], ball_pos[history[i][1]][0], ball_pos[history[i][1]][1], arcade.color.RED)
    arcade.draw_text(f'Number infected: {len(history) + 1}\nTime elapsed: {(time_elapsed):.2f}', 0, 0,
                     arcade.color.BLACK, 18)
def on_key_press(key, modifiers):
    pass


def on_key_release(key, modifiers):
    pass


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
