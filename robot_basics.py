import RPi.GPIO as GPIO  # Import the GPIO Library
from time import sleep

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set variables for the GPIO motor pins
in1 = 27
in2 = 17
enA = 22
in3 = 9
in4 = 10
enB = 18
temp1 = 1

# Set the GPIO Pin mode
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(enA, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)

GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

ns = 50      # normal speed
fs = 100     # full speed
ds = 5      # decreased Speed

p = GPIO.PWM(enA, 100)
p.start(ns)

q = GPIO.PWM(enB, 100)
q.start(ns)


# Speed control


def ON():
    p.start(fs)
    q.start(fs)


def OFF():
    p.stop()
    q.stop()


def ChangeSpeed(speed):
    p.ChangeDutyCycle(speed)
    q.ChangeDutyCycle(speed)


def Low():
    ON()
    ChangeSpeed(35)


def Medium():
    ON()
    ChangeSpeed(70)


def High():
    ON()
    ChangeSpeed(100)


# Turn all motors off
def StopMotors():
    GPIO.output(in1, 0)
    GPIO.output(in2, 0)
    GPIO.output(in3, 0)
    GPIO.output(in4, 0)


# Basic controls
def Forwards():
    Medium()
    GPIO.output(in1, 1)
    GPIO.output(in2, 0)
    GPIO.output(in3, 1)
    GPIO.output(in4, 0)


def Backwards():
    Medium()
    GPIO.output(in1, 0)
    GPIO.output(in2, 1)
    GPIO.output(in3, 0)
    GPIO.output(in4, 1)


def Right():
    OFF()
    p.start(fs)
    q.start(ds)


def Left():
    OFF()
    p.start(ds)
    q.start(fs)


def CntrClockwise():
    High()
    GPIO.output(in1, 0)
    GPIO.output(in2, 1)
    GPIO.output(in3, 1)
    GPIO.output(in4, 0)


def Clockwise():
    High()
    GPIO.output(in1, 1)
    GPIO.output(in2, 0)
    GPIO.output(in3, 0)
    GPIO.output(in4, 1)
