from thermostat_relay_setter import BaseRelaySetter

from ctypes import *
import struct

class HIDUSBRelaySetter(BaseRelaySetter):

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
		
	def set(self, state):
	
		mask = 1 << self.usbRelayNum
		
		# ALL ON=0xFE, ALL OFF=0xFC
		if state :
			bit = 0xFF
		else:
			bit = 0xFD
			
		rep = struct.pack('BBBBBBBBB', 0x00, bit, self.usbRelayNum + 1, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
		
		reportnum = c_int(0)
		len = c_int(9) # report id 1 byte + 8 bytes data 
		
		if self.relayHandle is not None:

			report = self.h.String(rep)
			res3 = self.h.usbhidSetReport(self.relayHandle, report, 9)
			
			# Read back & verify
			buffer = self.h.String("")
			err = self.h.usbhidGetReport(self.relayHandle, reportnum, buffer, byref(len))
			
			if err != 0:
				return -1
			
			if len != 9 or buffer.raw[8:9] != reportnum:
				#printerr("ERROR: wrong HID report returned! %d\n", len)
				return -2
				
			intState = int.from_bytes(buffer.raw[8:9], byteorder='little')
			
			isSet = mask & intState
			
			return isSet and state
			
			
			
		