#!/bin/env python2

import sys

def barr2i(bytes):
	return bytes[0] + 256*bytes[1] + 256*256*bytes[2] + 256*256*256*bytes[3]

def show_row(bytes):
	print "\t\t0x%.2x, 0x%.2x,   /*  %.8s%s  */" %(bytes[0], bytes[1], (bin(bytes[0]) + '0'*10)[2:10], (bin(bytes[1]) + '0'*10)[2:w-6])

def show_glyph(bytes, size):
	for i in range(0, size/2):
		show_row(bytes[2*i : 2*(i+1)])

if __name__ == '__main__':
	f = open(sys.argv[1])
	bytes = [ord(x) for x in f.read()]

	#print "Magic: %.2x %.2x %.2x %.2x" %(bytes[0], bytes[1], bytes[2], bytes[3])
	#print "Version: %d" %(barr2i(bytes[4:8]))
	#print "Offset: %d" %(barr2i(bytes[8:12]))
	#print "Flags: %d" %(barr2i(bytes[12:16]))
	#print "Length: %d" %(barr2i(bytes[16:20]))
	#print "Charsize: %d" %(barr2i(bytes[20:24]))
	#print "Height: %d" %(barr2i(bytes[24:28]))
	#print "Width: %d" %(barr2i(bytes[28:32]))

	n = barr2i(bytes[8:12])
	w = barr2i(bytes[28:32])
	chsize = barr2i(bytes[20:24])

	print "#include <linux/font.h>\n"
	print "#define FONTDATAMAX 12288\n"
	print "static const unsigned char fontdata_ter12x24[FONTDATAMAX] = {"

	for i in range(0, 256):
		print "\t\t/* %d 0x%.2x '%c' */" %(i, i, chr(i) if '\n' != chr(i) else 'n')
		show_glyph(bytes[n+chsize*i:n+chsize*(i+1)], chsize)
		print "\n\n"

	print "};\n\n"

	print "const struct font_desc font_ter_12x24 = {"
	print "\t\t.idx	= TER12x22_IDX,"
	print "\t\t.name	= \"TER12x22\","
	print "\t\t.width	= 12,"
	print "\t\t.height	= 24,"
	print "\t\t.data	= fontdata_ter12x24,"
	print "#ifdef __sparc__"
	print "\t\t.pref	= 5,"
	print "#else"
	print "\t\t.pref	= -1,"
	print "#endif"
	print "};"
