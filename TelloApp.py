import re
import socket
import threading
import time
from subprocess import call
from pynput import keyboard

UDP_IP = "192.168.10.1"
UDP_PORT = 8889
commands_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
commands_socket.bind(('', 9000))

stats_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
stats_socket.bind(('', 8890))


def command(message):
    print('sending {!r}'.format(message))
    commands_socket.sendto(bytes(message, 'utf-8'), (UDP_IP, UDP_PORT))
    data, server = commands_socket.recvfrom(4096)
    print('received {!r}'.format(data))


def receive_stats():
    while True:
        data, addr = stats_socket.recvfrom(4096)
        data = data.decode('utf-8')
        format_data(data)
        time.sleep(0.25)
        clear_console()


def format_data(data):
    regex = re.search(
        "vgx:-?(\d{1,3});vgy:-?\d{1,3};vgz:-?\d{1,3};templ:-?\d{1,3};temph:-?\d{1,3};tof:-?\d{1,3};h:(-?\d{1,3});bat:(\d{1,3})",
        data)
    battery = regex.group(3)
    height = regex.group(2)
    speed = regex.group(1)
    print(data)
    print('Battery: {}'.format(battery))
    if int(battery) < 35:
        print('!!! LOW BATTERY LEVEL !!!')
    print('Height: {}'.format(height))
    print('Speed: {}'.format(speed))


def clear_console():
    _ = call('clear')


def on_press(key):
    letter = str(key)
    letter = letter.replace("'", "")
    if (letter == 'Key.up'):
        print('forward 50')
        command('forward 50')
    elif (letter == 'Key.down'):
        print('back 50')
        command('back 50')
    elif (letter == 'Key.left'):
        print('left 50')
        command('left 50')
    elif (letter == 'Key.right'):
        print('right 50')
        command('right 50')
    elif (letter == 'w'):
        print('up 50')
        command('up 50')
    elif (letter == 's'):
        print('down 50')
        command('down 50')
    elif (letter == 'a'):
        print('turn left 45')
        command('ccw 45')
    elif (letter == 'd'):
        print('turn right 45')
        command('cw 45')
    elif (letter == 't'):
        print('take-off')
        command('takeoff')
    elif (letter == 'l'):
        print('land')
        command('land')
    elif (letter == 'b'):
        print('battery')
        command('battery?')
    elif (letter == 'W'):
        print('flip forward')
        command('flip f')
    elif (letter == 'S'):
        print('flip back')
        command('flip b')
    elif (letter == 'A'):
        print('flip left')
        command('flip l')
    elif (letter == 'D'):
        print('flip right')
        command('flip r')
    elif (letter == 'Key.esc'):
        print('EMERGENCY')
        command('emergency')
    else:
        print("Action for key: '{}' not found".format(letter))


print("start")
command('command')

threading.Thread(target=receive_stats).start()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
