from HummingbirdBit import Hummingbird, Microbit
import time


myBird    = Hummingbird('B')
testM = Microbit('A')
testM.print("q")
print(myBird.getLight(1))
for i in range(0,10):
	myBird.setLED(1,100)
	time.sleep(1)
	myBird.setLED(1,0)
	time.sleep(1)

myBird.stopAll()