from thermostat_reader import BaseReader


class AdafruitCCS811Reader(BaseReader):

	def __init__(self):
		
		self.lastGoodMeasured = dict(temp=20,humi=30,co2=800)
		self.temperatureBuffer = CircularBuffer(size=20)
	
		try:
			#installed with 
			#sudo pip3 install adafruit-circuitpython-ccs811
			import board
			import busio
			import adafruit_ccs811
			 
			i2c = busio.I2C(board.SCL, board.SDA)
			ccs811 = adafruit_ccs811.CCS811(i2c)		
			
			# Wait for the sensor to be ready and calibrate the thermistor
			i = 0
			while not ccs811.data_ready and i < 10000:
				i = i + 1
				pass
			
			self.ccs811 = ccs811
			
		except ImportError as e:
			print ("Error loading Adafruit_CCS811: {0}:{1}".format(e.__class__.__name__, e.message)) 
			return None
	
	def read(self):
	
		try:
		
			if self.ccs811 is not None:
			
				self.lastGoodMeasured = dict(temp=self.ccs811.temperature,humi=40,co2=self.ccs811.eco2)
			
			#if (rawHumi is not None and rawHumi < 101) and rawTemp is not None:
			#	self.temperatureBuffer.append(rawTemp)
				#print "@%s, Average: %s" % (self.temperatureBuffer, self.temperatureBuffer.average)
			#	self.lastGoodMeasured = dict(temp=self.temperatureBuffer.average,humi=rawHumi,co2=800)
				
		except OSError as e:
			print ("OSError reading Adafruit_CCS811: {0}:{1}".format(e.__class__.__name__, str(e)))
		except RuntimeError as e:
			print ("RuntimeError reading Adafruit_CCS811: {0}:{1}".format(e.__class__.__name__, str(e)))
		
		return self.lastGoodMeasured
		
from collections import deque

class CircularBuffer(deque):
	def __init__(self, size=0):
		 super(CircularBuffer, self).__init__(maxlen=size)
	@property
	def average(self):
		return sum(self)/len(self)