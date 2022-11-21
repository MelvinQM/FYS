import keyboard

print("Keyboard test")

# variabelen initialiseren
keep_looping = True
counter = 0

# main loop
while keep_looping:
    if keyboard.is_pressed(key.SPACE):
        print("Score omhoog!")