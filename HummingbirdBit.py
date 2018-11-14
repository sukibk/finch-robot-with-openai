###############################################################
###############################################################
# Author                  Raghunath J, revised by Bambi Brewer
# Last Edit Date          11/12/2018
# Description             This python file contains Microbit and Hummingbird classes.
# The Microbit class controls a micro:bit via bluetooth. It includes methods to print on the micro:bit LED array or 
# set those LEDs individually. It also contains methods to read the values of the micro:bit accelerometer and magnetometer.
# The Hummingbird class extends the Microbit class to incorporate functions to control the inputs and outputs
# of the Hummingbird Bit. It includes methods to set the values of motors and LEDs, as well
# as methods to read the values of the sensors.
###############################################################
###############################################################
import urllib.request
import sys
import time
###############################################################
###############################################################
#Constants 

CHAR_FLASH_TIME = 0.3		#Character Flash time

# Error strings
CONNECTION_SERVER_CLOSED = "Error: Request to device failed"
NO_CONNECTION = "Error: The device is not connected"

#Calculations after receveing the raw values
DISTANCE_FACTOR          = 117/100
SOUND_FACTOR             = 200/255
DIAL_FACTOR              = 100/230
LIGHT_FACTOR             = 100/255
VOLTAGE_FACTOR			 = 3.3/255

TEMPO 					 = 60
###############################################################
###############################################################

#Microbit Class includes the control of the outputs and inputs
#present on the micro:bit.

