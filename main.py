import pygame
import pyautogui
import win32com.client
import winsound

# for the beep sound 
upshift_frequency = 1500
downshift_frequency = 1000
duration = 200

# EYES HERE!!!!!!!!!!!!!!!!!!!!!!!!
# Since the location of the app/mod in assetto corsa is set to a certain position in the ganme
# this can be uncommented so that the location of said sector colors from said mod
# can be changed to any location
# pyautogui.displayMousePosition()

# approximate delta colors from the mod
green_delta = (36, 181, 54)
yellow_delta = (196, 168, 6)
purple_delta = (133, 15, 155)

# EYES HERE!!!!!!!!!!!!!!!!!!!!!!!!
# change location here
sector_one = (122, 1027)
sector_two = (242, 1030)
sector_three = (369, 1029)

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

def make_a_beep(a_pressed_before, y_pressed_before):
    ''' this is mapped a and y but can be changed to b and y with get_button(number)
    A Button = 0
    B Button = 1
    X Button = 2
    Y Button = 3
    '''
    a_pressed_now = joystick.get_button(0)
    y_pressed_now = joystick.get_button(3)
    
    # if A pressed then beep
    if a_pressed_now and not a_pressed_before:
        winsound.Beep(downshift_frequency, duration)
    
    # if Y pressed then beep
    if y_pressed_now and not y_pressed_before:
        winsound.Beep(upshift_frequency, duration)
    
    # track state
    a_pressed_before = a_pressed_now
    y_pressed_before = y_pressed_now

# driver code to make windows say the text
def speak(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

# how close the colors from the mod coordinates
# high tolerance meaning less stricter in RGB value
def close(c, target, tolerance=60):
    # zip() function returns a zip object, which is an iterator of tuples 
    # where the first item in each passed iterator is paired together, 
    # and then the second item in each passed iterator are paired together 
    # and so on and so forth
    
    ''' EXPLANATION
    basically zip is
    c is RGB color taken by pyautogui from the pixel 
    position of the hardcoded sectors from the mod
    c = (133, 15, 155)      # pixel

    target = (94, 17, 111)  # hardcoded purple color

    zip(c, target)  →  (133, 94), (15, 17), (155, 111)

    Loop 1: a=133, b=94. abs(133-94) = 39. Is 39 > 60? No. Keep going.
    Loop 2: a=15, b=17. abs(15-17) = 2. Is 2 > 60? No. Keep going.
    Loop 3: a=155, b=111. abs(155-111) = 44. Is 44 > 60? No. Keep going.

    If all is True then return True which would then be 
    used for the speak logic
    '''
    return all(abs(a - b) <= tolerance for a, b in zip(c, target))

# track sector color states
last_color1 = None
last_color2 = None
last_color3 = None

# say the delta color of sector 1 
def say_sector1_color():
    global last_color1
    color = pyautogui.pixel(*sector_one)
    current = None

    # track the last color each sector showed, so it only speaks
    # when the color changes (e.g. gray -> purple). if it stays
    # purple frame after frame, it won't repeat saying it.
    if close(color, green_delta):  current = "Green"
    elif close(color, yellow_delta): current = "Yellow"
    elif close(color, purple_delta): current = "Purple"

    # only speak when this sector has a color AND it's different
    # from what was seen last frame. when the light goes back to
    # gray, current becomes None, so the next color change fires again.
    if current is not None and current != last_color1:
        # print(f"Sector 1 {current}")
        speak(f"Sector 1 {current}")

    last_color1 = current

# say the delta color of sector 2
def say_sector2_color():
    global last_color2
    color = pyautogui.pixel(*sector_two)
    current = None

    if close(color, green_delta):  current = "Green"
    elif close(color, yellow_delta): current = "Yellow"
    elif close(color, purple_delta): current = "Purple"

    if current is not None and current != last_color2:
        # print(f"Sector 2 {current}")
        speak(f"Sector 2 {current}")

    last_color2 = current

# say the delta color of sector 3
def say_sector3_color():
    global last_color3
    color = pyautogui.pixel(*sector_three)
    current = None
    if close(color, green_delta):  current = "Green"
    elif close(color, yellow_delta): current = "Yellow"
    elif close(color, purple_delta): current = "Purple"

    if current is not None and current != last_color3:
        # print(f"Sector 3 {current}")
        speak(f"Sector 3 {current}")

    last_color3 = current

# driver code for the saying the delta colors 
def say_sector_colors():
    say_sector1_color()
    say_sector2_color()
    say_sector3_color()

while running:
    pygame.event.pump()
    make_a_beep(a_pressed_before, y_pressed_before)
    say_sector_colors()