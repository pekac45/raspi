from gpiozero import TrafficLights
from time import sleep

# JUMPERS IN SLOTS 3,5,7,9. 
# 3 = RED
# 5 = AMBER
# 7 = GREEN
# 9 = GROUND

lights = TrafficLights(2, 3, 4)

lights.green.on()

while True:
    sleep(5)
    lights.green.off()
    lights.amber.on()
    sleep(1)
    lights.amber.off()
    lights.red.on()
    sleep(5)
    lights.amber.on()
    sleep(1)
    lights.green.on()
    lights.amber.off()
    lights.red.off()