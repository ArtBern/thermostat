from thermostat_relay_setter import BaseRelaySetter
from thermostat_hidusb_base import HIDRelay

from ctypes import *
import struct

class HIDUSBRelaySetter(BaseRelaySetter, HIDRelay):

	def __init__(self, settings):
		HIDRelay.__init__(self, settings)
		
	def set(self, state):
	
		if self.relayHandle is None:
			if (self.opendevice() is False):
				return -1

		mask = 1 << self.usbRelayNum
		
		# ALL ON=0xFE, ALL OFF=0xFC
		if state :
			bit = 0xFF
		else:
			bit = 0xFD
			
		rep = struct.pack('BBBBBBBBB', 0x00, bit, self.usbRelayNum + 1, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
		
		reportnum = c_int(0)
		len = c_int(9) # report id 1 byte + 8 bytes data 
		
		report = self.h.String(rep)
		res3 = self.h.usbhidSetReport(self.relayHandle, report, 9)
		
		# Read back & verify
		buffer = self.h.String("")
		err = self.h.usbhidGetReport(self.relayHandle, reportnum, buffer, byref(len))
		
		if err != 0:
			errmsg = self.h.String("")
			self.h.usbhidStrerror_r(result, errmsg, c_int(80))
			print ("Error switching USB relay: {0}".format(errmsg))
			return -1
		
		if len != 9 or buffer.raw[8:9] != reportnum:
			#printerr("ERROR: wrong HID report returned! %d\n", len)
			return -2
			
		intState = int.from_bytes(buffer.raw[8:9], byteorder='little')
		
		isSet = mask & intState
		
		return isSet and state
			
			
			
		