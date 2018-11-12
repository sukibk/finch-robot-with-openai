from HummingbirdBit import Hummingbird, Microbit
import time


bird1    = Hummingbird('B')
bit1 = Microbit('A')
#bit1.print("hithere")

print("button "+ str(bit1.getButton('A')))
#bird1.setPositionServo(4,180)
#bird1.setTriLED(2,150,0,0)
bit1.setDisplay([0,0,1,1,1,0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1,1,1,1,0])


#bird1.setRotationServo(2, 0)
#bird1.print("hellohellohellohello")
print(bit1.getMagnetometer())
if bit1.isShaking():
	print("help me")

#print(bird1.getLight(1))

bit1.setPoint(4,1,0)
time.sleep(1)
bit1.setPoint(5,1,0)

bird1.setTriLED(1,0,50,0)
bird1.playNote(25.0, 1)
time.sleep(1)
#bird1.print("hi there")
time.sleep(2)




