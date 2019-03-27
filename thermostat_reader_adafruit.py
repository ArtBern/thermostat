from thermostat_reader import BaseReader

class AdafruitDhtReader(BaseReader):

	def __init__(self):
		
		self.lastGoodMeasured = dict(temp=20,humi=30,co2=800)
		self.temperatureBuffer = CircularBuffer(size=20)
	
		try:
			import Adafruit_DHT
		except ImportError as e:
			print ("Error loading Adafruit_DHT: {0}:{1}".format(e.__class__.__name__, e.message)) 
			return None
	
	def read(self):
	
		try:
			rawHumi, rawTemp = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
			
			if (rawHumi is not None and rawHumi < 101) and rawTemp is not None:
				self.temperatureBuffer.append(rawTemp)
				#print "@%s, Average: %s" % (self.temperatureBuffer, self.temperatureBuffer.average)
				self.lastGoodMeasured = dict(temp=self.temperatureBuffer.average,humi=rawHumi,co2=800)
				
		except ImportError as e:
			print ("Error reading Adafruit_DHT: {0}:{1}".format(e.__class__.__name__, e.message)) 
		
		return self.lastGoodMeasured
		
from collections import deque

class CircularBuffer(deque):
	def __init__(self, size=0):
		 super(CircularBuffer, self).__init__(maxlen=size)
	@property
	def average(self):
		return sum(self)/len(self)