from machine import Pin, SPI
from microbit import *
import random
import st7789
import framebuf
import controller

width, height = 128, 64
buffer = bytearray(width * height * 2)  # 2 bytes per pixel (RGB565)
fb = framebuf.FrameBuffer(buffer, width, height, framebuf.RGB565)

def config(rotation=0, buffer_size=0, options=0):
    return st7789.ST7789(
        SPI(2, baudrate=60_000_000, sck=Pin(18), mosi=Pin(14)),
        128,
        160,
        reset=Pin(46, Pin.OUT),
        cs=Pin(39, Pin.OUT),
        dc=Pin(16, Pin.OUT),
        backlight=Pin(47, Pin.OUT),
        color_order=st7789.RGB,
        rotation=rotation,
        buffer_size = 64*64*2,
        inversion=False)

tft = config(1)
tft.init()
tft.fill(st7789.BLACK)

left_score = 0
right_score = 0

player_one_pos = 28
player_two_pos = 28
player_length = 10
player_speed = 10

ball_x_pos = 62
ball_y_pos = 30

ball_x_vel = -3
ball_y_vel = 3

ball_steady = True
steady_counter = 0

def draw_setup():
    fb.text(str(left_score), 28, 5)
    fb.text(str(right_score), 95, 5)
    fb.line(64, 0, 64, 63, st7789.WHITE)
    for i in range(10):
       fb.line(64, 4+(i*10), 64, 9+(i*10), st7789.BLACK)
    return


def draw_players():
    for i in range(3):
        fb.line(2+i, player_one_pos, 2+i, player_one_pos+player_length, st7789.WHITE)
        fb.line(125+i, player_two_pos, 125+i, player_two_pos+player_length, st7789.WHITE)


def draw_ball():
    for i in range(4):
        fb.line(ball_x_pos+i, ball_y_pos, ball_x_pos+i, ball_y_pos+3, st7789.WHITE)


def move_player_one(inputs):
    global player_one_pos 
    global player_length
    global player_speed

    player_one_pos = player_one_pos + int(player_speed*(inputs[controller.JOY_Y1]/-700))
    
    if player_one_pos < 0:
        player_one_pos = 0
    
    if player_one_pos > 64-player_length:
        player_one_pos = 64-player_length

def move_player_AI():
    global player_two_pos 
    global player_length
    global player_speed

    if ball_y_pos > (player_two_pos-2) and (player_two_pos+player_length)<ball_y_pos:
        player_two_pos = player_two_pos + 3
    elif ball_y_pos < player_two_pos and (player_two_pos+player_length-2)>ball_y_pos:
        player_two_pos = player_two_pos - 3

    if player_two_pos < 0:
        player_two_pos = 0
    
    if player_two_pos > 64-player_length:
        player_two_pos = 64-player_length


def move_ball():
    global ball_x_pos
    global ball_y_pos
    global ball_x_vel
    global ball_y_vel
    global left_score
    global right_score
    global steady_counter

    if steady_counter < 40:
        steady_counter = steady_counter + 1
        gain = random.randint(1,5)
        ball_x_vel = -(6-gain)
        ball_y_vel = gain
        return

    ball_x_pos = ball_x_pos + ball_x_vel
    ball_y_pos = ball_y_pos + ball_y_vel

    if ball_x_pos < 0:
        steady_counter = 0
        right_score = right_score + 1
    if ball_x_pos > 127:
        steady_counter = 0
        left_score = left_score + 1

    if steady_counter == 0:
        ball_y_pos = 30
        ball_x_pos = 62

    if ball_y_pos < 0 or ball_y_pos > 63:
        ball_y_pos = ball_y_pos - ball_y_vel*2
        ball_y_vel = -ball_y_vel

def detect_colision():
    global ball_x_pos
    global ball_x_vel
    global ball_y_pos
    global ball_y_vel

    gain = random.randint(1,5)

    if ((ball_y_pos > player_two_pos and ball_y_pos < player_two_pos+player_length) or (((ball_y_pos+3) > player_two_pos and (ball_y_pos+3) < player_two_pos+player_length))) and ball_x_pos >= 122:
        ball_x_pos = ball_x_pos - ball_x_vel*2
        ball_x_vel = -(6-gain)
        ball_y_vel = int(-(ball_y_vel/ball_y_vel)) * (gain)

    if ((ball_y_pos > player_one_pos and ball_y_pos < player_one_pos+player_length) or (((ball_y_pos+3) > player_one_pos and (ball_y_pos+3) < player_one_pos+player_length))) and ball_x_pos <= 6:
        ball_x_pos = ball_x_pos - ball_x_vel*2
        ball_x_vel = (6-gain)
        ball_y_vel = int(-(ball_y_vel/ball_y_vel)) * (gain)


def play_state():
    global left_score, right_score

    inputs = controller.read_all_inputs()
    detect_colision()

    move_player_one(inputs)
    move_player_AI()
    move_ball()

    draw_setup()
    draw_players()
    draw_ball()

    if left_score == 12 or right_score == 12:
        return 2

    if pin2.read_digital() == False:
        while pin2.read_digital() == False:
            pass
        left_score = 0
        right_score = 1
        return 2
    return 1


def start_state():
    fb.text("Press start", 20, 20, st7789.WHITE)
    fb.text("for a new game", 9, 30, st7789.WHITE)

    if pin2.read_digital() == False:
        while pin2.read_digital() == False:
            pass
        return 1
    return 0


def game_over_state():
    global left_score, right_score
    global player_one_pos, player_two_pos, player_length, player_speed
    global ball_x_pos, ball_y_pos, ball_x_vel, ball_y_vel, ball_steady, steady_counter

    if left_score > right_score:
       fb.text("You win!", 23, 20, st7789.WHITE)
    else:
       fb.text("Game over", 23, 20, st7789.WHITE)

    sleep(2000)

    left_score = 0
    right_score = 0

    player_one_pos = 28
    player_two_pos = 28
    player_length = 10
    player_speed = 10

    ball_x_pos = 62
    ball_y_pos = 30

    ball_x_vel = -3
    ball_y_vel = 3

    ball_steady = True
    steady_counter = 0



def state_machine(state):
    fb.fill(st7789.BLACK)
    out = state

    if state == 0:
        out = start_state()
    elif state == 1:
        out = play_state()
    elif state == 2:
        game_over_state()
        out = 0

    tft.rect(15, 31, width+4, height+2, st7789.WHITE)
    tft.blit_buffer(buffer, 16, 32, width, height)
    return out


states = 0    
while True:
    states = state_machine(states)
    sleep(5)
