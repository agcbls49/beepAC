import pygame
import winsound

frequency = 1500
duration = 200

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller found!")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# a and y buttons which are assetto corsa upshift and downshift
a_pressed_before = False
y_pressed_before = False

running = True

while running:
    pygame.event.pump()

    a_pressed_now = joystick.get_button(0)
    y_pressed_now = joystick.get_button(3)

    # if A pressed then beep
    if a_pressed_now and not a_pressed_before:
        winsound.Beep(frequency, duration)

    # if Y pressed then beep
    if y_pressed_now and not y_pressed_before:
        winsound.Beep(frequency, duration)

    # track state
    a_pressed_before = a_pressed_now
    y_pressed_before = y_pressed_now