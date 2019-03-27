from thermostat_relay_reader import BaseRelayReader
from thermostat_hidusb_base import HIDRelay

from ctypes import *

class HIDUSBRelayReader(BaseRelayReader, HIDRelay):

	def __init__(self, settings):

		HIDRelay.__init__(self, settings)
		
		
	def read(self):
		reportnum = c_int(0)
		len = c_int(9)
		
		if self.relayHandle is None:
			if (self.opendevice() is False):
				return -1
			
		buffer = self.h.String("")
		err = self.h.usbhidGetReport(self.relayHandle, reportnum, buffer, byref(len))
		
		if err != 0:
			errmsg = self.h.String("")
			self.h.usbhidStrerror_r(result, errmsg, c_int(80))
			print ("Error reading USB relay: {0}".format(errmsg))
			return -1
		
		#i = 0
		#while (i < 9):
		#	print (buffer.raw[i:i+1])
		#	i = i + 1
		
		intState = int.from_bytes(buffer.raw[8:9], byteorder='little')
		mask = 1 << self.usbRelayNum
		
		return (intState & mask)
		