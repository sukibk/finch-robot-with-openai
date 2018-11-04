###############################################################
###############################################################
#Author                  Raghunath J
#Last Edit Date          10/24/2018
#Description             This python file contains the driver 
#						 to interact with BluebirdConnector.
#						 Link to API -- 
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
RGB_W_VALUE = 6


#Error Codes
SERVO_PORT_NO_CHECK      = 1
RGB_PORT_NO_CHECK  		 = 2
CONNECTION_SERVER_CLOSED = 3
GARBAGE_VALUE_PORT       = 4
PRINT_DISPLAY_E_CODE 	 = 5
PLOT_NOT_VALID 			 = 6
NO_CONNECTION 			 = 7
NO_BUTTON_NAME           = 8
SENSOR_PORT_NO_CHECK     = 9
LED_PORT_NO_CHECK      	 = 10
BUZZER_NOTE_CHECK		 = 11 
BUZZER_BEAT_CHECK		 = 12


#Calculations after receveing the raw values
DISTANCE_FACTOR          = 117/100
SOUND_FACTOR             = 200/255
DIAL_FACTOR              = 100/230
LIGHT_FACTOR             = 100/255

TEMPO 					 = 60
###############################################################
###############################################################

#Microbit Class includes the control of the outputs and inputs
#present on the microbit.

