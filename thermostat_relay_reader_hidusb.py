from thermostat_relay_reader import BaseRelayReader

from ctypes import *

#from ctypes import *
#mylib = CDLL('/usr/local/lib/libhidusb-relay.so')
#mylib.printf
#res = mylib.usb_init()
#print (res)

#print ("should be res above")

#res1 = mylib.usbhidEnumDevices()

#print (res1)

class HIDUSBRelayReader(BaseRelayReader):

	def __init__(self, settings):
		
		try:
			import hidusbrelay as h
			self.h = h
			CB_TYPE = CFUNCTYPE(self.h.UNCHECKED(c_int), h.USBDEVHANDLE, POINTER(None))
			self.cb_func = CB_TYPE(self.callback)
			vendorId = int("0x16c0", 0)
			deviceId = int("0x05DF", 0)
			result = self.h.usbhidEnumDevices(vendorId, deviceId, 0, self.cb_func)

			self.usbRelayNum = 0 if not( settings.exists( "thermostat" ) ) else settings.get( "thermostat" )[ "usbRelayNum" ]		
		except ImportError:
			self.cb_func = None
				

	def callback(self, handle, b):
		self.relayHandle = handle
		return 1	
		
	def read(self):
		reportnum = c_int(0)
		len = c_int(9)
			
		if self.relayHandle is not None:
			buffer = self.h.String("")
			err = self.h.usbhidGetReport(self.relayHandle, reportnum, buffer, byref(len))
			
			if err != 0:
				return -1
			
			#i = 0
			#while (i < 9):
			#	print (buffer.raw[i:i+1])
			#	i = i + 1
			
			intState = int.from_bytes(buffer.raw[8:9], byteorder='little')
			mask = 1 << self.usbRelayNum
			
			return (intState & mask)

		else:
			return -1
		