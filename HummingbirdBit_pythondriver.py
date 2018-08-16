###############################################################
###############################################################
#Author                  Raghunath J
#Date                    7/7/2018
###############################################################
###############################################################
import urllib.request
import sys
import time
###############################################################
###############################################################
#Constants 

CHAR_FLASH_TIME = 0.3		#Character Flash time

LED_MIN     = 0
LED_MAX     = 100

RGB_MIN     = 0
RGB_MAX     = 100

SERVO_P_MIN = 0
SERVO_P_MAX = 180

SERVO_R_MIN = -100
SERVO_R_MAX =  100


#Warning Codes
LED_W_VALUE 	= 1
SERVO_P_W_VALUE = 2
SERVO_R_W_VALUE = 3
PRINT_LENGTH_W_CODE = 4
PRINT_DISPLAY_W_CODE = 5


#Error Codes
LED_SERVO_PORT_NO_CHECK  = 1
RGB_PORT_NO_CHECK  		 = 2
CONNECTION_SERVER_CLOSED = 3
GARBAGE_VALUE_PORT       = 4
PRINT_DISPLAY_E_CODE 	 = 5
PLOT_NOT_VALID 			 = 6
NO_CONNECTION 			 = 7
NO_BUTTON_NAME           = 8
SENSOR_PORT_NO_CHECK     = 9


#Calculations after receveing the raw values
DISTANCE_FACTOR          = 117/100
SOUND_FACTOR             = 200/255
DIAL_FACTOR              = 100/230
LIGHT_FACTOR             = 100/255

###############################################################
###############################################################