##############################################################
###############################################################
class Microbit:
	""" Test requests to find the devices connected""" 
	base_request_out = "http://127.0.0.1:30061/hummingbird/out"
	base_request_in  = "http://127.0.0.1:30061/hummingbird/in"
	stopall          = "http://127.0.0.1:30061/hummingbird/out/stopall"
	shake_A			 = "http://127.0.0.1:30061/hummingbird/in/orientation/Shake/A"
	shake_B			 = "http://127.0.0.1:30061/hummingbird/in/orientation/Shake/B"
	shake_C			 = "http://127.0.0.1:30061/hummingbird/in/orientation/Shake/C"
	sensor4_A        = "http://127.0.0.1:30061/hummingbird/in/sensor/4/A"
	sensor4_B        = "http://127.0.0.1:30061/hummingbird/in/sensor/4/B"
	sensor4_C        = "http://127.0.0.1:30061/hummingbird/in/sensor/4/C"
	
	symbolvalue      =  None


	###############################################################################################################
	#######################     UTILITY FUNCTIONS                                ##################################
	###############################################################################################################

	""" Called whenever a class is initialized"""
	def __init__(self, s_no = 'A'):
		self.PrintDevices()
		self.device_s_no = s_no
	###############################################################################################################

	""" Prints the type of the device which you are connected , very useful to know what 
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
					device.append("Hummingbird Bit")
				else:
					device.append("micro:bit")
			else:
				device.append("None")
			length = length + 1
		print ("Device A:  " + device[0])
		print ("Device B:  " + device[1])
		print ("Device C:  " + device[2])
	###############################################################################################################
		
	""" Check to see if the input arguments of print statement are valid"""
	def check_valid_params_3(self,peri , string_value):
		try:
			if(peri == "print"):
				"""Check if the length of the LED Array is greater than 18"""
				if( len(string_value) > 18):
					self.print_warning(PRINT_LENGTH_W_CODE)
			else:
				"""Check if the length of the array to form a symbol is greater than 25"""
				if(len(string_value) != 25):
					self.print_warning(PRINT_DISPLAY_W_CODE)
				for letter in string_value:
					"""Check if all the 25 characters entered are valid"""
					if ((letter != '0') and (letter != '1')):
						sys.exit();
		except:
			self.print_error(GARBAGE_VALUE_PORT)
			sys.exit()
	###############################################################################################################

	""" Convert a string of 1's and 0's into true and false"""
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
	###############################################################################################################
	###############################################################################################################
	###############################################################################################################


	###############################################################################################################
	#######################     OUTPUTS MICRO BIT #################################################################
	############################################################################################################### 
	""" Set Display of the LED Array on microbit  with the given input LED_string """
	def setDisplay(self, LED_string):
		"""Check if LED_string is valid to be printed on the display"""
		self.check_valid_params_3("Display" , LED_string)
		"""Convert the LED_string to  an appropriate value which the server can understad"""
		LED_string_c = self.process_display(LED_string)
		"""Send the http request"""
		response = self.send_httprequest_micro("symbol",LED_string_c)
		return response
    ###############################################################################################################

	"""Print the characters on the LED screen  """
	def print(self, Print_string):
		"""Check if the print string is valid to be printed on the screen i.e length of the string is less than 18"""
		self.check_valid_params_3("print" , Print_string)
		"""Send the http request"""
		response = self.send_httprequest_micro("print",Print_string)
		return response
	###############################################################################################################
	
	
	"""Choose a certain LED on the LED Array and switch on/switch off the respective LED"""
	def setPoint(self, x , y , value):
		value = str(value)
		new_str = None
		"""Check if x, y and value is valid""" 
		if((x > 4) or (x<0) or (y<0) or (y>4) or ((value != '0') and (value != '1'))):
			self.print_error(PLOT_NOT_VALID)
			sys.exit()
		else :
			"""Calculate which LED should be selected"""
			index = x*5 + y
			""" Select the LED to be changed and make the others zero if this is the first time other wise use the previous value"""
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
			"""Send to the function which sends the http request"""
			self.setDisplay(self.symbolvalue)
	###############################################################################################################
	###############################################################################################################
	###############################################################################################################


	###############################################################################################################
	##############################       INPUTS MICROBIT                ###########################################
	###############################################################################################################
	
	"""Gives the acceleration of X,Y,Z in m/sec2"""
	def getAcceleration(self):
		dimension = ['X','Y','Z']
		acc_value = []  
		try:
			for i in range(0,3):
				"""Send HTTP request"""
				response = self.send_httprequest_micro_in("Accelerometer",dimension[i])
				acc_value.append(response)
		except:
			self.print_error(NO_CONNECTION)
			sys.exit()
		""" Round the value to 2 decimal places """
		acc_x 	=	round((float(acc_value[0])),3)
		acc_y 	=	round((float(acc_value[1])),3)
		acc_z 	=	round((float(acc_value[2])),3)
		return (acc_x,acc_y,acc_z)
	###############################################################################################################
	
	""" Returns values 0-359 indicating the orentation of the Earth's magnetic field"""  
	def getCompass(self):
		try:
			"""Send HTTP request"""
			response = self.send_httprequest_micro_in("Compass",None)
			compass_heading = int(response)
			return compass_heading
		except:
			self.print_error(NO_CONNECTION)
			sys.exit()
	###############################################################################################################
	
	"""Return the values of X,Y,Z of a magnetommeter"""
	def getMagnetometer(self):
		dimension = ['X','Y','Z']
		mag_value = []  
		try:
			for i in range(0,3):
				"""Send HTTP request"""
				response = self.send_httprequest_micro_in("Magnetometer",dimension[i])
				mag_value.append(response)
		except:
			self.print_error(NO_CONNECTION)
			sys.exit()
		mag_x 	=	int(mag_value[0])
		mag_y 	=	int(mag_value[1])
		mag_z 	=	int(mag_value[2])
		return (mag_x,mag_y,mag_z)
	###############################################################################################################

	"""Return the status of the button asked """
	def getButton(self,button_name):
		try:
			button_name = button_name.upper()
			""" Check if the button A and button B are represented in a valid manner"""
			if((button_name != 'A') and (button_name != 'B')):
				sys.exit()
			"""Send HTTP request"""
			response = self.send_httprequest_micro_in("button", button_name)
			"""Convert to boolean form"""
			if(response == "true"):
				button_value = True
			else:
				button_value = False
		except:
			self.print_error(NO_BUTTON_NAME)
			exit()
		return button_value
	###############################################################################################################

	"""Return the True/False based on the device status of shake """
	def isShaking(self):
		try:
			"""Send HTTP request"""
			response = self.send_httprequest_micro_in("Shake",None)
			shake    = response
		except:
			self.print_error(NO_CONNECTION)
			sys.exit()
		return shake
	###############################################################################################################

	"""Return the orentation of device listed in the orention_result list"""
	def getOrientation(self):
		orentation = ["Screen%20Up","Screen%20Down","Tilt%20Left","Tilt%20Right","Logo%20Up","Logo%20Down"]
		orentation_result = ["ScreenUp","ScreenDown","TiltLeft","TiltRight","LogoUp","LogoDown","Shake"]
		try:
			response = self.isShaking()
			if(response == "true"):
				return orentation_result[6]
			""" Check for orientation of each device and if true return that state """
			for i in range(0,6):
				response = self.send_httprequest_micro_in(orentation[i],None)
				if(response == "true"):
					return orentation_result[i]
		except:
			self.print_error(NO_CONNECTION)
			sys.exit()
		"""If we are in a state in which none of the above seven states are true"""
		return "In Between"
	###############################################################################################################
	###############################################################################################################
	###############################################################################################################

	###############################################################################################################
	#######################        SEND HTTP REQUESTS               ###############################################
	###############################################################################################################
	""" Utility function to arrange and send the hrrp request for microbit output functions """
	def send_httprequest_micro(self, peri , value):
		"""Print command  """
		if(peri == "print"):
			http_request = self.base_request_out + "/" + peri +  "/" + str(value)   + "/" + str(self.device_s_no)
		elif(peri == "symbol"):
			http_request = self.base_request_out + "/" + peri +  "/"  + str(self.device_s_no)  + "/" + str(value)
		try :
			response_request =  urllib.request.urlopen(http_request)
			if(response_request.read() == b'200'):
				response = 1
			else :
				response = 0
		except:
			self.print_error(CONNECTION_SERVER_CLOSED)
			sys.exit()
		return response
	###############################################################################################################

	""" Utility function to arrange and send the hrrp request for microbit input functions """
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
	###############################################################################################################

	"""Utility function to print error based on error codes """
	def print_error(self,error_code):
		print("**************************************************")
		if(error_code == LED_PORT_NO_CHECK):
			print("Error: Please choose a port value between 1-3")
		elif(error_code == RGB_PORT_NO_CHECK):
			print("Error: Please choose a port value between 1-2")
		elif(error_code == CONNECTION_SERVER_CLOSED):
			print("Error: Please open the BlueBird Connection App / unexpected disconnection")
		elif(error_code == GARBAGE_VALUE_PORT):
			print("Error: Please check the input arguments")
		elif(error_code == PLOT_NOT_VALID):
			print("Error: Value should be 0/1 , x value 0-4 and y value 0-4")
		elif(error_code == NO_CONNECTION):
			print("Error: Please connect the respective device")
		elif(error_code == SENSOR_PORT_NO_CHECK):
			print("Error: Please choose a value between 1-3")
		elif(error_code == NO_BUTTON_NAME):
			print("Error: Please choose the input argumnets as 'A' or 'B' ")
		elif(error_code == SERVO_PORT_NO_CHECK):
			print("Error: Please choose a port value between 1-4")
		elif(error_code == BUZZER_NOTE_CHECK):
			print("Error: Please choose a note value between 32-135")
		elif(error_code == BUZZER_BEAT_CHECK):
			print("Error: Please choose a beat value between 0-16")
		print("**************************************************")
		"""Utility function to print warnings based on warning codes """
	###############################################################################################################
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
		elif(warning_code == RGB_W_VALUE):
			print("Warning: Please choose RGB intensity value between 0-100")
		elif(warning_code == PRINT_DISPLAY_W_CODE):
			print("Warning: Length of the string should be 25 characters of 0's/1's")
		print("####################################################################")
	###############################################################################################################
	###############################################################################################################
	###############################################################################################################


