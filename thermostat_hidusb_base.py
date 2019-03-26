
from ctypes import *

#from ctypes import *
#mylib = CDLL('/usr/local/lib/libhidusb-relay.so')
#mylib.printf
#res = mylib.usb_init()
#print (res)

#print ("should be res above")

#res1 = mylib.usbhidEnumDevices()

#print (res1)

class HIDRelay():

	def __init__(self, settings):

		self.relayHandle = None
		self.usbRelayNum = 0 if not( settings.exists( "thermostat" ) ) else settings.get( "thermostat" )[ "usbRelayNum" ]
		self.usbRelayID = "ABCDE" if not( settings.exists( "thermostat" ) ) else settings.get( "thermostat" )[ "usbRelayId" ]
		
		if (self.opendevice() is False):
			return None
	
				
	def opendevice(self):
		try:
			import hidusbrelay as h
			self.h = h
			CB_TYPE = CFUNCTYPE(self.h.UNCHECKED(c_int), h.USBDEVHANDLE, POINTER(None))
			self.cb_func = CB_TYPE(self.callback)
			vendorId = int("0x16c0", 0)
			deviceId = int("0x05DF", 0)
			result = self.h.usbhidEnumDevices(vendorId, deviceId, 0, self.cb_func)
			
			if (result != 0):
				buffer = self.h.String("")
				self.h.usbhidStrerror_r(result, buffer, c_int(80))
				print ("Error finding USB relay: {0}".format(buffer))
				return False

		except ImportError as e:
			print ("Error loading hidusbrelay: {0}:{1}".format(e.__class__.__name__, e.message)) 
			return False
		
		return True
				
	def callback(self, handle, b):
		self.relayHandle = handle
		return 1	
