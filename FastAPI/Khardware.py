from adafruit_motorkit import MotorKit
import time

kit = MotorKit()
kit.motor1.throttle = 1.0
time.sleep(5)
kit.motor1.throttle = 0