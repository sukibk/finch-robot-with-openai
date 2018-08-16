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

	while(1):
		buttonA, buttonB = check_buttons()
		if(buttonA == "true"):
			buttonA = "false"
			while(buttonB == "false"):
				(buttonA , buttonB) = check_buttons()
				animation1()
		elif(buttonB == "true"):
			buttonB = "false"
			while(buttonA == "false"):
				(buttonA , buttonB) = check_buttons()
				animation2()

if __name__ == "__main__":
	main()
