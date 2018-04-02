import os, os.path, sys, time

import struct

import ctypes

from ctypes import *

import hidusbrelay as h


vendorId = int("0x16c0", 0)
deviceId = int("0x05DF", 0)
	
CB_TYPE = ctypes.CFUNCTYPE(h.UNCHECKED(c_int), h.USBDEVHANDLE, POINTER(None))

def callback(handle, b):
	print ("in callback")
	
	buf = h.String("                     ")
	buf1 = h.String("")
	
	res = h.usbhidGetVendorString(handle, buf, 17)
	
	print buf
	
	res1 = h.usbhidGetProductString(handle, buf1, 10)
	
	print buf1
	
	reportnum = c_int(0)
	len = c_int(9)
	buf3 = h.String("")
	
	print type(buf3)

	rep = struct.pack('BBBBBBBBB', 0x00, 0xFC, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
	report = h.String(rep)
	
	print type(report)
	print (report.raw[1:2].encode('hex'))
	print (bin(int(report.raw[1:2].encode('hex'), base=16)))
	
	res3 = h.usbhidSetReport(handle, report, 9)
	print res3
	
	res2 = h.usbhidGetReport(handle, reportnum, buf3, byref(len))
	
	if (len != 9) or (buf3[0] != 0):
		print "wrong if condition"
		print "len is {}".format(len.value)
	
	
	print (buf3.raw[:6])
	
	print buf3.raw[8:9].encode('hex')
	
	print (bin(int(buf3.raw[8:9].encode('hex'), base=16)))
	print int(buf3.raw[8:9].encode('hex'), base=16)
	
	h.usbhidCloseDevice(handle);
	
	return 1

cb_func = CB_TYPE(callback)	

print ("about to call")

result = h.usbhidEnumDevices(vendorId, deviceId, 0, cb_func)
print("call ok")
print (result)

print ("Ok")