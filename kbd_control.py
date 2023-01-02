import time
import curses
import robot_basics as rb
import os
import tgSend as tgs

stdscr = curses.initscr()
stdscr
stdscr.keypad(True)
curses.noecho()

button_delay = 1


def Sleep():
    time.sleep(button_delay)


while True:
    char = stdscr.getch()

    if char == ord(' '):
        stdscr.clear()
        print('Motors stopped.')
        rb.StopMotors()
        stdscr.clear()
        Sleep()

    elif char == ord('q'):
        print('CONNECTION CLOSED.')
        msg = "\"aConnessione terminata\""
        cmd = 'espeak -v mb-it3 -p 0 --stdout ' + msg + ' | aplay -q'
        os.system(cmd)
        stdscr.clear()
        Sleep()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        exit(0)

    elif char == curses.KEY_LEFT:
        rb.Left()
        stdscr.clear()
        print("Left.")
        stdscr.clear()
        Sleep()

    elif char == curses.KEY_RIGHT:
        rb.Right()
        print("Move right.")
        stdscr.clear()
        Sleep()

    elif char == curses.KEY_UP:
        rb.Forwards()
        print("Move forkwards.")
        stdscr.clear()
        Sleep()

    elif char == curses.KEY_DOWN:
        rb.Backwards()
        print("Move backwards.")
        stdscr.clear()
        Sleep()

    elif char == ord('l'):
        rb.Low()
        msg = "\"aVelocità ridotta.\""
        cmd = 'espeak -v mb-it3 -p 0 --stdout ' + msg + ' | aplay -q'
        os.system(cmd)
        print("Low speed.")
        stdscr.clear()
        Sleep()

    elif char == ord('m'):
        rb.Medium()
        msg = "\"aVelocità media.\""
        cmd = 'espeak -v mb-it3 -p 0 --stdout ' + msg + ' | aplay -q'
        os.system(cmd)
        print("Medium speed.")
        stdscr.clear()
        Sleep()

    elif char == ord('h'):
        rb.High()
        msg = "\"aVelocità massima.\""
        cmd = 'espeak -v mb-it3 -p 0 --stdout ' + msg + ' | aplay -q'
        os.system(cmd)
        print("High speed.")
        stdscr.clear()
        Sleep()

    elif char == ord('i'):
        curses.nocbreak()
        curses.echo()
        msg = "   " + str(stdscr.getstr())
        cmd = 'espeak -v mb-it3 -p 0 -a 150 --stdout ' + msg + ' | aplay -q'
        stdscr.clear()
        os.system(cmd)
        stdscr.clear()
        curses.cbreak()
        curses.noecho()

    elif char == ord('v'):
        tgs.VideoSend()
        stdscr.clear()

    elif char == ord('r'):
        tgs.AudioSend()
        stdscr.clear()

    elif char == ord('p'):
        tgs.Snapshot()
        stdscr.clear()

    else:
        stdscr.clear()
        print("Wrong command.")
        Sleep()
        stdscr.clear()
