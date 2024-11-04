from microbit import *
import controller
import random

controller.init()
controller.oled.fill(0)
controller.oled.show()

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
    controller.oled.line(64, 0, 64, 63, 1)
    controller.oled.text(str(left_score), 28, 5)
    controller.oled.text(str(right_score), 95, 5)
    for i in range(10):
       controller.oled.line(64, 4+(i*10), 64, 9+(i*10), 0)


def draw_players():
    for i in range(3):
        controller.oled.line(2+i, player_one_pos, 2+i, player_one_pos+player_length, 1)
        controller.oled.line(125+i, player_two_pos, 125+i, player_two_pos+player_length, 1)


def draw_ball():
    for i in range(4):
        controller.oled.line(ball_x_pos+i, ball_y_pos, ball_x_pos+i, ball_y_pos+3, 1)


def move_player_one(inputs):
    global player_one_pos 
    global player_length
    global player_speed

    player_one_pos = player_one_pos + int(player_speed*(inputs[controller.inputs.JOY_Y1[0]]/-32000))

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
    controller.oled.text("Press start", 20, 20, 1)
    controller.oled.text("for a new game", 9, 30, 1)

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
       controller.oled.text("You win!", 23, 20, 1)
    else:
        controller.oled.text("Game over", 23, 20, 1)

    controller.oled.show()
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
    controller.oled.fill(0)
    out = state

    if state == 0:
        out = start_state()
    elif state == 1:
        out = play_state()
    elif state == 2:
        game_over_state()
        out = 0

    controller.oled.show()
    return out
    
states = 0    
while True:
    states = state_machine(states)
