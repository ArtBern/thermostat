import os                           

ZLIB_INC_DIR = "/usr/include"       
ZLIB_LIB_DIR = "/usr/local/lib"       
ZLIB_LIB = "libhidusb-relay.so"       
ZLIB_HEADERS = "/opt/openwrt-artbern/pavelusb/src/hiddata.h"       

# Set location of ctypesgen.py                                      
ctypesgen_path = 'ctypesgen/ctypesgen.py'                                       

wrapper_filename = 'hidusbrelay.py'
cmd = "LD_LIBRARY_PATH={} {} -I {} -L {} -l {} {} -o {}".format(             
ZLIB_LIB_DIR, ctypesgen_path, ZLIB_INC_DIR, ZLIB_LIB_DIR, ZLIB_LIB,      
ZLIB_HEADERS, wrapper_filename)                                        

print(cmd)
os.system(cmd) 