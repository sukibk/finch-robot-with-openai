from HummingbirdBit_pythondriver import Hummingbird,Microbit
import time

bird1    = Hummingbird('A')

def animation1():
	global bird1
	bird1.setDisplay("10000"\
					 "01000"\
					 "00100"\
					 "00010"\
					 "00001")
	time.sleep(0.1)
	bird1.setDisplay("00100"\
					 "00100"\
					 "00100"\
					 "00100"\
					 "00100")
	time.sleep(0.1)
	bird1.setDisplay("00001"\
					 "00010"\
					 "00100"\
					 "01000"\
					 "10000")
	time.sleep(0.1)
	bird1.setDisplay("00000"\
					 "00000"\
					 "11111"\
					 "00000"\
					 "00000")
	time.sleep(0.1)
	bird1.setDisplay("00100"\
					 "00100"\
					 "00100"\
					 "00100"\
					 "00100")
	time.sleep(0.1)
	bird1.setDisplay("00001"\
					 "00010"\
					 "00100"\
					 "01000"\
					 "10000")
	time.sleep(0.1)
	bird1.setDisplay("00000"\
					 "00000"\
					 "11111"\
					 "00000"\
					 "00000")
	time.sleep(0.1)


def animation2():
	global bird1
	bird1.setDisplay("00000"\
					 "00000"\
					 "10000"\
					 "00000"\
					 "00000")
	time.sleep(0.1)
	bird1.setDisplay("00000"\
					 "00000"\
					 "11000"\
					 "00000"\
					 "00000")
	time.sleep(0.1)
	bird1.setDisplay("00000"\
					 "00000"\
					 "11100"\
					 "00000"\
					 "00000")
	time.sleep(0.1)
	bird1.setDisplay("00000"\
					 "00000"\
					 "11110"\
					 "00000"\
					 "00000")
	time.sleep(0.1)
	bird1.setDisplay("00000"\
					 "00000"\
					 "11111"\
					 "00000"\
					 "00000")
	time.sleep(0.1)



def check_buttons():
	global bird1
	buttonA = bird1.getButton('A')
	buttonB = bird1.getButton('B')
	return (buttonA, buttonB)


def main():
	bird1.setTriLED(1,100,100,100)
	bird1.setPoint(3,3,'1')
	bird1.playNote(60,1)
	bird1.getDial(1)
	while(1):
		##LED Ceck
		for i in range(1,3):
			for j in range(0,100):
				bird1.setLED(i,j)
				time.sleep(0.01)
		##ORB Check
		for i in range(1,2):
			for j in range(0,100):
				bird1.setTriLED(i,j,j,j)
				time.sleep(0.01)

		#Servo Check
		for i in range(1,4):
			for j in range(0,100):
				bird1.setPositionServo(i,j)
				time.sleep(0.01)

		#Rotation Servo Check
		for i in range(1,4):
			for j in range(0,100):
				bird1.setRotationServo(i,j)
				time.sleep(0.01)
	

		#LED Print
		# bird1.print("HELLO")
		# time.sleep(5)
		#LED Point
		bird1.setPoint(1,1,1)
		time.sleep(1)
		# ###
		# bird1.setPoint(1,2,1)
		# time.sleep(1)
		# ###
		# bird1.setPoint(1,1,0)
		# time.sleep(1)
		# ###
		# bird1.setPoint(1,2,0)
		# time.sleep(1)
		#####
		##Read values
		for k in range(1,4):
			print(bird1.getDial(k))
			print(bird1.getLight(k))
			print(bird1.getDistance(k))
			print(bird1.getSound(k))
		
		print(bird1.getCompass())
		print(bird1.getMagnetometer())
		print(bird1.getAcceleration())
		print(bird1.getButton('A'))


		#print(bird1.getOrientation())
		buttonA, buttonB = check_buttons()
		#print(buttonA)
		if(buttonA == True):
			buttonA = False
			while(buttonB == False):
				(buttonA , buttonB) = check_buttons()
				animation1()
		elif(buttonB == True):
			buttonB = False
			while(buttonA == False):
				(buttonA , buttonB) = check_buttons()
				animation2()

if __name__ == "__main__":
	main()
