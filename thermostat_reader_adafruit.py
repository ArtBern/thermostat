from thermostat_reader import BaseReader

class AdafruitDhtReader(BaseReader):

	def __init__(self):
		import Adafruit_DHT
	
	def read(self):
		rawHumi, rawTemp = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
		
		if (rawHumi is not None and rawHumi < 101) and rawTemp is not None:
			self.lastGoodMeasured = dict(temp=rawTemp,humi=rawHumi,co2=800)
		
		return self.lastGoodMeasured