##############################################################
###############################################################
class Microbit:
	""" Test requests to find the devices connected""" 
	base_request_out = "http://127.0.0.1:30061/hummingbird/out"
	base_request_in  = "http://127.0.0.1:30061/hummingbird/in"
	stopall          = "http://127.0.0.1:30061/hummingbird/out/stopall"
	
	symbolvalue      =  None


	###############################################################################################################
	#######################     UTILITY FUNCTIONS                                ##################################
	###############################################################################################################

	""" Called whenever a class is initialized"""
	def __init__(self, device = 'A'):
		"""Check if the letter of the device is valid, exit otherwise"""
		if('ABC'.find(device) != -1):
			self.device_s_no = device
			self.symbolvalue = [0]*25
		else:
			print("Error: Device must be A, B, or C.")
			self.stopAll()
			sys.exit()
		
	# This function checks whether an input parameter is within the given bounds. If not, it prints
	# a warning and returns a value of the input parameter that is within the required range.
	# Otherwise, it just returns the initial value.
	def clampParametersToBounds(self, input, inputMin, inputMax):
		if ((input < inputMin) or (input > inputMax)):
			print("Warning: Please choose a parameter between " + str(inputMin) + " and " + str(inputMax))
			return max(inputMin, min(input, inputMax))
		else:
			return input

	###############################################################################################################
	
	""" Convert a string of 1's and 0's into true and false"""
	def process_display(self , value):
		new_str = ""
		for letter in value:
			if(letter == 0):
				new_str += "false/"
			else:					#All nonzero values become true
				new_str += "true/"
		
		# Remove the last character in a string
		new_str = new_str[:len(new_str)-1]
		return new_str
	###############################################################################################################
	###############################################################################################################
	###############################################################################################################


	###############################################################################################################
	#######################     OUTPUTS MICRO BIT #################################################################
	############################################################################################################### 
	""" Set Display of the LED Array on microbit  with the given input LED list of 0's and 1's """
	def setDisplay(self, LEDlist):
		"""Check if LED_string is valid to be printed on the display"""
		"""Check if the length of the array to form a symbol not equal than 25"""
		if(len(LEDlist) != 25):
			print("Error: setDisplay() requires a list of length 25")
			return 			# if the array is the wrong length, don't want to do anything else
		
		"""Check if all the characters entered are valid"""
		for index in range(0,len(LEDlist)):
			LEDlist[index] = self.clampParametersToBounds(LEDlist[index],0,1) 
		
		# Reset the display status
		self.symbolvalue = LEDlist

		"""Convert the LED_list to  an appropriate value which the server can understand"""
		LED_string = self.process_display(LEDlist)
		"""Send the http request"""
		response = self.send_httprequest_micro("symbol",LED_string)
		return response
    ###############################################################################################################

	"""Print the characters on the LED screen  """
	def print(self, message):
		
		"""Check if the print string is valid to be printed on the screen i.e length of the string is less than 18"""
		if(len(message) > 15):
			print("Warning: print() requires a String with 15 or fewer characters")

		# Warn the user about any special characters - we can mostly only print English characters and digits
		for letter in message:
			if not (((letter >= 'a') and (letter <= 'z')) or ((letter >= 'A') and (letter <= 'Z')) or ((letter >= '0') and (letter <= '9')) or (letter == ' ')):
				print("Warning: Many special characters cannot be printed on the LED display")

		# Need to replace spaces with %20
		message = message.replace(' ','%20')

		# Empty out the internal representation of the display, since it will be blank when the print ends
		self.symbolvalue = [0]*25

		"""Send the http request"""
		response = self.send_httprequest_micro("print",message)
		return response
	###############################################################################################################
	
	
	"""Choose a certain LED on the LED Array and switch on/switch off the respective LED"""
	def setPoint(self, x , y , value):
		"""Check if x, y and value are valid""" 
		x = self.clampParametersToBounds(x,1,5)
		y = self.clampParametersToBounds(y,1,5)
		value = self.clampParametersToBounds(value,0,1)
		
		"""Calculate which LED should be selected"""
		index = (x-1)*5 + (y-1)
		
		# Update the state of the LED displayf
		self.symbolvalue[index] = value
		
		"""Convert the display status to  an appropriate value which the server can understand"""
		outputString = self.process_display(self.symbolvalue)

		"""Send the http request"""
		response = self.send_httprequest_micro("symbol",outputString)
		return response
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
		for i in range(0,3):
			"""Send HTTP request"""
			response = self.send_httprequest_micro_in("Accelerometer",dimension[i])
			acc_value.append(response)
		
		""" Round the value to 2 decimal places """
		acc_x 	=	round((float(acc_value[0])),3)
		acc_y 	=	round((float(acc_value[1])),3)
		acc_z 	=	round((float(acc_value[2])),3)
		return (acc_x,acc_y,acc_z)
	###############################################################################################################
	
	""" Returns values 0-359 indicating the orentation of the Earth's magnetic field"""  
	def getCompass(self):
		"""Send HTTP request"""
		response = self.send_httprequest_micro_in("Compass",None)
		compass_heading = int(response)
		return compass_heading
		
	###############################################################################################################
	
	"""Return the values of X,Y,Z of a magnetommeter"""
	def getMagnetometer(self):
		dimension = ['X','Y','Z']
		mag_value = []  
		
		for i in range(0,3):
			"""Send HTTP request"""
			response = self.send_httprequest_micro_in("Magnetometer",dimension[i])
			mag_value.append(response)
		
		mag_x 	=	int(mag_value[0])
		mag_y 	=	int(mag_value[1])
		mag_z 	=	int(mag_value[2])
		return (mag_x,mag_y,mag_z)
	###############################################################################################################

	"""Return the status of the button asked """
	def getButton(self,button):
		button = button.upper()
		""" Check if the button A and button B are represented in a valid manner"""
		if((button != 'A') and (button != 'B')):
			sys.exit()
		"""Send HTTP request"""
		response = self.send_httprequest_micro_in("button", button)
		"""Convert to boolean form"""
		if(response == "true"):
			button_value = True
		else:
			button_value = False
		
		return button_value
	###############################################################################################################

	"""Return the True/False based on the device status of shake """
	def isShaking(self):
		"""Send HTTP request"""
		response = self.send_httprequest_micro_in("Shake",None)
		if(response == "true"):		# convert to boolean
			shake = True
		else:
			shake = False
		
		return shake
	###############################################################################################################

	"""Return the orentation of device listed in the orention_result list"""
	def getOrientation(self):
		orientations = ["Screen%20Up","Screen%20Down","Tilt%20Left","Tilt%20Right","Logo%20Up","Logo%20Down"]
		orientation_result = ["Screen up","Screen down","Tilt left","Tilt right","Logo up","Logo down"]
		
		""" Check for orientation of each device and if true return that state """
		for targetOrientation in orientations:
			response = self.send_httprequest_micro_in(targetOrientation,None)
			if(response == "true"):
				return orientation_result[orientations.index(targetOrientation)]
		
		"""If we are in a state in which none of the above seven states are true"""
		return "In between"
	###############################################################################################################
	""" Stop all stops the Servos , LED , ORB , LED Array """ 
	def stopAll(self):		
		response = self.send_httprequest_stopAll()
		return response
	##################################################################################################################


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
			print(CONNECTION_SERVER_CLOSED)
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
			print(CONNECTION_SERVER_CLOSED)
			sys.exit();
		response = response_request.read().decode('utf-8')
		if(response == "Not Connected"):
			print(NO_CONNECTION)
			sys.exit()
		return response
	
	##################################################################################################################


	"""Send HTTP request for hummingbird bit output"""
	def send_httprequest_stopAll(self):
		""" Combine diffrenet strings to form a HTTP request """ 
		http_request = self.stopall + "/" +str(self.device_s_no)
		try :
			response_request =  urllib.request.urlopen(http_request)
		except:
			print(CONNECTION_SERVER_CLOSED)
			sys.exit();
		if(response_request.read() == b'200'):
			response = 1
		else :
			response = 0
		return response
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
	def __init__(self , device = 'A'):
		try: 
			"""Check if the length of the array to form a symbol is greater than 25"""
			if('ABC'.find(device) != -1):
				self.device_s_no = device
				self.symbolvalue = [0]*25
			else:
				self.stopAll()
				sys.exit()
		except:
			print("Error: Device must be A, B, or C.")

	#############################################################################################################

	# This function checks whether a port is within the given bounds. It returns a boolean value 
	# that is either true or false and prints an error if necessary
	def isPortValid(self, port, portMax):
		if ((port < 1) or (port > portMax)):
			print("Error: Please choose a port value between 1 and " + str(portMax))
			return False
		else:
			return True	
	##################################################################################################################

	""" Utility function to covert LED from 0-100 to 0-255"""
	def calculate_LED(self,intensity):
		intensity_c = int((intensity * 255) / 100) ;
		
		return intensity_c
	##################################################################################################################

	""" Utility function to covert RGB LED from 0-100 to 0-255"""
	def calculate_RGB(self,r_intensity, g_intensity, b_intensity):
		r_intensity_c   = int((r_intensity * 255) / 100) ;
		g_intensity_c   = int((g_intensity * 255) / 100) ;
		b_intensity_c	= int((b_intensity * 255) / 100) ;
		
		return (r_intensity_c,g_intensity_c,b_intensity_c)
	##################################################################################################################

	""" Utility function to covert Servo from 0-180 to 0-255"""
	def calculate_servo_p(self,servo_value):
		servo_value_c   = int((servo_value * 254)/180) ;
		
		return servo_value_c
	##################################################################################################################

	""" Utility function to covert Servo from -100 - 100 to 0-255"""
	def calculate_servo_r(self,servo_value):
		""" If the vlaues are above the limits fix the instensity to maximum value, if less than the minimum value fix the intensity to minimum value"""
		if ((servo_value>-10) and (servo_value<10)):
			servo_value_c = 255
		else:
			servo_value_c = int(( servo_value*23 /100) + 122)
		return servo_value_c
	##################################################################################################################


	##################################################################################################################
	###########################     HUMMINGBIRD BIT OUTPUT  ##########################################################
	##################################################################################################################

	"""Set LED  of a certain port requested to a valid intensity"""
	def setLED(self, port, intensity):
		# Early return if we can't execute the command because the port is invalid
		if not self.isPortValid(port,2):
			return

		"""Check the intensity value lies with in the range of LED limits"""
		intensity = self.clampParametersToBounds(intensity,0,100)

		"""Change the range from 0-100 to 0-255"""
		intensity_c = self.calculate_LED(intensity)
		"""Send HTTP request """
		response    = self.send_httprequest("led" , port , intensity_c)
		return response
	##################################################################################################################

	"""Set TriLED  of a certain port requested to a valid intensity"""
	def setTriLED(self, port, redIntensity, greenIntensity, blueIntensity):
		
		# Early return if we can't execute the command because the port is invalid
		if not self.isPortValid(port,2):
			return
		
		"""Check the intensity value lies with in the range of RGB LED limits"""
		red = self.clampParametersToBounds(redIntensity,0,100)
		green = self.clampParametersToBounds(greenIntensity,0,100)
		blue = self.clampParametersToBounds(blueIntensity,0,100)
		
		"""Change the range from 0-100 to 0-255"""
		(r_intensity_c, g_intensity_c, b_intensity_c) = self.calculate_RGB(red,green,blue)
		"""Send HTTP request """
		response = self.send_httprequest("triled" , port , str(r_intensity_c)+ "/" + str(g_intensity_c) +"/" + str(b_intensity_c))
		return response
	##################################################################################################################

	"""Set Position servo of a certain port requested to a valid angle"""
	def setPositionServo(self, port, angle):
		# Early return if we can't execute the command because the port is invalid
		if not self.isPortValid(port,4):
			return

		"""Check the angle lies within servo limits"""
		angle = self.clampParametersToBounds(angle,0,180)

		angle_c = self.calculate_servo_p(angle)
		"""Send HTTP request """
		response = self.send_httprequest("servo" , port , angle_c)
		return response
	##################################################################################################################

	"""Set Rotation servo of a certain port requested to a valid speed"""
	def setRotationServo(self, port, speed):
		# Early return if we can't execute the command because the port is invalid
		if not self.isPortValid(port,4):
			return

		"""Check the speed lies within servo limits"""
		speed = self.clampParametersToBounds(speed,-100,100)

		speed_c  = self.calculate_servo_r(speed)
		"""Send HTTP request """
		response = self.send_httprequest("rotation", port, speed_c)
		return response
	##################################################################################################################
	
	""" Make the buzzer play a note for certain number of beats"""
	def playNote(self, note, beats ):
		
		### Check that both parameters are within the required bounds
		note = self.clampParametersToBounds(note,32,135)
		beats = self.clampParametersToBounds(beats,0,16)

		beats = int(beats * (60000/TEMPO))
		"""Send HTTP request """
		response = self.send_httprequest_buzzer(note, beats)
		return response
	##################################################################################################################

	
	##################################################################################################################
	###########################     HUMMINGBIRD BIT INPUT   ##########################################################
	##################################################################################################################

	""" Read the value of  the sensor attached to a certain port. If the port is not valid, it 
	returns -1 """
	def getSensor(self,port):
		# Early return if we can't execute the command because the port is invalid
		if not self.isPortValid(port,3):
			return -1

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
		dial_value    = int(response *DIAL_FACTOR)
		if(dial_value > 100):
			dial_value = 100
		return dial_value
	##################################################################################################################

	""" Read the value of  the dial attached to a certain port"""
	def getVoltage(self, port):
		response 	  = self.getSensor(port)
		voltage_value    = response *VOLTAGE_FACTOR
		return voltage_value
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
			print(CONNECTION_SERVER_CLOSED)
			sys.exit();
		response = response_request.read().decode('utf-8')
		if(response == "Not Connected"):
			print(NO_CONNECTION)
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
			print(CONNECTION_SERVER_CLOSED)
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
			print(CONNECTION_SERVER_CLOSED)
			sys.exit();
		if(response_request.read() == b'200'):
			response = 1
		else :
			response = 0
		return response
	##################################################################################################################
	##################################################################################################################
	##################################################################################################################