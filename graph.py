import arcade
import time

WIDTH = 1280
HEIGHT = 720

mouse_x = 0
mouse_y = 0
mouse_press = False


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
    pass

def on_draw():
    arcade.start_render()
    # Draw in here...
    # arcade.draw_circle_filled(mouse_x, mouse_y, 25, ball_color)
    arcade.draw_line(0, HEIGHT / 2, WIDTH, HEIGHT / 2, arcade.color.BLACK)
    arcade.draw_line(WIDTH / 2, HEIGHT, WIDTH/2, 0, arcade.color.BLACK)
    for i in range(WIDTH*2):
        arcade.draw_point(i, 0.001 * (i - WIDTH / 2) ** 2, arcade.color.BLUE, 10)

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
