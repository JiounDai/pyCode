#!/usr/bin/env python

import sys
import binascii

print '--- str2hex : AAAA to 41414141'
print '--- hex2str : 41414141 to AAAA'
print '--- str2x   : AAAA to \\x41\\x41\\x41\\x41'
print '--- x2str   : \\x41\\x41\\x41\\x41 to AAAA'
print '--- hex2x   : 41414141 to \\x41\\x41\\x41\\x41'
print '--- x2hex   : \\x41\\x41\\x41\\x41 to 41414141'
print "\n"

arg1 = sys.argv[1]
data = str(sys.argv[2])


if arg1 == "str2hex":
	print binascii.hexlify(data)

elif arg1 == "hex2str":
	print binascii.unhexlify(data)

elif arg1 == "str2x":
	hex_str = binascii.hexlify(data)
	length = len(hex_str)
	xstr = ""
	for i in range(0,length,2):
		xstr += "\\x" + hex_str[i : i+2]

	print xstr

elif arg1 == "x2str":
	str_a = data.replace("\\x",'')
	print binascii.unhexlify(str_a)

elif arg1 == "hex2x":
	length = len(data)
	xstr = ""
	for i in range(0,length,2):
		xstr += "\\x" + data[i : i+2]

	print xstr

elif arg1 == "x2hex":
	str_a = data.replace("\\x",'')
	print str_a

else:
	print "input converttt type error !"