class Microbit:
	##Test requests
	base_request_out = "http://127.0.0.1:30061/hummingbird/out"
	base_request_in  = "http://127.0.0.1:30061/hummingbird/in"
	shake_A			 = "http://127.0.0.1:30061/hummingbird/in/orientation/Shake/A"
	shake_B			 = "http://127.0.0.1:30061/hummingbird/in/orientation/Shake/B"
	shake_C			 = "http://127.0.0.1:30061/hummingbird/in/orientation/Shake/C"
	sensor4_A        = "http://127.0.0.1:30061/hummingbird/in/sensor/4/A"
	sensor4_B        = "http://127.0.0.1:30061/hummingbird/in/sensor/4/B"
	sensor4_C        = "http://127.0.0.1:30061/hummingbird/in/sensor/4/C"
	##########
	symbolvalue      =  None

	"""Called whenever a class is initialized"""
	def __init__(self, s_no = 'A'):
		self.PrintDevices()
		self.device_s_no = s_no

	""" Prints the tyoe of the device which you are connected , very useful to know what 
		device you are connected to"""
	def PrintDevices(self):
		response_request_micro 	= []
		response_request_bit 	= []
		device = []
		output = urllib.request.urlopen(self.shake_A) 
		response_request_micro.append(output.read().decode('utf-8'))
		output = urllib.request.urlopen(self.shake_B)
		response_request_micro.append(output.read().decode('utf-8'))
		output = urllib.request.urlopen(self.shake_C)
		response_request_micro.append(output.read().decode('utf-8'))
		output = urllib.request.urlopen(self.sensor4_A)
		response_request_bit.append(output.read().decode('utf-8'))
		output = urllib.request.urlopen(self.sensor4_B)
		response_request_bit.append(output.read().decode('utf-8'))
		output = urllib.request.urlopen(self.sensor4_C)
		response_request_bit.append(output.read().decode('utf-8'))
		
		length = 0
		#Based on the sensor 4 value we can say whether device connected is a Micro Bit or a HUmmingbird Bit 
		for i in response_request_micro:
			if(i != "Not Connected"):
				if(response_request_bit[length] != "255"):
					device.append("Connected as Hummingbird bit")
				else:
					device.append("Connected as Micro:Bit")
			else:
				device.append("Not connected")
			length = length + 1
		print("########################################################################################")
		print("########################################################################################")
		print ("Device A    --  " + device[0])
		print ("Device B    --  " + device[1])
		print ("Device C    --  " + device[2])
		print("########################################################################################")
		print("########################################################################################")

		

	def check_valid_params_3(self,peri , string_value):
		try:
			if(peri == "print"):
				if( len(string_value) > 18):
					self.print_warning(PRINT_LENGTH_W_CODE)
			else:
				if(len(string_value) != 25):
					self.print_warning(PRINT_DISPLAY_W_CODE)
				for letter in string_value:
					if ((letter != '0') and (letter != '1')):
						self.print_error(GARBAGE_VALUE_PORT)
						sys.exit();
		except:
			self.print_error(GARBAGE_VALUE_PORT)
			sys.exit()

	def setDisplay(self, LED_string):
		self.check_valid_params_3("Display" , LED_string)
		LED_string_c = self.process_display(LED_string)
		response = self.send_httprequest_micro("symbol",LED_string_c)
		return response

	def print(self, Print_string):
		self.check_valid_params_3("print" , Print_string)
		response = self.send_httprequest_micro("print",Print_string)
		return response

	def printAndWait(self, Print_string):
		self.check_valid_params_3("print" , Print_string)
		response = self.send_httprequest_micro("print",Print_string)
		time.sleep(len(Print_string)*CHAR_FLASH_TIME*2 +1)
		return response

	def plot(self, x , y , value):
		value = str(value)
		new_str = None
		# if(value == '1'):
		# 	print((value))
		#try:
		if((x > 4) or (x<0) or (y<0) or (y>4) or ((value != '0') and (value != '1'))):
			self.print_error(PLOT_NOT_VALID)
			sys.exit()
		else :
			index = x*5 + y
			if(self.symbolvalue == None):
				for i in range(0,25):
					if(i == index):
						if(self.symbolvalue == None):
							self.symbolvalue = value
						else :
							self.symbolvalue += value
					else :
						if(self.symbolvalue == None):
							self.symbolvalue = "0"
						else :
							self.symbolvalue += "0"
			else:
				#self.symbolvalue[index] = value
				length = 0
				new_str = None
				for i in self.symbolvalue:
					if(new_str == None):
						if(index == length):
							new_str = value
						else:
							new_str = i
					else:
						if(index == length):
							new_str += value
						else:
							new_str += i
					length += 1 
				self.symbolvalue = new_str
			
			self.setDisplay(self.symbolvalue)
		# except:
		# 		self.print_error(GARBAGE_VALUE_PORT)
		# 		sys.exit()

	def process_display(self , value):
		length = 1
		for letter in value:
			if(length == 1):
				if(letter == '1'):
					new_str = "true"
				else:
					new_str = "false"
			elif(length < 26):
				if(letter == '1'):
					new_str += "/true"
				else :
					new_str += "/false"
			length = length + 1
		return new_str

	def getAcceleration(self):
		dimension = ['X','Y','Z']
		acc_value = []  
		try:
			for i in range(0,3):
				response = self.send_httprequest_micro_in("Accelerometer",dimension[i])
				acc_value.append(response)
		except:
			self.print_error(GARBAGE_VALUE_PORT)
			sys.exit()
		acc_x 	=	float(acc_value[0])
		acc_y 	=	float(acc_value[1])
		acc_z 	=	float(acc_value[2])
		return (acc_x,acc_y,acc_z)


	def getCompass(self):
		try:
			response = self.send_httprequest_micro_in("Compass",None)
			compass_heading = float(response)
			return compass_heading
		except:
			self.print_error(GARBAGE_VALUE_PORT)
			sys.exit()

	def getMagnetometer(self):
		dimension = ['X','Y','Z']
		mag_value = []  
		try:
			for i in range(0,3):
				response = self.send_httprequest_micro_in("Magnetometer",dimension[i])
				mag_value.append(response)
		except:
			self.print_error(GARBAGE_VALUE_PORT)
			sys.exit()
		mag_x 	=	float(mag_value[0])
		mag_y 	=	float(mag_value[1])
		mag_z 	=	float(mag_value[2])
		return (mag_x,mag_y,mag_z)

	def getButton(self,button_name):
		try:
			button_name = button_name.upper()
			if((button_name != 'A') and (button_name != 'B')):
				self.print_error(NO_BUTTON_NAME)
				sys.exit()
			response = self.send_httprequest_micro_in("button", button_name)
			button_value = response
		except:
			self.print_error(GARBAGE_VALUE_PORT)
			sys.exit()
		return button_value

	def isShaking(self):
		try:
			response = self.send_httprequest_micro_in("Shake",None)
			shake    = response
		except:
			self.print_error(GARBAGE_VALUE_PORT)
			sys.exit()
		return shake

	def getOrientation(self):
		orentation = ["Screen%20Up","Screen%20Down","Tilt%20Left","Tilt%20Right","Logo%20Up","Logo%20Down"]
		orentation_result = ["ScreenUp","ScreenDown","TiltLeft","TiltRight","LogoUp","LogoDown"]
		try:
			for i in range(0,6):
				response = self.send_httprequest_micro_in(orentation[i],None)
				if(response == "true"):
					return orentation_result[i]
		except:
			self.print_error(GARBAGE_VALUE_PORT)
			sys.exit()
		return "In Between"

	def send_httprequest_micro(self, peri , value):
		if(peri == "print"):
			http_request = self.base_request_out + "/" + peri +  "/" + str(value)   + "/" + str(self.device_s_no)
		elif(peri == "symbol"):
			http_request = self.base_request_out + "/" + peri +  "/"  + str(self.device_s_no)  + "/" + str(value)
		#print(http_request)
		try :
			response_request =  urllib.request.urlopen(http_request)
			if(response_request.read() == b'200'):
				response = 1
			else :
				response = 0
		except:
			self.print_error(CONNECTION_SERVER_CLOSED)
			sys.exit()
		#print(response)
		return response


	def send_httprequest_micro_in(self, peri , value):
		if(peri == "Accelerometer"):
			http_request = self.base_request_in + "/" + peri +  "/" + str(value)   + "/" + str(self.device_s_no)
		elif(peri == "Compass"):
			http_request = self.base_request_in + "/" + peri + "/" + str(self.device_s_no)
		elif(peri == "Magnetometer"):
			http_request = self.base_request_in + "/" + peri + "/" + str(value)   + "/"+str(self.device_s_no)
		elif(peri == "button"):
			http_request = self.base_request_in + "/" + peri + "/" + str(value)   + "/"+str(self.device_s_no)
		elif(peri == "Shake"):
			http_request = self.base_request_in + "/" + "orientation" + "/" + peri + "/" +str(self.device_s_no)
		elif(peri == "Screen%20Up"):
			http_request = self.base_request_in + "/" + "orientation" + "/" + peri + "/" +str(self.device_s_no)
		elif(peri == "Screen%20Down"):
			http_request = self.base_request_in + "/" + "orientation" + "/" + peri + "/" +str(self.device_s_no)
		elif(peri == "Tilt%20Right"):
			http_request = self.base_request_in + "/" + "orientation" + "/" + peri + "/" +str(self.device_s_no)
		elif(peri == "Tilt%20Left"):
			http_request = self.base_request_in + "/" + "orientation" +  "/" + peri + "/" +str(self.device_s_no)
		elif(peri == "Logo%20Up"):
			http_request = self.base_request_in + "/" + "orientation" + "/" + peri + "/" +str(self.device_s_no)
		elif(peri == "Logo%20Down"):
			http_request = self.base_request_in + "/" + "orientation" + "/" + peri + "/" +str(self.device_s_no)
			

		try :
			response_request =  urllib.request.urlopen(http_request)
		except:
			self.print_error(CONNECTION_SERVER_CLOSED)
			sys.exit();
		response = response_request.read().decode('utf-8')
		if(response == "Not Connected"):
			self.print_error(NO_CONNECTION)
			sys.exit()
		return response




	def print_error(self,error_code):
		print("**************************************************")
		if(error_code == LED_SERVO_PORT_NO_CHECK):
			print("Error: Please choose a port value between 1-4")
		elif(error_code == RGB_PORT_NO_CHECK):
			print("Error: Please choose a port value between 1-2")
		elif(error_code == CONNECTION_SERVER_CLOSED):
			print("Error: Please open the BlueBird Connection App / unnexpected disconnection")
		elif(error_code == GARBAGE_VALUE_PORT):
			print("Error: Please check the input argumnets")
		elif(error_code == PLOT_NOT_VALID):
			print("Error: Value should be 0/1 , x value 0-4 and y value 0-4")
		elif(error_code == NO_CONNECTION):
			print("Error: Please connect the respective device")
		elif(error_code == SENSOR_PORT_NO_CHECK):
			print("Error: Please choose a value between 1-4")
		elif(error_code == NO_BUTTON_NAME):
			print("Error: Please choose the input argumnets as 'A'or'B'")
		print("**************************************************")


	def print_warning(self,warning_code):
		print("####################################################################")
		if(warning_code == LED_W_VALUE):
			print("Warning: Please choose a value between 0 - 100")
		elif(warning_code == SERVO_P_W_VALUE):
			print("Warning: Please choose a value between 0 - 180")
		elif(warning_code == SERVO_R_W_VALUE):
			print("Warning: Please choose a value between -100 - 100 ")
		elif(warning_code == PRINT_LENGTH_W_CODE):
			print("Warning: Length of the string should be between 1-18 ")
		elif(warning_code == PRINT_DISPLAY_W_CODE):
			print("Warning: Length of the string should be 25 characters of 0's/1's")
		print("####################################################################")


