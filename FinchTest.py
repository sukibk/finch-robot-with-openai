from BirdBrainBit import Finch
import time

myFinch = Finch()

myFinch.setBeak(100, 100, 100)
myFinch.setTail("all", 100, 100, 100)

myFinch.setMove('F', 10, 50)
myFinch.setMove('B', 10, 50)
myFinch.setTurn('R', 180, 50)
myFinch.setTurn('L', 180, 50)

myFinch.playNote(60, 0.25)
time.sleep(0.25)
myFinch.playNote(67, 0.25)
time.sleep(0.25)

for i in range(4):
	myFinch.setTail((i+1), 0, 0, 100)
	time.sleep(0.5)

myFinch.stopAll()
