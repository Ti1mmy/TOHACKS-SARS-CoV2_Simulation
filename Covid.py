import arcade


WIDTH = 640
HEIGHT = 480

mouse_x = 0
mouse_y = 0
mouse_press = False
ball_color = arcade.color.BLUE
slider_x = WIDTH / 2
slider_y = HEIGHT / 2
slide_color = arcade.color.BLUE

def setup():
    arcade.open_window(WIDTH, HEIGHT, "My Arcade Game")
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
    global ball_color, slide_color, slider_x
    if mouse_press:
        ball_color = arcade.color.RED
    else:
        ball_color = arcade.color.BLUE
    if slider_x - 5 <= mouse_x <= slider_x + 5 and slider_y - 13 <= mouse_y <= slider_y + 13:
        slide_color = arcade.color.DARK_GRAY
        if mouse_press:
            slide_color = arcade.color.GRAY
            if WIDTH/2 - 100 < slider_x < WIDTH/2 + 100:
                slider_x = mouse_x
            if slider_x < 420 or slider_x > 220:
                if 220 <= mouse_x <= 420:
                    slider_x = mouse_x
    else:
        slide_color = arcade.color.BLUE


def on_draw():
    arcade.start_render()
    # Draw in here...
    # arcade.draw_circle_filled(mouse_x, mouse_y, 25, ball_color)
    arcade.draw_text(f'mouse_x={mouse_x}\nmouse_y={mouse_y}\nmouse_press={mouse_press}\nslider_x={slider_x}', 0, 0, arcade.color.BLACK)
    arcade.draw_rectangle_outline(WIDTH/2, HEIGHT/2, 200, 5, arcade.color.BLACK)
    arcade.draw_rectangle_filled(slider_x, slider_y, 10, 25, slide_color)



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
