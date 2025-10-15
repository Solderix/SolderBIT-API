from microbit import *
import re
from machine import Timer

_ticks = 4
_bpm = 120
_volume = 255

_timer = Timer(-1)
_active_melody = None
_pin = pin0
counter = 0
_started = False
_loop = False

_pattern = re.compile(r'^([a-grA-GR])(#|b)?(\d+)?(?::(\d+))?$')
_notes = { 'r' : 0, 'r#' : 0, 'rb' : 0, 'a' : 440, 'b#' : 466, 'bb' : 466, 'b' : 494, 'c' : 523, 'c#' : 554, 'd' : 587, 'd#' : 622, 'e' : 659, 'f' : 698, 'f#' : 740, 'g' : 784, 'g#' : 830 }


def _parse_note(note_str):
    global _bpm
    global _ticks
    m = _pattern.match(note_str)
    if not m:
        return (0, 0)
    
    note = m.group(1)
    accidental = m.group(2)
    octave = m.group(3)
    duration = m.group(4)

    nt = str(note.lower()) + (accidental if accidental else '')
    freq = _notes[nt] * (int(octave) if octave else 1)
    dur =  (60000 / (_bpm * _ticks) ) * int(duration) if duration else 4
    return (freq, dur)


def _play_note(frequency, dur):
    global _volume
    global _pin

    
    if frequency != 0:
        _pin.set_analog_period( float(1/(frequency)) * 1000 ) 
        _pin.write_analog(_volume>>1)
    else:
        _pin.write_analog(0)


def melody_cb(t):
    global _active_melody
    global _timer
    global counter
    global _pin
    global _started
    global _loop

    if counter >= len(_active_melody):
        if _loop:
            counter = 0
        else:
            _started = False
            _pin.write_analog(0)
            return

    frequency, dur = _parse_note(_active_melody[counter])
    _play_note(frequency, dur)
    _timer.init(period=int(dur), mode=Timer.ONE_SHOT, callback=melody_cb)
    counter += 1
    

def play(melody, pin=pin0, wait=True, loop=False):
    global counter
    global _pin
    global _timer
    global _volume
    global _active_melody
    global _started
    global _loop

    if _started:
        return

    _active_melody = melody
    _pin = pin
    _loop = loop

    if not wait:
        _started = True
        frequency, dur = _parse_note(melody[0])
        counter = 1
        _pin.set_analog_period( float(1/(frequency)) * 1000 ) 
        _pin.write_analog(_volume>>1)
        _timer.init(period=int(dur), mode=Timer.ONE_SHOT, callback=melody_cb)
        return

    for note in _active_melody:
        frequency, dur = _parse_note(_active_melody[counter])
        _play_note(frequency, dur)
        sleep(int(dur))


def set_tempo(ticks=4, bpm=120):
    global _bpm
    global _ticks
    _ticks = ticks
    _bpm = bpm


def stop(pin=pin0):
    global _loop 
    global _started
    global _timer

    _loop = False
    _started = False
    pin.write_analog(0)
    _timer.deinit()


def reset():
    pass


def get_tempo():
    return (_ticks, _bpm)


def set_volume(volume):
    global _volume
    _volume = volume
    if _volume < 0:
        _volume = 0
    if _volume > 255:
        _volume = 255
   


def pitch(frequency, duration=0, pin=pin0, wait=True):
    pin.set_analog_period(frequency) 
    pin.write_analog(_volume>>1)

    if wait:
        sleep(duration)
        pin.write_analog(0)
    else:
        _timer.init(period=duration, mode=Timer.ONE_SHOT, callback=lambda t: pin.write_analog(0))