from HummingbirdBit_pythondriver import Hummingbird,Microbit
import time

bird1    = Hummingbird('A')
initial_time = time.time()
count = 0
f = open('results.txt','w') 
f.write("S.No		current_time		BatteryVolatge" )
print("S.No		current_time		BatteryVolatge" )
print("-----------------------------------------------------------------") 
print("-----------------------------------------------------------------") 
print("-----------------------------------------------------------------") 

while(1):
	bird1.setTriLED(1,100,100,100)
	bird1.setRotationServo(1,100)
	bird1.setRotationServo(2,100)
	time.sleep(1)
	bird1.setTriLED(1,0,0,0)
	bird1.setRotationServo(1,-100)
	bird1.setRotationServo(2,-100)
	time.sleep(1)
	current_time    = (int)(time.time() - initial_time) 
	battery_volatge = bird1.getSensor(4) * 0.0406
	count = count + 1
	string = str(count) + "\t\t" +(str)(current_time) + "\t\t" + (str)(battery_volatge) 
	print(count , current_time,battery_volatge)
	f.write(string)
	


