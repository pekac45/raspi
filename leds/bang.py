from gpiozero import Button, LED
from time import sleep
import random
from signal import pause

green = LED(17)
amber = LED(22)
red = LED (27)

player_1 = Button(2)
player_2 = Button(3)

time = random.uniform (2,6)

sleep(1)
red.on()
sleep(2)
amber.on()

sleep(time)
green.on()

while True:
    if player_1.is_pressed:
        print("Player 1 wins!")
        break
    if player_2.is_pressed:
        print("Player 2 wins!")
        break

green.off()
amber.off()
red.off()