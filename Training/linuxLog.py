import keyboard

def x1():
    if keyboard.is_pressed('a'):
        return 1
    else:
        return 0
def x2():
    if keyboard.is_pressed('w'):
        return 1
    else:
        return 0
def x4():
    if keyboard.is_pressed('s'):
        return 1
    else:
        return 0
def x3():
    if keyboard.is_pressed('d'):
        return 1
    else:
        return 0

def key_check():
    keys = [0, 0, 0, 0]
    a = 0
    w = 0
    s = 0
    d = 0
    a = int(x1())
    w = int(x2())
    s = int(x4())
    d = int(x3())
    keys[0] = a
    keys[1] = w
    keys[2] = d
    keys[3] = s
    return keys
