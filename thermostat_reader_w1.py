from thermostat_reader import BaseReader

class W1Reader(BaseReader):

	def __init__(self):
		from w1thermsensor import W1ThermSensor
		self.tempSensor = W1ThermSensor()
		#sensorUnits	= W1ThermSensor.DEGREES_C if tempScale == "metric" else W1ThermSensor.DEGREES_F
		self.sensorUnits	= W1ThermSensor.DEGREES_C if True else W1ThermSensor.DEGREES_F
	
	def read(self):
		return dict(temp=self.tempSensor.get_temperature( self.sensorUnits ),humi=30,co2=800)