##################################################################################################################
##################################################################################################################

#Hummingbird Bit Class includes the control of the outputs and inputs
#present on the Hummingbird Bit.

##################################################################################################################
##################################################################################################################
class Hummingbird(Microbit):

	######################  UTILITY FUNCTIONS ####################################################################
	##############################################################################################################
	##############################################################################################################
	def __init__(self , s_no = 'A'):
		self.PrintDevices()
		self.device_s_no = s_no
	#############################################################################################################

	"""  Print the devices that are connected to the Bluebird App  """
	def print_device_info(self):
		print(self.device_s_no)
	############################################################################################################

	"""  Utility function to check if the parameters of LED , servo are valid  """
	def check_valid_params_1(self ,peri , port , value):
		if(peri == "LED"):
			try:
				"""Check the port of the LED selected is within the range of 1-3"""
				if((port > 3) or (port < 1)):
					self.stopAll()
					sys.exit()
			except:
				self.print_error(LED_PORT_NO_CHECK)
				sys.exit()
		elif ((peri =="servo_p") or (peri == "servo_r")):
			try :
				"""Check the port of the servo selected is within the range of 1-4"""
				if((port > 4) or (port < 1)):
					self.stopAll()
					sys.exit()
			except:
				self.print_error(SERVO_PORT_NO_CHECK)
				sys.exit()	
		if(peri == "LED" ):
			try :
				"""Check the intensity value lies with in the range of LED limits"""
				if((value < LED_MIN) or (value > LED_MAX)):
					warning_code = LED_W_VALUE;
					self.print_warning(warning_code)
			except:
				self.print_error(GARBAGE_VALUE_PORT)
				sys.exit()

		elif(peri == "servo_p"):
			try:
				"""Check the intensity value lies with in the range of position servo limits"""
				if((value < SERVO_P_MIN) or (value > SERVO_P_MAX)):
					warning_code = SERVO_P_W_VALUE;
					self.print_warning(warning_code)
			except:
				self.print_error(GARBAGE_VALUE_PORT)
				sys.exit()

		elif(peri == "servo_r"):
			try:
				"""Check the intensity value lies with in the range of roatation servo limits"""
				if((value < SERVO_R_MIN) or (value > SERVO_R_MAX)):
					warning_code = SERVO_R_W_VALUE;
					self.print_warning(warning_code)
			except:
				self.print_error(GARBAGE_VALUE_PORT)
				sys.exit()
	##################################################################################################################

	"""  Utility function to check if the parameters of RGB  are valid  """
	def check_valid_params_2(self ,peri , port , value_1 , value_2 , value_3):
		try:
			"""Check the port of the RGB selected is within the range of 1-2"""
			if(peri == "RGB"):
				if((port > 2) or (port < 1)):
					self.stopAll()
					sys.exit()
		except:
			self.print_error(RGB_PORT_NO_CHECK)
			sys.exit()

		"""Check the intensity value lies with in the range of RGB LED limits"""
		if(((value_1 < RGB_MIN ) or (value_1 > RGB_MAX)) or ((value_2 < RGB_MIN ) or (value_2 > RGB_MAX)) or ((value_3 < RGB_MIN ) or (value_3 > RGB_MAX))) :
			warning_code = RGB_W_VALUE
			self.print_warning(warning_code)
	##################################################################################################################
		
	"""  Utility function to check if the parameters of Sensors  are valid  """
	def check_valid_params_4(self ,peri , port ):
		try:
			"""Check the port of the sensor selected is within the range of 1-2"""
			if(peri == "sensor"):
				if((port > 3) or (port < 1)):
					
					self.stopAll()
					sys.exit()
		except:
			self.print_error(SENSOR_PORT_NO_CHECK)
			sys.exit()
	##################################################################################################################

	"""  Utility function to check if the parameters of buzzer are valid  """
	def check_valid_params_buzzer(self , note , beats ):
		try:
			"""Check if the note is within the range"""
			if((note > 135) or (note < 32)):
				self.stopAll()
				sys.exit()
		except:
			self.print_error(BUZZER_NOTE_CHECK)
			sys.exit()
		try:
			"""Check if the beat is within the range"""
			if((beats > 16) or (beats < 0)):
				self.stopAll()
				sys.exit()
		except:
			self.print_error(BUZZER_BEAT_CHECK)
			sys.exit()
	##################################################################################################################

	"""Utiltity function to checkif the intensity of RGB ,LED are in check"""
	def checkIntensity(self, intensity):
		if (intensity > 255):
			intensity = 255
		elif (intensity < 0):
			intensity = 0
		return intensity
	##################################################################################################################

	""" Utility function to covert LED from 0-100 to 0-255"""
	def calculate_LED(self,intensity):
		intensity_c = 0
		intensity_c = int((intensity * 255) / 100) ;
		""" If the vlaues are above the limits fix the instensity to maximum value, if less than the minimum value fix the intensity to minimum value"""
		intensity_c = self.checkIntensity(intensity_c)
		return intensity_c
	##################################################################################################################

	""" Utility function to covert RGB LED from 0-100 to 0-255"""
	def calculate_RGB(self,r_intensity, g_intensity, b_intensity):
		r_intensity_c   = int((r_intensity * 255) / 100) ;
		g_intensity_c   = int((g_intensity * 255) / 100) ;
		b_intensity_c	= int((b_intensity * 255) / 100) ;
		""" If the vlaues are above the limits fix the instensity to maximum value, if less than the minimum value fix the intensity to minimum value"""
		r_intensity_c = self.checkIntensity(r_intensity_c)
		g_intensity_c = self.checkIntensity(g_intensity_c)
		b_intensity_c = self.checkIntensity(b_intensity_c)
		return (r_intensity_c,g_intensity_c,b_intensity_c)
	##################################################################################################################

	""" Utility function to covert Servo from 0-180 to 0-255"""
	def calculate_servo_p(self,servo_value):
		servo_value_c   = int((servo_value * 254)/180) ;
		""" If the vlaues are above the limits fix the instensity to maximum value, if less than the minimum value fix the intensity to minimum value"""
		if (servo_value_c > 254):
			servo_value_c = 254
		elif (servo_value_c < 0):
			servo_value_c = 0
		return servo_value_c
	##################################################################################################################

	""" Utility function to covert Servo from -100 - 100 to 0-255"""
	def calculate_servo_r(self,servo_value):
		""" If the vlaues are above the limits fix the instensity to maximum value, if less than the minimum value fix the intensity to minimum value"""
		if ((servo_value>-10) and (servo_value<10)):
			servo_value_c = 255
		elif servo_value>100:
			servo_value_c = 100
		elif servo_value< -100:
			servo_value_c = -100
		else:
			servo_value_c = int(( servo_value*23 /100) + 122)
		return servo_value_c
	##################################################################################################################

	


	##################################################################################################################
	###########################     HUMMINGBIRD BIT OUTPUT  ##########################################################
	##################################################################################################################

	"""Set LED  of a certain port requested to a valid intensity"""
	def setLED(self, port, intensity):
		self.check_valid_params_1("LED" , port, intensity)
		"""Change the range from 0-100 to 0-255"""
		intensity_c = self.calculate_LED(intensity)
		"""Send HTTP request """
		response    = self.send_httprequest("led" , port , intensity_c)
		return response
	##################################################################################################################

	"""Set TriLED  of a certain port requested to a valid intensity"""
	def setTriLED(self, port, r_intensity, g_intensity, b_intensity):
		self.check_valid_params_2("RGB" , port, r_intensity, g_intensity, b_intensity)
		"""Change the range from 0-100 to 0-255"""
		(r_intensity_c, g_intensity_c, b_intensity_c) = self.calculate_RGB(r_intensity,g_intensity,b_intensity)
		"""Send HTTP request """
		response = self.send_httprequest("triled" , port , str(r_intensity_c)+ "/" + str(g_intensity_c) +"/" + str(b_intensity_c))
		return response
	##################################################################################################################

	"""Set Position servo of a certain port requested to a valid angle"""
	def setPositionServo(self, port, angle):
		self.check_valid_params_1("servo_p" , port, angle)
		angle_c = self.calculate_servo_p(angle)
		"""Send HTTP request """
		response = self.send_httprequest("servo" , port , angle_c)
		return response
	##################################################################################################################

	"""Set Rotation servo of a certain port requested to a valid speed"""
	def setRotationServo(self, port, speed):
		self.check_valid_params_1("servo_r", port, speed)   
		speed_c  = self.calculate_servo_r(speed)
		"""Send HTTP request """
		response = self.send_httprequest("rotation", port, speed_c)
		return response
	##################################################################################################################
	
	""" Make the buzzer play a note for certain number of beats"""
	def playNote(self, note ,beats ):
		self.check_valid_params_buzzer(note , beats)
		beats = int(beats * (60000/TEMPO))
		"""Send HTTP request """
		response = self.send_httprequest_buzzer(note, beats)
		return response
	##################################################################################################################

	""" Stop all stops the Servos , LED , ORB , LED Array """ 
	def stopAll(self):		
		response = self.send_httprequest_stopAll()
		return response
	##################################################################################################################

	##################################################################################################################
	###########################     HUMMINGBIRD BIT INPUT   ##########################################################
	##################################################################################################################

	""" Read the value of  the sensor attached to a certain port"""
	def getSensor(self,port):
		self.check_valid_params_4("sensor",port)
		response       = self.send_httprequest_in("sensor",port)
		return response
	##################################################################################################################

	""" Read the value of  the light sensor attached to a certain port"""
	def getLight(self, port):
		response = self.getSensor(port)
		light_value    = int(response * LIGHT_FACTOR)
		return light_value
	##################################################################################################################

	""" Read the value of  the sound sensor attached to a certain port"""
	def getSound(self, port):
		response = self.getSensor(port)
		sound_value    = int(response *SOUND_FACTOR)
		return sound_value
	##################################################################################################################

	""" Read the value of  the distance sensor attached to a certain port"""
	def getDistance(self, port):
		response = self.getSensor(port)
		distance_value    = int(response * DISTANCE_FACTOR)
		return distance_value
	##################################################################################################################

	""" Read the value of  the dial attached to a certain port"""
	def getDial(self, port):
		response 	  = self.getSensor(port)
		dail_value    = int(response *DIAL_FACTOR)
		if(dail_value > 100):
			dail_value = 100
		return dail_value
	##################################################################################################################



	
	##################################################################################################################
	###########################    SEND HTTP REQUESTS       ##########################################################
	##################################################################################################################
	
	"""Send HTTP requests for Hummingbird bit inputs """
	def send_httprequest_in(self, peri, port):
		""" Combine diffrenet strings to form a HTTP request """ 
		http_request = self.base_request_in + "/" + peri    + "/" + str(port) + "/" + str(self.device_s_no) 
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
	##################################################################################################################

	"""Send HTTP request for Hummingbird bit output"""
	def send_httprequest(self, peri, port , value):
		""" Combine diffrenet strings to form a HTTP request """ 
		http_request = self.base_request_out + "/" + peri    + "/" + str(port) +  "/" + str(value)   + "/" + str(self.device_s_no) 
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
	##################################################################################################################


	"""Send HTTP request for hummingbird bit output"""
	def send_httprequest_stopAll(self):
		""" Combine diffrenet strings to form a HTTP request """ 
		http_request = self.stopall
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
	##################################################################################################################

	""" Send HTTP request for hummingbird bit buzzer """
	def send_httprequest_buzzer(self, note, beats):
		""" Combine diffrenet strings to form a HTTP request """ 
		http_request = self.base_request_out + "/" + "playnote" +  "/" + str(note)   + "/" + str(beats)   + "/" + str(self.device_s_no) 
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
	##################################################################################################################
	##################################################################################################################
	##################################################################################################################

	







































