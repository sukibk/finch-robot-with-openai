from HummingbirdBit_pythondriver import Hummingbird,Microbit
import time

bird1    = Hummingbird('A')

while(1):
	time.sleep(0.1)
	response = bird1.getOrientation()
	if(response == "TiltLeft"):
		print("Tilt Left")
		bird1.setPositionServo(1,180)
	elif(response == "TiltRight"):
		print("Tilt Right")
		bird1.setPositionServo(1,0)
	elif(response == "LogoUp"):
		print("LogoUp")
		bird1.print("LOGOUP")

