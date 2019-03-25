from thermostat_relay_reader import BaseRelayReader

class GPIORelayReader(BaseRelayReader):

	def __init__(self, settings):
		
		import RPi.GPIO as GPIO
		
		self.GPIO = GPIO
		
		self.heatPin = 23 if not( settings.exists( "thermostat" ) ) else settings.get( "thermostat" )[ "heatPin" ]
		
		self.GPIO.setmode( self.GPIO.BCM )
		self.GPIO.setup( self.heatPin, self.GPIO.OUT )
		self.GPIO.output( self.heatPin, self.GPIO.LOW )
		
	def read(self):
		return self.GPIO.input( self.heatPin )