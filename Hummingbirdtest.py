from HummingbirdBit import Hummingbird, Microbit
import time


bird1    = Hummingbird('B')
bit1 = Microbit('A')
bit1.print("hi there")

print(bit1.getAcceleration())
print(bit1.getMagnetometer())
print("button "+ str(bit1.getButton('B')))
#bird1.setPositionServo(4,180)
#bird1.setTriLED(2,150,0,0)
\

while not bit1.isShaking():
	
	if (bird1.getDial(3) < 10):
		#bit1.setPoint(1,1,1)
		bird1.setLED(1,100)
		bird1.setTriLED(2,50,50,0)
		bird1.setTriLED(1,100,0,10)
		bird1.setPositionServo(1,180)
		bird1.setRotationServo(2,0)
		bird1.playNote(44, .2)
		time.sleep(.5)
	else:
		#bit1.setPoint(5,5,0)
		bird1.setLED(1,0)
		bird1.setTriLED(2,0,0,0)
		bird1.setTriLED(1,0,0,0)
		bird1.setPositionServo(1,0)
		bird1.setRotationServo(2,0)
		bird1.playNote(80, .2)
		time.sleep(.5)
#bird1.print("hi there")
time.sleep(2)




