from microbit import *
import follower
import vehicle

integral = 0
derivative = 0
previous_error = 0 
pos_old = 0
sens_old = 0

sample_time = 0.01

while button_a.is_pressed() == False:
    sleep(1)

offsets = [0, 0, 0, 0]
for i in range(10):
    offsets[0] = offsets[0] + follower.read(0)
    offsets[1] = offsets[1] + follower.read(1)
    offsets[2] = offsets[2] + follower.read(2)
    offsets[3] = offsets[3] + follower.read(3)

offsets[0] = offsets[0] / 10
offsets[1] = offsets[1] / 10
offsets[2] = offsets[2] / 10
offsets[3] = offsets[3] / 10    

def get_position():
    global offsets
    readings = [follower.read(0)-offsets[0], follower.read(1)-offsets[1], follower.read(2)-offsets[2], follower.read(3)-offsets[3]]
    weights = [12, 4, -4, -12]
    res = 0
    for idx,reading in enumerate(readings):
        res = res + ((reading) * weights[idx])
    return res


def PID(target, current):
    global integral, derivative, previous_error, sample_time

    kp = 0.80
    ki = 0.4
    kd = 0.05

    error = target - current
    integral = integral + (error * sample_time)
    derivative = (error - previous_error) / sample_time
    previous_error = error

    return (error * kp + integral * ki + derivative * kd), derivative


while True:
    sens = get_position() * 0.9 + sens_old * 0.1
    sens_old = sens
    pos, delta_error = PID(0, sens)
    
    if delta_error > 100:
        pos = pos * 10

    pos = pos*0.7 + pos_old*0.3
    pos_old = pos
    sign = 1

    rotation = 90 * (pos)
    forward = -80 + (abs(pos) * 50)
    if forward > 0:
        forward = 0
    
    print(delta_error)

    vehicle.move(rotation, forward)
    sleep(int(sample_time*1000))