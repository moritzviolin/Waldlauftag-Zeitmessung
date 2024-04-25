import playsound


def say_number(text):
    playsound.playsound("lib/sounds/beep.mp3", block=True)
    for number in text:
        playsound.playsound("lib/sounds/" + str(number) + ".mp3", block=True)