class Hummingbird(Microbit):

	#/led/<port>/<intensity>/<device instance>

	def __init__(self , s_no = 'A'):

		self.PrintDevices()
		self.device_s_no = s_no

	def print_device_info(self):
		print(self.device_s_no)

	def check_valid_params_1(self ,peri , port_no , value):
		if ((peri == "LED") or (peri =="servo_p") or (peri == "servo_r")):
			try :
				if((port_no > 4) or (port_no < 1)):
					error_code = LED_SERVO_PORT_NO_CHECK
					self.print_error(error_code)
					self.stopAll()
					sys.exit()
			except:
				self.print_error(GARBAGE_VALUE_PORT)
				sys.exit()

		if(peri == "LED" ):
			try :
				if((value < LED_MIN) or (value > LED_MAX)):
					warning_code = LED_W_VALUE;
					self.print_warning(warning_code)
			except:
				self.print_error(GARBAGE_VALUE_PORT)
				sys.exit()

		elif(peri == "servo_p"):
			try:
				if((value < SERVO_P_MIN) or (value > SERVO_P_MAX)):
					warning_code = SERVO_P_W_VALUE;
					self.print_warning(warning_code)
			except:
				self.print_error(GARBAGE_VALUE_PORT)
				sys.exit()

		elif(peri == "servo_r"):
			try:
				if((value < SERVO_R_MIN) or (value > SERVO_R_MAX)):
					warning_code = SERVO_R_W_VALUE;
					self.print_warning(warning_code)
			except:
				self.print_error(GARBAGE_VALUE_PORT)
				sys.exit()

	def check_valid_params_2(self ,peri , port_no , value_1 , value_2 , value_3):
		try:
			if(peri == "RGB"):
				if((port_no > 2) or (port_no < 1)):
					error_code = RGB_PORT_NO_CHECK
					self.print_error(error_code)
					self.stopAll()
					sys.exit()
			if(((value_1 < RGB_MIN ) or (value_1 > RGB_MAX)) or ((value_2 < RGB_MIN ) or (value_2 > RGB_MAX)) or ((value_3 < RGB_MIN ) or (value_3 > RGB_MAX))) :
				warning_code = RGB_W_VALUE
				print_warning(warning_code)
		except:
			self.print_error(GARBAGE_VALUE_PORT)
			sys.exit()
	
	def check_valid_params_4(self ,peri , port_no ):
		try:
			if(peri == "sensor"):
				if((port_no > 4) or (port_no < 1)):
					error_code = SENSOR_PORT_NO_CHECK
					self.print_error(error_code)
					self.stopAll()
					sys.exit()
		except:
			self.print_error(GARBAGE_VALUE_PORT)
			sys.exit()

	# def playNoteAndWait(self,frequency,duartion):
	# 	try:
	# 	except:

	# def playNotet(self,frequency,duartion):
	# 	try:
	# 	except:


	def setLED(self, port_no, intensity):
		self.check_valid_params_1("LED" , port_no, intensity)
		intensity_c = self.calculate_LED(intensity)
		response    = self.send_httprequest("led" , port_no , intensity_c)
		return response


	def setTriLED(self, port_no, r_intensity, g_intensity, b_intensity):
		self.check_valid_params_2("RGB" , port_no, r_intensity, g_intensity, b_intensity)
		(r_intensity_c, g_intensity_c, b_intensity_c) = self.calculate_RGB(r_intensity,g_intensity,b_intensity)
		response = self.send_httprequest("triled" , port_no , str(r_intensity_c)+ "/" + str(g_intensity_c) +"/" + str(b_intensity_c))
		return response

	def setPositionServo(self, port_no, angle):
		self.check_valid_params_1("servo_p" , port_no, angle)
		angle_c = self.calculate_servo_p(angle)
		response = self.send_httprequest("servo" , port_no , angle_c)
		return response

	def setRotationServo(self, port_no, speed):
		self.check_valid_params_1("servo_r", port_no, speed)   
		speed_c  = self.calculate_servo_r(speed)
		response = self.send_httprequest("rotation", port_no, speed_c)
		return response
	
	def getSensor(self,port_no):
		self.check_valid_params_4("sensor",port_no)
		response       = self.send_httprequest_in("sensor",port_no)
		return response

	def getLight(self, port_no):
		response = self.getSensor(port_no)
		light_value    = response * LIGHT_FACTOR
		return light_value

	def getSound(self, port_no):
		response = self.getSensor(port_no)
		sound_value    = response *SOUND_FACTOR
		return sound_value

	def getDistance(self, port_no):
		response = self.getSensor(port_no)
		distance_value    = response * DISTANCE_FACTOR
		return distance_value


	def getDail(self, port_no):
		response 	  = self.getSensor(port_no)
		dail_value    = response *DIAL_FACTOR
		if(dail_value > 100):
			dail_value = 100
		return dail_value



	def calculate_LED(self,intensity):
		intensity_c = 0
		intensity_c = int((intensity * 255) / 100) ;
		if (intensity_c > 255):
			intensity_c = 255
		elif (intensity_c < 0):
			intensity_c = 0
		return intensity_c


	def calculate_RGB(self,r_intensity, g_intensity, b_intensity):
		r_intensity_c   = int((r_intensity * 255) / 100) ;
		g_intensity_c   = int((g_intensity * 255) / 100) ;
		b_intensity_c	= int((b_intensity * 255) / 100) ;
		return (r_intensity_c,g_intensity_c,b_intensity_c)


	def calculate_servo_p(self,servo_value):
		servo_value_c   = int((servo_value * 254)/180) ;
		if (servo_value_c > 254):
			servo_value_c = 254
		elif (servo_value_c < 0):
			servo_value_c = 0
		return servo_value_c


	def calculate_servo_r(self,servo_value):
		
		if ((servo_value>-10) and (servo_value<10)):
			servo_value_c = 255
		elif servo_value>100:
			servo_value = 100
		elif servo_value< -100:
			servo_value = -100

		servo_value_c = int(( servo_value*23 /100) + 122)

		return servo_value_c

	

	def send_httprequest(self, peri, port_no , value):
		http_request = self.base_request_out + "/" + peri    + "/" + str(port_no) +  "/" + str(value)   + "/" + str(self.device_s_no) 
		try :
			response_request =  urllib.request.urlopen(http_request)
		except:
			self.print_error(CONNECTION_SERVER_CLOSED)
			sys.exit();
		if(response_request.read() == b'200'):
			response = 1
		else :
			response = 0
		return response


	def send_httprequest_in(self, peri, port_no):
		http_request = self.base_request_in + "/" + peri    + "/" + str(port_no) + "/" + str(self.device_s_no) 
		try :
			response_request =  urllib.request.urlopen(http_request)
		except:
			self.print_error(CONNECTION_SERVER_CLOSED)
			sys.exit();
		response = response_request.read().decode('utf-8')
		if(response == "Not Connected"):
			self.print_error(NO_CONNECTION)
			sys.exit()

		return int(response)


	def stopAll(self):		
		response = 1
		return response







































